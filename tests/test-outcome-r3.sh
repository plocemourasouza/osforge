#!/usr/bin/env bash
# =============================================================================
# test-outcome-r3.sh — outcome eval round r3 (docs/intake/ponytail/MEDICAO-r3.md), offline
# =============================================================================
#
# Never calls a model: only build_variants.py and driver.py --dry (whose judge step is
# judge.py --dry). Checks:
#
#   1. build_variants.py --round r3 builds all 10 variants, and the committed ones are current
#   2. arm C differs from arm B for every r3 target
#   3. r1 and r2 variants rebuild byte-identical (r3 did not change them)
#   4. driver.py --dry --round r3 validates and plans 396 calls; --skip ponytail-ref plans 288
#   5. --skip with an unknown target fails
#   6. ponytail-ref B keeps its MIT header in the file but not in the system prompt
#   7. the map tasks (cg1m/cg3m/cg5m) do not carry the helper file; mapa-repo C carries the map
#   8. ponytail-ref reads the coding-guidelines task files (no copies)
#
# USO:  ./tests/test-outcome-r3.sh
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTCOME="$REPO_ROOT/scripts/evals/outcome"
R3="$OUTCOME/r3"
TARGETS="coding-guidelines code-review repo-audit mapa-repo ponytail-ref"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PASS=0
FAIL=0

check() {
    local desc="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "  ✅ $desc"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $desc  (expected: $expected · got: $actual)"
        FAIL=$((FAIL + 1))
    fi
}

# sha256 of every file in a directory, one "name hash" per line (portable: python, not sha256sum).
digest_dir() {
    python3 -c '
import hashlib, os, sys
d = sys.argv[1]
for f in sorted(os.listdir(d)):
    print(f, hashlib.sha256(open(os.path.join(d, f), "rb").read()).hexdigest())
' "$1"
}

echo "── 1. build_variants.py --round r3"
digest_dir "$R3/variants" > "$WORK/r3.before" 2>/dev/null || : > "$WORK/r3.before"
python3 "$OUTCOME/build_variants.py" --round r3 > "$WORK/build-r3.log" 2>&1
check "build r3 exits 0" "0" "$?"
digest_dir "$R3/variants" > "$WORK/r3.after"
n=0
for t in $TARGETS; do
    for arm in B C; do
        [ -s "$R3/variants/$t.$arm.md" ] && n=$((n + 1))
    done
done
check "10 r3 variants present (5 targets x B/C)" "10" "$n"
if cmp -s "$WORK/r3.before" "$WORK/r3.after"; then same=yes; else same=no; fi
check "committed r3 variants were already current (rebuild changed nothing)" "yes" "$same"

echo "── 2. arm C differs from arm B"
for t in $TARGETS; do
    if cmp -s "$R3/variants/$t.B.md" "$R3/variants/$t.C.md"; then d=same; else d=differs; fi
    check "$t: C differs from B" "differs" "$d"
done

echo "── 3. r1 / r2 variants unchanged"
digest_dir "$OUTCOME/variants" > "$WORK/r1.before"
digest_dir "$OUTCOME/r2/variants" > "$WORK/r2.before"
python3 "$OUTCOME/build_variants.py" > /dev/null 2>&1
check "build r1 exits 0" "0" "$?"
python3 "$OUTCOME/build_variants.py" --round r2 > /dev/null 2>&1
check "build r2 exits 0" "0" "$?"
digest_dir "$OUTCOME/variants" > "$WORK/r1.after"
digest_dir "$OUTCOME/r2/variants" > "$WORK/r2.after"
if cmp -s "$WORK/r1.before" "$WORK/r1.after"; then same=yes; else same=no; fi
check "r1 variants rebuild byte-identical" "yes" "$same"
if cmp -s "$WORK/r2.before" "$WORK/r2.after"; then same=yes; else same=no; fi
check "r2 variants rebuild byte-identical" "yes" "$same"
if git -C "$REPO_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
    dirty="$(git -C "$REPO_ROOT" status --porcelain -- scripts/evals/outcome/variants scripts/evals/outcome/r2/variants | wc -l | tr -d ' ')"
    check "r1/r2 variants match git (no diff after rebuild)" "0" "$dirty"
fi

