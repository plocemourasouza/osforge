#!/usr/bin/env bash
# tests/test-monitor.sh — B-036 (SPEC-P05 rev. 3): the read-only monitor contract.
#
# Real osforge-db on a temporary database, temporary HOME, TZ=UTC so days are deterministic.
# Every number is checked against a hand count of what was seeded. No network.
#   1. portfolio: grouping by lifecycle status, archived out without --all, legacy status → outro
#   2. project: % per phase and overall, counts per status, open dependencies, blocker age,
#      agent minutes with the 5-min cap, sessions, cost from pricing.json, orchestrator/subagent
#   3. empty project → empty blocks; unknown slug → exit 2; --days out of range → exit 2
#   4. --discover: unregistered folder listed, registered project without root gets a
#      suggested root, malformed/old transcripts ignored, database untouched
#   5. quality block: open signals, tests state, shortcut ledger from git grep
#   6. --compact for the band
#   7. budget on 50,000 calls (median of 5): band --compact < 200 ms (runs every turn);
#      project < 400 ms and portfolio < 600 ms (the panel fetches them in the background)
#   8. read-only: the database file is byte-identical after every monitor call
#   9. Canvas: /monitor loads nothing external and never writes data as HTML; /api/monitor
#      validates slug/days/Origin and maps unknown project to 404 (needs bun, else skipped)
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }

export TZ=UTC HOME="$WORK/home"; mkdir -p "$HOME"
export OSFORGE_DB="$WORK/db.sqlite" OSFORGE_QUOTA_FILE="$WORK/quota.json" OSFORGE_PRICING="$REPO/claude-code/pricing.json"
unset OSFORGE_PROJECT OSFORGE_TRANSCRIPTS_DIR
db(){ python3 "$REPO/scripts/osforge-db.py" "$@"; }
GIT="git -c user.name=t -c user.email=t@t -c init.defaultBranch=main -c commit.gpgsign=false"
J="$WORK/out.json"
q(){ python3 -c "import json,sys; d=json.load(open('$J')); print($1)"; }   # expression over d

# ── seed ────────────────────────────────────────────────────────────────────────────────────
A="$WORK/alpha"; mkdir -p "$A/lib"
printf 'export const cache = new Map(); // shortcut: in-memory cache, replace when >1 instance\n' > "$A/lib/cache.ts"
printf '# shortcut: no retry\nx = 1\n' > "$A/lib/job.py"
(cd "$A" && $GIT init -q && $GIT add -A && $GIT commit -qm init)
db upsert-project alpha "Loja" standard active --root="$A" >/dev/null 2>&1
db upsert-project beta "Backlog" standard backlog >/dev/null 2>&1
db upsert-project gamma "Arquivado" standard archived >/dev/null 2>&1
db upsert-project empty "Vazio" standard paused >/dev/null 2>&1
db set-phase alpha "F1" complete >/dev/null 2>&1
db set-phase alpha "F2" in-progress >/dev/null 2>&1
db add-task alpha "t1" --phase=F1 >/dev/null 2>&1      # 1 done
db add-task alpha "t2" --phase=F1 >/dev/null 2>&1      # 2 done
db add-task alpha "t3" --phase=F1 >/dev/null 2>&1      # 3 pending
db add-task alpha "t4" --phase=F2 >/dev/null 2>&1      # 4 blocked
db add-task alpha "t5" --phase=F2 --depends=1,4 --priority=p0 >/dev/null 2>&1   # 5 in-progress
db add-task alpha "t6" --phase=F2 >/dev/null 2>&1      # 6 cancelled
for x in "1 done" "2 done" "4 blocked" "5 in-progress" "6 cancelled"; do set -- $x; db set-task alpha "$1" "$2" >/dev/null 2>&1; done
db add-blocker alpha "aguardando chave do Pix" --waiting=cliente >/dev/null 2>&1
db add-decision alpha "Usar Server Actions para o checkout" --category=arch >/dev/null 2>&1
db add-signal alpha callers_open formatPrice --detail='{"file":"lib/price.ts","count":2}' >/dev/null 2>&1
db add-signal alpha tests state --detail='{"state":"passed","passed":12}' >/dev/null 2>&1
python3 - "$OSFORGE_DB" <<'EOF'
import sqlite3, sys
from datetime import datetime, timedelta, timezone
c = sqlite3.connect(sys.argv[1])
pid = lambda s: c.execute("SELECT id FROM projects WHERE slug=?", (s,)).fetchone()[0]
now = datetime.now(timezone.utc).replace(microsecond=0)
c.execute("UPDATE blockers SET created_at=?", ((now - timedelta(days=3, hours=1)).strftime("%Y-%m-%d %H:%M:%S"),))
c.execute("UPDATE projects SET status='someday' WHERE slug='empty'")       # legacy value
d2 = (now - timedelta(days=2)).replace(hour=10, minute=0, second=0)
d5 = (now - timedelta(days=5)).replace(hour=9, minute=0, second=0)
iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
rows = [  # message_id, project, session, ts, model, input, output, cache_read, w5m, w1h, sidechain
    ("m1", "alpha", "s1", d2, "claude-sonnet-4-6", 1000, 500, 10000, 0, 0, 0),
    ("m2", "alpha", "s1", d2 + timedelta(seconds=60), "claude-sonnet-4-6", 2000, 100, 0, 400, 0, 0),
    ("m3", "alpha", "s1", d2 + timedelta(seconds=460), "claude-sonnet-4-6", 0, 100, 0, 0, 0, 1),  # gap 400 s -> 300
    ("m4", "alpha", "s2", d5, "claude-haiku-4-5", 300, 30, 0, 0, 0, 1),
    ("m5", None,    "s3", d2, "claude-sonnet-4-6", 10, 10, 0, 0, 0, 0),
    ("m6", "alpha", "s9", now - timedelta(days=200), "claude-sonnet-4-6", 9, 9, 0, 0, 0, 0),  # outside horizon
]
for m, p, s, ts, model, i, o, cr, w5, w1, sc in rows:
    c.execute("INSERT INTO calls (message_id, project_id, session_id, ts, model, input, output, cache_read, "
              "cache_write_5m, cache_write_1h, sidechain) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
              (m, pid(p) if p else None, s, iso(ts), model, i, o, cr, w5, w1, sc))
