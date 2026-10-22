#!/usr/bin/env bash
# tests/test-inbox.sh — B-041 (SPEC-P06 §3): the panel's messages reach the running agent.
#
# Real hook (hooks/inbox-deliver.py), real osforge-db on a temporary database and HOME.
#   1. no inbox dir / no flag → silent and fast (the path every tool call takes)
#   2. a flag for another project only → silent, nothing taken
#   3. PostToolUse in the project → additionalContext with the text, in order; delivery recorded
#   4. next call → silent (taken once)
#   5. UserPromptSubmit and SessionStart answer with their own hookEventName
#   6. a subagent (agent_id) never takes the message; the main session does later
#   7. OSFORGE_INBOX=off, garbage payloads, unknown events → exit 0, silent
#   8. a slug that is not filename-safe → hashed flag name, same on both sides; delivered
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }

export HOME="$WORK/home"; mkdir -p "$HOME"
export OSFORGE_DB="$WORK/db.sqlite" OSFORGE_INBOX_DIR="$WORK/inbox"
unset OSFORGE_PROJECT OSFORGE_INBOX
HOOK="$REPO/hooks/inbox-deliver.py"
db(){ python3 "$REPO/scripts/osforge-db.py" "$@"; }
GIT="git -c user.name=t -c user.email=t@t -c init.defaultBranch=main -c commit.gpgsign=false"
P="$WORK/loja"; mkdir -p "$P/src" && (cd "$P" && $GIT init -q && echo x > a && $GIT add a && $GIT commit -qm i)
Q="$WORK/outro"; mkdir -p "$Q" && (cd "$Q" && $GIT init -q && echo x > a && $GIT add a && $GIT commit -qm i)
db upsert-project loja "Loja" standard active --root="$P" >/dev/null 2>&1
db upsert-project outro "Outro" standard active --root="$Q" >/dev/null 2>&1
pay(){  # event cwd [extra json fields]
  python3 -c "import json,sys; d={'hook_event_name': sys.argv[1], 'session_id': 'sessao-principal-1', 'cwd': sys.argv[2], 'tool_name': 'Read', 'tool_input': {}}; d.update(json.loads(sys.argv[3])); print(json.dumps(d))" "$1" "$2" "${3:-{\}}"
}
ctx(){ python3 -c "import json,sys; d=json.loads(sys.stdin.read()); h=d['hookSpecificOutput']; print(h['hookEventName']); print(h['additionalContext'])" 2>/dev/null; }

section "1. nothing pending"
OUT="$(pay PostToolUse "$P/src" | python3 "$HOOK")"; RC=$?
check "no inbox dir → exit 0, silent" "[ $RC -eq 0 ] && [ -z \"\$OUT\" ]"
MS="$(python3 - "$HOOK" "$P" <<'PY'
import json, subprocess, sys, time
hook, root = sys.argv[1:3]
pay = json.dumps({"hook_event_name": "PostToolUse", "session_id": "s", "cwd": root, "tool_name": "Read", "tool_input": {}})
ts = []
for _ in range(10):
    t0 = time.time(); subprocess.run(["python3", hook], input=pay, text=True, capture_output=True); ts.append(time.time() - t0)
print(int(sorted(ts)[5] * 1000))
PY
)"
echo "     median ${MS} ms with nothing pending"
check "fast path: median < 120 ms (Python start-up, no subprocess)" "[ \"$MS\" -lt 120 ]"

section "2. a message for another project"
db inbox-add outro "só para o outro" >/dev/null 2>&1
OUT="$(pay PostToolUse "$P" | python3 "$HOOK")"
check "silent here, still pending there" "[ -z \"\$OUT\" ] && db --json inbox outro | grep -q '\"pendente\"'"

