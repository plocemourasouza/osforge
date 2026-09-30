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
#
# GUARDA DE COTA (B-026, SPEC-L01 Parte B): mesmo contrato do harness de skills.
# Antes de CADA caso e depois de CADA execução: `rate_limit_info.status ==
# "rejected"` (ou is_error com texto de limite) NO STREAM da própria execução
# PARA o lote ali -- o caso corrente e todos os seguintes saem NOT RUN, fora do
# k de N. `quota.json` acima de OSFORGE_EVAL_QUOTA_STOP (padrão 85) ou com
# rejeição de reset futuro PARA antes de iniciar qualquer caso. Nos dois casos:
# exit 75 (EX_TEMPFAIL). is_error que não é cota conta como ERROR (fora do k de
# N, não para o lote). --ignore-quota desliga as duas checagens.
# =============================================================================

set -uo pipefail

EX_TEMPFAIL=75

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
IGNORE_QUOTA=0               # --ignore-quota: desliga a guarda de cota (B-026)
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
        --ignore-quota) IGNORE_QUOTA=1; shift ;;
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

# ── Validação do arquivo de casos (roda sempre, inclusive em --dry) ─────────
# Um caso com agente/skill/tier que não existe é um caso quebrado: sem isto,
# só a execução paga (--model) descobre, gastando chamadas num FAIL garantido
# (N-01/B-025, EV-O-N03 — o --dry de roteamento não conferia nada).
ACCEPTED_TIERS="haiku sonnet opus fable"

agent_exists() {
    local name="$1"
    [ -f "$REPO_ROOT/agents/${name}.md" ] && return 0
    [ -f "$REPO_ROOT/agents/${name}/AGENT.md" ] && return 0
    return 1
}

validate_routing_cases() {
    local errs=0 checked=0
    while IFS=$'\t' read -r cid exp_agents exp_skill exp_tier critico _prompt; do
        [ -z "$cid" ] && continue
        case "$cid" in \#*) continue ;; esac
        checked=$((checked + 1))

        if [ "$exp_agents" != "-" ]; then
            local agents_field="$exp_agents" a_ifs
            case "$agents_field" in \!*) agents_field="${agents_field#!}" ;; esac
            a_ifs="$IFS"; IFS='|'
            for aname in $agents_field; do
                if ! agent_exists "$aname"; then
                    echo "  ❌ $cid: agente '$aname' não existe em agents/"
                    errs=$((errs + 1))
                fi
            done
            IFS="$a_ifs"
        fi

        if [ "$exp_skill" != "-" ]; then
            local s_ifs srel
            s_ifs="$IFS"; IFS='|'
            for sname in $exp_skill; do
                srel="$(skill_rel_path "${sname##*/}")"
                if [ -z "$srel" ]; then
                    echo "  ❌ $cid: skill '$sname' não existe em skills/"
                    errs=$((errs + 1))
                fi
            done
            IFS="$s_ifs"
        fi

        if [ "$exp_tier" != "-" ]; then
            local t_ifs
            t_ifs="$IFS"; IFS='|'
            for tname in $exp_tier; do
                case " $ACCEPTED_TIERS " in
                    *" $tname "*) : ;;
                    *) echo "  ❌ $cid: tier '$tname' fora do conjunto aceito ($ACCEPTED_TIERS)"; errs=$((errs + 1)) ;;
                esac
            done
            IFS="$t_ifs"
        fi

        case "$critico" in
            ""|"-"|"sim") : ;;
            *) echo "  ❌ $cid: critico '$critico' inválido (use 'sim' ou vazio)"; errs=$((errs + 1)) ;;
        esac
    done < "$CASES_FILE"

    echo "validação de roteamento: $checked caso(s), $errs problema(s)"
    [ "$errs" -eq 0 ]
}

validate_routing_cases || { echo "[ERRO] corrija $CASES_FILE antes de rodar."; exit 1; }

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
ERRORED=0                   # is_error sem ser cota (B2) -- fora do k de N, não reprova o lote
declare -a RESULTS=()
CASE_JSON="$OUTPUT_BASE/cases.json"; : > "$CASE_JSON"
START_EPOCH=$(date +%s)
QUOTA_STOPPED=0
QUOTA_REASON=""
NOT_RUN_FROM=""