c.commit()
EOF
printf '{"schema":"osforge.quota.v1","at":%s,"source":"statusline","five_hour":{"pct":63.0,"resets_at":%s}}' "$(date +%s)" "$(( $(date +%s) + 3600 ))" > "$OSFORGE_QUOTA_FILE"
SHA0="$(python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$OSFORGE_DB")"

# expected cost of alpha in the 30-day period, from pricing.json by hand
EXP_COST="$(python3 - "$OSFORGE_PRICING" <<'EOF'
import json, sys
m = json.load(open(sys.argv[1]))["models"]
def price(model):
    best = max((k for k in m if model.startswith(k)), key=len)
    return m[best]
def cost(model, i, o, cr, w5, w1):
    p = price(model)
    return (i * p["input"] + o * p["output"] + cr * p["cache_read"] + w5 * p["cache_write_5m"] + w1 * p.get("cache_write_1h", 0)) / 1e6
print(round(cost("claude-sonnet-4-6", 1000, 500, 10000, 0, 0) + cost("claude-sonnet-4-6", 2000, 100, 0, 400, 0)
            + cost("claude-sonnet-4-6", 0, 100, 0, 0, 0) + cost("claude-haiku-4-5", 300, 30, 0, 0, 0), 4))
EOF
)"

section "1. portfolio"
db monitor > "$J"; RC=$?
check "exit 0, schema v1" "[ $RC -eq 0 ] && [ \"\$(q 'd[\"schema\"]')\" = osforge.monitor.v1 ]"
check "archived project listed (history library)" "[ \"\$(q 'sorted(p[\"slug\"] for p in d[\"projetos\"])')\" = \"['alpha', 'beta', 'empty', 'gamma']\" ]"
check "groups: active+recent → andamento, backlog, archived → historico; listed in group order" "[ \"\$(q '[(p[\"slug\"], p[\"grupo_base\"]) for p in d[\"projetos\"]]')\" = \"[('alpha', 'andamento'), ('empty', 'andamento'), ('beta', 'backlog'), ('gamma', 'historico')]\" ]"
check "legacy status kept raw, shown as outro" "[ \"\$(q '[p[\"status_bruto\"] for p in d[\"projetos\"] if p[\"slug\"]==\"empty\"][0]')\" = someday ]"
check "totals: open tasks 3, blockers 1, signals 1 (tests excluded)" "[ \"\$(q '(d[\"totais\"][\"tarefas_abertas\"], d[\"totais\"][\"bloqueios_abertos\"], d[\"totais\"][\"sinais_abertos\"])')\" = '(3, 1, 1)' ]"
check "period: 5 calls (one outside the horizon), 3 sessions" "[ \"\$(q '(d[\"totais\"][\"chamadas\"], d[\"totais\"][\"sessoes\"])')\" = '(5, 3)' ]"
check "health: 1 of 5 calls without project = 20.0%" "[ \"\$(q 'd[\"saude\"][\"chamadas_sem_projeto_pct\"]')\" = 20.0 ]"
check "open blockers across projects, with project and age" "[ \"\$(q '[(b[\"projeto\"], b[\"idade_dias\"]) for b in d[\"bloqueios\"]]')\" = \"[('alpha', 3)]\" ]"
check "health: projects without a root" "[ \"\$(q 'sorted(d[\"saude\"][\"projetos_sem_raiz\"])')\" = \"['beta', 'empty', 'gamma']\" ]"
check "window from quota.json" "[ \"\$(q 'd[\"janela\"][\"five_hour\"][\"pct\"]')\" = 63.0 ]"
check "series covers the 84-day horizon" "[ \"\$(q 'len(d[\"projetos\"][0][\"serie\"])')\" = 84 ]"
check "alpha: pct = 2 done / 5 live = 40.0" "[ \"\$(q 'd[\"projetos\"][0][\"pct\"]')\" = 40.0 ]"
check "alpha: cost matches the hand count" "[ \"\$(q 'd[\"projetos\"][0][\"periodo\"][\"custo\"]')\" = \"$EXP_COST\" ]"
check "alpha: tokens = input+output+writes (cache reads apart)" "[ \"\$(q 'd[\"projetos\"][0][\"periodo\"][\"tokens\"]')\" = $((1000+500+2000+100+400+100+300+30)) ]"
check "alpha: agent minutes = (60 s + capped 300 s) / 60 = 6.0" "[ \"\$(q 'd[\"projetos\"][0][\"periodo\"][\"minutos\"]')\" = 6.0 ]"
check "alpha: has a root on disk" "[ \"\$(q 'd[\"projetos\"][0][\"acesso\"][\"raiz_existe\"]')\" = True ]"
db monitor --all > "$J"
check "--all still accepted" "[ \"\$(q 'len(d[\"projetos\"])')\" = 4 ]"
db monitor --days=7 > "$J"
check "--days=7: s2 (5 days ago) in, horizon still 84" "[ \"\$(q '(d[\"totais\"][\"chamadas\"], d[\"horizonte_dias\"])')\" = '(5, 84)' ]"
db monitor --days=90 > "$J"
check "--days=90: horizon 180 for the previous-period delta" "[ \"\$(q 'd[\"horizonte_dias\"]')\" = 180 ]"

