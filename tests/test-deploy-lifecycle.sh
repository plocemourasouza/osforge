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
#  12. legacy embedder (Ollama) is not a deploy step: no embed-backfill, even when it answers
#  13. brain (ADR-017): osforge_brain.py lands next to osforge-db and imports from there;
#      --no-brain = one skip line, no venv; --dry-run only reports the venv/model/migrate steps;
#      an offline venv setup (pip unreachable) never aborts the deploy
#  14. deploy-source guard + --release (ADR-018): refuses non-main / dirty / no v* tag, --force-branch
#      and OSFORGE_DEPLOY_FORCE_BRANCH=1 pass, --dry-run reports, --release deploys the highest tag
#      (local bare remote, no network); every deploy call here passes --force-branch because this
#      working copy is a feature branch (and CI checks out a detached merge ref)
#
# Tudo acontece em mktemp; nunca toca o $HOME real. Sem rede (--no-archify --no-qdrant --no-brain).
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

# rsync não é usado no caminho com estado. O stub é criado SEMPRE, sombreando um rsync
# real se houver: numa máquina com rsync instalado (todo runner de CI tem) a asserção
# "não foi chamado" passaria de graça, provando nada. Com o stub que falha, qualquer
# chamada aparece no output e derruba o deploy.
mkdir -p "$WORK/bin"
printf '#!/bin/sh\necho "rsync chamado pelo caminho com estado" >&2; exit 97\n' > "$WORK/bin/rsync"
chmod +x "$WORK/bin/rsync"
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
  OUT="$(HOME="$home" "$R/deploy.sh" --force-branch --claude-only --no-archify --no-qdrant --no-brain "$@" 2>&1)"; RC=$?
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
NEW_COMMIT="$(git -C "$R" log --format=%H -n 1 -- hooks/notify-done.sh)"
OLD_COMMIT="$(git -C "$R" log --format=%H -n 2 -- hooks/notify-done.sh | tail -1)"
if [ -n "$OLD_COMMIT" ] && [ "$OLD_COMMIT" != "$NEW_COMMIT" ] && git -C "$R" show "$OLD_COMMIT:hooks/notify-done.sh" > "$H/.claude/hooks/notify-done.sh" 2>/dev/null \
   && ! cmp -s "$H/.claude/hooks/notify-done.sh" "$R/hooks/notify-done.sh"; then
  LEGACY=1; chmod +x "$H/.claude/hooks/notify-done.sh"
else
  LEGACY=0; rm -f "$H/.claude/hooks/notify-done.sh"; echo "  (sem revisão antiga distinta de notify-done.sh; item 9 pulado)"
fi
# Instalação legada de um arquivo GERADO: o SKILLS.md instalado é o do repo com
# __OSFORGE_SKILLS_ROOT__ expandido para o caminho da máquina, então nunca é
# byte-idêntico a uma revisão. Sem tratar isso, o manifesto que dirige a descoberta de
# skills ficaria congelado numa instalação legada, tratado como "arquivo seu".
# A comparação tem de ser entre o BLOB antigo e o arquivo atual do repo (os dois com o
# token), nunca entre o arquivo já gerado e o do repo: a substituição por si só já os faz
# diferentes, e num clone raso (`fetch-depth: 1`) isso semearia como "revisão antiga" um
# arquivo idêntico ao de hoje — foi assim que o caso passou aqui e reprovou no CI.
NEW_SK="$(git -C "$R" log --format=%H -n 1 -- claude-code/SKILLS.md)"
OLD_SK="$(git -C "$R" log --format=%H -n 2 -- claude-code/SKILLS.md | tail -1)"
if [ -n "$OLD_SK" ] && [ "$OLD_SK" != "$NEW_SK" ] \
   && git -C "$R" show "$OLD_SK:claude-code/SKILLS.md" > "$WORK/old-skills.md" 2>/dev/null \
   && ! cmp -s "$WORK/old-skills.md" "$R/claude-code/SKILLS.md"; then
  sed "s|__OSFORGE_SKILLS_ROOT__|$R/skills|g" "$WORK/old-skills.md" > "$H/.claude/SKILLS.md"
  LEGACY_GEN=1
