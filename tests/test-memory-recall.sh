#!/usr/bin/env bash
# tests/test-memory-recall.sh — osforge-db memory: OR-FTS recall, temporal filters,
# embedding coverage and visible degradation.
#
# Runs the real osforge-db against a temp database (OSFORGE_DB) and a temp HOME/config.
# The embedder is `off`, `mock` (deterministic, offline) or `ollama` pointed at a dead
# port (OSFORGE_OLLAMA_URL) — never the real Ollama, never the network. Verifies:
#   1. a natural question finds its decision (terms OR-ed, stopwords dropped, bm25 order)
#   2. a query made only of short/stop words falls back to its raw terms
#   3. FTS operators and quotes in the query never break the search
#   4. accent-insensitive matching (unicode61 remove_diacritics 2)
#   5. migration of an old FTS index: rebuilt, complete, idempotent
#   6. --since/--until on search, search-hybrid (both legs) and list-decisions
#   7. JSON rows of search and search-hybrid: id, project, category, created_at, content
#   8. search-hybrid says when it degraded (stdout note + `degraded` field)
#   9. add-decision embeds when it can and never fails the write when it cannot
#  10. coverage: vec-status and memory-health report embedded/total; embed-backfill fills it
#  11. recall eval floors on the synthetic fixture (FTS only, offline): natural + expanded
# Usage: tests/test-memory-recall.sh
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }

export HOME="$WORK/home"; mkdir -p "$HOME"
export OSFORGE_DB="$WORK/db.sqlite" OSFORGE_CONFIG="$WORK/config.json" OSFORGE_VECTOR=sqlite
export OSFORGE_OLLAMA_URL="http://127.0.0.1:9"      # dead port: "ollama" can never be reached
export OSFORGE_EMBED=off
unset OSFORGE_PROJECT OSFORGE_EMBED_MODEL
db(){ python3 "$REPO/scripts/osforge-db.py" "$@"; }
ids(){ python3 -c 'import json,sys; print(" ".join(str(r["id"]) for r in json.loads(sys.stdin.read() or "[]")))'; }
sql(){ python3 -c 'import sqlite3,sys; r=sqlite3.connect(sys.argv[1]).execute(sys.argv[2]).fetchone(); print(r[0] if r else "")' "$OSFORGE_DB" "$1"; }
add(){ # add <slug> <created_at> <category> <content> → prints the new id
  db add-decision "$1" "$4" --category="$3" >/dev/null 2>&1
  local id; id="$(sql 'select max(id) from decisions')"
  python3 -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); c.execute("update decisions set created_at=? where id=?", (sys.argv[2], int(sys.argv[3]))); c.commit()' "$OSFORGE_DB" "$2" "$id"
  echo "$id"
}

section "Fixture"
db init >/dev/null 2>&1
db upsert-project shop "loja" >/dev/null 2>&1
db upsert-project api "api" >/dev/null 2>&1
D_PAG="$(add shop "2026-08-04 10:00:00" data 'Paginação por cursor na listagem de produtos: 24 itens por página.')"
D_FUN="$(add shop "2026-08-19 09:15:00" arch 'Funções de perfil devolvem Result em vez de null para distinguir falha de rede.')"
D_UI="$(add shop "2026-09-02 16:00:00" ux 'UI kit: botões primários usam o token brand-600.')"
D_TEN="$(add api "2026-09-10 12:00:00" security 'Isolamento multi-tenant via RLS por organização no Postgres.')"
D_C9="$(add shop "2026-09-15 11:20:00" data 'Cache do catálogo no Redis com TTL de 10 minutos.')"
D_C10="$(add shop "2026-10-06 08:45:00" data 'Catalog cache moved from Redis to the Next.js data cache.')"
check "fixture has 6 decisions" '[ "$(sql "select count(*) from decisions")" = 6 ]'

section "1. Natural question (OR, stopwords, bm25)"
R="$(db --json search 'quantos itens por página na listagem de produtos?' 2>/dev/null | ids)"
check "pt-BR question ranks the pagination decision #1" '[ "${R%% *}" = "$D_PAG" ]'
R="$(db --json search 'how is the catalog cache configured now?' 2>/dev/null | ids)"
check "en question ranks the (en) cache decision #1" '[ "${R%% *}" = "$D_C10" ]'
R="$(db --json search-hybrid 'por que as funções de perfil devolvem um resultado?' 2>/dev/null | ids)"
check "search-hybrid FTS leg uses the same query building" '[ "${R%% *}" = "$D_FUN" ]'

section "2. Fallback to raw terms"
R="$(db --json search 'UI' 2>/dev/null | ids)"
check "'UI' (short) falls back to the raw term and finds the decision" '[ "$R" = "$D_UI" ]'

