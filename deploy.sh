#!/usr/bin/env bash
# deploy.sh — Agent Skills Framework
# Sincroniza agent-skills-consolidado/ → ~/.claude/ e ~/.cursor/
# Uso: ./deploy.sh [--claude-only | --cursor-only | --dry-run]
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
OSFORGE_VERSION="$(tr -d "[:space:]" < "$REPO/VERSION" 2>/dev/null || echo "dev")"
CLAUDE="$HOME/.claude"
CURSOR="$HOME/.cursor"
DRY_RUN=false
DEPLOY_CLAUDE=true
DEPLOY_CURSOR=true
DEPLOY_QDRANT_OVERRIDE=""   # "yes" | "no" | "" (interativo)
DEPLOY_ALL_SKILLS=false     # false = só o core allowlist (Model A); true = todas as skills

# Archify (tt-a1i/archify, MIT) — motor de diagramas verificados usado pela skill
# core `system-diagrams`. É uma FERRAMENTA que executamos, não um padrão que
# curamos: não vive no repo, é instalada pinada em ~/.claude/skills/archify e
# ~/.cursor/skills/archify (precedente: llmfit). Upgrade = mudar a tag abaixo,
# rodar ./deploy.sh e conferir o `doctor`. Ver docs/ANALISE-ARCHIFY.md §4.1.
ARCHIFY_VERSION="2.16.0"    # tag upstream sem o "v"
ARCHIFY_REPO="tt-a1i/archify"
DEPLOY_ARCHIFY=true         # --no-archify desliga

# ── Flags ──────────────────────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --claude-only) DEPLOY_CURSOR=false ;;
    --cursor-only) DEPLOY_CLAUDE=false ;;
    --dry-run) DRY_RUN=true ;;
    --with-qdrant) DEPLOY_QDRANT_OVERRIDE="yes" ;;
    --no-qdrant)   DEPLOY_QDRANT_OVERRIDE="no"  ;;
    --all-skills)  DEPLOY_ALL_SKILLS=true ;;
    --with-archify) DEPLOY_ARCHIFY=true ;;
    --no-archify)   DEPLOY_ARCHIFY=false ;;
    --help)
      echo "Uso: ./deploy.sh [--claude-only | --cursor-only | --dry-run | --with-qdrant | --no-qdrant | --all-skills | --no-archify]"
      echo ""
      echo "  --with-qdrant   Sobe Qdrant via Docker sem prompt interativo"
      echo "  --no-qdrant     Pula Qdrant; configura SQLite como backend vetorial"
      echo "  --all-skills    Deploya TODAS as skills globalmente (default: só o core de claude-code/skills-core.txt)"
      echo "  --with-archify  Instala/atualiza o Archify pinado (v$ARCHIFY_VERSION) em ~/.claude/skills e ~/.cursor/skills (default)"
      echo "  --no-archify    Pula o Archify (a skill system-diagrams cai no fallback Mermaid)"
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

# SKILLS.md carrega o MANIFEST, cujos paths precisam ser ABSOLUTOS: as skills
# não-core só existem neste repo, e o manifesto é lido em sessões satélite
# (outro diretório), onde um `skills/<nome>/SKILL.md` relativo não resolve.
# O repo guarda o token; o deploy grava o caminho real desta cópia.
copy_skills_md() {
  local dst="$1"
  local src="$REPO/claude-code/SKILLS.md"
  if $DRY_RUN; then skip "cp SKILLS.md → $dst (com raiz de skills expandida)"; return; fi
  sed "s|__OSFORGE_SKILLS_ROOT__|$REPO/skills|g" "$src" > "$dst"
  ok "SKILLS.md (raiz: $REPO/skills)"
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
  # Merge reconciliador: hooks OSForge-managed (.claude/hooks/) refletem sempre
  # o repo (matcher/command atualizados, removidos somem); hooks próprios do
  # usuário em settings.json são preservados intactos. Idempotente.
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

# Merge reconciliador: hooks OSForge-managed (command referencia
# ".claude/hooks/") são AUTORITATIVOS — reflete sempre o repo (matcher +
# command atualizados, hooks removidos somem). Hooks próprios do usuário
# (qualquer outro command) são preservados. Idempotente.
new_hooks = new_data.get("hooks", {})
cur_hooks  = current.setdefault("hooks", {})

def _is_managed(cmd):
    return "/.claude/hooks/" in (cmd or "")

def _entry_all_managed(entry):
    cmds = [h.get("command", "") for h in entry.get("hooks", [])]
    return bool(cmds) and all(_is_managed(c) for c in cmds)

for event, new_entries in new_hooks.items():
    # Preserva entradas do usuário; descarta as nossas (possivelmente stale)
    kept = [e for e in cur_hooks.get(event, []) if not _entry_all_managed(e)]
    # Re-adiciona as do repo (cópia profunda via round-trip JSON)
    fresh = json.loads(json.dumps(new_entries))
    cur_hooks[event] = kept + fresh

with open(settings, "w") as f:
    json.dump(current, f, indent=2, ensure_ascii=False)
print("  ✅ settings.json merged (OSForge-managed reconciliados; user hooks preservados)")
PYEOF
}


