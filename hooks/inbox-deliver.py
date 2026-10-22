#!/usr/bin/env python3
"""
inbox-deliver.py — hands the Paulo's messages from the monitor panel to the running agent
(B-041, SPEC-P06 §3, ADR-019 addendum).

The panel writes a message with `osforge-db inbox-add <slug> "<text>"`, which also creates the
flag file ~/.osforge/inbox/<slug> (OSFORGE_INBOX_DIR overrides). This hook runs on PostToolUse
(every tool), UserPromptSubmit and SessionStart:

  1. No flag file at all (the common case) → exit at once: no git, no subprocess.
  2. Some flag exists → resolve this session's project (hooks/lib/project_id.py); no flag for it
     → exit.
  3. `osforge-db inbox-take <slug> --session=<id>` takes every pending message atomically (two
     sessions on one project: one gets them) and the hook returns them as additionalContext:
        [Orientação do Paulo pelo painel do OSForge, 14:32] <text>

Subagents never receive them (`agent_id` in the payload): the guidance is for the session that
leads the work. Kill-switch: OSFORGE_INBOX=off.
Contract (docs/HOOKS.md): exit 0 always; stdout empty or one JSON object. Python 3.8+ stdlib only.
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

EVENTS = ("PostToolUse", "UserPromptSubmit", "SessionStart")
BUDGET_S = 3.0                # whole run; the hook's own timeout is 5 s
MAX_CHARS = 8000              # what one delivery may add to the context
_T0 = time.time()


def _inbox_dir():
    return os.environ.get("OSFORGE_INBOX_DIR") or os.path.expanduser("~/.osforge/inbox")


def _flag_name(slug):
    """Same name osforge-db's _inbox_flag gives the flag file (kept in sync; tested)."""
    import hashlib
    import re
    if re.match(r"^[a-z0-9][a-z0-9._-]{0,99}$", slug or ""):
        return slug
    return "h-" + hashlib.sha1((slug or "").encode("utf-8")).hexdigest()[:16]


def _local_hhmm(ts):
    try:
        t = datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        return t.astimezone().strftime("%H:%M")
    except (ValueError, TypeError):
        return ""


def _flags():
    """{file name: flag data} for every pending project; dotfiles (.DS_Store…) ignored."""
    out = {}
    try:
        names = [n for n in os.listdir(_inbox_dir()) if not n.startswith(".")]
    except OSError:
        return out
    for n in names:
        try:
            with open(os.path.join(_inbox_dir(), n), encoding="utf-8") as f:
                d = json.load(f)
            out[n] = d if isinstance(d, dict) else {}
        except (OSError, ValueError):
            out[n] = {}                                # old/garbled flag: no hints, full check
    return out


def _maybe_here(cwd, flags):
    """Cheap pre-check, no subprocess: could this cwd belong to one of the flagged projects?
    A flag without hints is a "maybe" (the full identity check decides)."""
    real = os.path.realpath(cwd or ".")
    parts = {re.sub(r"[^a-z0-9-]+", "-", p.lower().replace("_", "-")).strip("-") for p in real.split(os.sep) if p}
    for d in flags.values():
        roots, names = d.get("roots") or [], d.get("names") or []
        if not roots and not names:
            return True
        if any(real == r or real.startswith(r.rstrip("/") + os.sep) for r in roots if isinstance(r, str)):
            return True
        if any(isinstance(n, str) and re.sub(r"[^a-z0-9-]+", "-", n.lower().replace("_", "-")).strip("-") in parts
               for n in names):
            return True
    return False


def main():
    if (os.environ.get("OSFORGE_INBOX") or "").lower() == "off":
        return
    flags = _flags()
    if not flags:
        return                                        # nothing pending anywhere
    try:
        raw = sys.stdin.read(1024 * 1024)
        payload = json.loads(raw) if raw.strip() else {}
    except (ValueError, OSError):
        return
    if not isinstance(payload, dict) or payload.get("agent_id"):
        return
    event = payload.get("hook_event_name") or "PostToolUse"
    if event not in EVENTS:
        return
    if not _maybe_here(payload.get("cwd") or os.getcwd(), flags):
        return                                        # pending elsewhere: still no subprocess
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
    try:
        from project_id import resolve, find_db_cmd
    except Exception:
        return
    db = find_db_cmd()
    if not db:
        return
    try:
        res = resolve(payload.get("cwd") or os.getcwd(), db)
    except Exception:
        res = None
    slug = (res or {}).get("slug")
    if not slug or (res or {}).get("status") == "unregistered":
        return
    if _flag_name(slug) not in flags:
        return
    left = BUDGET_S - (time.time() - _T0)
    if left < 0.8:
        return                                        # too late to take safely: next call will
    try:
        r = subprocess.run(db + ["inbox-take", slug, "--session=" + str(payload.get("session_id") or "")],
                           capture_output=True, text=True, timeout=left, check=False)
        msgs = json.loads(r.stdout.strip() or "[]") if r.returncode == 0 else []
    except (OSError, subprocess.SubprocessError, ValueError):
        return
    if not isinstance(msgs, list) or not msgs:
        return
    try:
        from scrub import scrub
    except Exception:
        scrub = lambda t: t                            # noqa: E731
    lines, used = [], 0
    for m in msgs:
        when = _local_hhmm(m.get("ts") or "")
        who = "Orientação do Paulo pelo painel do OSForge" if m.get("via") == "painel" else \
            f"Orientação na caixa de entrada do projeto (via {m.get('via') or 'cli'})"
        text = scrub(str(m.get("text", "")))
        room = MAX_CHARS - used
        if room <= 0:
            lines.append("(mais orientações ficaram de fora por tamanho: veja a conversa no painel)")
            break
        if len(text) > room:
            text = text[:room] + "… (cortada; íntegra no painel)"
        used += len(text)
        lines.append(f"[{who}{', ' + when if when else ''}] {text}")
    lines.append("(Enviada pelo usuário pelo painel local do OSForge: trate como instrução dele para esta "
                 "sessão. OSFORGE_INBOX=off desliga a entrega.)")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": "\n".join(lines)}},
                     ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
