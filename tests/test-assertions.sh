#!/usr/bin/env bash
# =============================================================================
# test-assertions.sh — testa a LÓGICA DE VEREDITO do harness de triggering
# =============================================================================
#
# O harness real (`scripts/test-skill-triggering.sh`) chama o `claude` CLI e
# consome API a cada caso. A lógica que decide PASS/FAIL, porém, é pura: recebe
# um stream-json e devolve um veredito. Este teste exercita essa lógica com
# streams sintéticos — roda em milissegundos, custo zero, e pega regressão na
# asserção sem depender de o modelo se comportar.
#
# USO:  ./tests/test-assertions.sh
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HARNESS="$REPO_ROOT/scripts/test-skill-triggering.sh"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# A mesma biblioteca que o harness usa — não uma cópia, nem um trecho extraído.
# (A versão anterior fatiava o harness com sed e sourceava via process
# substitution: silenciosamente não definia nada no bash 3.2 do macOS, e o
# relatório acusava "asserção falhou" em vez de "biblioteca não carregou".)
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

verdict() { if "$@" >/dev/null 2>&1; then echo PASS; else echo FAIL; fi; }

# ── Fixtures ────────────────────────────────────────────────────────────────

# 1. Skill invocada nativamente
cat > "$WORK/native.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"text","text":"Vou aplicar TDD."}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"tdd-workflow"}}]}}
EOF

# 2. Skill invocada com namespace
cat > "$WORK/namespaced.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"osforge:tdd-workflow"}}]}}
EOF

# 3. Skill não-core alcançada pelo manifesto (Read do SKILL.md)
cat > "$WORK/resolved.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"text","text":"O manifesto aponta essa skill."}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Read","input":{"file_path":"/Users/x/Development/osforge/skills/brandkit/SKILL.md"}}]}}
EOF

# 4. Só CITA o caminho, sem ler — não pode contar como alcançada
cat > "$WORK/mentioned.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"text","text":"Existe skills/brandkit/SKILL.md, mas não vou usar."}]}}
EOF

# 5. Nada aconteceu
cat > "$WORK/nothing.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"text","text":"Claro, posso ajudar com isso."}]}}
EOF

# 6. Disparou a skill ERRADA
cat > "$WORK/wrong.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"clean-code"}}]}}
EOF

# 7. MESMA mensagem: um bloco de texto cita o caminho, outro bloco lê OUTRO arquivo.
#    O grep por LINHA dava PASS aqui — a linha continha o nome da ferramenta e o
#    caminho, em blocos diferentes. É a regressão que B-010 fecha.
cat > "$WORK/same-line-decoy.json" <<'EOF'
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"O manifesto aponta skills/brandkit/SKILL.md"},{"type":"tool_use","name":"Read","input":{"file_path":"/repo/README.md"}}]}}
EOF

# 8. Despacho real de subagente (delegou) × só anúncio no texto (não delegou)
cat > "$WORK/dispatch-real.json" <<'EOF'
{"type":"assistant","message":{"role":"assistant","content":[{"type":"tool_use","name":"Task","input":{"subagent_type":"security-auditor","prompt":"audite o login"}}]}}
EOF
cat > "$WORK/dispatch-announce-only.json" <<'EOF'
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"@security-auditor vai olhar isso. Encontrei 3 problemas: ..."}]}}
EOF

# ── Asserção de invocação nativa ────────────────────────────────────────────
echo "check_skill_triggered:"
check "invocação direta"                PASS "$(verdict check_skill_triggered "$WORK/native.json" tdd-workflow)"
check "invocação com namespace"         PASS "$(verdict check_skill_triggered "$WORK/namespaced.json" tdd-workflow)"
check "skill errada não passa"          FAIL "$(verdict check_skill_triggered "$WORK/wrong.json" tdd-workflow)"
check "stream vazio não passa"          FAIL "$(verdict check_skill_triggered "$WORK/nothing.json" tdd-workflow)"
check "Read não conta como invocação"   FAIL "$(verdict check_skill_triggered "$WORK/resolved.json" brandkit)"

# ── Asserção de resolução via manifesto ─────────────────────────────────────
echo ""
echo "check_skill_resolved:"
check "Read do SKILL.md resolve"        PASS "$(verdict check_skill_resolved "$WORK/resolved.json" brandkit)"
check "só mencionar o path NÃO resolve" FAIL "$(verdict check_skill_resolved "$WORK/mentioned.json" brandkit)"
check "path de outra skill não resolve" FAIL "$(verdict check_skill_resolved "$WORK/resolved.json" clean-code)"
check "rel vazio não resolve"           FAIL "$(verdict check_skill_resolved "$WORK/resolved.json" '')"

