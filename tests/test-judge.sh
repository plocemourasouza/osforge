#!/usr/bin/env bash
# =============================================================================
# test-judge.sh -- contract tests for scripts/lib/judge.py (B-029, SPEC-L02)
# =============================================================================
#
# judge.py is the isolated `claude` call used as a model-based judge: no tools,
# no user CLAUDE.md/hooks/MCPs, a fresh empty cwd, structured output validated
# locally. This never invokes the real `claude` binary -- a fake one is put
# first on PATH that records the argv/env/cwd it received and replays a
# stream-json fixture chosen per case, so the whole suite is offline.
#
# Covers the spec's six cases:
#   1. --dry and a real run: argv has --tools "", --setting-sources "",
#      --strict-mcp-config, --json-schema, --model; never --bare or
#      --dangerously-skip-permissions; env carries the two OSFORGE vars;
#      cwd is an empty dir that no longer exists afterwards.
#   2. system/init with non-empty tools -> exit 3, isolation violated.
#   3. structured_output valid -> exit 0; missing/enum-invalid/wrong-type -> exit 2.
#   4. result.is_error with a rejected rate_limit_event, or with rate-limit
#      wording and no rate_limit_event -> exit 75.
#   5. CLI timeout -> exit 3, temp cwd removed even so.
#   6. schema validator: a table of >= 20 cases against scripts/lib/judge.py's
#      validate_schema() directly.
#
# Offline, no network, no API key needed. Usage: ./tests/test-judge.sh
# =============================================================================

set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JUDGE="$REPO/scripts/lib/judge.py"

if [[ ! -f "$JUDGE" ]]; then
    echo "FAIL: judge.py not found at $JUDGE"
    exit 1
fi

JUDGE="$JUDGE" python3 - <<'PY'
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

JUDGE = os.environ["JUDGE"]
REPO = os.path.abspath(os.path.join(os.path.dirname(JUDGE), "..", ".."))

# ---------------------------------------------------------------- load judge.py as a module,
# for the direct validate_schema() table (case 6) -- same trick as test-gateguard-sql.sh.
spec = importlib.util.spec_from_file_location("judge", JUDGE)
judge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(judge)

PASS = 0
FAIL = 0


def ok(name):
    global PASS
    PASS += 1
    print("  ok   %s" % name)


def bad(name, detail=""):
    global FAIL
    FAIL += 1
    print("  FAIL %s%s" % (name, ("  -- " + str(detail)) if detail != "" else ""))


def check(name, cond, detail=""):
    if cond:
        ok(name)
    else:
        bad(name, detail)


def section(title):
    print("")
    print("-- %s" % title)


WORK = tempfile.mkdtemp(prefix="osforge-judge-test-")
FAKE_BIN = os.path.join(WORK, "bin")
os.makedirs(FAKE_BIN)
RECORDS_ROOT = os.path.join(WORK, "records")
os.makedirs(RECORDS_ROOT)

# ---------------------------------------------------------------- fake `claude` on PATH.
# Records argv/env/cwd/stdin as JSON (not line-per-arg: the real -p and
# --append-system-prompt values contain embedded newlines, which would corrupt a
# "one arg per line" text format). Then replays a fixture and exits with a chosen code.
FAKE_CLAUDE = os.path.join(FAKE_BIN, "claude")
with open(FAKE_CLAUDE, "w", encoding="utf-8") as fh:
    fh.write('''#!/usr/bin/env python3
import json, os, sys, time

record_dir = os.environ.get("OSFORGE_JUDGE_FAKE_RECORD_DIR")
if record_dir:
    with open(os.path.join(record_dir, "argv.json"), "w", encoding="utf-8") as f:
        json.dump(sys.argv[1:], f)
    with open(os.path.join(record_dir, "env.json"), "w", encoding="utf-8") as f:
        json.dump(dict(os.environ), f)
    with open(os.path.join(record_dir, "cwd.txt"), "w", encoding="utf-8") as f:
        f.write(os.getcwd())
    try:
        stdin_data = sys.stdin.read()
    except Exception:
        stdin_data = ""
    with open(os.path.join(record_dir, "stdin.txt"), "w", encoding="utf-8") as f:
        f.write(stdin_data)

sleep_s = os.environ.get("OSFORGE_JUDGE_FAKE_SLEEP")
if sleep_s:
    time.sleep(float(sleep_s))

stream_path = os.environ.get("OSFORGE_JUDGE_FAKE_STREAM")
if stream_path:
    with open(stream_path, encoding="utf-8") as f:
        sys.stdout.write(f.read())

sys.exit(int(os.environ.get("OSFORGE_JUDGE_FAKE_EXIT", "0")))
''')
os.chmod(FAKE_CLAUDE, 0o755)

