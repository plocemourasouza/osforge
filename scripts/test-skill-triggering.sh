#!/usr/bin/env bash
# =============================================================================
# test-skill-triggering.sh — Harness de eval de triggering de skills OSForge
# =============================================================================
#
# Verifica se uma skill dispara quando deveria, sem mencionar o nome dela no
# prompt. Usa `claude -p ... --output-format stream-json` e faz PASS quando
# o stream contém invocação da Skill com o nome esperado.
#
# IMPORTANTE: Este script consome chamadas de API. Cada caso pode demorar
# até TIMEOUT_SECS segundos. Comece com poucos casos ao explorar.
#
# ESCOPO: amostra das skills críticas (~18 seed). As 140+ skills completas
# não estão aqui — expanda skills-triggering-cases.tsv conforme necessário.
#
# DEPENDÊNCIAS:
#   - claude CLI (no PATH, com ANTHROPIC_API_KEY configurada)
#   - bash 4+, grep, sed
#   - jq (opcional — degrada para grep puro se ausente)
#
# USO:
#   # Rodar todas as skills do arquivo de casos (seed)
#   ./scripts/test-skill-triggering.sh
#
#   # Rodar apenas uma skill pelo nome
#   ./scripts/test-skill-triggering.sh --skill tdd-workflow
#
#   # Rodar uma lista de skills
#   ./scripts/test-skill-triggering.sh --skill "tdd-workflow,osforge-canvas"
#
#   # Usar arquivo de casos diferente
#   ./scripts/test-skill-triggering.sh --cases /caminho/para/outros-casos.tsv
#
#   # Suíte ampla colhida do frontmatter (240 casos — custa API)
#   ./scripts/test-skill-triggering.sh --generated --sample 20
#
#   # Validar sintaxe sem rodar:
#   bash -n scripts/test-skill-triggering.sh
#
# SAÍDA:
#   Arquivos de log em /tmp/osforge-skill-tests/<timestamp>/<skill>/
#   Relatório final no stdout com PASS/FAIL por skill e contagem total.
#
# COMO DECIDE PASS/FAIL (dois modos, por causa do Model A):
#   Só as skills de claude-code/skills-core.txt vivem em ~/.claude/skills e podem
#   ser invocadas pela ferramenta Skill. As demais são alcançadas lendo o SKILL.md
#   apontado pelo MANIFEST em SKILLS.md. Exigir invocação nativa de todas
#   reprovaria as não-core por construção — e sem a segunda asserção o Model A
#   não teria como ser validado.
#
#   skill CORE      → PASS exige invocação nativa:
#                     linha com '"name":"Skill"' E '"skill":"<nome>"' (ou "ns:nome")
#   skill NÃO-CORE  → PASS com invocação nativa OU resolução via manifesto:
#                     evento Read/Glob/Grep/Bash citando skills/<rel>/SKILL.md.
#                     O OU existe porque install-skill.sh pode tê-la tornado
#                     nativa naquele projeto.
#                     Só MENCIONAR o caminho em texto não conta — nome da
#                     ferramenta e caminho têm de estar no mesmo evento.
#
#   A lógica de veredito é testada offline, sem gastar API: ./tests/test-assertions.sh
#
# SUÍTES DE CASOS:
#   scripts/skill-triggering-cases.tsv            escrita à mão, ~25 casos, difícil
#                                                 (fraseado do usuário, sem vocabulário da description)
#   scripts/skill-triggering-cases.generated.tsv  colhida do frontmatter (--generated),
#                                                 240 casos: o gatilho que o próprio autor escreveu.
#                                                 FAIL aqui = description quebrada.
#                                                 Regenerar: python3 scripts/_generate_triggering_cases.py
#
# VARIÁVEIS DE AMBIENTE (override):
#   OSFORGE_TEST_MAX_TURNS   número de turnos max por caso (padrão: 3)
#   OSFORGE_TEST_TIMEOUT     timeout por caso em segundos (padrão: 120)
#   OSFORGE_TEST_VERBOSE     se "1", imprime o stream completo no stdout
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Constantes e paths
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_CASES_FILE="$SCRIPT_DIR/skill-triggering-cases.tsv"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_BASE="/tmp/osforge-skill-tests/${TIMESTAMP}"

MAX_TURNS="${OSFORGE_TEST_MAX_TURNS:-3}"
TIMEOUT_SECS="${OSFORGE_TEST_TIMEOUT:-120}"
VERBOSE="${OSFORGE_TEST_VERBOSE:-0}"

