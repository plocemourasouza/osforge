#!/usr/bin/env python3
"""
judge.py -- an isolated `claude` inference call, on the subscription quota, used as a
model-based judge (B-029, spec docs/intake/laya/SPEC-L02-juiz-isolado.md).

The eval harnesses (stream_assert.py) measure *trigger*: did the right skill/agent fire.
They cannot measure *quality*: did a review find the right problem, is a plan proportional,
did a reviewer go lenient. That needs a judge -- a model call that takes an artifact and a
rubric and returns a structured verdict.

Calling `claude` the way the trigger harnesses do (EV-O01: `--dangerously-skip-permissions`,
full tool access, the user's own ~/.claude) would be wrong here: it would load the user's
CLAUDE.md (route line, hooks, MCPs), give the model tools it has no business using for a pure
judgment call, and return free text instead of a structured verdict. This module builds the
isolated recipe instead:

  cwd  = a fresh, empty mkdtemp() directory, removed afterwards even on timeout.
  env  += CLAUDE_CODE_DISABLE_CLAUDE_MDS=1, CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
  argv: -p "<artifact + instruction>" --model <id> --output-format stream-json --verbose
        --tools "" --setting-sources "" --strict-mcp-config --permission-mode default
        --json-schema <schema> --append-system-prompt "<non-interactive directive + rubric>"
  stdin: /dev/null

Never: --bare (forces API-key billing, EV-C05), --dangerously-skip-permissions, --mcp-config,
a high --max-turns.

Isolation is VERIFIED on every real call, not presumed: the `system/init` event (EV-C11) must
report no `tools` beyond the `StructuredOutput` channel that --json-schema adds, and empty
`mcp_servers`, or the call is rejected before its structured_output
is even looked at.

CLI:
    judge.py --model ID --schema FILE --rubric FILE --input FILE [--timeout SECONDS] [--dry]

Output: exactly one line of JSON on stdout, always. Exit codes:
    0   valid verdict, matching the schema
    2   structured_output missing, or present but outside the schema
    3   CLI error (`is_error` not attributable to quota), timeout, or isolation violated
    75  quota rejection (same rule L-01 gives `stream_assert.py run-status == quota`,
        mirrored here rather than imported: a `result` event with `is_error`, plus either
        a `rate_limit_event` whose `rate_limit_info.status == "rejected"`, or rate-limit
        wording in the result/error text. No heuristic beyond those two.)

No retries (a schema-forced call does not need one; an error should not spend quota twice).
Sequential by default -- OSFORGE_JUDGE_CONCURRENCY (default 1) caps how many judge.py
processes run the model concurrently, for callers that dispatch a batch.

Python 3 stdlib only.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

# stream_assert.py lives next to this file (scripts/lib/); sys.path[0] is already that
# directory when judge.py is run directly (`python3 .../judge.py`), same as every caller does.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stream_assert import is_quota_result  # noqa: E402 -- the sys.path insert above must run first

DEFAULT_TIMEOUT = 120.0
DEFAULT_CONCURRENCY = 1
# Tools system/init may list without breaking isolation: the channel --json-schema adds itself.
SCHEMA_TOOLS = frozenset({"StructuredOutput"})
LOCK_DIR_DEFAULT = os.path.join(tempfile.gettempdir(), "osforge-judge-locks")

# EV-L03-style directive, written in our own words: no questions, no proposed actions --
# there is no one on the other end to answer them.
NON_INTERACTIVE_DIRECTIVE = (
    "You are running as an isolated evaluation judge inside an automated pipeline, not as an "
    "interactive assistant. You have no tools, no memory of any other session, and no context "
    "beyond the rubric below and the artifact given as the user message. Never ask a "
    "clarifying question, never propose a next step, and never request confirmation: there is "
    "no one able to answer. Read the rubric, then read the artifact, and respond with exactly "
    "one JSON object matching the schema you were given -- nothing else: no prose, no markdown "
    "fences, no explanation before or after the object."
)



# --------------------------------------------------------------------------- schema validator

def _type_ok(instance, type_name):
    if type_name == "object":
        return isinstance(instance, dict)
    if type_name == "array":
        return isinstance(instance, list)
    if type_name == "string":
        return isinstance(instance, str)
    if type_name == "boolean":
        return isinstance(instance, bool)
    if type_name == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if type_name == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if type_name == "null":
        return instance is None
    return True  # unknown type keyword: tolerate rather than fail on it


def validate_schema(instance, schema, path="$"):
    """Pure-Python validator for the local subset: type, required, enum, properties, items,
    minimum, maximum. Returns a list of human-readable errors (empty = valid). One node's
    errors stop at the first structural mismatch (wrong type, bad enum) rather than piling on
    consequential errors underneath it."""
    errors = []
    if not isinstance(schema, dict):
        return errors

    if "enum" in schema:
        allowed = schema["enum"]
        if instance not in allowed:
            errors.append("%s: value %r not in enum %r" % (path, instance, allowed))
            return errors

    if "type" in schema:
        declared = schema["type"]
        names = declared if isinstance(declared, list) else [declared]
        if not any(_type_ok(instance, t) for t in names):
            errors.append("%s: expected type %r, got %s" % (path, declared, type(instance).__name__))
            return errors

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append("%s.%s: missing required property" % (path, key))
        for key, subschema in schema.get("properties", {}).items():
            if key in instance:
                errors.extend(validate_schema(instance[key], subschema, "%s.%s" % (path, key)))

    if isinstance(instance, list):
        items_schema = schema.get("items")
        if isinstance(items_schema, dict):
            for i, item in enumerate(instance):
                errors.extend(validate_schema(item, items_schema, "%s[%d]" % (path, i)))

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append("%s: %r < minimum %r" % (path, instance, schema["minimum"]))
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append("%s: %r > maximum %r" % (path, instance, schema["maximum"]))

    return errors


# --------------------------------------------------------------------------- recipe construction

def build_prompt(artifact_text):
    return (
        "## Artifact under evaluation\n\n"
        + artifact_text.strip()
        + "\n\n## Instruction\n\nEvaluate the artifact above using the rubric given in your "
          "system prompt, and return the verdict as a single JSON object matching the "
          "required schema."
    )


def build_system_prompt(rubric_text):
    return NON_INTERACTIVE_DIRECTIVE + "\n\n## Rubric\n\n" + rubric_text.strip()


def build_argv(model, prompt_text, system_prompt_text, schema_text):
    """The full command, argv[0] included -- this exact list is what gets hashed into
    argv_sha256 and, on --dry, printed back for inspection."""
    return [
        "claude", "-p", prompt_text,
        "--model", model,
        "--output-format", "stream-json",
        "--verbose",
        "--tools", "",
        "--setting-sources", "",
        "--strict-mcp-config",
        "--permission-mode", "default",
        "--json-schema", schema_text,
        "--append-system-prompt", system_prompt_text,
    ]


def build_env():
    env = os.environ.copy()
    env["CLAUDE_CODE_DISABLE_CLAUDE_MDS"] = "1"
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    return env


ENV_ADDITIONS = ("CLAUDE_CODE_DISABLE_CLAUDE_MDS", "CLAUDE_CODE_DISABLE_AUTO_MEMORY")


def argv_sha256(argv):
    return hashlib.sha256(json.dumps(argv, ensure_ascii=False).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- concurrency gate

def acquire_slot():
    """Best-effort cross-process semaphore capping concurrent model calls at
    OSFORGE_JUDGE_CONCURRENCY (default 1). Degrades to no enforcement if fcntl is
    unavailable (non-POSIX) rather than failing the call -- a non-critical dependency."""
    try:
        import fcntl
    except ImportError:
        return None
    try:
        limit = max(1, int(os.environ.get("OSFORGE_JUDGE_CONCURRENCY", str(DEFAULT_CONCURRENCY))))
    except ValueError:
        limit = DEFAULT_CONCURRENCY
    lock_dir = os.environ.get("OSFORGE_JUDGE_LOCK_DIR", LOCK_DIR_DEFAULT)
    try:
        os.makedirs(lock_dir, exist_ok=True)
    except OSError:
        return None
    while True:
        for i in range(limit):
            path = os.path.join(lock_dir, "slot-%d.lock" % i)
            try:
                fh = open(path, "w")
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return fh
            except (OSError, IOError):
                try:
                    fh.close()
                except OSError:
                    pass
        time.sleep(0.2)


def release_slot(fh):
    if fh is None:
        return
    try:
        import fcntl
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
    except (ImportError, OSError):
        pass
    try:
        fh.close()
    except OSError:
        pass


# --------------------------------------------------------------------------- stream parsing

def parse_stream(text):
    """Best-effort line-by-line JSON parse of a stream-json transcript. Non-JSON and
    non-object lines are skipped silently, same tolerance as stream_assert.py."""
    events = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            evt = json.loads(line)
        except ValueError:
            continue
        if isinstance(evt, dict):
            events.append(evt)
    return events


def find_init(events):
    for evt in events:
        if evt.get("type") == "system" and evt.get("subtype") == "init":
            return evt.get("tools"), evt.get("mcp_servers")
    return None, None


def find_last_rate_limit(events):
    info = None
    for evt in events:
        if evt.get("type") == "rate_limit_event":
            candidate = evt.get("rate_limit_info")
            if isinstance(candidate, dict):
                info = candidate
    return info


def find_result(events):
    result = None
    for evt in events:
        if evt.get("type") == "result":
            result = evt
    return result


def rate_limit_out(info):
    if not isinstance(info, dict):
        return {"status": "allowed", "resets_at": 0}
    status = info.get("status", "allowed")
    resets_at = info.get("resetsAt", info.get("resets_at", 0))
    return {"status": status, "resets_at": resets_at}


def usage_out(result_event):
    usage = (result_event or {}).get("usage")
    if not isinstance(usage, dict):
        usage = {}
    return {
        "input": usage.get("input_tokens", 0) or 0,
        "output": usage.get("output_tokens", 0) or 0,
        "cache_read": usage.get("cache_read_input_tokens", 0) or 0,
        "cache_create": usage.get("cache_creation_input_tokens", 0) or 0,
    }


def is_quota(result_event, rate_limit_info):
    """The B1 rule (SPEC-L01 Part B): a `result` event with `is_error`, AND EITHER the last
    rate_limit_info says rejected, OR the result carries rate-limit wording. No other
    heuristic. Delegates to stream_assert.is_quota_result() -- the canonical implementation --
    so this and `stream_assert.py run-status` cannot drift apart."""
    return is_quota_result(result_event, rate_limit_info)


# --------------------------------------------------------------------------- CLI

def parse_args(argv):
    parser = argparse.ArgumentParser(prog="judge.py", description=__doc__.split("\n\n")[0])
    parser.add_argument("--model", required=True, help="model id passed to `claude --model`")
    parser.add_argument("--schema", required=True, help="path to the JSON Schema file")
    parser.add_argument("--rubric", required=True, help="path to the rubric text/markdown file")
    parser.add_argument("--input", required=True, help="path to the artifact being judged")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                         help="seconds before the CLI call is killed (default: %(default)s)")
    parser.add_argument("--dry", action="store_true",
                         help="print the effective argv/env and exit 0 without calling the model")
    return parser.parse_args(argv)


def _read_text(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def emit(**fields):
    print(json.dumps(fields, ensure_ascii=False))


def main(argv):
    args = parse_args(argv)

    try:
        rubric_text = _read_text(args.rubric)
        input_text = _read_text(args.input)
        schema_text = _read_text(args.schema)
        schema = json.loads(schema_text)
    except (OSError, ValueError) as exc:
        emit(ok=False, model=args.model, error="setup failed: %s" % exc)
        return 3

    prompt_text = build_prompt(input_text)
    system_prompt_text = build_system_prompt(rubric_text)
    cmd = build_argv(args.model, prompt_text, system_prompt_text, schema_text)
    digest = argv_sha256(cmd)

    cwd = tempfile.mkdtemp(prefix="osforge-judge-")
    try:
        if args.dry:
            emit(ok=True, dry=True, model=args.model, argv=cmd,
                 env={k: "1" for k in ENV_ADDITIONS}, cwd=cwd, argv_sha256=digest)
            return 0

        slot = acquire_slot()
        try:
            env = build_env()
            timed_out = False
            stdout_text = ""
            try:
                proc = subprocess.run(
                    cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, timeout=args.timeout,
                )
                stdout_text = proc.stdout or ""
            except subprocess.TimeoutExpired as exc:
                timed_out = True
                stdout_text = exc.stdout or ""
            except OSError as exc:
                emit(ok=False, model=args.model, argv_sha256=digest,
                     error="could not run claude: %s" % exc)
                return 3
        finally:
            release_slot(slot)

        events = parse_stream(stdout_text)
        init_tools, init_mcp = find_init(events)
        isolation = {"tools": init_tools, "mcp_servers": init_mcp}

        if timed_out:
            emit(ok=False, model=args.model, argv_sha256=digest, isolation=isolation,
                 error="timeout after %ss" % args.timeout)
            return 3

        # --json-schema exposes one synthetic tool carrying the verdict; anything else leaked.
        if [t for t in (init_tools or []) if t not in SCHEMA_TOOLS]:
            emit(ok=False, model=args.model, argv_sha256=digest, isolation=isolation,
                 error="isolation violated: tools")
            return 3
        if init_mcp:
            emit(ok=False, model=args.model, argv_sha256=digest, isolation=isolation,
                 error="isolation violated: mcp_servers")
            return 3

        rate_limit_info = find_last_rate_limit(events)
        result_event = find_result(events)
        rate_limit = rate_limit_out(rate_limit_info)
        usage = usage_out(result_event)
        cost = (result_event or {}).get("total_cost_usd")

        if result_event is None:
            emit(ok=False, model=args.model, argv_sha256=digest, isolation=isolation,
                 usage=usage, rate_limit=rate_limit, error="no result event in stream")
            return 3

        if result_event.get("is_error"):
            if is_quota(result_event, rate_limit_info):
                emit(ok=False, model=args.model, argv_sha256=digest, isolation=isolation,
                     usage=usage, rate_limit=rate_limit,
                     total_cost_usd_equivalent=cost, error="quota: rejected")
                return 75
            emit(ok=False, model=args.model, argv_sha256=digest, isolation=isolation,
                 usage=usage, rate_limit=rate_limit, total_cost_usd_equivalent=cost,
                 error="cli error: %s" % result_event.get("result", result_event.get("error", "")))
            return 3

        structured_output = result_event.get("structured_output")
        if structured_output is None:
            emit(ok=False, model=args.model, argv_sha256=digest, isolation=isolation,
                 usage=usage, rate_limit=rate_limit, total_cost_usd_equivalent=cost,
                 error="structured_output missing")
            return 2

        errors = validate_schema(structured_output, schema)
        if errors:
            emit(ok=False, model=args.model, argv_sha256=digest, isolation=isolation,
                 usage=usage, rate_limit=rate_limit, total_cost_usd_equivalent=cost,
                 error="structured_output failed schema validation: %s" % "; ".join(errors))
            return 2

        emit(ok=True, model=args.model, argv_sha256=digest, isolation=isolation,
             usage=usage, rate_limit=rate_limit, total_cost_usd_equivalent=cost,
             verdict=structured_output)
        return 0
    finally:
        shutil.rmtree(cwd, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