# ---------------------------------------------------------------- fixtures shared by every case.
SCHEMA_PATH = os.path.join(WORK, "schema.json")
RUBRIC_PATH = os.path.join(WORK, "rubric.md")
INPUT_PATH = os.path.join(WORK, "artifact.md")

with open(SCHEMA_PATH, "w", encoding="utf-8") as fh:
    json.dump({
        "type": "object",
        "required": ["score", "verdict"],
        "properties": {
            "score": {"type": "integer", "minimum": 0, "maximum": 10},
            "verdict": {"type": "string", "enum": ["pass", "fail"]},
        },
    }, fh)
with open(RUBRIC_PATH, "w", encoding="utf-8") as fh:
    fh.write("Score the artifact 0-10 and say pass or fail.\n")
with open(INPUT_PATH, "w", encoding="utf-8") as fh:
    fh.write("This is the artifact under review. It has a heading and one sentence.\n")

COMMON_ARGS = [
    "--model", "fake-judge-model",
    "--schema", SCHEMA_PATH,
    "--rubric", RUBRIC_PATH,
    "--input", INPUT_PATH,
]


def jsonl(*events):
    return "\n".join(json.dumps(e) for e in events) + "\n"


INIT_CLEAN = {"type": "system", "subtype": "init", "tools": [], "mcp_servers": []}
INIT_LEAKED = {"type": "system", "subtype": "init", "tools": ["Bash"], "mcp_servers": []}


def result_event(is_error=False, structured_output=None, text=""):
    evt = {"type": "result", "is_error": is_error,
           "usage": {"input_tokens": 100, "output_tokens": 20,
                      "cache_read_input_tokens": 5, "cache_creation_input_tokens": 0},
           "total_cost_usd": 0.001}
    if structured_output is not None:
        evt["structured_output"] = structured_output
    if text:
        evt["result"] = text
    return evt


def rate_limit_event(status="rejected"):
    return {"type": "rate_limit_event",
            "rate_limit_info": {"status": status, "resetsAt": 1790000000,
                                 "rateLimitType": "five_hour", "isUsingOverage": False}}


VALID_VERDICT = {"score": 7, "verdict": "pass"}


def run_judge(extra_args, stream_text=None, fake_exit=0, sleep_s=None, timeout=None):
    """Invoke judge.py as a subprocess with the fake claude first on PATH. Returns
    (proc, record_dir) -- record_dir has argv.json/env.json/cwd.txt/stdin.txt written
    by the fake claude, IF it was actually invoked (not on --dry)."""
    record_dir = tempfile.mkdtemp(dir=RECORDS_ROOT)
    env = dict(os.environ)
    env["PATH"] = FAKE_BIN + os.pathsep + env.get("PATH", "")
    env["OSFORGE_JUDGE_FAKE_RECORD_DIR"] = record_dir
    env["OSFORGE_JUDGE_FAKE_EXIT"] = str(fake_exit)
    if stream_text is not None:
        stream_path = os.path.join(record_dir, "stream.jsonl")
        with open(stream_path, "w", encoding="utf-8") as fh:
            fh.write(stream_text)
        env["OSFORGE_JUDGE_FAKE_STREAM"] = stream_path
    if sleep_s is not None:
        env["OSFORGE_JUDGE_FAKE_SLEEP"] = str(sleep_s)
    args = [sys.executable, JUDGE] + COMMON_ARGS + extra_args
    if timeout is not None:
        args += ["--timeout", str(timeout)]
    proc = subprocess.run(args, env=env, capture_output=True, text=True)
    return proc, record_dir


def parse_stdout(proc):
    try:
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


# =============================================================== Case 1: --dry and a real run

section("Case 1 -- --dry and a real call build the same isolated recipe")

proc, _ = run_judge(["--dry"])
check("--dry exits 0", proc.returncode == 0, "rc=%s stderr=%s" % (proc.returncode, proc.stderr))
dry = parse_stdout(proc)
check("--dry prints one JSON line", dry is not None, proc.stdout)

