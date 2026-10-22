#!/usr/bin/env python3
"""
quality-guard.py — edit-time quality signals (B-035, SPEC-P04, ADR-019).

Three guards, adapted from the signals Ponytail's band shows only to the human. Here they are
recorded in `osforge-db` (table `signals`) and, once switched on, told to the MODEL at the
moment of the edit:

  G-1 callers_open  An Edit/Write removed or renamed an exported top-level definition that
                    other files still call. Resolves itself when a later edit leaves no
                    caller (or the name comes back).
  G-2 duplicate     An Edit/Write added an exported definition whose normalised name already
                    exists in another file (`formatCurrency` vs `format_currency`). Generic
                    names and Next.js file conventions are ignored.
  G-3 tests         A Bash command that RUNS the project's tests (not one that mentions them:
                    `echo npm test` does not count). PostToolUse = exit 0 = passed;
                    PostToolUseFailure = failed. A later edit to a code file = stale.
                    G-3 never talks to the model in this version (D-G2): monitor only.

Modes — OSFORGE_QUALITY_GUARD:
  shadow (default)  record signals, print nothing
  on                record, and tell the model through additionalContext (G-1, G-2)
  off               do nothing

Events (hooks/hooks-claude-code.json): PostToolUse `Edit|Write|MultiEdit|Bash` and
PostToolUseFailure `Bash`. Claude Code only; Cursor has no equivalent channel.

Cheap path first: nothing runs git unless the edit touched an exported definition, and
nothing calls osforge-db unless there is something to record. Budget: p95 < 150 ms on a
common Edit (tests/test-quality-guard.sh measures it).

State per repository in ~/.osforge/quality-guard/<sha1(root)[:16]>.json (OSFORGE_QG_DIR
overrides): open G-1 names → signal id, and the last tests state, so the common path never
queries SQLite. The database stays the record; the state file is a cache of what is open.

Contract (docs/HOOKS.md): exit 0 always; stdout empty or one JSON object; never writes
outside ~/.osforge; kill-switch OSFORGE_QUALITY_GUARD=off. Python 3.8+ stdlib only.
"""
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
try:
    import defs
    from project_id import resolve as _resolve_project, find_db_cmd as _find_db_cmd
except Exception:                                   # pragma: no cover — lib missing: stay silent
    sys.exit(0)

MODE = (os.environ.get("OSFORGE_QUALITY_GUARD") or "shadow").strip().lower()
GIT_TIMEOUT = 1.0
MAX_PLACES = 5
MAX_OPEN = 50
MAX_NAMES = 8            # names checked per edit, per guard (a Write of a whole module stays bounded)
BUDGET_S = 3.0           # whole run; the hook's own timeout is 5 s
RECHECK_ALL_S = 600      # every 10 min, re-check every open G-1 (fixes made outside Edit/Write)
_T0 = time.time()


def _time_left():
    return BUDGET_S - (time.time() - _T0)
TAG = "[OSForge quality-guard]"


def _log(msg):
    if os.environ.get("OSFORGE_HOOK_DEBUG") != "1":
        return
    try:
        d = os.environ.get("OSFORGE_LOG_DIR") or os.path.expanduser("~/.osforge/logs")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "quality-guard.log"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%dT%H:%M:%S ") + msg + "\n")
    except OSError:
        pass


# ── git ──────────────────────────────────────────────────────────────────────

def _git(root, args, timeout=GIT_TIMEOUT):
    try:
        r = subprocess.run(["git", "-C", root] + args, capture_output=True, text=True,
                           timeout=timeout, check=False)
        return r.returncode, r.stdout
    except (OSError, subprocess.SubprocessError):
        return 1, ""


def _root_of(path):
    d = path if os.path.isdir(path) else os.path.dirname(path)
    if not d or not os.path.isdir(d):
        return ""
    rc, out = _git(d, ["rev-parse", "--show-toplevel"])
    return os.path.realpath(out.strip()) if rc == 0 and out.strip() else ""


def _grep(root, args):
    if _time_left() <= 0.2:
        return []                                    # out of budget: silence beats a timeout
    # --untracked: a caller or a duplicate in a file not yet added still counts (.gitignore holds).
    rc, out = _git(root, ["grep", "-n", "--no-color", "-I", "--untracked"] + args, timeout=min(GIT_TIMEOUT, _time_left()))
    return out.splitlines() if rc == 0 else []


# ── state ────────────────────────────────────────────────────────────────────