section "2. project detail"
db monitor alpha > "$J"
check "phases: F1 2/3 = 66.7, F2 0/2 = 0.0 (cancelled out)" "[ \"\$(q '[(f[\"nome\"], f[\"feitas\"], f[\"total\"], f[\"pct\"]) for f in d[\"projeto\"][\"fases_detalhe\"]]')\" = \"[('F1', 2, 3, 66.7), ('F2', 0, 2, 0.0)]\" ]"
check "counts per status" "[ \"\$(q 'd[\"projeto\"][\"tarefas\"]')\" = \"{'pending': 1, 'in_progress': 1, 'blocked': 1, 'done': 2, 'cancelled': 1}\" ]"
check "open dependencies: t5 waits on 4, not on done 1" "[ \"\$(q '[t[\"dependencias_abertas\"] for t in d[\"projeto\"][\"tarefas_abertas_lista\"] if t[\"id\"]==5][0]')\" = \"['4']\" ]"
check "p0 first in the open list" "[ \"\$(q 'd[\"projeto\"][\"tarefas_abertas_lista\"][0][\"id\"]')\" = 5 ]"
check "blocker age 3 days" "[ \"\$(q 'd[\"projeto\"][\"bloqueios\"][0][\"idade_dias\"]')\" = 3 ]"
check "decisions listed" "[ \"\$(q 'len(d[\"projeto\"][\"decisoes\"])')\" = 1 ]"
check "sessions: s1 then s2, s1 = 3 calls, 6.0 min, main model sonnet" "[ \"\$(q '[(s[\"sessao\"], s[\"chamadas\"], s[\"minutos\"], s[\"modelo\"]) for s in d[\"projeto\"][\"sessoes\"]]')\" = \"[('s1', 3, 6.0, 'claude-sonnet-4-6'), ('s2', 1, 0.0, 'claude-haiku-4-5')]\" ]"
check "orchestrator 2 calls, subagent 2 calls" "[ \"\$(q '(d[\"projeto\"][\"consumo\"][\"orquestrador_subagente\"][\"orquestrador\"][\"chamadas\"], d[\"projeto\"][\"consumo\"][\"orquestrador_subagente\"][\"subagente\"][\"chamadas\"])')\" = '(2, 2)' ]"
check "per day and model: 2 rows" "[ \"\$(q 'len(d[\"projeto\"][\"consumo\"][\"por_dia_modelo\"])')\" = 2 ]"
check "activity: 84 days, 6.0 minutes in total" "[ \"\$(q '(len(d[\"projeto\"][\"atividade\"]), sum(x[\"minutos\"] for x in d[\"projeto\"][\"atividade\"]))')\" = '(84, 6.0)' ]"

section "3. empty / unknown / bad flags"
db monitor beta > "$J"; RC=$?
check "project without tasks → empty blocks, exit 0" "[ $RC -eq 0 ] && [ \"\$(q '(d[\"projeto\"][\"pct\"], d[\"projeto\"][\"tarefas_abertas_lista\"], d[\"projeto\"][\"sessoes\"], d[\"projeto\"][\"qualidade\"][\"atalhos\"])')\" = '(None, [], [], None)' ]"
db monitor nope >/dev/null 2>&1; RC=$?
check "unknown slug → exit 2" "[ $RC -eq 2 ]"
db monitor --days=0 >/dev/null 2>&1; RC=$?
check "--days=0 → exit 2" "[ $RC -eq 2 ]"
db monitor --days=x >/dev/null 2>&1; RC=$?
check "--days=x → exit 2" "[ $RC -eq 2 ]"

section "4. --discover"
T="$HOME/.claude/projects"; mkdir -p "$T/-new" "$T/-beta" "$T/-bad" "$T/-old"
N="$WORK/novo-app"; mkdir -p "$N/src" && (cd "$N" && $GIT init -q && echo x > a && $GIT add a && $GIT commit -qm i)
Bdir="$WORK/beta"; mkdir -p "$Bdir" && (cd "$Bdir" && $GIT init -q && echo x > a && $GIT add a && $GIT commit -qm i)
printf '{"type":"summary"}\n{"type":"user","cwd":"%s/src","sessionId":"x"}\n' "$N" > "$T/-new/1.jsonl"
printf '{"type":"user","cwd":"%s","sessionId":"y"}\n' "$Bdir" > "$T/-beta/1.jsonl"
printf 'not json\n{"cwd": 3}\n' > "$T/-bad/1.jsonl"
O="$WORK/velho"; mkdir -p "$O"
printf '{"type":"user","cwd":"%s"}\n' "$O" > "$T/-old/1.jsonl"
python3 -c "import os,time; t=time.time()-40*86400; os.utime('$T/-old/1.jsonl',(t,t))"
W2="$WORK/we\"ird \$(x)"; mkdir -p "$W2" && (cd "$W2" && $GIT init -q && echo x > a && $GIT add a && $GIT commit -qm i)
mkdir -p "$T/-weird"; python3 -c "import json,sys; print(json.dumps({'type':'user','cwd':sys.argv[1]}))" "$W2" > "$T/-weird/1.jsonl"
db monitor --discover > "$J"
W2REAL="$(cd "$W2" && pwd -P)"; W2NAME="$(basename "$W2")"
check "suggested command survives quotes and \$( ) in the folder name (shlex round-trip)" "python3 -c 'import json,shlex,sys; d=json.load(open(sys.argv[1])); c=[x[\"comando\"] for x in d[\"sem_cadastro\"] if x[\"nome\"].startswith(\"we\")][0]; a=shlex.split(c); assert a[3]==sys.argv[2] and a[-1]==\"--root=\"+sys.argv[3], a' \"\$J\" \"\$W2NAME\" \"\$W2REAL\""
check "unregistered git folder listed by its root, with the command" "[ \"\$(q '[(x[\"nome\"], x[\"git\"], \"upsert-project novo-app\" in x[\"comando\"]) for x in d[\"sem_cadastro\"] if x[\"nome\"]==\"novo-app\"]')\" = \"[('novo-app', True, True)]\" ]"
check "registered project without root → suggested root and bind command" "[ \"\$(q '[p[\"acesso\"].get(\"raiz_sugerida\") for p in d[\"projetos\"] if p[\"slug\"]==\"beta\"][0]')\" = \"$(cd "$Bdir" && pwd -P)\" ]"
check "registered project with a root → no suggestion" "[ \"\$(q '[\"raiz_sugerida\" in p[\"acesso\"] for p in d[\"projetos\"] if p[\"slug\"]==\"alpha\"][0]')\" = False ]"
db monitor > "$J"
check "without --discover → no sem_cadastro block" "[ \"\$(q '\"sem_cadastro\" in d')\" = False ]"

