#!/usr/bin/env bash
# tests/test-context-usage.sh — B-021 (aviso de contexto pelo uso real) e B-022 (tokens por sessão/projeto).
#
# Transcripts sintéticos com `message.usage` reais de formato; hooks reais; osforge-db real
# em banco temporário. Verifica por execução:
#   1. contexto de 100k / 125k / 155k → 0 / 1 / 2 avisos (um por faixa por sessão)
#   2. a mesma faixa não avisa duas vezes; outra sessão avisa de novo; faixa maior avisa uma vez
#   3. transcript de 30 MB → aviso correto em < 40 ms de leitura (lê só o fim)
#   4. transcript fora de ~/.claude → silêncio; kill-switch → silêncio; payload inválido → exit 0
#   5. session-save: mesma message.id em duas linhas conta uma vez; tokens separados por modelo
#   6. `usage <slug>`, `board` e `stats` mostram o total do projeto; Stop repetido não duplica
# Offline. Uso: tests/test-context-usage.sh
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }

export HOME="$WORK/home"; mkdir -p "$HOME/.claude/projects/x"
export OSFORGE_DB="$WORK/db.sqlite" OSFORGE_LOG_DIR="$WORK/logs" OSFORGE_CONTEXT_STATE_DIR="$WORK/ctx"
unset OSFORGE_PROJECT OSFORGE_CONTEXT_THRESHOLD OSFORGE_CONTEXT_BANDS
CT="$REPO/hooks/context-threshold.py"; SAVE="$REPO/hooks/session-save.py"
db(){ python3 "$REPO/scripts/osforge-db.py" "$@"; }

transcript(){ # transcript <path> <context_tokens> [pad_lines]  — última resposta com esse contexto
  python3 - "$1" "$2" "${3:-5}" <<'EOF'
import json, sys
p, ctx, pad = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
with open(p, "w") as f:
    for i in range(pad):
        f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "x" * 200}}) + "\n")
        f.write(json.dumps({"type": "assistant", "uuid": f"u{i}", "message": {"id": f"m{i}", "role": "assistant", "model": "claude-opus-4",
                 "usage": {"input_tokens": 100, "cache_read_input_tokens": 1000, "cache_creation_input_tokens": 0, "output_tokens": 50},
                 "content": [{"type": "text", "text": "ok"}]}}) + "\n")
    f.write(json.dumps({"type": "assistant", "uuid": "last", "message": {"id": "mlast", "role": "assistant", "model": "claude-opus-4",
             "usage": {"input_tokens": 2000, "cache_read_input_tokens": ctx - 2500, "cache_creation_input_tokens": 500, "output_tokens": 80},
             "content": [{"type": "text", "text": "fim"}]}}) + "\n")
EOF
}
run_ct(){ # run_ct <transcript> <session> → $OUT $RC
  OUT="$(printf '{"session_id":"%s","transcript_path":"%s","prompt":"oi"}' "$2" "$1" | python3 "$CT" 2>/dev/null)"; RC=$?
}
ctx_of(){ python3 -c "import json,sys; print(json.loads(sys.argv[1])['hookSpecificOutput']['additionalContext'])" "$1" 2>/dev/null; }

section "context-threshold: faixas"
T="$HOME/.claude/projects/x/t.jsonl"
transcript "$T" 100000; run_ct "$T" s1; check "100k → sem aviso" '[ $RC -eq 0 ] && [ -z "$OUT" ]'
transcript "$T" 125000; run_ct "$T" s1; check "125k → aviso da faixa 1 (salvar estado)" 'ctx_of "$OUT" | grep -q "125,000 tokens (faixa 120–150k"'
run_ct "$T" s1; check "125k de novo, mesma sessão → sem aviso repetido" '[ -z "$OUT" ]'
run_ct "$T" s2; check "outra sessão → avisa" 'ctx_of "$OUT" | grep -q "faixa 120–150k"'
transcript "$T" 155000; run_ct "$T" s1; check "155k → aviso da faixa 2 (PARE)" 'ctx_of "$OUT" | grep -q "155,000 tokens (>150k, dumb zone): PARE"'
run_ct "$T" s1; check "155k de novo → sem aviso" '[ -z "$OUT" ]'
transcript "$T" 130000; run_ct "$T" s1; check "voltou para a faixa 1 depois da 2 → sem aviso (já passou por faixa maior)" '[ -z "$OUT" ]'
transcript "$T" 155000; run_ct "$T" s3; N="$(ctx_of "$OUT" | grep -c PARE)"; check "sessão nova direto em 155k → um único aviso (faixa 2)" '[ "$N" = 1 ]'
check "hook mede o contexto da ÚLTIMA resposta (input+cache_read+cache_create)" '[ "$(python3 -c "
import sys; sys.path.insert(0, sys.argv[1]); import importlib.util
spec = importlib.util.spec_from_file_location(\"ct\", sys.argv[2]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.last_context_tokens(sys.argv[3]))" "$REPO/hooks" "$CT" "$T")" = 155000 ]'

