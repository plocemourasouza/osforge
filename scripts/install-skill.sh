#!/usr/bin/env bash
# install-skill.sh — Puxa uma skill de DOMÍNIO do repo OSForge para o projeto atual.
#
# Model A: só as skills do core (claude-code/skills-core.txt) ficam globais em
# ~/.claude/skills. As demais permanecem no repo e são instaladas por projeto,
# sob demanda, com este helper — em <projeto>/.claude/skills/, onde a descoberta
# nativa do Claude Code as encontra e passa a dispará-las por trigger.
#
# Uso:
#   install-skill.sh <nome|termo> [nome2 ...]   # instala no cwd (.claude/skills)
#   install-skill.sh --list <termo>             # só lista candidatos, não copia
#   install-skill.sh --target <dir> <nome>      # destino explícito
#   install-skill.sh --global <nome>            # instala em ~/.claude/skills
#
# Resolve o path via INDICE-SKILLS.json (match exato de name → depois substring).
set -euo pipefail

# Resolução do repo, em ordem: override explícito → posição do script (uso a
# partir do próprio repo) → âncora escrita pelo deploy (uso a partir de
# ~/.local/bin, onde "../" seria ~/.local e não acharia skills/).
REPO="${OSFORGE_REPO:-$(cd "$(dirname "$0")/.." && pwd)}"
if [ ! -f "$REPO/INDICE-SKILLS.json" ] && [ -f "$HOME/.osforge/repo-path" ]; then
  REPO="$(cat "$HOME/.osforge/repo-path")"
fi
if [ ! -f "$REPO/INDICE-SKILLS.json" ]; then
  echo "erro: repo OSForge não encontrado (tentei '$REPO')." >&2
  echo "      rode ./deploy.sh no repo, ou exporte OSFORGE_REPO=/caminho/do/osforge" >&2
  exit 1
fi
INDEX="$REPO/INDICE-SKILLS.json"
SKILLS_DIR="$REPO/skills"

TARGET="$PWD/.claude/skills"
LIST_ONLY=false
declare -a TERMS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --list)   LIST_ONLY=true; shift ;;
    --global) TARGET="$HOME/.claude/skills"; shift ;;
    --target) TARGET="$2"; shift 2 ;;
    --help|-h)
      sed -n '2,18p' "$0"; exit 0 ;;
    *) TERMS+=("$1"); shift ;;
  esac
done

[ -f "$INDEX" ] || { echo "❌ INDICE-SKILLS.json não encontrado. Rode: python3 scripts/_extract_index.py" >&2; exit 1; }
[ ${#TERMS[@]} -gt 0 ] || { echo "Uso: install-skill.sh <nome|termo> [...]  (--list para só buscar)"; exit 1; }

# resolve_paths <termo> → imprime local_path(s) relativos a skills/, um por linha
resolve_paths() {
  python3 - "$INDEX" "$1" <<'PY'
import json, sys
idx = json.load(open(sys.argv[1]))
term = sys.argv[2].lower()
exact = [x for x in idx if x.get('name','').lower() == term]
subs  = [x for x in idx if term in x.get('name','').lower()
         or term in x.get('description','').lower()]
chosen = exact if exact else subs
seen=set(); out=[]
for x in chosen:
    lp = x.get('local_path','')
    if lp.startswith('skills/'): lp = lp.split('skills/',1)[1]
    if lp and lp not in seen:
        seen.add(lp); out.append(f"{x.get('name','?')}\t{lp}")
print("\n".join(out))
PY
}

# Só cria o destino quando vai mesmo instalar: `--list` é uma consulta e não deve
# deixar um .claude/skills vazio em qualquer diretório de onde foi chamado.
$LIST_ONLY || mkdir -p "$TARGET"
installed=0
for term in "${TERMS[@]}"; do
  # `mapfile` é bash 4+; o /bin/bash do macOS é 3.2 e este script é deployado em
  # ~/.local/bin, ou seja, roda na máquina do usuário. Laço de leitura equivalente.
  # (scripts/check-portability.py impede que isso volte.)
  hits=()
  while IFS= read -r _line; do
    [ -n "$_line" ] && hits+=("$_line")
  done < <(resolve_paths "$term")
  if [ ${#hits[@]} -eq 0 ]; then
    echo "⚠️  nenhuma skill casa com: $term" >&2; continue
  fi
  if [ ${#hits[@]} -gt 1 ] && ! $LIST_ONLY; then
    echo "🔎 '$term' casou com ${#hits[@]} skills — refine ou use --list:" >&2
    printf '   %s\n' "${hits[@]}" >&2
    continue
  fi
  for h in "${hits[@]}"; do
    name="${h%%$'\t'*}"; rel="${h##*$'\t'}"
    if $LIST_ONLY; then echo "   $name  →  skills/$rel"; continue; fi
    src="$SKILLS_DIR/$rel"
    [ -d "$src" ] || { echo "⚠️  path ausente no repo: $rel" >&2; continue; }
    cp -a "$src" "$TARGET/$(basename "$rel")"
    echo "✅ $name → $TARGET/$(basename "$rel")"
    installed=$((installed+1))
  done
done

$LIST_ONLY && exit 0
[ "$installed" -gt 0 ] && echo "" && echo "$installed skill(s) instalada(s). Reinicie a sessão do Claude Code para a descoberta nativa indexá-las."
exit 0
