#!/usr/bin/env bash
# install-mcp.sh — Instala um MCP server por PROJETO (escopo project via .mcp.json).
#
# Model MCP: só Context7 fica global (mcp/claude-code.json). Servers de stack
# (github, supabase, prisma, nextjs, shadcn, browser) vivem em mcp/stacks/ e são
# ligados só no projeto que precisa — conectam apenas ali, sem custo de contexto
# nos demais projetos.
#
# Uso:
#   install-mcp.sh <stack> [stack2 ...]   # merge em ./.mcp.json (cwd)
#   install-mcp.sh --list                 # lista stacks disponíveis
#   install-mcp.sh --target <dir> <stack> # destino explícito
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
STACKS="$REPO/mcp/stacks"
TARGET_DIR="$PWD"
declare -a NAMES=()

while [ $# -gt 0 ]; do
  case "$1" in
    --list) ls -1 "$STACKS" 2>/dev/null | sed 's/\.mcp\.json$//' | sed 's/^/  /'; exit 0 ;;
    --target) TARGET_DIR="$2"; shift 2 ;;
    --help|-h) sed -n '2,14p' "$0"; exit 0 ;;
    *) NAMES+=("$1"); shift ;;
  esac
done

[ ${#NAMES[@]} -gt 0 ] || { echo "Uso: install-mcp.sh <stack> [...]  (--list para ver stacks)"; exit 1; }

DEST="$TARGET_DIR/.mcp.json"
for name in "${NAMES[@]}"; do
  src="$STACKS/$name.mcp.json"
  if [ ! -f "$src" ]; then
    echo "⚠️  stack desconhecido: $name  (use --list)" >&2; continue
  fi
  SRC="$src" DEST="$DEST" python3 - <<'PY'
import json, os
src, dest = os.environ['SRC'], os.environ['DEST']
new = json.load(open(src)).get('mcpServers', {})
try:
    cur = json.load(open(dest))
except (FileNotFoundError, json.JSONDecodeError):
    cur = {}
servers = cur.setdefault('mcpServers', {})
added = []
for k, v in new.items():
    if k not in servers:
        servers[k] = v; added.append(k)
json.dump(cur, open(dest, 'w'), indent=2, ensure_ascii=False)
open(dest,'a').write('\n')
print(f"✅ {os.path.basename(src)} → {dest}" + (f"  (+{added})" if added else "  (já presente)"))
PY
done

echo ""
echo "Pronto. Preencha tokens/placeholders no $DEST e reinicie a sessão do Claude Code."
echo "Dica: adicione .mcp.json ao versionamento se o time compartilha os mesmos servers."
