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
    "$HARNESS" --cases "$WORK/cases.tsv" > "$WORK/loop.log" 2>&1
loop_exit=$?
set -e
done_cases=$(grep -cE '^\[(PASS|FAIL)\]' "$WORK/loop.log" || true)
check "os 3 casos executaram (não morreu no 1º FAIL)" "3" "$done_cases"
check "placar final impresso" "PASS" "$(grep -q 'RESULTADO FINAL' "$WORK/loop.log" && echo PASS || echo FAIL)"
check "exit 1 com FAILs presentes" "1" "$loop_exit"

# ── Resultado ───────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  PASS: $PASS   FAIL: $FAIL"
echo "============================================================"
[ "$FAIL" -eq 0 ]