section "3. FTS operators and quotes never break the query"
for q in 'multi-tenant' 'NOT AND OR' '"aspas" soltas"' 'col:valor ^início *' '???' 'NEAR(a b)'; do
  OUT="$(db --json search "$q" 2>"$WORK/err")"; RC=$?
  check "search \"$q\" → exit 0, valid JSON" '[ $RC -eq 0 ] && python3 -c "import json,sys; json.loads(sys.argv[1])" "$OUT" && ! grep -qi "fts5\|syntax" "$WORK/err"'
done
R="$(db --json search 'multi-tenant' 2>/dev/null | ids)"
check "'multi-tenant' finds the multi-tenant decision" '[ "${R%% *}" = "$D_TEN" ]'

section "4. Accent-insensitive matching"
R="$(db --json search 'funcoes de perfil' 2>/dev/null | ids)"
check "'funcoes' matches 'Funções'" '[ "${R%% *}" = "$D_FUN" ]'
R="$(db --json search 'paginacao' 2>/dev/null | ids)"
check "'paginacao' matches 'Paginação'" '[ "$R" = "$D_PAG" ]'
check "decisions_fts uses remove_diacritics 2" '[ -n "$(sql "select 1 from sqlite_master where name=\"decisions_fts\" and sql like \"%remove_diacritics 2%\"")" ]'

section "5. Migration of an old FTS index"
OLD="$WORK/old.sqlite"
python3 - "$OLD" <<'EOF'
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
c.executescript("""
CREATE TABLE projects (id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL DEFAULT '', triage TEXT NOT NULL DEFAULT 'standard',
  status TEXT NOT NULL DEFAULT 'active', stack_json TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now','utc')), updated_at TEXT NOT NULL DEFAULT (datetime('now','utc')));
CREATE TABLE decisions (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER NOT NULL REFERENCES projects(id),
  content TEXT NOT NULL, category TEXT NOT NULL DEFAULT 'arch', created_at TEXT NOT NULL DEFAULT (datetime('now','utc')));
CREATE VIRTUAL TABLE decisions_fts USING fts5(content, project_slug, category, content='decisions', content_rowid='id');
CREATE TRIGGER decisions_ai AFTER INSERT ON decisions BEGIN
  INSERT INTO decisions_fts(rowid, content, project_slug, category)
  VALUES (new.id, new.content, (SELECT slug FROM projects WHERE id = new.project_id), new.category);
END;
INSERT INTO projects(slug) VALUES ('legacy');
INSERT INTO decisions(project_id, content, category) VALUES (1, 'Decisão antiga sobre migração de índice', 'data');
INSERT INTO decisions(project_id, content, category) VALUES (1, 'Outra decisão: usar autenticação por sessão', 'security');
""")
c.commit()
EOF
O1="$(OSFORGE_DB="$OLD" db --json search 'migracao indice' 2>/dev/null | ids)"
check "old DB migrated: accent-free query finds the old decision" '[ "$O1" = 1 ]'
TOK="$(OSFORGE_DB="$OLD" python3 -c 'import sqlite3,os; print(sqlite3.connect(os.environ["OSFORGE_DB"]).execute("select sql from sqlite_master where name=\"decisions_fts\"").fetchone()[0])')"
check "old DB tokenizer now has remove_diacritics 2" 'grep -q "remove_diacritics 2" <<<"$TOK"'
NF="$(OSFORGE_DB="$OLD" python3 -c 'import sqlite3,os; print(sqlite3.connect(os.environ["OSFORGE_DB"]).execute("select count(*) from decisions_fts where decisions_fts match \"legacy\"").fetchone()[0])')"
check "index rebuilt complete (2 rows, project_slug included)" '[ "$NF" = 2 ]'
OSFORGE_DB="$OLD" db stats >/dev/null 2>&1
TOK2="$(OSFORGE_DB="$OLD" python3 -c 'import sqlite3,os; print(sqlite3.connect(os.environ["OSFORGE_DB"]).execute("select sql from sqlite_master where name=\"decisions_fts\"").fetchone()[0])')"
NF2="$(OSFORGE_DB="$OLD" python3 -c 'import sqlite3,os; print(sqlite3.connect(os.environ["OSFORGE_DB"]).execute("select count(*) from decisions_fts where decisions_fts match \"legacy\"").fetchone()[0])')"
check "migration is idempotent (same schema and count on a second run)" '[ "$TOK" = "$TOK2" ] && [ "$NF2" = 2 ]'
OSFORGE_DB="$OLD" db add-decision legacy "decisão nova pós-migração" >/dev/null 2>&1
O2="$(OSFORGE_DB="$OLD" db --json search 'pos-migracao' 2>/dev/null | ids)"
check "insert trigger keeps feeding the new index" 'grep -qw 3 <<<"$O2"'

