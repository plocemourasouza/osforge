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
#   # Rodar o claude em um diretório específico (padrão: temporário neutro)
#   ./scripts/test-skill-triggering.sh --workdir ~/Projects/algum-projeto
#
#   # OBRIGATÓRIO fora de --dry: qual modelo está sendo medido (B-010, E-A45)
#   ./scripts/test-skill-triggering.sh --model claude-sonnet-4-6 --runs 3
#
#   # Listar os casos sem chamar modelo nenhum (custo zero, serve ao CI)
#   ./scripts/test-skill-triggering.sh --dry
#
#   # Contra um deploy limpo, sem o ~/.claude vivo da máquina
#   ./scripts/test-skill-triggering.sh --model X --home /tmp/home-limpo
#
#   # Gravar o relatório versionável (docs/evals/, B-012)
#   ./scripts/test-skill-triggering.sh --model X --report docs/evals/2026-09-18-sonnet-trigger.md
#
# ONDE O CLAUDE RODA IMPORTA:
#   Por padrão cada caso roda em um diretório temporário vazio. Rodando de
#   dentro do repo OSForge, `skills/<x>/SKILL.md` está a um Glob de distância e
#   o modelo acha a skill explorando o diretório — o teste passaria a medir
#   "sabe achar arquivo no cwd" em vez de "o manifesto funciona". O script avisa
#   se o WORKDIR estiver dentro do repo.
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
#
# REPETIÇÕES E ESTABILIDADE (B-010):
#   Cada caso roda --runs vezes (padrão 3) e o relatório traz k de N.
#     k = N          PASS
#     0 < k < N      FLAKY — o caso é instável, não "passou"; é a saída que o
#                    experimento E1 consome para decidir o que medir
#     k = 0          FAIL
#   Um resultado de 1 execução não distingue "a skill dispara" de "disparou uma vez".
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

# B-010: modelo explícito, repetições, HOME isolado, modo seco e relatório versionável.
MODEL=""                    # --model (obrigatório fora de --dry): o que está sendo medido
RUNS="${OSFORGE_TEST_RUNS:-3}"   # --runs N: k de N por caso
HOME_OVERRIDE=""            # --home DIR: roda contra um deploy limpo, não o ~/.claude vivo
DRY=0                       # --dry: lista os casos e sai, sem chamar modelo
REPORT_FILE=""              # --report FILE: markdown versionável (docs/evals/)
ALLOW_FLAKY=0               # --allow-flaky: FLAKY não reprova a suíte

# Detect a timeout binary (macOS lacks `timeout`; coreutils provides `gtimeout`)
if command -v timeout &>/dev/null; then
    TIMEOUT_CMD="timeout $TIMEOUT_SECS"
elif command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD="gtimeout $TIMEOUT_SECS"
else
    TIMEOUT_CMD=""
    echo "[WARN] sem timeout/gtimeout — rodando sem limite por caso" >&2
    echo "[WARN] no macOS: brew install coreutils (fornece gtimeout)" >&2
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

# Lógica de veredito: arquivo compartilhado com tests/test-assertions.sh
# shellcheck source=lib/harness-assertions.sh
source "$SCRIPT_DIR/lib/harness-assertions.sh"