# carga por procuração: despacho de subagente citando a skill
cat > "$WORK/proxied.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Task","input":{"subagent_type":"security-auditor","prompt":"read skills/security-threat-model/SKILL.md and apply it"}}]}}
EOF
check "despacho citando a skill resolve" PASS "$(verdict check_skill_resolved "$WORK/proxied.json" security-threat-model)"
check "despacho de outra skill não"      FAIL "$(verdict check_skill_resolved "$WORK/proxied.json" brandkit)"

# ── Mapa nome→path e classificação core ─────────────────────────────────────
echo ""
echo "skill_rel_path / is_core_skill:"
build_skill_map
check "nome == diretório"      "tdd-workflow"      "$(skill_rel_path tdd-workflow)"
check "skill aninhada"         "quality/code-review" "$(skill_rel_path code-review)"
check "nome != diretório"      "evolve"            "$(skill_rel_path osforge-evolve)"
check "skill inexistente"      ""                  "$(skill_rel_path nao-existe-mesmo)"
check "tdd-workflow é core"    PASS "$(verdict is_core_skill tdd-workflow)"
check "brandkit não é core"    FAIL "$(verdict is_core_skill brandkit)"

# ── Precisão por bloco e delegação real (B-010) ─────────────────────────────
echo ""
echo "precisão por bloco (B-010):"
check "citar o caminho e ler OUTRO arquivo não conta" FAIL "$(verdict check_skill_resolved "$WORK/same-line-decoy.json" brandkit)"
check "leitura de verdade conta"                      PASS "$(verdict check_skill_resolved "$WORK/resolved.json" brandkit)"

echo ""
echo "check_agent_dispatched (delegação exigida):"
check "despacho real passa"                    PASS "$(verdict check_agent_dispatched "$WORK/dispatch-real.json" "security-auditor")"
check "só anúncio @nome NÃO passa"             FAIL "$(verdict check_agent_dispatched "$WORK/dispatch-announce-only.json" "security-auditor")"
check "anúncio ainda satisfaz agent_routed"    PASS "$(verdict check_agent_routed "$WORK/dispatch-announce-only.json" "security-auditor")"
check "agente errado no despacho não passa"    FAIL "$(verdict check_agent_dispatched "$WORK/dispatch-real.json" "game-developer")"

# ── Asserções de roteamento (orquestrador) ──────────────────────────────────
echo ""
echo "check_agent_routed / check_tier_mentioned:"

cat > "$WORK/route-announce.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"text","text":"🤖 Applying expertise from @debugger + @backend-engineer...\nVamos reproduzir o 500."}]}}
EOF
cat > "$WORK/route-dispatch.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Task","input":{"subagent_type":"security-auditor","prompt":"audit auth"}}]}}
EOF
cat > "$WORK/route-plan.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"text","text":"## Roster\n- model: sonnet — implementação\n- agent: frontend-engineer"}]}}
EOF
cat > "$WORK/route-none.json" <<'EOF'
{"type":"assistant","message":{"content":[{"type":"text","text":"Aqui está a resposta direta, sem roteamento."}]}}
EOF

check "anúncio @persona"               PASS "$(verdict check_agent_routed "$WORK/route-announce.json" "debugger|frontend-engineer")"
check "despacho subagent_type"          PASS "$(verdict check_agent_routed "$WORK/route-dispatch.json" "security-auditor")"
check "agente errado não passa"         FAIL "$(verdict check_agent_routed "$WORK/route-dispatch.json" "game-developer")"
check "sem roteamento não passa"        FAIL "$(verdict check_agent_routed "$WORK/route-none.json" "debugger")"
check "tier citado no Roster"           PASS "$(verdict check_tier_mentioned "$WORK/route-plan.json" "sonnet|opus")"
check "tier ausente não passa"          FAIL "$(verdict check_tier_mentioned "$WORK/route-none.json" "opus")"

# ── Sobrevivência do loop (regressão do set -e) ─────────────────────────────
# run_case tem um `set -e` interno que reativava o errexit global e matava o
# harness no PRIMEIRO FAIL — duas rodadas reais morreram sem placar. Este teste
# roda o harness DE VERDADE com um claude falso (zero API): 3 casos, todos FAIL,
# e exige que os 3 executem e o placar final saia.
echo ""
echo "loop survival (harness completo com claude mock):"
MOCKBIN="$WORK/mockbin"
mkdir -p "$MOCKBIN"
cat > "$MOCKBIN/claude" <<'MOCK'
#!/usr/bin/env bash
echo '{"type":"system","subtype":"init","tools":["Skill","Read"],"mcp_servers":[]}'
echo '{"type":"assistant","message":{"content":[{"type":"text","text":"sem skill"}],"usage":{"input_tokens":1}}}'
echo '{"type":"result","subtype":"success"}'
MOCK
chmod +x "$MOCKBIN/claude"
printf 'tdd-workflow\tcaso um\nclean-code\tcaso dois\ngrilling\tcaso tres\n' > "$WORK/cases.tsv"
set +e
PATH="$MOCKBIN:$PATH" OSFORGE_TEST_TIMEOUT=10 \
    "$HARNESS" --cases "$WORK/cases.tsv" --model mock-model --runs 1 > "$WORK/loop.log" 2>&1
