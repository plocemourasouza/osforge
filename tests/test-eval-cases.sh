#!/usr/bin/env bash
# =============================================================================
# test-eval-cases.sh — N-01/B-025: categoria, casos críticos e validação
#                       sem modelo nos harnesses de eval
# =============================================================================
#
# Os nove casos do spec (docs/intake/needle/SPEC-N01-casos-de-eval.md §Testes),
# todos offline e contra CÓPIAS TEMPORÁRIAS dos arquivos de caso — nunca invoca
# o `claude` de verdade, nunca gasta API:
#
#   1. caso sem 'category' reprova; 'category: negacao' com should_trigger:true reprova
#   2. 'negacao' sem critical:true reprova
#   3. skill com 1 vizinho, ou sem negação, ou sem irrelevante reprova (dizendo o quê falta)
#   4. expect_route para skill inexistente reprova
#   5. os casos do repositório, depois da migração, aprovam
#   6. TSV de trigger com skill inexistente: --dry sai 1
#   7. roteamento com agente/despacho/alternativa inexistente: --dry sai 1; caso válido sai 0
#   8. veredito da suíte com resultados sintéticos (crítico × --allow-flaky × NOT RUN)
#   9. eval_report.py: linha por categoria + críticos reprovados no topo
#
# USO:  ./tests/test-eval-cases.sh
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TRIGGER="$REPO_ROOT/scripts/run-trigger-eval.sh"
SKILLTRIG="$REPO_ROOT/scripts/test-skill-triggering.sh"
ROUTING="$REPO_ROOT/scripts/test-orchestrator-routing.sh"
EVAL_REPORT="$REPO_ROOT/scripts/lib/eval_report.py"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# harness-assertions.sh precisa de REPO_ROOT/OUTPUT_BASE definidos pelo chamador.
OUTPUT_BASE="$WORK"
# shellcheck source=../scripts/lib/harness-assertions.sh
source "$REPO_ROOT/scripts/lib/harness-assertions.sh"

PASS=0
FAIL=0

check() {
    local desc="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "  ✅ $desc"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $desc  (esperado: $expected · obtido: $actual)"
        FAIL=$((FAIL + 1))
    fi
}

# ── Helpers ──────────────────────────────────────────────────────────────────

# run-trigger-eval.sh resolve SCRIPT_DIR a partir do próprio caminho: a cópia
# sed-editada precisa viver DENTRO de scripts/ para achar lib/harness-assertions.sh
# e o skills/ do repo pelo caminho relativo certo.
run_trigger_dry() {
    local cases_dir="$1" log="$2"
    local tmp_script="$REPO_ROOT/scripts/_test_eval_cases_tmp.sh"
    sed "s#CASES_DIR=\"\$SCRIPT_DIR/evals/trigger\"#CASES_DIR=\"$cases_dir\"#" "$TRIGGER" > "$tmp_script"
    ( bash "$tmp_script" --dry ) > "$log" 2>&1
    local rc=$?
    rm -f "$tmp_script"
    return $rc
}

# Escreve uma fixture v2 válida e autocontida: 5 positivo, 2 vizinho,
# 2 irrelevante, 1 negacao(crítico) — mínimos batidos, split cobrindo tudo.
# rel="tdd-workflow" existe de verdade (skills/tdd-workflow/SKILL.md), então a
# checagem de "rel existe" passa sem precisar duplicar as 15 skills reais.
write_base_fixture() {
    cat > "$1" <<'JSON'
{
  "$schema": "osforge/trigger-eval/v2",
  "skill": "eval-fixture",
  "rel": "tdd-workflow",
  "core": false,
  "note": "fixture sintética de tests/test-eval-cases.sh — não é uma skill real.",
  "split": {
    "tune": ["p1", "p2", "p3", "v1", "i1"],
    "eval": ["p4", "p5", "v2", "i2", "n1"],
    "policy": "fixture"
  },
  "cases": [
    {"id": "p1", "should_trigger": true, "category": "positivo", "query": "fixture positivo um"},
    {"id": "p2", "should_trigger": true, "category": "positivo", "query": "fixture positivo dois"},
    {"id": "p3", "should_trigger": true, "category": "positivo", "query": "fixture positivo tres"},
    {"id": "p4", "should_trigger": true, "category": "positivo", "query": "fixture positivo quatro"},
    {"id": "p5", "should_trigger": true, "category": "positivo", "query": "fixture positivo cinco"},
    {"id": "v1", "should_trigger": false, "category": "vizinho", "expect_route": "clean-code", "query": "fixture vizinho um"},
    {"id": "v2", "should_trigger": false, "category": "vizinho", "expect_route": "code-review", "query": "fixture vizinho dois"},
    {"id": "i1", "should_trigger": false, "category": "irrelevante", "query": "fixture irrelevante um"},
    {"id": "i2", "should_trigger": false, "category": "irrelevante", "query": "fixture irrelevante dois"},
    {"id": "n1", "should_trigger": false, "category": "negacao", "critical": true, "query": "fixture negacao um"}
  ]
}
JSON
}

