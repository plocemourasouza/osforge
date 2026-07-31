#!/usr/bin/env bash
# =============================================================================
# harness-assertions.sh — lógica de veredito do harness de triggering
# =============================================================================
#
# Biblioteca compartilhada por:
#   scripts/test-skill-triggering.sh   (roda de verdade, consome API)
#   tests/test-assertions.sh           (exercita esta lógica offline)
#
# Existe como ARQUIVO, e não como trecho extraído do harness com sed, porque a
# extração por sed + `source <(...)` falhou silenciosamente no bash 3.2 do
# macOS: nenhuma função era definida, e como as chamadas eram feitas dentro de
# um wrapper que redirecionava stderr, o resultado parecia "asserção falhou"
# em vez de "biblioteca não carregou". Um arquivo sourceado normalmente não tem
# esse modo de falha.
#
# Requer definidos pelo chamador:
#   REPO_ROOT     raiz do repo OSForge
#   OUTPUT_BASE   diretório de trabalho (para o mapa de skills)
# =============================================================================

# Extrai skills acionadas do log (nome do campo "skill" nos eventos)
extract_triggered_skills() {
    local log_file="$1"
    grep -o '"skill":"[^"]*"' "$log_file" 2>/dev/null | \
        sed 's/"skill":"//;s/"//' | sort -u || true
}

# ── Invocação nativa ────────────────────────────────────────────────────────
# Evento da ferramenta Skill com o nome esperado (aceita namespace "ns:nome").
check_skill_triggered() {
    local log_file="$1"
    local skill_name="$2"

    local skill_pattern='"skill":"([^"]*:)?'"${skill_name}"'"'

    if grep -q '"name":"Skill"' "$log_file" 2>/dev/null && \
       grep -qE "$skill_pattern" "$log_file" 2>/dev/null; then
        return 0
    fi
    return 1
}

# ── Resolução via manifesto (Model A) ───────────────────────────────────────
# Só as skills de claude-code/skills-core.txt vivem em ~/.claude/skills e podem
# ser invocadas pela ferramenta Skill. As demais são alcançadas lendo o SKILL.md
# apontado pelo MANIFEST — exigir invocação nativa delas reprovaria 100% dos
# casos por construção, e o Model A ficaria sem critério de aceite.

SKILL_MAP_FILE="${OUTPUT_BASE:-/tmp}/skill-map.tsv"

# Mapa nome→path relativo. Indexa tanto o nome do diretório quanto o `name` do
# frontmatter, porque divergem em algumas skills (skills/evolve → osforge-evolve).
build_skill_map() {
    mkdir -p "$(dirname "$SKILL_MAP_FILE")"
    python3 - "$REPO_ROOT" > "$SKILL_MAP_FILE" <<'PY'
import re, sys
from pathlib import Path
root = Path(sys.argv[1]) / "skills"
for sf in sorted(root.rglob("SKILL.md")):
    rel = sf.parent.relative_to(root).as_posix()
    m = re.match(r"^---\s*\n(.*?)\n---", sf.read_text(encoding="utf-8", errors="replace"), re.S)
    fm = m.group(1) if m else ""
    n = re.search(r'^name:\s*["\']?([^"\'#\n]+)["\']?\s*$', fm, re.M)
    keys = {sf.parent.name}
    if n:
        keys.add(n.group(1).strip())
    for k in keys:
        print(f"{k}\t{rel}")
PY
}

skill_rel_path() {
    awk -F'\t' -v n="$1" '$1==n {print $2; exit}' "$SKILL_MAP_FILE" 2>/dev/null || true
}

is_core_skill() {
    local rel="$1"
    [ -z "$rel" ] && return 1
    grep -qxF "$rel" "$REPO_ROOT/claude-code/skills-core.txt" 2>/dev/null
}

# PASS por resolução: o stream mostra uma LEITURA do SKILL.md da skill esperada.
# Nome da ferramenta e caminho têm de estar no MESMO evento — só citar o caminho
# em prosa não conta como ter alcançado a skill.
check_skill_resolved() {
    local log_file="$1"
    local rel="$2"
    [ -z "$rel" ] && return 1

    grep -E '"name":"(Read|Glob|Grep|Bash)"' "$log_file" 2>/dev/null \
        | grep -qF "skills/${rel}/SKILL.md" 2>/dev/null
}

# ── Roteamento do orquestrador ──────────────────────────────────────────────
# O CLAUDE.md/orchestrator promete saídas verificáveis: anúncio de persona
# (`@agent-name`), despacho via Task/Agent (`"subagent_type":"<name>"`), ou
# leitura do AGENT.md. Qualquer uma das três evidências conta.

# Texto do assistant concatenado (para asserções de prosa: @agent, tier).
response_text() {
    local log_file="$1"
    if command -v jq &>/dev/null; then
        grep '"type":"assistant"' "$log_file" 2>/dev/null \
            | jq -r '[.message.content[]? | select(.type=="text") | .text] | join("\n")' 2>/dev/null
    else
        grep -o '"text":"[^"]*"' "$log_file" 2>/dev/null | sed 's/"text":"//;s/"$//'
    fi
}

# Agente esperado alcançado? Aceita lista separada por | (alternativas válidas).
check_agent_routed() {
    local log_file="$1"
    local agents_alt="$2"   # ex.: "debugger|backend-engineer"
    local text; text="$(response_text "$log_file")"
    local IFS='|'
    for a in $agents_alt; do
        # 1. anúncio de persona: @nome no texto
        if printf '%s' "$text" | grep -qF "@${a}"; then return 0; fi
        # 2. despacho real de subagente
        if grep -qE "\"subagent_type\":\"${a}\"" "$log_file" 2>/dev/null; then return 0; fi
        # 3. leitura do AGENT.md correspondente
        if grep -E '"name":"(Read|Bash)"' "$log_file" 2>/dev/null | grep -q "agents/${a}"; then return 0; fi
    done
    return 1
}

# Tier de modelo citado na resposta (Roster do plano / manifesto de tasks).
check_tier_mentioned() {
    local log_file="$1"
    local tier="$2"         # sonnet | opus | haiku (aceita alternativas com |)
    local text; text="$(response_text "$log_file")"
    local IFS='|'
    for t in $tier; do
        if printf '%s' "$text" | grep -qiE "\b${t}\b"; then return 0; fi
    done
    return 1
}