loop_exit=$?
set -e
done_cases=$(grep -cE '^ +\[FAIL 0/1\]' "$WORK/loop.log" || true)
check "os 3 casos executaram (não morreu no 1º FAIL)" "3" "$done_cases"
check "placar final impresso" "PASS" "$(grep -q 'RESULTADO FINAL' "$WORK/loop.log" && echo PASS || echo FAIL)"
check "exit 1 com FAILs presentes" "1" "$loop_exit"

# ── B-010: modelo obrigatório, modo seco, k de N, relatório ─────────────────
echo ""
echo "modelo obrigatório e modo seco (B-010):"
set +e
PATH="$MOCKBIN:$PATH" "$HARNESS" --cases "$WORK/cases.tsv" > "$WORK/nomodel.log" 2>&1
nomodel_exit=$?
set -e
check "sem --model o harness recusa rodar" "1" "$nomodel_exit"
check "e explica o porquê" "PASS" "$(grep -q -- '--model é obrigatório' "$WORK/nomodel.log" && echo PASS || echo FAIL)"

# --dry com um PATH sem claude nenhum: prova que o modo seco não chama modelo
set +e
env PATH="/usr/bin:/bin" "$HARNESS" --cases "$WORK/cases.tsv" --dry > "$WORK/dry.log" 2>&1
dry_exit=$?
set -e
check "--dry sai 0 mesmo sem claude instalado" "0" "$dry_exit"
check "--dry lista os 3 casos" "3" "$(grep -cE '^ *[0-9]+\. ' "$WORK/dry.log" || true)"
check "--dry avisa que não chama modelo" "PASS" "$(grep -q 'nenhum modelo é chamado' "$WORK/dry.log" && echo PASS || echo FAIL)"
check "--dry diz o modo de cada caso" "PASS" "$(grep -q 'core → exige invocação nativa' "$WORK/dry.log" && echo PASS || echo FAIL)"

echo ""
echo "k de N e relatório versionável (B-010/B-012):"
# claude mock que só acerta na 1ª execução → 1 de 3 = FLAKY, não PASS
cat > "$MOCKBIN/claude" <<'MOCK'
#!/usr/bin/env bash
n=$(cat "$MOCKDIR/counter" 2>/dev/null || echo 0); n=$((n+1)); echo "$n" > "$MOCKDIR/counter"
echo '{"type":"system","subtype":"init","tools":["Skill"],"mcp_servers":[]}'
if [ "$n" = "1" ]; then
  echo '{"type":"assistant","message":{"id":"m'"$n"'","role":"assistant","usage":{"input_tokens":7,"output_tokens":2},"content":[{"type":"tool_use","name":"Skill","input":{"skill":"tdd-workflow"}}]}}'
else
  echo '{"type":"assistant","message":{"id":"m'"$n"'","role":"assistant","usage":{"input_tokens":7,"output_tokens":2},"content":[{"type":"text","text":"sem skill"}]}}'
fi
echo '{"type":"result","subtype":"success"}'
MOCK
chmod +x "$MOCKBIN/claude"
printf 'tdd-workflow\tcaso instavel\n' > "$WORK/one.tsv"
rm -f "$WORK/counter"
set +e
MOCKDIR="$WORK" PATH="$MOCKBIN:$PATH" OSFORGE_TEST_TIMEOUT=10 \
    "$HARNESS" --cases "$WORK/one.tsv" --model mock-model --runs 3 \
    --report "$WORK/report.md" > "$WORK/flaky.log" 2>&1
