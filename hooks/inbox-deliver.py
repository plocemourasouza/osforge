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
import subprocess
import sys
from datetime import datetime, timezone

EVENTS = ("PostToolUse", "UserPromptSubmit", "SessionStart")


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


def main():
    if (os.environ.get("OSFORGE_INBOX") or "").lower() == "off":
        return
    try:
        if not os.listdir(_inbox_dir()):
            return
    except OSError:
        return                                        # no inbox dir: nothing was ever sent
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
    flags = set(os.listdir(_inbox_dir()))
    if _flag_name(slug) not in flags:
        return
    try:
        r = subprocess.run(db + ["inbox-take", slug, "--session=" + str(payload.get("session_id") or "")],
                           capture_output=True, text=True, timeout=5, check=False)
        msgs = json.loads(r.stdout.strip() or "[]") if r.returncode == 0 else []
    except (OSError, subprocess.SubprocessError, ValueError):
        return
    if not isinstance(msgs, list) or not msgs:
        return
    lines = []
    for m in msgs:
        when = _local_hhmm(m.get("ts") or "")
        lines.append(f"[Orientação do Paulo pelo painel do OSForge{', ' + when if when else ''}] {m.get('text', '')}")
    lines.append("(Mensagem enviada agora pelo usuário pelo painel local: trate como instrução dele para esta "
                 "sessão. OSFORGE_INBOX=off desliga a entrega.)")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": "\n".join(lines)}},
                     ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