# mutate_fixture <arquivo> <script-python-que-recebe 'd' já carregado>
mutate_fixture() {
    local path="$1" pyexpr="$2"
    python3 - "$path" <<PY
import json
p = "$path"
d = json.load(open(p, encoding="utf-8"))
$pyexpr
json.dump(d, open(p, "w", encoding="utf-8"))
PY
}

# ── 1. category ausente / incoerente com should_trigger ─────────────────────
echo "1. category obrigatória e coerente com should_trigger:"

DIR1A="$WORK/case1a"; mkdir -p "$DIR1A"
write_base_fixture "$DIR1A/eval-fixture.json"
mutate_fixture "$DIR1A/eval-fixture.json" "
for c in d['cases']:
    if c['id'] == 'p1':
        del c['category']
"
run_trigger_dry "$DIR1A" "$WORK/case1a.log"
check "sem 'category' reprova"        "1"   "$?"
check "e diz qual caso"               "PASS" "$(grep -q "caso p1 sem 'category'" "$WORK/case1a.log" && echo PASS || echo FAIL)"

DIR1B="$WORK/case1b"; mkdir -p "$DIR1B"
write_base_fixture "$DIR1B/eval-fixture.json"
mutate_fixture "$DIR1B/eval-fixture.json" "
for c in d['cases']:
    if c['id'] == 'p1':
        c['category'] = 'negacao'
"
run_trigger_dry "$DIR1B" "$WORK/case1b.log"
check "'negacao' com should_trigger:true reprova" "1" "$?"
check "e diz que é incoerente"        "PASS" "$(grep -q "incoerente com should_trigger" "$WORK/case1b.log" && echo PASS || echo FAIL)"

# ── 2. negacao sem critical:true ─────────────────────────────────────────────
echo ""
echo "2. negacao exige critical:true:"

DIR2="$WORK/case2"; mkdir -p "$DIR2"
write_base_fixture "$DIR2/eval-fixture.json"
mutate_fixture "$DIR2/eval-fixture.json" "
for c in d['cases']:
    if c['id'] == 'n1':
        c.pop('critical', None)
"
run_trigger_dry "$DIR2" "$WORK/case2.log"
check "negacao sem critical:true reprova" "1" "$?"
check "e diz que falta critical"      "PASS" "$(grep -q "negacao mas não tem critical:true" "$WORK/case2.log" && echo PASS || echo FAIL)"

# ── 3. mínimos por categoria (dizendo qual falta) ────────────────────────────
echo ""
echo "3. mínimos por categoria (≥5 positivo, ≥2 vizinho, ≥1 negacao, ≥1 irrelevante):"

DIR3A="$WORK/case3a"; mkdir -p "$DIR3A"
write_base_fixture "$DIR3A/eval-fixture.json"
mutate_fixture "$DIR3A/eval-fixture.json" "
for c in d['cases']:
    if c['id'] == 'v2':
        c['category'] = 'irrelevante'
        c.pop('expect_route', None)
"
run_trigger_dry "$DIR3A" "$WORK/case3a.log"
check "1 vizinho (mínimo 2) reprova"   "1"    "$?"
check "e diz que é vizinho que falta" "PASS" "$(grep -q "'vizinho' (mínimo 2)" "$WORK/case3a.log" && echo PASS || echo FAIL)"

DIR3B="$WORK/case3b"; mkdir -p "$DIR3B"
write_base_fixture "$DIR3B/eval-fixture.json"
mutate_fixture "$DIR3B/eval-fixture.json" "
for c in d['cases']:
    if c['id'] == 'n1':
        c['category'] = 'irrelevante'
        c.pop('critical', None)
