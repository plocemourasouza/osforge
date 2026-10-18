#!/usr/bin/env bash
# tests/test-brain.sh — the brain: long-term memory (decisions, knowledge, techniques,
# methodologies) in Qdrant, with ~/.osforge/brain.jsonl as the source of truth.
#
# Runs the real osforge-db against a temp HOME (so ~/.osforge, the journal and the venv are
# all temp), a temp SQLite (OSFORGE_DB) and a temp qdrant LOCAL store (OSFORGE_BRAIN_PATH).
# Never a real server: OSFORGE_QDRANT_URL points at a dead port. Never a real model: the
# embedder is `fake` (deterministic hash dense + sparse, no download).
#
# Part A runs stdlib-only (`python3 -S` hides site-packages, so qdrant-client/fastembed are
# not importable even when installed): journal, scrub, lexical fallback, migrate, forget,
# add-decision best-effort, health, session-resume hint.
# Part B needs a python with qdrant-client: $OSFORGE_TEST_BRAIN_PYTHON, else python3 when it
# imports qdrant_client. Without one, Part B prints SKIP lines and is not counted.
#   1. the CLI and the module import without qdrant-client/fastembed (heavy imports lazy)
#   2. journal is written before the upsert; an unwritable journal means nothing indexed
#   3. secrets are scrubbed before they reach the journal (hooks/lib/scrub.py)
#   4. remember / recall / forget round trip (dense, keyword, hybrid)
#   5. filters (project, kind, global, since, until) applied inside the query / each prefetch
#   6. dense below the threshold → keyword fallback (not a degradation)
#   7. brain migrate imports SQLite decisions once (idempotent via the source key)
#   8. brain rebuild recreates the collection from the journal; forgotten stays forgotten
#   9. store or embedder unavailable → lexical fallback, with a note and `degraded`
#  10. add-decision remembers best-effort: brain failure never fails the write
#  11. brain health: silent when fine or empty, one line when degraded, no model load
#  12. recall eval --mode=brain runs on the fixture with the fake embedder
# Usage: tests/test-brain.sh
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0; SKIP=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }
Q="'"                                                   # a literal quote inside check strings

export HOME="$WORK/home"; mkdir -p "$HOME"
export OSFORGE_DB="$WORK/db.sqlite" OSFORGE_CONFIG="$WORK/config.json"
export OSFORGE_EMBED=off OSFORGE_VECTOR=sqlite OSFORGE_OLLAMA_URL="http://127.0.0.1:9"
export OSFORGE_QDRANT_URL="http://127.0.0.1:9"          # dead port: no real Qdrant, ever
export OSFORGE_BRAIN_STORE=local OSFORGE_BRAIN_PATH="$WORK/store" OSFORGE_BRAIN_EMBED=fake
export OSFORGE_BRAIN_PYTHON="$WORK/no-venv/bin/python"   # Part A: no brain venv at all
unset OSFORGE_PROJECT OSFORGE_BRAIN OSFORGE_BRAIN_MIN_SCORE OSFORGE_BRAIN_MODELS OSFORGE_BRAIN_COLLECTION
JOURNAL="$HOME/.osforge/brain.jsonl"
ODB="$REPO/scripts/osforge-db.py"
sdb(){ python3 -S "$ODB" "$@"; }                         # stdlib only
jq_(){ python3 -c "import json,sys; d=json.loads(sys.stdin.read() or 'null'); print($1)"; }
jlines(){ [ -f "$JOURNAL" ] && grep -c . "$JOURNAL" || echo 0; }
sql(){ python3 -c 'import sqlite3,sys; r=sqlite3.connect(sys.argv[1]).execute(sys.argv[2]).fetchone(); print(r[0] if r else "")' "$OSFORGE_DB" "$1"; }

section "A1. Importable without deps"
check "osforge_brain imports stdlib-only, nothing heavy loaded" 'python3 -S -c "import sys; sys.path.insert(0, \"$REPO/scripts\"); import osforge_brain; assert not any(m.split(\".\")[0] in (\"qdrant_client\",\"fastembed\",\"onnxruntime\",\"numpy\") for m in sys.modules)"'
check "osforge-db help still works stdlib-only" 'sdb 2>/dev/null | grep -q "recall"'

