#!/usr/bin/env bash
# prune-global-mcps.sh — Remove MCP servers do ~/.claude.json (escopo User/global).
#
# O deploy.sh faz merge ADITIVO de MCPs (nunca poda). Servers antigos, quebrados
# ou que migraram para escopo de projeto ficam acumulados no global consumindo
# contexto em TODA sessão. Este script remove os que você indicar. Faz backup antes.
#
# Uso:
#   prune-global-mcps.sh --list                 # mostra servers globais atuais
#   prune-global-mcps.sh <nome> [nome2 ...]     # remove os nomeados
#   prune-global-mcps.sh --dead                 # remove defaults mortos/migrados:
#                                               #   MCP_DOCKER, Prisma-Remote
#   prune-global-mcps.sh --dry-run <nome> ...   # mostra o que faria
set -euo pipefail

CLAUDE_JSON="$HOME/.claude.json"
DRY=false
declare -a TARGETS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --list)
      python3 - "$CLAUDE_JSON" <<'PY'
import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception as e: print("erro lendo ~/.claude.json:",e); sys.exit(1)
m=d.get('mcpServers',{})
print(f"{len(m)} MCP servers globais em ~/.claude.json:")
for k in sorted(m): print("  -",k)
PY
      exit 0 ;;
    --dead) TARGETS+=("MCP_DOCKER" "Prisma-Remote"); shift ;;
    --dry-run) DRY=true; shift ;;
    --help|-h) sed -n '2,16p' "$0"; exit 0 ;;
    *) TARGETS+=("$1"); shift ;;
  esac
done

[ ${#TARGETS[@]} -gt 0 ] || { echo "Uso: prune-global-mcps.sh <nome> [...] | --dead | --list"; exit 1; }
[ -f "$CLAUDE_JSON" ] || { echo "❌ $CLAUDE_JSON não existe"; exit 1; }

if ! $DRY; then
  bak="$HOME/.claude_backups/.claude.json.bak.$(date +%Y%m%d%H%M%S)"
  mkdir -p "$HOME/.claude_backups"; cp "$CLAUDE_JSON" "$bak"
  echo "🗄️  backup: $bak"
fi

DRY=$DRY python3 - "$CLAUDE_JSON" "${TARGETS[@]}" <<'PY'
import json, os, sys
path=sys.argv[1]; targets=sys.argv[2:]; dry=os.environ.get('DRY')=='true'
d=json.load(open(path)); m=d.get('mcpServers',{})
removed=[t for t in targets if t in m]
missing=[t for t in targets if t not in m]
if dry:
    print("[dry-run] removeria:", removed or "nada")
else:
    for t in removed: del m[t]
    json.dump(d, open(path,'w'), indent=2, ensure_ascii=False)
    print("✅ removidos:", removed or "nada")
if missing: print("ℹ️  não encontrados (ok):", missing)
PY

$DRY || echo "Reinicie a sessão do Claude Code para refletir. Confira com /context e /mcp."
