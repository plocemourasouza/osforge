#!/usr/bin/env bash
# =============================================================================
# test-harness-quota.sh -- spec cases 6-8 of SPEC-L01 Part B (B-026)
# =============================================================================
#
# 6. scripts/lib/stream_assert.py run-status: a table of ok/quota/error streams,
#    exercised directly (no subprocess, no fake claude needed).
# 7. scripts/test-skill-triggering.sh with a fake `claude` on PATH that replays
#    a rejected stream on the 2nd case: case 1 PASS, case 2+ NOT RUN, exit 75,
#    no FLAKY/FAIL anywhere in the case JSON.
# 8. Same harness with quota.json already at 90% (fresh, no rejection): no case
#    starts, exit 75; with --ignore-quota, the same quota.json is ignored and
#    the suite runs to completion.
#
# Never calls the real `claude` -- a fake one (tests/fixtures/fake-claude.py,
# see below) is put first on PATH, controlled entirely by env vars.
# =============================================================================
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HARNESS="$REPO/scripts/test-skill-triggering.sh"
STREAM_ASSERT="$REPO/scripts/lib/stream_assert.py"

PASS=0
FAIL=0

ok() { PASS=$((PASS + 1)); echo "  ok   $1"; }
bad() { FAIL=$((FAIL + 1)); echo "  FAIL $1${2:+  -- $2}"; }
check() { if [ "$2" = "1" ]; then ok "$1"; else bad "$1" "${3:-}"; fi; }