section "A2. Journal + degraded remember (no venv)"
OUT="$(sdb remember 'Paginação por cursor na listagem de produtos: 24 itens por página.' --kind=decision --project=shop --tags=data,api 2>&1)"; RC=$?
check "remember without venv → exit 0" '[ $RC -eq 0 ]'
check "remember without venv → says brain degraded, journal only" 'grep -q "brain degraded" <<<"$OUT" && grep -qi "journal" <<<"$OUT"'
check "journal holds the record with the full payload" 'python3 -c "import json,sys; r=json.loads(open(sys.argv[1]).readline()); assert r[\"op\"]==\"remember\" and r[\"kind\"]==\"decision\" and r[\"project\"]==\"shop\" and r[\"tags\"]==[\"data\",\"api\"] and r[\"source\"]==\"manual\" and r[\"created_at\"].endswith(\"Z\") and isinstance(r[\"created_ts\"], int) and len(r[\"id\"])==36" "$JOURNAL"'
sdb remember 'Técnica: reproduzir o bug com um teste antes de corrigir.' --kind=technique --global >/dev/null 2>&1
sdb remember 'Methodology: grill the plan one question at a time.' --kind=methodology --project=api >/dev/null 2>&1
check "--global stores project null" 'python3 -c "import json,sys; rs=[json.loads(l) for l in open(sys.argv[1])]; assert [r for r in rs if r[\"kind\"]==\"technique\"][0][\"project\"] is None" "$JOURNAL"'
sdb remember 'x' --kind=opinion >/dev/null 2>&1; RC=$?
check "unknown --kind → exit ≠ 0, nothing journaled" '[ $RC -ne 0 ] && [ "$(jlines)" = 3 ]'
sdb remember 'sem kind' >/dev/null 2>&1; RC=$?
check "missing --kind → exit ≠ 0" '[ $RC -ne 0 ] && [ "$(jlines)" = 3 ]'

section "A3. Scrub before the journal"
SECRET="sk-ant-api03-$(printf 'A%.0s' $(seq 1 40))"
sdb remember "chave do provider: $SECRET usada no staging" --kind=knowledge --project=shop >/dev/null 2>&1
check "secret never reaches the journal" '! grep -q "$SECRET" "$JOURNAL" && grep -q "redacted:key" "$JOURNAL"'

section "A4. Lexical fallback recall (no venv)"
R="$(sdb --json recall 'paginacao da listagem' 2>/dev/null)"
check "accent-insensitive lexical recall finds the decision first" '[ "$(jq_ "d[0][\"content\"][:9]" <<<"$R")" = "Paginação" ]'
check "JSON row: id, kind, project, tags, created_at, score, content" 'jq_ "all(all(k in r for k in (\"id\",\"kind\",\"project\",\"tags\",\"created_at\",\"score\",\"content\")) for r in d) and len(d)>0" <<<"$R" | grep -q True'
check "JSON marks degraded with the reason" '[ "$(jq_ "d[0][\"degraded\"]" <<<"$R")" != "None" ] && jq_ "d[0][\"degraded\"]" <<<"$R" | grep -qi "venv"'
OUT="$(sdb recall 'paginacao da listagem' 2>/dev/null)"
check "text output carries the degraded note" 'grep -q "note: brain degraded (.*) — lexical fallback" <<<"$OUT"'
R="$(sdb --json recall 'teste bug grill plan paginacao' --kind=technique 2>/dev/null)"
check "lexical --kind filter" '[ "$(jq_ "sorted({r[\"kind\"] for r in d})" <<<"$R")" = "[${Q}technique${Q}]" ]'
R="$(sdb --json recall 'teste bug grill plan paginacao' --project=api 2>/dev/null)"
check "lexical --project filter" '[ "$(jq_ "sorted({r[\"project\"] for r in d})" <<<"$R")" = "[${Q}api${Q}]" ]'
sdb --json recall 'cache' --since=10/2026 >/dev/null 2>&1; RC=$?
check "invalid --since → exit ≠ 0" '[ $RC -ne 0 ]'

