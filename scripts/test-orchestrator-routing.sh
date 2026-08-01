#!/usr/bin/env bash
# =============================================================================
# test-orchestrator-routing.sh — eval de ROTEAMENTO do orquestrador OSForge
# =============================================================================
#
# O harness de skills prova que a skill certa dispara. Este prova a camada
# acima: dado uma demanda ingênua, o DETECT do orquestrador identifica o
# AGENTE certo, alcança a SKILL certa e (em demanda de plano) declara o TIER
# de modelo no Roster — os três contratos verificáveis do CLAUDE.md.
#
# EVIDÊNCIAS aceitas por dimensão (qualquer uma):
#   agente : anúncio `@nome` no texto · despacho `"subagent_type":"nome"` ·
#            leitura de agents/<nome>*.md
#   skill  : invocação nativa (ferramenta Skill) OU leitura do SKILL.md
#            (mesmas asserções do harness de skills)
#   tier   : palavra do tier (sonnet/opus/haiku) no texto do plano
#
# Um caso PASSA quando TODAS as dimensões não-"-" passam. Cada dimensão é
# reportada separadamente para o diagnóstico não virar adivinhação.
#
# CONSOME API — ~1 chamada por caso (16 casos no arquivo padrão).
#
# USO:
#   ./scripts/test-orchestrator-routing.sh                # todos os casos
#   ./scripts/test-orchestrator-routing.sh --id r01,r03   # subconjunto
#   ./scripts/test-orchestrator-routing.sh --cases outro.tsv
#
# A lógica de veredito é a mesma biblioteca do harness de skills
# (scripts/lib/harness-assertions.sh), testada offline por tests/test-assertions.sh.
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CASES_FILE="$SCRIPT_DIR/routing-cases.tsv"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_BASE="/tmp/osforge-routing-tests/${TIMESTAMP}"
# Turnos e timeout maiores que o harness de skills DE PROPÓSITO: o route-guard
# (Stop hook) pode bloquear a resposta e exigir um ciclo extra de correção
# (carregar a skill declarada). Medido com max-turns=4: o guard disparou certo
# no r10 e o modelo ficou sem turnos para obedecer (error_max_turns); em r03 e
# r12 a sessão morreu por turnos ANTES do Stop — que só roda em conclusão
# normal — e o guard nunca chegou a existir. Sessões reais não têm max-turns.
MAX_TURNS="${OSFORGE_TEST_MAX_TURNS:-8}"
TIMEOUT_SECS="${OSFORGE_TEST_TIMEOUT:-300}"

FILTER_IDS=""
while [ $# -gt 0 ]; do
    case "$1" in
        --id) FILTER_IDS="$2"; shift 2 ;;
        --cases) CASES_FILE="$2"; shift 2 ;;
        --help|-h) sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "argumento desconhecido: $1 (use --help)"; exit 1 ;;
    esac
done

if command -v timeout &>/dev/null; then TIMEOUT_CMD="timeout $TIMEOUT_SECS"
elif command -v gtimeout &>/dev/null; then TIMEOUT_CMD="gtimeout $TIMEOUT_SECS"
else TIMEOUT_CMD=""; echo "[WARN] sem timeout/gtimeout (macOS: brew install coreutils)" >&2; fi

command -v claude &>/dev/null || { echo "[ERRO] claude CLI não encontrado no PATH"; exit 1; }
[ -f "$CASES_FILE" ] || { echo "[ERRO] arquivo de casos não existe: $CASES_FILE"; exit 1; }

mkdir -p "$OUTPUT_BASE"

# shellcheck source=lib/harness-assertions.sh
source "$SCRIPT_DIR/lib/harness-assertions.sh"
build_skill_map

echo "============================================================"
echo "OSForge Orchestrator Routing Eval"
echo "============================================================"
echo "Casos   : $CASES_FILE"
echo "Filtro  : ${FILTER_IDS:-'(todos)'}"
echo "Output  : $OUTPUT_BASE"
echo "============================================================"

PASSED=0; FAILED=0; TIMED_OUT=0
declare -a RESULTS=()

while IFS=$'\t' read -r cid exp_agents exp_skill exp_tier prompt; do
    [ -z "$cid" ] && continue
    case "$cid" in \#*) continue ;; esac
    if [ -n "$FILTER_IDS" ]; then
        case ",$FILTER_IDS," in *",$cid,"*) : ;; *) continue ;; esac
    fi

    out="$OUTPUT_BASE/$cid"; mkdir -p "$out/workdir"
    log="$out/stream.json"
    printf '%s\n' "$prompt" > "$out/prompt.txt"

    echo "------------------------------------------------------------"
    echo "[$cid] $prompt" | head -c 160; echo ""

    ( cd "$out/workdir" && $TIMEOUT_CMD claude \
        -p "$prompt" \
        --dangerously-skip-permissions \
        --max-turns "$MAX_TURNS" \
        --output-format stream-json \
        --verbose < /dev/null ) > "$log" 2>&1
    rc=$?

    verdict="PASS"; detail=""

    # dimensão AGENTE
    if [ "$exp_agents" != "-" ]; then
        if check_agent_routed "$log" "$exp_agents"; then detail+=" agente:OK"
        else verdict="FAIL"; detail+=" agente:X(esperado $exp_agents)"; fi
    fi

    # dimensão SKILL — nativa OU resolvida, qualquer alternativa
    if [ "$exp_skill" != "-" ]; then
        sk_ok=1
        OLD_IFS="$IFS"; IFS='|'
        for sname in $exp_skill; do
            srel="$(skill_rel_path "${sname##*/}")"
            [ -z "$srel" ] && srel="$sname"
            if check_skill_triggered "$log" "${sname##*/}" || check_skill_resolved "$log" "$srel"; then
                sk_ok=0; break
            fi
        done
        IFS="$OLD_IFS"
        if [ "$sk_ok" = "0" ]; then detail+=" skill:OK"
        else verdict="FAIL"; detail+=" skill:X(esperado $exp_skill)"; fi
    fi

    # dimensão TIER
    if [ "$exp_tier" != "-" ]; then
        if check_tier_mentioned "$log" "$exp_tier"; then detail+=" tier:OK"
        else verdict="FAIL"; detail+=" tier:X(esperado $exp_tier)"; fi
    fi

    # timeout só reprova se nenhuma dimensão exigida foi evidenciada antes do corte
    if [ "$rc" = "124" ] && [ "$verdict" = "FAIL" ]; then
        verdict="TIMEOUT"
    fi

    echo "$verdict" > "$out/result.txt"
    echo "  →$detail"
    case "$verdict" in
        PASS)    PASSED=$((PASSED+1)) ;;
        TIMEOUT) TIMED_OUT=$((TIMED_OUT+1)) ;;
        *)       FAILED=$((FAILED+1)) ;;
    esac
    RESULTS+=("[$verdict] $cid —$detail")
done < "$CASES_FILE"

echo ""
echo "============================================================"
echo "RESULTADO FINAL — ROTEAMENTO"
echo "============================================================"
for r in "${RESULTS[@]:-}"; do [ -n "$r" ] && echo "  $r"; done
echo ""
echo "  PASS: $PASSED   FAIL: $FAILED   TIMEOUT: $TIMED_OUT"
echo "  Logs: $OUTPUT_BASE"
echo "============================================================"
[ "$FAILED" -eq 0 ] && [ "$TIMED_OUT" -eq 0 ]
