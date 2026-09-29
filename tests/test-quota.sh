#!/usr/bin/env bash
# tests/test-quota.sh — B-027 (SPEC-L01 Parte A: guarda de janela de cota).
#
# Roda os scripts REAIS (hooks/quota-record.py, hooks/context-threshold.py,
# hooks/session-save.py) contra fixtures sintéticas, sem rede e sem API. Casos do spec
# (docs/intake/laya/SPEC-L01-guarda-de-cota.md), 1 a 5 e 9 — 6 a 8 são do harness de evals
# (Parte B, outro item):
#   1. gravador: statusline com five_hour.used_percentage=83 → quota.json com pct/resets_at;
#      stdout vazio; exit 0
#   2. gravador: rate_limits ausente, null, JSON inválido → arquivo anterior intacto; exit 0
#   3. aviso: faixas 79/80/95 → 0/1/2 avisos; repetir 95 na mesma janela → nenhum; nova
#      resets_at → avisa de novo; sessão diferente na mesma janela → não avisa de novo
#   4. aviso: `at` de 20 min atrás → silêncio; `resets_at` no passado → silêncio;
#      OSFORGE_QUOTA_THRESHOLD=off → silêncio
#   5. rejeição: transcript com linha no formato de EV-C04 → Stop grava `rejected`; o
#      próximo UserPromptSubmit depois do reset avisa uma vez, e não repete
#   9. gravador: stdin de ~1 MB processado em < 20 ms
# Offline. Uso: tests/test-quota.sh
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
unset OSFORGE_PROJECT OSFORGE_QUOTA_THRESHOLD OSFORGE_QUOTA_BANDS OSFORGE_QUOTA_FILE OSFORGE_CONTEXT_THRESHOLD
REC="$REPO/hooks/quota-record.py"
CT="$REPO/hooks/context-threshold.py"
SAVE="$REPO/hooks/session-save.py"
NOW="$(python3 -c 'import time; print(int(time.time()))')"

# quota_file <path> <at_epoch> <pct|"" > <resets_at_epoch> [rejected_type] [rejected_resets_epoch]
# Writes a raw osforge.quota.v1 record with full control over `at`/`resets_at`, so band/window
# tracking can be tested deterministically (the recorder itself always uses "now").
quota_file(){
  python3 - "$@" <<'EOF'
import json, sys
path, at, pct, resets_at = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
rej_type = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] else None
rej_reset = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] else None
d = {"schema": "osforge.quota.v1", "at": at, "source": "statusline"}
if pct != "":
    d["five_hour"] = {"pct": float(pct), "resets_at": float(resets_at)}
if rej_type:
    d["rejected"] = {"type": rej_type, "resets_at": float(rej_reset), "at": at}
with open(path, "w", encoding="utf-8") as f:
    json.dump(d, f)
EOF
}
ctx_of(){ python3 -c "import json,sys; print(json.loads(sys.argv[1])['hookSpecificOutput']['additionalContext'])" "$1" 2>/dev/null; }
# read_state_json <quota_file> <now_epoch> <out_file> → writes hooks/lib/quota.py's read_state()
# result as JSON to <out_file> (the literal `null` when it returns None). A file, not a captured
# stdout string, because the result can itself contain double quotes that would break the
# check() one-liners below if inlined as a shell string.
read_state_json(){
  OSFORGE_QUOTA_FILE="$1" python3 - "$REPO/hooks/lib" "$2" "$3" <<'EOF'
import sys, json
sys.path.insert(0, sys.argv[1])
import quota
state = quota.read_state(float(sys.argv[2]))
with open(sys.argv[3], "w", encoding="utf-8") as f:
    json.dump(state, f)
EOF
}
run_ct(){ # run_ct <session_id> <quota_file> → $OUT $RC
  OUT="$(printf '{"session_id":"%s","prompt":"oi"}' "$1" | OSFORGE_QUOTA_FILE="$2" python3 "$CT" 2>/dev/null)"; RC=$?
}

section "1. gravador: statusline → quota.json"
Q1="$WORK/quota1.json"
R1=$((NOW + 3600))
IN1="$(printf '{"rate_limits":{"five_hour":{"used_percentage":83,"resets_at":%d},"seven_day":{"used_percentage":41,"resets_at":%d}}}' "$R1" "$((NOW + 500000))")"
OUT="$(printf '%s' "$IN1" | OSFORGE_QUOTA_FILE="$Q1" python3 "$REC")"; RC=$?
check "stdout vazio" '[ -z "$OUT" ]'
check "exit 0" '[ $RC -eq 0 ]'
check "quota.json gravado com pct=83 e resets_at" "python3 -c \"
import json
d = json.load(open('$Q1'))
assert d['schema'] == 'osforge.quota.v1', d
assert d['five_hour']['pct'] == 83, d
assert d['five_hour']['resets_at'] == $R1, d
assert d['seven_day']['pct'] == 41, d
\""