# Mostra primeira resposta do assistant (truncada)
show_first_response() {
    local log_file="$1"
    if [ "$HAS_JQ" = "1" ]; then
        # Pega o primeiro bloco de TEXTO. `content[0]` pegava o bloco de
        # thinking, cujo texto é vazio e vinha acompanhado de uma signature
        # gigante — o relatório ficava ilegível.
        grep '"type":"assistant"' "$log_file" 2>/dev/null | \
            jq -r '[.message.content[]? | select(.type=="text") | .text] | first // empty' 2>/dev/null | \
            grep -v '^$' | head -1 | \
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

    # Workdir POR CASO. O workdir único contaminava casos entre si: o
    # agency-support escreveu customer-service-flow.md e o agency-marketing,
    # dois casos depois, LEU esse arquivo procurando "the site" — gastando os
    # turnos em contexto alheio. Um --workdir explícito (projeto real do
    # usuário) continua compartilhado de propósito.
    local case_workdir_base="$WORKDIR"
    if [ "$WORKDIR_IS_DEFAULT" = "1" ]; then
        case_workdir_base="${out_dir}/workdir"
    fi

    echo "$prompt" > "${out_dir}/prompt.txt"
    local rel; rel="$(skill_rel_path "$skill_name")"

    log_info "Testando skill: $skill_name  (${RUNS} execução(ões))"
    log_info "Prompt: $(echo "$prompt" | head -c 120)..."

    local hits=0 timeouts=0 run i log_file case_workdir exit_code
    for (( i=1; i<=RUNS; i++ )); do
        # Cada execução tem o SEU workdir e o SEU log: a 2ª execução herdando os
        # arquivos que a 1ª escreveu mediria memória de disco, não triggering.
        case_workdir="$case_workdir_base"
        if [ "$WORKDIR_IS_DEFAULT" = "1" ]; then
            case_workdir="${out_dir}/workdir-${i}"
        fi
        mkdir -p "$case_workdir"
        log_file="${out_dir}/stream-${i}.json"

        set +e
        ( cd "$case_workdir" && ${HOME_OVERRIDE:+env HOME="$HOME_OVERRIDE"} $TIMEOUT_CMD claude \
            -p "$prompt" \
            --model "$MODEL" \
            --dangerously-skip-permissions \
            --max-turns "$MAX_TURNS" \
            --output-format stream-json \
            --verbose \
            < /dev/null ) > "$log_file" 2>&1
        exit_code=$?
        set -e

        [ "$VERBOSE" = "1" ] && { echo "--- stream (run $i) ---"; cat "$log_file"; echo "--- fim ---"; }

        # Veredito desta execução:
        #   core     → invocação nativa (ferramenta Skill)
        #   não-core → nativa OU resolução via manifesto (leitura do SKILL.md)
        # Timeout não invalida evidência já presente no stream parcial: o
        # offensive-fuzzing leu o SKILL.md certo e despachou o subagente, e era
        # marcado TIMEOUT porque o SUBAGENTE estourou os 120s depois disso.
        if check_skill_triggered "$log_file" "$skill_name" \
           || { [ -n "$rel" ] && ! is_core_skill "$rel" && check_skill_resolved "$log_file" "$rel"; }; then
            hits=$((hits + 1))
            log_info "  run $i: HIT"
        else
            [ "$exit_code" = "124" ] && { timeouts=$((timeouts + 1)); log_info "  run $i: timeout (${TIMEOUT_SECS}s), sem evidência"; } \
                                    || log_info "  run $i: miss"
        fi
    done

    RUN_HITS=$hits                      # lidos pelo chamador (k de N)
    RUN_TIMEOUTS=$timeouts
    printf '%s/%s\n' "$hits" "$RUNS" > "${out_dir}/result.txt"

    if [ -z "$rel" ]; then
        log_warn "skill '$skill_name' não existe em skills/ — caso órfão no TSV"
    elif is_core_skill "$rel"; then
        log_info "Esperado: invocação nativa (skill está no core allowlist)"
    else
        log_info "Esperado: invocação nativa OU leitura de skills/${rel}/SKILL.md"
    fi

    local triggered; triggered=$(extract_triggered_skills "${out_dir}/stream-1.json")
    log_info "Skills acionadas (run 1): ${triggered:-(nenhuma)}"
    echo "Resposta (run 1, truncada):"
    show_first_response "${out_dir}/stream-1.json"
    echo ""

    if [ "$hits" = "$RUNS" ]; then
        log_pass "PASS ${hits}/${RUNS}: $skill_name"; return 0
    elif [ "$hits" -gt 0 ]; then
        log_warn "FLAKY ${hits}/${RUNS}: $skill_name"; return 3
    elif [ "$timeouts" -gt 0 ]; then
        log_warn "TIMEOUT 0/${RUNS}: $skill_name"; return 2
    else
        log_fail "FAIL 0/${RUNS}: $skill_name"; return 1
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
WORKDIR=""

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
        --workdir)
            # Diretório onde o `claude` roda. Padrão: temporário vazio.
            WORKDIR="$2"
            shift 2
            ;;
        --model)
            # O que está sendo medido. Sem isto o resultado não é comparável
            # com o de ontem nem com o da outra máquina (E-A45).
            MODEL="$2"
            shift 2
            ;;
        --runs)
            RUNS="$2"
            shift 2
            ;;
        --home)
            # Deploy limpo em vez do ~/.claude vivo da máquina.
            HOME_OVERRIDE="$2"
            shift 2
            ;;
        --dry)
            DRY=1
            shift
            ;;
        --report)
            REPORT_FILE="$2"
            shift 2
            ;;
        --allow-flaky)
            ALLOW_FLAKY=1
            shift
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
if [ "$DRY" = "0" ]; then
    if ! command -v claude &>/dev/null; then
        echo "[ERRO] 'claude' não encontrado no PATH. Configure o Claude CLI antes de rodar."
        exit 1
    fi
    if [ -z "$MODEL" ]; then
        echo "[ERRO] --model é obrigatório (ex.: --model claude-sonnet-4-6)."
        echo "       Um resultado sem o id do modelo não é comparável com nenhum outro (E-A45)."
        echo "       Para só listar os casos, sem custo: --dry"
        exit 1
    fi
fi
case "$RUNS" in ''|*[!0-9]*|0) echo "[ERRO] --runs precisa ser um inteiro ≥ 1 (recebido: '$RUNS')"; exit 1 ;; esac
if [ -n "$HOME_OVERRIDE" ] && [ ! -d "$HOME_OVERRIDE" ]; then
    echo "[ERRO] --home aponta para um diretório que não existe: $HOME_OVERRIDE"; exit 1
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
echo "Modelo           : ${MODEL:-'(dry-run)'}"
echo "Execuções/caso   : $RUNS"
echo "HOME             : ${HOME_OVERRIDE:-$HOME (vivo)}"
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
FLAKY=0
declare -a RESULTS=()