# Detect a timeout binary (macOS lacks `timeout`; coreutils provides `gtimeout`)
if command -v timeout &>/dev/null; then
    TIMEOUT_CMD="timeout $TIMEOUT_SECS"
elif command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD="gtimeout $TIMEOUT_SECS"
else
    TIMEOUT_CMD=""
    echo "[WARN] no timeout/gtimeout found — running without per-case timeout" >&2
fi

# ---------------------------------------------------------------------------
# Detectar jq (degradar para grep se ausente)
# ---------------------------------------------------------------------------
HAS_JQ=0
if command -v jq &>/dev/null; then
    HAS_JQ=1
fi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log_info()  { echo "[INFO]  $*"; }
log_pass()  { echo "[PASS]  $*"; }
log_fail()  { echo "[FAIL]  $*"; }
log_skip()  { echo "[SKIP]  $*"; }
log_warn()  { echo "[WARN]  $*"; }

# Extrai skills acionadas do log (nome do campo "skill" nos eventos)
extract_triggered_skills() {
    local log_file="$1"
    grep -o '"skill":"[^"]*"' "$log_file" 2>/dev/null | \
        sed 's/"skill":"//;s/"//' | sort -u || true
}

# Verifica se a skill esperada aparece no stream
check_skill_triggered() {
    local log_file="$1"
    local skill_name="$2"

    # Padrão: "skill":"nome" ou "skill":"namespace:nome"
    local skill_pattern='"skill":"([^"]*:)?'"${skill_name}"'"'

    if grep -q '"name":"Skill"' "$log_file" 2>/dev/null && \
       grep -qE "$skill_pattern" "$log_file" 2>/dev/null; then
        return 0
    fi
    return 1
}

# ---------------------------------------------------------------------------
# Resolução via manifesto (Model A)
# ---------------------------------------------------------------------------
# Só as skills de claude-code/skills-core.txt vivem em ~/.claude/skills e podem
# ser invocadas pela ferramenta Skill. As demais são alcançadas lendo o
# SKILL.md apontado pelo MANIFEST em SKILLS.md — e para essas, exigir invocação
# nativa reprovaria 100% dos casos por construção. Sem esta asserção o Model A
# não tem critério de aceite.

# Mapa nome→path relativo, construído uma vez (nome do frontmatter E nome do
# diretório apontam para o mesmo path, porque divergem em algumas skills:
# skills/evolve tem `name: osforge-evolve`).
SKILL_MAP_FILE="${OUTPUT_BASE}/skill-map.tsv"

