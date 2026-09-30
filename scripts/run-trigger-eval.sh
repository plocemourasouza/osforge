#!/usr/bin/env bash
# =============================================================================
# run-trigger-eval.sh — liga o eval de trigger que já existia no repo (B-011, E-A46)
# =============================================================================
#
# `skills/skill-creator/scripts/run_eval.py` já sabia medir se uma description faz
# a skill disparar: `should_trigger` verdadeiro/falso, N execuções por consulta,
# `--model`. Nada em scripts/, tests/ ou deploy.sh o chamava — um eval pronto e
# desconectado. Este runner é a conexão: pega os casos de `scripts/evals/trigger/`,
# entrega no formato que ele espera e escreve o relatório versionável (B-012).
#
# POSITIVAS e NEGATIVAS. Uma description "boa" que dispara em tudo é pior que
# uma que não dispara: o custo aparece em toda sessão. Por isso cada skill tem
# 5 consultas onde ela DEVE disparar e 5 onde NÃO deve.
#
# 60/40. Cada arquivo divide os casos em `tune` (ajustar a description) e `eval`
# (medir). Ajustar olhando o conjunto de avaliação é ajustar ao teste.
#
# USO:
#   ./scripts/run-trigger-eval.sh --dry                  # valida e lista; custo zero
#   ./scripts/run-trigger-eval.sh --model claude-sonnet-4-6
#   ./scripts/run-trigger-eval.sh --model X --skill tdd-workflow --split tune
#   ./scripts/run-trigger-eval.sh --model X --report docs/evals/2026-09-18-sonnet-trigger.md
#
# CUSTO: (casos do split) × --runs chamadas de API. Com 15 skills, split `eval`
# (4 casos por skill) e --runs 3, são 180 chamadas. Comece por --skill uma só.
#
# GUARDA DE COTA (B-026, SPEC-L01 Parte B): `skills/skill-creator/scripts/
# run_eval.py` roda TODAS as consultas de uma skill numa chamada só e nunca
# devolve o stream/is_error/rate_limit_event bruto -- por isso a detecção
# mid-run (B2) que os outros dois harnesses fazem por EXECUÇÃO não é possível
# aqui. Substituto prático: preflight de cota (B3) antes de CADA bloco de
# skill, não só uma vez no início -- se uma rejeição aconteceu durante o
# bloco anterior, o Stop hook (Parte A, session-save.py) já deve ter
# atualizado quota.json a tempo do preflight seguinte. `quota.json` acima de
# OSFORGE_EVAL_QUOTA_STOP (padrão 85) ou com rejeição de reset futuro PARA
# antes do próximo bloco: exit 75 (EX_TEMPFAIL), blocos restantes NOT RUN.
# --ignore-quota desliga a checagem.
# =============================================================================
set -uo pipefail

EX_TEMPFAIL=75

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CASES_DIR="$SCRIPT_DIR/evals/trigger"
RUN_EVAL="$REPO_ROOT/skills/skill-creator/scripts/run_eval.py"

MODEL=""; RUNS="${OSFORGE_TEST_RUNS:-3}"; SPLIT="all"; ONLY=""; DRY=0; REPORT_FILE=""
TIMEOUT_SECS="${OSFORGE_TEST_TIMEOUT:-60}"; WORKERS="${OSFORGE_EVAL_WORKERS:-4}"
HOME_OVERRIDE=""
IGNORE_QUOTA=0               # --ignore-quota: desliga a guarda de cota (B-026)

while [ $# -gt 0 ]; do
    case "$1" in
        --model)  MODEL="$2"; shift 2 ;;
        --runs)   RUNS="$2"; shift 2 ;;
        --split)  SPLIT="$2"; shift 2 ;;   # tune | eval | all
        --skill)  ONLY="$2"; shift 2 ;;    # CSV de nomes de skill
        --home)   HOME_OVERRIDE="$2"; shift 2 ;;
        --report) REPORT_FILE="$2"; shift 2 ;;
        --dry)    DRY=1; shift ;;
        --ignore-quota) IGNORE_QUOTA=1; shift ;;
        --help|-h) sed -n '2,38p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "argumento desconhecido: $1 (use --help)"; exit 1 ;;
    esac
done

