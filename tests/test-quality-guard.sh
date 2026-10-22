#!/usr/bin/env bash
# tests/test-quality-guard.sh — B-035 (SPEC-P04): edit-time guards in a temporary git repo.
#
# Real hook (hooks/quality-guard.py), real osforge-db on a temporary database, temporary HOME.
# No network, nothing under the live ~/.claude. Cases of SPEC-P04 + the signals CLI:
#   1. rename formatPrice used in two files → G-1 lists both; fix the callers → resolved
#   2. rename a function nobody calls → silence
#   3. same word only as text / property (obj.formatPrice, "formatPrice(") → silence
#   4. Write a new file with formatCurrency existing in lib/format.ts → G-2; generic name → silence
#   5. new page.tsx with `export default function Page` → silence
#   6. Bash `npm test` exit 0 → passed; Edit .ts afterwards → stale; `echo npm test` → nothing;
#      PostToolUseFailure → failed; interrupted → nothing
#   7. shadow → signals recorded, stdout empty; off → nothing recorded; on → additionalContext
#   8. no git, file outside the repo, invalid payloads → exit 0, silent
#   9. budget: 5,000-file repo → p95 < 150 ms on a common Edit (no git, no db on the cheap path)
#   10. signals CLI: dedupe of open signals, tests closes the previous state, --report, retention,
#       set-project-status, unknown kind → exit 2
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }

export HOME="$WORK/home"; mkdir -p "$HOME"
export OSFORGE_DB="$WORK/db.sqlite" OSFORGE_LOG_DIR="$WORK/logs" OSFORGE_QG_DIR="$WORK/qg"
unset OSFORGE_PROJECT OSFORGE_QUALITY_GUARD
HOOK="$REPO/hooks/quality-guard.py"
db(){ python3 "$REPO/scripts/osforge-db.py" "$@"; }
GIT="git -c user.name=t -c user.email=t@t -c init.defaultBranch=main -c commit.gpgsign=false"

P="$WORK/shop"; mkdir -p "$P/lib" "$P/app/cart" "$P/app/orders" "$P/components"
cat > "$P/lib/price.ts" <<'EOF'
export function formatPrice(cents: number): string {
  return (cents / 100).toFixed(2);
}

export function orphanHelper(): number {
  return 1;
}
EOF
cat > "$P/lib/format.ts" <<'EOF'
const brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
export function formatCurrency(cents: number): string {
  return brl.format(cents / 100);
}
EOF
cat > "$P/app/cart/page.tsx" <<'EOF'
import { formatPrice } from "@/lib/price";
export default function Page() {
  return <p>{formatPrice(100)}</p>;
}
EOF
cat > "$P/app/orders/summary.ts" <<'EOF'
import { formatPrice } from "../../lib/price";
export const total = (c: number) => formatPrice(c);
EOF
cat > "$P/components/note.ts" <<'EOF'
// formatPrice( is mentioned in this comment only
export const label = "call formatPrice(x) to format";
export const obj = { formatPrice: 1 };
export const v = obj.formatPrice;
EOF
cat > "$P/package.json" <<'EOF'
{"name":"shop","scripts":{"test":"vitest run","test:e2e":"playwright test","lint":"eslint ."}}
EOF
(cd "$P" && $GIT init -q && $GIT add -A && $GIT commit -qm init)
db upsert-project shop "loja" standard active --root="$P" >/dev/null 2>&1