else
  LEGACY_GEN=0; rm -f "$H/.claude/SKILLS.md"; echo "  (sem revisão antiga de SKILLS.md; item extra pulado)"
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
if [ "$LEGACY_GEN" = 1 ]; then
  check "arquivo GERADO de revisão antiga também é reconhecido (SKILLS.md)" 'grep -q "SKILLS.md: versão antiga do OSForge" <<<"$OUT"'
  check "…e fica com o conteúdo novo, com a raiz expandida" 'grep -q "Context Budget" "$H/.claude/SKILLS.md" && grep -q "$R/skills" "$H/.claude/SKILLS.md" && ! grep -q "__OSFORGE_SKILLS_ROOT__" "$H/.claude/SKILLS.md"'
  check "…e NÃO foi tratado como arquivo seu" '! grep -q "SKILLS.md: existe e não é do OSForge" <<<"$OUT"'
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
section "Legacy embedder: not a deploy step"
H4="$WORK/home-memory"; mkdir -p "$H4"
export OSFORGE_EMBED=mock                                # embedder "reachable": deploy still skips it
deploy "$H4"
unset OSFORGE_EMBED
check "deploy exits 0" '[ $RC -eq 0 ]'
check "deploy never runs embed-backfill" '! grep -q "embed-backfill" <<<"$OUT"'

# ─────────────────────────────────────────────────────────────────────────────
section "Brain runtime (ADR-017)"
H5="$WORK/home-brain"; mkdir -p "$H5"
deploy "$H5"
check "osforge_brain.py installed next to osforge-db" '[ -f "$H5/.local/bin/osforge_brain.py" ] && cmp -s "$H5/.local/bin/osforge_brain.py" "$R/scripts/osforge_brain.py"'
check "installed osforge-db imports the brain from ~/.local/bin (help lists recall)" 'HOME="$H5" python3 "$H5/.local/bin/osforge-db" 2>/dev/null | grep -q "recall"'
check "--no-brain → exit 0, one skip line, no venv" '[ $RC -eq 0 ] && [ "$(grep -c "brain runtime skipped (--no-brain)" <<<"$OUT")" = 1 ] && [ ! -e "$H5/.osforge/venv" ]'
OUT="$(HOME="$H5" "$R/deploy.sh" --force-branch --claude-only --no-archify --no-qdrant --dry-run 2>&1)"
check "dry-run → reports venv, model and migrate steps, creates no venv" 'grep -q "\[dry-run\] python3 -m venv" <<<"$OUT" && grep -q "\[dry-run\] osforge-db brain migrate" <<<"$OUT" && [ ! -e "$H5/.osforge/venv" ]'
OUT="$(HOME="$H5" PIP_INDEX_URL="http://127.0.0.1:9/simple" PIP_NO_CACHE_DIR=1 PIP_RETRIES=0 PIP_TIMEOUT=2 "$R/deploy.sh" --force-branch --claude-only --no-archify --no-qdrant 2>&1)"; RC=$?
check "pip unreachable → deploy exits 0 with one 'brain venv skipped' line" '[ $RC -eq 0 ] && [ "$(grep -c "brain venv skipped" <<<"$OUT")" = 1 ]'
check "brain pins in deploy.sh match VENV_PINS in osforge_brain.py" '[ "$(sed -n "s/^BRAIN_PINS=\"\(.*\)\"$/\1/p" "$R/deploy.sh")" = "$(python3 -c "import sys; sys.path.insert(0, sys.argv[1]); import osforge_brain as b; print(\" \".join(b.VENV_PINS))" "$R/scripts")" ]'

# ─────────────────────────────────────────────────────────────────────────────
section "Deploy em HOME vazio + uninstall = HOME vazio (exceto dados)"
H3="$WORK/home-fresh"; mkdir -p "$H3"
deploy "$H3"; check "deploy em HOME vazio sai com 0" '[ $RC -eq 0 ]'
HOME="$H3" "$R/deploy.sh" --uninstall >/dev/null 2>&1
LEFT="$(cd "$H3" && find . -type f | LC_ALL=C sort | tr '\n' ' ')"
# .osforge/config.json (backend vetorial) e osforge.db são DADOS seus, não arquivos gerenciados: ficam.
check "só sobram dados e o settings.json vazio" '[ "$LEFT" = "./.claude.json ./.claude/settings.json ./.osforge/config.json ./.osforge/osforge.db " ] || { echo "   sobrou: $LEFT"; false; }'

