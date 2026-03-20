#!/usr/bin/env bash
# deploy.sh — Agent Skills Framework
# Sincroniza agent-skills-consolidado/ → ~/.claude/ e ~/.cursor/
# Uso: ./deploy.sh [--claude-only | --cursor-only | --dry-run]
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
CLAUDE="$HOME/.claude"
CURSOR="$HOME/.cursor"
DRY_RUN=false
DEPLOY_CLAUDE=true
DEPLOY_CURSOR=true

# ── Flags ──────────────────────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --claude-only) DEPLOY_CURSOR=false ;;
    --cursor-only) DEPLOY_CLAUDE=false ;;
    --dry-run) DRY_RUN=true ;;
    --help)
      echo "Uso: ./deploy.sh [--claude-only | --cursor-only | --dry-run]"
      exit 0 ;;
    *) echo "Flag desconhecida: $arg"; exit 1 ;;
  esac
done

# ── Helpers ─────────────────────────────────────────────────────────────
log()  { echo "  $1"; }
ok()   { echo "  ✅ $1"; }
skip() { echo "  ⟳  [dry-run] $1"; }

backup_file() {
  # Cria backup versionado antes de sobrescrever arquivo crítico
  local dst="$1"
  if [ -f "$dst" ]; then
    local bak="${dst}.bak.$(date +%Y%m%d%H%M%S)"
    cp "$dst" "$bak"
  fi
}

copy_file() {
  local src="$1" dst="$2" critical="${3:-false}"
  if $DRY_RUN; then skip "cp $(basename $src) → $dst"; return; fi
  [ "$critical" = "true" ] && backup_file "$dst"
  cp "$src" "$dst"
  ok "$(basename $src)"
}

