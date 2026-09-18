#!/bin/bash
# Hook: Stop (Claude Code) / stop (Cursor)
# Claude Code payload: { hook_event_name: "Stop", stop_hook_active, session_id, transcript_path }
# Cursor payload:      { status, ... }
# Notifica via osascript (macOS; silencioso em outros SOs) e registra em ~/.osforge/logs/hooks.log.
#
# B-007 (E-A13): `stop_hook_active` é TRUE só quando o Claude Code já está continuando
# a partir de um Stop hook que bloqueou — não é o sinal de "parou normalmente". Uma
# parada normal chega com stop_hook_active=false. A versão anterior tinha a lógica
# invertida e só notificava no caso raro. Nunca escreve em /tmp (previsível, legível por todos).
# Saída para o modelo: nenhuma (stdout vazio). Sempre exit 0.

input=$(cat)

eval "$(printf '%s' "$input" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    if not isinstance(d, dict): d = {}
except Exception:
    d = {}
is_claude = bool(d.get("hook_event_name")) or "transcript_path" in d or "stop_hook_active" in d
active = str(d.get("stop_hook_active", "")).lower() == "true"
print("IS_CLAUDE={}".format("1" if is_claude else "0"))
print("ACTIVE={}".format("1" if active else "0"))
print("CURSOR_STATUS={}".format(str(d.get("status", "")).replace("\"", "")[:20]))
' 2>/dev/null)"

LOG_DIR="${OSFORGE_LOG_DIR:-$HOME/.osforge/logs}"
mkdir -p "$LOG_DIR" 2>/dev/null
LOG="$LOG_DIR/hooks.log"
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
notify() { command -v osascript >/dev/null 2>&1 && osascript -e "display notification \"$2\" with title \"$1\" sound name \"$3\"" >/dev/null 2>&1; return 0; }

if [ "${IS_CLAUDE:-0}" = "1" ] && [ "${ACTIVE:-0}" != "1" ]; then
  notify "Claude Code" "Agente concluiu a tarefa ✅" "Glass"
  echo "{\"timestamp\": \"$timestamp\", \"event\": \"agent_stop\", \"source\": \"claude_code\"}" >> "$LOG" 2>/dev/null
elif [ "${CURSOR_STATUS:-}" = "completed" ]; then
  notify "Cursor Agent" "Task concluída com sucesso ✅" "Glass"
  echo "{\"timestamp\": \"$timestamp\", \"event\": \"agent_stop\", \"source\": \"cursor\", \"status\": \"completed\"}" >> "$LOG" 2>/dev/null
elif [ "${CURSOR_STATUS:-}" = "error" ]; then
  notify "Cursor Agent" "Task falhou ❌" "Basso"
  echo "{\"timestamp\": \"$timestamp\", \"event\": \"agent_stop\", \"source\": \"cursor\", \"status\": \"error\"}" >> "$LOG" 2>/dev/null
fi
exit 0
