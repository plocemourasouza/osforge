#!/usr/bin/env bash
# =============================================================================
# test-route-guard-race.sh — route-guard must not judge a turn it cannot see yet
# =============================================================================
#
# Measured on 2026-10-08 (DeskcommCRM session 9a72c8e2): the Stop hook fired
# 79–87 ms after the final assistant text entry was timestamped, read the
# transcript before that entry reached disk, and blocked replies whose FIRST
# line was the route line. Replaying the same transcript with the entry present
# → allow; without it → block. Every reply whose route line lived only in the
# final text block (after tool calls) was blocked.
#
# Offline. A writer appends the final entry AFTER the hook has started reading.
# =============================================================================
set -u
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK="$REPO/hooks/route-guard.py"
PASS=0; FAIL=0
ok()   { echo "  ✓ $1"; PASS=$((PASS + 1)); }
bad()  { echo "  ✗ $1"; FAIL=$((FAIL + 1)); }

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
TR="$WORK/t.jsonl"
FINAL='{"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "🤖 route: @debugger · skill: none · model: sonnet\n\nFeito."}]}}'

seed() {
  cat > "$TR" <<'JSONL'
{"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": "corrige o off-by-one"}]}}
{"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "name": "Edit", "input": {"file_path": "src/x.ts"}}]}}
{"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "ok"}]}}
JSONL
}
payload() { printf '{"hook_event_name":"Stop","stop_hook_active":false,"transcript_path":"%s"}' "$TR"; }

echo "── 1. final entry lands after the hook started → allow"
seed
( sleep 0.15; printf '%s\n' "$FINAL" >> "$TR" ) &
out="$(payload | python3 "$HOOK")"; wait
[ -z "$out" ] && ok "late final entry is seen (no block)" || bad "blocked a turn whose route line arrived late: $out"

echo "── 2. final entry never lands → still blocks, and promptly"
seed
start=$(python3 -c 'import time;print(time.time())')
out="$(payload | python3 "$HOOK")"
elapsed=$(python3 -c "import time;print(round(time.time()-$start,2))")
printf '%s' "$out" | grep -q '"decision": "block"' && ok "missing route line still blocks" || bad "missing route line no longer blocks: $out"
python3 -c "import sys; sys.exit(0 if $elapsed < 2.0 else 1)" && ok "wait is bounded (${elapsed}s < 2s)" || bad "hook waited ${elapsed}s"

echo "── 3. route line already on disk → allow without waiting"
seed; printf '%s\n' "$FINAL" >> "$TR"
start=$(python3 -c 'import time;print(time.time())')
out="$(payload | python3 "$HOOK")"
elapsed=$(python3 -c "import time;print(round(time.time()-$start,2))")
[ -z "$out" ] && ok "route on disk → allow" || bad "route on disk blocked: $out"
python3 -c "import sys; sys.exit(0 if $elapsed < 0.3 else 1)" && ok "no wait on the happy path (${elapsed}s)" || bad "happy path waited ${elapsed}s"

echo
echo "route-guard race: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