section "context-threshold: custo e guardas"
BIG="$HOME/.claude/projects/x/big.jsonl"; transcript "$BIG" 155000 60000
SZ="$(stat -c %s "$BIG" 2>/dev/null || stat -f %z "$BIG")"
check "transcript grande (≥ 25 MB) gerado" '[ "$SZ" -ge 25000000 ]'
MS="$(python3 - "$REPO/hooks" "$CT" "$BIG" <<'EOF'
import sys, time, importlib.util
spec = importlib.util.spec_from_file_location("ct", sys.argv[2]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t = time.perf_counter(); n = m.last_context_tokens(sys.argv[3]); dt = (time.perf_counter() - t) * 1000
print(int(dt) if n == 155000 else -1)
EOF
)"
check "leitura do fim do transcript de 30 MB em < 40 ms (levou ${MS} ms)" '[ "$MS" -ge 0 ] && [ "$MS" -lt 40 ]'
run_ct "$BIG" s9; check "…e o hook avisa" 'ctx_of "$OUT" | grep -q PARE'
cp "$T" "$WORK/fora.jsonl"; run_ct "$WORK/fora.jsonl" s4; check "transcript fora de ~/.claude → silêncio" '[ -z "$OUT" ]'
OUT="$(printf '{"session_id":"s5","transcript_path":"%s"}' "$T" | OSFORGE_CONTEXT_THRESHOLD=off python3 "$CT")"; check "kill-switch → silêncio" '[ -z "$OUT" ]'
OUT="$(printf '{"session_id":"s6","transcript_path":"%s"}' "$T" | OSFORGE_CONTEXT_BANDS=100000,140000 python3 "$CT")"; check "faixas configuráveis (100k,140k → 155k é faixa 2)" 'ctx_of "$OUT" | grep -q PARE'
OUT="$(echo 'not json' | python3 "$CT")"; RC=$?; check "payload inválido → exit 0, silêncio" '[ $RC -eq 0 ] && [ -z "$OUT" ]'
OUT="$(echo '{"transcript_path":"/nonexistent/x.jsonl"}' | python3 "$CT")"; RC=$?; check "transcript ausente → silêncio" '[ $RC -eq 0 ] && [ -z "$OUT" ]'
printf 'garbage\n{"message":{"role":"assistant","usage":"nope"}}\n' > "$HOME/.claude/projects/x/bad.jsonl"
run_ct "$HOME/.claude/projects/x/bad.jsonl" s7; check "usage malformado → silêncio" '[ $RC -eq 0 ] && [ -z "$OUT" ]'

section "session-save: tokens por sessão e modelo (B-022)"
GIT="git -c user.name=t -c user.email=t@t -c init.defaultBranch=main -c commit.gpgsign=false"
PROJ="$WORK/proj"; mkdir -p "$PROJ" && (cd "$PROJ" && $GIT init -q && echo x > f && $GIT add f && $GIT commit -qm i)
db upsert-project alpha "a" standard active --root="$PROJ" >/dev/null 2>&1
U="$HOME/.claude/projects/x/usage.jsonl"
python3 - "$U" <<'EOF'
import json, sys
def a(mid, model, inp, out, cr, cc, text):
    return json.dumps({"type": "assistant", "message": {"id": mid, "role": "assistant", "model": model,
            "usage": {"input_tokens": inp, "output_tokens": out, "cache_read_input_tokens": cr, "cache_creation_input_tokens": cc},
            "content": [{"type": "text", "text": text}]}})
with open(sys.argv[1], "w") as f:
    f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "primeira tarefa"}}) + "\n")
    f.write(a("m1", "claude-opus-4", 1000, 100, 50000, 0, "bloco 1") + "\n")
    f.write(a("m1", "claude-opus-4", 1000, 100, 50000, 0, "bloco 2 — MESMA mensagem, outra linha") + "\n")
    f.write(a("m2", "claude-haiku-4", 10, 5, 0, 0, "subagente") + "\n")
    f.write(a("m3", "claude-opus-4", 2000, 300, 60000, 500, "fim") + "\n")
    f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "última"}}) + "\n")
EOF
(cd "$PROJ" && printf '{"session_id":"sess-A","transcript_path":"%s"}' "$U" | python3 "$SAVE"); RC=$?
J="$(db usage alpha --json)"
check "exit 0 e uso gravado" '[ $RC -eq 0 ] && [ -n "$J" ]'
check "mesma message.id em duas linhas conta UMA vez (opus in=3000, não 4000)" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1]); o=[s for s in d[\"sessions\"] if s[\"model\"]==\"claude-opus-4\"][0]
assert (o[\"input_tokens\"],o[\"output_tokens\"],o[\"cache_read\"],o[\"cache_create\"],o[\"turns\"])==(3000,400,110000,500,2), o" "$J"'
check "modelos separados (haiku à parte)" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1]); h=[s for s in d[\"sessions\"] if s[\"model\"]==\"claude-haiku-4\"][0]; assert h[\"input_tokens\"]==10 and h[\"turns\"]==1" "$J"'
check "total do projeto = soma de tudo" 'python3 -c "
import json,sys; d=json.loads(sys.argv[1]); assert d[\"totals\"][\"total\"]==3000+400+110000+500+10+5, d[\"totals\"]" "$J"'
(cd "$PROJ" && printf '{"session_id":"sess-A","transcript_path":"%s"}' "$U" | python3 "$SAVE")
check "Stop repetido na mesma sessão não duplica (upsert)" '[ "$(db usage alpha --json | python3 -c "import json,sys; print(json.load(sys.stdin)[\"totals\"][\"total\"])")" = 113915 ]'
check "board mostra o total do projeto" 'db board | grep -q "alpha: sem tasks  (113,915 tokens em 1 sessão(ões))"'
check "stats mostra o total" 'db stats | grep -q "Tokens: 113,915 em 1 sessão(ões)"'
(cd "$PROJ" && printf '{"session_id":"sess-B","transcript_path":"%s"}' "$U" | python3 "$SAVE")
check "outra sessão soma" 'db usage alpha | grep -q "total: 227,830 tokens em 2 sessão(ões)"'
check "resume também foi gravado no mesmo Stop" 'db resume alpha | grep -q "última"'

echo ""; echo "══ context-usage: $PASS ok, $FAIL falha(s)"
[ "$FAIL" -eq 0 ]
