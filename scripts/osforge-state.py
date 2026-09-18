#!/usr/bin/env python3
"""
osforge-state.py — the deploy's memory (B-014/B-015/B-016, ADR-015).

Before this file, `deploy.sh` could not tell a file it had written from a file the user
had put there, so it overwrote same-name agents without backup, deleted user skills with
`rsync --delete`, unregistered user hooks stored under ~/.claude/hooks/ and clobbered its
own settings.json backup (audit E-A27–E-A30). Everything the deploy writes is now recorded
in ONE state file with a SHA-256 per file, and every later run consults it.

State file: $OSFORGE_STATE_FILE, else ~/.osforge/install-state.json  (schema osforge.install.v1)
Backups:    ~/.claude_backups/<run_id>/<path relative to HOME>   (never overwritten)

Subcommands (all stdlib, all exit 0 on success, 1 on failure or refusal)
  apply    --manifest FILE --run-id ID --version V --repo R --commit C [--dry-run] [--force] [--adopt]
           Manifest: one JSON object per line
             {"src": ..., "dst": ..., "critical": bool, "executable": bool, "origin": "repo/relative/path"}
           Rules per file, in this order:
             dst missing                                  → copy, record
             dst == src (hash)                             → record (adopt), nothing written
             dst recorded and unmodified since (hash==rec) → overwrite, record
             dst recorded but user modified it             → backup, KEEP user's file, warn
                                                             (--force: backup, overwrite)
             dst not recorded, differs, but equals an older
               git revision of `origin` in --repo          → overwrite, record (legacy deploy wrote it)
             dst not recorded and differs from src         → skip, warn: user-owned
                                                             (--adopt: backup, overwrite, record)
           Files recorded in a previous run and absent from this manifest are PRUNED —
           only if their current hash still equals the recorded one; otherwise retained + warned.
  merge-hooks    --hooks FILE --settings FILE --run-id ID [--dry-run] [--force-hooks]
           Id-keyed, three-way: each managed group is identified by event|matcher|basename(cmd).
           Managed groups are replaced only if they still equal what was recorded; a group the
           user edited aborts the deploy with a diff. User groups are never touched. Groups of
           events the repo dropped are removed. First run adopts groups whose command is one of
           this repo's hook scripts.
  merge-settings --base FILE --settings FILE [--dry-run]
           settings-base.json → settings.json (top-level keys, env key-by-key, `_unset` paths),
           recording each key's previous value the first time it is set.
  record-mcps    --names a,b,c              Remember MCP servers the deploy added to ~/.claude.json.
  doctor         Report missing / drifted files and drifted hooks. Exit 1 if any.
  uninstall      [--dry-run]  Delete recorded files whose hash still matches; retain the rest and
           list them; remove managed hooks that still equal the recorded entry; restore previous
           settings values; remove recorded MCP servers; delete the state file.
  restore  --run-id ID [--dry-run]   Copy that run's backups back into place.
  status         Print a one-screen summary.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

SCHEMA = "osforge.install.v1"
HOME = os.path.expanduser("~")
STATE_FILE = os.environ.get("OSFORGE_STATE_FILE") or os.path.join(HOME, ".osforge", "install-state.json")
BACKUP_ROOT = os.environ.get("OSFORGE_BACKUP_DIR") or os.path.join(HOME, ".claude_backups")
# Scripts this repo ships as hooks; used only to ADOPT pre-state hook groups on the first run.
OWN_HOOK_SCRIPTS = {"canvas-autostart.sh", "session-resume.sh", "gateguard.py", "protect-tests.sh",
                    "observe-capture.py", "scan-secrets.sh", "scan-secrets.py", "notify-done.sh",
                    "session-save.py", "route-guard.py", "canvas-feedback.py", "context-threshold.py"}


# ── helpers ──────────────────────────────────────────────────────────────────

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def expand(p):
    return os.path.expanduser(os.path.expandvars(p))


def rel_home(path):
    path = os.path.abspath(path)
    return os.path.relpath(path, HOME) if path.startswith(HOME + os.sep) else path.lstrip(os.sep)


def load_state():
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            st = json.load(f)
        if st.get("schema") != SCHEMA:
            fail(f"state file {STATE_FILE} has schema {st.get('schema')!r}, expected {SCHEMA!r}")
        return st
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        fail(f"state file {STATE_FILE} is not valid JSON ({exc}); refusing to guess")


def empty_state(run_id, version, repo, commit):
    return {"schema": SCHEMA, "version": version, "repo": repo, "commit": commit, "run_id": run_id,
            "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "files": {}, "hooks": {}, "settings": {}, "mcps": []}


def save_state(st):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2, ensure_ascii=False, sort_keys=True)
    os.replace(tmp, STATE_FILE)


def atomic_write_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".osforge-", dir=os.path.dirname(path) or ".")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def backup(path, run_id, dry):
    """Copy `path` to the run's backup dir; never overwrites; returns the backup path."""
    if not os.path.isfile(path):
        return None
    dst = os.path.join(BACKUP_ROOT, run_id, rel_home(path))
    if os.path.exists(dst):
        return dst
    if not dry:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
    return dst