section "2. gravador: dado ausente/inválido → arquivo anterior intacto"
Q2="$WORK/quota2.json"
printf '%s' "$IN1" | OSFORGE_QUOTA_FILE="$Q2" python3 "$REC" >/dev/null
BASE="$(cat "$Q2")"
OUT="$(printf '{"foo":"bar"}' | OSFORGE_QUOTA_FILE="$Q2" python3 "$REC")"; RC=$?
check "sem rate_limits: stdout vazio, exit 0" '[ -z "$OUT" ] && [ $RC -eq 0 ]'
check "sem rate_limits: arquivo intacto" '[ "$(cat "$Q2")" = "$BASE" ]'
OUT="$(printf '{"rate_limits":null}' | OSFORGE_QUOTA_FILE="$Q2" python3 "$REC")"; RC=$?
check "rate_limits null: stdout vazio, exit 0" '[ -z "$OUT" ] && [ $RC -eq 0 ]'
check "rate_limits null: arquivo intacto" '[ "$(cat "$Q2")" = "$BASE" ]'
OUT="$(printf 'not json {{{' | OSFORGE_QUOTA_FILE="$Q2" python3 "$REC")"; RC=$?
check "JSON inválido: stdout vazio, exit 0" '[ -z "$OUT" ] && [ $RC -eq 0 ]'
check "JSON inválido: arquivo intacto" '[ "$(cat "$Q2")" = "$BASE" ]'

section "3. aviso: faixas e janela (resets_at)"
Q3="$WORK/quota3.json"
RA=$((NOW + 3600))
quota_file "$Q3" "$NOW" 79 "$RA"
run_ct s1 "$Q3"; check "79% (abaixo da faixa 1) → nenhum aviso" '[ -z "$OUT" ]'
quota_file "$Q3" "$NOW" 80 "$RA"
run_ct s1 "$Q3"; check "80% → aviso da faixa 1" 'ctx_of "$OUT" | grep -q "Janela de 5h em 80%"'
quota_file "$Q3" "$NOW" 95 "$RA"
run_ct s1 "$Q3"; check "95% na mesma janela → 2º aviso (faixa 2, PARE)" 'ctx_of "$OUT" | grep -q "PARE"'
quota_file "$Q3" "$NOW" 95 "$RA"
run_ct s1 "$Q3"; check "repetir 95% na mesma janela → nenhum aviso novo" '[ -z "$OUT" ]'
RB=$((NOW + 10800))
quota_file "$Q3" "$NOW" 95 "$RB"
run_ct s1 "$Q3"; check "nova resets_at (nova janela) → avisa de novo" 'ctx_of "$OUT" | grep -q "PARE"'
quota_file "$Q3" "$NOW" 95 "$RB"
run_ct s2 "$Q3"; check "sessão diferente, mesma janela → não avisa de novo" '[ -z "$OUT" ]'

section "4. aviso: silêncio (stale / janela passada / kill-switch)"
Q4A="$WORK/quota4a.json"
quota_file "$Q4A" "$((NOW - 1200))" 95 "$((NOW + 3600))"
run_ct s1 "$Q4A"; check "\`at\` de 20 min atrás → silêncio" '[ -z "$OUT" ]'
Q4B="$WORK/quota4b.json"
quota_file "$Q4B" "$NOW" 95 "$((NOW - 60))"
run_ct s1 "$Q4B"; check "\`resets_at\` no passado → silêncio" '[ -z "$OUT" ]'
Q4C="$WORK/quota4c.json"
quota_file "$Q4C" "$NOW" 95 "$((NOW + 3600))"
OUT="$(printf '{"session_id":"s1","prompt":"oi"}' | OSFORGE_QUOTA_FILE="$Q4C" OSFORGE_QUOTA_THRESHOLD=off python3 "$CT")"
check "OSFORGE_QUOTA_THRESHOLD=off → silêncio" '[ -z "$OUT" ]'

