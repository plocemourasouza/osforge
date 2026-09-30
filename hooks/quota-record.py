#!/usr/bin/env python3
"""
hooks/quota-record.py — A1 recorder (SPEC-L01 Parte A). NOT a Claude Code hook: it is not wired
in hooks/hooks-claude-code.json (D-2) and OSForge does not manage the user's statusline script.
It is invoked by one OPTIONAL, documented line the user adds to their own
`~/.claude/statusline-command.sh` (D-1, docs/HOOKS.md):

    printf '%s' "$input" | python3 "$HOME/.claude/hooks/quota-record.py" >/dev/null 2>&1 &

Reads the statusline's stdin JSON (EV-C01: `rate_limits.five_hour` / `.seven_day`, each with
`used_percentage` and `resets_at`; `rate_limits: null` for API-key/Bedrock/Vertex auth) and
writes `~/.osforge/quota.json` atomically via hooks/lib/quota.py.

Rules: never prints anything; exits 0 on any error; `rate_limits` missing or null leaves the
existing file untouched; capped at 1 MB of stdin (same as context-threshold.py); must run in
well under 20 ms (tests/test-quota.sh case 9). Path override: OSFORGE_QUOTA_FILE (tests).
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
try:
    from quota import record_statusline
except Exception:                                    # pragma: no cover — never block the caller
    record_statusline = None

MAX_STDIN = 1024 * 1024


def main():
    if record_statusline is None:
        return
    try:
        raw = sys.stdin.read(MAX_STDIN)
    except Exception:
        return
    if not raw or not raw.strip():
        return
    try:
        payload = json.loads(raw)
    except Exception:
        return
    try:
        record_statusline(payload)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