_HIST_CACHE = {}


def known_old_version(repo, origin, cur_hash, max_commits=300):
    """Return the short commit where `origin` (repo-relative path) had content `cur_hash`,
    or None. Used to recognise files a LEGACY deploy wrote before install-state existed:
    they are OSForge's, just stale — not the user's. Fail-soft when git is unavailable."""
    if not repo or not origin or not os.path.isdir(os.path.join(repo, ".git")):
        return None
    key = (repo, origin)
    if key not in _HIST_CACHE:
        table = {}
        try:
            out = subprocess.run(["git", "-C", repo, "log", f"-n{max_commits}", "--format=%H", "--", origin],
                                 capture_output=True, text=True, timeout=20, check=False).stdout.split()
            seen_blobs = set()
            for commit in out:
                blob = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "-q", f"{commit}:{origin}"],
                                      capture_output=True, text=True, timeout=10, check=False).stdout.strip()
                if not blob or blob in seen_blobs:
                    continue
                seen_blobs.add(blob)
                data = subprocess.run(["git", "-C", repo, "cat-file", "blob", blob],
                                      capture_output=True, timeout=10, check=False).stdout
                table.setdefault(hashlib.sha256(data).hexdigest(), commit[:7])
        except (OSError, subprocess.SubprocessError):
            pass
        _HIST_CACHE[key] = table
    return _HIST_CACHE[key].get(cur_hash)


def fail(msg):
    print(f"  ❌ {msg}", file=sys.stderr)
    sys.exit(1)


def say(msg):
    print(f"  {msg}")


# ── apply ────────────────────────────────────────────────────────────────────

