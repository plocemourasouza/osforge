#!/usr/bin/env bash
# =============================================================================
# test-trigger-detect.sh — the trigger eval counts what the model actually does
# =============================================================================
#
# First paid E1 trigger pilot (2026-09-29, tdd-workflow): 0/15 triggers, positives
# included. Two harness defects, not model behaviour:
#
#   1. Shadowing — run_eval.py only counted a call to its temporary clone
#      `<skill>-skill-<uuid>`. A core skill is already native under the same
#      description, so a model that invokes the REAL `tdd-workflow` was scored
#      as "did not trigger": positives fail for free, negatives pass for free.
#   2. Contaminated cwd — the eval ran with the OSForge repo as project root, so
#      the hub-session rule ("never execute another repo's code here") answered
#      the query before any skill was considered.
#
# Offline: a fake `claude` first on PATH emits a stream-json Skill call and
# records the directory it was run from. Never touches the API.
# =============================================================================
set -u
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0; FAIL=0
ok()   { echo "  ✓ $1"; PASS=$((PASS + 1)); }
bad()  { echo "  ✗ $1"; FAIL=$((FAIL + 1)); }

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

echo "── 1. detector: unit"
PYTHONPATH="$REPO/skills/skill-creator" python3 - "$REPO" <<'PY' && ok "is_skill_trigger accepts clone and real skill, rejects others" || bad "is_skill_trigger"
import sys
sys.path.insert(0, sys.argv[1] + "/skills/skill-creator/scripts")
from run_eval import is_skill_trigger as t
clone, real = "tdd-workflow-skill-ab12cd34", "tdd-workflow"
cases = [
    (("Skill", {"skill": clone}), True),
    (("Skill", {"skill": real}), True),
    (("Skill", {"skill": "plugin:" + real}), True),
    (("Skill", {"skill": "tdd-workflow-extra"}), False),
    (("Skill", {"skill": "code-review"}), False),
    (("Read", {"file_path": "/x/.claude/commands/" + clone + ".md"}), True),
    (("Read", {"file_path": "/Users/u/.claude/skills/tdd-workflow/SKILL.md"}), True),
    (("Read", {"file_path": "/repo/src/tdd-workflow.ts"}), False),
    (("Bash", {"command": "cat skills/tdd-workflow/SKILL.md"}), False),
]
bad = [(a, want) for a, want in cases if t(*a, clone, real) is not want]
for a, want in bad:
    print("    want", want, "for", a)
sys.exit(1 if bad else 0)
PY

echo "── 2. harness: real-skill call counts, cwd is not the OSForge repo"
mkdir -p "$WORK/bin"
cat > "$WORK/bin/claude" <<EOF
#!/usr/bin/env bash
pwd -P >> "$WORK/cwds"
printf '%s\n' '{"type":"system","subtype":"init"}'
printf '%s\n' '{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"tdd-workflow"}}]}}'
printf '%s\n' '{"type":"result","subtype":"success"}'
EOF
chmod +x "$WORK/bin/claude"

PATH="$WORK/bin:$PATH" OSFORGE_EVAL_WORKERS=1 "$REPO/scripts/run-trigger-eval.sh" \
    --model fake --runs 1 --split eval --skill tdd-workflow --ignore-quota \
    > "$WORK/out.txt" 2>&1
art="$(sed -n 's/^ *artefatos *: *//p' "$WORK/out.txt" | tail -1)"
res="$art/tdd-workflow.result.json"
if [ -s "$res" ]; then
    pos="$(python3 -c 'import json,sys; r=json.load(open(sys.argv[1]))["results"]; print(sum(x["triggers"] for x in r if x["should_trigger"]))' "$res")"
    [ "$pos" -ge 1 ] && ok "fake model calling real skill counted as trigger ($pos)" \
                     || bad "real-skill call scored as no trigger (positives triggers=$pos)"
else
    bad "no result.json (see output below)"; sed 's/^/    /' "$WORK/out.txt" | tail -8
fi
rm -rf "$art"

if [ -s "$WORK/cwds" ]; then
    repo_real="$(cd "$REPO" && pwd -P)"
    if grep -q "^$repo_real" "$WORK/cwds"; then
        bad "claude ran inside the OSForge repo: $(head -1 "$WORK/cwds")"
    else
        ok "claude ran outside the OSForge repo"
    fi
else
    bad "fake claude never invoked"
fi

echo ""
echo "trigger-detect: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