section "3. delivery on the next tool call"
db inbox-add loja "Use Server Actions no checkout" >/dev/null 2>&1
db inbox-add loja "Depois rode os testes" >/dev/null 2>&1
OUT="$(pay PostToolUse "$P/src" | python3 "$HOOK")"
check "PostToolUse → additionalContext with both, in order" "printf '%s' \"\$OUT\" | ctx | python3 -c 'import sys; t=sys.stdin.read(); assert t.startswith(\"PostToolUse\") and t.index(\"Server Actions\") < t.index(\"rode os testes\") and \"Orientação do Paulo\" in t, t'"
check "delivery recorded with the session" "db --json inbox loja | python3 -c 'import json,sys; d=json.load(sys.stdin); assert all(m[\"status\"]==\"entregue\" and m[\"sessao\"]==\"sessao-p\" for m in d), d'"
check "flag removed" "[ ! -f \"$OSFORGE_INBOX_DIR/loja\" ] && [ -f \"$OSFORGE_INBOX_DIR/outro\" ]"

section "4. taken once"
OUT="$(pay PostToolUse "$P" | python3 "$HOOK")"
check "next call → silent" "[ -z \"\$OUT\" ]"

section "5. other events"
db inbox-add loja "mensagem 3" >/dev/null 2>&1
OUT="$(pay UserPromptSubmit "$P" | python3 "$HOOK")"
check "UserPromptSubmit → its own hookEventName" "[ \"\$(printf '%s' \"\$OUT\" | ctx | head -1)\" = UserPromptSubmit ]"
db inbox-add loja "mensagem 4" >/dev/null 2>&1
OUT="$(pay SessionStart "$P" | python3 "$HOOK")"
check "SessionStart → its own hookEventName" "[ \"\$(printf '%s' \"\$OUT\" | ctx | head -1)\" = SessionStart ]"

section "6. subagents"
db inbox-add loja "para quem conduz" >/dev/null 2>&1
OUT="$(pay PostToolUse "$P" '{"agent_id":"a1","agent_type":"general-purpose"}' | python3 "$HOOK")"
check "subagent → silent, message still pending" "[ -z \"\$OUT\" ] && [ -f \"$OSFORGE_INBOX_DIR/loja\" ]"
OUT="$(pay PostToolUse "$P" | python3 "$HOOK")"
check "the main session gets it next" "printf '%s' \"\$OUT\" | grep -q 'para quem conduz'"

section "7. switches and bad input"
db inbox-add loja "não entregar" >/dev/null 2>&1
OUT="$(pay PostToolUse "$P" | OSFORGE_INBOX=off python3 "$HOOK")"; RC=$?
check "OSFORGE_INBOX=off → silent, still pending" "[ $RC -eq 0 ] && [ -z \"\$OUT\" ] && [ -f \"$OSFORGE_INBOX_DIR/loja\" ]"
for p in 'not json' '[1,2]' '{"hook_event_name":"Stop","cwd":"/"}' ''; do
  OUT="$(printf '%s' "$p" | python3 "$HOOK")"; RC=$?
  check "payload '$p' → exit 0, silent" "[ $RC -eq 0 ] && [ -z \"\$OUT\" ]"
done
OUT="$(pay PostToolUse "$WORK" | python3 "$HOOK")"
check "cwd outside any project → silent" "[ -z \"\$OUT\" ]"

section "8. slug that is not filename-safe"
W="$WORK/Weird Proj"; mkdir -p "$W" && (cd "$W" && $GIT init -q && echo x > a && $GIT add a && $GIT commit -qm i)
db upsert-project "Weird Proj" "w" standard active --root="$W" >/dev/null 2>&1
db inbox-add "Weird Proj" "orientação estranha" >/dev/null 2>&1
check "flag name is hashed, never the raw slug" "ls \"$OSFORGE_INBOX_DIR\" | grep -q '^h-' && [ ! -e \"$OSFORGE_INBOX_DIR/Weird Proj\" ]"
OUT="$(pay PostToolUse "$W" | python3 "$HOOK")"
check "delivered" "printf '%s' \"\$OUT\" | grep -q 'orientação estranha'"

echo ""
echo "test-inbox: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
