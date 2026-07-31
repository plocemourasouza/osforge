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

# Importa só as funções do harness, sem executar o corpo dele.
# shellcheck disable=SC1090
OUTPUT_BASE="$WORK"
source <(sed -n '/^# Helpers$/,/^# Rodar um único caso/p' "$HARNESS")

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

# ── Resultado ───────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  PASS: $PASS   FAIL: $FAIL"
echo "============================================================"
[ "$FAIL" -eq 0 ]