case "$SPLIT" in tune|eval|all) : ;; *) echo "[ERRO] --split aceita tune|eval|all"; exit 1 ;; esac
case "$RUNS" in ''|*[!0-9]*|0) echo "[ERRO] --runs precisa ser inteiro ≥ 1"; exit 1 ;; esac
[ -d "$CASES_DIR" ] || { echo "[ERRO] sem casos em $CASES_DIR"; exit 1; }

# shellcheck source=lib/harness-assertions.sh
source "$SCRIPT_DIR/lib/harness-assertions.sh"

# ── Validação dos arquivos de caso (roda sempre, inclusive em --dry) ─────────
# Schema osforge/trigger-eval/v2 (N-01/B-025): cada caso ganha "category" —
# positivo/vizinho/irrelevante/negacao — e, quando aplicável, "critical" e
# "expect_route". Um FLAKY sozinho não diz ONDE a skill falha; a categoria diz
# se foi no caso difícil (vizinho), no fácil (irrelevante) ou no que desobedece
# o usuário (negacao) — ver docs/intake/needle/SPEC-N01-casos-de-eval.md.
validate() {
    python3 - "$CASES_DIR" "$REPO_ROOT" <<'PY'
import json, os, re, sys

cases_dir, repo = sys.argv[1:3]
VALID_CATEGORIES = {"positivo", "vizinho", "irrelevante", "negacao"}
MIN_BY_CATEGORY = {"positivo": 5, "vizinho": 2, "negacao": 1, "irrelevante": 1}

_skill_names = None


def skill_exists(name):
    """A skill identifier resolves if it matches a skill dir name or its
    frontmatter `name:`, anywhere under skills/ — not just the 15 skills
    this suite measures. `expect_route` routinely points elsewhere."""
    global _skill_names
    if _skill_names is None:
        _skill_names = set()
        root = os.path.join(repo, "skills")
        for dirpath, _dirs, filenames in os.walk(root):
            if "SKILL.md" not in filenames:
                continue
            _skill_names.add(os.path.basename(dirpath))
            text = open(os.path.join(dirpath, "SKILL.md"), encoding="utf-8", errors="replace").read()
            m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
            if m:
                n = re.search(r'^name:\s*["\']?([^"\'#\n]+)["\']?\s*$', m.group(1), re.M)
                if n:
                    _skill_names.add(n.group(1).strip())
    return name in _skill_names


errs, total, skills, critical_total = [], 0, 0, 0
seen_q = {}
for f in sorted(os.listdir(cases_dir)):
    if not f.endswith(".json"):
        continue
    p = os.path.join(cases_dir, f)
    try:
        d = json.load(open(p, encoding="utf-8"))
    except ValueError as exc:
        errs.append(f"{f}: JSON inválido ({exc})"); continue
    skills += 1
    rel = d.get("rel", "")
    if not os.path.isfile(os.path.join(repo, "skills", rel, "SKILL.md")):
        errs.append(f"{f}: rel '{rel}' não aponta para uma skill existente")
    ids = [c["id"] for c in d.get("cases", [])]
    if len(ids) != len(set(ids)):
        errs.append(f"{f}: ids repetidos")
    pos = [c for c in d["cases"] if c["should_trigger"]]
    neg = [c for c in d["cases"] if not c["should_trigger"]]
    if len(pos) < 5 or len(neg) < 5:
        errs.append(f"{f}: {len(pos)} positivas / {len(neg)} negativas (mínimo 5+5)")
    split = d.get("split", {})
    cover = set(split.get("tune", [])) | set(split.get("eval", []))
    if set(ids) - cover:
        errs.append(f"{f}: casos fora do split: {sorted(set(ids) - cover)}")
    if set(split.get("tune", [])) & set(split.get("eval", [])):
        errs.append(f"{f}: caso em tune E eval ao mesmo tempo")

    cat_count = {}
    for c in d["cases"]:
        q = c["query"].strip().lower()
        if q in seen_q and seen_q[q] != f:
            errs.append(f"{f}: consulta repetida de {seen_q[q]}: {q[:50]}")
        seen_q[q] = f
        total += 1

        cat = c.get("category")
        if cat is None:
            errs.append(f"{f}: caso {c['id']} sem 'category'")
        elif cat not in VALID_CATEGORIES:
            errs.append(f"{f}: caso {c['id']} categoria desconhecida '{cat}'")
        else:
            cat_count[cat] = cat_count.get(cat, 0) + 1
            expected_trigger = (cat == "positivo")
            if c["should_trigger"] != expected_trigger:
                errs.append(
                    f"{f}: caso {c['id']} categoria '{cat}' incoerente com "
                    f"should_trigger={c['should_trigger']}"
                )
            if cat == "negacao" and c.get("critical") is not True:
                errs.append(f"{f}: caso {c['id']} é negacao mas não tem critical:true")

        if "critical" in c:
            if not isinstance(c["critical"], bool):
                errs.append(f"{f}: caso {c['id']} 'critical' não é booleano")
            elif c["critical"]:
                critical_total += 1

        route = c.get("expect_route")
        if route and not skill_exists(route):
            errs.append(f"{f}: caso {c['id']} expect_route '{route}' não aponta para skill existente")

    for cat, minimum in MIN_BY_CATEGORY.items():
        got = cat_count.get(cat, 0)
        if got < minimum:
            errs.append(f"{f}: {got} caso(s) '{cat}' (mínimo {minimum})")

for e in errs:
    print(f"  ❌ {e}")
print(f"validação: {skills} skills, {total} casos, {critical_total} críticos, {len(errs)} problema(s)")
sys.exit(1 if errs else 0)
PY
}