section "5. rejeição pelo transcript (EV-C04) → aviso após o reset"
TR="$HOME/.claude/projects/x/rejected.jsonl"
RR=$((NOW - 2))
python3 - "$TR" "$RR" <<EOF
import json
path, r = "$TR", $RR
with open(path, "w", encoding="utf-8") as f:
    f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "trabalhando"}}) + "\n")
    f.write(json.dumps({
        "type": "assistant", "uuid": "u-rej",
        "message": {"id": "m-rej", "role": "assistant", "model": "<synthetic>",
                    "usage": {"input_tokens": 0, "output_tokens": 0,
                              "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
                    "content": [{"type": "text", "text": ""}]},
        "isApiErrorMessage": True, "error": "rate_limit",
        "quotaLimits": {"status": "rejected", "rateLimitType": "five_hour", "resetsAt": r,
                         "overageStatus": "rejected", "overageDisabledReason": "org_level_disabled"},
    }) + "\n")
EOF
Q5="$WORK/quota5.json"
OUT="$(printf '{"session_id":"s-rej","transcript_path":"%s"}' "$TR" | OSFORGE_QUOTA_FILE="$Q5" python3 "$SAVE")"; RC=$?
check "Stop: stdout vazio, exit 0" '[ -z "$OUT" ] && [ $RC -eq 0 ]'
check "Stop: quota.json ganha \`rejected\`" "python3 -c \"
import json
d = json.load(open('$Q5'))
assert d['rejected']['type'] == 'five_hour', d
assert d['rejected']['resets_at'] == $RR, d
assert d.get('source') == 'transcript', d
\""
run_ct s-after "$Q5"
check "próximo UserPromptSubmit depois do reset avisa uma vez" 'ctx_of "$OUT" | grep -q "rejeitada"'
run_ct s-after2 "$Q5"
check "aviso de rejeição não repete" '[ -z "$OUT" ]'

section "9. gravador: custo de stdin ~1 MB"
Q9="$WORK/quota9.json"
MS="$(python3 - "$REPO/hooks" "$REC" "$Q9" <<'EOF'
import sys, time, json, io, os, importlib.util
hooks_dir, rec_path, qpath = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(hooks_dir, "lib"))
os.environ["OSFORGE_QUOTA_FILE"] = qpath
spec = importlib.util.spec_from_file_location("quota_record", rec_path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
payload = json.dumps({"rate_limits": {"five_hour": {"used_percentage": 83, "resets_at": 1790012345}},
                       "pad": "x" * (1000 * 1000)})
assert len(payload) < 1024 * 1024, len(payload)
old_stdin = sys.stdin
sys.stdin = io.StringIO(payload)
t0 = time.perf_counter()
try:
    m.main()
finally:
    sys.stdin = old_stdin
dt = (time.perf_counter() - t0) * 1000
print(int(dt))
EOF
)"
check "stdin de ~1 MB processado em < 20 ms (levou ${MS} ms)" '[ "$MS" -ge 0 ] && [ "$MS" -lt 20 ]'
check "e o registro foi gravado corretamente" "python3 -c \"
import json
d = json.load(open('$Q9'))
assert d['five_hour']['pct'] == 83, d
\""
OUT="$(python3 -c "print('x' * (1024*1024 + 100))" | OSFORGE_QUOTA_FILE="$WORK/quota9b.json" python3 "$REC")"; RC=$?
check "stdin acima do teto (1 MB): ainda assim exit 0 e silencioso" '[ -z "$OUT" ] && [ $RC -eq 0 ]'

section "10. read_state: \`rejected\` sobrevive ao stale gate (gap do item 4, B-026)"
# Known limitation documented in hooks/lib/quota.py: the uniform staleness gate on \`at\` used
# to blind BOTH the A3 warning and the eval harness's B3 preflight to a still-relevant
# \`rejected\` whenever nothing refreshed quota.json for 15+ minutes. \`rejected\` must survive
# on its own; stale usage numbers (\`five_hour\`) must not.
Q10="$WORK/quota10.json"
S10="$WORK/state10.json"
FUTURE_RESET=$((NOW + 300))
quota_file "$Q10" "$((NOW - 1200))" 95 "$((NOW + 3600))" "five_hour" "$FUTURE_RESET"
read_state_json "$Q10" "$NOW" "$S10"
check "\`at\` de 20 min atrás mas \`rejected\` com reset no futuro: read_state não retorna None" "python3 -c \"
import json
assert json.load(open('$S10')) is not None
\""
check "rejected.resets_at preservado" "python3 -c \"
import json
d = json.load(open('$S10'))
assert d['rejected']['resets_at'] == $FUTURE_RESET, d
\""
check "five_hour (uso, stale) não é exposto pelo estado exemptado" "python3 -c \"
import json
d = json.load(open('$S10'))
assert 'five_hour' not in d, d
\""

Q10B="$WORK/quota10b.json"
S10B="$WORK/state10b.json"
quota_file "$Q10B" "$((NOW - 1200))" 95 "$((NOW + 3600))"
read_state_json "$Q10B" "$NOW" "$S10B"
check "\`at\` stale e sem \`rejected\`: read_state ainda retorna None (sem regressão)" "python3 -c \"
import json
assert json.load(open('$S10B')) is None
\""

Q10C="$WORK/quota10c.json"
S10C="$WORK/state10c.json"
quota_file "$Q10C" "$NOW" 95 "$((NOW + 3600))" "five_hour" "$FUTURE_RESET"
read_state_json "$Q10C" "$NOW" "$S10C"
check "registro fresco: five_hour e rejected presentes normalmente" "python3 -c \"
import json
d = json.load(open('$S10C'))
assert d['five_hour']['pct'] == 95, d
assert d['rejected']['resets_at'] == $FUTURE_RESET, d
\""

echo ""; echo "══ quota: $PASS ok, $FAIL falha(s)"
[ "$FAIL" -eq 0 ]