section "A5. Migrate (stdlib: journal only), idempotent, dates preserved"
sdb init >/dev/null 2>&1
OSFORGE_BRAIN=off sdb upsert-project shop "loja" >/dev/null 2>&1
OSFORGE_BRAIN=off sdb upsert-project api "api" >/dev/null 2>&1
pin(){ python3 -c 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); c.execute("update decisions set created_at=? where id=?", (sys.argv[2], int(sys.argv[3]))); c.commit()' "$OSFORGE_DB" "$1" "$2"; }
B0="$(jlines)"
OSFORGE_BRAIN=off sdb add-decision shop 'Cache do catálogo no Redis com TTL de 10 minutos.' --category=data >/dev/null 2>&1; D1="$(sql 'select max(id) from decisions')"; pin "2026-09-15 11:20:00" "$D1"
OSFORGE_BRAIN=off sdb add-decision shop 'Catalog cache moved from Redis to the Next.js data cache.' --category=data >/dev/null 2>&1; D2="$(sql 'select max(id) from decisions')"; pin "2026-10-06 08:45:00" "$D2"
OSFORGE_BRAIN=off sdb add-decision api 'Isolamento multi-tenant via RLS por organização.' --category=security >/dev/null 2>&1; D3="$(sql 'select max(id) from decisions')"; pin "2026-09-10 12:00:00" "$D3"
check "OSFORGE_BRAIN=off → add-decision leaves the journal alone" '[ "$(jlines)" = "$B0" ]'
OUT="$(sdb brain migrate 2>&1)"; RC=$?
check "migrate (no venv) → exit 0, 3 decisions journaled" '[ $RC -eq 0 ] && [ "$(jlines)" = $((B0+3)) ]'
check "migrate keeps created_at, project, tags=[category], source migrate:sqlite#<id>" 'python3 -c "import json,sys; rs=[json.loads(l) for l in open(sys.argv[1])]; r=[x for x in rs if x.get(\"source\")==\"migrate:sqlite#$D1\"][0]; assert r[\"created_at\"]==\"2026-09-15T11:20:00Z\" and r[\"project\"]==\"shop\" and r[\"tags\"]==[\"data\"] and r[\"kind\"]==\"decision\"" "$JOURNAL"'
sdb brain migrate >/dev/null 2>&1
check "second migrate adds nothing (idempotent)" '[ "$(jlines)" = $((B0+3)) ]'
R="$(sdb --json recall 'cache catálogo catalog Redis' --since=2026-10-01 2>/dev/null)"
check "lexical --since → only the October decision" '[ "$(jq_ "[r[\"source\"] for r in d]" <<<"$R")" = "[${Q}migrate:sqlite#$D2${Q}]" ]'
R="$(sdb --json recall 'cache catálogo catalog Redis' --until=2026-09-30 2>/dev/null)"
check "lexical --until inclusive → only September" '[ "$(jq_ "[r[\"source\"] for r in d]" <<<"$R")" = "[${Q}migrate:sqlite#$D1${Q}]" ]'

section "A6. Forget"
FID="$(jq_ "d[0][\"id\"]" <<<"$(sdb --json recall 'grill plan question' 2>/dev/null)")"
sdb forget "${FID:0:8}" >/dev/null 2>&1; RC=$?
check "forget <id-prefix> → exit 0, tombstone appended" '[ $RC -eq 0 ] && tail -n1 "$JOURNAL" | grep -q "\"op\": *\"forget\""'
R="$(sdb --json recall 'grill plan question' 2>/dev/null)"
check "forgotten memory no longer recalled" '! grep -q "$FID" <<<"$R"'
sdb forget 00000000-dead-beef >/dev/null 2>&1; RC=$?
check "forget unknown id → exit ≠ 0" '[ $RC -ne 0 ]'

