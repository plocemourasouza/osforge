#!/usr/bin/env bash
# tests/test-calls.sh — B-028 (auditoria por chamada + custo + retenção).
#
# Transcripts sintéticos com o formato real de message.usage/timestamp/isSidechain/
# isApiErrorMessage; hooks reais (session-save.py); osforge-db real em banco temporário.
# Sem rede, sem tocar em ~/.claude vivo. Cobre os 10 casos do SPEC-L03 + privacidade:
#   1. mesmo message.id em 3 linhas → 1 linha em `calls`; tokens == tabela usage da mesma sessão
#   2. isSidechain:true → sidechain=1; --by sidechain separa
#   3. linha de rejeição (formato EV-C04) → error="rate_limit" e tokens zero
#   4. Stop repetido → contagem de linhas inalterada
#   5. cache_creation com 5m e 1h → colunas separadas; sem detalhe → tudo em 5m
#   6. preço: modelo conhecido bate com conta manual; modelo desconhecido → custo 0 + "sem preço"
#   7. --since 5h exclui chamada de 6h atrás
#   8. prune-calls --older-than 90d remove só o que passou; roda no máximo uma vez por dia
#   9. backfill-calls numa árvore com subpastas → mesma contagem que passada direta; idempotente
#   10. nenhuma linha de `calls` contém texto de mensagem (varredura por marcador plantado)
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }

export HOME="$WORK/home"; mkdir -p "$HOME/.claude/projects/x"
export OSFORGE_DB="$WORK/db.sqlite" OSFORGE_LOG_DIR="$WORK/logs"
export OSFORGE_CALLS_PRUNE_MARKER="$WORK/calls-pruned-at"
unset OSFORGE_PROJECT OSFORGE_CALLS OSFORGE_CALLS_RETENTION_DAYS OSFORGE_PRICING
SAVE="$REPO/hooks/session-save.py"
db(){ python3 "$REPO/scripts/osforge-db.py" "$@"; }

GIT="git -c user.name=t -c user.email=t@t -c init.defaultBranch=main -c commit.gpgsign=false"
PROJ="$WORK/proj"; mkdir -p "$PROJ" && (cd "$PROJ" && $GIT init -q && echo x > f && $GIT add f && $GIT commit -qm i)
db upsert-project alpha "a" standard active --root="$PROJ" >/dev/null 2>&1

now_iso(){ python3 -c "import sys; from datetime import datetime,timezone,timedelta; print((datetime.now(timezone.utc)-timedelta(hours=float(sys.argv[1]))).strftime('%Y-%m-%dT%H:%M:%SZ'))" "$1"; }

section "1+2+5. mesma message.id 3x, sidechain, cache_creation 5m/1h (write path)"
U1="$HOME/.claude/projects/x/u1.jsonl"
TS1="$(now_iso 0)"
python3 - "$U1" "$TS1" <<'EOF'
import json, sys
p, ts = sys.argv[1], sys.argv[2]
def a(mid, model, sidechain, extra_usage, text, uuid):
    e = {"type": "assistant", "uuid": uuid, "timestamp": ts, "isSidechain": sidechain,
         "message": {"id": mid, "role": "assistant", "model": model, "stop_reason": "end_turn",
                      "usage": {"input_tokens": 100, "output_tokens": 50,
                                "cache_read_input_tokens": 10, **extra_usage},
                      "content": [{"type": "text", "text": text}]}}
    return json.dumps(e)