if [ "$DRY" = "1" ]; then
    echo "MODO SECO — nenhum modelo é chamado, nenhum token é gasto."
    echo ""
    n=0
    while IFS=$'\t' read -r cid exp_agents exp_skill exp_tier critico prompt; do
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
        [ "$critico" = "sim" ] && dims="$dims · CRÍTICO"
        printf '%3d. %-6s %s\n' "$n" "$cid" "$dims"
        printf '     %s\n' "$(printf '%s' "$prompt" | head -c 100)"
    done < "$CASES_FILE"
    echo ""
    echo "$n caso(s). Para rodar de verdade: --model <id> [--runs N]"
    exit 0
fi

# Guarda de cota (B-026, B3): snapshot ANTES de gastar qualquer chamada de API,
# para o relatório poder mostrar em que estado a janela estava ao começar.
# Calculado só aqui (depois do --dry) -- --dry não gasta chamada nem precisa
# de leitura de quota.json.
QUOTA_AT_START="$(quota_snapshot)"

CASE_IDX=0
while IFS=$'\t' read -r cid exp_agents exp_skill exp_tier critico prompt; do
    [ -z "$cid" ] && continue
    case "$cid" in \#*) continue ;; esac
    if [ -n "$FILTER_IDS" ]; then
        case ",$FILTER_IDS," in *",$cid,"*) : ;; *) continue ;; esac
    fi
    CASE_IDX=$((CASE_IDX + 1))

    # B3: preflight de cota ANTES de gastar a chamada deste caso. Fail-open por
    # design (quota_preflight_reason já cobre isso) -- só para quando há motivo
    # explícito. `|| true` porque `set -e` não está ativo aqui, mas mantém o
    # padrão do harness de skills.
    if [ "$IGNORE_QUOTA" = "0" ]; then
        preflight_reason="$(quota_preflight_reason || true)"
        if [ -n "$preflight_reason" ]; then
            echo "[cota] $preflight_reason -- parando antes de '$cid'"
            QUOTA_STOPPED=1
            QUOTA_REASON="cota: $preflight_reason (antes de '$cid')"
            NOT_RUN_FROM="$CASE_IDX"
            break
        fi
    fi

    # `!agente` = o contrato do caso é DELEGAR: só despacho real conta (B-010).
    need_dispatch=0
    case "$exp_agents" in \!*) need_dispatch=1; exp_agents="${exp_agents#!}" ;; esac

    out="$OUTPUT_BASE/$cid"; mkdir -p "$out"
    printf '%s\n' "$prompt" > "$out/prompt.txt"

    echo "------------------------------------------------------------"
    printf '[%s] %s\n' "$cid" "$(printf '%s' "$prompt" | head -c 150)"

    hits=0; timeouts=0; errors=0; last_detail=""; case_quota_hit=0
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

        # Guarda de cota (B-026, B1/B2): rejeição detectada NESTA execução para o
        # lote inteiro -- não conta como hit nem como miss, e os runs restantes
        # deste caso não rodam. --ignore-quota pula esta checagem por completo.
        run_status="ok"
        if [ "$IGNORE_QUOTA" = "0" ]; then
            run_status="$(run_status_of "$log")"
        fi
        if [ "$run_status" = "quota" ]; then
            echo "  run $i: quota (rate_limit rejected) -- abortando o lote"
            case_quota_hit=1
            break
        elif [ "$run_status" = "error" ]; then
            errors=$((errors + 1))
            echo "  run $i: error (is_error, não é cota) -- fora do k de N"
            continue
        fi

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

    # B2: rejeição detectada NO MEIO deste caso -- ele próprio conta como NOT
    # RUN (não como o hit/miss parcial que já tinha acumulado), e o lote para.
    if [ "$case_quota_hit" = "1" ]; then
        echo "  → NOT RUN (cota: rejeição mid-run)"
        QUOTA_STOPPED=1
        QUOTA_REASON="cota: rejeição mid-run em '$cid'"
        emit_not_run_case "$CASE_JSON" "$cid" "$RUNS" "$([ "$critico" = "sim" ] && echo 1 || echo 0)" "quota: rejeição mid-run"
        NOT_RUN_FROM=$((CASE_IDX + 1))
        RESULTS+=("[NOT RUN 0/${RUNS}] $cid — cota: rejeição mid-run")
        break
    fi

    verdict="$(case_verdict "$hits" "$RUNS" "$timeouts" "$errors")"
    case "$verdict" in
        PASS)    PASSED=$((PASSED+1)) ;;
        FLAKY)   FLAKY=$((FLAKY+1)) ;;
        TIMEOUT) TIMED_OUT=$((TIMED_OUT+1)) ;;
        ERROR)   ERRORED=$((ERRORED+1)) ;;
        *)       FAILED=$((FAILED+1)) ;;
    esac

    printf '%s/%s\n' "$hits" "$RUNS" > "$out/result.txt"
    echo "  → $verdict ${hits}/${RUNS}"
    RESULTS+=("[$verdict ${hits}/${RUNS}] $cid —${last_detail:-tudo OK}")
    python3 - "$cid" "$hits" "$RUNS" "$verdict" "${last_detail:-}" "$errors" "$critico" >> "$CASE_JSON" <<'PY'