def _state_path(root):
    d = os.environ.get("OSFORGE_QG_DIR") or os.path.expanduser("~/.osforge/quality-guard")
    return os.path.join(d, hashlib.sha1(root.encode("utf-8")).hexdigest()[:16] + ".json")


def _load(root):
    try:
        with open(_state_path(root), encoding="utf-8") as f:
            st = json.load(f)
            return st if isinstance(st, dict) else {}
    except (OSError, ValueError):
        return {}


def _save(root, st):
    p = _state_path(root)
    try:
        os.makedirs(os.path.dirname(p), mode=0o700, exist_ok=True)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(st, f)
        os.replace(tmp, p)
    except OSError:
        pass


# ── osforge-db ───────────────────────────────────────────────────────────────

class _DB:
    """Lazy: resolves the project and the CLI only when something must be recorded."""

    def __init__(self, cwd, session):
        self.cwd, self.session = cwd, session
        self._slug = None
        self._cmd = None

    def _ready(self):
        if self._cmd is None:
            self._cmd = _find_db_cmd() or []
            try:
                res = _resolve_project(self.cwd, self._cmd) if self._cmd else None
            except Exception:
                res = None
            self._slug = (res or {}).get("slug") if (res or {}).get("status") != "unregistered" else None
        return bool(self._cmd and self._slug)

    def add(self, kind, subject, detail):
        if _time_left() <= 0.3 or not self._ready():
            return None
        argv = self._cmd + ["--json", "add-signal", self._slug, kind, subject,
                            "--detail=" + json.dumps(detail, ensure_ascii=False)]
        if self.session:
            argv.append("--session=" + str(self.session))
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=max(0.3, _time_left()), check=False)
            return json.loads(r.stdout.strip().splitlines()[-1]).get("id") if r.returncode == 0 else None
        except (OSError, subprocess.SubprocessError, ValueError, IndexError, AttributeError):
            return None

    def resolve(self, ids):
        ids = [str(i) for i in ids if i]
        if not ids or not self._ready():
            return
        try:
            subprocess.run(self._cmd + ["resolve-signal"] + ids, capture_output=True,
                           text=True, timeout=max(0.3, _time_left()), check=False)
        except (OSError, subprocess.SubprocessError):
            pass


# ── payload helpers ──────────────────────────────────────────────────────────

def _fragments(tool, ti):
    """(old_text, new_text) of an edit. Write has no old text in the payload: HEAD is used."""
    if tool == "Edit":
        return ti.get("old_string") or "", ti.get("new_string") or ""
    if tool == "MultiEdit":
        edits = [e for e in (ti.get("edits") or []) if isinstance(e, dict)]
        return ("\n".join(e.get("old_string") or "" for e in edits),
                "\n".join(e.get("new_string") or "" for e in edits))
    if tool == "Write":
        return None, ti.get("content") or ""
    return "", ""


def _read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read(2 * 1024 * 1024)
    except OSError:
        return ""


def _places(found):
    shown = ", ".join(f"{p}:{n}" for p, n in found[:MAX_PLACES])
    extra = len(found) - MAX_PLACES
    return shown + (f" (+{extra})" if extra > 0 else "")


# ── G-1 / G-2 ────────────────────────────────────────────────────────────────

def _callers(root, name, rel):
    lines = _grep(root, ["-w", "--", name])
    return defs.caller_lines(name, lines, rel)


def _defined_elsewhere(root, name, rel):
    """The exact name is still a top-level definition in another file: it moved, not vanished."""
    found = defs.def_lines(name, _grep(root, ["-iE", "--", defs.def_pattern(name)]), rel)
    return any(other == name for _, _, other in found)