if dry is not None:
    argv = dry.get("argv") or []
    pairs = list(zip(argv, argv[1:]))
    check("argv has --tools \"\"", ("--tools", "") in pairs, argv)
    check("argv has --setting-sources \"\"", ("--setting-sources", "") in pairs, argv)
    check("argv has --strict-mcp-config", "--strict-mcp-config" in argv, argv)
    check("argv has --permission-mode default", ("--permission-mode", "default") in pairs, argv)
    check("argv has --json-schema", "--json-schema" in argv, argv)
    check("argv has --model", "--model" in argv, argv)
    check("argv never has --bare", "--bare" not in argv, argv)
    check("argv never has --dangerously-skip-permissions",
          "--dangerously-skip-permissions" not in argv, argv)
    env = dry.get("env") or {}
    check("env has CLAUDE_CODE_DISABLE_CLAUDE_MDS", env.get("CLAUDE_CODE_DISABLE_CLAUDE_MDS") == "1", env)
    check("env has CLAUDE_CODE_DISABLE_AUTO_MEMORY", env.get("CLAUDE_CODE_DISABLE_AUTO_MEMORY") == "1", env)
    dry_cwd = dry.get("cwd")
    check("dry cwd is cleaned up afterwards", bool(dry_cwd) and not os.path.exists(dry_cwd), dry_cwd)

success_stream = jsonl(INIT_CLEAN, result_event(structured_output=VALID_VERDICT))
proc, record_dir = run_judge([], stream_text=success_stream)
check("a real successful call exits 0", proc.returncode == 0, "rc=%s stderr=%s" % (proc.returncode, proc.stderr))
out = parse_stdout(proc)
check("real call also prints one JSON line", out is not None, proc.stdout)
if out is not None:
    check("verdict matches structured_output", out.get("verdict") == VALID_VERDICT, out)

argv_path = os.path.join(record_dir, "argv.json")
if os.path.exists(argv_path):
    real_argv = json.load(open(argv_path, encoding="utf-8"))
    real_pairs = list(zip(real_argv, real_argv[1:]))
    check("fake claude received --tools \"\"", ("--tools", "") in real_pairs, real_argv)
    check("fake claude received --setting-sources \"\"", ("--setting-sources", "") in real_pairs, real_argv)
    check("fake claude received --strict-mcp-config", "--strict-mcp-config" in real_argv, real_argv)
    check("fake claude never received --bare", "--bare" not in real_argv, real_argv)
    check("fake claude never received --dangerously-skip-permissions",
          "--dangerously-skip-permissions" not in real_argv, real_argv)
else:
    bad("fake claude recorded argv.json", "missing: %s" % argv_path)

env_path = os.path.join(record_dir, "env.json")
if os.path.exists(env_path):
    real_env = json.load(open(env_path, encoding="utf-8"))
    check("real call env has CLAUDE_CODE_DISABLE_CLAUDE_MDS",
          real_env.get("CLAUDE_CODE_DISABLE_CLAUDE_MDS") == "1")
    check("real call env has CLAUDE_CODE_DISABLE_AUTO_MEMORY",
          real_env.get("CLAUDE_CODE_DISABLE_AUTO_MEMORY") == "1")
else:
    bad("fake claude recorded env.json", "missing: %s" % env_path)

stdin_path = os.path.join(record_dir, "stdin.txt")
if os.path.exists(stdin_path):
    check("claude's stdin was empty (/dev/null)", open(stdin_path, encoding="utf-8").read() == "")
else:
    bad("fake claude recorded stdin.txt", "missing: %s" % stdin_path)

cwd_path = os.path.join(record_dir, "cwd.txt")
if os.path.exists(cwd_path):
    real_cwd = open(cwd_path, encoding="utf-8").read()
    check("call ran in a fresh temp dir, not the repo", bool(real_cwd) and real_cwd != REPO, real_cwd)
    check("temp cwd no longer exists after the call", not os.path.exists(real_cwd), real_cwd)
else:
    bad("fake claude recorded cwd.txt", "missing: %s" % cwd_path)

# =============================================================== Case 2: isolation violated

section("Case 2 -- system/init with leaked tools")

leak_stream = jsonl(INIT_LEAKED, result_event(structured_output=VALID_VERDICT))
proc, _ = run_judge([], stream_text=leak_stream)
check("leaked tools -> exit 3", proc.returncode == 3, proc.returncode)
out = parse_stdout(proc)
if out is not None:
    check("error names the isolation leak", "isolation violated: tools" in (out.get("error") or ""), out)
    check("ok is false", out.get("ok") is False, out)