build_skill_map() {
    mkdir -p "$OUTPUT_BASE"
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

# PASS por resolução: o stream mostra uma leitura do SKILL.md da skill esperada.
# Exige name+path no MESMO evento — o modelo apenas CITAR o caminho em texto não
# conta como ter alcançado a skill.
check_skill_resolved() {
    local log_file="$1"
    local rel="$2"
    [ -z "$rel" ] && return 1

    grep -E '"name":"(Read|Glob|Grep|Bash)"' "$log_file" 2>/dev/null \
        | grep -qF "skills/${rel}/SKILL.md" 2>/dev/null
}

# Mostra primeira resposta do assistant (truncada)
show_first_response() {
    local log_file="$1"
    if [ "$HAS_JQ" = "1" ]; then
        grep '"type":"assistant"' "$log_file" 2>/dev/null | \
            head -1 | \
            jq -r '.message.content[0].text // .message.content // "n/a"' 2>/dev/null | \
            head -c 300 || echo "(não foi possível extrair)"
    else
        grep '"type":"assistant"' "$log_file" 2>/dev/null | \
            head -1 | \
            grep -o '"text":"[^"]*"' | \
            head -1 | \
            sed 's/"text":"//;s/"//' | \
            head -c 300 || echo "(não foi possível extrair — instale jq para melhor output)"
    fi
}

# ---------------------------------------------------------------------------
# Rodar um único caso de teste
# ---------------------------------------------------------------------------
run_case() {
    local skill_name="$1"
    local prompt="$2"

    local out_dir="${OUTPUT_BASE}/${skill_name}"
    mkdir -p "$out_dir"

    local log_file="${out_dir}/stream.json"
    local prompt_file="${out_dir}/prompt.txt"

    echo "$prompt" > "$prompt_file"

    log_info "Testando skill: $skill_name"
    log_info "Prompt: $(echo "$prompt" | head -c 120)..."
    log_info "Log: $log_file"

    # Rodar claude headless com output stream-json
    # --dangerously-skip-permissions: necessário em modo headless/não-interativo
    set +e
    $TIMEOUT_CMD claude \
        -p "$prompt" \
        --dangerously-skip-permissions \
        --max-turns "$MAX_TURNS" \
        --output-format stream-json \
        --verbose \
        < /dev/null > "$log_file" 2>&1
    local exit_code=$?
    set -e

    if [ "$exit_code" = "124" ]; then
        log_warn "Timeout (${TIMEOUT_SECS}s) para skill: $skill_name"
        echo "TIMEOUT" > "${out_dir}/result.txt"
        return 2
    fi

    if [ "$VERBOSE" = "1" ]; then
        echo "--- stream ---"
        cat "$log_file"
        echo "--- fim stream ---"
    fi

    # Verificar PASS/FAIL
    #   core     → tem de ser invocada nativamente (ferramenta Skill)
    #   não-core → vale invocação nativa OU resolução via manifesto (Read do SKILL.md);
    #              já pode estar instalada no projeto por install-skill.sh, daí o OU
    local rel result
    rel="$(skill_rel_path "$skill_name")"

    if check_skill_triggered "$log_file" "$skill_name"; then
        result="PASS"
        log_info "Modo: invocação nativa"
    elif ! is_core_skill "$rel" && check_skill_resolved "$log_file" "$rel"; then
        result="PASS"
        log_info "Modo: resolvida via manifesto (skills/${rel}/SKILL.md)"
    else
        result="FAIL"
        if [ -z "$rel" ]; then
            log_warn "skill '$skill_name' não existe em skills/ — caso órfão no TSV"
        elif is_core_skill "$rel"; then
            log_info "Esperado: invocação nativa (skill está no core allowlist)"
        else
            log_info "Esperado: invocação nativa OU leitura de skills/${rel}/SKILL.md"
        fi
    fi

    echo "$result" > "${out_dir}/result.txt"

    # Reportar skills que foram acionadas (para diagnóstico)
    local triggered
    triggered=$(extract_triggered_skills "$log_file")
    if [ -n "$triggered" ]; then
        log_info "Skills acionadas: $triggered"
    else
        log_info "Skills acionadas: (nenhuma)"
    fi

    # Mostrar início da resposta
    echo "Resposta (truncada):"
    show_first_response "$log_file"
    echo ""

    if [ "$result" = "PASS" ]; then
        log_pass "PASS: $skill_name"
        return 0
    else
        log_fail "FAIL: $skill_name"
        return 1
    fi
}

# ---------------------------------------------------------------------------
# Carregar e filtrar casos do TSV
# ---------------------------------------------------------------------------
load_cases() {
    local cases_file="$1"
    local filter_skills="$2"  # CSV ou vazio para todos

    # Lê o TSV, ignora linhas de comentário (# ...) e linhas em branco
    while IFS=$'\t' read -r skill_name prompt; do
        # Pular comentários e linhas vazias
        [[ "$skill_name" =~ ^#.*$ || -z "$skill_name" ]] && continue

        # Filtrar por skill se especificado
        if [ -n "$filter_skills" ]; then
            local found=0
            IFS=',' read -ra wanted <<< "$filter_skills"
            for w in "${wanted[@]}"; do
                if [ "$w" = "$skill_name" ]; then
                    found=1
                    break
                fi
            done
            [ "$found" = "0" ] && continue
        fi

        echo "${skill_name}	${prompt}"
    done < "$cases_file"
}

# ---------------------------------------------------------------------------
# Parse de argumentos
# ---------------------------------------------------------------------------
CASES_FILE="$DEFAULT_CASES_FILE"
FILTER_SKILLS=""
SAMPLE_N=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skill)
            FILTER_SKILLS="$2"
            shift 2
            ;;
        --cases)
            CASES_FILE="$2"
            shift 2
            ;;
        --generated)
            # Suíte ampla colhida do frontmatter (_generate_triggering_cases.py)
            CASES_FILE="$SCRIPT_DIR/skill-triggering-cases.generated.tsv"
            shift
            ;;
        --sample)
            # Amostra aleatória de N casos: a suíte completa custa API demais
            # para rodar inteira a cada commit.
            SAMPLE_N="$2"
            shift 2
            ;;
        --help|-h)
            sed -n '/^# =/,/^# ======/p' "$0" | grep '^#' | sed 's/^# \?//'
            exit 0
            ;;
        *)
            echo "Argumento desconhecido: $1. Use --help."
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Verificações de pré-requisitos
# ---------------------------------------------------------------------------
if ! command -v claude &>/dev/null; then
    echo "[ERRO] 'claude' não encontrado no PATH. Configure o Claude CLI antes de rodar."
    exit 1
