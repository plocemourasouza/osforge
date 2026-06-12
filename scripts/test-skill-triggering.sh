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
#   # Validar sintaxe sem rodar:
#   bash -n scripts/test-skill-triggering.sh
#
# SAÍDA:
#   Arquivos de log em /tmp/osforge-skill-tests/<timestamp>/<skill>/
#   Relatório final no stdout com PASS/FAIL por skill e contagem total.
#
# COMO DECIDE PASS/FAIL:
#   O stream-json do `claude` emite eventos por linha. Um evento de invocação
#   da ferramenta Skill tem `"name":"Skill"` e dentro do input o campo
#   `"skill":"<nome>"` (podendo ter namespace: "ns:nome"). O script:
#     1. Grava o stream completo em LOG_FILE
#     2. Verifica se alguma linha contém '"name":"Skill"'
#     3. Verifica se alguma linha contém '"skill":"<nome>"' ou '"skill":"*:<nome>"'
#     4. Ambas verdadeiras → PASS; qualquer falha → FAIL
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
    timeout "$TIMEOUT_SECS" claude \
        -p "$prompt" \
        --dangerously-skip-permissions \
        --max-turns "$MAX_TURNS" \
        --output-format stream-json \
        > "$log_file" 2>&1
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
    local result
    if check_skill_triggered "$log_file" "$skill_name"; then
        result="PASS"
    else
        result="FAIL"
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
done < <(load_cases "$CASES_FILE" "$FILTER_SKILLS")

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