section "A7. add-decision best-effort"
OUT="$(sdb add-decision shop 'Decisão gravada sem venv.' 2>&1)"; RC=$?
N="$(sql 'select max(id) from decisions')"
check "no venv: add-decision exit 0, SQLite written, journaled as add-decision:<id>" '[ $RC -eq 0 ] && [ "$(sql "select content from decisions where id=$N")" = "Decisão gravada sem venv." ] && grep -q "\"add-decision:$N\"" "$JOURNAL"'
check "no venv: exactly one brain line in the output" '[ "$(grep -c "brain" <<<"$OUT")" = 1 ]'
mkdir -p "$WORK/broken/bin"; printf '#!/bin/sh\nexit 3\n' > "$WORK/broken/bin/python"; chmod +x "$WORK/broken/bin/python"
OUT="$(OSFORGE_BRAIN_PYTHON="$WORK/broken/bin/python" sdb add-decision shop 'Decisão com venv quebrado.' 2>&1)"; RC=$?
N="$(sql 'select max(id) from decisions')"
check "broken venv: add-decision exit 0 and SQLite written" '[ $RC -eq 0 ] && [ "$(sql "select content from decisions where id=$N")" = "Decisão com venv quebrado." ]'
check "broken venv: journaled first, one brain line naming brain rebuild" 'grep -q "\"add-decision:$N\"" "$JOURNAL" && [ "$(grep -c "brain" <<<"$OUT")" = 1 ] && grep -q "brain rebuild" <<<"$OUT"'
B1="$(jlines)"; sdb brain migrate >/dev/null 2>&1
check "add-decision:<id> and migrate:sqlite#<id> count as the same source" '[ "$(jlines)" = "$B1" ]'
mv "$JOURNAL" "$WORK/journal.bak"; mkdir -p "$JOURNAL"
OUT="$(sdb add-decision shop 'Decisão com o journal travado.' 2>&1)"; RC=$?
N="$(sql 'select max(id) from decisions')"
rmdir "$JOURNAL"; mv "$WORK/journal.bak" "$JOURNAL"
check "journal unwritable: add-decision exit 0, SQLite written, one line naming brain migrate" '[ $RC -eq 0 ] && [ "$(sql "select content from decisions where id=$N")" = "Decisão com o journal travado." ] && [ "$(grep -c "brain" <<<"$OUT")" = 1 ] && grep -q "brain migrate" <<<"$OUT"'
sdb brain migrate >/dev/null 2>&1
check "migrate later picks the missed decision up" 'grep -q "\"migrate:sqlite#$N\"" "$JOURNAL"'

section "A8. Unwritable journal"
mv "$JOURNAL" "$WORK/journal.bak"; mkdir -p "$JOURNAL"
sdb remember 'não pode gravar' --kind=knowledge >/dev/null 2>&1; RC=$?
check "journal not writable → remember fails (exit ≠ 0)" '[ $RC -ne 0 ]'
rmdir "$JOURNAL"; mv "$WORK/journal.bak" "$JOURNAL"

section "A9. brain health (stdlib, no model load)"
T0=$(python3 -c 'import time; print(time.time())')
H="$(sdb brain health --timeout=0.3 2>/dev/null)"
DT=$(python3 -c "import time; print(round(time.time()-$T0, 2))")
check "records + no venv → one 'brain:' line naming the reason" '[ "$(grep -c . <<<"$H")" = 1 ] && grep -q "^brain: degraded (.*venv" <<<"$H"'
check "health is fast (${DT}s < 1.5s)" 'python3 -c "import sys; sys.exit(0 if $DT < 1.5 else 1)"'
check "health --json: ok=false + reason" '[ "$(sdb --json brain health 2>/dev/null | jq_ "(d[\"ok\"], bool(d[\"reason\"]))")" = "(False, True)" ]'
check "empty brain (no journal) → silent" '[ -z "$(HOME="$WORK/empty-home" python3 -S "$ODB" brain health 2>/dev/null)" ]'
check "OSFORGE_BRAIN=off → silent" '[ -z "$(OSFORGE_BRAIN=off sdb brain health 2>/dev/null)" ]'

section "A10. session-resume hint"
mkdir -p "$WORK/proj"; (cd "$WORK/proj" && git init -q . 2>/dev/null)
OSFORGE_BRAIN=off sdb upsert-project proj "p" --root="$WORK/proj" >/dev/null 2>&1
OSFORGE_BRAIN=off sdb set-resume proj "continuar a fase 2" >/dev/null 2>&1
ctx_of(){ python3 -c "import json,sys; print(json.load(sys.stdin)['hookSpecificOutput']['additionalContext'])" 2>/dev/null; }
C="$(cd "$WORK/proj" && echo '{}' | bash "$REPO/hooks/session-resume.sh" | ctx_of)"
check "degraded brain → resume carries exactly one 'brain:' line" 'grep -q "continuar a fase 2" <<<"$C" && [ "$(grep -c "^brain: " <<<"$C")" = 1 ]'
C="$(cd "$WORK/proj" && echo '{}' | OSFORGE_BRAIN=off bash "$REPO/hooks/session-resume.sh" | ctx_of)"
check "brain off → no 'brain:' line" 'grep -q "continuar a fase 2" <<<"$C" && ! grep -q "^brain: " <<<"$C"'