with open(p, "w") as f:
    f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "tarefa"}}) + "\n")
    # message m1 repetida em 3 linhas (blocos de conteúdo) — deve contar UMA vez
    f.write(a("m1", "claude-sonnet-4-6", False, {"cache_creation_input_tokens": 0}, "bloco 1", "u1a") + "\n")
    f.write(a("m1", "claude-sonnet-4-6", False, {"cache_creation_input_tokens": 0}, "bloco 2", "u1b") + "\n")
    f.write(a("m1", "claude-sonnet-4-6", False, {"cache_creation_input_tokens": 0}, "bloco 3", "u1c") + "\n")
    # m2: subagente (sidechain), sem cache_creation detalhado (fallback -> 5m)
    f.write(a("m2", "claude-haiku-4-5", True, {"cache_creation_input_tokens": 40}, "sub", "u2") + "\n")
    # m3: cache_creation detalhado com 5m e 1h
    e3 = {"type": "assistant", "uuid": "u3", "timestamp": ts, "isSidechain": False,
          "message": {"id": "m3", "role": "assistant", "model": "claude-sonnet-4-6", "stop_reason": "end_turn",
                       "usage": {"input_tokens": 20, "output_tokens": 10, "cache_read_input_tokens": 0,
                                 "cache_creation": {"ephemeral_5m_input_tokens": 7, "ephemeral_1h_input_tokens": 13}},
                       "content": [{"type": "text", "text": "detalhado"}]}}
    f.write(json.dumps(e3) + "\n")