section "5. quality block"
db monitor alpha > "$J"
check "open signal listed (tests apart)" "[ \"\$(q '[(s[\"tipo\"], s[\"assunto\"]) for s in d[\"projeto\"][\"qualidade\"][\"sinais\"]]')\" = \"[('callers_open', 'formatPrice')]\" ]"
check "tests state passed, 12" "[ \"\$(q '(d[\"projeto\"][\"qualidade\"][\"testes\"][\"state\"], d[\"projeto\"][\"qualidade\"][\"testes\"][\"passed\"])')\" = \"('passed', 12)\" ]"
check "shortcut ledger: 2, 1 without trigger" "[ \"\$(q '(d[\"projeto\"][\"qualidade\"][\"atalhos\"][\"total\"], d[\"projeto\"][\"qualidade\"][\"atalhos\"][\"sem_gatilho\"])')\" = '(2, 1)' ]"

section "6. --compact (band)"
db monitor alpha --compact > "$J"
check "one line" "[ \"\$(wc -l < \"$J\" | tr -d ' ')\" = 1 ]"
check "phase, in-progress task, blockers, signals, tests" "[ \"\$(q '(d[\"projeto\"][\"em_andamento\"], d[\"projeto\"][\"bloqueios_abertos\"], d[\"projeto\"][\"sinais\"], d[\"projeto\"][\"testes\"])')\" = \"('t5', 1, {'callers_open': 1}, 'passed')\" ]"

section "8. read-only (and never in the future)"
SHA1="$(python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$OSFORGE_DB")"
check "database byte-identical after every monitor call" "[ \"$SHA0\" = \"$SHA1\" ]"
python3 -c "import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); c.execute(\"UPDATE state SET updated_at=datetime('now','+5 hours')\"); c.commit()" "$OSFORGE_DB"
db monitor > "$J"
check "last activity clamped to now (datetime('now','utc') shifts by the local offset)" "python3 -c 'import json,sys; from datetime import datetime,timezone; d=json.load(open(sys.argv[1])); now=datetime.now(timezone.utc).strftime(\"%Y-%m-%dT%H:%M:%SZ\"); assert all((p[\"ultima_atividade\"] or \"\") <= now for p in d[\"projetos\"])' \"$J\""

section "9. Canvas: /monitor page and /api/monitor"
H="$REPO/scripts/canvas/monitor.html"
check "page loads nothing external (no script src, stylesheet link, http(s) src/href/url, @import)" "! grep -Eq '<script[^>]+src=|<link[^>]+stylesheet|(src|href)=\"https?:|url\\(https?:|@import' \"$H\""
check "page never writes data as HTML (no .innerHTML / insertAdjacentHTML / document.write)" "! grep -Eq '\\.innerHTML|insertAdjacentHTML|document\\.write' \"$H\""
python3 - "$H" "$WORK/monitor.js" <<'EOF'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
open(sys.argv[2], "w", encoding="utf-8").write(re.findall(r"<script>(.*?)</script>", s, re.S)[0])
EOF
check "page script parses (node --check)" "node --check \"$WORK/monitor.js\" 2>/dev/null || ! command -v node >/dev/null"
if ! command -v bun >/dev/null 2>&1; then
  echo "  ⟳  bun ausente — rotas do Canvas não testadas aqui (rodam onde o Canvas roda)"
else
  PORT="$(python3 -c "import socket; s=socket.socket(); s.bind(('127.0.0.1',0)); print(s.getsockname()[1])")"
  CANVAS_PORT="$PORT" bun "$REPO/scripts/canvas/server.ts" --dir="$WORK/canvas" >"$WORK/server.log" 2>&1 &
  SPID=$!
  for _ in $(seq 50); do curl -sf "http://127.0.0.1:$PORT/api/health" >/dev/null 2>&1 && break; sleep 0.1; done
  U="http://127.0.0.1:$PORT"
  code(){ curl -s -o "$WORK/resp" -w '%{http_code}' "$@"; }
  check "GET /monitor → 200 html" "[ \"\$(code \"$U/monitor\")\" = 200 ] && grep -q 'OSForge Monitor' \"$WORK/resp\""
  check "/monitor sends a CSP that forbids external loads" "curl -s -D - -o /dev/null \"$U/monitor\" | grep -i '^content-security-policy:' | grep -q \"default-src 'none'\""
  check "/api/monitor → portfolio JSON" "[ \"\$(code \"$U/api/monitor?days=30\")\" = 200 ] && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d[\"schema\"]==\"osforge.monitor.v1\" and \"projetos\" in d' \"$WORK/resp\""
  check "/api/monitor?project=alpha → detail" "[ \"\$(code \"$U/api/monitor?project=alpha\")\" = 200 ] && grep -q '\"fases_detalhe\"' \"$WORK/resp\""
  check "unknown project → 404" "[ \"\$(code \"$U/api/monitor?project=nope\")\" = 404 ]"
  check "bad slug (path traversal) → 400" "[ \"\$(code \"$U/api/monitor?project=..%2Fx\")\" = 400 ]"
  check "days out of range → 400" "[ \"\$(code \"$U/api/monitor?days=0\")\" = 400 ] && [ \"\$(code \"$U/api/monitor?days=1e3\")\" = 400 ]"
  check "foreign Origin → 403" "[ \"\$(code -H 'Origin: https://evil.example' \"$U/api/monitor\")\" = 403 ]"
  check "foreign Host (DNS rebinding) → 403" "[ \"\$(code -H 'Host: evil.example:$PORT' \"$U/api/monitor\")\" = 403 ] && [ \"\$(code -H 'Host: evil.example:$PORT' \"$U/monitor\")\" = 403 ]"
  # SSE: reading the db (the page's own reload) must not emit "monitor"; a write must.
  curl -sN --max-time 9 "$U/api/events" > "$WORK/sse.txt" 2>/dev/null &
  CPID=$!
  sleep 0.5; curl -s "$U/api/monitor?days=7" >/dev/null; sleep 2.6; curl -s "$U/api/monitor?days=90" >/dev/null; sleep 2.6
  READS="$(grep -c '"monitor"' "$WORK/sse.txt" || true)"
  db add-decision alpha "decisão nova para o SSE" >/dev/null 2>&1; sleep 3
  wait "$CPID" 2>/dev/null
  check "SSE: reads do not trigger a monitor event (no reload loop)" "[ \"$READS\" = 0 ]"
  check "SSE: a write triggers one" "[ \"\$(grep -c '\"monitor\"' \"$WORK/sse.txt\")\" -ge 1 ]"
  check "discover=1 → sem_cadastro block" "[ \"\$(code \"$U/api/monitor?discover=1\")\" = 200 ] && grep -q '\"sem_cadastro\"' \"$WORK/resp\""
  # Optional browser smoke test (Playwright for Python + a Chromium): both views render with no
  # page error. Skipped where no browser is installed.
  if python3 -c "import playwright" >/dev/null 2>&1; then
    SMOKE="$(python3 - "$U" <<'EOF' 2>&1