echo "============================================================"
echo "OSForge Trigger Eval (positivas + negativas)"
echo "============================================================"
echo "Casos  : $CASES_DIR"
echo "Split  : $SPLIT"
echo "Modelo : ${MODEL:-'(dry-run)'}"
echo "Runs   : $RUNS"
echo "============================================================"

validate || { echo "[ERRO] corrija os casos antes de rodar."; exit 1; }

# Lista de (arquivo, skill, rel) já filtrada por --skill
MANIFEST="$(mktemp)"; trap 'rm -f "$MANIFEST"' EXIT
python3 - "$CASES_DIR" "$ONLY" > "$MANIFEST" <<'PY'
import json, os, sys
cases_dir, only = sys.argv[1], sys.argv[2]
want = {x.strip() for x in only.split(",") if x.strip()}
for f in sorted(os.listdir(cases_dir)):
    if not f.endswith(".json"):
        continue
    d = json.load(open(os.path.join(cases_dir, f), encoding="utf-8"))
    if want and d["skill"] not in want:
        continue
    print("\t".join([os.path.join(cases_dir, f), d["skill"], d["rel"]]))
PY
[ -s "$MANIFEST" ] || { echo "[ERRO] nenhum arquivo de caso corresponde a --skill '$ONLY'"; exit 1; }

if [ "$DRY" = "1" ]; then
    echo ""
    echo "MODO SECO — nenhum modelo é chamado, nenhum token é gasto."
    while IFS=$'\t' read -r file skill rel; do
        python3 - "$file" "$SPLIT" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); split = sys.argv[2]
sel = d["split"].get(split) if split in ("tune", "eval") else [c["id"] for c in d["cases"]]
print(f"\n{d['skill']}  ({'core' if d.get('core') else 'manifesto'} · {d['rel']})")
for c in d["cases"]:
    if c["id"] not in sel:
        continue
    mark = "＋" if c["should_trigger"] else "－"
    print(f"   {mark} {c['id']:3} {c['query']}")
PY
    done < "$MANIFEST"
    n=$(python3 - "$MANIFEST" "$SPLIT" <<'PY'
import json, sys
tot = 0
for line in open(sys.argv[1], encoding="utf-8"):
    f = line.split("\t")[0]
    d = json.load(open(f, encoding="utf-8")); split = sys.argv[2]
    sel = d["split"].get(split) if split in ("tune", "eval") else [c["id"] for c in d["cases"]]
    tot += len(sel)
print(tot)
PY
)
    echo ""
    echo "$n caso(s) no split '$SPLIT'. Rodada real custaria $((n * RUNS)) chamadas de API."
    echo "Para rodar: --model <id> [--runs N] [--skill nome]"
    exit 0
fi

[ -n "$MODEL" ] || { echo "[ERRO] --model é obrigatório fora de --dry (E-A45). Para listar: --dry"; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "[ERRO] claude CLI não encontrado no PATH"; exit 1; }
[ -f "$RUN_EVAL" ] || { echo "[ERRO] run_eval.py não encontrado em $RUN_EVAL"; exit 1; }