# ─────────────────────────────────────────────────────────────────────────────
section "Deploy-source guard + --release (ADR-018)"
# Throwaway git world: a work repo (this tree, fresh history), a local bare "origin", a clone.
W="$WORK/gitworld"; mkdir -p "$W/work"
(cd "$R" && tar --exclude=.git -cf - .) | tar -xf - -C "$W/work"
GIT() { git -c user.name=t -c user.email=t@example.invalid -c commit.gpgsign=false -c tag.gpgsign=false "$@"; }
( cd "$W/work" && GIT init -q -b main && GIT add -A && GIT commit -q -m c1 && GIT tag v1.9.0 \
  && GIT init -q --bare -b main "$W/origin.git" && GIT remote add origin "$W/origin.git" && GIT push -q origin main --tags ) >/dev/null 2>&1
GIT clone -q "$W/origin.git" "$W/clone" >/dev/null 2>&1
G="$W/clone"
check "fixture: clone is main at v1.9.0" '[ "$(git -C "$G" describe --tags --exact-match HEAD 2>/dev/null)" = v1.9.0 ]'
# the release that --release must find, pushed AFTER the clone: v1.10.0 > v1.9.0 only by version sort
( cd "$W/work" && printf '1.10.0\n' > VERSION && GIT commit -q -am c2 && GIT tag v1.10.0 && GIT push -q origin main --tags ) >/dev/null 2>&1
gdeploy() {  # gdeploy <home> [flags...] — real deploy.sh of the clone, guard ACTIVE unless a flag/env says otherwise
  local home="$1"; shift
  OUT="$(HOME="$home" "$G/deploy.sh" --claude-only --no-archify --no-qdrant --no-brain "$@" 2>&1)"; RC=$?
}

HG="$WORK/hg-ok"; mkdir -p "$HG"; gdeploy "$HG"
check "clean main at a v* tag → deploys (exit 0, banner shows the ref)" '[ $RC -eq 0 ] && grep -q "Ref:  main @ v1.9.0" <<<"$OUT"'
check "banner names the official release (highest tag on main)" 'grep -q "official release v1.9.0" <<<"$OUT"'
check "install-state records the ref" 'grep -q "main @ v1.9.0" "$HG/.osforge/install-state.json"'

git -C "$G" checkout -q -b topic
HG="$WORK/hg-topic"; mkdir -p "$HG"; gdeploy "$HG"
check "non-main branch → refused, names the reason and the flag" '[ $RC -ne 0 ] && grep -q "branch is .topic., not main" <<<"$OUT" && grep -q -- "--force-branch" <<<"$OUT"'
check "refused deploy wrote nothing" '[ "$(find "$HG" -type f | wc -l | tr -d " ")" = 0 ]'
gdeploy "$HG" --force-branch
check "--force-branch on a non-main branch → deploys" '[ $RC -eq 0 ] && grep -q "guard bypassed" <<<"$OUT"'
HG2="$WORK/hg-topic-env"; mkdir -p "$HG2"; OUT="$(OSFORGE_DEPLOY_FORCE_BRANCH=1 HOME="$HG2" "$G/deploy.sh" --claude-only --no-archify --no-qdrant --no-brain 2>&1)"; RC=$?
check "OSFORGE_DEPLOY_FORCE_BRANCH=1 → deploys" '[ $RC -eq 0 ] && grep -q "guard bypassed" <<<"$OUT"'
HG3="$WORK/hg-topic-dry"; mkdir -p "$HG3"; gdeploy "$HG3" --dry-run
check "--dry-run reports the verdict and continues (exit 0, nothing written)" '[ $RC -eq 0 ] && grep -q "guard would REFUSE" <<<"$OUT" && grep -q "Deploy finalizado" <<<"$OUT" && [ "$(find "$HG3" -type f | wc -l | tr -d " ")" = 0 ]'
gdeploy "$HG" --doctor
check "--doctor is not guarded" '! grep -q "Refusing" <<<"$OUT"'
git -C "$G" checkout -q main

: > "$G/stray.txt"
HG4="$WORK/hg-dirty"; mkdir -p "$HG4"; gdeploy "$HG4"
check "dirty tree on main → refused" '[ $RC -ne 0 ] && grep -q "uncommitted changes" <<<"$OUT"'
mv "$G/stray.txt" "$WORK/stray.txt"