"
run_trigger_dry "$DIR3B" "$WORK/case3b.log"
check "sem negacao reprova"           "1"    "$?"
check "e diz que é negacao que falta" "PASS" "$(grep -q "'negacao' (mínimo 1)" "$WORK/case3b.log" && echo PASS || echo FAIL)"

DIR3C="$WORK/case3c"; mkdir -p "$DIR3C"
write_base_fixture "$DIR3C/eval-fixture.json"
mutate_fixture "$DIR3C/eval-fixture.json" "
for c in d['cases']:
    if c['id'] in ('i1', 'i2'):
        c['category'] = 'vizinho'
        c['expect_route'] = 'clean-code'
"
run_trigger_dry "$DIR3C" "$WORK/case3c.log"
check "sem irrelevante reprova"           "1"    "$?"
check "e diz que é irrelevante que falta" "PASS" "$(grep -q "'irrelevante' (mínimo 1)" "$WORK/case3c.log" && echo PASS || echo FAIL)"

# ── 4. expect_route para skill inexistente ───────────────────────────────────
echo ""
echo "4. expect_route aponta para skill existente:"

DIR4="$WORK/case4"; mkdir -p "$DIR4"
write_base_fixture "$DIR4/eval-fixture.json"
mutate_fixture "$DIR4/eval-fixture.json" "
for c in d['cases']:
    if c['id'] == 'v1':
        c['expect_route'] = 'no-such-skill-xyz-really-not-real'
"
run_trigger_dry "$DIR4" "$WORK/case4.log"
check "expect_route inexistente reprova"  "1"    "$?"
check "e nomeia a rota ruim"               "PASS" "$(grep -q "expect_route 'no-such-skill-xyz-really-not-real' não aponta" "$WORK/case4.log" && echo PASS || echo FAIL)"

# Controle: a fixture BASE (sem mutação) tem de aprovar — prova que os testes
# acima falham pela mutação, não por algum outro detalhe da fixture.
DIRBASE="$WORK/casebase"; mkdir -p "$DIRBASE"
write_base_fixture "$DIRBASE/eval-fixture.json"
run_trigger_dry "$DIRBASE" "$WORK/casebase.log"
check "fixture base (sem mutação) aprova" "0" "$?"

# ── 5. os casos do repositório, depois da migração, aprovam ─────────────────
echo ""
echo "5. casos reais do repo (pós-migração v2):"

run_trigger_dry "$REPO_ROOT/scripts/evals/trigger" "$WORK/repo.log"
check "170 casos, 20 críticos, 0 problemas" "PASS" \
    "$(grep -q '170 casos, 20 críticos, 0 problema(s)' "$WORK/repo.log" && echo PASS || echo FAIL)"
check "--dry do repo aprova"                "0"    "$?"

# ── 6. test-skill-triggering.sh: caso órfão no TSV ──────────────────────────
echo ""
echo "6. test-skill-triggering.sh recusa caso órfão:"

printf 'tdd-workflow\tcaso ok\nno-such-skill-xyz\tcaso orfao\n' > "$WORK/orphan-cases.tsv"
printf 'tdd-workflow\tcaso ok\n' > "$WORK/valid-cases.tsv"

"$SKILLTRIG" --cases "$WORK/orphan-cases.tsv" --dry > "$WORK/orphan-dry.log" 2>&1
check "--dry com órfão sai 1"          "1" "$?"
check "e avisa ÓRFÃO"                  "PASS" "$(grep -q 'ÓRFÃO' "$WORK/orphan-dry.log" && echo PASS || echo FAIL)"

"$SKILLTRIG" --cases "$WORK/valid-cases.tsv" --dry > "$WORK/valid-dry.log" 2>&1
check "--dry sem órfão sai 0"          "0" "$?"

