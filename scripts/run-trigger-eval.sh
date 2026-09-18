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
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CASES_DIR="$SCRIPT_DIR/evals/trigger"
RUN_EVAL="$REPO_ROOT/skills/skill-creator/scripts/run_eval.py"

MODEL=""; RUNS="${OSFORGE_TEST_RUNS:-3}"; SPLIT="all"; ONLY=""; DRY=0; REPORT_FILE=""
TIMEOUT_SECS="${OSFORGE_TEST_TIMEOUT:-60}"; WORKERS="${OSFORGE_EVAL_WORKERS:-4}"
HOME_OVERRIDE=""

while [ $# -gt 0 ]; do
    case "$1" in
        --model)  MODEL="$2"; shift 2 ;;
        --runs)   RUNS="$2"; shift 2 ;;
        --split)  SPLIT="$2"; shift 2 ;;   # tune | eval | all
        --skill)  ONLY="$2"; shift 2 ;;    # CSV de nomes de skill
        --home)   HOME_OVERRIDE="$2"; shift 2 ;;
        --report) REPORT_FILE="$2"; shift 2 ;;
        --dry)    DRY=1; shift ;;
        --help|-h) sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "argumento desconhecido: $1 (use --help)"; exit 1 ;;
    esac
done

case "$SPLIT" in tune|eval|all) : ;; *) echo "[ERRO] --split aceita tune|eval|all"; exit 1 ;; esac
case "$RUNS" in ''|*[!0-9]*|0) echo "[ERRO] --runs precisa ser inteiro ≥ 1"; exit 1 ;; esac
[ -d "$CASES_DIR" ] || { echo "[ERRO] sem casos em $CASES_DIR"; exit 1; }

# shellcheck source=lib/harness-assertions.sh
source "$SCRIPT_DIR/lib/harness-assertions.sh"

# ── Validação dos arquivos de caso (roda sempre, inclusive em --dry) ─────────
validate() {
    python3 - "$CASES_DIR" "$REPO_ROOT" <<'PY'
import json, os, sys
cases_dir, repo = sys.argv[1:3]
errs, total, skills = [], 0, 0
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
    for c in d["cases"]:
        q = c["query"].strip().lower()
        if q in seen_q and seen_q[q] != f:
            errs.append(f"{f}: consulta repetida de {seen_q[q]}: {q[:50]}")
        seen_q[q] = f
        total += 1
for e in errs:
    print(f"  ❌ {e}")
print(f"validação: {skills} skills, {total} casos, {len(errs)} problema(s)")
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
START_EPOCH=$(date +%s)
TOTAL_PASS=0; TOTAL_FAIL=0

while IFS=$'\t' read -r file skill rel; do
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
    ( cd "$REPO_ROOT/skills/skill-creator" && \
      ${HOME_OVERRIDE:+env HOME="$HOME_OVERRIDE"} python3 "$RUN_EVAL" \
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
    }, ensure_ascii=False))
PY
    s_pass=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['summary']['passed'])" "$res")
    s_tot=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['summary']['total'])" "$res")
    echo "  $s_pass/$s_tot consultas OK"
    TOTAL_PASS=$((TOTAL_PASS + s_pass)); TOTAL_FAIL=$((TOTAL_FAIL + s_tot - s_pass))
done < "$MANIFEST"

echo ""
echo "============================================================"
echo "RESULTADO — TRIGGER EVAL"
echo "============================================================"
echo "  consultas OK : $TOTAL_PASS"
echo "  consultas NOK: $TOTAL_FAIL"
echo "  artefatos    : $OUT_BASE"
echo "============================================================"

if [ -n "$REPORT_FILE" ]; then
    MODEL="$MODEL" RUNS="$RUNS" HOME_OVERRIDE="$HOME_OVERRIDE" \
        emit_eval_report "trigger" "$REPORT_FILE" "$CASE_JSON" "$START_EPOCH" "$(printf '%s ' "$0" "$@")"
fi

[ "$TOTAL_FAIL" -eq 0 ]