# ── Part B: real qdrant-client (local mode), fake embedder ─────────────────────
BPY="${OSFORGE_TEST_BRAIN_PYTHON:-}"
if [ -z "$BPY" ] && python3 -c "import qdrant_client" 2>/dev/null; then BPY="$(command -v python3)"; fi
if [ -z "$BPY" ] || ! "$BPY" -c "import qdrant_client" 2>/dev/null; then
  echo ""; echo "── B. SKIP: no python with qdrant-client (set OSFORGE_TEST_BRAIN_PYTHON) — store checks not run"
  SKIP=1
else
export OSFORGE_BRAIN_PYTHON="$BPY"
rm -f "$JOURNAL"; rm -rf "$OSFORGE_BRAIN_PATH" "$OSFORGE_DB"*
db(){ python3 "$ODB" "$@"; }                             # re-execs into $OSFORGE_BRAIN_PYTHON
status(){ db --json brain status 2>/dev/null | jq_ "$1"; }

section "B1. remember → journal + index"
OUT="$(db --json remember 'Paginação por cursor na listagem de produtos: 24 itens por página.' --kind=decision --project=shop --tags=data 2>/dev/null)"; RC=$?
P1="$(jq_ "d[\"id\"]" <<<"$OUT")"
check "remember (fake embedder) → exit 0, indexed, not degraded" '[ $RC -eq 0 ] && [ "$(jq_ "(d[\"indexed\"], d[\"degraded\"])" <<<"$OUT")" = "(True, None)" ]'
check "brain status: 1 journal record, 1 point, store=local" '[ "$(status "(d[\"journal_live\"], d[\"points\"], d[\"store\"])")" = "(1, 1, ${Q}local${Q})" ]'
db remember 'Funções de perfil devolvem Result em vez de null para distinguir falha de rede.' --kind=decision --project=shop >/dev/null 2>&1
db remember 'Isolamento multi-tenant via RLS por organização no Postgres.' --kind=decision --project=api >/dev/null 2>&1
db remember 'Técnica: reproduzir o bug com um teste que falha antes de corrigir.' --kind=technique --global >/dev/null 2>&1
db remember 'Methodology: grill the plan one question at a time before building.' --kind=methodology --project=api >/dev/null 2>&1
db remember 'Knowledge: Postgres partial indexes speed up soft-delete filters.' --kind=knowledge --project=shop >/dev/null 2>&1
check "6 remembered → 6 points" '[ "$(status "d[\"points\"]")" = 6 ]'

section "B2. Journal before upsert"
mv "$JOURNAL" "$WORK/journal.bak"; mkdir -p "$JOURNAL"
db remember 'nunca indexado' --kind=knowledge >/dev/null 2>&1; RC=$?
rmdir "$JOURNAL"; mv "$WORK/journal.bak" "$JOURNAL"
check "journal not writable → exit ≠ 0 and nothing indexed" '[ $RC -ne 0 ] && [ "$(status "d[\"points\"]")" = 6 ]'
OUT="$(OSFORGE_BRAIN_STORE=server db remember 'Memória gravada com o store fora do ar.' --kind=knowledge --project=shop 2>&1)"; RC=$?
check "store down → exit 0, journaled, note says degraded" '[ $RC -eq 0 ] && grep -q "Memória gravada com o store fora do ar" "$JOURNAL" && grep -q "brain degraded" <<<"$OUT"'
check "store down → the point is not in the local store (journal ahead)" '[ "$(status "(d[\"journal_live\"], d[\"points\"])")" = "(7, 6)" ]'
SECRET="ghp_$(printf 'b%.0s' $(seq 1 36))"
db remember "token de deploy $SECRET no CI" --kind=knowledge --project=shop >/dev/null 2>&1
check "scrub with the store on: secret neither in the journal nor recalled" '! grep -q "$SECRET" "$JOURNAL" && ! db --json recall "token deploy CI" 2>/dev/null | grep -q "$SECRET"'