# execução real (mock claude, zero API): recusa ANTES de invocar o mock
MOCKBIN="$WORK/mockbin"; mkdir -p "$MOCKBIN"
cat > "$MOCKBIN/claude" <<'MOCK'
#!/usr/bin/env bash
echo "invoked" >> "$MOCK_LOG"
echo '{"type":"result","subtype":"success"}'
MOCK
chmod +x "$MOCKBIN/claude"
: > "$WORK/mock-invoked.log"
MOCK_LOG="$WORK/mock-invoked.log" PATH="$MOCKBIN:$PATH" \
    "$SKILLTRIG" --cases "$WORK/orphan-cases.tsv" --model mock-model --runs 1 \
    > "$WORK/orphan-real.log" 2>&1
check "execução real com órfão recusa (exit 1)" "1" "$?"
check "e NÃO chama o claude nem uma vez"          "0" "$(wc -l < "$WORK/mock-invoked.log" | tr -d ' ')"

# ── 7. test-orchestrator-routing.sh: validação de agente/skill/tier ─────────
echo ""
echo "7. test-orchestrator-routing.sh valida agente/skill/tier no --dry:"

printf 'x1\tno-such-agent-xyz\t-\t-\t-\tprompt um\n' > "$WORK/bad-agent.tsv"
printf 'x1\t!no-such-agent-xyz\t-\t-\tsim\tprompt um\n' > "$WORK/bad-dispatch.tsv"
printf 'x1\tdebugger|no-such-agent-xyz\t-\t-\t-\tprompt um\n' > "$WORK/bad-alt.tsv"
printf 'x1\tdebugger\ttdd-workflow\thaiku\t-\tprompt um\n' > "$WORK/good-case.tsv"

"$ROUTING" --cases "$WORK/bad-agent.tsv" --dry > "$WORK/bad-agent.log" 2>&1
check "agente inexistente: --dry sai 1"     "1" "$?"

"$ROUTING" --cases "$WORK/bad-dispatch.tsv" --dry > "$WORK/bad-dispatch.log" 2>&1
check "!agente inexistente: --dry sai 1"    "1" "$?"

"$ROUTING" --cases "$WORK/bad-alt.tsv" --dry > "$WORK/bad-alt.log" 2>&1
check "alternativa ruim em a|b: --dry sai 1" "1" "$?"

"$ROUTING" --cases "$WORK/good-case.tsv" --dry > "$WORK/good-case.log" 2>&1
check "caso válido: --dry sai 0"             "0" "$?"

# ── 8. veredito da suíte (crítico × --allow-flaky × NOT RUN) ────────────────
echo ""
echo "8. suite_verdict — crítico pesa mais, NOT RUN crítico é incompleta:"

printf '%s\n' '{"id":"c1","verdict":"FLAKY","critical":true}' > "$WORK/crit-flaky.jsonl"
suite_verdict "$WORK/crit-flaky.jsonl" 1 > "$WORK/crit-flaky-out.log"
check "crítico FLAKY + --allow-flaky reprova" "1" "$?"
check "e diz FAIL"                            "PASS" "$(grep -q '^FAIL$' "$WORK/crit-flaky-out.log" && echo PASS || echo FAIL)"

printf '%s\n' '{"id":"c1","verdict":"FLAKY","critical":false}' > "$WORK/noncrit-flaky.jsonl"
suite_verdict "$WORK/noncrit-flaky.jsonl" 1 > "$WORK/noncrit-flaky-out.log"
check "não crítico FLAKY + --allow-flaky aprova" "0" "$?"
check "e diz PASS"                               "PASS" "$(grep -q '^PASS$' "$WORK/noncrit-flaky-out.log" && echo PASS || echo FAIL)"

printf '%s\n' '{"id":"c1","verdict":"NOT RUN","critical":true}' > "$WORK/crit-notrun.jsonl"
suite_verdict "$WORK/crit-notrun.jsonl" 0 > "$WORK/crit-notrun-out.log"
check "crítico NOT RUN é 'incompleta' (exit 2)" "2" "$?"
check "e diz INCOMPLETE"                        "PASS" "$(grep -q '^INCOMPLETE$' "$WORK/crit-notrun-out.log" && echo PASS || echo FAIL)"

printf '%s\n' '{"id":"c1","verdict":"PASS","critical":true}' '{"id":"c2","verdict":"PASS","critical":false}' > "$WORK/all-pass.jsonl"
suite_verdict "$WORK/all-pass.jsonl" 0 > /dev/null
check "tudo PASS aprova"                        "0" "$?"

