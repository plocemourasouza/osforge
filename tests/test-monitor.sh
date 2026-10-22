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
check "archived project left out by default" "[ \"\$(q '[p[\"slug\"] for p in d[\"projetos\"]]')\" = \"['alpha', 'beta', 'empty']\" ]"
check "order: active, backlog, then outro" "[ \"\$(q '[p[\"status\"] for p in d[\"projetos\"]]')\" = \"['active', 'backlog', 'outro']\" ]"
check "legacy status kept raw, shown as outro" "[ \"\$(q '[p[\"status_bruto\"] for p in d[\"projetos\"] if p[\"slug\"]==\"empty\"][0]')\" = someday ]"
check "totals: open tasks 3, blockers 1, signals 1 (tests excluded)" "[ \"\$(q '(d[\"totais\"][\"tarefas_abertas\"], d[\"totais\"][\"bloqueios_abertos\"], d[\"totais\"][\"sinais_abertos\"])')\" = '(3, 1, 1)' ]"
check "period: 5 calls (one outside the horizon), 3 sessions" "[ \"\$(q '(d[\"totais\"][\"chamadas\"], d[\"totais\"][\"sessoes\"])')\" = '(5, 3)' ]"
check "health: 1 of 5 calls without project = 20.0%" "[ \"\$(q 'd[\"saude\"][\"chamadas_sem_projeto_pct\"]')\" = 20.0 ]"
check "health: projects without a root" "[ \"\$(q 'd[\"saude\"][\"projetos_sem_raiz\"]')\" = \"['beta', 'empty']\" ]"
check "window from quota.json" "[ \"\$(q 'd[\"janela\"][\"five_hour\"][\"pct\"]')\" = 63.0 ]"
check "series covers the 84-day horizon" "[ \"\$(q 'len(d[\"projetos\"][0][\"serie\"])')\" = 84 ]"
check "alpha: pct = 2 done / 5 live = 40.0" "[ \"\$(q 'd[\"projetos\"][0][\"pct\"]')\" = 40.0 ]"
check "alpha: cost matches the hand count" "[ \"\$(q 'd[\"projetos\"][0][\"periodo\"][\"custo\"]')\" = \"$EXP_COST\" ]"
check "alpha: tokens = input+output+writes (cache reads apart)" "[ \"\$(q 'd[\"projetos\"][0][\"periodo\"][\"tokens\"]')\" = $((1000+500+2000+100+400+100+300+30)) ]"
check "alpha: agent minutes = (60 s + capped 300 s) / 60 = 6.0" "[ \"\$(q 'd[\"projetos\"][0][\"periodo\"][\"minutos\"]')\" = 6.0 ]"
check "alpha: has a root on disk" "[ \"\$(q 'd[\"projetos\"][0][\"acesso\"][\"raiz_existe\"]')\" = True ]"
db monitor --all > "$J"
check "--all includes archived" "[ \"\$(q 'sorted(p[\"slug\"] for p in d[\"projetos\"])')\" = \"['alpha', 'beta', 'empty', 'gamma']\" ]"
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
db monitor --discover > "$J"
check "unregistered git folder listed by its root, with the command" "[ \"\$(q '[(x[\"nome\"], x[\"git\"], \"upsert-project novo-app\" in x[\"comando\"]) for x in d[\"sem_cadastro\"]]')\" = \"[('novo-app', True, True)]\" ]"
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

section "8. read-only"
SHA1="$(python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$OSFORGE_DB")"
check "database byte-identical after every monitor call" "[ \"$SHA0\" = \"$SHA1\" ]"

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