section "B3. Recall round trip"
R="$(db --json recall 'quantos itens por página na listagem de produtos?' 2>/dev/null)"
check "dense recall: the pagination memory first" '[ "$(jq_ "d[0][\"id\"]" <<<"$R")" = "$P1" ]'
check "dense recall: mode=dense, degraded=null, numeric score" '[ "$(jq_ "(d[0][\"mode\"], d[0][\"degraded\"], isinstance(d[0][\"score\"], float))" <<<"$R")" = "(${Q}dense${Q}, None, True)" ]'
R="$(db --json recall 'listagem produtos página' --mode=keyword 2>/dev/null)"
check "--mode=keyword: bm25 sparse finds it, mode=keyword" '[ "$(jq_ "(d[0][\"id\"], d[0][\"mode\"])" <<<"$R")" = "(${Q}$P1${Q}, ${Q}keyword${Q})" ]'
R="$(OSFORGE_BRAIN_MIN_SCORE=1.01 db --json recall 'listagem produtos página' 2>/dev/null)"
check "dense below threshold → keyword fallback, not degraded" '[ "$(jq_ "(d[0][\"id\"], d[0][\"mode\"], d[0][\"degraded\"])" <<<"$R")" = "(${Q}$P1${Q}, ${Q}keyword${Q}, None)" ]'
OUT="$(db recall 'quantos itens por página?' 2>/dev/null)"
check "text output: short id, kind, project; no degraded note" 'grep -q "#${P1:0:8} \[decision\] shop" <<<"$OUT" && ! grep -q "degraded" <<<"$OUT"'
R="$(db --json recall 'listagem' --top=2 2>/dev/null)"
check "--top=2 → at most 2 rows" '[ "$(jq_ "len(d)" <<<"$R")" -le 2 ]'

section "B4. Filters inside the query / prefetch"
QRY='Postgres teste plan página falha organização'
for m in dense keyword hybrid; do
  R="$(db --json recall "$QRY" --mode=$m --project=api --top=10 2>/dev/null)"
  check "--mode=$m --project=api → only api rows" '[ "$(jq_ "sorted({r[\"project\"] for r in d})" <<<"$R")" = "[${Q}api${Q}]" ]'
  R="$(db --json recall "$QRY" --mode=$m --kind=technique --top=10 2>/dev/null)"
  check "--mode=$m --kind=technique → only the technique" '[ "$(jq_ "[r[\"kind\"] for r in d]" <<<"$R")" = "[${Q}technique${Q}]" ]'
done
R="$(db --json recall "$QRY" --global --top=10 2>/dev/null)"
check "--global → only project-less memories" '[ "$(jq_ "sorted({str(r[\"project\"]) for r in d})" <<<"$R")" = "[${Q}None${Q}]" ]'
db init >/dev/null 2>&1
OSFORGE_BRAIN=off db upsert-project shop "loja" >/dev/null 2>&1
OSFORGE_BRAIN=off db add-decision shop 'Cache do catálogo no Redis com TTL de 10 minutos.' --category=data >/dev/null 2>&1; D1="$(sql 'select max(id) from decisions')"; pin "2026-09-15 11:20:00" "$D1"
OSFORGE_BRAIN=off db add-decision shop 'Catalog cache moved from Redis to the Next.js data cache.' --category=data >/dev/null 2>&1; D2="$(sql 'select max(id) from decisions')"; pin "2026-10-06 08:45:00" "$D2"
srcs(){ jq_ "sorted(r[\"source\"] for r in d)"; }

section "B5. Migrate into the store"
PT0="$(status "d[\"points\"]")"
OUT="$(db brain migrate 2>&1)"; RC=$?
check "migrate → exit 0, 2 decisions indexed" '[ $RC -eq 0 ] && [ "$(status "d[\"points\"]")" = $((PT0+2)) ]'
JL="$(jlines)"; db brain migrate >/dev/null 2>&1
check "second migrate: no new journal line, no new point" '[ "$(jlines)" = "$JL" ] && [ "$(status "d[\"points\"]")" = $((PT0+2)) ]'
for m in dense keyword hybrid; do
  R="$(db --json recall 'cache catálogo catalog Redis' --mode=$m --since=2026-10-01 --top=10 2>/dev/null)"
  check "--mode=$m --since=2026-10-01 → only the October decision" '[ "$(srcs <<<"$R")" = "[${Q}migrate:sqlite#$D2${Q}]" ]'
  R="$(db --json recall 'cache catálogo catalog Redis' --mode=$m --since=2026-09-15 --until=2026-09-15 --top=10 2>/dev/null)"
  check "--mode=$m --since=--until=2026-09-15 → that day's decision" '[ "$(srcs <<<"$R")" = "[${Q}migrate:sqlite#$D1${Q}]" ]'
done

