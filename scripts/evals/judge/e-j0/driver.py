#!/usr/bin/env python3
"""
driver.py -- E-J0, the isolation sanity experiment for scripts/lib/judge.py
(docs/intake/laya/SPEC-L02-juiz-isolado.md, section "Experimento E-J0").

Four short checks, each a single real call to `claude` through judge.py:
  1. ANTHROPIC_API_KEY absent from the environment -> the call still completes (proves
     subscription usage, not API billing).
  2. system/init reports empty tools and mcp_servers (judge.py already refuses the call
     otherwise with exit 3 -- this just confirms a normal probe clears it).
  3. A contamination probe: a question whose answer only exists in the user's own CLAUDE.md
     (e.g. the mandatory route line). The judge must NOT know it.
  4. A valid structured_output, noting whether a rate_limit_event turned up (feeds L-01).

Default is --dry: builds and prints each probe's judge.py invocation, calls no model, spends
nothing. Real calls (1-3 short subscription messages) require explicit opt-in, decided by the
user, not by this script:

    python3 driver.py --run --model <id>

This is prepared, not run: do not pass --run without the user's authorization for that run.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
JUDGE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "lib", "judge.py"))
RUBRIC = os.path.join(HERE, "rubric.md")
SCHEMA_YESNO = os.path.join(HERE, "schemas", "probe-yesno.json")
SCHEMA_FREEFORM = os.path.join(HERE, "schemas", "probe-freeform.json")
INPUT_TRIVIAL = os.path.join(HERE, "inputs", "probe-trivial.md")
INPUT_CONTAMINATION = os.path.join(HERE, "inputs", "probe-contamination.md")

# Best-effort substrings: if the judge's free-text answer contains one of these it likely saw
# the user's own CLAUDE.md conventions. This only flags the obvious case -- a human still has
# to read the answer, per SPEC-L02's own "if item 3 fails, do not adopt the judge" fallback.
LEAK_MARKERS = ("route:", "@orchestrator", "skill:", "detect", "claude.md")

PROBES = [
    {"id": 1, "name": "no ANTHROPIC_API_KEY -> call still completes",
     "input": INPUT_TRIVIAL, "schema": SCHEMA_YESNO},
    {"id": 2, "name": "system/init reports empty tools/mcp_servers",
     "input": INPUT_TRIVIAL, "schema": SCHEMA_YESNO},
    {"id": 3, "name": "contamination probe: judge must not know the user's CLAUDE.md",
     "input": INPUT_CONTAMINATION, "schema": SCHEMA_FREEFORM},
    {"id": 4, "name": "valid structured_output; note any rate_limit_event",
     "input": INPUT_TRIVIAL, "schema": SCHEMA_YESNO},
]


def build_cmd(probe, model, timeout, dry):
    cmd = [sys.executable, JUDGE, "--model", model, "--schema", probe["schema"],
           "--rubric", RUBRIC, "--input", probe["input"], "--timeout", str(timeout)]
    if dry:
        cmd.append("--dry")
    return cmd


def run_probe(probe, model, timeout, dry):
    cmd = build_cmd(probe, model, timeout, dry)
    # Every probe in this experiment runs without ANTHROPIC_API_KEY: probe 1 is specifically
    # about proving that works, and running the other three the same way keeps all four under
    # one condition instead of switching environments mid-experiment.
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
    out = None
    try:
        out = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        pass
    return proc, out


def report(probe, proc, out, dry):
    print("")
    print("## Probe %d -- %s" % (probe["id"], probe["name"]))
    if dry:
        print("  DRY: not executed. This is what --run would send.")
        if out:
            print("  argv: %s" % json.dumps(out.get("argv")))
            print("  env additions: %s" % json.dumps(out.get("env")))
        else:
            print("  (judge.py --dry did not return parseable JSON: %r)" % proc.stdout)
        return

    print("  exit code: %d" % proc.returncode)
    if out is None:
        print("  could not parse judge.py stdout: %r" % proc.stdout)
        print("  stderr: %s" % proc.stderr)
        return

    if probe["id"] == 1:
        if proc.returncode == 0:
            print("  PASS: call completed with ANTHROPIC_API_KEY unset")
        else:
            print("  FAIL: call did not complete (exit %d, error=%s)"
                  % (proc.returncode, out.get("error")))
    elif probe["id"] == 2:
        isolation = out.get("isolation") or {}
        clean = set(isolation.get("tools") or []) <= {"StructuredOutput"} and isolation.get("mcp_servers") == []
        if clean:
            print("  PASS: system/init reported no tools beyond StructuredOutput, mcp_servers=[]")
        else:
            print("  FAIL: isolation leaked: %s" % isolation)
    elif probe["id"] == 3:
        answer = (out.get("verdict") or {}).get("answer", "")
        print("  answer: %r" % answer)
        hit = [m for m in LEAK_MARKERS if m in answer.lower()]
        if hit:
            print("  SUSPICIOUS (possible leak, markers=%s) -- read the answer yourself" % hit)
        else:
            print("  no obvious leak marker (still needs a human read before trusting it)")
    elif probe["id"] == 4:
        print("  verdict: %s" % out.get("verdict"))
        print("  rate_limit: %s" % out.get("rate_limit"))
        print("  note: 'allowed'/resets_at=0 here also means no rate_limit_event was seen at "
              "all -- this field alone cannot tell the two apart; check judge.py's raw stream "
              "if that distinction matters for L-01.")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--run", action="store_true",
                         help="make the 4 real calls, spending subscription quota. Requires --model.")
    parser.add_argument("--model", help="model id for `claude --model`; required with --run")
    parser.add_argument("--timeout", type=float, default=60.0,
                         help="seconds per call before judge.py kills it (default: %(default)s)")
    args = parser.parse_args(argv)

    if args.run and not args.model:
        parser.error("--run requires --model")

    dry = not args.run
    model = args.model or "<model-not-set-in-dry-preview>"
    if dry:
        print("DRY RUN: no model will be called. Pass --run --model <id> to make the 4 real "
              "calls -- only after the user has authorized that run.")

    exit_code = 0
    for probe in PROBES:
        proc, out = run_probe(probe, model, args.timeout, dry)
        report(probe, proc, out, dry)
        if not dry and proc.returncode not in (0,):
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
