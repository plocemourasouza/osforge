#!/bin/bash
# Hook: PreToolUse (Bash) — Claude Code and Cursor (beforeShellExecution).
# Thin wrapper: all logic lives in scan-secrets.py next to this file (B-002).
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/scan-secrets.py"
