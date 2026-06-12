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
DEPLOY_QDRANT_OVERRIDE=""   # "yes" | "no" | "" (interativo)

# ── Flags ──────────────────────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --claude-only) DEPLOY_CURSOR=false ;;
    --cursor-only) DEPLOY_CLAUDE=false ;;
    --dry-run) DRY_RUN=true ;;
    --with-qdrant) DEPLOY_QDRANT_OVERRIDE="yes" ;;
    --no-qdrant)   DEPLOY_QDRANT_OVERRIDE="no"  ;;
    --help)
      echo "Uso: ./deploy.sh [--claude-only | --cursor-only | --dry-run | --with-qdrant | --no-qdrant]"
      echo ""
      echo "  --with-qdrant   Sobe Qdrant via Docker sem prompt interativo"
      echo "  --no-qdrant     Pula Qdrant; configura SQLite como backend vetorial"
      exit 0 ;;
    *) echo "Flag desconhecida: $arg"; exit 1 ;;
  esac
done

# ── Helpers ─────────────────────────────────────────────────────────────
log()  { echo "  $1"; }
ok()   { echo "  ✅ $1"; }
skip() { echo "  ⟳  [dry-run] $1"; }

backup_file() {
  # Cria backup versionado em ~/.claude_backups (fora da pasta oficial)
  local dst="$1"
  if [ -f "$dst" ]; then
    local bak_dir="$HOME/.claude_backups"
    mkdir -p "$bak_dir"
    local filename="$(basename "$dst")"
    local bak="${bak_dir}/${filename}.bak.$(date +%Y%m%d%H%M%S)"
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
  log "Commands spec-* (9):"
  # Remover legados com ':' no nome (pré-ADR-008, ilegal em NTFS/Windows)
  rm -f "$CLAUDE/commands/spec:"*.md 2>/dev/null || true
  copy_dir "$REPO/commands" "$CLAUDE/commands"

  echo ""
  log "OSForge Canvas (server + viewer):"
  if $DRY_RUN; then skip "cp scripts/canvas/{server.ts,viewer.html} → ~/.claude/canvas/"
  else
    mkdir -p "$CLAUDE/canvas"
    cp "$REPO/scripts/canvas/server.ts" "$REPO/scripts/canvas/viewer.html" "$CLAUDE/canvas/"
    ok "canvas deployado em $CLAUDE/canvas/ (autostart via SessionStart hook)"
  fi

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

# ── Deploy osforge-db ────────────────────────────────────────────────────
deploy_osforge_db() {
  echo ""
  echo "🗄️  Deploy → osforge-db CLI"

  local db_dir="$HOME/.osforge"
  local db_bin="$HOME/.local/bin/osforge-db"
  local script_src="$REPO/scripts/osforge-db.py"

  if $DRY_RUN; then
    skip "mkdir -p $db_dir"
    skip "cp osforge-db.py → $db_bin"
    return
  fi

  mkdir -p "$db_dir"
  mkdir -p "$HOME/.local/bin"
  cp "$script_src" "$db_bin"
  chmod +x "$db_bin"
  ok "osforge-db instalado em $db_bin"

  # Inicializar banco global se ainda não existe
  if [ ! -f "$db_dir/osforge.db" ]; then
    python3 "$db_bin" init >/dev/null 2>&1 && ok "Banco global criado: $db_dir/osforge.db"
  else
    # Garantir que schema está atualizado (idempotente)
    python3 "$db_bin" init >/dev/null 2>&1
    ok "Banco global verificado: $db_dir/osforge.db"
  fi

  # Checar se ~/.local/bin está no PATH
  if ! command -v osforge-db &>/dev/null; then
    echo "  ⚠️  ~/.local/bin não está no PATH"
    echo "     Adicione ao ~/.zshrc ou ~/.bashrc:"
    echo '     export PATH="$HOME/.local/bin:$PATH"'
  fi
}

# ── Deploy Qdrant (opcional) ─────────────────────────────────────────────
deploy_qdrant() {
  echo ""
  echo "🔵 Deploy → Qdrant (vector store)"

  local compose_file="$REPO/scripts/qdrant/docker-compose.yml"
  local cfg_dir="$HOME/.osforge"
  local cfg_file="$cfg_dir/config.json"

  # Determinar se o usuário quer Qdrant
  local do_qdrant="$DEPLOY_QDRANT_OVERRIDE"
  if [ -z "$do_qdrant" ]; then
    # Modo interativo: só perguntar se TTY disponível
    if [ -t 0 ]; then
      printf "  Subir Qdrant via Docker? [y/N] "
      read -r ans
      case "$ans" in
        [Yy]*) do_qdrant="yes" ;;
        *)     do_qdrant="no"  ;;
      esac
    else
      do_qdrant="no"
    fi
  fi

  if [ "$do_qdrant" != "yes" ]; then
    # Caminho sem Qdrant: configurar SQLite como backend
    if $DRY_RUN; then
      skip "Qdrant pulado → backend vetorial: sqlite"
      skip "write $cfg_file {vector_backend: sqlite}"
    else
      mkdir -p "$cfg_dir"
      # Ler backend atual para distinguir downgrade real de preservação
      local cur_backend
      cur_backend=$(python3 -c "import json,pathlib;p=pathlib.Path.home()/'.osforge'/'config.json';print(json.loads(p.read_text()).get('vector_backend','') if p.exists() else '')" 2>/dev/null || echo "")
      if [ "$cur_backend" = "qdrant" ]; then
        echo "  ℹ️  config.json já está em vector_backend=qdrant — preservado (nada a fazer)."
        echo "      Para re-provisionar o Qdrant: ./deploy.sh --with-qdrant"
      else
        python3 - <<'PYEOF'