else:
    bad("leaked-tools call prints JSON", proc.stdout)

# --json-schema makes Claude Code expose one synthetic tool, StructuredOutput, to carry the
# verdict (seen live in E-J0, 2026-09-29). It is the schema channel, not a leak -- but it must
# not become a door for anything else.
INIT_SCHEMA_ONLY = {"type": "system", "subtype": "init", "tools": ["StructuredOutput"], "mcp_servers": []}
proc, _ = run_judge([], stream_text=jsonl(INIT_SCHEMA_ONLY, result_event(structured_output=VALID_VERDICT)))
check("StructuredOutput alone is not a leak -> exit 0", proc.returncode == 0, proc.returncode)

INIT_SCHEMA_PLUS = {"type": "system", "subtype": "init", "tools": ["StructuredOutput", "Bash"], "mcp_servers": []}
proc, _ = run_judge([], stream_text=jsonl(INIT_SCHEMA_PLUS, result_event(structured_output=VALID_VERDICT)))
check("StructuredOutput + another tool -> exit 3", proc.returncode == 3, proc.returncode)

# =============================================================== Case 3: structured_output validation

section("Case 3 -- structured_output validity")

valid_stream = jsonl(INIT_CLEAN, result_event(structured_output=VALID_VERDICT))
proc, _ = run_judge([], stream_text=valid_stream)
check("valid structured_output -> exit 0", proc.returncode == 0, proc.returncode)

missing_stream = jsonl(INIT_CLEAN, result_event(structured_output=None))
proc, _ = run_judge([], stream_text=missing_stream)
check("missing structured_output -> exit 2", proc.returncode == 2, proc.returncode)
out = parse_stdout(proc)
if out is not None:
    check("error says structured_output missing", "missing" in (out.get("error") or ""), out)

required_missing_stream = jsonl(INIT_CLEAN, result_event(structured_output={"score": 5}))
proc, _ = run_judge([], stream_text=required_missing_stream)
check("missing required field -> exit 2", proc.returncode == 2, proc.returncode)
out = parse_stdout(proc)
if out is not None:
    check("error names the missing property",
          "verdict" in (out.get("error") or "") and "missing required" in (out.get("error") or ""), out)

enum_invalid_stream = jsonl(INIT_CLEAN, result_event(structured_output={"score": 5, "verdict": "maybe"}))
proc, _ = run_judge([], stream_text=enum_invalid_stream)
check("invalid enum value -> exit 2", proc.returncode == 2, proc.returncode)

wrong_type_stream = jsonl(INIT_CLEAN, result_event(structured_output={"score": "five", "verdict": "pass"}))
proc, _ = run_judge([], stream_text=wrong_type_stream)
check("wrong type -> exit 2", proc.returncode == 2, proc.returncode)

# =============================================================== Case 4: quota rejection

section("Case 4 -- quota rejection (exit 75)")

quota_stream = jsonl(INIT_CLEAN, rate_limit_event(status="rejected"),
                      result_event(is_error=True, text="5-hour limit reached"))
proc, _ = run_judge([], stream_text=quota_stream)
check("rejected rate_limit_event + is_error -> exit 75", proc.returncode == 75, proc.returncode)
out = parse_stdout(proc)
if out is not None:
    check("rate_limit.status is rejected", (out.get("rate_limit") or {}).get("status") == "rejected", out)
    check("error mentions quota", "quota" in (out.get("error") or ""), out)

quota_text_stream = jsonl(INIT_CLEAN, result_event(is_error=True, text="Claude AI usage limit reached."))
proc, _ = run_judge([], stream_text=quota_text_stream)
check("is_error + rate-limit wording, no event -> exit 75", proc.returncode == 75, proc.returncode)

generic_error_stream = jsonl(INIT_CLEAN, result_event(is_error=True, text="internal server error"))
proc, _ = run_judge([], stream_text=generic_error_stream)
check("is_error without quota signal -> exit 3 (not 75)", proc.returncode == 3, proc.returncode)

# =============================================================== Case 5: CLI timeout

section("Case 5 -- CLI timeout")