def cmd_apply(a):
    dry = a.dry_run
    prev = load_state() or {}
    prev_files = prev.get("files", {})
    st = empty_state(a.run_id, a.version, a.repo, a.commit)
    st["hooks"] = prev.get("hooks", {})
    st["settings"] = prev.get("settings", {})
    st["mcps"] = prev.get("mcps", [])
    if not prev:
        say("nenhum estado anterior: primeira execução (modo adoção — nada é apagado)")

    entries = []
    with open(a.manifest, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    counts = {"copied": 0, "unchanged": 0, "adopted": 0, "kept-user-edit": 0, "forced": 0,
              "skipped-user-owned": 0, "pruned": 0, "retained": 0}
    seen = set()
    for e in entries:
        src, dst = expand(e["src"]), expand(e["dst"])
        if not os.path.isfile(src):
            say(f"⚠️  origem ausente, ignorada: {src}")
            continue
        seen.add(dst)
        src_hash = sha256(src)
        rec = prev_files.get(dst)
        exists = os.path.isfile(dst)
        cur_hash = sha256(dst) if exists else None
        action = None
        if not exists:
            action = "copied"
        elif cur_hash == src_hash:
            action = "unchanged" if rec else "adopted"
        elif rec and rec.get("sha256") == cur_hash:
            action = "copied"                       # managed, untouched by user → update
        elif rec:                                   # managed but user edited it
            b = backup(dst, a.run_id, dry)
            if a.force:
                action = "forced"
                say(f"⚠️  {rel_home(dst)}: editado por você; backup em {b}; sobrescrito (--force)")
            else:
                action = "kept-user-edit"
                say(f"⚠️  {rel_home(dst)}: editado por você desde o último deploy — mantido "
                    f"(backup do seu arquivo em {b}; use --force para sobrescrever)")
        elif (old := known_old_version(a.repo, e.get("origin"), cur_hash)):
            action = "copied"                       # legacy deploy wrote it (matches commit `old`) → update
            say(f"↻  {rel_home(dst)}: versão antiga do OSForge ({old}), atualizada")
            counts["legacy-updated"] = counts.get("legacy-updated", 0) + 1
        else:                                       # not recorded and differs → user-owned
            if a.adopt:
                b = backup(dst, a.run_id, dry)
                action = "forced"
                say(f"⚠️  {rel_home(dst)}: arquivo seu, backup em {b}, sobrescrito (--adopt)")
            else:
                action = "skipped-user-owned"
                say(f"⚠️  {rel_home(dst)}: existe e não é do OSForge — mantido (use --adopt para assumir)")
        counts[action] += 1
        if action in ("copied", "forced"):
            if not dry:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                if e.get("executable") or os.access(src, os.X_OK):
                    os.chmod(dst, os.stat(dst).st_mode | 0o111)
            st["files"][dst] = {"src": e["src"], "sha256": src_hash, "critical": bool(e.get("critical"))}
        elif action in ("unchanged", "adopted"):
            st["files"][dst] = {"src": e["src"], "sha256": src_hash, "critical": bool(e.get("critical"))}
        elif action == "kept-user-edit":
            st["files"][dst] = rec                  # keep the old record → doctor reports drift
        # skipped-user-owned: not recorded

    # prune: recorded before, absent now — only under the roots this run deployed
    # (--claude-only must not touch what a previous run wrote under ~/.cursor)
    roots = [expand(r).rstrip("/") for r in (a.prune_under or [])]
    for dst, rec in prev_files.items():
        if dst in seen:
            continue
        if roots and not any(dst == r or dst.startswith(r + os.sep) for r in roots):
            st["files"][dst] = rec                  # outside this run's scope: carry over
            continue
        if not os.path.isfile(dst):
            continue
        if sha256(dst) == rec.get("sha256"):
            counts["pruned"] += 1
            say(f"🗑  aposentado: {rel_home(dst)}")
            if not dry:
                os.remove(dst)
                d = os.path.dirname(dst)
                try:
                    while d and d != HOME and not os.listdir(d):
                        os.rmdir(d); d = os.path.dirname(d)
                except OSError:
                    pass
        else:
            counts["retained"] += 1
            st["files"][dst] = rec
            say(f"⚠️  {rel_home(dst)}: saiu do repo mas foi editado por você — mantido")

    if not dry:
        save_state(st)
    say(("[dry-run] " if dry else "") + "arquivos: " + ", ".join(f"{k}={v}" for k, v in counts.items() if v))
    if counts["skipped-user-owned"]:
        say(f"ℹ️  {counts['skipped-user-owned']} arquivo(s) seu(s) colidem com o OSForge e foram mantidos; "
            "`./deploy.sh --adopt` assume todos (com backup em ~/.claude_backups/<run>/)")
    return 0


# ── hooks ────────────────────────────────────────────────────────────────────

def group_id(event, group):
    hooks = group.get("hooks") or []
    cmd = (hooks[0].get("command", "") if hooks else "")
    base = os.path.basename(cmd.split()[-1]) if cmd.split() else ""
    return f"{event}|{group.get('matcher') or '*'}|{base}"


def is_own_script(group):
    for h in group.get("hooks") or []:
        cmd = h.get("command", "")
        if cmd.split() and os.path.basename(cmd.split()[-1]) in OWN_HOOK_SCRIPTS:
            return True
    return False


def cmd_merge_hooks(a):
    dry = a.dry_run
    st = load_state()
    if st is None:
        if not dry:
            fail("merge-hooks precisa de estado (rode `apply` antes)")
        st = empty_state(a.run_id, "", "", "")     # dry-run em HOME sem estado: simula a primeira execução
    recorded = st.get("hooks", {})                       # id → group as written
    desired_all = json.load(open(a.hooks, encoding="utf-8")).get("hooks", {})
    try:
        settings = json.load(open(a.settings, encoding="utf-8"))
    except FileNotFoundError:
        settings = {}
    except json.JSONDecodeError as exc:
        fail(f"{a.settings} inválido, não vou sobrescrever: {exc}")
    cur_all = settings.setdefault("hooks", {})
    desired = {}
    for event, groups in desired_all.items():
        for g in groups:
            desired[group_id(event, g)] = (event, g)

    changes = []
    new_recorded = {}
    events = set(cur_all) | set(desired_all) | {gid.split("|")[0] for gid in recorded}
    for event in sorted(events):
        kept = []
        for g in cur_all.get(event, []):
            gid = group_id(event, g)
            if gid in recorded:
                if g != recorded[gid]:
                    if not a.force_hooks:
                        fail(f"hook {gid} foi alterado em {a.settings} depois do último deploy — "
                             f"não vou sobrescrever. Gravado: {json.dumps(recorded[gid])}  Atual: "
                             f"{json.dumps(g)}  (--force-hooks para sobrepor)")
                    changes.append(f"sobrescrito (--force-hooks): {gid}")
                continue                                  # managed → drop, re-add desired below
            if not recorded and is_own_script(g):        # first run: adopt our own entries
                changes.append(f"adotado: {gid}")
                continue
            kept.append(g)                                # user's group: untouched
        for gid, (ev, g) in desired.items():
            if ev == event:
                kept.append(g)
                new_recorded[gid] = g
                if gid not in recorded:
                    changes.append(f"adicionado: {gid}")
                elif recorded[gid] != g:
                    changes.append(f"atualizado: {gid}")
        if kept:
            cur_all[event] = kept
        else:
            cur_all.pop(event, None)
    for gid in recorded:
        if gid not in desired:
            changes.append(f"removido: {gid}")
    if not dry:
        if changes:                                       # em paridade: não toca o arquivo nem gera backup
            backup(a.settings, a.run_id, dry)
            atomic_write_json(a.settings, settings)
        st["hooks"] = new_recorded
        save_state(st)
    say(("[dry-run] " if dry else "") + ("hooks: " + "; ".join(changes) if changes else "hooks: em paridade"))
    return 0


# ── settings ─────────────────────────────────────────────────────────────────

def get_path(d, path):
    node = d
    for p in path.split("."):
        if not isinstance(node, dict) or p not in node:
            return None, False
        node = node[p]
    return node, True


def cmd_merge_settings(a):
    dry = a.dry_run
    st = load_state()
    if st is None:
        if not dry:
            fail("merge-settings precisa de estado (rode `apply` antes)")
        st = empty_state("dry-run", "", "", "")
    base = json.load(open(a.base, encoding="utf-8"))
    unset_paths = base.pop("_unset", [])
    for k in [k for k in list(base) if k.startswith("_")]:
        base.pop(k)
    try:
        cur = json.load(open(a.settings, encoding="utf-8"))
    except FileNotFoundError:
        cur = {}
    except json.JSONDecodeError as exc:
        fail(f"{a.settings} inválido, não vou sobrescrever: {exc}")
    prev_vals = st.setdefault("settings", {})
    applied = []

    def remember(path, value_before, present):
        if path not in prev_vals:
            prev_vals[path] = {"previous": value_before, "present": present}

    for path in unset_paths:
        parts = path.split(".")
        node = cur
        for p in parts[:-1]:
            node = node.get(p) if isinstance(node, dict) else None
            if node is None:
                break
        if isinstance(node, dict) and parts[-1] in node:
            remember(path, node[parts[-1]], True)
            node.pop(parts[-1]); applied.append(f"-{path}")
    for k, v in base.items():
        if k == "env" and isinstance(v, dict):
            env = cur.setdefault("env", {})
            for ek, ev in v.items():
                before, present = get_path(cur, f"env.{ek}")
                if env.get(ek) != ev:
                    remember(f"env.{ek}", before, present); applied.append(f"env.{ek}={ev}")
                env[ek] = ev
        else:
            before, present = get_path(cur, k)
            if cur.get(k) != v:
                remember(k, before, present); applied.append(f"{k}={v}")
            cur[k] = v
    if not dry:
        if applied:
            atomic_write_json(a.settings, cur)
        save_state(st)
    say(("[dry-run] " if dry else "") + "settings-base aplicado: " + (", ".join(applied) if applied else "já em paridade"))
    return 0


def cmd_record_mcps(a):
    st = load_state()
    if st is None:
        fail("record-mcps precisa de estado")
    names = [n for n in a.names.split(",") if n]
    st["mcps"] = sorted(set(st.get("mcps", [])) | set(names))
    save_state(st)
    return 0


# ── doctor / uninstall / restore / status ────────────────────────────────────

def cmd_doctor(a):
    st = load_state()
    if st is None:
        say("sem estado de instalação (nunca deployado com estado, ou desinstalado)")
        return 0
    problems = 0
    for dst, rec in sorted(st.get("files", {}).items()):
        if not os.path.isfile(dst):
            say(f"❌ ausente:  {rel_home(dst)}"); problems += 1
        elif sha256(dst) != rec.get("sha256"):
            say(f"⚠️  alterado: {rel_home(dst)}"); problems += 1
    settings_path = os.path.join(HOME, ".claude", "settings.json")
    try:
        cur = json.load(open(settings_path, encoding="utf-8")).get("hooks", {})
    except (FileNotFoundError, json.JSONDecodeError):
        cur = {}
    for gid, g in st.get("hooks", {}).items():
        event = gid.split("|")[0]
        if g not in cur.get(event, []):
            say(f"⚠️  hook divergente ou ausente em settings.json: {gid}"); problems += 1
    say(f"doctor: {len(st.get('files', {}))} arquivos, {len(st.get('hooks', {}))} hooks gerenciados, "
        f"{problems} problema(s) — run {st.get('run_id')} (v{st.get('version')}, {st.get('commit', '')[:7]})")
    return 1 if problems else 0


def cmd_uninstall(a):
    dry = a.dry_run
    st = load_state()
    if st is None:
        say("nada a desinstalar: sem estado"); return 0
    removed, retained = 0, []
    for dst, rec in sorted(st.get("files", {}).items()):
        if not os.path.isfile(dst):
            continue
        if sha256(dst) == rec.get("sha256"):
            removed += 1
            if not dry:
                os.remove(dst)
                d = os.path.dirname(dst)
                try:
                    while d and d != HOME and not os.listdir(d):
                        os.rmdir(d); d = os.path.dirname(d)
                except OSError:
                    pass
        else:
            retained.append(dst)
    settings_path = os.path.join(HOME, ".claude", "settings.json")
    try:
        settings = json.load(open(settings_path, encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        settings = None
    if settings is not None:
        hooks = settings.get("hooks", {})
        for gid, g in st.get("hooks", {}).items():
            event = gid.split("|")[0]
            if g in hooks.get(event, []):
                hooks[event] = [x for x in hooks[event] if x != g]
                if not hooks[event]:
                    hooks.pop(event)
        for path, info in st.get("settings", {}).items():
            parts = path.split(".")
            node = settings
            for p in parts[:-1]:
                node = node.setdefault(p, {}) if isinstance(node, dict) else None
                if node is None:
                    break
            if isinstance(node, dict):
                if info.get("present"):
                    node[parts[-1]] = info.get("previous")
                else:
                    node.pop(parts[-1], None)
        if not dry:
            atomic_write_json(settings_path, settings)
    claude_json = os.path.join(HOME, ".claude.json")
    if st.get("mcps") and os.path.isfile(claude_json):
        try:
            cj = json.load(open(claude_json, encoding="utf-8"))
            for n in st["mcps"]:
                cj.get("mcpServers", {}).pop(n, None)
            if not dry:
                atomic_write_json(claude_json, cj)
        except json.JSONDecodeError:
            say("⚠️  ~/.claude.json inválido; MCPs não removidos")
    if not dry:
        os.remove(STATE_FILE)
    say(("[dry-run] " if dry else "") + f"uninstall: {removed} arquivo(s) removido(s), {len(retained)} retido(s) "
        f"(alterados por você), {len(st.get('hooks', {}))} hook(s) gerenciado(s) removido(s), "
        f"{len(st.get('settings', {}))} chave(s) de settings restaurada(s)")
    for r in retained:
        say(f"   retido: {rel_home(r)}")
    return 0


def cmd_restore(a):
    root = os.path.join(BACKUP_ROOT, a.run_id)
    if not os.path.isdir(root):
        fail(f"sem backups para run {a.run_id} em {BACKUP_ROOT}")
    n = 0
    for dirpath, _, files in os.walk(root):
        for f in files:
            src = os.path.join(dirpath, f)
            dst = os.path.join(HOME, os.path.relpath(src, root))
            n += 1
            say(("[dry-run] " if a.dry_run else "") + f"restaurar {rel_home(dst)}")
            if not a.dry_run:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
    say(f"restore: {n} arquivo(s) do run {a.run_id}")
    return 0


def cmd_status(a):
    st = load_state()
    if st is None:
        say("sem estado de instalação"); return 0
    say(f"run {st['run_id']} · v{st.get('version')} · {st.get('commit', '')[:7]} · {st.get('written_at')}")
    say(f"{len(st.get('files', {}))} arquivos · {len(st.get('hooks', {}))} hooks · "
        f"{len(st.get('settings', {}))} chaves de settings · MCPs: {', '.join(st.get('mcps', [])) or '-'}")
    return 0


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(prog="osforge-state")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("apply"); s.add_argument("--manifest", required=True); s.add_argument("--run-id", required=True)
    s.add_argument("--version", default=""); s.add_argument("--repo", default=""); s.add_argument("--commit", default="")
    s.add_argument("--dry-run", action="store_true"); s.add_argument("--force", action="store_true"); s.add_argument("--adopt", action="store_true")
    s.add_argument("--prune-under", action="append", default=[])
    s = sub.add_parser("merge-hooks"); s.add_argument("--hooks", required=True); s.add_argument("--settings", required=True)
    s.add_argument("--run-id", required=True); s.add_argument("--dry-run", action="store_true"); s.add_argument("--force-hooks", action="store_true")
    s = sub.add_parser("merge-settings"); s.add_argument("--base", required=True); s.add_argument("--settings", required=True); s.add_argument("--dry-run", action="store_true")
    s = sub.add_parser("record-mcps"); s.add_argument("--names", required=True)
    sub.add_parser("doctor")
    s = sub.add_parser("uninstall"); s.add_argument("--dry-run", action="store_true")
    s = sub.add_parser("restore"); s.add_argument("--run-id", required=True); s.add_argument("--dry-run", action="store_true")
    sub.add_parser("status")
    a = p.parse_args()
    return {"apply": cmd_apply, "merge-hooks": cmd_merge_hooks, "merge-settings": cmd_merge_settings,
            "record-mcps": cmd_record_mcps, "doctor": cmd_doctor, "uninstall": cmd_uninstall,
            "restore": cmd_restore, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
