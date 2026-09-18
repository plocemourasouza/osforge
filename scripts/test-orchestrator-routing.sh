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
#            Com `!` na frente do campo (ex.: `!security-auditor`), SÓ despacho real
#            conta: o contrato daquele caso é delegar, e anunciar `@nome` e responder
#            sozinho não é delegar (B-010).
#   skill  : invocação nativa (ferramenta Skill) OU leitura do SKILL.md
#            (mesmas asserções do harness de skills)
#   tier   : palavra do tier (sonnet/opus/haiku) no texto do plano
#
# Um caso PASSA quando TODAS as dimensões não-"-" passam. Cada dimensão é
# reportada separadamente para o diagnóstico não virar adivinhação.
#
# CONSOME API — --runs chamadas por caso (padrão 3; 16 casos no arquivo padrão).
# Um caso só é PASS quando passa nas N execuções; 0 < k < N é FLAKY (instável).
#
# USO:
#   ./scripts/test-orchestrator-routing.sh --model claude-sonnet-4-6     # todos os casos
#   ./scripts/test-orchestrator-routing.sh --model X --id r01,r03        # subconjunto
#   ./scripts/test-orchestrator-routing.sh --dry                         # lista, custo zero
#   ./scripts/test-orchestrator-routing.sh --model X --runs 5 --home /tmp/limpo \
#       --report docs/evals/2026-09-18-sonnet-routing.md
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
MODEL=""
RUNS="${OSFORGE_TEST_RUNS:-3}"
HOME_OVERRIDE=""
DRY=0
REPORT_FILE=""
ALLOW_FLAKY=0
while [ $# -gt 0 ]; do
    case "$1" in
        --id) FILTER_IDS="$2"; shift 2 ;;
        --cases) CASES_FILE="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        --runs) RUNS="$2"; shift 2 ;;
        --home) HOME_OVERRIDE="$2"; shift 2 ;;
        --dry) DRY=1; shift ;;
        --report) REPORT_FILE="$2"; shift 2 ;;
        --allow-flaky) ALLOW_FLAKY=1; shift ;;
        --help|-h) sed -n '2,40p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "argumento desconhecido: $1 (use --help)"; exit 1 ;;
    esac
done

if command -v timeout &>/dev/null; then TIMEOUT_CMD="timeout $TIMEOUT_SECS"
elif command -v gtimeout &>/dev/null; then TIMEOUT_CMD="gtimeout $TIMEOUT_SECS"
else TIMEOUT_CMD=""; echo "[WARN] sem timeout/gtimeout (macOS: brew install coreutils)" >&2; fi

[ -f "$CASES_FILE" ] || { echo "[ERRO] arquivo de casos não existe: $CASES_FILE"; exit 1; }
if [ "$DRY" = "0" ]; then
    command -v claude &>/dev/null || { echo "[ERRO] claude CLI não encontrado no PATH"; exit 1; }
    [ -n "$MODEL" ] || { echo "[ERRO] --model é obrigatório (ex.: --model claude-sonnet-4-6)."
                         echo "       Sem o id do modelo o resultado não é comparável (E-A45). Para só listar: --dry"; exit 1; }
fi
case "$RUNS" in ''|*[!0-9]*|0) echo "[ERRO] --runs precisa ser um inteiro ≥ 1"; exit 1 ;; esac
[ -z "$HOME_OVERRIDE" ] || [ -d "$HOME_OVERRIDE" ] || { echo "[ERRO] --home não existe: $HOME_OVERRIDE"; exit 1; }

mkdir -p "$OUTPUT_BASE"

# shellcheck source=lib/harness-assertions.sh
source "$SCRIPT_DIR/lib/harness-assertions.sh"
build_skill_map

echo "============================================================"
echo "OSForge Orchestrator Routing Eval"
echo "============================================================"
echo "Casos   : $CASES_FILE"
echo "Filtro  : ${FILTER_IDS:-'(todos)'}"
echo "Modelo  : ${MODEL:-'(dry-run)'}"
echo "Runs    : $RUNS"
echo "HOME    : ${HOME_OVERRIDE:-$HOME (vivo)}"
echo "Output  : $OUTPUT_BASE"
echo "============================================================"

PASSED=0; FAILED=0; TIMED_OUT=0; FLAKY=0
declare -a RESULTS=()
CASE_JSON="$OUTPUT_BASE/cases.json"; : > "$CASE_JSON"
START_EPOCH=$(date +%s)

if [ "$DRY" = "1" ]; then
    echo "MODO SECO — nenhum modelo é chamado, nenhum token é gasto."
    echo ""
    n=0
    while IFS=$'\t' read -r cid exp_agents exp_skill exp_tier prompt; do
        [ -z "$cid" ] && continue
        case "$cid" in \#*) continue ;; esac
        if [ -n "$FILTER_IDS" ]; then
            case ",$FILTER_IDS," in *",$cid,"*) : ;; *) continue ;; esac
        fi
        n=$((n + 1))
        dims=""
        case "$exp_agents" in
            -) : ;;
            \!*) dims="agente(DESPACHO obrigatório): ${exp_agents#!}" ;;
            *)  dims="agente: $exp_agents" ;;
        esac
        [ "$exp_skill" != "-" ] && dims="$dims · skill: $exp_skill"
        [ "$exp_tier" != "-" ] && dims="$dims · tier: $exp_tier"
        printf '%3d. %-6s %s\n' "$n" "$cid" "$dims"
        printf '     %s\n' "$(printf '%s' "$prompt" | head -c 100)"
    done < "$CASES_FILE"
    echo ""
    echo "$n caso(s). Para rodar de verdade: --model <id> [--runs N]"
    exit 0