section() { echo ""; echo "-- $1"; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# ── fake `claude` on PATH ────────────────────────────────────────────────────
# Call N (1-based, across the whole harness run -- OSFORGE_TEST_RUNS=1 in every
# case below, so call N == case N): if OSFORGE_FAKE_REJECT_AT matches, emits a
# rejected stream and exits 1; otherwise emits a Skill tool_use for whatever the
# `-p` prompt says (the fixture cases below use skill_name AS the prompt, so the
# fake claude just echoes it back as the triggered skill) and exits 0.
FAKE_BIN="$WORK/bin"
mkdir -p "$FAKE_BIN"
cat > "$FAKE_BIN/claude" <<'PYEOF'
#!/usr/bin/env python3
import json
import os
import sys

counter_file = os.environ["OSFORGE_FAKE_COUNTER_FILE"]
with open(counter_file, "a", encoding="utf-8") as fh:
    fh.write("x")
with open(counter_file, encoding="utf-8") as fh:
    call_n = len(fh.read())

prompt = ""
argv = sys.argv[1:]
if "-p" in argv:
    prompt = argv[argv.index("-p") + 1]

reject_at = os.environ.get("OSFORGE_FAKE_REJECT_AT")


def emit(evt):
    sys.stdout.write(json.dumps(evt) + "\n")


emit({"type": "system", "subtype": "init", "tools": ["Skill"], "mcp_servers": []})

if reject_at and call_n == int(reject_at):
    emit({"type": "assistant", "message": {"role": "assistant",
          "content": [{"type": "text", "text": "hit a rate limit"}]}})
    emit({"type": "rate_limit_event",
          "rate_limit_info": {"status": "rejected", "resetsAt": 9999999999,
                               "rateLimitType": "five_hour"}})
    emit({"type": "result", "is_error": True, "result": "rate_limit_error",
          "usage": {"input_tokens": 10, "output_tokens": 1,
                     "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}})
    sys.exit(1)

emit({"type": "assistant", "message": {"role": "assistant",
      "content": [{"type": "tool_use", "id": "t1", "name": "Skill",
                    "input": {"skill": prompt}}]}})
emit({"type": "result", "is_error": False, "result": "ok",
      "usage": {"input_tokens": 10, "output_tokens": 1,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}})
sys.exit(0)
PYEOF
chmod +x "$FAKE_BIN/claude"

# Three real skill directories (so skill_rel_path()/is_core_skill() resolve),
# used as BOTH skill name and prompt -- the fake claude just echoes -p back.
CASES_FILE="$WORK/cases.tsv"
printf 'architecture\tarchitecture\napi-patterns\tapi-patterns\ndatabase-design\tdatabase-design\n' > "$CASES_FILE"

run_harness() {
    # run_harness <quota_file_or_empty> [extra harness args...]
    local quota_file="$1"; shift
    local counter="$WORK/counter-$$-$RANDOM"
    : > "$counter"
    env \
        PATH="$FAKE_BIN:$PATH" \
        OSFORGE_FAKE_COUNTER_FILE="$counter" \
        OSFORGE_QUOTA_FILE="${quota_file:-$WORK/no-such-quota.json}" \
        "$HARNESS" --model fake-model --runs 1 --cases "$CASES_FILE" "$@"
}

# ── 6. stream_assert.py run-status: table -----------------------------------
section "6. stream_assert.py run-status (B1)"

mk_stream() {
    # mk_stream <file> <event-json-lines...>
    local f="$1"; shift
    printf '%s\n' "$@" > "$f"
}

S_OK="$WORK/s-ok.jsonl"
mk_stream "$S_OK" \
    '{"type":"result","is_error":false,"result":"done"}'
check "result sem is_error -> ok" \
    "$([ "$(python3 "$STREAM_ASSERT" run-status "$S_OK")" = "ok" ] && echo 1 || echo 0)" 1

S_ALLOWED="$WORK/s-allowed.jsonl"
mk_stream "$S_ALLOWED" \
    '{"type":"rate_limit_event","rate_limit_info":{"status":"allowed"}}' \
    '{"type":"result","is_error":false,"result":"done"}'
check "is_error false + rate_limit allowed -> ok" \
    "$([ "$(python3 "$STREAM_ASSERT" run-status "$S_ALLOWED")" = "ok" ] && echo 1 || echo 0)" 1

S_QUOTA_RL="$WORK/s-quota-rl.jsonl"
mk_stream "$S_QUOTA_RL" \
    '{"type":"rate_limit_event","rate_limit_info":{"status":"rejected","resetsAt":123}}' \
    '{"type":"result","is_error":true,"result":"boom"}'
check "is_error + rate_limit rejected -> quota" \
    "$([ "$(python3 "$STREAM_ASSERT" run-status "$S_QUOTA_RL")" = "quota" ] && echo 1 || echo 0)" 1

S_QUOTA_TXT="$WORK/s-quota-txt.jsonl"
mk_stream "$S_QUOTA_TXT" \
    '{"type":"result","is_error":true,"result":"You have exceeded your usage limit"}'
check "is_error + texto de limite, sem rate_limit_event -> quota" \
    "$([ "$(python3 "$STREAM_ASSERT" run-status "$S_QUOTA_TXT")" = "quota" ] && echo 1 || echo 0)" 1

S_ERROR="$WORK/s-error.jsonl"
mk_stream "$S_ERROR" \
    '{"type":"result","is_error":true,"result":"some other tool failure"}'
check "is_error sem cota -> error" \
    "$([ "$(python3 "$STREAM_ASSERT" run-status "$S_ERROR")" = "error" ] && echo 1 || echo 0)" 1

S_NONE="$WORK/s-none.jsonl"
: > "$S_NONE"
check "sem evento result -> ok (ausência de evidência não é cota)" \
    "$([ "$(python3 "$STREAM_ASSERT" run-status "$S_NONE")" = "ok" ] && echo 1 || echo 0)" 1

# ── 7. mid-run rejection aborts the batch ------------------------------------
section "7. harness: rejeição no 2o caso -> caso 1 PASS, resto NOT RUN, exit 75"

OUT7="$WORK/out7.txt"
set +e
OSFORGE_FAKE_REJECT_AT=2 run_harness "" > "$OUT7" 2>&1
EXIT7=$?
set -e

check "exit code 75 (EX_TEMPFAIL)" "$([ "$EXIT7" = "75" ] && echo 1 || echo 0)" "got $EXIT7"

CASES_JSON7="$(ls -d /tmp/osforge-skill-tests/*/ 2>/dev/null | sort | tail -1)cases.json"
if [ -f "$CASES_JSON7" ]; then
    VERDICTS7="$(python3 -c '
import json, sys
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.strip()
    if line:
        d = json.loads(line)
        print(d["id"], d["verdict"])
' "$CASES_JSON7")"
    V1="$(echo "$VERDICTS7" | awk '$1=="architecture"{print $2}')"
    V2="$(echo "$VERDICTS7" | awk '$1=="api-patterns"{print $2}')"
    V3="$(echo "$VERDICTS7" | awk '$1=="database-design"{print $2}')"
    check "caso 1 (architecture) = PASS" "$([ "$V1" = "PASS" ] && echo 1 || echo 0)" "got '$V1'"
    check "caso 2 (api-patterns, onde a rejeição bateu) = NOT RUN" "$([ "$V2" = "NOT" ] && echo 1 || echo 0)" "got '$V2 ...' (linha: $(echo "$VERDICTS7" | grep api-patterns))"
    check "caso 3 (database-design, nunca rodou) = NOT RUN" "$([ "$V3" = "NOT" ] && echo 1 || echo 0)" "got '$V3 ...' (linha: $(echo "$VERDICTS7" | grep database-design))"
    NO_BAD="$(echo "$VERDICTS7" | grep -Ec 'FLAKY|FAIL' || true)"
    check "nenhum FLAKY/FAIL no relatório" "$([ "$NO_BAD" = "0" ] && echo 1 || echo 0)" "encontrado: $(echo "$VERDICTS7" | grep -E 'FLAKY|FAIL')"
else
    bad "cases.json do caso 7 encontrado" "não achei em /tmp/osforge-skill-tests -- $CASES_JSON7"
    bad "(pulando os 3 checks de veredito por caso)"
    bad "(pulando o check de FLAKY/FAIL)"
fi

# ── 8. preflight stop + --ignore-quota ---------------------------------------
section "8. preflight: quota.json em 90% para o lote antes de iniciar"

QUOTA90="$WORK/quota-90.json"
python3 -c '
import json, sys, time
json.dump({"schema": "osforge.quota.v1", "at": time.time(), "source": "statusline",
           "five_hour": {"pct": 90.0, "resets_at": time.time() + 3600},
           "seven_day": {"pct": 10.0, "resets_at": time.time() + 500000},
           "rejected": None}, open(sys.argv[1], "w", encoding="utf-8"))
' "$QUOTA90"

OUT8="$WORK/out8.txt"
set +e
run_harness "$QUOTA90" > "$OUT8" 2>&1
EXIT8=$?
set -e

check "exit code 75 (preflight parou antes de qualquer caso)" "$([ "$EXIT8" = "75" ] && echo 1 || echo 0)" "got $EXIT8"
check "nenhum caso rodou (0 PASS/FLAKY/FAIL no output)" \
    "$(grep -Eq '^  PASS   : 0' "$OUT8" && echo 1 || echo 0)" "$(grep '^  PASS' "$OUT8" || echo '(sem linha PASS)')"

section "8b. --ignore-quota ignora o mesmo quota.json em 90%"

OUT8B="$WORK/out8b.txt"
set +e
run_harness "$QUOTA90" --ignore-quota > "$OUT8B" 2>&1
EXIT8B=$?
set -e

check "exit 0 (rodou normalmente, ignorando a cota)" "$([ "$EXIT8B" = "0" ] && echo 1 || echo 0)" "got $EXIT8B"
check "3 PASS (todos os casos rodaram)" \
    "$(grep -Eq '^  PASS   : 3' "$OUT8B" && echo 1 || echo 0)" "$(grep '^  PASS' "$OUT8B" || echo '(sem linha PASS)')"

echo ""
echo "══ quota harness (B-026, spec cases 6-8): $PASS ok, $FAIL falha(s) ══"
[ "$FAIL" = "0" ]
