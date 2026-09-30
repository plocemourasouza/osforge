#!/usr/bin/env bash
# tests/test-installers.sh — os dois helpers que rodam na MÁQUINA do usuário.
#
# `install-skill` e `install-mcp` são deployados em ~/.local/bin e são a metade
# sob demanda do Model A: só 47 skills ficam globais, o resto é puxado por projeto
# com `install-skill`. Mesmo assim os dois não tinham UM teste — e um `mapfile`
# (bash 4+) deixou o `install-skill` quebrado no /bin/bash 3.2 do macOS sem que
# `bash -n`, o CI ou o preflight percebessem: `bash -n` só faz o parse.
#
# Verifica por execução, em diretórios temporários:
#   1. --list acha por nome exato e por substring, e não copia nada
#   2. instalação no cwd (.claude/skills), com --target e com --global
#   3. termo ambíguo não instala nada e explica
#   4. termo inexistente avisa e sai sem quebrar o laço (outros termos continuam)
#   5. roda a partir de ~/.local/bin, achando o repo pela âncora ~/.osforge/repo-path
#   6. install-mcp: --list, merge em .mcp.json novo, merge preservando o que já existe,
#      stack desconhecido avisa, .mcp.json inválido não vira lixo silencioso
#   7. os dois sobrevivem a um shell sem os builtins do bash 4 (simulado com um
#      wrapper que remove `mapfile`/`readarray` do ambiente)
#
# Offline, sem API. Uso: tests/test-installers.sh
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }

SKILL="$REPO/scripts/install-skill.sh"
MCP="$REPO/scripts/install-mcp.sh"
export HOME="$WORK/home"; mkdir -p "$HOME"

# Uma skill que existe e NÃO é core (o caso de uso real do helper).
PICK="$(python3 - "$REPO" <<'PY'
import json, os, sys
repo = sys.argv[1]
core = {l.strip() for l in open(os.path.join(repo, "claude-code", "skills-core.txt"), encoding="utf-8")
        if l.strip() and not l.startswith("#")}
idx = json.load(open(os.path.join(repo, "INDICE-SKILLS.json"), encoding="utf-8"))
for x in idx:
    lp = x.get("local_path", "").replace("skills/", "", 1)
    if lp and lp not in core and "/" not in lp and os.path.isfile(os.path.join(repo, "skills", lp, "SKILL.md")):
        print(x["name"]); break
PY
)"
[ -n "$PICK" ] || { echo "não achei uma skill não-core para testar"; exit 1; }
echo "skill de teste: $PICK"

section "install-skill: busca e instalação"
OUT="$(cd "$WORK" && "$SKILL" --list "$PICK" 2>&1)"; RC=$?
check "--list acha a skill por nome exato" '[ $RC -eq 0 ] && grep -q "$PICK" <<<"$OUT"'
check "--list não copia nada" '[ ! -d "$WORK/.claude/skills" ]'

P1="$WORK/proj1"; mkdir -p "$P1"
OUT="$(cd "$P1" && "$SKILL" "$PICK" 2>&1)"; RC=$?
check "instala no cwd, em .claude/skills" '[ $RC -eq 0 ] && [ -f "$P1/.claude/skills/$PICK/SKILL.md" ]'
check "o SKILL.md instalado é o do repo" 'cmp -s "$P1/.claude/skills/$PICK/SKILL.md" "$REPO/skills/$PICK/SKILL.md"'

P2="$WORK/proj2"; mkdir -p "$P2"
OUT="$(cd "$WORK" && "$SKILL" --target "$P2/skills" "$PICK" 2>&1)"; RC=$?
check "--target respeita o destino explícito" '[ $RC -eq 0 ] && [ -f "$P2/skills/$PICK/SKILL.md" ]'

OUT="$(cd "$WORK" && "$SKILL" --global "$PICK" 2>&1)"; RC=$?
check "--global instala em ~/.claude/skills" '[ $RC -eq 0 ] && [ -f "$HOME/.claude/skills/$PICK/SKILL.md" ]'

section "install-skill: casos que não deveriam instalar"
P3="$WORK/proj3"; mkdir -p "$P3"
OUT="$(cd "$P3" && "$SKILL" "e" 2>&1)"; RC=$?
# O destino pode existir (é modo de instalação), mas vazio: nenhuma skill entrou.
check "termo ambíguo não instala e explica" '[ -z "$(ls -A "$P3/.claude/skills" 2>/dev/null)" ] && grep -qE "casou com [0-9]+ skills" <<<"$OUT"'
OUT="$(cd "$P3" && "$SKILL" "zzz-nao-existe-zzz" 2>&1)"; RC=$?
check "termo inexistente avisa, exit 0" '[ $RC -eq 0 ] && grep -q "nenhuma skill casa" <<<"$OUT"'
OUT="$(cd "$P3" && "$SKILL" "zzz-nao-existe-zzz" "$PICK" 2>&1)"; RC=$?
check "termo ruim não impede o bom (o laço sobrevive)" '[ -f "$P3/.claude/skills/$PICK/SKILL.md" ]'
OUT="$(cd "$P3" && "$SKILL" 2>&1)"; RC=$?
check "sem argumento nenhum, mostra o uso e sai 1" '[ $RC -eq 1 ] && grep -q "Uso:" <<<"$OUT"'