fi

while IFS=$'\t' read -r cid exp_agents exp_skill exp_tier prompt; do
    [ -z "$cid" ] && continue
    case "$cid" in \#*) continue ;; esac
    if [ -n "$FILTER_IDS" ]; then
        case ",$FILTER_IDS," in *",$cid,"*) : ;; *) continue ;; esac
    fi

    # `!agente` = o contrato do caso é DELEGAR: só despacho real conta (B-010).
    need_dispatch=0
    case "$exp_agents" in \!*) need_dispatch=1; exp_agents="${exp_agents#!}" ;; esac

    out="$OUTPUT_BASE/$cid"; mkdir -p "$out"
    printf '%s\n' "$prompt" > "$out/prompt.txt"

    echo "------------------------------------------------------------"
    printf '[%s] %s\n' "$cid" "$(printf '%s' "$prompt" | head -c 150)"

    hits=0; timeouts=0; last_detail=""
    for (( i=1; i<=RUNS; i++ )); do
        mkdir -p "$out/workdir-$i"
        log="$out/stream-$i.json"
        ( cd "$out/workdir-$i" && ${HOME_OVERRIDE:+env HOME="$HOME_OVERRIDE"} $TIMEOUT_CMD claude \
            -p "$prompt" \
            --model "$MODEL" \
            --dangerously-skip-permissions \
            --max-turns "$MAX_TURNS" \
            --output-format stream-json \
            --verbose < /dev/null ) > "$log" 2>&1
        rc=$?

        run_ok=1; detail=""

        # dimensão AGENTE (roteado, ou despachado quando o caso exige delegação)
        if [ "$exp_agents" != "-" ]; then
            if [ "$need_dispatch" = "1" ]; then
                if check_agent_dispatched "$log" "$exp_agents"; then detail="$detail despacho:OK"
                else run_ok=0; detail="$detail despacho:X(esperado $exp_agents)"; fi
            else
                if check_agent_routed "$log" "$exp_agents"; then detail="$detail agente:OK"
                else run_ok=0; detail="$detail agente:X(esperado $exp_agents)"; fi
            fi
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
            if [ "$sk_ok" = "0" ]; then detail="$detail skill:OK"
            else run_ok=0; detail="$detail skill:X(esperado $exp_skill)"; fi
        fi

        # dimensão TIER
        if [ "$exp_tier" != "-" ]; then
            if check_tier_mentioned "$log" "$exp_tier"; then detail="$detail tier:OK"
            else run_ok=0; detail="$detail tier:X(esperado $exp_tier)"; fi
        fi

        if [ "$run_ok" = "1" ]; then
            hits=$((hits + 1)); echo "  run $i: OK —$detail"
        else
            [ "$rc" = "124" ] && timeouts=$((timeouts + 1))
            echo "  run $i: falhou —$detail"
            last_detail="$detail"
        fi
    done

    if [ "$hits" = "$RUNS" ]; then verdict="PASS"; PASSED=$((PASSED+1))
    elif [ "$hits" -gt 0 ]; then verdict="FLAKY"; FLAKY=$((FLAKY+1))
    elif [ "$timeouts" -gt 0 ]; then verdict="TIMEOUT"; TIMED_OUT=$((TIMED_OUT+1))
    else verdict="FAIL"; FAILED=$((FAILED+1)); fi

    printf '%s/%s\n' "$hits" "$RUNS" > "$out/result.txt"
    echo "  → $verdict ${hits}/${RUNS}"
    RESULTS+=("[$verdict ${hits}/${RUNS}] $cid —${last_detail:-tudo OK}")
    python3 - "$cid" "$hits" "$RUNS" "$verdict" "${last_detail:-}" >> "$CASE_JSON" <<'PY'
import json, sys
cid, k, n, verdict, detail = sys.argv[1:6]
print(json.dumps({"id": cid, "k": int(k), "n": int(n), "verdict": verdict, "detail": detail.strip()}))
PY
done < "$CASES_FILE"

echo ""
echo "============================================================"
echo "RESULTADO FINAL — ROTEAMENTO"
echo "============================================================"
for r in "${RESULTS[@]:-}"; do [ -n "$r" ] && echo "  $r"; done
echo ""
echo "  PASS: $PASSED   FLAKY: $FLAKY   FAIL: $FAILED   TIMEOUT: $TIMED_OUT"
echo "  Logs: $OUTPUT_BASE"
echo "============================================================"

if [ -n "$REPORT_FILE" ]; then
    emit_eval_report "routing" "$REPORT_FILE" "$CASE_JSON" "$START_EPOCH" \
        "$(printf '%s ' "$0" "$@")" "$OUTPUT_BASE"/*/stream-*.json
fi

[ "$FAILED" -eq 0 ] && [ "$TIMED_OUT" -eq 0 ] && { [ "$FLAKY" -eq 0 ] || [ "$ALLOW_FLAKY" = "1" ]; }