section "6. --since / --until"
R="$(db --json search 'cache catálogo catalog' --since=2026-10-01 2>/dev/null | ids)"
check "search --since=2026-10-01 → only the October decision" '[ "$R" = "$D_C10" ]'
R="$(db --json search 'cache catálogo catalog' --until=2026-09-30 2>/dev/null | ids)"
check "search --until=2026-09-30 → only September (until is inclusive)" '[ "$R" = "$D_C9" ]'
R="$(db --json search 'cache catálogo catalog' --since=2026-09-15 --until=2026-09-15 2>/dev/null | ids)"
check "search --since = --until = same day → that day's decision" '[ "$R" = "$D_C9" ]'
# decisions above were added with embed=off; embed them (mock) for the vector leg
OSFORGE_EMBED=mock db embed-backfill >/dev/null 2>&1
R="$(OSFORGE_EMBED=mock db --json search-hybrid 'cache catálogo catalog' --since=2026-10-01 --top=10 2>/dev/null | ids)"
check "search-hybrid --since with vector leg on → nothing before October" '[ "$R" = "$D_C10" ]'
R="$(OSFORGE_EMBED=mock db --json search-hybrid 'Redis' --until=2026-09-30 --top=10 2>/dev/null)"
# mock vectors score every decision, so the vector leg brings all of them: none may be after --until
check "search-hybrid --until filters the vector leg too" 'python3 -c "import json,sys; r=json.loads(sys.argv[1]); assert r and all(x[\"created_at\"] < \"2026-10-01\" for x in r); assert $D_C9 in [x[\"id\"] for x in r]" "$R"'
R="$(db --json list-decisions shop --since=2026-09-01 --until=2026-09-30 --limit=50 2>/dev/null | ids)"
check "list-decisions --since/--until → only the project's September" '[ "$(tr " " "\n" <<<"$R" | sort -n | tr "\n" " ")" = "$D_UI $D_C9 " ]'
db --json search 'cache' --since=10/2026 >/dev/null 2>&1; RC=$?
check "invalid date → error (exit ≠ 0), not a silently ignored filter" '[ $RC -ne 0 ]'

