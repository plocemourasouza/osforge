#!/bin/bash
# Hook: PostToolUse (Write | Edit | MultiEdit) — Claude Code; afterFileEdit — Cursor
# Claude Code payload: { hook_event_name, tool_name, tool_input, tool_response, session_id }
# Cursor payload:      { file_path, ... }
#
# Detecta modificação de arquivo de TESTE. PostToolUse não pode bloquear; o que ele
# pode é falar com o modelo. B-007 (E-A12): antes só gravava uma linha em /tmp e nada
# chegava a ninguém. Agora, no Claude Code, injeta `additionalContext` lembrando a
# Iron Law do TDD (teste só muda com o usuário ciente); no Cursor continua só o log,
# em ~/.osforge/logs/hooks.log. Sempre exit 0.

input=$(cat)

eval "$(printf '%s' "$input" | python3 -c '
import sys, json, os
try:
    d = json.load(sys.stdin)
    if not isinstance(d, dict): d = {}
except Exception:
    d = {}
ti = d.get("tool_input") if isinstance(d.get("tool_input"), dict) else {}
fp = ti.get("file_path") or ti.get("path") or d.get("file_path") or ""
is_claude = bool(d.get("hook_event_name")) or "tool_input" in d
print("FILE_PATH=" + repr(str(fp)))
print("TOOL=" + repr(str(d.get("tool_name", "unknown"))))
print("IS_CLAUDE={}".format("1" if is_claude else "0"))
' 2>/dev/null)"

[ -z "${FILE_PATH:-}" ] && exit 0
printf '%s' "$FILE_PATH" | grep -qiE '(\.(test|spec)\.(ts|tsx|js|jsx|py|mjs|cjs)$|__tests__/|/test/|/tests/)' || exit 0

LOG_DIR="${OSFORGE_LOG_DIR:-$HOME/.osforge/logs}"
mkdir -p "$LOG_DIR" 2>/dev/null
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"timestamp\": \"$timestamp\", \"event\": \"test_file_modified\", \"tool\": \"${TOOL:-unknown}\", \"file\": \"$FILE_PATH\"}" >> "$LOG_DIR/hooks.log" 2>/dev/null

if [ "${IS_CLAUDE:-0}" = "1" ]; then
  python3 -c '
import json, sys
fp = sys.argv[1]
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext":
  "[protect-tests] Test file modified: " + fp + ". TDD Iron Law: a test changes only to describe intended behaviour, never to make a failing test pass — if this edit was to get green, revert it and fix the source instead, and say so to the user."}}))
' "$FILE_PATH"
fi
exit 0
