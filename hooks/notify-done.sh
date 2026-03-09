#!/bin/bash
# Hook: Stop (Claude Code) / stop (Cursor)
# Claude Code payload: { stop_hook_active, session_id, transcript_path }
# Cursor payload:      { status, ... }
# Notifica via osascript e registra no log.

input=$(cat)

# Detectar ferramenta pelo payload
stop_hook_active=$(echo "$input" | python3 -c "
import sys, json
try: print(json.load(sys.stdin).get('stop_hook_active', 'unknown'))
except: print('unknown')
" 2>/dev/null)

cursor_status=$(echo "$input" | python3 -c "
import sys, json
try: print(json.load(sys.stdin).get('status', ''))
except: print('')
" 2>/dev/null)

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Claude Code: stop_hook_active=true significa agente parou normalmente
if [ "$stop_hook_active" = "True" ] || [ "$stop_hook_active" = "true" ]; then
  osascript -e 'display notification "Agente concluiu a tarefa ✅" with title "Claude Code" sound name "Glass"' 2>/dev/null
  echo "{\"timestamp\": \"$timestamp\", \"event\": \"agent_stop\", \"source\": \"claude_code\", \"stop_hook_active\": true}" >> /tmp/agent-hooks.log

# Cursor: status=completed
elif [ "$cursor_status" = "completed" ]; then
  osascript -e 'display notification "Task concluída com sucesso ✅" with title "Cursor Agent" sound name "Glass"' 2>/dev/null
  echo "{\"timestamp\": \"$timestamp\", \"event\": \"agent_stop\", \"source\": \"cursor\", \"status\": \"completed\"}" >> /tmp/agent-hooks.log

# Cursor: status=error
elif [ "$cursor_status" = "error" ]; then
  osascript -e 'display notification "Task falhou ❌" with title "Cursor Agent" sound name "Basso"' 2>/dev/null
  echo "{\"timestamp\": \"$timestamp\", \"event\": \"agent_stop\", \"source\": \"cursor\", \"status\": \"error\"}" >> /tmp/agent-hooks.log
fi