proc, record_dir = run_judge([], stream_text=jsonl(INIT_CLEAN), sleep_s=3, timeout=1)
check("timeout -> exit 3", proc.returncode == 3, proc.returncode)
out = parse_stdout(proc)
if out is not None:
    check("error mentions timeout", "timeout" in (out.get("error") or ""), out)
cwd_path = os.path.join(record_dir, "cwd.txt")
if os.path.exists(cwd_path):
    real_cwd = open(cwd_path, encoding="utf-8").read()
    check("temp cwd removed even after a timeout", not os.path.exists(real_cwd), real_cwd)
else:
    bad("fake claude recorded cwd.txt before sleeping", "missing: %s" % cwd_path)

# =============================================================== Case 6: schema validator table

section("Case 6 -- validate_schema() table (>= 20 cases)")

OBJ_SCHEMA = {
    "type": "object",
    "required": ["score", "verdict"],
    "properties": {
        "score": {"type": "integer", "minimum": 0, "maximum": 10},
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
    },
}

NESTED_SCHEMA = {
    "type": "object",
    "required": ["items"],
    "properties": {
        "items": {"type": "array", "items": {
            "type": "object", "required": ["label"],
            "properties": {"label": {"type": "string"}},
        }},
    },
}

# (name, instance, schema, expect_valid)
CASES = [
    ("object: valid", {"score": 5, "verdict": "pass"}, OBJ_SCHEMA, True),
    ("object: wrong root type", "not an object", OBJ_SCHEMA, False),
    ("object: missing one required field", {"score": 5}, OBJ_SCHEMA, False),
    ("object: missing both required fields", {}, OBJ_SCHEMA, False),
    ("object: extra property is tolerated", {"score": 5, "verdict": "pass", "note": "x"}, OBJ_SCHEMA, True),
    ("enum: valid value", "pass", {"type": "string", "enum": ["pass", "fail"]}, True),
    ("enum: invalid value", "maybe", {"type": "string", "enum": ["pass", "fail"]}, False),
    ("type string: valid", "hello", {"type": "string"}, True),
    ("type string: got integer", 5, {"type": "string"}, False),
    ("type integer: valid", 5, {"type": "integer"}, True),
    ("type integer: got float", 5.5, {"type": "integer"}, False),
    ("type integer: bool is not an integer", True, {"type": "integer"}, False),
    ("type number: int accepted", 5, {"type": "number"}, True),
    ("type number: float accepted", 5.5, {"type": "number"}, True),
    ("type number: bool is not a number", False, {"type": "number"}, False),
    ("type boolean: valid", True, {"type": "boolean"}, True),
    ("type boolean: got string", "true", {"type": "boolean"}, False),
    ("type null: valid", None, {"type": "null"}, True),
    ("type null: got empty string", "", {"type": "null"}, False),
    ("type array: valid", [1, 2, 3], {"type": "array"}, True),
    ("type array: got object", {"a": 1}, {"type": "array"}, False),
    ("minimum: at boundary passes", 0, {"type": "integer", "minimum": 0}, True),
    ("minimum: below boundary fails", -1, {"type": "integer", "minimum": 0}, False),
    ("maximum: at boundary passes", 10, {"type": "integer", "maximum": 10}, True),
    ("maximum: above boundary fails", 11, {"type": "integer", "maximum": 10}, False),
    ("items: every element valid", {"items": [{"label": "a"}, {"label": "b"}]}, NESTED_SCHEMA, True),
    ("items: one element missing required field", {"items": [{"label": "a"}, {}]}, NESTED_SCHEMA, False),
    ("items: one element wrong type", {"items": [{"label": "a"}, {"label": 5}]}, NESTED_SCHEMA, False),
    ("nested properties: root missing required array", {}, NESTED_SCHEMA, False),
    ("empty schema: anything passes", {"whatever": True}, {}, True),
]

check("case table has >= 20 rows", len(CASES) >= 20, len(CASES))

for name, instance, schema, expect_valid in CASES:
    errors = judge.validate_schema(instance, schema)
    got_valid = len(errors) == 0
    check("validate_schema: %s" % name, got_valid == expect_valid,
          "errors=%r" % errors if got_valid != expect_valid else "")

shutil.rmtree(WORK, ignore_errors=True)

print("")
if FAIL:
    print("FAILED: %d of %d checks" % (FAIL, PASS + FAIL))
    sys.exit(1)
print("PASSED: %d/%d checks" % (PASS, PASS + FAIL))
PY

exit $?