merge_settings_claude() {
  # Merge não-destrutivo de claude-code/settings-base.json em ~/.claude/settings.json.
  # Chaves top-level do base são autoritativas; env é mesclado chave-a-chave
  # (preserva o env do usuário); qualquer outra config do usuário é preservada.
  # Objetivo: cortar bloat de contexto de MCP (disableClaudeAiConnectors, ENABLE_TOOL_SEARCH).
  local base_src="$REPO/claude-code/settings-base.json"
  local settings="$CLAUDE/settings.json"
  [ -f "$base_src" ] || return 0
  if $DRY_RUN; then skip "merge settings-base.json → settings.json (disableClaudeAiConnectors, ENABLE_TOOL_SEARCH)"; return; fi
  backup_file "$settings"
  BASE_SRC="$base_src" SETTINGS="$settings" python3 - <<'PYEOF'
import json, os
base_src = os.environ['BASE_SRC']; settings = os.environ['SETTINGS']
with open(base_src) as f: base = json.load(f)
base.pop('_comment', None)
base.pop('_unset_rationale', None)
# _unset: caminhos "a.b" que o OSForge quer REMOVER da settings viva. Sem isso o
# merge só sabe adicionar, e uma configuração empurrada por engano fica presa
# para sempre em ~/.claude/settings.json. Mesma classe de problema que o merge
# reconciliador de hooks já resolve.
unset_paths = base.pop('_unset', [])
try:
    with open(settings) as f: cur = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    cur = {}
applied = []
for path in unset_paths:
    parts = path.split('.')
    node = cur
    for p in parts[:-1]:
        node = node.get(p) if isinstance(node, dict) else None
        if node is None: break
    if isinstance(node, dict) and parts[-1] in node:
        node.pop(parts[-1])
        applied.append(f"-{path}")
for k, v in base.items():
    if k == 'env' and isinstance(v, dict):
        env = cur.setdefault('env', {})
        for ek, ev in v.items():
            if env.get(ek) != ev: applied.append(f"env.{ek}={ev}")
            env[ek] = ev
    else:
        if cur.get(k) != v: applied.append(f"{k}={v}")
        cur[k] = v
with open(settings, 'w') as f: json.dump(cur, f, indent=2, ensure_ascii=False)
print("  ✅ settings-base aplicado: " + (", ".join(applied) if applied else "já em paridade"))
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

# ── Skills deploy (Model A: core allowlist, ou todas com --all-skills) ────
# Deploya só as skills listadas em claude-code/skills-core.txt (paths relativos
# sob skills/). As demais permanecem no repo, indexadas em SKILLS.md, e são
# puxadas por projeto via scripts/install-skill.sh. --all-skills volta ao antigo.
deploy_skills() {
  local dst="$1"
  local manifest="$REPO/claude-code/skills-core.txt"

  if $DRY_RUN; then
    if $DEPLOY_ALL_SKILLS || [ ! -f "$manifest" ]; then skip "rsync TODAS skills/ → $dst"
    else skip "deploy core skills (~$(grep -cvE '^[[:space:]]*(#|$)' "$manifest" 2>/dev/null || echo '?') dirs) → $dst"; fi
    return
  fi

  mkdir -p "$dst"

  if $DEPLOY_ALL_SKILLS || [ ! -f "$manifest" ]; then
    # Buckets de ciclo de vida ficam de fora mesmo em --all-skills: uma skill
    # aposentada deployada volta a competir por gatilho, que é justamente o que
    # aposentá-la deveria impedir.
    rsync -a --delete --exclude '_deprecated/' --exclude '_in-progress/' --exclude 'archify/' "$REPO/skills/" "$dst/"
    ok "$(find "$dst" -name 'SKILL.md' | wc -l | tr -d ' ') skills sincronizadas (todas, exceto buckets _)"
    return
  fi

  # Stage apenas o core, depois rsync --delete espelha exatamente o allowlist.
  #
  # ACHATADO no destino: a descoberta nativa do Claude Code só varre UM nível
  # (~/.claude/skills/<dir>/SKILL.md). Preservar o caminho do repo
  # (planning/phase-discussion) deixava as 17 skills aninhadas do core
  # invisíveis em runtime — medido no init de sessão real: todas as flat
  # apareciam, nenhuma aninhada. Pré-condições verificadas: basenames do core
  # não colidem e o `name:` do frontmatter é igual ao basename.
  local stage; stage="$(mktemp -d)"
  while IFS= read -r rel; do
    rel="${rel%$'\r'}"                          # tolera CRLF
    case "$rel" in ''|\#*) continue ;; esac     # ignora vazias/comentários
    local src="$REPO/skills/$rel"
    if [ ! -d "$src" ]; then echo "  ⚠️  core skill ausente no repo: $rel" >&2; continue; fi
    local flat; flat="$(basename "$rel")"
    if [ -e "$stage/$flat" ]; then
      echo "  ❌ colisão de basename no core: '$rel' vs skill já staged como '$flat' — ajuste skills-core.txt" >&2
      rm -rf "$stage"; exit 1
    fi
    cp -a "$src" "$stage/$flat"
  done < "$manifest"
  # `archify/` é instalado por deploy_archify (terceiro, pinado) e não existe no
  # repo — excluído para que o --delete não o apague a cada deploy.
  rsync -a --delete --exclude 'archify/' "$stage/" "$dst/"
  rm -rf "$stage"
  ok "$(find "$dst" -name 'SKILL.md' | wc -l | tr -d ' ') skills core sincronizadas (demais via install-skill.sh)"
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
  log "Skills (Model A: core global + domínio on-demand):"
  deploy_skills "$CLAUDE/skills"

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
  log "Settings base → settings.json (anti-bloat de contexto MCP):"
  merge_settings_claude

  echo ""
  log "CLAUDE.md + SKILLS.md + CONTEXT.md:"
  copy_file "$REPO/claude-code/CLAUDE.md" "$CLAUDE/CLAUDE.md" true
  copy_skills_md "$CLAUDE/SKILLS.md"
  copy_file "$REPO/claude-code/CONTEXT.md" "$CLAUDE/CONTEXT.md"

  log "Authoring templates/standards → docs/:"
  mkdir -p "$CLAUDE/docs"
  copy_file "$REPO/docs/PLAN.template.md"   "$CLAUDE/docs/PLAN.template.md"
  copy_file "$REPO/docs/SKILL.template.md"  "$CLAUDE/docs/SKILL.template.md"
  copy_file "$REPO/docs/SKILL-STANDARD.md"  "$CLAUDE/docs/SKILL-STANDARD.md"

  echo ""
  log "MCPs → ~/.claude.json (sync não-destrutivo):"
  MCP_SRC="$REPO/mcp/claude-code.json" CLAUDE_JSON="$HOME/.claude.json" sync_mcps_claude


  echo ""
  log "Verificar drift MCPs:"
  # REPO via env: hardcoding ~/Development/osforge broke any clone living elsewhere.
  MCP_SRC="$REPO/mcp/claude-code.json" python3 - <<'PYEOF'
import json, os
with open(os.environ["MCP_SRC"]) as f:
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
  # Âncora: helpers rodando de ~/.local/bin não conseguem derivar o repo da
  # própria posição. Escrita aqui, lida por install-skill.sh / install-mcp.sh.
  printf '%s\n' "$REPO" > "$db_dir/repo-path"
  cp "$script_src" "$db_bin"
  chmod +x "$db_bin"
  ok "osforge-db instalado em $db_bin"

  # O protocolo de resolução do MANIFEST manda rodar `install-skill.sh <nome>`
  # de dentro de um projeto satélite — então ele precisa estar no PATH, não só
  # no repo. Idem install-mcp.sh, citado no CLAUDE.md global.
  for helper in install-skill install-mcp; do
    if [ -f "$REPO/scripts/${helper}.sh" ]; then
      cp "$REPO/scripts/${helper}.sh" "$HOME/.local/bin/${helper}"
      chmod +x "$HOME/.local/bin/${helper}"
      ok "${helper} instalado em ~/.local/bin/${helper}"
    fi
  done

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

# ── Deploy Archify (terceiro, pinado) ────────────────────────────────────
# Instala o pacote da skill `archify/` do tarball da tag pinada em cada
# <dst>/skills/archify. Slim: sem test/ (1,3 MB) e sem examples/*.html (3,6 MB);
# os examples/*.json ficam porque a SKILL.md e o `doctor` os leem.
# Idempotente: compara skill-release.json com ARCHIFY_VERSION.
archify_installed_version() {
  local rel="$1/skill-release.json"
  [ -f "$rel" ] || { echo ""; return; }
  sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$rel" | head -1
}

deploy_archify() {
  $DEPLOY_ARCHIFY || { log "Archify: pulado (--no-archify)"; return 0; }

  local targets=()
  $DEPLOY_CLAUDE && targets+=("$CLAUDE/skills/archify")
  $DEPLOY_CURSOR && targets+=("$CURSOR/skills/archify")

  echo ""
  echo "🗺️  Archify v$ARCHIFY_VERSION (github.com/$ARCHIFY_REPO, MIT)"

  local pending=()
  for dst in "${targets[@]}"; do
    local have; have="$(archify_installed_version "$dst")"
    if [ "$have" = "$ARCHIFY_VERSION" ]; then ok "já instalado em $dst"
    else pending+=("$dst"); fi
  done
  [ ${#pending[@]} -eq 0 ] && return 0

  if $DRY_RUN; then
    for dst in "${pending[@]}"; do skip "baixar v$ARCHIFY_VERSION → $dst"; done
    return 0
  fi

  if ! command -v node >/dev/null 2>&1; then
    echo "  ⚠️  node não encontrado — Archify precisa de Node ≥ 18; pulando (system-diagrams usa o fallback Mermaid)"
    return 0
  fi
  local node_major; node_major="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)"
  if [ "${node_major:-0}" -lt 18 ]; then
    echo "  ⚠️  node $(node --version) < 18 — pulando Archify"
    return 0
  fi

  local tmp; tmp="$(mktemp -d)"
  local url="https://github.com/$ARCHIFY_REPO/archive/refs/tags/v$ARCHIFY_VERSION.tar.gz"
  log "baixando $url"
  if ! curl -fsSL --retry 2 -o "$tmp/archify.tgz" "$url"; then
    echo "  ⚠️  download falhou — Archify não instalado (rode ./deploy.sh --with-archify depois)"
    rm -rf "$tmp"; return 0
  fi
  if ! tar -xzf "$tmp/archify.tgz" -C "$tmp"; then
    echo "  ⚠️  tarball inválido — Archify não instalado"; rm -rf "$tmp"; return 0
  fi
  local src; src="$(find "$tmp" -maxdepth 2 -type d -name archify | head -1)"
  if [ -z "$src" ] || [ ! -f "$src/SKILL.md" ] || [ ! -f "$src/bin/archify.mjs" ]; then
    echo "  ⚠️  layout inesperado no tarball (sem archify/SKILL.md) — não instalado"; rm -rf "$tmp"; return 0
  fi
  rm -rf "$src/test"
  rm -f "$src"/examples/*.html

  for dst in "${pending[@]}"; do
    mkdir -p "$dst"
    rsync -a --delete "$src/" "$dst/"
    if node "$dst/bin/archify.mjs" doctor >/dev/null 2>&1; then
      ok "v$ARCHIFY_VERSION → $dst ($(du -sh "$dst" | cut -f1), doctor ok)"
    else
      echo "  ⚠️  instalado em $dst mas \`node bin/archify.mjs doctor\` falhou — verifique manualmente"
    fi
  done
  rm -rf "$tmp"
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
  log "Skills (Model A: core global + domínio on-demand):"
  deploy_skills "$CURSOR/skills"

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
  log "SKILLS.md + CONTEXT.md:"
  copy_skills_md "$CURSOR/SKILLS.md"
  copy_file "$REPO/claude-code/CONTEXT.md" "$CURSOR/CONTEXT.md"

  log "Authoring templates/standards → docs/:"
  mkdir -p "$CURSOR/docs"
  copy_file "$REPO/docs/PLAN.template.md"   "$CURSOR/docs/PLAN.template.md"
  copy_file "$REPO/docs/SKILL.template.md"  "$CURSOR/docs/SKILL.template.md"
  copy_file "$REPO/docs/SKILL-STANDARD.md"  "$CURSOR/docs/SKILL-STANDARD.md"

  echo ""
  ok "Cursor deploy completo"
}

# ── Pre-flight: o índice não pode divergir do acervo ─────────────────────
# Model A deploya só o core; as demais skills só existem para o agente através
# do MANIFEST em SKILLS.md. Índice desatualizado = skill invisível. Falha cedo.
preflight_manifest() {
  echo ""
  echo "🔍 Pre-flight: manifesto de skills"
  if ! command -v python3 &>/dev/null; then
    echo "  ⚠️  python3 ausente — pulando verificação do manifesto"
    return 0
  fi
  if python3 "$REPO/scripts/_generate_manifest.py" --check; then
    ok "manifesto sincronizado com skills/"
  else
    echo ""
    echo "  ❌ O MANIFEST em claude-code/SKILLS.md está desatualizado."
    echo "     Skills fora dele são invisíveis para o agente em runtime."
    echo "     Corrija com: python3 scripts/_generate_manifest.py"
    exit 1
  fi
}

# ── Main ─────────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════"
echo " OSForge v$OSFORGE_VERSION — Deploy"
echo " Repo: $REPO"
$DRY_RUN && echo " Modo: DRY RUN (sem alterações reais)"
echo "═══════════════════════════════════════════════════"

preflight_manifest

$DEPLOY_CLAUDE && deploy_claude
$DEPLOY_CURSOR && deploy_cursor
deploy_archify || true  # terceiro, opcional; falha de rede não aborta o deploy
deploy_osforge_db
deploy_qdrant || true   # Qdrant é opt-in; falha (Docker ausente etc.) não aborta o deploy

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ Deploy finalizado"
echo "═══════════════════════════════════════════════════"

# ── Verificar dependências opcionais ─────────────────────────────────────
echo ''
echo '🔍 Verificando dependências opcionais...'
if $DEPLOY_ARCHIFY && [ -f "$CLAUDE/skills/archify/bin/archify.mjs" ]; then
  echo "  ✅ archify: v$(archify_installed_version "$CLAUDE/skills/archify")"
elif $DEPLOY_ARCHIFY; then
  echo '  ⚠️  archify não instalado — skill system-diagrams usará o fallback Mermaid'
  echo '     Instalar: ./deploy.sh --with-archify'
fi
if command -v llmfit &>/dev/null; then
  LLMFIT_VER=$(llmfit --version 2>/dev/null | head -1 || echo 'instalado')
  echo "  ✅ llmfit: $LLMFIT_VER"
else
  echo '  ⚠️  llmfit não encontrado — skill llmfit-advisor não estará disponível'
  echo '     Instalar: brew tap AlexsJones/llmfit && brew install llmfit'
  echo '     Ou via Rust: cargo install llmfit'
fi