section "install-skill: rodando de ~/.local/bin (âncora do deploy)"
BIN="$HOME/.local/bin"; mkdir -p "$BIN" "$HOME/.osforge"
cp "$SKILL" "$BIN/install-skill"; chmod +x "$BIN/install-skill"
printf '%s\n' "$REPO" > "$HOME/.osforge/repo-path"
P4="$WORK/proj4"; mkdir -p "$P4"
OUT="$(cd "$P4" && "$BIN/install-skill" "$PICK" 2>&1)"; RC=$?
check "acha o repo pela âncora ~/.osforge/repo-path" '[ $RC -eq 0 ] && [ -f "$P4/.claude/skills/$PICK/SKILL.md" ]'
mv "$HOME/.osforge/repo-path" "$HOME/.osforge/repo-path.bak"
OUT="$(cd "$P4" && "$BIN/install-skill" "$PICK" 2>&1)"; RC=$?
check "sem âncora e sem repo, erro explicativo (exit 1)" '[ $RC -eq 1 ] && grep -q "repo OSForge não encontrado" <<<"$OUT"'
mv "$HOME/.osforge/repo-path.bak" "$HOME/.osforge/repo-path"
OUT="$(cd "$P4" && OSFORGE_REPO="$REPO" "$BIN/install-skill" --list "$PICK" 2>&1)"
check "OSFORGE_REPO tem precedência" 'grep -q "$PICK" <<<"$OUT"'

section "install-skill roda em bash sem os builtins do bash 4"
# O /bin/bash do macOS é 3.2: sem mapfile, sem readarray. `enable -n` desliga o
# builtin dentro do próprio bash 5, o que reproduz o sintoma sem precisar de um Mac.
cat > "$WORK/bash32-ish" <<'SH'
#!/usr/bin/env bash
enable -n mapfile 2>/dev/null || true
enable -n readarray 2>/dev/null || true
source "$1"
SH
chmod +x "$WORK/bash32-ish"
P5="$WORK/proj5"; mkdir -p "$P5"
OUT="$(cd "$P5" && bash "$WORK/bash32-ish" "$SKILL" "$PICK" 2>&1)"; RC=$?
check "instala mesmo sem os builtins do bash 4 disponíveis" '[ $RC -eq 0 ] && [ -f "$P5/.claude/skills/$PICK/SKILL.md" ]'   # portable-ok: é o nome do caso, não uma chamada
check "e não reclama de comando não encontrado" '! grep -qiE "mapfile|readarray" <<<"$OUT"'   # portable-ok: procura o sintoma na saída

section "install-mcp"
STACK="$(ls -1 "$REPO/mcp/stacks" | head -1 | sed 's/\.mcp\.json$//')"
OUT="$("$MCP" --list 2>&1)"; RC=$?
check "--list mostra os stacks" '[ $RC -eq 0 ] && grep -q "$STACK" <<<"$OUT"'
M1="$WORK/mcp1"; mkdir -p "$M1"
OUT="$(cd "$M1" && "$MCP" "$STACK" 2>&1)"; RC=$?
check "cria .mcp.json com o server do stack" '[ $RC -eq 0 ] && python3 -c "
import json,sys; d=json.load(open(sys.argv[1])); assert d[\"mcpServers\"], d" "$M1/.mcp.json"'
python3 - "$M1/.mcp.json" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
d["mcpServers"]["meu-server-proprio"] = {"command": "echo"}
json.dump(d, open(p, "w"), indent=2)
PY
OUT="$(cd "$M1" && "$MCP" "$STACK" 2>&1)"
check "merge não apaga server que era seu" 'python3 -c "
import json,sys; d=json.load(open(sys.argv[1])); assert \"meu-server-proprio\" in d[\"mcpServers\"], d" "$M1/.mcp.json"'
check "merge idempotente avisa que já estava lá" 'grep -q "já presente" <<<"$OUT"'
OUT="$(cd "$M1" && "$MCP" stack-que-nao-existe 2>&1)"
check "stack desconhecido avisa e não quebra" 'grep -q "stack desconhecido" <<<"$OUT"'
M2="$WORK/mcp2"; mkdir -p "$M2"; printf 'isto não é json\n' > "$M2/.mcp.json"
OUT="$(cd "$M2" && "$MCP" "$STACK" 2>&1)"; RC=$?
check ".mcp.json inválido é substituído por um válido, com aviso no stdout" '[ $RC -eq 0 ] && python3 -c "
import json,sys; json.load(open(sys.argv[1]))" "$M2/.mcp.json"'
OUT="$(cd "$M2" && bash "$WORK/bash32-ish" "$MCP" "$STACK" 2>&1)"; RC=$?
check "install-mcp também roda sem builtins do bash 4" '[ $RC -eq 0 ]'

echo ""; echo "══ installers: $PASS ok, $FAIL falha(s)"
[ "$FAIL" -eq 0 ]