section "7. Complete JSON rows"
keys_ok(){ python3 -c '
import json,sys
rows=json.loads(sys.stdin.read() or "[]"); assert rows, "no rows"
for r in rows:
    for k in ("id","project","category","created_at","content"):
        assert r.get(k) not in (None,""), (k, r)
'; }
check "search --json: id/project/category/created_at/content" 'db --json search "cache" 2>/dev/null | keys_ok'
check "search-hybrid --json (mock): complete fields" 'OSFORGE_EMBED=mock db --json search-hybrid "cache" 2>/dev/null | keys_ok'
check "search-hybrid --json (off): complete fields, project not null" 'db --json search-hybrid "cache" 2>/dev/null | keys_ok'
check "search-hybrid --json (ollama down): complete fields" 'OSFORGE_EMBED=ollama db --json search-hybrid "cache" 2>/dev/null | keys_ok'

section "8. Visible degradation"
deg(){ python3 -c 'import json,sys; rows=json.loads(sys.stdin.read() or "[]"); print(rows[0].get("degraded") if rows else "NO-ROWS")'; }
check "ollama down: JSON marks degraded" '[ "$(OSFORGE_EMBED=ollama db --json search-hybrid "cache" 2>/dev/null | deg)" = "embedder-unreachable" ]'
check "off: normal mode, not a degradation (degraded is null)" '[ "$(db --json search-hybrid "cache" 2>/dev/null | deg)" = "None" ]'
check "mock: degraded is null" '[ "$(OSFORGE_EMBED=mock db --json search-hybrid "cache" 2>/dev/null | deg)" = "None" ]'
OUT="$(OSFORGE_EMBED=ollama db search-hybrid 'cache' 2>/dev/null)"
check "ollama down: normal output (stdout) carries the degradation note" 'grep -qi "degraded" <<<"$OUT" && grep -qi "FTS" <<<"$OUT"'
OUT="$(OSFORGE_EMBED=mock db search-hybrid 'cache' 2>/dev/null)"
check "mock: no degradation note" '! grep -qi "degraded" <<<"$OUT"'
OUT="$(db search-hybrid 'cache' 2>/dev/null)"
check "off: no degradation note, still returns results" '! grep -qi "degraded" <<<"$OUT" && grep -q "#[0-9]" <<<"$OUT"'

section "9. add-decision and embedding"
OSFORGE_EMBED=mock db add-decision api "Decisão com embedding mock" >/dev/null 2>&1; RC=$?
NEW="$(sql 'select max(id) from decisions')"
check "mock provider: add-decision writes and embeds" '[ $RC -eq 0 ] && [ "$(sql "select count(*) from vec_memory where source_table=\"decisions\" and source_id=\"$NEW\"")" = 1 ]'
OSFORGE_EMBED=ollama db add-decision api "Decisão com ollama fora do ar" >"$WORK/out" 2>"$WORK/err"; RC=$?
NEW="$(sql 'select max(id) from decisions')"
check "ollama down: add-decision exits 0 and the decision is written" '[ $RC -eq 0 ] && [ "$(sql "select content from decisions where id=$NEW")" = "Decisão com ollama fora do ar" ]'
check "ollama down: no vector written and the warning points to embed-backfill" '[ "$(sql "select count(*) from vec_memory where source_id=\"$NEW\"")" = 0 ] && grep -q "embed-backfill" "$WORK/err"'

section "10. Coverage"
for n in 1 2 3; do db add-decision api "Decisão sem embedding $n" >/dev/null 2>&1; done   # embed=off → coverage drops below 80%
cov(){ python3 -c 'import json,sys; d=json.loads(sys.stdin.read()); c=d["coverage"]; print(c["embedded"], c["total"])'; }
TOTAL="$(sql 'select count(*) from decisions')"
EMB="$(sql 'select count(distinct source_id) from vec_memory where source_table="decisions" and model="mock-hash-64"')"
check "vec-status --json reports coverage embedded/total" '[ "$(OSFORGE_EMBED=mock db --json vec-status 2>/dev/null | cov)" = "$EMB $TOTAL" ]'
check "vec-status text shows coverage" 'OSFORGE_EMBED=mock db vec-status 2>/dev/null | grep -q "coverage.*$EMB/$TOTAL"'
H="$(OSFORGE_EMBED=mock db memory-health 2>/dev/null)"
check "memory-health: low coverage → hint naming embed-backfill" '[ "$EMB" -lt "$TOTAL" ] && grep -q "embed-backfill" <<<"$H"'
H="$(OSFORGE_EMBED=ollama db memory-health --timeout=0.3 2>/dev/null)"
check "memory-health: embedder down → degraded-search hint" 'grep -qi "unreachable" <<<"$H"'
check "memory-health --json: embedder_reachable=false with ollama down" '[ "$(OSFORGE_EMBED=ollama db --json memory-health --timeout=0.3 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)[\"embedder_reachable\"])")" = False ]'
OSFORGE_EMBED=mock db embed-backfill >/dev/null 2>&1
check "embed-backfill → full coverage" '[ "$(OSFORGE_EMBED=mock db --json vec-status 2>/dev/null | cov)" = "$TOTAL $TOTAL" ]'
check "memory-health: everything embedded → silent" '[ -z "$(OSFORGE_EMBED=mock db memory-health 2>/dev/null)" ]'
check "memory-health: provider off → silent (deliberate choice)" '[ -z "$(db memory-health 2>/dev/null)" ]'
check "memory-health on an empty DB → silent" '[ -z "$(OSFORGE_DB="$WORK/empty.sqlite" OSFORGE_EMBED=ollama db memory-health --timeout=0.3 2>/dev/null)" ]'

section "11. Recall eval (synthetic fixture, FTS, offline)"
EVAL="$(python3 "$REPO/scripts/evals/memory/run.py" --mode=fts --floor=0.8 2>&1)"; RC=$?
echo "     $EVAL" | tail -2
check "eval FTS natural questions: hit@5 ≥ 80% on the fixture" '[ $RC -eq 0 ]'
EVAL="$(python3 "$REPO/scripts/evals/memory/run.py" --mode=fts --set=expanded --floor=0.95 2>&1)"; RC=$?
echo "     $EVAL" | tail -2
check "eval FTS expanded (agent keyword rewrite): hit@5 ≥ 95% on the fixture" '[ $RC -eq 0 ]'
n_nat="$(grep -vc "^#\|^$" "$REPO/scripts/evals/memory/questions.tsv")"; n_exp="$(grep -vc "^#\|^$" "$REPO/scripts/evals/memory/questions-expanded.tsv")"
check "expanded set mirrors the natural set (same count and gold column)" '[ "$n_nat" = "$n_exp" ] && [ "$(grep -v "^#" "$REPO/scripts/evals/memory/questions.tsv" | cut -f1)" = "$(grep -v "^#" "$REPO/scripts/evals/memory/questions-expanded.tsv" | cut -f1)" ]'
check "eval fixture holds no real data (synthetic projects only)" '! grep -vE "^#|^D[0-9]+[[:space:]](acme-shop|nimbus-api|orbit-docs)[[:space:]]" "$REPO/scripts/evals/memory/decisions.tsv" | grep -q .'

echo ""; echo "══ memory-recall: $PASS ok, $FAIL failure(s)"
[ "$FAIL" -eq 0 ]
