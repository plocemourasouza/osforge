#!/usr/bin/env bash
# session-resume.sh — SessionStart hook
# Injeta contexto de resume do osforge-db quando o cwd é um projeto registrado.
#
# Saída esperada pelo Claude Code (SessionStart):
#   {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "<texto>"}}
#
# Silencioso e exit 0 em qualquer caso de erro ou projeto não registrado.
set -uo pipefail

# ── Localiza osforge-db ───────────────────────────────────────────────────────
OSFORGE_DB=""
for candidate in \
    "$HOME/.local/bin/osforge-db" \
    "$HOME/Development/osforge/scripts/osforge-db.py" \
    "$(dirname "$0")/../scripts/osforge-db.py"
do
    if [ -x "$candidate" ] || [ -f "$candidate" ]; then
        OSFORGE_DB="$candidate"
        break
    fi
done

[ -z "$OSFORGE_DB" ] && exit 0

run_db() {
    if [[ "$OSFORGE_DB" == *.py ]]; then
        python3 "$OSFORGE_DB" "$@" 2>/dev/null
    else
        "$OSFORGE_DB" "$@" 2>/dev/null
    fi
}

# ── Resolve o slug a partir do cwd ───────────────────────────────────────────
# Estratégia: basename do cwd em lowercase com hífens (igual ao padrão do osforge).
CWD="$(pwd -P 2>/dev/null || echo "")"
[ -z "$CWD" ] && exit 0

SLUG="$(basename "$CWD" | tr '[:upper:]' '[:lower:]' | tr '_' '-')"
[ -z "$SLUG" ] && exit 0

# Verifica se o slug existe no banco global (saída vazia → não registrado).
# Usa list-projects --json para consulta limpa; filtra pelo slug exato.
PROJECT_STATUS="$(run_db list-projects --status=all --json 2>/dev/null \
    | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    slug = sys.argv[1]
    match = next((p for p in data if p.get('slug') == slug), None)
    print(match['status'] if match else '')
except Exception:
    pass
" "$SLUG" 2>/dev/null || true)"

[ -z "$PROJECT_STATUS" ] && exit 0

# ── Coleta resume point ───────────────────────────────────────────────────────
RESUME_RAW="$(run_db resume "$SLUG" 2>/dev/null || true)"
[ -z "$RESUME_RAW" ] && exit 0

# Se resume point for "sem estado registrado" ou "fase=– | resume=–", sai silencioso
# (não polui a sessão com contexto vazio).
if echo "$RESUME_RAW" | grep -qE '^sem estado|resume=–$'; then
    exit 0
fi

# ── Coleta board compacto ─────────────────────────────────────────────────────
BOARD_RAW="$(run_db board 2>/dev/null | head -40 || true)"

# ── Monta additionalContext ───────────────────────────────────────────────────
CONTEXT="OSForge resume — projeto: ${SLUG} (${PROJECT_STATUS})
${RESUME_RAW}"

if [ -n "$BOARD_RAW" ]; then
    CONTEXT="${CONTEXT}

--- board (cross-project) ---
${BOARD_RAW}"
fi

# ── Emite JSON para o Claude Code ─────────────────────────────────────────────
# python3 stdlib para serialização segura (evita problemas com aspas/newlines).
python3 -c "
import json, sys
context = sys.argv[1]
payload = {
    'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': context
    }
}
print(json.dumps(payload, ensure_ascii=False))
" "$CONTEXT" 2>/dev/null || true

exit 0