# payload builders ---------------------------------------------------------------------------
edit_payload(){  # file old new [event]
  python3 - "$P" "$1" "$2" "$3" "${4:-PostToolUse}" <<'EOF'
import json, sys
root, f, old, new, ev = sys.argv[1:6]
print(json.dumps({"hook_event_name": ev, "session_id": "s1", "cwd": root, "tool_name": "Edit",
                  "tool_input": {"file_path": f"{root}/{f}", "old_string": old, "new_string": new},
                  "tool_response": {"filePath": f"{root}/{f}"}}))
EOF
}
write_payload(){  # file (content read from disk)
  python3 - "$P" "$1" <<'EOF'
import json, sys
root, f = sys.argv[1:3]
content = open(f"{root}/{f}").read()
print(json.dumps({"hook_event_name": "PostToolUse", "session_id": "s1", "cwd": root, "tool_name": "Write",
                  "tool_input": {"file_path": f"{root}/{f}", "content": content}}))
EOF
}
bash_payload(){  # command event [interrupted] [stdout]
  python3 - "$P" "$1" "$2" "${3:-}" "${4-__default__}" <<'EOF'
import json, sys
root, cmd, ev, intr, out = sys.argv[1:6]
p = {"hook_event_name": ev, "session_id": "s1", "cwd": root, "tool_name": "Bash", "tool_input": {"command": cmd}}
if ev == "PostToolUse":
    if out == "__default__":
        out = " Test Files  3 passed (3)\n      Tests  12 passed (12)\n"
    p["tool_response"] = {"stdout": out, "stderr": "", "interrupted": bool(intr)}
else:
    p["error"] = "Exit code 1\n Tests  2 failed | 10 passed (12)"
    p["is_interrupt"] = bool(intr)
print(json.dumps(p))
EOF
}
apply_edit(){  # file old new — performs the edit on disk like Claude Code would, then the hook
  python3 - "$P/$1" "$2" "$3" <<'EOF'
import sys
p, old, new = sys.argv[1:4]
s = open(p).read(); assert s.count(old) == 1, (p, old); open(p, "w").write(s.replace(old, new))
EOF
}
run(){ python3 "$HOOK"; }
count(){  # kind [open|all]
  db --json signals shop 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); k=sys.argv[1]; print(sum(1 for x in d if x['kind']==k and (sys.argv[2]=='all' or not x['resolved_at'])))" "$1" "${2:-open}"; }