OUT_BASE="$(mktemp -d)"
CASE_JSON="$OUT_BASE/cases.json"; : > "$CASE_JSON"
# Neutral project for `claude -p`: run_eval.py writes its command clone under the
# first `.claude/` above the cwd. From inside this repo the OSForge project rules
# (hub session: "never execute another repo's code here") answered the query
# before any skill was considered — first paid pilot, 2026-09-29: 0/15 triggers.
EVAL_PROJECT="$OUT_BASE/project"; mkdir -p "$EVAL_PROJECT/.claude/commands"
START_EPOCH=$(date +%s)
TOTAL_PASS=0; TOTAL_FAIL=0
QUOTA_STOPPED=0
QUOTA_REASON=""
SKILL_IDX=0
NOT_RUN_FROM=""

# Guarda de cota (B-026, B3): snapshot ANTES de gastar qualquer chamada de API.
QUOTA_AT_START="$(quota_snapshot)"

while IFS=$'\t' read -r file skill rel; do
    SKILL_IDX=$((SKILL_IDX + 1))
    # B3: preflight de cota antes de CADA bloco de skill (ver nota no topo do
    # arquivo sobre por que é por-bloco, e não por-consulta, aqui). Fail-open
    # por design -- só para quando há motivo explícito.
    if [ "$IGNORE_QUOTA" = "0" ]; then
        preflight_reason="$(quota_preflight_reason || true)"
        if [ -n "$preflight_reason" ]; then
            echo ""
            echo "[cota] $preflight_reason -- parando antes de '$skill'"
            QUOTA_STOPPED=1
            QUOTA_REASON="cota: $preflight_reason (antes de '$skill')"
            NOT_RUN_FROM="$SKILL_IDX"
            break
        fi
    fi

    echo ""
    echo "------------------------------------------------------------"
    echo "skill: $skill"
    set_file="$OUT_BASE/${skill//\//-}.eval.json"
    python3 - "$file" "$SPLIT" > "$set_file" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); split = sys.argv[2]
sel = d["split"].get(split) if split in ("tune", "eval") else [c["id"] for c in d["cases"]]
# formato que skills/skill-creator/scripts/run_eval.py consome
print(json.dumps([{"query": c["query"], "should_trigger": c["should_trigger"]}
                  for c in d["cases"] if c["id"] in sel], ensure_ascii=False))
PY
    res="$OUT_BASE/${skill//\//-}.result.json"
    # PYTHONPATH: run_eval.py imports `scripts.utils`; `python3 <file>` puts the script's
    # own dir on sys.path, not the cwd (first real E1 run, 2026-09-29: 15/15 rc=1).
    ( cd "$EVAL_PROJECT" && \
      env ${HOME_OVERRIDE:+HOME="$HOME_OVERRIDE"} PYTHONPATH="$REPO_ROOT/skills/skill-creator" python3 "$RUN_EVAL" \
        --eval-set "$set_file" \
        --skill-path "$REPO_ROOT/skills/$rel" \
        --model "$MODEL" \
        --runs-per-query "$RUNS" \
        --num-workers "$WORKERS" \
        --timeout "$TIMEOUT_SECS" \
        --verbose ) > "$res" 2>"$res.err"
    rc=$?
    if [ "$rc" != "0" ] || [ ! -s "$res" ]; then
        echo "  ❌ run_eval falhou (rc=$rc). stderr: $(tail -3 "$res.err" 2>/dev/null)"
        printf '{"id":"%s","k":0,"n":1,"verdict":"FAIL","detail":"run_eval falhou (rc=%s)"}\n' "$skill" "$rc" >> "$CASE_JSON"
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
        continue
    fi
    # Um caso por CONSULTA no relatório: é a granularidade que permite consertar
    # a description sabendo qual frase falhou.
    python3 - "$res" "$skill" "$RUNS" "$file" "$SPLIT" >> "$CASE_JSON" <<'PY'