import json, pathlib
cfg_path = pathlib.Path.home() / ".osforge" / "config.json"
cfg = {}
if cfg_path.exists():
    try:
        cfg = json.loads(cfg_path.read_text())
    except Exception:
        pass
cfg["vector_backend"] = "sqlite"
cfg.setdefault("embed_provider", "ollama")
cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
print("  ℹ️  config.json → vector_backend=sqlite")
PYEOF
        echo "  ⚠️  Memória vetorial Qdrant NÃO instalada. Backend: SQLite (cosseno brute-force)."
        echo "      Busca semântica continua funcionando, porém a PERFORMANCE pode DEGRADAR"
        echo "      em corpus grande (busca O(n) vs índice HNSW do Qdrant)."
        echo "      Para ativar depois: ./deploy.sh --with-qdrant"
      fi
    fi
    return
  fi

  # ── Caminho com Qdrant ───────────────────────────────────────────────
  if $DRY_RUN; then
    skip "docker compose -f $compose_file up -d"
    skip "poll http://localhost:6333/healthz"
    skip "vec-init (cria/valida coleção)"
    skip "write $cfg_file {vector_backend: qdrant}"
    return
  fi

  # Checar Docker
  if ! command -v docker &>/dev/null; then
    echo "  ❌ Docker não encontrado. Instale Docker Desktop ou Docker Engine."
    echo "     Qdrant não será iniciado. Backend: sqlite."
    return 1
  fi

  # Subir container
  mkdir -p "$HOME/.osforge/qdrant/storage"
  if docker compose -f "$compose_file" up -d 2>&1; then
    ok "Qdrant container iniciado"
  else
    echo "  ❌ Falha ao subir Qdrant. Backend: sqlite."
    return 1
  fi

  # Poll /healthz (máx 30s)
  local deadline=$((SECONDS + 30))
  printf "  Aguardando Qdrant..."
  while [ $SECONDS -lt $deadline ]; do
    if curl -sf http://localhost:6333/healthz >/dev/null 2>&1; then
      echo " ok"
      break
    fi
    printf "."
    sleep 1
  done
  if [ $SECONDS -ge $deadline ]; then
    echo " timeout!"
    echo "  ❌ Qdrant não respondeu em 30s. Backend: sqlite."
    return 1
  fi

  # Checar Ollama
  if ! command -v ollama &>/dev/null; then
    echo "  ⚠️  Ollama não encontrado. Embeddings não funcionarão sem ele."
    echo "     Instale: https://ollama.com — depois rode: ollama pull bge-m3"
  else
    # Checagem confiável via API do Ollama (/api/tags); fallback para o CLI.
    # `ollama list | grep` sozinho dá falso-negativo se o CLI estiver lento/frio.
    if curl -s --max-time 5 http://localhost:11434/api/tags 2>/dev/null | grep -q '"bge-m3' \
       || ollama list 2>/dev/null | grep -q "bge-m3"; then
      ok "Ollama + bge-m3 disponíveis"
    else
      echo "  ⚠️  Modelo bge-m3 ausente. Rode: ollama pull bge-m3"
    fi
  fi

  # Criar/validar coleção via vec-init
  local db_bin="$HOME/.local/bin/osforge-db"
  if [ -f "$db_bin" ]; then
    OSFORGE_VECTOR=qdrant OSFORGE_EMBED=ollama python3 "$db_bin" vec-init 2>&1 \
      && ok "Coleção Qdrant inicializada" \
      || echo "  ⚠️  vec-init falhou (Ollama ausente?). Coleção será criada na primeira escrita."
  fi

  # Escrever config.json
  mkdir -p "$cfg_dir"
  python3 - <<'PYEOF'
import json, pathlib
cfg_path = pathlib.Path.home() / ".osforge" / "config.json"
cfg = {}
if cfg_path.exists():
    try:
        cfg = json.loads(cfg_path.read_text())
    except Exception:
        pass
cfg["vector_backend"]  = "qdrant"
cfg["embed_provider"]  = "ollama"
cfg.setdefault("embed_model",  "bge-m3")
cfg.setdefault("qdrant_url",   "http://localhost:6333")
cfg.setdefault("collection",   "osforge_memory")
cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
print(f"  config.json → vector_backend=qdrant")
PYEOF
  ok "Qdrant deploy completo"
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
deploy_osforge_db
deploy_qdrant || true   # Qdrant é opt-in; falha (Docker ausente etc.) não aborta o deploy

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