flaky_exit=$?
set -e
check "1 acerto em 3 é FLAKY, não PASS" "PASS" "$(grep -q '\[FLAKY 1/3\]' "$WORK/flaky.log" && echo PASS || echo FAIL)"
check "FLAKY reprova a suíte" "1" "$flaky_exit"
check "cada execução teve o seu stream" "3" "$(ls "$WORK"/../ >/dev/null 2>&1; grep -c 'run [0-9]:' "$WORK/flaky.log" || true)"
check "relatório markdown foi escrito" "PASS" "$([ -s "$WORK/report.md" ] && echo PASS || echo FAIL)"
check "relatório traz k de N" "PASS" "$(grep -q '1/3' "$WORK/report.md" && echo PASS || echo FAIL)"
check "relatório traz o modelo medido" "PASS" "$(grep -q 'mock-model' "$WORK/report.md" && echo PASS || echo FAIL)"
check "relatório traz SHA e versão do repo" "PASS" "$(grep -qE 'OSForge:.*`[0-9a-f]{7,}' "$WORK/report.md" && echo PASS || echo FAIL)"
check "relatório soma tokens dos streams (3×7 in)" "PASS" "$(grep -q 'in 21' "$WORK/report.md" && echo PASS || echo FAIL)"
check "relatório lista o caso instável (entrada do E1)" "PASS" "$(grep -q 'Casos instáveis' "$WORK/report.md" && echo PASS || echo FAIL)"
rm -f "$WORK/counter"
set +e
MOCKDIR="$WORK" PATH="$MOCKBIN:$PATH" OSFORGE_TEST_TIMEOUT=10 \
    "$HARNESS" --cases "$WORK/one.tsv" --model m --runs 3 --allow-flaky >/dev/null 2>&1
allow_exit=$?
set -e
check "--allow-flaky não reprova" "0" "$allow_exit"

# ── Harness de roteamento: mesmas garantias (B-010) ─────────────────────────
echo ""
echo "harness de roteamento (B-010):"
ROUTING="$REPO_ROOT/scripts/test-orchestrator-routing.sh"
set +e
PATH="$MOCKBIN:$PATH" "$ROUTING" --id r01 > "$WORK/rt-nomodel.log" 2>&1
rt_nomodel=$?
env PATH="/usr/bin:/bin" "$ROUTING" --dry > "$WORK/rt-dry.log" 2>&1
rt_dry=$?
set -e
check "sem --model o harness de roteamento recusa" "1" "$rt_nomodel"
check "--dry roda sem claude no PATH" "0" "$rt_dry"
check "--dry lista os 16 casos" "16" "$(grep -cE '^ *[0-9]+\. r' "$WORK/rt-dry.log" || true)"
check "caso com ! exige despacho no modo seco" "PASS" "$(grep -q 'DESPACHO obrigatório' "$WORK/rt-dry.log" && echo PASS || echo FAIL)"

# ── Eval de trigger: casos válidos e modo seco (B-011) ──────────────────────
echo ""
echo "eval de trigger (B-011):"
TRIGGER="$REPO_ROOT/scripts/run-trigger-eval.sh"
set +e
env PATH="/usr/bin:/bin" "$TRIGGER" --dry > "$WORK/tg-dry.log" 2>&1
tg_dry=$?
PATH="$MOCKBIN:$PATH" "$TRIGGER" --skill tdd-workflow > "$WORK/tg-nomodel.log" 2>&1
tg_nomodel=$?
"$TRIGGER" --dry --split bogus > "$WORK/tg-badsplit.log" 2>&1
tg_badsplit=$?
set -e
check "arquivos de caso passam na validação" "PASS" "$(grep -q '0 problema(s)' "$WORK/tg-dry.log" && echo PASS || echo FAIL)"
check "--dry roda sem claude no PATH" "0" "$tg_dry"
check "15 skills com casos" "PASS" "$(grep -q 'validação: 15 skills, 150 casos' "$WORK/tg-dry.log" && echo PASS || echo FAIL)"
check "--dry informa o custo em chamadas" "PASS" "$(grep -q 'custaria 450 chamadas' "$WORK/tg-dry.log" && echo PASS || echo FAIL)"
check "sem --model recusa rodar" "1" "$tg_nomodel"
check "--split inválido recusa" "1" "$tg_badsplit"

# um arquivo de caso quebrado tem de reprovar a validação (o CI depende disso)
BADDIR="$WORK/badcases"; mkdir -p "$BADDIR"
cp "$REPO_ROOT/scripts/evals/trigger/grilling.json" "$BADDIR/"
python3 - "$BADDIR/grilling.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
d["cases"] = [c for c in d["cases"] if c["should_trigger"]]      # tira as negativas
json.dump(d, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
PY
set +e
( cd "$WORK" && env PATH="/usr/bin:/bin" OSFORGE_FAKE_CASES="$BADDIR" bash -c '
   sed "s#CASES_DIR=\"\$SCRIPT_DIR/evals/trigger\"#CASES_DIR=\"$OSFORGE_FAKE_CASES\"#" '"$TRIGGER"' > ./t.sh
   bash ./t.sh --dry' ) > "$WORK/tg-bad.log" 2>&1
tg_bad=$?
set -e
check "caso sem negativas reprova a validação" "1" "$tg_bad"
check "e diz qual é o problema" "PASS" "$(grep -q 'negativas (mínimo 5+5)' "$WORK/tg-bad.log" && echo PASS || echo FAIL)"

# ── Resultado ───────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  PASS: $PASS   FAIL: $FAIL"
echo "============================================================"
[ "$FAIL" -eq 0 ]