section "B6. add-decision with the brain on"
OUT="$(db add-decision shop 'Webhooks do gateway com retry exponencial e fila de mensagens mortas.' --category=arch 2>&1)"; RC=$?
N="$(sql 'select max(id) from decisions')"
R="$(db --json recall 'webhook retry fila mensagens mortas' 2>/dev/null)"
check "add-decision → exit 0, recalled as kind=decision source add-decision:<id>" '[ $RC -eq 0 ] && [ "$(jq_ "(d[0][\"kind\"], d[0][\"source\"], d[0][\"project\"], d[0][\"tags\"])" <<<"$R")" = "(${Q}decision${Q}, ${Q}add-decision:$N${Q}, ${Q}shop${Q}, [${Q}arch${Q}])" ]'

section "B7. Forget"
FID="$(jq_ "d[0][\"id\"]" <<<"$(db --json recall 'grill the plan one question' 2>/dev/null)")"
PT="$(status "d[\"points\"]")"
db forget "$FID" >/dev/null 2>&1; RC=$?
check "forget → exit 0, point deleted" '[ $RC -eq 0 ] && [ "$(status "d[\"points\"]")" = $((PT-1)) ]'
check "forgotten id never recalled (dense or keyword)" '! db --json recall "grill the plan one question" --top=20 2>/dev/null | grep -q "$FID" && ! db --json recall "grill plan question" --mode=keyword --top=20 2>/dev/null | grep -q "$FID"'

section "B8. Rebuild from the journal"
LIVE="$(status "d[\"journal_live\"]")"
rm -rf "$OSFORGE_BRAIN_PATH"
OUT="$(db brain rebuild 2>&1)"; RC=$?
check "rebuild → exit 0, points = live journal records (incl. the one journaled while down)" '[ $RC -eq 0 ] && [ "$(status "(d[\"points\"], d[\"journal_live\"])")" = "($LIVE, $LIVE)" ]'
check "rebuild never resurrects a forgotten memory" '! db --json recall "grill the plan one question" --top=20 2>/dev/null | grep -q "$FID"'
R="$(db --json recall 'quantos itens por página na listagem de produtos?' 2>/dev/null)"
check "recall after rebuild still finds the pagination memory first" '[ "$(jq_ "d[0][\"id\"]" <<<"$R")" = "$P1" ]'

section "B9. Degraded: store or embedder unavailable"
R="$(OSFORGE_BRAIN_STORE=server db --json recall 'listagem produtos página' 2>/dev/null)"; RC=$?
check "server down → exit 0, lexical rows with degraded reason" '[ $RC -eq 0 ] && [ "$(jq_ "(d[0][\"id\"], d[0][\"mode\"], bool(d[0][\"degraded\"]))" <<<"$R")" = "(${Q}$P1${Q}, ${Q}lexical${Q}, True)" ]'
OUT="$(OSFORGE_BRAIN_STORE=server db recall 'listagem produtos página' 2>/dev/null)"
check "server down → text note 'brain degraded (…) — lexical fallback'" 'grep -q "note: brain degraded (.*) — lexical fallback" <<<"$OUT"'
R="$(OSFORGE_BRAIN_EMBED=gemma OSFORGE_BRAIN_MODELS="$WORK/no-models" db --json recall 'listagem produtos página' 2>/dev/null)"
check "embedder unavailable (no model) → lexical fallback, degraded" '[ "$(jq_ "(d[0][\"mode\"], bool(d[0][\"degraded\"]))" <<<"$R")" = "(${Q}lexical${Q}, True)" ]'
check "health with venv + local store + nothing pending → silent" '[ -z "$(db brain health 2>/dev/null)" ]'

section "B10. Recall eval --mode=brain (fixture, fake embedder)"
EVAL="$(OSFORGE_BRAIN_PYTHON="$BPY" python3 "$REPO/scripts/evals/memory/run.py" --mode=brain 2>&1)"; RC=$?
echo "     $(tail -1 <<<"$EVAL")"
check "eval --mode=brain runs on a temp store and reports hit@1/hit@5" '[ $RC -eq 0 ] && grep -q "mode=brain .*hit@1=.*hit@5=" <<<"$EVAL"'
fi

echo ""; echo "══ brain: $PASS ok, $FAIL failure(s)$([ "$SKIP" = 1 ] && echo ", part B skipped")"
[ "$FAIL" -eq 0 ]