copy_dir() {
  local src_dir="$1" dst_dir="$2"
  mkdir -p "$dst_dir"
  for f in "$src_dir"/*; do
    [ -f "$f" ] || continue
    copy_file "$f" "$dst_dir/$(basename $f)"
  done
}

merge_hooks_claude() {
  # Merge não-destrutivo: preserva hooks existentes em settings.json,
  # adiciona/atualiza apenas os eventos definidos em hooks-claude-code.json
  local hook_src="$REPO/hooks/hooks-claude-code.json"
  local settings="$CLAUDE/settings.json"
  if $DRY_RUN; then skip "merge hooks-claude-code.json → settings.json (não-destrutivo)"; return; fi
  backup_file "$settings"
  python3 - <<'PYEOF'
import json, sys, os
hook_src = os.environ.get('HOOK_SRC')
settings  = os.environ.get('SETTINGS')

with open(hook_src) as f:
    new_data = json.load(f)

try:
    with open(settings) as f:
        current = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    current = {}

# Merge não-destrutivo: iterar por evento e fazer union das listas
new_hooks = new_data.get("hooks", {})
cur_hooks  = current.setdefault("hooks", {})

for event, new_entries in new_hooks.items():
    if event not in cur_hooks:
        cur_hooks[event] = new_entries
    else:
        # Adicionar apenas entradas que não existem (por command)
        existing_cmds = set()
        for entry in cur_hooks[event]:
            for h in entry.get("hooks", []):
                existing_cmds.add(h.get("command",""))
        for entry in new_entries:
            for h in entry.get("hooks", []):
                if h.get("command","") not in existing_cmds:
                    cur_hooks[event].append(entry)
                    break

with open(settings, "w") as f:
    json.dump(current, f, indent=2, ensure_ascii=False)
print("  ✅ settings.json merged (não-destrutivo)")
PYEOF
}


sync_mcps_claude() {
  # Merge não-destrutivo de mcp/claude-code.json em ~/.claude.json
  local mcp_src="$REPO/mcp/claude-code.json"
  local claude_json="$HOME/.claude.json"
  if $DRY_RUN; then skip "sync mcp/claude-code.json → ~/.claude.json"; return; fi
  backup_file "$claude_json"
  python3 - <<'PYEOF'
import json, os
mcp_src    = os.environ.get('MCP_SRC')
claude_json = os.environ.get('CLAUDE_JSON')

with open(mcp_src) as f:
    src = json.load(f)
new_mcps = src.get('mcpServers', {})

with open(claude_json) as f:
    current = json.load(f)
cur_mcps = current.setdefault('mcpServers', {})

added = []
for name, cfg in new_mcps.items():
    if name not in cur_mcps:
        cur_mcps[name] = cfg
        added.append(name)

with open(claude_json, 'w') as f:
    json.dump(current, f, indent=2, ensure_ascii=False)

if added:
    print(f"  ✅ MCPs adicionados: {added}")
else:
    print("  ✅ MCPs em paridade — nenhuma alteração")
PYEOF
}

# ── Deploy Claude Code ───────────────────────────────────────────────────
deploy_claude() {
  echo ""
  echo "🔵 Deploy → Claude Code (~/.claude/)"

  echo ""
  log "Agentes:"
  copy_dir "$REPO/agents" "$CLAUDE/agents"
  # Orchestrator tem subdiretório próprio — copiar o AGENT.md para agents/
  if [ -f "$REPO/agents/orchestrator/AGENT.md" ]; then
    if $DRY_RUN; then skip "cp orchestrator/AGENT.md → agents/orchestrator.md"
    else
      cp "$REPO/agents/orchestrator/AGENT.md" "$CLAUDE/agents/orchestrator.md"
      ok "orchestrator.md"
    fi
  fi

  echo ""
  log "Skills (on-demand):"
  if $DRY_RUN; then skip "rsync skills/ → ~/.claude/skills/"
  else
    mkdir -p "$CLAUDE/skills"
    rsync -a --delete "$REPO/skills/" "$CLAUDE/skills/"
    count=$(find "$CLAUDE/skills" -name 'SKILL.md' | wc -l | tr -d ' ')
    ok "$count skills sincronizadas"
  fi

  echo ""
  log "Commands spec:* (9):"
  copy_dir "$REPO/commands" "$CLAUDE/commands"

  echo ""
  log "Hook scripts e Python hooks:"
  mkdir -p "$CLAUDE/hooks"
  for f in "$REPO/hooks/"*.sh "$REPO/hooks/"*.py; do
    [ -f "$f" ] || continue
    if $DRY_RUN; then skip "cp $(basename $f) + chmod +x"; continue; fi
    cp "$f" "$CLAUDE/hooks/"
    chmod +x "$CLAUDE/hooks/$(basename $f)"
    ok "$(basename $f)"
  done

  echo ""
  log "Hooks → settings.json (merge não-destrutivo):"
  HOOK_SRC="$REPO/hooks/hooks-claude-code.json" SETTINGS="$CLAUDE/settings.json" merge_hooks_claude

  echo ""
  log "CLAUDE.md + SKILLS.md:"
  copy_file "$REPO/claude-code/CLAUDE.md" "$CLAUDE/CLAUDE.md" true
  copy_file "$REPO/claude-code/SKILLS.md" "$CLAUDE/SKILLS.md"

  echo ""
  log "MCPs → ~/.claude.json (sync não-destrutivo):"
  MCP_SRC="$REPO/mcp/claude-code.json" CLAUDE_JSON="$HOME/.claude.json" sync_mcps_claude


  echo ""
  log "Verificar drift MCPs:"
  python3 - <<'PYEOF'
import json, os
with open(os.path.expanduser("~/Development/osforge/mcp/claude-code.json")) as f:
    repo_mcps = set(json.load(f).get("mcpServers", {}).keys())
with open(os.path.expanduser("~/.claude.json")) as f:
    live_mcps = set(json.load(f).get("mcpServers", {}).keys())
extra = live_mcps - repo_mcps
missing = repo_mcps - live_mcps
if extra:
    print(f"  ⚠️  MCPs em ~/.claude.json não no repo: {sorted(extra)}")
if missing:
    print(f"  ⚠️  MCPs no repo não em ~/.claude.json: {sorted(missing)}")
if not extra and not missing:
    print("  ✅ MCPs em paridade")
PYEOF

  echo ""
  ok "Claude Code deploy completo"
}

# ── Deploy Cursor ────────────────────────────────────────────────────────
deploy_cursor() {
  echo ""
  echo "🟣 Deploy → Cursor (~/.cursor/)"

  echo ""
  log "Agentes:"
  copy_dir "$REPO/agents" "$CURSOR/agents"
  if [ -f "$REPO/agents/orchestrator/AGENT.md" ]; then
    if $DRY_RUN; then skip "cp orchestrator/AGENT.md → agents/orchestrator.md"
    else
      cp "$REPO/agents/orchestrator/AGENT.md" "$CURSOR/agents/orchestrator.md"
      ok "orchestrator.md"
    fi
  fi

  echo ""
  log "Skills (on-demand):"
  if $DRY_RUN; then skip "rsync skills/ → ~/.cursor/skills/"
  else
    mkdir -p "$CURSOR/skills"
    rsync -a --delete "$REPO/skills/" "$CURSOR/skills/"
    count=$(find "$CURSOR/skills" -name 'SKILL.md' | wc -l | tr -d ' ')
    ok "$count skills sincronizadas"
  fi

  echo ""
  log "Rules:"
  copy_dir "$REPO/rules" "$CURSOR/rules"

  echo ""
  log "Hook scripts:"
  mkdir -p "$CURSOR/hooks"
  for f in "$REPO/hooks/"*.sh; do
    if $DRY_RUN; then skip "cp $(basename $f) + chmod +x"; continue; fi
    cp "$f" "$CURSOR/hooks/"
    chmod +x "$CURSOR/hooks/$(basename $f)"
    ok "$(basename $f)"
  done

  echo ""
  log "hooks.json (paths absolutos):"
  copy_file "$REPO/hooks/hooks.json" "$CURSOR/hooks.json" true

  echo ""
  log "SKILLS.md:"
  copy_file "$REPO/claude-code/SKILLS.md" "$CURSOR/SKILLS.md"

  echo ""
  ok "Cursor deploy completo"
}

# ── Main ─────────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════"
echo " Agent Skills Framework — Deploy"
echo " Repo: $REPO"
$DRY_RUN && echo " Modo: DRY RUN (sem alterações reais)"
echo "═══════════════════════════════════════════════════"

$DEPLOY_CLAUDE && deploy_claude
$DEPLOY_CURSOR && deploy_cursor

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ Deploy finalizado"
echo "═══════════════════════════════════════════════════"

# ── Verificar dependências opcionais ─────────────────────────────────────
echo ''
echo '🔍 Verificando dependências opcionais...'
if command -v llmfit &>/dev/null; then
  LLMFIT_VER=$(llmfit --version 2>/dev/null | head -1 || echo 'instalado')
  echo "  ✅ llmfit: $LLMFIT_VER"
else
  echo '  ⚠️  llmfit não encontrado — skill llmfit-advisor não estará disponível'
  echo '     Instalar: brew tap AlexsJones/llmfit && brew install llmfit'
  echo '     Ou via Rust: cargo install llmfit'
fi