EOF
(cd "$PROJ" && printf '{"session_id":"sess-1","transcript_path":"%s"}' "$U1" | python3 "$SAVE"); RC=$?
check "Stop: exit 0" '[ $RC -eq 0 ]'
CJ="$(db calls --project=alpha --by=model --json)"
check "m1 (3 linhas, mesmo message.id) conta como 1 chamada" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1]); g=[x for x in d[\"groups\"] if x[\"key\"]==\"claude-sonnet-4-6\"][0]
assert g[\"calls\"]==2, g" "$CJ"'
UJ="$(db usage alpha --json)"
check "tokens de calls == tokens de usage (mesma sessão, mesmo modelo)" 'python3 -c "
import json,sys; c=json.loads(sys.argv[1]); u=json.loads(sys.argv[2])
gs=[x for x in c[\"groups\"] if x[\"key\"]==\"claude-sonnet-4-6\"][0]
us=[s for s in u[\"sessions\"] if s[\"model\"]==\"claude-sonnet-4-6\"][0]
assert gs[\"input\"]==us[\"input_tokens\"]==120, (gs,us)
assert gs[\"output\"]==us[\"output_tokens\"]==60, (gs,us)" "$CJ" "$UJ"'
check "sidechain separa m2 do restante (--by sidechain)" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1]); s=[x for x in d[\"groups\"] if x[\"key\"]==\"sidechain\"][0]
assert s[\"calls\"]==1, s" "$(db calls --project=alpha --by=sidechain --json)"'
check "sem cache_creation detalhado (m2) → tudo em cache_write_5m" 'python3 -c "
import sqlite3; c=sqlite3.connect(\"$OSFORGE_DB\"); r=c.execute(\"SELECT cache_write_5m,cache_write_1h FROM calls WHERE message_id=\\\"m2\\\"\").fetchone()
assert r==(40,0), r"'
check "cache_creation detalhado (m3) → 5m e 1h em colunas separadas" 'python3 -c "
import sqlite3; c=sqlite3.connect(\"$OSFORGE_DB\"); r=c.execute(\"SELECT cache_write_5m,cache_write_1h FROM calls WHERE message_id=\\\"m3\\\"\").fetchone()
assert r==(7,13), r"'

section "4. Stop repetido não duplica"
N_BEFORE="$(python3 -c "import sqlite3; print(sqlite3.connect('$OSFORGE_DB').execute('SELECT COUNT(*) FROM calls').fetchone()[0])")"
(cd "$PROJ" && printf '{"session_id":"sess-1","transcript_path":"%s"}' "$U1" | python3 "$SAVE")
N_AFTER="$(python3 -c "import sqlite3; print(sqlite3.connect('$OSFORGE_DB').execute('SELECT COUNT(*) FROM calls').fetchone()[0])")"
check "Stop repetido: contagem de linhas inalterada ($N_BEFORE == $N_AFTER)" '[ "$N_BEFORE" = "$N_AFTER" ]'

section "3. rejeição (formato EV-C04) → error='rate_limit', tokens zero"
U2="$HOME/.claude/projects/x/u2.jsonl"
TS2="$(now_iso 0)"
python3 - "$U2" "$TS2" <<'EOF'
import json, sys
p, ts = sys.argv[1], sys.argv[2]
with open(p, "w") as f:
    f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "trabalhando"}}) + "\n")
    f.write(json.dumps({
        "type": "assistant", "uuid": "u-rej", "timestamp": ts, "isSidechain": False,
        "message": {"id": "m-rej", "role": "assistant", "model": "<synthetic>",
                     "usage": {"input_tokens": 0, "output_tokens": 0,
                               "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
                     "content": [{"type": "text", "text": ""}]},
        "isApiErrorMessage": True, "error": "rate_limit",
        "quotaLimits": {"status": "rejected", "rateLimitType": "five_hour"},
    }) + "\n")
EOF
(cd "$PROJ" && printf '{"session_id":"sess-rej","transcript_path":"%s"}' "$U2" | python3 "$SAVE")
check "linha de rejeição gravada com error=rate_limit e tokens zero" 'python3 -c "
import sqlite3; c=sqlite3.connect(\"$OSFORGE_DB\"); r=c.execute(\"SELECT error,input,output FROM calls WHERE message_id=\\\"m-rej\\\"\").fetchone()
assert r==(\"rate_limit\",0,0), r"'

section "6. preço: modelo conhecido bate com conta manual; desconhecido → custo 0 + sem preço"
CJ6="$(db calls --project=alpha --by=model --json)"
check "claude-sonnet-4-6: custo == conta manual (pricing.json real do repo)" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1]); g=[x for x in d[\"groups\"] if x[\"key\"]==\"claude-sonnet-4-6\"][0]
# 2 chamadas: in=120 out=60 cache_read=10 cache_write_5m=7 cache_write_1h=13 (m1+m3)
expect = 120*3/1e6 + 60*15/1e6 + 10*0.30/1e6 + 7*3.75/1e6 + 13*6/1e6
assert abs(g[\"cost_usd\"] - expect) < 1e-9, (g[\"cost_usd\"], expect)" "$CJ6"'
check "claude-haiku-4-5 (m2): custo == conta manual" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1]); g=[x for x in d[\"groups\"] if x[\"key\"]==\"claude-haiku-4-5\"][0]
# m2: input=100 output=50 cache_read=10 cache_write_5m=40 (fallback sem cache_creation detalhado) cache_write_1h=0
expect = 100*1/1e6 + 50*5/1e6 + 10*0.10/1e6 + 40*1.25/1e6 + 0*2/1e6
assert abs(g[\"cost_usd\"] - expect) < 1e-9, (g[\"cost_usd\"], expect)" "$CJ6"'
check "<synthetic> (rejeição): custo 0" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1]); g=[x for x in d[\"groups\"] if x[\"key\"]==\"<synthetic>\"][0]
assert g[\"cost_usd\"]==0.0, g" "$CJ6"'
U3="$HOME/.claude/projects/x/u3.jsonl"
TS3="$(now_iso 0)"
python3 - "$U3" "$TS3" <<'EOF'
import json, sys
p, ts = sys.argv[1], sys.argv[2]
with open(p, "w") as f:
    f.write(json.dumps({"type": "assistant", "uuid": "u-unk", "timestamp": ts, "isSidechain": False,
        "message": {"id": "m-unk", "role": "assistant", "model": "totally-unknown-model-9000",
                     "usage": {"input_tokens": 500, "output_tokens": 200,
                               "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
                     "content": [{"type": "text", "text": "x"}]}}) + "\n")
EOF
(cd "$PROJ" && printf '{"session_id":"sess-unk","transcript_path":"%s"}' "$U3" | python3 "$SAVE")
CJ6b="$(db calls --project=alpha --json)"
check "modelo sem preço: custo 0 e listado em 'priceless'" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1])
g=[x for x in d[\"groups\"] if x[\"key\"]==\"totally-unknown-model-9000\"][0]
assert g[\"cost_usd\"]==0.0, g
assert d[\"priceless\"].get(\"totally-unknown-model-9000\")==1, d[\"priceless\"]" "$CJ6b"'
check "texto humano 'sem preço' aparece na saída não-JSON" 'db calls --project=alpha | grep -q "sem preço: 1 chamadas de totally-unknown-model-9000"'
check "rótulo 'custo equivalente de API' aparece na saída" 'db calls --project=alpha | grep -q "custo equivalente de API"'

section "7. --since 5h exclui chamada de 6h atrás"
U4="$HOME/.claude/projects/x/u4.jsonl"
TS_OLD="$(now_iso 6)"
python3 - "$U4" "$TS_OLD" <<'EOF'
import json, sys
p, ts = sys.argv[1], sys.argv[2]
with open(p, "w") as f:
    f.write(json.dumps({"type": "assistant", "uuid": "u-old", "timestamp": ts, "isSidechain": False,
        "message": {"id": "m-old-6h", "role": "assistant", "model": "claude-sonnet-4-6",
                     "usage": {"input_tokens": 1, "output_tokens": 1,
                               "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
                     "content": [{"type": "text", "text": "x"}]}}) + "\n")
EOF
(cd "$PROJ" && printf '{"session_id":"sess-old","transcript_path":"%s"}' "$U4" | python3 "$SAVE")
check "chamada de 6h atrás está no banco (sem filtro)" 'python3 -c "
import sqlite3; c=sqlite3.connect(\"$OSFORGE_DB\"); r=c.execute(\"SELECT COUNT(*) FROM calls WHERE message_id=\\\"m-old-6h\\\"\").fetchone()[0]
assert r==1, r"'
check "--since 5h EXCLUI a chamada de 6h atrás" '! (db calls --project=alpha --since=5h --json | grep -q "m-old-6h")'
check "--since 5h ainda inclui as chamadas recentes (sonnet presente)" 'db calls --project=alpha --since=5h --json | grep -q "claude-sonnet-4-6"'

section "8. prune-calls --older-than: remove só o passado; throttle diário"
N_TOTAL_BEFORE="$(python3 -c "import sqlite3; print(sqlite3.connect('$OSFORGE_DB').execute('SELECT COUNT(*) FROM calls').fetchone()[0])")"
db prune-calls --older-than=7d >/dev/null
N_AFTER_7D="$(python3 -c "import sqlite3; print(sqlite3.connect('$OSFORGE_DB').execute('SELECT COUNT(*) FROM calls').fetchone()[0])")"
check "prune 7d: remove só a chamada de 6h?? não — 6h < 7d, permanece; só remove o que é MAIS antigo" '[ "$N_TOTAL_BEFORE" = "$N_AFTER_7D" ]'
db prune-calls --older-than=0d >/dev/null
N_AFTER_0D="$(python3 -c "import sqlite3; print(sqlite3.connect('$OSFORGE_DB').execute('SELECT COUNT(*) FROM calls').fetchone()[0])")"
check "prune 0d: remove tudo (tudo é 'mais antigo que agora')" '[ "$N_AFTER_0D" -lt "$N_TOTAL_BEFORE" ]'
rm -f "$OSFORGE_CALLS_PRUNE_MARKER"
(cd "$PROJ" && printf '{"session_id":"sess-throttle-1","transcript_path":"%s"}' "$U1" | OSFORGE_CALLS_RETENTION_DAYS=0 python3 "$SAVE")
check "OSFORGE_CALLS_RETENTION_DAYS=0 desabilita a poda (sem marcador)" '[ ! -f "$OSFORGE_CALLS_PRUNE_MARKER" ]'
(cd "$PROJ" && printf '{"session_id":"sess-throttle-2","transcript_path":"%s"}' "$U1" | python3 "$SAVE")
check "poda roda e grava marcador (retention padrão)" '[ -f "$OSFORGE_CALLS_PRUNE_MARKER" ]'
MARKER_1="$(cat "$OSFORGE_CALLS_PRUNE_MARKER")"
(cd "$PROJ" && printf '{"session_id":"sess-throttle-3","transcript_path":"%s"}' "$U1" | python3 "$SAVE")
MARKER_2="$(cat "$OSFORGE_CALLS_PRUNE_MARKER")"
check "marcador não muda no mesmo dia (poda no máximo 1x/dia)" '[ "$MARKER_1" = "$MARKER_2" ]'

section "9. backfill-calls: subpastas, mesma contagem, idempotente"
BROOT="$WORK/backfill-src"; mkdir -p "$BROOT/proj-b/sub1/sub2"
BPROJ="$WORK/proj-b"; mkdir -p "$BPROJ" && (cd "$BPROJ" && $GIT init -q && echo x > f && $GIT add f && $GIT commit -qm i)
db upsert-project beta "b" standard active --root="$BPROJ" >/dev/null 2>&1
BF="$BROOT/proj-b/sub1/sub2/deep.jsonl"
TSB="$(now_iso 0)"
python3 - "$BF" "$TSB" "$BPROJ" <<'EOF'
import json, sys
p, ts, cwd = sys.argv[1], sys.argv[2], sys.argv[3]
with open(p, "w") as f:
    f.write(json.dumps({"type": "user", "cwd": cwd, "sessionId": "bf-sess", "message": {"role": "user", "content": "oi"}}) + "\n")
    for i in range(3):
        f.write(json.dumps({"type": "assistant", "uuid": f"bf-u{i}", "cwd": cwd, "sessionId": "bf-sess", "timestamp": ts, "isSidechain": False,
            "message": {"id": f"bf-m{i}", "role": "assistant", "model": "claude-haiku-4-5",
                         "usage": {"input_tokens": 5, "output_tokens": 2,
                                   "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
                         "content": [{"type": "text", "text": f"linha {i}"}]}}) + "\n")
EOF
OUT_BF1="$(db backfill-calls "$BROOT")"
check "backfill-calls varreu a subpasta profunda" 'echo "$OUT_BF1" | grep -q "1 arquivo"'
N_BETA="$(python3 -c "
import sqlite3; c=sqlite3.connect('$OSFORGE_DB')
pid=c.execute(\"SELECT id FROM projects WHERE slug='beta'\").fetchone()[0]
print(c.execute('SELECT COUNT(*) FROM calls WHERE project_id=?',(pid,)).fetchone()[0])")"
check "backfill-calls resolveu o projeto pelo cwd (beta) e importou as 3 chamadas" '[ "$N_BETA" = 3 ]'
db backfill-calls "$BROOT" >/dev/null
N_BETA_2="$(python3 -c "
import sqlite3; c=sqlite3.connect('$OSFORGE_DB')
pid=c.execute(\"SELECT id FROM projects WHERE slug='beta'\").fetchone()[0]
print(c.execute('SELECT COUNT(*) FROM calls WHERE project_id=?',(pid,)).fetchone()[0])")"
check "backfill-calls rodado 2x é idempotente (mesma contagem)" '[ "$N_BETA_2" = "$N_BETA" ]'

section "10. privacidade: nenhuma linha de calls contém texto de mensagem"
MARKER="MARCADOR_SECRETO_QUE_NAO_PODE_VAZAR_$$"
U5="$HOME/.claude/projects/x/u5.jsonl"
TS5="$(now_iso 0)"
python3 - "$U5" "$TS5" "$MARKER" <<'EOF'
import json, sys
p, ts, marker = sys.argv[1], sys.argv[2], sys.argv[3]
with open(p, "w") as f:
    f.write(json.dumps({"type": "assistant", "uuid": "u-priv", "timestamp": ts, "isSidechain": False,
        "message": {"id": "m-priv", "role": "assistant", "model": "claude-sonnet-4-6",
                     "usage": {"input_tokens": 3, "output_tokens": 3,
                               "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
                     "content": [{"type": "text", "text": marker}]}}) + "\n")
EOF
(cd "$PROJ" && printf '{"session_id":"sess-priv","transcript_path":"%s"}' "$U5" | python3 "$SAVE")
check "marcador plantado NÃO aparece em nenhuma coluna da tabela calls" '! python3 -c "
import sqlite3; c=sqlite3.connect(\"$OSFORGE_DB\")
rows = c.execute(\"SELECT * FROM calls\").fetchall()
marker = \"$MARKER\"
found = any(marker in str(v) for r in rows for v in r)
import sys; sys.exit(0 if found else 1)
"'

echo ""; echo "══ calls: $PASS ok, $FAIL falha(s)"
[ "$FAIL" -eq 0 ]