fi

if [ ! -f "$CASES_FILE" ]; then
    echo "[ERRO] Arquivo de casos não encontrado: $CASES_FILE"
    exit 1
fi

if [ "$HAS_JQ" = "0" ]; then
    log_warn "jq não encontrado — extração de resposta usará fallback grep (menos precisa)"
fi

# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------
mkdir -p "$OUTPUT_BASE"

echo "============================================================"
echo "OSForge Skill Triggering Eval"
echo "============================================================"
echo "Arquivo de casos : $CASES_FILE"
echo "Filtro de skills : ${FILTER_SKILLS:-'(todas)'}"
echo "Max turns        : $MAX_TURNS"
echo "Timeout/caso     : ${TIMEOUT_SECS}s"
echo "Output dir       : $OUTPUT_BASE"
echo "jq disponível    : $( [ "$HAS_JQ" = "1" ] && echo 'sim' || echo 'não (degradado)')"
echo "============================================================"
echo ""

PASSED=0
FAILED=0
SKIPPED=0
TIMED_OUT=0
declare -a RESULTS=()

build_skill_map
log_info "Mapa de skills: $(wc -l < "$SKILL_MAP_FILE" | tr -d ' ') entradas"
log_info "Core allowlist: $(grep -vc '^\s*#\|^\s*$' "$REPO_ROOT/claude-code/skills-core.txt" 2>/dev/null || echo '?') skills (invocação nativa exigida)"

# Amostragem: a suíte gerada tem centenas de casos e cada um custa API.
CASES_STREAM="${OUTPUT_BASE}/cases.tsv"
mkdir -p "$OUTPUT_BASE"
load_cases "$CASES_FILE" "$FILTER_SKILLS" > "$CASES_STREAM"
if [ -n "$SAMPLE_N" ]; then
    TOTAL_AVAIL=$(wc -l < "$CASES_STREAM" | tr -d ' ')
    if command -v shuf &>/dev/null; then
        shuf -n "$SAMPLE_N" "$CASES_STREAM" > "${CASES_STREAM}.sample"
    else
        # macOS sem coreutils: sort -R é o fallback disponível
        sort -R "$CASES_STREAM" | head -n "$SAMPLE_N" > "${CASES_STREAM}.sample"
    fi
    mv "${CASES_STREAM}.sample" "$CASES_STREAM"
    log_info "Amostra: $SAMPLE_N de $TOTAL_AVAIL casos"
fi

# Carregar casos e iterar
while IFS=$'\t' read -r skill_name prompt; do
    echo "------------------------------------------------------------"
    set +e
    run_case "$skill_name" "$prompt"
    case_exit=$?
    set -e

    case "$case_exit" in
        0)
            PASSED=$((PASSED + 1))
            RESULTS+=("[PASS] $skill_name")
            ;;
        2)
            TIMED_OUT=$((TIMED_OUT + 1))
            RESULTS+=("[TIMEOUT] $skill_name")
            ;;
        *)
            FAILED=$((FAILED + 1))
            RESULTS+=("[FAIL] $skill_name")
            ;;
    esac

    echo ""
done < "$CASES_STREAM"

# ---------------------------------------------------------------------------
# Relatório final
# ---------------------------------------------------------------------------
echo "============================================================"
echo "RESULTADO FINAL"
echo "============================================================"
for r in "${RESULTS[@]}"; do
    echo "  $r"
done
echo ""
echo "  PASS   : $PASSED"
echo "  FAIL   : $FAILED"
echo "  TIMEOUT: $TIMED_OUT"
echo "  SKIP   : $SKIPPED"
echo ""
echo "Logs completos em: $OUTPUT_BASE"
echo "============================================================"

# Exit code: 0 se todos PASS, 1 se algum falhou
if [ "$FAILED" -gt 0 ] || [ "$TIMED_OUT" -gt 0 ]; then
    exit 1
fi
exit 0