# ERROR = não medido (is_error sem ser cota: login ausente, API caída). Visto no piloto
# E1 de 2026-09-29: 2/2 casos ERROR e a suíte saiu PASS. Nada medido não é aprovado.
printf '%s\n' '{"id":"c1","verdict":"ERROR","critical":false}' '{"id":"c2","verdict":"PASS","critical":false}' > "$WORK/err.jsonl"
suite_verdict "$WORK/err.jsonl" 0 > "$WORK/err-out.log"
check "caso ERROR deixa a suíte 'incompleta' (exit 2)" "2" "$?"
check "e diz INCOMPLETE"                               "PASS" "$(grep -q '^INCOMPLETE$' "$WORK/err-out.log" && echo PASS || echo FAIL)"

printf '%s\n' '{"id":"c1","verdict":"ERROR","critical":false}' '{"id":"c2","verdict":"FAIL","critical":false}' > "$WORK/err-fail.jsonl"
suite_verdict "$WORK/err-fail.jsonl" 0 > /dev/null
check "FAIL medido prevalece sobre ERROR (exit 1)" "1" "$?"

# ── 9. eval_report.py: categoria + críticos no topo ─────────────────────────
echo ""
echo "9. eval_report.py — linha por categoria e críticos reprovados no topo:"

python3 - "$EVAL_REPORT" > "$WORK/report.md" <<'PY'
import json, subprocess, sys
gen = sys.argv[1]
payload = {
    "suite": "trigger", "model": "mock-model", "runs": 3, "command": "x",
    "started": "2026-09-28T00:00:00Z", "duration_s": 1,
    "repo_sha": "abc1234", "repo_version": "5.1.0", "dirty": False, "home": "/tmp",
    "tokens": {"input": 1, "output": 1, "cache_read": 0, "cache_create": 0},
    "cases": [
        {"id": "s/n1-", "k": 1, "n": 3, "verdict": "FLAKY", "detail": "negou e disparou",
         "category": "negacao", "critical": True},
        {"id": "s/p1+", "k": 3, "n": 3, "verdict": "PASS", "detail": "", "category": "positivo", "critical": False},
        {"id": "s/p2+", "k": 0, "n": 3, "verdict": "FAIL", "detail": "", "category": "positivo", "critical": False},
        {"id": "s/v1-", "k": 3, "n": 3, "verdict": "PASS", "detail": "", "category": "vizinho", "critical": False},
        {"id": "s/i1-", "k": 3, "n": 3, "verdict": "PASS", "detail": "", "category": "irrelevante", "critical": False},
    ],
}
p = subprocess.run([sys.executable, gen], input=json.dumps(payload), text=True, stdout=subprocess.PIPE)
sys.stdout.write(p.stdout)
PY

check "traz a coluna Categoria"        "PASS" "$(grep -q '| Caso | Categoria | k de N |' "$WORK/report.md" && echo PASS || echo FAIL)"
check "resumo por categoria: positivo 1/2" "PASS" "$(grep -q 'positivo.*1/2 PASS' "$WORK/report.md" && echo PASS || echo FAIL)"
check "resumo por categoria: negacao 0/1"  "PASS" "$(grep -q 'negacao.*0/1 PASS' "$WORK/report.md" && echo PASS || echo FAIL)"
check "resumo por categoria: vizinho 1/1"  "PASS" "$(grep -q 'vizinho.*1/1 PASS' "$WORK/report.md" && echo PASS || echo FAIL)"
check "lista o crítico reprovado"          "PASS" "$(grep -q 's/n1-' "$WORK/report.md" && grep -q 'Críticos reprovados' "$WORK/report.md" && echo PASS || echo FAIL)"

crit_line=$(grep -n '## Críticos reprovados' "$WORK/report.md" | head -1 | cut -d: -f1)
resultado_line=$(grep -n '^\*\*Resultado:\*\*' "$WORK/report.md" | head -1 | cut -d: -f1)
check "críticos reprovados aparecem ANTES do Resultado" "PASS" \
    "$([ -n "$crit_line" ] && [ -n "$resultado_line" ] && [ "$crit_line" -lt "$resultado_line" ] && echo PASS || echo FAIL)"

# ── Resultado ────────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  PASS: $PASS   FAIL: $FAIL"
echo "============================================================"
[ "$FAIL" -eq 0 ]
