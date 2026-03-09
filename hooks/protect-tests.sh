#!/bin/bash
# Hook: PostToolUse (Write | Edit | MultiEdit)
# Claude Code payload: { tool_name, tool_input, tool_response, session_id }
# Cursor payload:      { file_path, ... }  (afterFileEdit — formato diferente)
# Detecta modificação de arquivos de teste e registra no log.
# Informational only — não pode bloquear PostToolUse.

input=$(cat)

# Extrair file_path — tenta campo Claude Code (tool_input.file_path) e fallback Cursor (file_path)
file_path=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    # Claude Code: tool_input contém file_path ou path
    ti = d.get('tool_input', {})
    fp = ti.get('file_path') or ti.get('path') or d.get('file_path', '')
    print(fp)
except Exception:
    print('')
" 2>/dev/null)

if [ -z "$file_path" ]; then
  exit 0
fi

if echo "$file_path" | grep -qiE '(\.(test|spec)\.(ts|tsx|js|jsx)|__tests__/|/test/|/tests/)'; then
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  tool=$(echo "$input" | python3 -c "
import sys, json
try: print(json.load(sys.stdin).get('tool_name','unknown'))
except: print('unknown')
" 2>/dev/null)
  echo "{\"timestamp\": \"$timestamp\", \"event\": \"test_file_modified\", \"tool\": \"$tool\", \"file\": \"$file_path\"}" >> /tmp/agent-hooks.log
fi