import json, sys
res, skill, runs, src, split = sys.argv[1:6]
d = json.load(open(res, encoding="utf-8"))
doc = json.load(open(src, encoding="utf-8"))
by_q = {c["query"]: c for c in doc["cases"]}
for r in d.get("results", []):
    c = by_q.get(r["query"], {})
    kind = "+" if r["should_trigger"] else "-"
    k = r["triggers"] if r["should_trigger"] else r["runs"] - r["triggers"]
    print(json.dumps({
        "id": f"{skill}/{c.get('id', '?')}{kind}",
        "k": int(k), "n": int(r["runs"]),
        "verdict": "PASS" if r["pass"] and k == r["runs"] else ("PASS" if r["pass"] else ("FLAKY" if 0 < k < r["runs"] else "FAIL")),
        "detail": ("deve disparar" if r["should_trigger"] else "NÃO deve disparar") + f" · {r['query'][:60]}",
        "category": c.get("category"),
        "critical": bool(c.get("critical", False)),
    }, ensure_ascii=False))
PY
    s_pass=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['summary']['passed'])" "$res")
    s_tot=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['summary']['total'])" "$res")
    echo "  $s_pass/$s_tot consultas OK"
    TOTAL_PASS=$((TOTAL_PASS + s_pass)); TOTAL_FAIL=$((TOTAL_FAIL + s_tot - s_pass))
done < "$MANIFEST"

# B3: lote parado por cota -- toda skill do ponto de parada em diante (a
# corrente inclusive, ela nunca chamou run_eval.py) sai NOT RUN, por consulta,
# no relatório -- não conta como hit nem como miss.
if [ "$QUOTA_STOPPED" = "1" ] && [ -n "$NOT_RUN_FROM" ]; then
    tail -n +"$NOT_RUN_FROM" "$MANIFEST" | while IFS=$'\t' read -r rfile rskill _rrel; do
        [ -z "$rfile" ] && continue
        python3 - "$rfile" "$rskill" "$SPLIT" "$RUNS" >> "$CASE_JSON" <<'PY'
import json, sys
src, skill, split, runs = sys.argv[1:5]
d = json.load(open(src, encoding="utf-8"))
sel = d["split"].get(split) if split in ("tune", "eval") else [c["id"] for c in d["cases"]]
for c in d["cases"]:
    if c["id"] not in sel:
        continue
    kind = "+" if c["should_trigger"] else "-"
    print(json.dumps({
        "id": f"{skill}/{c['id']}{kind}", "k": 0, "n": int(runs), "verdict": "NOT RUN",
        "detail": "quota: lote interrompido antes de iniciar",
        "category": c.get("category"), "critical": bool(c.get("critical", False)),
    }, ensure_ascii=False))
PY
    done
fi
QUOTA_AT_END="$(quota_snapshot)"
export QUOTA_AT_START QUOTA_AT_END

echo ""
echo "============================================================"
echo "RESULTADO — TRIGGER EVAL"
echo "============================================================"
echo "  consultas OK : $TOTAL_PASS"
echo "  consultas NOK: $TOTAL_FAIL"
if [ "$QUOTA_STOPPED" = "1" ]; then
    echo "  NOT RUN      : cota ($QUOTA_REASON)"
fi
echo "  artefatos    : $OUT_BASE"
echo "============================================================"

if [ -n "$REPORT_FILE" ]; then
    MODEL="$MODEL" RUNS="$RUNS" HOME_OVERRIDE="$HOME_OVERRIDE" \
        emit_eval_report "trigger" "$REPORT_FILE" "$CASE_JSON" "$START_EPOCH" "$(printf '%s ' "$0" "$@")"
fi

# B2/B3: lote interrompido por cota -- exit 75 (EX_TEMPFAIL), distinto do
# veredito de suíte. Não é "reprovado", é "não terminou".
if [ "$QUOTA_STOPPED" = "1" ]; then
    echo "[QUOTA] $QUOTA_REASON"
    exit "$EX_TEMPFAIL"
fi

# Veredito da suíte (N-01/B-025, B-026): um caso crítico que não seja PASS
# reprova mesmo que TOTAL_FAIL pareça pequeno (harness-assertions.sh: suite_verdict).
suite_result="$(suite_verdict "$CASE_JSON" "0")"
suite_exit=$?
echo "  Veredito da suíte: $suite_result"
[ "$TOTAL_FAIL" -eq 0 ] && [ "$suite_exit" -eq 0 ]