GIT -C "$G" commit -q --allow-empty -m local-work
HG5="$WORK/hg-untagged"; mkdir -p "$HG5"; gdeploy "$HG5"
check "main past its tag (HEAD not at a v* tag) → refused" '[ $RC -ne 0 ] && grep -q "not at a v\* tag" <<<"$OUT"'
gdeploy "$HG5" --force-branch
check "--force-branch deploys an untagged main" '[ $RC -eq 0 ]'

mv "$G/.git" "$G/.git.off"
HG6="$WORK/hg-tarball"; mkdir -p "$HG6"; gdeploy "$HG6" --dry-run
check "not a git checkout → no guard" '[ $RC -eq 0 ] && grep -q "not a git checkout" <<<"$OUT"'
mv "$G/.git.off" "$G/.git"

# --release: from a feature branch with a dirty tree, still deploys the highest tag from a detached worktree
git -C "$G" checkout -q -b wip; : > "$G/stray.txt"
HR="$WORK/hr"; mkdir -p "$HR"; gdeploy "$HR" --release
check "--release → exit 0 from a dirty feature branch" '[ $RC -eq 0 ] || { echo "$OUT" | tail -15; false; }'
check "--release picked v1.10.0 (version sort, not v1.9.0) in ~/.osforge/release/" '[ -f "$HR/.osforge/release/v1.10.0/VERSION" ] && [ ! -e "$HR/.osforge/release/v1.9.0" ]'
check "--release state says v1.10.0, source main (not 'detached')" 'grep -q "\"version\": \"1.10.0\"" "$HR/.osforge/install-state.json" && grep -q "main @ v1.10.0" "$HR/.osforge/install-state.json" && ! grep -q "detached @" "$HR/.osforge/install-state.json"'
check "--release guard and banner name main and the official release" 'grep -q "main @ v1.10.0 (official release v1.10.0), clean tree" <<<"$OUT" && grep -q "Ref:  main @ v1.10.0 · official release v1.10.0" <<<"$OUT"'
check "--release deploys the release's files, not the wip checkout's" '[ "$(cat "$HR/.osforge/repo-path")" = "$HR/.osforge/release/v1.10.0" ]'
( cd "$W/work" && GIT checkout -q -b side && printf '9.9.9\n' > VERSION && GIT commit -q -am side && GIT tag v9.9.9 \
  && GIT push -q origin side --tags && GIT checkout -q main ) >/dev/null 2>&1
gdeploy "$HR" --release
check "--release ignores a higher tag cut off main (v9.9.9 on a side branch)" '[ $RC -eq 0 ] && [ ! -e "$HR/.osforge/release/v9.9.9" ] && grep -q "official release v1.10.0" <<<"$OUT"'
git -C "$G" fetch -q origin --tags; git -C "$G" stash -q -u 2>/dev/null; git -C "$G" checkout -q --detach v9.9.9
HG7="$WORK/hg-offmain"; mkdir -p "$HG7"; gdeploy "$HG7"
check "detached at a tag that is not on main → refused" '[ $RC -ne 0 ] && grep -q "tag v9.9.9 is not on main" <<<"$OUT"'
git -C "$G" checkout -q wip; git -C "$G" stash pop -q 2>/dev/null
gdeploy "$HR" --release
check "--release again reuses the worktree" '[ $RC -eq 0 ] && grep -q "reusing worktree" <<<"$OUT"'
HOME="$HR" "$G/deploy.sh" --doctor > "$WORK/rel-doctor.log" 2>&1
check "--doctor shows installed version vs latest local tag" 'grep -q "installed v1.10.0 = latest local tag v1.10.0" "$WORK/rel-doctor.log"'
git -C "$G" remote set-url origin "$W/does-not-exist.git"
HR2="$WORK/hr-offline"; mkdir -p "$HR2"; gdeploy "$HR2" --release
check "--release with an unreachable origin → clear failure, nothing written" '[ $RC -ne 0 ] && grep -q "fetch --tags origin failed" <<<"$OUT" && [ "$(find "$HR2" -type f | wc -l | tr -d " ")" = 0 ]'

echo ""
echo "══ lifecycle: $PASS ok, $FAIL falha(s)"
[ "$FAIL" -eq 0 ]