echo "── 4. driver.py --dry --round r3"
python3 "$OUTCOME/driver.py" --dry --round r3 > "$WORK/dry.log" 2>&1
check "--dry --round r3 exits 0" "0" "$?"
check "no PROBLEM lines" "0" "$(grep -c '^PROBLEM' "$WORK/dry.log")"
check "plans 198 executor + 198 judge calls" "1" "$(grep -c '^plan: 198 executor calls + 198 judge calls (runs=3)' "$WORK/dry.log")"
check "total model calls 396" "1" "$(grep -c 'total model calls: 396' "$WORK/dry.log")"
check "judge.py --dry ok" "1" "$(grep -c "judge.py --dry ok=True isolation-argv has --tools '': True" "$WORK/dry.log")"
python3 "$OUTCOME/driver.py" --dry --round r3 --skip ponytail-ref > "$WORK/dry-skip.log" 2>&1
check "--skip ponytail-ref exits 0" "0" "$?"
check "--skip ponytail-ref: total model calls 288" "1" "$(grep -c 'total model calls: 288' "$WORK/dry-skip.log")"
check "--skip ponytail-ref: target not planned" "0" "$(grep -c '^  ponytail-ref ' "$WORK/dry-skip.log")"
python3 "$OUTCOME/driver.py" --dry --round r3 --only mapa-repo > "$WORK/dry-only.log" 2>&1
check "--only mapa-repo: total model calls 54" "1" "$(grep -c 'total model calls: 54' "$WORK/dry-only.log")"

echo "── 5. bad --skip"
python3 "$OUTCOME/driver.py" --dry --round r3 --skip no-such-target > "$WORK/dry-bad.log" 2>&1
rc=$?
if [ "$rc" -ne 0 ]; then bad=fails; else bad=passes; fi
check "--skip no-such-target fails" "fails" "$bad"

echo "── 6. ponytail-ref license header"
check "variant file starts with the MIT header" "1" "$(head -5 "$R3/variants/ponytail-ref.B.md" | grep -c 'MIT License, Copyright (c) 2026 DietrichGebert')"
in_prompt="$(cd "$OUTCOME" && python3 -c '
import driver as D
D.configure("r3")
s = D.system_prompt("ponytail-ref", "B")
print("header" if ("<!--" in s or "MIT License" in s) else "clean", "body" if "# Ponytail" in s else "nobody")
')"
check "system prompt has the body, not the header" "clean body" "$in_prompt"

echo "── 7. map tasks"
check "cg1m has no components/ui/input" "0" "$(grep -c 'components/ui/input' "$R3/tasks/mapa-repo/cg1m.md")"
check "cg3m has no lib/format" "0" "$(grep -c 'lib/format' "$R3/tasks/mapa-repo/cg3m.md")"
check "cg3m never names formatCurrency" "0" "$(grep -c 'formatCurrency' "$R3/tasks/mapa-repo/cg3m.md")"
check "cg5m has no lib/money" "0" "$(grep -c 'lib/money' "$R3/tasks/mapa-repo/cg5m.md")"
check "cg5m never names toCents" "0" "$(grep -c 'toCents' "$R3/tasks/mapa-repo/cg5m.md")"
check "mapa-repo C carries the codebase map" "1" "$(grep -c '^Codebase map (what already exists' "$R3/variants/mapa-repo.C.md")"
check "mapa-repo B has no map" "0" "$(grep -c '^Codebase map' "$R3/variants/mapa-repo.B.md")"
if cmp -s "$R3/variants/mapa-repo.B.md" "$R3/variants/coding-guidelines.C.md"; then same=yes; else same=no; fi
check "mapa-repo B = coding-guidelines C (coding-guidelines + P-01)" "yes" "$same"
if cmp -s "$R3/variants/ponytail-ref.C.md" "$R3/variants/coding-guidelines.C.md"; then same=yes; else same=no; fi
check "ponytail-ref C = coding-guidelines C" "yes" "$same"

echo "── 8. ponytail-ref reuses the coding-guidelines tasks"
if [ -d "$R3/tasks/ponytail-ref" ]; then copies=yes; else copies=no; fi
check "no tasks/ponytail-ref copy" "no" "$copies"

echo ""
echo "test-outcome-r3: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