import json, sys
cid, k, n, verdict, detail, errors, critico = sys.argv[1:8]
detail = detail.strip()
if int(errors):
    extra = f"{errors} error(s) (fora do k de N)"
    detail = f"{detail}, {extra}" if detail else extra
print(json.dumps({
    "id": cid, "k": int(k), "n": int(n), "verdict": verdict, "detail": detail,
    "critical": critico.strip().lower() == "sim",
}))
PY
done < "$CASES_FILE"

# B2/B3: lote parado por cota -- tudo do ponto de parada em diante (inclusive o
# caso corrente, se a parada foi no preflight) sai como NOT RUN no relatório.
if [ "$QUOTA_STOPPED" = "1" ] && [ -n "$NOT_RUN_FROM" ]; then
    tail -n +"$NOT_RUN_FROM" "$CASES_FILE" | while IFS=$'\t' read -r rcid _rest; do
        [ -z "$rcid" ] && continue
        case "$rcid" in \#*) continue ;; esac
        emit_not_run_case "$CASE_JSON" "$rcid" "$RUNS" "0" "quota: lote interrompido antes de iniciar"
    done
fi
QUOTA_AT_END="$(quota_snapshot)"
export QUOTA_AT_START QUOTA_AT_END

echo ""
echo "============================================================"
echo "RESULTADO FINAL — ROTEAMENTO"
echo "============================================================"
for r in "${RESULTS[@]:-}"; do [ -n "$r" ] && echo "  $r"; done
echo ""
echo "  PASS: $PASSED   FLAKY: $FLAKY   FAIL: $FAILED   TIMEOUT: $TIMED_OUT   ERROR: $ERRORED"
if [ "$QUOTA_STOPPED" = "1" ]; then
    echo "  NOT RUN: $(tail -n +"${NOT_RUN_FROM:-1}" "$CASES_FILE" | grep -vc '^\(#\|$\)' || true)  ($QUOTA_REASON)"
fi
echo "  Logs: $OUTPUT_BASE"
echo "============================================================"

if [ -n "$REPORT_FILE" ]; then
    emit_eval_report "routing" "$REPORT_FILE" "$CASE_JSON" "$START_EPOCH" \
        "$(printf '%s ' "$0" "$@")" "$OUTPUT_BASE"/*/stream-*.json
fi

# B2/B3: lote interrompido por cota -- exit 75 (EX_TEMPFAIL), distinto de
# FAIL(1)/INCOMPLETE(2) do suite_verdict. Não é veredito da suíte, é "não terminou".
if [ "$QUOTA_STOPPED" = "1" ]; then
    echo "[QUOTA] $QUOTA_REASON"
    exit "$EX_TEMPFAIL"
fi

# Veredito da suíte (N-01/B-025): um caso crítico (r12, despacho obrigatório)
# que não seja PASS reprova mesmo com --allow-flaky; NOT RUN nele deixa a
# suíte "incompleta" em vez de aprovada (harness-assertions.sh: suite_verdict).
suite_result="$(suite_verdict "$CASE_JSON" "$ALLOW_FLAKY")"
suite_exit=$?
echo "  Veredito da suíte: $suite_result"
exit "$suite_exit"