# Diretório neutro: o teste tem de medir alcance pelo manifesto, não a
# capacidade do modelo de achar arquivo no diretório corrente.
WORKDIR_IS_DEFAULT=0
if [ -z "$WORKDIR" ]; then
    WORKDIR="${OUTPUT_BASE}/workdir"
    WORKDIR_IS_DEFAULT=1        # dispara workdir POR CASO em run_case
    mkdir -p "$WORKDIR"
fi
case "$(cd "$WORKDIR" && pwd)/" in
    "$REPO_ROOT"/*)
        log_warn "WORKDIR está dentro do repo OSForge ($WORKDIR)."
        log_warn "As skills não-core ficam alcançáveis por exploração do diretório,"
        log_warn "e um PASS por resolução deixa de provar que o manifesto funcionou."
        ;;
esac
log_info "Workdir do claude: $WORKDIR"

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
CASE_JSON="${OUTPUT_BASE}/cases.json"
: > "$CASE_JSON"
START_EPOCH=$(date +%s)

if [ "$DRY" = "1" ]; then
    echo "MODO SECO — nenhum modelo é chamado, nenhum token é gasto."
    echo ""
    n=0
    while IFS=$'\t' read -r skill_name prompt; do
        n=$((n + 1))
        rel="$(skill_rel_path "$skill_name")"
        if [ -z "$rel" ]; then
            kind="ÓRFÃO (não existe em skills/)"
        elif is_core_skill "$rel"; then
            kind="core → exige invocação nativa"
        else
            kind="manifesto → nativa OU leitura de skills/${rel}/SKILL.md"
        fi
        printf '%3d. %-34s %s\n' "$n" "$skill_name" "$kind"
        printf '     %s\n' "$(echo "$prompt" | head -c 100)"
    done < "$CASES_STREAM"
    echo ""
    echo "$n caso(s). Para rodar de verdade: --model <id> [--runs N]"
    exit 0
fi

while IFS=$'\t' read -r skill_name prompt; do
    echo "------------------------------------------------------------"
    # NÃO usar o par `set +e` / `set -e` aqui: run_case contém o seu próprio
    # `set -e` interno (após capturar o exit do claude), que reativava o errexit
    # GLOBALMENTE e anulava a proteção do call site — o script morria no
    # primeiro return 1, ou seja, no primeiro FAIL, sem placar e sem erro.
    # Duas rodadas reais morreram assim. A forma `|| case_exit=$?` põe a chamada
    # em contexto de condição, onde o bash ignora errexit inclusive DENTRO da
    # função. Regressão coberta por tests/test-assertions.sh (loop survival).
    case_exit=0
    RUN_HITS=0; RUN_TIMEOUTS=0
    run_case "$skill_name" "$prompt" || case_exit=$?

    case "$case_exit" in
        0) verdict="PASS";    PASSED=$((PASSED + 1)) ;;
        3) verdict="FLAKY";   FLAKY=$((FLAKY + 1)) ;;
        2) verdict="TIMEOUT"; TIMED_OUT=$((TIMED_OUT + 1)) ;;
        *) verdict="FAIL";    FAILED=$((FAILED + 1)) ;;
    esac
    RESULTS+=("[$verdict ${RUN_HITS}/${RUNS}] $skill_name")
    python3 - "$skill_name" "$RUN_HITS" "$RUNS" "$verdict" "$RUN_TIMEOUTS" >> "$CASE_JSON" <<'PY'
import json, sys
cid, k, n, verdict, tmo = sys.argv[1:6]
detail = f"{tmo} timeout(s)" if int(tmo) else ""
print(json.dumps({"id": cid, "k": int(k), "n": int(n), "verdict": verdict, "detail": detail}))
PY
    echo ""
done < "$CASES_STREAM"

# ---------------------------------------------------------------------------
# Relatório final
# ---------------------------------------------------------------------------
echo "============================================================"
echo "RESULTADO FINAL"
echo "============================================================"
for r in "${RESULTS[@]:-}"; do [ -n "$r" ] && echo "  $r"; done
echo ""
echo "  PASS   : $PASSED   (k = $RUNS de $RUNS)"
echo "  FLAKY  : $FLAKY    (0 < k < $RUNS — instável, não aprovado)"
echo "  FAIL   : $FAILED"
echo "  TIMEOUT: $TIMED_OUT"
echo ""
echo "Logs completos em: $OUTPUT_BASE"
echo "============================================================"

if [ -n "$REPORT_FILE" ]; then
    emit_eval_report "trigger" "$REPORT_FILE" "$CASE_JSON" "$START_EPOCH" \
        "$(printf '%s ' "$0" "$@")" "${OUTPUT_BASE}"/*/stream-*.json
fi

# Exit: FLAKY reprova junto com FAIL — um caso que acerta 2 de 3 não está verde.
if [ "$FAILED" -gt 0 ] || [ "$TIMED_OUT" -gt 0 ] || { [ "$FLAKY" -gt 0 ] && [ "$ALLOW_FLAKY" = "0" ]; }; then
    exit 1
fi
exit 0
