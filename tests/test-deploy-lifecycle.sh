#!/usr/bin/env bash
# tests/test-deploy-lifecycle.sh — B-017: o deploy com estado não perde nada seu.
#
# Roda o deploy REAL (./deploy.sh) contra um HOME temporário semeado com
# arquivos do usuário e verifica, por execução, as garantias do ADR-015:
#   1. hook seu em ~/.claude/hooks/ + entrada sua em settings.json sobrevivem
#   2. skill sua em ~/.claude/skills/ sobrevive
#   3. arquivo seu que colide com um do OSForge é mantido (e avisado)
#   4. chave sua em settings.json e env sobrevivem ao merge do settings-base
#   5. segundo deploy é idempotente (árvore byte-idêntica, backups não crescem)
#   6. --doctor detecta arquivo gerenciado alterado; o deploy mantém sua edição
#      com backup; --force sobrescreve; --restore devolve a sua versão
#   7. hook gerenciado editado em settings.json aborta o deploy; --force-hooks sobrepõe
#   8. skill que sai do core é removida; a sua e a instalada com --global ficam
#   9. instalação legada (arquivo igual a uma revisão antiga do repo) é reconhecida
#      e atualizada, não tratada como colisão
#  10. --uninstall remove só o que é do OSForge e restaura settings; o seu fica
#  11. --dry-run num HOME vazio não cria nada
#
# Tudo acontece em mktemp; nunca toca o $HOME real. Sem rede (--no-archify --no-qdrant).
# Uso: tests/test-deploy-lifecycle.sh   (exit 0 = tudo verde; 1 = alguma garantia falhou)
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
REAL_HOME="$HOME"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PASS=0; FAIL=0
ok()   { PASS=$((PASS+1)); echo "  ✅ $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }   # check "label" "bash condition"
section(){ echo ""; echo "── $1"; }

# rsync não é usado no caminho com estado; se faltar no PATH, um stub que FALHA
# satisfaz o preflight e ao mesmo tempo prova que o caminho novo não o chama.
mkdir -p "$WORK/bin"
if ! command -v rsync >/dev/null 2>&1; then
  printf '#!/bin/sh\necho "rsync chamado pelo caminho com estado" >&2; exit 97\n' > "$WORK/bin/rsync"; chmod +x "$WORK/bin/rsync"
fi
export PATH="$WORK/bin:$PATH"
export OSFORGE_SKIP_PREFLIGHT_TESTS=1     # o preflight roda ESTA suíte; evita recursão

# Cópia de trabalho do repo (o teste edita skills-core.txt para simular aposentadoria)
# com o .git preservado: o reconhecimento de instalação legada consulta o histórico.
cp -R "$REPO" "$WORK/repo"
R="$WORK/repo"

set_core() {  # set_core add|del <rel> — edita skills-core.txt da cópia e regenera o MANIFEST (preflight exige)
  if [ "$1" = del ]; then grep -vxF "$2" "$R/claude-code/skills-core.txt" > "$R/claude-code/skills-core.tmp" && mv "$R/claude-code/skills-core.tmp" "$R/claude-code/skills-core.txt"
  else echo "$2" >> "$R/claude-code/skills-core.txt"; fi
  (cd "$R" && python3 scripts/_generate_manifest.py >/dev/null 2>&1)
}
deploy() {  # deploy <home> [flags...] → stdout+stderr em $OUT, código em $RC
  local home="$1"; shift
  OUT="$(HOME="$home" "$R/deploy.sh" --claude-only --no-archify --no-qdrant "$@" 2>&1)"; RC=$?
}
sha() { if command -v sha256sum >/dev/null 2>&1; then sha256sum | cut -c1-64; else shasum -a 256 | cut -c1-64; fi; }  # macOS sem coreutils
tree_sha() {  # hash de conteúdo+caminho+modo de uma árvore (sem timestamps)
  (cd "$1" && find . -type f | LC_ALL=C sort | while IFS= read -r f; do
     printf '%s %s ' "$f" "$(stat -c %a "$f" 2>/dev/null || stat -f %Lp "$f")"; sha < "$f"; done) | sha | cut -c1-16
}
jq_py() { python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print($2)" "$1" 2>/dev/null; }

# ─────────────────────────────────────────────────────────────────────────────
section "Semente: HOME com arquivos do usuário"
H="$WORK/home"; mkdir -p "$H/.claude/hooks" "$H/.claude/skills/my-skill" "$H/.claude/skills/global-skill" "$H/.claude/docs"
printf '#!/bin/sh\necho user-hook\n' > "$H/.claude/hooks/my-hook.sh"; chmod +x "$H/.claude/hooks/my-hook.sh"
printf -- '---\nname: my-skill\n---\nminha skill\n' > "$H/.claude/skills/my-skill/SKILL.md"
printf -- '---\nname: global-skill\n---\ninstalada com install-skill --global\n' > "$H/.claude/skills/global-skill/SKILL.md"
printf '# meu CLAUDE.md pessoal\n' > "$H/.claude/CLAUDE.md"            # colide com claude-code/CLAUDE.md
printf 'template meu\n' > "$H/.claude/docs/PLAN.template.md"          # colide com docs/PLAN.template.md
cat > "$H/.claude/settings.json" <<'EOF'
{
  "theme": "dark",
  "env": { "MY_VAR": "1" },
  "hooks": {
    "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "$HOME/.claude/hooks/my-hook.sh" } ] } ],
    "Stop": [ { "hooks": [ { "type": "command", "command": "$HOME/.claude/hooks/my-hook.sh" } ] } ]
  }
}
EOF
printf '{"mcpServers":{"my-mcp":{"command":"echo"}}}\n' > "$H/.claude.json"
# Instalação legada: um hook do OSForge de uma revisão ANTIGA do repo (sem estado)
OLD_COMMIT="$(git -C "$R" log --format=%H -n 2 -- hooks/notify-done.sh | tail -1)"
if [ -n "$OLD_COMMIT" ] && git -C "$R" show "$OLD_COMMIT:hooks/notify-done.sh" > "$H/.claude/hooks/notify-done.sh" 2>/dev/null \
   && ! cmp -s "$H/.claude/hooks/notify-done.sh" "$R/hooks/notify-done.sh"; then
  LEGACY=1; chmod +x "$H/.claude/hooks/notify-done.sh"
else
  LEGACY=0; rm -f "$H/.claude/hooks/notify-done.sh"; echo "  (sem revisão antiga distinta de notify-done.sh; item 9 pulado)"
fi
ok "semeado"

# ─────────────────────────────────────────────────────────────────────────────
section "1º deploy: nada seu se perde"
deploy "$H"
check "deploy sai com 0" '[ $RC -eq 0 ]'
check "rsync não foi chamado" '! grep -q "rsync chamado" <<<"$OUT"'
check "estado gravado" '[ -f "$H/.osforge/install-state.json" ]'
check "hook seu continua no disco" '[ -x "$H/.claude/hooks/my-hook.sh" ]'
check "entrada sua (PreToolUse) continua em settings.json" '[ "$(jq_py "$H/.claude/settings.json" "sum(1 for g in d[\"hooks\"][\"PreToolUse\"] if \"my-hook\" in g[\"hooks\"][0][\"command\"])")" = 1 ]'
check "entrada sua (Stop) continua em settings.json" '[ "$(jq_py "$H/.claude/settings.json" "sum(1 for g in d[\"hooks\"][\"Stop\"] if \"my-hook\" in g[\"hooks\"][0][\"command\"])")" = 1 ]'
N_GROUPS="$(python3 -c "import json,sys; print(sum(len(v) for v in json.load(open(sys.argv[1]))[\"hooks\"].values()))" "$R/hooks/hooks-claude-code.json")"
check "hooks do OSForge registrados ($N_GROUPS grupos, como no JSON)" '[ "$(jq_py "$H/.osforge/install-state.json" "len(d[\"hooks\"])")" = "$N_GROUPS" ]'
check "skill sua sobrevive" '[ -f "$H/.claude/skills/my-skill/SKILL.md" ]'
check "skill --global sobrevive" '[ -f "$H/.claude/skills/global-skill/SKILL.md" ]'
check "skills core instaladas" '[ "$(find "$H/.claude/skills" -name SKILL.md | wc -l)" -gt 40 ]'
check "CLAUDE.md seu mantido (colisão avisada)" 'grep -q "meu CLAUDE.md pessoal" "$H/.claude/CLAUDE.md" && grep -q "CLAUDE.md: existe e não é do OSForge" <<<"$OUT"'
check "PLAN.template.md seu mantido" 'grep -q "template meu" "$H/.claude/docs/PLAN.template.md"'
check "dica de --adopt exibida" 'grep -q -- "--adopt" <<<"$OUT"'
check "theme seu preservado" '[ "$(jq_py "$H/.claude/settings.json" "d[\"theme\"]")" = dark ]'
check "env seu preservado + env do OSForge" '[ "$(jq_py "$H/.claude/settings.json" "d[\"env\"][\"MY_VAR\"]+d[\"env\"][\"ENABLE_TOOL_SEARCH\"]")" = 1true ]'
check "MCP seu preservado + Context7 adicionado" '[ "$(jq_py "$H/.claude.json" "sorted(d[\"mcpServers\"])")" = "['"'"'Context7'"'"', '"'"'my-mcp'"'"']" ]'
check "banco global criado" '[ -f "$H/.osforge/osforge.db" ]'
if [ "$LEGACY" = 1 ]; then
  check "instalação legada reconhecida e atualizada" 'grep -q "notify-done.sh: versão antiga do OSForge" <<<"$OUT" && cmp -s "$H/.claude/hooks/notify-done.sh" "$R/hooks/notify-done.sh"'
fi
# só os dois JSONs de fato alterados (hooks/settings e MCPs) são copiados para o backup do run
check "backup do 1º deploy contém só settings.json e .claude.json" '[ "$(cd "$H/.claude_backups" && find . -type f | LC_ALL=C sort | sed "s|^\./[^/]*/||" | tr "\n" " ")" = ".claude.json .claude/settings.json " ]'
HOME="$H" "$R/deploy.sh" --doctor >/dev/null 2>&1; check "--doctor limpo após deploy" '[ $? -eq 0 ]'
RUN1="$(jq_py "$H/.osforge/install-state.json" "d[\"run_id\"]")"

# ─────────────────────────────────────────────────────────────────────────────
section "2º deploy: idempotente"
BEFORE="$(tree_sha "$H/.claude")"; BK_BEFORE="$(find "$H/.claude_backups" -type f 2>/dev/null | wc -l)"
deploy "$H"
check "deploy sai com 0" '[ $RC -eq 0 ]'
check "árvore ~/.claude byte-idêntica" '[ "$(tree_sha "$H/.claude")" = "$BEFORE" ]'
check "backups não cresceram" '[ "$(find "$H/.claude_backups" -type f 2>/dev/null | wc -l)" = "$BK_BEFORE" ]'
check "hooks em paridade" 'grep -q "hooks: em paridade" <<<"$OUT"'
check "settings já em paridade" 'grep -q "já em paridade" <<<"$OUT"'
check "nada copiado" '! grep -q "copied=" <<<"$OUT"'

# ─────────────────────────────────────────────────────────────────────────────
section "Arquivo gerenciado editado por você"
MANAGED="$H/.claude/hooks/protect-tests.sh"
echo "# minha edição" >> "$MANAGED"; EDITED_SHA="$(sha < "$MANAGED")"
HOME="$H" "$R/deploy.sh" --doctor > "$WORK/doctor.log" 2>&1; DRC=$?
check "--doctor sai com 1 e aponta o arquivo" '[ $DRC -eq 1 ] && grep -q "alterado: .claude/hooks/protect-tests.sh" "$WORK/doctor.log"'
deploy "$H"
check "deploy mantém sua edição" '[ $RC -eq 0 ] && [ "$(sha < "$MANAGED")" = "$EDITED_SHA" ] && grep -q "kept-user-edit=1" <<<"$OUT"'
RUN_KEEP="$(jq_py "$H/.osforge/install-state.json" "d[\"run_id\"]")"
check "backup da sua versão gravado" '[ -f "$H/.claude_backups/$RUN_KEEP/.claude/hooks/protect-tests.sh" ]'
deploy "$H" --force
check "--force sobrescreve" '[ $RC -eq 0 ] && cmp -s "$MANAGED" "$R/hooks/protect-tests.sh" && grep -q "forced=1" <<<"$OUT"'
RUN_FORCE="$(jq_py "$H/.osforge/install-state.json" "d[\"run_id\"]")"
HOME="$H" "$R/deploy.sh" --doctor >/dev/null 2>&1; check "--doctor limpo após --force" '[ $? -eq 0 ]'
HOME="$H" "$R/deploy.sh" --restore="$RUN_FORCE" >/dev/null 2>&1
check "--restore devolve sua versão" '[ "$(sha < "$MANAGED")" = "$EDITED_SHA" ]'
deploy "$H" --force; check "re-força para seguir" '[ $RC -eq 0 ]'

# ─────────────────────────────────────────────────────────────────────────────
section "Hook gerenciado editado em settings.json"
python3 - "$H/.claude/settings.json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
for g in d["hooks"]["Stop"]:
    if "route-guard" in g["hooks"][0]["command"]:
        g["hooks"][0]["timeout"] = 99
json.dump(d, open(p, "w"), indent=2)
EOF
deploy "$H"
check "deploy aborta sem sobrescrever" '[ $RC -ne 0 ] && grep -q "não vou sobrescrever" <<<"$OUT"'
check "sua edição do hook permanece" '[ "$(jq_py "$H/.claude/settings.json" "[g[\"hooks\"][0].get(\"timeout\") for g in d[\"hooks\"][\"Stop\"] if \"route-guard\" in g[\"hooks\"][0][\"command\"]]")" = "[99]" ]'
deploy "$H" --force-hooks
check "--force-hooks sobrepõe" '[ $RC -eq 0 ] && [ "$(jq_py "$H/.claude/settings.json" "[g[\"hooks\"][0].get(\"timeout\") for g in d[\"hooks\"][\"Stop\"] if \"route-guard\" in g[\"hooks\"][0][\"command\"]]")" = "[None]" ]'
check "hook seu ainda lá depois do --force-hooks" '[ "$(jq_py "$H/.claude/settings.json" "sum(1 for g in d[\"hooks\"][\"Stop\"] if \"my-hook\" in g[\"hooks\"][0][\"command\"])")" = 1 ]'

# ─────────────────────────────────────────────────────────────────────────────
section "Skill que sai do core é aposentada; as suas ficam"
RETIRE_REL="$(grep -vE '^[[:space:]]*(#|$)' "$R/claude-code/skills-core.txt" | tail -1)"
RETIRE="$(basename "$RETIRE_REL")"
check "skill core '$RETIRE' estava instalada" '[ -f "$H/.claude/skills/$RETIRE/SKILL.md" ]'
set_core del "$RETIRE_REL"
deploy "$H"
check "deploy sai com 0" '[ $RC -eq 0 ]'
check "skill aposentada removida" '[ ! -e "$H/.claude/skills/$RETIRE" ] && grep -q "aposentado: .claude/skills/$RETIRE/SKILL.md" <<<"$OUT"'
check "skill sua sobrevive" '[ -f "$H/.claude/skills/my-skill/SKILL.md" ]'
check "skill --global sobrevive" '[ -f "$H/.claude/skills/global-skill/SKILL.md" ]'
# skill aposentada mas editada por você → retida
set_core add "$RETIRE_REL"; deploy "$H"; check "skill volta ao core" '[ -f "$H/.claude/skills/$RETIRE/SKILL.md" ]'
echo "# minha nota" >> "$H/.claude/skills/$RETIRE/SKILL.md"
set_core del "$RETIRE_REL"
deploy "$H"
check "skill aposentada MAS editada por você é retida" '[ -f "$H/.claude/skills/$RETIRE/SKILL.md" ] && grep -q "retained=1" <<<"$OUT"'
set_core add "$RETIRE_REL"; deploy "$H" --force

# ─────────────────────────────────────────────────────────────────────────────
section "--uninstall: só o que é do OSForge sai; settings restaurados"
HOME="$H" "$R/deploy.sh" --uninstall --dry-run > "$WORK/un-dry.log" 2>&1
check "--uninstall --dry-run não remove nada" '[ -f "$H/.osforge/install-state.json" ] && [ -f "$H/.claude/hooks/gateguard.py" ]'
HOME="$H" "$R/deploy.sh" --uninstall > "$WORK/un.log" 2>&1; URC=$?
check "--uninstall sai com 0" '[ $URC -eq 0 ]'
check "estado removido" '[ ! -f "$H/.osforge/install-state.json" ]'
check "hooks do OSForge removidos do disco" '[ ! -e "$H/.claude/hooks/gateguard.py" ] && [ ! -e "$H/.claude/hooks/route-guard.py" ]'
check "skills core removidas" '[ ! -e "$H/.claude/skills/$RETIRE" ]'
check "hook seu + skill sua + CLAUDE.md seu ficam" '[ -x "$H/.claude/hooks/my-hook.sh" ] && [ -f "$H/.claude/skills/my-skill/SKILL.md" ] && grep -q "meu CLAUDE.md pessoal" "$H/.claude/CLAUDE.md"'
check "hooks do OSForge saem de settings.json; os seus ficam" '[ "$(jq_py "$H/.claude/settings.json" "sum(len(v) for v in d[\"hooks\"].values())")" = 2 ]'
check "chaves do settings-base revertidas; as suas ficam" '[ "$(jq_py "$H/.claude/settings.json" "(\"disableClaudeAiConnectors\" in d, \"ENABLE_TOOL_SEARCH\" in d[\"env\"], d[\"env\"][\"MY_VAR\"], d[\"theme\"])")" = "(False, False, '"'"'1'"'"', '"'"'dark'"'"')" ]'
check "MCP do OSForge removido; o seu fica" '[ "$(jq_py "$H/.claude.json" "sorted(d[\"mcpServers\"])")" = "['"'"'my-mcp'"'"']" ]'
check "banco global (dados seus) preservado" '[ -f "$H/.osforge/osforge.db" ]'
check "SKILLS.md, CONTEXT.md e agents removidos" '[ ! -e "$H/.claude/SKILLS.md" ] && [ ! -e "$H/.claude/CONTEXT.md" ] && [ ! -d "$H/.claude/agents" ]'

# ─────────────────────────────────────────────────────────────────────────────
section "--dry-run num HOME vazio não cria nada"
H2="$WORK/home-empty"; mkdir -p "$H2"
deploy "$H2" --dry-run
check "dry-run sai com 0" '[ $RC -eq 0 ]'
check "nenhum arquivo criado" '[ -z "$(find "$H2" -type f)" ]'
check "dry-run relata o que faria" 'grep -q "\[dry-run\] arquivos: copied=" <<<"$OUT"'

# ─────────────────────────────────────────────────────────────────────────────
section "Deploy em HOME vazio + uninstall = HOME vazio (exceto dados)"
H3="$WORK/home-fresh"; mkdir -p "$H3"
deploy "$H3"; check "deploy em HOME vazio sai com 0" '[ $RC -eq 0 ]'
HOME="$H3" "$R/deploy.sh" --uninstall >/dev/null 2>&1
LEFT="$(cd "$H3" && find . -type f | LC_ALL=C sort | tr '\n' ' ')"
# .osforge/config.json (backend vetorial) e osforge.db são DADOS seus, não arquivos gerenciados: ficam.
check "só sobram dados e o settings.json vazio" '[ "$LEFT" = "./.claude.json ./.claude/settings.json ./.osforge/config.json ./.osforge/osforge.db " ] || { echo "   sobrou: $LEFT"; false; }'

echo ""
echo "══ lifecycle: $PASS ok, $FAIL falha(s)"
[ "$FAIL" -eq 0 ]