section "1. G-1: rename formatPrice used in two files"
apply_edit lib/price.ts "export function formatPrice(" "export function formatMoney("
OUT="$(edit_payload lib/price.ts "export function formatPrice(" "export function formatMoney(" | OSFORGE_QUALITY_GUARD=on run)"; RC=$?
check "exit 0" "[ $RC -eq 0 ]"
check "model told: both callers listed" "printf '%s' \"\$OUT\" | grep -q 'app/cart/page.tsx:3' && printf '%s' \"\$OUT\" | grep -q 'app/orders/summary.ts:2'"
check "message names the kill-switch" "printf '%s' \"\$OUT\" | grep -q 'OSFORGE_QUALITY_GUARD=off'"
check "stdout is one JSON object with additionalContext" "printf '%s' \"\$OUT\" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d[\"hookSpecificOutput\"][\"hookEventName\"]==\"PostToolUse\" and d[\"hookSpecificOutput\"][\"additionalContext\"]'"
check "comment, string and property usages not counted (2 callers, not more)" "db --json signals shop | python3 -c 'import json,sys; d=[x for x in json.load(sys.stdin) if x[\"kind\"]==\"callers_open\"]; assert d[0][\"detail\"][\"count\"]==2, d'"
check "one open callers_open signal" "[ \"\$(count callers_open)\" = 1 ]"
OUT2="$(edit_payload lib/price.ts "export function formatPrice(" "export function formatMoney(" | OSFORGE_QUALITY_GUARD=on run)"
check "same edit again → no duplicate signal" "[ \"\$(count callers_open all)\" = 1 ]"
apply_edit app/cart/page.tsx 'import { formatPrice } from "@/lib/price";' 'import { formatMoney } from "@/lib/price";'
apply_edit app/cart/page.tsx '{formatPrice(100)}' '{formatMoney(100)}'
OUT="$(edit_payload app/cart/page.tsx '{formatPrice(100)}' '{formatMoney(100)}' | OSFORGE_QUALITY_GUARD=on run)"
check "one caller fixed → still open, nothing new said" "[ \"\$(count callers_open)\" = 1 ] && [ -z \"\$OUT\" ]"
apply_edit app/orders/summary.ts 'import { formatPrice } from "../../lib/price";' 'import { formatMoney } from "../../lib/price";'
apply_edit app/orders/summary.ts '=> formatPrice(c)' '=> formatMoney(c)'
OUT="$(edit_payload app/orders/summary.ts '=> formatPrice(c)' '=> formatMoney(c)' | OSFORGE_QUALITY_GUARD=on run)"
check "last caller fixed → signal resolved by itself, silent" "[ \"\$(count callers_open)\" = 0 ] && [ \"\$(count callers_open all)\" = 1 ] && [ -z \"\$OUT\" ]"

section "2. rename a function nobody calls"
apply_edit lib/price.ts "export function orphanHelper(" "export function lonelyHelper("
OUT="$(edit_payload lib/price.ts "export function orphanHelper(" "export function lonelyHelper(" | OSFORGE_QUALITY_GUARD=on run)"
check "silence" "[ -z \"\$OUT\" ] && [ \"\$(count callers_open)\" = 0 ]"

section "3. word only as text/property elsewhere"
cat > "$P/lib/units.ts" <<'EOF'
export function toLabel(n: number) { return String(n); }
EOF
(cd "$P" && $GIT add -A && $GIT commit -qm units)
cat > "$P/components/props.ts" <<'EOF'
export const conf = { toLabel: true };
export const s = "toLabel(";
// toLabel(1)
export const w = conf.toLabel;
EOF
apply_edit lib/units.ts "export function toLabel(" "export function asLabel("
OUT="$(edit_payload lib/units.ts "export function toLabel(" "export function asLabel(" | OSFORGE_QUALITY_GUARD=on run)"
check "silence" "[ -z \"\$OUT\" ]"

section "3b. moved, not removed; indented fragment"
cat > "$P/lib/round.ts" <<'EOF'
export function roundHalfUp(x: number) { return Math.round(x); }
EOF
cat > "$P/app/cart/sum.ts" <<'EOF'
import { roundHalfUp } from "@/lib/round";
export const s = roundHalfUp(1.5);
EOF
(cd "$P" && $GIT add -A && $GIT commit -qm round)
printf 'export function roundHalfUp(x: number) { return Math.round(x); }\n' > "$P/lib/rounding.ts"
apply_edit lib/round.ts "export function roundHalfUp(x: number) { return Math.round(x); }" ""
apply_edit app/cart/sum.ts '"@/lib/round"' '"@/lib/rounding"'
OUT="$(edit_payload lib/round.ts "export function roundHalfUp(x: number) { return Math.round(x); }" "" | OSFORGE_QUALITY_GUARD=on run)"
check "function moved to another file → no G-1" "[ -z \"\$OUT\" ]"
mkdir -p "$P/py"
printf 'def compute_total(items):\n    return sum(items)\n' > "$P/py/totals.py"
printf 'class Order:\n    def total(self):\n        return 1\n' > "$P/py/orders.py"
(cd "$P" && $GIT add -A && $GIT commit -qm py)
apply_edit py/orders.py "        return 1" "        computeTotal = 3\n        return computeTotal"
OUT="$(edit_payload py/orders.py "        return 1" "computeTotal = 3
        return computeTotal" | OSFORGE_QUALITY_GUARD=on run)"
check "local variable in an indented fragment → no G-2" "[ -z \"\$OUT\" ]"

section "4. G-2: new file duplicates formatCurrency"
cat > "$P/lib/money.ts" <<'EOF'
export function format_currency(cents: number): string {
  return "R$ " + (cents / 100).toFixed(2);
}
export function get(x: number) { return x; }
EOF
OUT="$(write_payload lib/money.ts | OSFORGE_QUALITY_GUARD=on run)"
check "model told where it already exists" "printf '%s' \"\$OUT\" | grep -q 'formatCurrency' && printf '%s' \"\$OUT\" | grep -q 'lib/format.ts:2'"
check "generic name 'get' not reported" "! printf '%s' \"\$OUT\" | grep -q '\`get\`'"
check "duplicate signal recorded" "[ \"\$(count duplicate)\" = 1 ]"

section "5. Next.js convention file"
mkdir -p "$P/app/about"
cat > "$P/app/about/page.tsx" <<'EOF'
export default function Page() { return <p>about</p>; }
export const metadata = { title: "About" };
EOF
OUT="$(write_payload app/about/page.tsx | OSFORGE_QUALITY_GUARD=on run)"
check "silence" "[ -z \"\$OUT\" ]"

section "6. G-3: tests state"
bash_payload "npm test" PostToolUse | run
check "npm test exit 0 → passed with counts" "db --json signals shop --open | python3 -c 'import json,sys; t=[x for x in json.load(sys.stdin) if x[\"kind\"]==\"tests\"]; assert len(t)==1 and t[0][\"detail\"][\"state\"]==\"passed\" and t[0][\"detail\"][\"passed\"]==12, t'"
bash_payload "echo npm test" PostToolUse | run
bash_payload "grep -r 'npm test' docs" PostToolUse | run
check "echo/grep of a test command → no new signal" "[ \"\$(count tests all)\" = 1 ]"
apply_edit lib/format.ts 'const brl' 'const brlFormatter'
apply_edit lib/format.ts 'return brl.format' 'return brlFormatter.format'
edit_payload lib/format.ts 'const brl' 'const brlFormatter' | run
check "edit after a run → stale (previous state closed)" "db --json signals shop --open | python3 -c 'import json,sys; t=[x for x in json.load(sys.stdin) if x[\"kind\"]==\"tests\"]; assert len(t)==1 and t[0][\"detail\"][\"state\"]==\"stale\", t'"
edit_payload lib/format.ts 'return brl.format' 'return brlFormatter.format' | run
check "second edit while stale → no new signal" "[ \"\$(count tests all)\" = 2 ]"
bash_payload "CI=1 pnpm run test:e2e" PostToolUseFailure | run
check "failure event → failed with counts" "db --json signals shop --open | python3 -c 'import json,sys; t=[x for x in json.load(sys.stdin) if x[\"kind\"]==\"tests\"]; assert t[0][\"detail\"][\"state\"]==\"failed\" and t[0][\"detail\"][\"failed\"]==2, t'"
bash_payload "npx vitest run" PostToolUseFailure 1 | run
check "interrupted run → ignored" "[ \"\$(count tests all)\" = 3 ]"
bash_payload "npm run lint" PostToolUse | run
check "non-test script → ignored" "[ \"\$(count tests all)\" = 3 ]"
bash_payload "python3 -m pytest -q && echo done" PostToolUse | run
check "python -m pytest inside a chain → passed" "[ \"\$(count tests all)\" = 4 ]"
state(){ db --json signals shop --open | python3 -c 'import json,sys; t=[x for x in json.load(sys.stdin) if x["kind"]=="tests"]; print(t[0]["detail"]["state"])'; }
bash_payload "npx vitest run 2>&1 | tail -5" PostToolUse "" " Tests  2 failed | 3 passed (5)"  | run
check "exit 0 hidden by a pipe, runner printed failures → failed" "[ \"\$(state)\" = failed ]"
bash_payload "pytest || true" PostToolUse "" "" | run
check "exit code masked (|| true), no summary → unknown, not passed" "[ \"\$(state)\" = unknown ]"
bash_payload "npm test; echo done" PostToolUse "" "" | run
check "runner not last (; echo) → unknown" "[ \"\$(state)\" = unknown ]"

section "7. modes"
BEFORE="$(count callers_open all)"
apply_edit lib/format.ts "export function formatCurrency(" "export function formatBRL("
cat > "$P/app/cart/total.ts" <<'EOF'
import { formatCurrency } from "@/lib/format";
export const t = formatCurrency(1);
EOF
(cd "$P" && $GIT add app/cart/total.ts)
OUT="$(edit_payload lib/format.ts "export function formatCurrency(" "export function formatBRL(" | OSFORGE_QUALITY_GUARD=off run)"
check "off → nothing recorded, silent" "[ -z \"\$OUT\" ] && [ \"\$(count callers_open all)\" = \"$BEFORE\" ]"
OUT="$(edit_payload lib/format.ts "export function formatCurrency(" "export function formatBRL(" | run)"
check "default is shadow → recorded, stdout empty" "[ -z \"\$OUT\" ] && [ \"\$(count callers_open)\" = 1 ]"

section "8. no git / outside the repo / bad payloads"
mkdir -p "$WORK/nogit"; echo 'export function a1234() {}' > "$WORK/nogit/x.ts"
OUT="$(printf '{"hook_event_name":"PostToolUse","tool_name":"Edit","cwd":"%s","tool_input":{"file_path":"%s/x.ts","old_string":"export function a1234","new_string":"export function b1234"}}' "$WORK/nogit" "$WORK/nogit" | OSFORGE_QUALITY_GUARD=on run)"; RC=$?
check "no git → exit 0, silent" "[ $RC -eq 0 ] && [ -z \"\$OUT\" ]"
OUT="$(printf 'not json' | run)"; RC=$?
check "garbage → exit 0, silent" "[ $RC -eq 0 ] && [ -z \"\$OUT\" ]"
OUT="$(printf '[1,2]' | run)"; RC=$?
check "list payload → exit 0, silent" "[ $RC -eq 0 ] && [ -z \"\$OUT\" ]"
OUT="$(printf '{"tool_name":"Edit","tool_input":"x"}' | run)"; RC=$?
check "tool_input not an object → exit 0, silent" "[ $RC -eq 0 ] && [ -z \"\$OUT\" ]"
OUT="$(printf '{"tool_name":"Edit","tool_input":{"file_path":"relative.ts"}}' | run)"; RC=$?
check "relative path → exit 0, silent" "[ $RC -eq 0 ] && [ -z \"\$OUT\" ]"
check "nothing written to /tmp by the hook" "[ -z \"\$(find /tmp -maxdepth 1 -newer \"$OSFORGE_DB\" -name '*quality*' 2>/dev/null)\" ]"

section "9. budget: 5,000-file repo, common Edit"
B="$WORK/big"; mkdir -p "$B/src"
python3 - "$B/src" <<'EOF'
import os, sys
d = sys.argv[1]
for i in range(5000):
    sub = os.path.join(d, f"m{i // 100}")
    os.makedirs(sub, exist_ok=True)
    with open(os.path.join(sub, f"f{i}.ts"), "w") as f:
        f.write(f"export function fn{i}(x: number) {{\n  return x + {i};\n}}\n")
EOF
(cd "$B" && $GIT init -q && $GIT add -A && $GIT commit -qm big)
db upsert-project big "b" standard active --root="$B" >/dev/null 2>&1
P95="$(python3 - "$HOOK" "$B" <<'EOF'
import json, subprocess, sys, time
hook, root = sys.argv[1:3]
f = f"{root}/src/m10/f1000.ts"
pay = json.dumps({"hook_event_name": "PostToolUse", "cwd": root, "tool_name": "Edit",
                  "tool_input": {"file_path": f, "old_string": "return x + 1000;", "new_string": "return x + 1001;"}})
ts = []
for _ in range(20):
    t0 = time.time(); subprocess.run(["python3", hook], input=pay, text=True, capture_output=True); ts.append(time.time() - t0)
ts.sort(); print(int(ts[int(len(ts) * .95) - 1] * 1000))
EOF
)"
echo "     p95 = ${P95} ms"
check "p95 < 150 ms" "[ \"$P95\" -lt 150 ]"

python3 - "$B/src" <<'EOF'
import sys
lines = [f"export function fn{i}(x: number) {{ return x; }}" for i in range(30)]
open(sys.argv[1] + "/many.ts", "w").write("\n".join(lines) + "\n")
EOF
MS="$(python3 - "$HOOK" "$B" <<'EOF'
import json, subprocess, sys, time
hook, root = sys.argv[1:3]
f = f"{root}/src/many.ts"
pay = json.dumps({"hook_event_name": "PostToolUse", "cwd": root, "tool_name": "Write",
                  "tool_input": {"file_path": f, "content": open(f).read()}})
t0 = time.time(); subprocess.run(["python3", hook], input=pay, text=True, capture_output=True, env=dict(__import__("os").environ, OSFORGE_QUALITY_GUARD="on")); print(int((time.time() - t0) * 1000))
EOF
)"
echo "     Write with 30 duplicated exports: ${MS} ms"
check "worst case stays inside the hook's 5 s timeout (budget 3 s)" "[ \"$MS\" -lt 4000 ]"

section "10. signals CLI"
check "unknown kind → exit 2" "db add-signal shop nope x >/dev/null 2>&1; [ \$? -eq 2 ]"
check "--detail must be JSON → exit 2" "db add-signal shop duplicate x --detail='{bad' >/dev/null 2>&1; [ \$? -eq 2 ]"
R="$(db --json signals shop --report)"
check "--report: per-kind totals and resolved counts" "printf '%s' \"\$R\" | python3 -c 'import json,sys; d=json.load(sys.stdin); k=d[\"kinds\"]; assert k[\"callers_open\"][\"total\"]>=2 and k[\"callers_open\"][\"resolved\"]>=1 and k[\"duplicate\"][\"total\"]==1, d'"
check "--report: sample excludes tests and has ≤ 20" "printf '%s' \"\$R\" | python3 -c 'import json,sys; d=json.load(sys.stdin); s=d[\"sample\"]; assert 0<len(s)<=20 and all(x[\"kind\"]!=\"tests\" for x in s)'"
python3 - "$OSFORGE_DB" <<'EOF'
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
c.execute("UPDATE signals SET ts='2020-01-01T00:00:00Z'")
c.commit()
EOF
OPEN_BEFORE="$(db --json signals --open | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')"
db prune-calls --older-than=90d >/dev/null 2>&1
check "retention removes old resolved signals, keeps open ones" "[ \"\$(db --json signals | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')\" = \"$OPEN_BEFORE\" ]"
check "set-project-status backlog" "db set-project-status shop backlog >/dev/null 2>&1 && db --json list-projects --status=backlog | grep -q '\"shop\"'"
check "set-project-status rejects other values (exit 2)" "db set-project-status shop someday >/dev/null 2>&1; [ \$? -eq 2 ]"
check "upsert-project rejects other status (exit 2)" "db upsert-project zz z standard someday >/dev/null 2>&1; [ \$? -eq 2 ]"

echo ""
echo "test-quality-guard: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