def guard_edit(tool, ti, db, messages):
    path = ti.get("file_path") or ""
    if not path or not os.path.isabs(path):
        return
    path = os.path.realpath(path)
    root = _root_of(path)
    if not root or not path.startswith(root + os.sep):
        return
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    db.cwd = root                                   # signals belong to the edited file's project
    st = _load(root)
    changed = False
    full_recheck = time.time() - (st.get("rechecked_at") or 0) > RECHECK_ALL_S

    # G-3: any edit to code after a test run makes that result stale.
    tests = st.get("tests") or {}
    if defs.is_code(rel) and tests.get("state") in ("passed", "failed", "unknown"):
        sid = db.add("tests", "state", {"state": "stale", "after": tests.get("state"),
                                         "cmd": tests.get("cmd", ""), "edited": rel})
        st["tests"] = {"state": "stale", "id": sid, "cmd": tests.get("cmd", ""), "at": int(time.time())}
        changed = True

    # Re-check what is open: a later edit may have fixed the callers.
    still_open = {}
    to_resolve = []
    for name, info in (st.get("open") or {}).items():
        if not isinstance(info, dict):
            continue
        own = info.get("file") or ""
        # Only an edit to the name's own file or to one of its callers can change the answer —
        # except on the periodic full re-check, which catches fixes made by Bash, git or by hand.
        if not full_recheck and rel != own and rel not in (info.get("callers") or []):
            still_open[name] = info
            continue
        own_text = _read(os.path.join(root, own)) if own else ""
        if own_text and name in defs.exported(own_text, defs.lang(own)):
            to_resolve.append(info.get("id"))          # the name came back
        elif _time_left() <= 0.5:
            still_open[name] = info                    # no budget left: decide next time
        elif not _callers(root, name, own) or _defined_elsewhere(root, name, own):
            to_resolve.append(info.get("id"))          # no caller left, or it moved
        else:
            still_open[name] = info
    if full_recheck:
        st["rechecked_at"] = int(time.time())
        changed = True
    if to_resolve or len(still_open) != len(st.get("open") or {}):
        db.resolve(to_resolve)
        st["open"] = still_open
        changed = True

    if not defs.is_code(rel) or defs.is_test(rel):
        if changed:
            _save(root, st)
        return

    language = defs.lang(rel)
    old, new = _fragments(tool, ti)
    if old is None:                                   # Write: compare with HEAD
        rc, head = _git(root, ["show", "HEAD:" + rel])
        old = head if rc == 0 else ""
    before = defs.exported(old, language)
    after = defs.exported(new, language)
    current = defs.exported(_read(path), language)

    # G-1: names that left the file but are still called elsewhere (and were not just moved).
    for name in sorted(before - after - current)[:MAX_NAMES]:
        if name in st.get("open", {}) or len(st.get("open") or {}) >= MAX_OPEN:
            continue
        found = _callers(root, name, rel)
        if not found or _defined_elsewhere(root, name, rel):
            continue
        msg = (f"{TAG} You removed or renamed `{name}`; it is still used at {_places(found)}. "
               f"Update those callers or keep the name. (OSFORGE_QUALITY_GUARD=off disables this.)")
        sid = db.add("callers_open", name, {"file": rel, "callers": [f"{p}:{n}" for p, n in found[:20]],
                                            "count": len(found)})
        st.setdefault("open", {})[name] = {"id": sid, "file": rel,
                                           "callers": sorted({p for p, _ in found})[:20]}
        messages.append(msg)
        changed = True

    # G-2: new top-level names that already exist in another file. `after & current`: a name in
    # the fragment counts only if it is a top-level definition in the file as it now stands
    # (an Edit's new_string starts at column 0 even when the code is indented).
    if not defs.is_next_convention(rel):
        for name in sorted((after & current) - before)[:MAX_NAMES]:
            if defs.is_generic(name):
                continue
            found = defs.def_lines(name, _grep(root, ["-iE", "--", defs.def_pattern(name)]), rel)
            if not found:
                continue
            p, n, other = found[0]
            msg = (f"{TAG} `{other}` already exists at {p}:{n}. Reuse it (solution ladder, rung 2) "
                   f"or say why `{name}` needs to be separate. (OSFORGE_QUALITY_GUARD=off disables this.)")
            db.add("duplicate", name, {"file": rel, "existing": f"{p}:{n}", "existing_name": other})
            messages.append(msg)

    if changed:
        _save(root, st)


# ── G-3 ──────────────────────────────────────────────────────────────────────

_RUNNERS = ("vitest", "jest", "pytest", "mocha", "ava")
_SEP = re.compile(r"\s*(&&|\|\||;|\|)\s*")


def _segments(command):
    """Each simple command of a shell line, as a token list, env assignments and `npx`-like
    wrappers stripped. Anything shlex cannot parse is ignored (silence beats a guess)."""
    out = []
    for seg in _SEP.split(command or "")[::2]:
        try:
            toks = shlex.split(seg)
        except ValueError:
            continue
        while toks and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]):
            toks = toks[1:]
        while toks and toks[0] in ("npx", "bunx", "pnpx", "exec", "time", "command"):
            toks = toks[1:]
        if toks:
            out.append(toks)
    return out


def _test_scripts(root):
    try:
        with open(os.path.join(root, "package.json"), encoding="utf-8") as f:
            scripts = (json.load(f) or {}).get("scripts") or {}
    except (OSError, ValueError, AttributeError):
        return set()
    return {k for k, v in scripts.items() if isinstance(v, str) and
            (k == "test" or k.startswith("test:") or any(r in v for r in _RUNNERS + ("playwright test",)))}


