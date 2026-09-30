#!/usr/bin/env bash
# canvas-autostart.sh — SessionStart hook
# Garante que o OSForge Canvas está rodando no início de cada sessão.
# Servidor global: dados em ~/.osforge/canvas (compartilhado entre projetos;
# artefatos devem usar slug do projeto no id para evitar colisão).
# Nunca falha a sessão: sem bun ou sem server → sai silencioso.
set -uo pipefail

PORT="${CANVAS_PORT:-4242}"
DATA_DIR="$HOME/.osforge/canvas"
SERVER="$HOME/.claude/canvas/server.ts"

command -v bun >/dev/null 2>&1 || exit 0
# Fallback para o repo OSForge quando o deploy ainda não copiou o canvas
[ -f "$SERVER" ] || SERVER="$HOME/Development/osforge/scripts/canvas/server.ts"
[ -f "$SERVER" ] || exit 0

health() { curl -sf --max-time 1 "http://127.0.0.1:${PORT}/api/health" 2>/dev/null; }

existing="$(health || true)"
if [ -n "$existing" ]; then
  echo "OSForge Canvas ATIVO: http://localhost:${PORT} — specs e planos devem ser apresentados como artefato canvas por default (skill osforge-canvas; data dir via GET /api/health)."
  exit 0
fi

mkdir -p "$DATA_DIR"
nohup bun "$SERVER" --dir="$DATA_DIR" >/dev/null 2>&1 &
disown 2>/dev/null || true
sleep 0.5

if [ -n "$(health || true)" ]; then
  echo "OSForge Canvas INICIADO: http://localhost:${PORT} (dir: ${DATA_DIR}) — specs e planos devem ser apresentados como artefato canvas por default (skill osforge-canvas)."
else
  echo "OSForge Canvas: falha ao iniciar na porta ${PORT}. Iniciar manualmente: bun ${SERVER} --dir=${DATA_DIR}"
fi
exit 0