import asyncio, sys
from playwright.async_api import async_playwright
async def main(u):
    errs = []
    async with async_playwright() as p:
        try:
            b = await p.chromium.launch()
        except Exception as e:
            print("SKIP", e.__class__.__name__); return
        pg = await b.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for frag, needle in (("", "Projetos"), ("", "Ativo agora"), ("#p=alpha", "Quadro de tarefas"), ("#p=alpha", "Conversa com os agentes")):
            await pg.goto(u + "/monitor" + frag); await pg.wait_for_timeout(1200)
            if needle not in await pg.inner_text("main"):
                errs.append("missing " + needle)
        await b.close()
    print("OK" if not errs else "ERR " + "; ".join(errs))
asyncio.run(main(sys.argv[1]))
EOF
)"
    case "$SMOKE" in
      SKIP*) echo "  ⟳  sem Chromium para o Playwright — smoke do navegador pulado" ;;
      *) check "browser: portfolio and project views render without page errors" "[ \"\$SMOKE\" = OK ] || { echo \"     \$SMOKE\"; false; }" ;;
    esac
  else
    echo "  ⟳  Playwright ausente — smoke do navegador pulado"
  fi
  kill "$SPID" 2>/dev/null; wait "$SPID" 2>/dev/null
fi

section "10. command centre: groups by age, live detection, inbox, runs (P-06)"
python3 - "$OSFORGE_DB" <<'EOF'
import sqlite3, sys
from datetime import datetime, timedelta, timezone
c = sqlite3.connect(sys.argv[1])
now = datetime.now(timezone.utc)
for slug, hours in (("w1", 30), ("w2", 24 * 29), ("h1", 24 * 31)):
    c.execute("INSERT INTO projects (slug, description, status) VALUES (?,?, 'active')", (slug, slug))
    pid = c.execute("SELECT id FROM projects WHERE slug=?", (slug,)).fetchone()[0]
    c.execute("INSERT INTO tasks (project_id, title, updated_at) VALUES (?,?,?)",
              (pid, "t", (now - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")))
c.execute("INSERT INTO projects (slug, description, status) VALUES ('held', 'h', 'paused')")
c.execute("INSERT INTO projects (slug, description, status) VALUES ('none', 'n', 'active')")
c.execute("UPDATE projects SET created_at=updated_at")
c.commit()
EOF
db monitor > "$J"
grp(){ q "[p[\"grupo_base\"] for p in d[\"projetos\"] if p[\"slug\"]==\"$1\"][0]"; }
check "30 h without activity → aguardando" "[ \"\$(grp w1)\" = aguardando ]"
check "29 days → still aguardando" "[ \"\$(grp w2)\" = aguardando ]"
check "31 days → historico" "[ \"\$(grp h1)\" = historico ]"
check "held (paused) → historico, with the reason" "[ \"\$(grp held)\" = historico ] && [ \"\$(q '[p[\"grupo_regra\"] for p in d[\"projetos\"] if p[\"slug\"]==\"held\"][0]')\" = segurado ]"
check "rules exposed: 24 h / 30 days" "[ \"\$(q '(d[\"regras_grupo\"][\"aguardando_apos_h\"], d[\"regras_grupo\"][\"historico_apos_dias\"])')\" = '(24, 30)' ]"

# live detection with captured ps/cwd (macOS process titles)
L="$WORK/live"; mkdir -p "$L/novo" && (cd "$L/novo" && $GIT init -q && echo x > a && $GIT add a && $GIT commit -qm i)
cat > "$WORK/ps.txt" <<EOF
  101 claude
  102 /Users/x/.local/bin/claude --resume abc
  103 node /x/node_modules/.bin/next dev --turbo
  104 /Applications/Cursor.app/Contents/Frameworks/Cursor Helper (Plugin).app/Contents/MacOS/Cursor Helper (Plugin): extension-host (user) alpha [1-1]
  105 /Applications/Visual Studio Code.app/Contents/Frameworks/Code Helper (Plugin).app/Contents/MacOS/Code Helper (Plugin): extension-host (user) outra-pasta [2-3]
  111 /Applications/Cursor.app/Contents/Frameworks/Cursor Helper (Plugin).app/Contents/MacOS/Cursor Helper (Plugin): extension-host (user) novo [3-1]
  106 /usr/bin/python3 /x/osforge-db.py live
  107 node server.js
  108 claude
  109 sh -c next dev
  110 node /x/node_modules/.bin/vite build
EOF
python3 -c "import json,sys; print(json.dumps({'101': sys.argv[1], '102': sys.argv[2], '103': sys.argv[1] + '/lib', '107': sys.argv[1], '108': '/', '109': sys.argv[1] + '/lib', '110': sys.argv[1]}))" "$A" "$L/novo" > "$WORK/cwd.json"
mkdir -p "$HOME/.claude/projects/$(printf '%s' "$A" | sed 's/[^A-Za-z0-9]/-/g')" && touch "$HOME/.claude/projects/$(printf '%s' "$A" | sed 's/[^A-Za-z0-9]/-/g')/s.jsonl"
OSFORGE_LIVE_PS_FILE="$WORK/ps.txt" OSFORGE_LIVE_CWD_FILE="$WORK/cwd.json" db live > "$J"
check "live: claude in alpha, working now (fresh transcript)" "[ \"\$(q '(d[\"projetos\"][\"alpha\"][\"claude\"], d[\"projetos\"][\"alpha\"][\"trabalhando\"])')\" = '(1, True)' ]"
check "live: next dev in a subfolder maps to alpha, its sh wrapper is the same server, vite build and plain node are not servers" "[ \"\$(q 'len(d[\"projetos\"][\"alpha\"][\"servidores\"])')\" = 1 ]"
check "live: Cursor window on alpha (IDE helper process title)" "[ \"\$(q 'd[\"projetos\"][\"alpha\"][\"ides\"]')\" = \"['Cursor']\" ]"
check "live: unregistered folders listed once each (claude + Cursor in novo, VS Code on outra-pasta)" "[ \"\$(q 'sorted((x[\"nome\"], x[\"claude\"], x[\"ides\"]) for x in d[\"sem_cadastro\"])')\" = \"[('novo', 1, ['Cursor']), ('outra-pasta', 0, ['VS Code'])]\" ]"
check "live: claude in / is ignored, osforge itself is not a server" "[ \"\$(q 'sum(v[\"claude\"] for v in d[\"projetos\"].values()) + sum(x[\"claude\"] for x in d[\"sem_cadastro\"])')\" = 2 ]"
OSFORGE_LIVE_PS_FILE="$WORK/ps.txt" OSFORGE_LIVE_CWD_FILE="$WORK/cwd.json" db monitor --live > "$J"
check "monitor --live embeds the live block" "[ \"\$(q 'd[\"ao_vivo\"][\"projetos\"][\"alpha\"][\"claude\"]')\" = 1 ]"

# inbox
export OSFORGE_INBOX_DIR="$WORK/inbox"
check "inbox-add → id and flag file" "db --json inbox-add alpha 'use Server Actions no checkout' | grep -q '\"id\"' && [ -f \"$OSFORGE_INBOX_DIR/alpha\" ]"
check "empty or oversized message → exit 2" "db inbox-add alpha '  ' >/dev/null 2>&1; [ \$? -eq 2 ] && db inbox-add alpha \"\$(python3 -c 'print(\"x\"*4001)')\" >/dev/null 2>&1; [ \$? -eq 2 ]"
db --json inbox-add alpha "segunda orientação" >/dev/null
db monitor alpha > "$J"
check "monitor: 2 pending in the project and in the conversation" "[ \"\$(q '(d[\"projeto\"][\"inbox_pendentes\"], [m[\"status\"] for m in d[\"projeto\"][\"conversa\"] if m[\"tipo\"]==\"orientacao\"])')\" = \"(2, ['pendente', 'pendente'])\" ]"
T1="$(db inbox-take alpha --session=sess-aaaaaaaa-1)"; T2="$(db inbox-take alpha --session=sess-bbbbbbbb-2)"
check "inbox-take hands both to the first session, none to the second" "[ \"\$(printf '%s' \"\$T1\" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')\" = 2 ] && [ \"\$T2\" = '[]' ]"
check "flag removed when nothing is pending" "[ ! -f \"$OSFORGE_INBOX_DIR/alpha\" ]"
check "delivery recorded with the session" "db --json inbox alpha | python3 -c 'import json,sys; d=json.load(sys.stdin); assert all(m[\"status\"]==\"entregue\" and m[\"sessao\"]==\"sess-aaa\" for m in d), d'"
ID="$(db --json inbox-add alpha 'cancelar esta' | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')"
db inbox-cancel "$ID" >/dev/null 2>&1
check "cancel → cancelada, flag gone" "[ ! -f \"$OSFORGE_INBOX_DIR/alpha\" ] && db --json inbox alpha | grep -q '\"cancelada\"'"
check "inbox-take on an unknown project → [] and exit 0" "[ \"\$(db inbox-take ghost --session=x)\" = '[]' ]"

# runs
RID="$(db --json run-add alpha --kind=background --tool=claude '--prompt=rode os testes' --status=rodando | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')"
db run-update "$RID" --status=concluida '--result=12 testes ok' --cost=0.42 >/dev/null 2>&1
check "runs: recorded and closed with result and cost" "db --json runs alpha | python3 -c 'import json,sys; r=json.load(sys.stdin)[0]; assert (r[\"status\"], r[\"resultado\"], r[\"custo\"])==(\"concluida\", \"12 testes ok\", 0.42) and r[\"fim\"], r'"
python3 -c "import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); c.execute(\"INSERT INTO runs (project_id, kind, tool, status, pid) VALUES ((SELECT id FROM projects WHERE slug='alpha'), 'background', 'claude', 'rodando', 999999)\"); c.commit()" "$OSFORGE_DB"
db runs-reconcile >/dev/null 2>&1
check "runs-reconcile: a run whose process is gone → interrompida" "db --json runs alpha | python3 -c 'import json,sys; r=[x for x in json.load(sys.stdin) if x[\"pid\"]==999999][0]; assert r[\"status\"]==\"interrompida\", r'"
check "run-add with a bad kind → exit 2" "db run-add alpha --kind=rocket >/dev/null 2>&1; [ \$? -eq 2 ]"
db monitor alpha > "$J"
check "conversation merges messages and runs" "[ \"\$(q 'sorted(set(m[\"tipo\"] for m in d[\"projeto\"][\"conversa\"]))')\" = \"['execucao', 'orientacao']\" ]"
unset OSFORGE_INBOX_DIR

section "11. command centre actions on the Canvas server (P-06 §4–5)"
if ! command -v bun >/dev/null 2>&1; then
  echo "  ⟳  bun ausente — ações do servidor não testadas aqui"
else
  F="$WORK/fake"; mkdir -p "$F" "$WORK/apps/Cursor.app"
  cat > "$F/open" <<'SH'
#!/bin/bash
printf '%s\n' "$@" > "$OPEN_LOG"
SH
  cat > "$F/claude" <<'SH'
#!/bin/bash
printf '%s\n' "$@" > "$CLAUDE_LOG"
if [ "$1" = "-p" ]; then
  echo '{"type":"system","subtype":"init"}'
  echo '{"type":"result","subtype":"success","is_error":false,"result":"2 arquivos revisados","total_cost_usd":0.12}'
fi
SH
  chmod +x "$F/open" "$F/claude"
  export OPEN_LOG="$WORK/open.log" CLAUDE_LOG="$WORK/claude.log" OSFORGE_INBOX_DIR="$WORK/inbox2"
  PORT2="$(python3 -c "import socket; s=socket.socket(); s.bind(('127.0.0.1',0)); print(s.getsockname()[1])")"
  OSFORGE_OPEN_CMD="$F/open" OSFORGE_CLAUDE_CMD="$F/claude" OSFORGE_APPS_DIRS="$WORK/apps" CANVAS_PORT="$PORT2" \
    bun "$REPO/scripts/canvas/server.ts" --dir="$WORK/canvas2" >"$WORK/server2.log" 2>&1 &
  SPID2=$!
  for _ in $(seq 50); do curl -sf "http://127.0.0.1:$PORT2/api/health" >/dev/null 2>&1 && break; sleep 0.1; done
  U2="http://127.0.0.1:$PORT2"
  post(){ curl -s -o "$WORK/resp" -w '%{http_code}' -X POST "$U2$1" -H 'Content-Type: application/json' --data "$2" "${@:3}"; }
  check "tools: Cursor found, claude found, Terminal available" "curl -s \"$U2/api/tools\" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert [i[\"id\"] for i in d[\"ides\"]]==[\"cursor\"] and d[\"claude\"] and d[\"terminal\"], d'"
  check "POST without JSON content-type → 415" "[ \"\$(curl -s -o /dev/null -w '%{http_code}' -X POST \"$U2/api/inbox\" --data '{}')\" = 415 ]"
  check "POST from a foreign Origin → 403" "[ \"\$(post /api/inbox '{\"project\":\"alpha\",\"text\":\"x\"}' -H 'Origin: https://evil.example')\" = 403 ]"
  check "GET on an action route → 404 (only POST acts)" "[ \"\$(curl -s -o /dev/null -w '%{http_code}' \"$U2/api/launch\")\" = 404 ]"
  check "inbox: message starting with -- stored literally (201)" "[ \"\$(post /api/inbox '{\"project\":\"alpha\",\"text\":\"--json nao e flag\"}')\" = 201 ] && db --json inbox alpha | grep -q -- '--json nao e flag' && [ -f \"$OSFORGE_INBOX_DIR/alpha\" ]"
  check "inbox: unknown project → 404; empty text → 400" "[ \"\$(post /api/inbox '{\"project\":\"ghost\",\"text\":\"x\"}')\" = 404 ] && [ \"\$(post /api/inbox '{\"project\":\"alpha\",\"text\":\" \"}')\" = 400 ]"
  check "launch on a project without a folder → 409" "[ \"\$(post /api/launch '{\"project\":\"empty\",\"mode\":\"ide\",\"ide\":\"cursor\"}')\" = 409 ]"
  check "launch IDE: open -a <Cursor.app> <root from the database>" "[ \"\$(post /api/launch '{\"project\":\"alpha\",\"mode\":\"ide\",\"ide\":\"cursor\"}')\" = 201 ] && [ \"\$(cat \"$OPEN_LOG\" | tr '\\n' '|')\" = \"-a|$WORK/apps/Cursor.app|$A|\" ]"
  check "launch IDE not installed → 400; a client-sent folder is ignored" "[ \"\$(post /api/launch '{\"project\":\"alpha\",\"mode\":\"ide\",\"ide\":\"zed\",\"root\":\"/etc\"}')\" = 400 ]"
  TXT='Revise o checkout; use '"'"'aspas'"'"', $(rm -rf ~) e `whoami` sem executar'
  BODY="$(python3 -c 'import json,sys; print(json.dumps({"project":"alpha","mode":"terminal","text":sys.argv[1]}))' "$TXT")"
  check "launch Terminal: .command opened in Terminal" "[ \"\$(post /api/launch \"\$BODY\")\" = 201 ] && sed -n 1,2p \"$OPEN_LOG\" | tr '\\n' '|' | grep -q '^-a|Terminal|'"
  CMDF="$(sed -n 3p "$OPEN_LOG")"
  check ".command is 0700 and only cds into the project" "[ \"\$(python3 -c 'import os,stat,sys; print(oct(stat.S_IMODE(os.stat(sys.argv[1]).st_mode)))' \"$CMDF\")\" = 0o700 ] && grep -q \"^cd '$A' || exit 1\" \"$CMDF\""
  bash "$CMDF" >/dev/null 2>&1
  check "the instruction reaches claude as ONE argument, byte for byte (quotes, \$( ), backticks inert)" "[ \"\$(cat \"$CLAUDE_LOG\")\" = \"\$TXT\" ]"
  BODY2="$(python3 -c 'import json; print(json.dumps({"project":"alpha","mode":"terminal","text":"--dangerously-skip-permissions"}))')"
  post /api/launch "$BODY2" >/dev/null; bash "$(sed -n 3p "$OPEN_LOG")" >/dev/null 2>&1
  check "an instruction starting with - stays a prompt (leading space), never a claude option" "[ \"\$(cat \"$CLAUDE_LOG\")\" = ' --dangerously-skip-permissions' ]"
  check "background without an instruction → 400" "[ \"\$(post /api/launch '{\"project\":\"alpha\",\"mode\":\"background\"}')\" = 400 ]"
  check "background: 201 with a run id" "[ \"\$(post /api/launch '{\"project\":\"alpha\",\"mode\":\"background\",\"text\":\"revise os testes\",\"acceptEdits\":true}')\" = 201 ]"
  for _ in $(seq 40); do db --json runs alpha | grep -q '"concluida".*"tipo": "background"\|"tipo": "background".*"concluida"' && break; sleep 0.1; done
  check "background: claude -p with stream-json and acceptEdits, run closed with result and cost" "db --json runs alpha | python3 -c 'import json,sys; r=[x for x in json.load(sys.stdin) if x[\"tipo\"]==\"background\"][0]; assert (r[\"status\"], r[\"resultado\"], r[\"custo\"])==(\"concluida\",\"2 arquivos revisados\",0.12), r' && head -1 \"$CLAUDE_LOG\" | grep -qx -- -p && grep -qx acceptEdits \"$CLAUDE_LOG\""
  check "status: segurar → historico" "[ \"\$(post /api/project/status '{\"project\":\"w1\",\"status\":\"paused\"}')\" = 200 ] && db monitor | python3 -c 'import json,sys; d=json.load(sys.stdin); assert [p[\"grupo_base\"] for p in d[\"projetos\"] if p[\"slug\"]==\"w1\"]==[\"historico\"]'"
  check "status: invalid value → 400" "[ \"\$(post /api/project/status '{\"project\":\"w1\",\"status\":\"deleted\"}')\" = 400 ]"
  BDR="$(cd "$Bdir" && pwd -P)"
  check "bind: suggested root from discovery (beta)" "[ \"\$(post /api/project/bind '{\"project\":\"beta\"}')\" = 200 ] && db --json list-projects --status=all | grep -qF \"\$BDR\""
  DUP="$WORK/dup/w1"; mkdir -p "$DUP" && (cd "$DUP" && $GIT init -q && echo x > a && $GIT add a && $GIT commit -qm i)
  mkdir -p "$HOME/.claude/projects/-dup"; python3 -c "import json,sys; print(json.dumps({'type':'user','cwd':sys.argv[1]}))" "$DUP" > "$HOME/.claude/projects/-dup/1.jsonl"
  DUPR="$(cd "$DUP" && pwd -P)"
  check "register: a folder named like an existing project (w1) is that project, never re-registered; w1 untouched" "[ \"\$(post /api/project/register \"{\\\"pasta\\\":\\\"$DUPR\\\"}\")\" != 201 ] && db --json list-projects --status=all | python3 -c 'import json,sys; p=[x for x in json.load(sys.stdin) if x[\"slug\"]==\"w1\"][0]; assert p[\"root_path\"] is None and p[\"status\"]==\"paused\", p'"
  check "register: only a discovered folder; then it is a project" "[ \"\$(post /api/project/register '{\"pasta\":\"/etc\"}')\" = 404 ] && [ \"\$(post /api/project/register \"{\\\"pasta\\\":\\\"$(cd "$N" && pwd -P)\\\"}\")\" = 201 ] && db --json list-projects --status=all | grep -q '\"novo-app\"'"
  kill "$SPID2" 2>/dev/null; wait "$SPID2" 2>/dev/null
  unset OSFORGE_INBOX_DIR
fi

section "7. budget: 50,000 calls"
python3 - "$OSFORGE_DB" <<'EOF'
import sqlite3, sys, random
from datetime import datetime, timedelta, timezone
c = sqlite3.connect(sys.argv[1])
ids = [r[0] for r in c.execute("SELECT id FROM projects")] + [None]
now = datetime.now(timezone.utc)
random.seed(7)
rows = []
# 1,250 sessions of 40 calls, ~45 s apart, each in one project, spread over 80 days (the shape
# of real transcripts: a session is a burst, not 40 calls scattered across months).
for sess in range(1250):
    start = now - timedelta(seconds=random.randint(3600, 80 * 86400))
    pid = random.choice(ids)
    for j in range(40):
        t = start + timedelta(seconds=45 * j + random.randint(0, 30))
        i = sess * 40 + j
        rows.append((f"b{i}", pid, f"sess{sess}", t.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                     random.choice(["claude-sonnet-4-6", "claude-haiku-4-5", "claude-opus-4-1"]), 100, 50, 1000, 10, 0, i % 3 == 0))
c.executemany("INSERT INTO calls (message_id, project_id, session_id, ts, model, input, output, cache_read, "
              "cache_write_5m, cache_write_1h, sidechain) VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
c.commit()
EOF
MS="$(python3 - "$REPO/scripts/osforge-db.py" <<'EOF'
import subprocess, sys, time
db = sys.argv[1]
def med(args):
    ts = []
    for _ in range(5):
        t0 = time.time(); subprocess.run(["python3", db] + args, capture_output=True, check=True); ts.append(time.time() - t0)
    return int(sorted(ts)[2] * 1000)
print(med(["monitor"]), med(["monitor", "alpha"]), med(["monitor", "alpha", "--compact"]))
EOF
)"
set -- $MS
echo "     portfolio ${1} ms · project ${2} ms · compact ${3} ms"
check "band (--compact) < 200 ms" "[ \"$3\" -lt 200 ]"
check "project detail < 400 ms" "[ \"$2\" -lt 400 ]"
check "portfolio < 600 ms" "[ \"$1\" -lt 600 ]"

echo ""
echo "test-monitor: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