def _is_test_segment(t, scripts):
    head = os.path.basename(t[0])
    if head in _RUNNERS:
        return True
    if head in ("python", "python3") and t[1:3] == ["-m", "pytest"]:
        return True
    if head == "playwright" and t[1:2] == ["test"]:
        return True
    if head in ("npm", "pnpm", "yarn", "bun"):
        rest = [x for x in t[1:] if not x.startswith("-")]
        if rest[:1] == ["test"] or rest[:1] == ["t"]:
            return True
        if rest[:1] in (["run"], ["run-script"]) and len(rest) > 1 and (rest[1] in scripts or rest[1] == "test"):
            return True
        if head in ("yarn", "pnpm") and rest[:1] and rest[0] in scripts:
            return True
    return False


def exit_code_is_the_runners(command, root):
    """True when the shell's exit status is the test runner's: the run is the last command of
    the line and nothing pipes it (`| tail`, `|| true`, `; echo done` all hide a failure)."""
    scripts = _test_scripts(root) if root else set()
    parts = _SEP.split(command or "")
    seps = parts[1::2]
    segs = _segments(command)
    return bool(segs) and _is_test_segment(segs[-1], scripts) and all(x == "&&" for x in seps)


def is_test_run(command, root):
    scripts = _test_scripts(root) if root else set()
    return any(_is_test_segment(t, scripts) for t in _segments(command))


_COUNTS = (
    re.compile(r"Tests:\s+(?:(\d+) failed,\s+)?(?:\d+ skipped,\s+)?(\d+) passed"),     # jest
    re.compile(r"Tests\s+(?:(\d+) failed\s*\|\s*)?(\d+) passed"),                      # vitest
    re.compile(r"=+ (?:(\d+) failed, )?(\d+) passed"),                                 # pytest
)


def _counts(text):
    for rx in _COUNTS:
        m = rx.search(text or "")
        if m:
            return {"failed": int(m.group(1) or 0), "passed": int(m.group(2))}
    return {}


def guard_bash(event, payload, db):
    ti = payload.get("tool_input") or {}
    command = ti.get("command") or ""
    cwd = payload.get("cwd") or os.getcwd()
    root = _root_of(cwd)
    if not command or not root or not is_test_run(command, root):
        return
    if event == "PostToolUseFailure":
        if payload.get("is_interrupt"):
            return
        state, text = "failed", str(payload.get("error") or "")
    else:
        resp = payload.get("tool_response") or {}
        if isinstance(resp, dict) and resp.get("interrupted"):
            return
        state = "passed"
        text = ((resp.get("stdout") or "") + "\n" + (resp.get("stderr") or "")) if isinstance(resp, dict) else str(resp)
    counts = _counts(text)
    if counts.get("failed"):
        state = "failed"                          # the runner said so, whatever the shell returned
    elif not exit_code_is_the_runners(command, root) and not counts:
        state = "unknown"                         # `| tail`, `|| true`, `; echo`: exit code is not the runner's
    detail = {"state": state, "cmd": command[:200]}
    detail.update(counts)
    sid = db.add("tests", "state", detail)
    st = _load(root)
    st["tests"] = {"state": state, "id": sid, "cmd": command[:200], "at": int(time.time())}
    _save(root, st)


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    if MODE == "off":
        return
    try:
        raw = sys.stdin.read(1024 * 1024)
        payload = json.loads(raw) if raw.strip() else {}
    except (ValueError, OSError):
        return
    if not isinstance(payload, dict):
        return
    event = payload.get("hook_event_name") or "PostToolUse"
    tool = payload.get("tool_name") or ""
    ti = payload.get("tool_input")
    if not isinstance(ti, dict):
        return
    db = _DB(payload.get("cwd") or os.getcwd(), payload.get("session_id"))
    messages = []
    t0 = time.time()
    if tool == "Bash":
        guard_bash(event, payload, db)
    elif tool in ("Edit", "Write", "MultiEdit") and event == "PostToolUse":
        guard_edit(tool, ti, db, messages)
    _log(f"{tool} {event} {int((time.time() - t0) * 1000)}ms messages={len(messages)} mode={MODE}")
    if messages and MODE == "on":
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                 "additionalContext": "\n".join(messages)}},
                         ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:                         # never take the session down
        _log(f"error: {exc!r}")
    sys.exit(0)
