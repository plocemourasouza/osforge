#!/usr/bin/env python3
"""driver.py -- outcome eval: does a skill's text change the quality of the answer?

Three arms per (skill, task), the ONLY difference being `--append-system-prompt`:
  A  control  -- a one-line neutral note (identical in all arms)
  B  current  -- the note + the current SKILL.md body (variants/<skill>.B.md)
  C  reduced  -- the note + the SKILL.md with the prompt audit's cuts (variants/<skill>.C.md)
The executor uses the judge.py isolation recipe (fresh mkdtemp cwd, CLAUDE_CODE_DISABLE_CLAUDE_MDS,
CLAUDE_CODE_DISABLE_AUTO_MEMORY, --setting-sources "", --strict-mcp-config, --tools "", stdin
/dev/null; never --bare, never --dangerously-skip-permissions). Each answer is graded by
scripts/lib/judge.py, blind: the judge sees only the task + the answer under a random id, and
judge calls run in shuffled order.

  python3 driver.py --dry                      # validate everything, print the plan; no model calls
  python3 driver.py --pilot --model <id>       # 1 executor + 1 judge call, print parsed results
  python3 driver.py --run --model <id> [--runs 3] [--concurrency 4]
  python3 driver.py --report <out.md> --model <id>
  ... --round r2 [--budget 40]                 # round 2: everything under r2/ (default round r1)
  ... --round r3 [--skip ponytail-ref]         # round 3: everything under r3/; ponytail-ref is optional

Real calls (--pilot/--run) are a human decision. Results are cached under results/ (gitignored)
and a re-run resumes: cached ok calls are not repeated. A quota rejection (judge exit 75, or the
same B1 rule on the executor stream) stops the run; everything not yet done is NOT RUN.
Python 3 stdlib only.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LIB = os.path.join(REPO, "scripts", "lib")
sys.path.insert(0, LIB)
import judge as J  # noqa: E402  (parse_stream, find_init, find_result, ..., build_env)
import stream_assert as SA  # noqa: E402  (record_rate_limit: persist rate-limit info to quota.json)

BASE = HERE  # round root: tasks/ rubrics/ schemas/ variants/ results/ live under it
RESULTS = os.path.join(HERE, "results")
QUOTA_FILE = os.path.expanduser("~/.osforge/quota.json")
QUOTA_STOP_PCT = 80
EXEC_TIMEOUT = 600.0
JUDGE_TIMEOUT = 420.0
ARMS = ("A", "B", "C")
NEUTRAL_NOTE = ("You are answering a single request in one turn. You have no tools and no files; "
                "answer in text.")

# skill -> tasks; each task: criteria ids in rubric order, the critical ones, seeded defect count
TASKS = {
    "clean-code": {
        "cc1": {"criteria": ["behavior", "simplified", "no_new_abstraction", "call_site", "proportionate"],
                "critical": ["behavior"]},
        "cc2": {"criteria": ["nesting", "duplication", "side_effect", "behavior", "no_new_abstraction",
                             "magic_numbers"], "critical": ["behavior"]},
        "cc3": {"criteria": ["root_cause", "fix_correct", "signature", "concise_explanation", "no_scope_creep"],
                "critical": ["root_cause", "fix_correct"]},
        "cc4": {"criteria": ["behavior", "comments_removed", "why_comment_kept", "dead_code_removed",
                             "no_additions", "accurate_list"], "critical": ["behavior"]},
    },
    "frontend-design": {
        "fd1": {"criteria": ["markup_valid", "brand_color", "typeface", "copy_verbatim", "mockup",
                             "audience_fit", "responsive", "accessible", "no_unneeded_questions"],
                "critical": ["markup_valid"]},
        "fd2": {"criteria": ["markup_valid", "plans_exact", "recommended", "toggle_works", "brand", "faq",
                             "tone_fit", "accessible", "responsive"], "critical": ["markup_valid"]},
        "fd3": {"criteria": ["markup_valid", "shell", "actions", "explains_value", "is_empty", "brand",
                             "responsive", "accessible"], "critical": ["markup_valid"]},
        "fd4": {"criteria": ["handles_ambiguity", "questions_focused", "markup_valid", "coherent",
                             "low_friction"], "critical": ["handles_ambiguity"]},
    },
    "adversarial-review": {
        "ar1": {"criteria": ["found_D1", "found_D2", "found_D3", "severity_right", "no_manufactured_high",
                             "actionable", "prioritized"], "critical": ["no_manufactured_high"], "seeded": 3},
        "ar2": {"criteria": ["no_blocking_findings", "clear_verdict", "shows_work", "low_noise"],
                "critical": ["no_blocking_findings"], "seeded": 0},
        "ar3": {"criteria": ["found_D1", "severity_right", "found_drop_timing", "no_manufactured_high",
                             "actionable"], "critical": ["found_D1", "no_manufactured_high"], "seeded": 1},
        "ar4": {"criteria": ["found_D1", "severity_right", "fix_right", "no_manufactured_high", "prioritized"],
                "critical": ["found_D1", "no_manufactured_high"], "seeded": 1},
    },
}
SKILL_EXTRA_RUBRIC = {"frontend-design": "_fd_tells.md", "adversarial-review": "_ar_counts.md"}
VARIANT_ARMS = {s: ("B", "C") for s in TASKS}  # arms whose system prompt comes from variants/
TRUTH_IN_RUBRIC = False  # r2: tasks/<target>/<task>.truth.md is appended to the judge rubric
PILOT = ("clean-code", "cc3")
ROUND = "r1"
SPEC = None    # r2+: the tasks_<round> module
TASK_DIRS = {}  # r3+: target -> tasks/ subdir it reads prompts and truths from (default: itself)


def configure(round_name):
    """Point every path and table at one round. r1 = the committed round-1 layout, unchanged."""
    global BASE, RESULTS, TASKS, SKILL_EXTRA_RUBRIC, VARIANT_ARMS, TRUTH_IN_RUBRIC, PILOT, ROUND, SPEC, TASK_DIRS
    ROUND = round_name
    if round_name == "r1":
        return
    sys.path.insert(0, HERE)
    import importlib  # noqa: E402
    R = importlib.import_module("tasks_" + round_name)  # tasks_r2, tasks_r3
    BASE = os.path.join(HERE, round_name)
    RESULTS = os.path.join(BASE, "results")
    TASKS, SKILL_EXTRA_RUBRIC, VARIANT_ARMS = R.TASKS, R.EXTRA_RUBRIC, R.VARIANT_ARMS
    TRUTH_IN_RUBRIC, PILOT = True, R.PILOT
    SPEC, TASK_DIRS = R, getattr(R, "TASK_DIRS", {})

JUDGE_MODEL = None   # --judge-model; None = same as --model
JUDGE_DIR = "judge"  # results subdir for verdicts; a different judge model gets its own


def configure_judge(judge_model, model):
    """A second judge writes to results/judge-<model>/ so the original verdicts stay intact
    and both judges grade the very same executor outputs."""
    global JUDGE_MODEL, JUDGE_DIR
    JUDGE_MODEL = judge_model or model
    if judge_model and judge_model != model:
        JUDGE_DIR = "judge-" + judge_model


def configure_only(only):
    """--only: restrict this process to some skills/targets (to split a run across processes)."""
    global TASKS
    if not only:
        return
    want = [x.strip() for x in only.split(",") if x.strip()]
    unknown = [x for x in want if x not in TASKS]
    if unknown:
        raise SystemExit("--only: unknown target(s) %s; known: %s" % (unknown, ", ".join(TASKS)))
    TASKS = {k: v for k, v in TASKS.items() if k in want}


def configure_skip(skip):
    """--skip: leave some targets out (r3: `--skip ponytail-ref` = the 288-call run without D-P1)."""
    global TASKS
    if not skip:
        return
    drop = [x.strip() for x in skip.split(",") if x.strip()]
    unknown = [x for x in drop if x not in TASKS]
    if unknown:
        raise SystemExit("--skip: unknown target(s) %s; known: %s" % (unknown, ", ".join(TASKS)))
    TASKS = {k: v for k, v in TASKS.items() if k not in drop}


STOP = threading.Event()
STOP_REASON = []
LOCK = threading.Lock()


# --------------------------------------------------------------------------- inputs

def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def task_file(skill, task, suffix=".md"):
    return os.path.join(BASE, "tasks", TASK_DIRS.get(skill, skill), task + suffix)


def task_prompt(skill, task):
    return read(task_file(skill, task))


def system_prompt(skill, arm):
    if arm not in VARIANT_ARMS[skill]:
        return NEUTRAL_NOTE
    body = read(os.path.join(BASE, "variants", "%s.%s.md" % (skill, arm)))
    if body.startswith("<!--"):  # r3: a leading license/provenance comment stays in the file, not the prompt
        body = body[body.index("-->") + 3:].lstrip("\n")
    return NEUTRAL_NOTE + "\n\n# Guidance for this kind of task\n\n" + body


def rubric_text(skill, task):
    parts = [read(os.path.join(BASE, "rubrics", "_common.md")),
             read(os.path.join(BASE, "rubrics", task + ".md"))]
    if TRUTH_IN_RUBRIC:
        parts.append("## Ground truth for this task\n\n"
                     + read(task_file(skill, task, ".truth.md")))
    if skill in SKILL_EXTRA_RUBRIC:
        parts.append(read(os.path.join(BASE, "rubrics", SKILL_EXTRA_RUBRIC[skill])))
    return "\n\n".join(p.strip() for p in parts) + "\n"


def schema_path(skill):
    return os.path.join(BASE, "schemas", skill + ".json")


def exec_argv(model, prompt, sysprompt):
    return ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
            "--tools", "", "--setting-sources", "", "--strict-mcp-config", "--permission-mode", "default",
            "--append-system-prompt", sysprompt]


def jobs(runs):
    out = []
    for skill, tasks in TASKS.items():
        for task in tasks:
            for arm in ARMS:
                for run in range(1, runs + 1):
                    out.append((skill, task, arm, run))
    return out


def exec_path(skill, task, arm, run):
    return os.path.join(RESULTS, "exec", skill, task, "%s-r%d.json" % (arm, run))


def judge_path(skill, task, arm, run):
    return os.path.join(RESULTS, JUDGE_DIR, skill, task, "%s-r%d.json" % (arm, run))


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


# --------------------------------------------------------------------------- quota

def quota_pct():
    q = load(QUOTA_FILE) or {}
    return (q.get("five_hour") or {}).get("pct"), q.get("at")


def check_quota_file():
    pct, _ = quota_pct()
    if isinstance(pct, (int, float)) and pct >= QUOTA_STOP_PCT:
        stop("quota.json five_hour at %s%% (>= %d%%)" % (pct, QUOTA_STOP_PCT))


def stop(reason):
    with LOCK:
        if not STOP.is_set():
            STOP_REASON.append(reason)
            print("STOP: " + reason, flush=True)
        STOP.set()


def rate_limit_check(info):
    if not isinstance(info, dict):
        return
    util = ((info.get("unifiedWindows") or {}).get("five_hour") or {}).get("utilization")
    if isinstance(util, (int, float)):
        pct = util * 100 if util <= 1 else util
        if pct >= QUOTA_STOP_PCT:
            stop("rate_limit_event five_hour utilization %.0f%%" % pct)


# --------------------------------------------------------------------------- executor

def run_executor(model, skill, task, arm, run):
    path = exec_path(skill, task, arm, run)
    cached = load(path)
    if cached and cached.get("status") == "ok":
        return cached
    if STOP.is_set():
        return {"status": "not_run"}
    check_quota_file()
    if STOP.is_set():
        return {"status": "not_run"}
    prompt, sysprompt = task_prompt(skill, task), system_prompt(skill, arm)
    cmd = exec_argv(model, prompt, sysprompt)
    cwd = tempfile.mkdtemp(prefix="osforge-outcome-")
    rec = {"skill": skill, "task": task, "arm": arm, "run": run, "model": model,
           "sys_prompt_chars": len(sysprompt),
           "argv_sha256": hashlib.sha256(json.dumps(cmd, ensure_ascii=False).encode()).hexdigest()}
    t0 = time.time()
    stdout, timed_out = "", False
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=J.build_env(), stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                              timeout=EXEC_TIMEOUT)
        stdout, rec["exit"] = proc.stdout or "", proc.returncode
        rec["stderr_tail"] = (proc.stderr or "")[-400:]
    except subprocess.TimeoutExpired as exc:
        timed_out, rec["exit"] = True, None
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    rec["wall_s"] = round(time.time() - t0, 1)
    events = J.parse_stream(stdout)
    tools, mcp = J.find_init(events)
    rec["isolation"] = {"tools": tools, "mcp_servers": mcp}
    info = J.find_last_rate_limit(events)
    rec["rate_limit_info"] = info
    with LOCK:
        SA.record_rate_limit(info)  # no statusline runs under `claude -p`
    result = J.find_result(events)
    rec["usage"] = J.usage_out(result)
    rec["cost_usd_equiv"] = (result or {}).get("total_cost_usd")
    rec["duration_ms"] = (result or {}).get("duration_ms")
    rec["num_turns"] = (result or {}).get("num_turns")
    if timed_out:
        rec["status"] = "timeout"
    elif tools or mcp:
        rec["status"] = "isolation_violated"
    elif result is None:
        rec["status"] = "error"
        rec["error"] = "no result event"
    elif result.get("is_error"):
        if J.is_quota(result, info):
            rec["status"] = "quota"
            stop("executor quota rejection (%s/%s/%s r%d)" % (skill, task, arm, run))
        else:
            rec["status"] = "error"
            rec["error"] = str(result.get("result", ""))[:400]
    else:
        rec["status"] = "ok"
        rec["output"] = result.get("result", "")
    rate_limit_check(info)
    save(path, rec)
    print("exec %-18s %s %s r%d -> %s %.0fs out=%s" % (skill, task, arm, run, rec["status"], rec["wall_s"],
                                                       rec["usage"].get("output")), flush=True)
    return rec


# --------------------------------------------------------------------------- judge

def blind_id(skill, task, arm, run):
    # Stable but opaque: the judge file name carries no arm/run information.
    salt = os.environ.get("OUTCOME_BLIND_SALT", "osforge-outcome-2026-10-17")
    return hashlib.sha256(("%s|%s|%s|%d|%s" % (skill, task, arm, run, salt)).encode()).hexdigest()[:12]


def run_judge(model, skill, task, arm, run, dry=False):
    path = judge_path(skill, task, arm, run)
    cached = load(path)
    if cached and cached.get("status") == "ok" and not dry:
        return cached
    ex = load(exec_path(skill, task, arm, run))
    if not dry and (not ex or ex.get("status") != "ok"):
        return {"status": "not_run"}
    if STOP.is_set() and not dry:
        return {"status": "not_run"}
    check_quota_file()
    if STOP.is_set() and not dry:
        return {"status": "not_run"}
    bid = blind_id(skill, task, arm, run)
    in_dir = os.path.join(RESULTS, "judge_inputs")
    os.makedirs(in_dir, exist_ok=True)
    answer = ex["output"] if ex and ex.get("output") is not None else "(dry run placeholder answer)"
    artifact = ("## Task given to the assistant (response id %s)\n\n%s\n\n## Assistant response\n\n%s\n"
                % (bid, task_prompt(skill, task).strip(), answer.strip()))
    in_path = os.path.join(in_dir, bid + ".md")
    with open(in_path, "w", encoding="utf-8") as fh:
        fh.write(artifact)
    rub_dir = os.path.join(RESULTS, "rubrics_built")
    os.makedirs(rub_dir, exist_ok=True)
    rub_path = os.path.join(rub_dir, "%s.md" % task)
    with open(rub_path, "w", encoding="utf-8") as fh:
        fh.write(rubric_text(skill, task))
    cmd = [sys.executable, os.path.join(LIB, "judge.py"), "--model", JUDGE_MODEL or model, "--schema", schema_path(skill),
           "--rubric", rub_path, "--input", in_path, "--timeout", str(JUDGE_TIMEOUT)]
    if dry:
        cmd.append("--dry")
    env = os.environ.copy()
    env.setdefault("OSFORGE_JUDGE_CONCURRENCY", "4")
    env.setdefault("OSFORGE_JUDGE_LOCK_DIR", os.path.join(tempfile.gettempdir(), "osforge-outcome-locks"))
    t0 = time.time()
    proc = subprocess.run(cmd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, timeout=JUDGE_TIMEOUT + 60)
    rec = {"skill": skill, "task": task, "arm": arm, "run": run, "blind_id": bid,
           "judge_exit": proc.returncode, "wall_s": round(time.time() - t0, 1)}
    try:
        out = json.loads((proc.stdout or "").strip().splitlines()[-1])
    except (ValueError, IndexError):
        out = {"ok": False, "error": "unparseable judge stdout: %r" % (proc.stdout or "")[-300:]}
    rec["judge"] = out
    if dry:
        return rec
    if proc.returncode == 75:
        rec["status"] = "quota"
        stop("judge exit 75 (%s/%s/%s r%d)" % (skill, task, arm, run))
    elif proc.returncode == 0 and out.get("ok"):
        problems = check_verdict(skill, task, out["verdict"])
        rec["status"] = "ok" if not problems else "bad_verdict"
        if problems:
            rec["problems"] = problems
    else:
        rec["status"] = "error"
    rate_limit_check((out.get("rate_limit") or {}))
    save(path, rec)
    print("judge %-18s %s %s r%d -> %s score=%s %.0fs" % (
        skill, task, arm, run, rec["status"], (out.get("verdict") or {}).get("score"), rec["wall_s"]), flush=True)
    return rec


def check_verdict(skill, task, verdict):
    want = TASKS[skill][task]["criteria"]
    got = [c.get("id") for c in verdict.get("criteria", [])]
    missing = [c for c in want if c not in got]
    return ["missing criteria: %s" % missing] if missing else []


# --------------------------------------------------------------------------- modes

def do_dry(runs):
    problems = []
    for skill, tasks in TASKS.items():
        for arm in VARIANT_ARMS[skill]:
            if not os.path.exists(os.path.join(BASE, "variants", "%s.%s.md" % (skill, arm))):
                problems.append("missing variant %s.%s (run build_variants.py --round %s)" % (skill, arm, ROUND))
        if not os.path.exists(schema_path(skill)):
            problems.append("missing schema " + skill)
        json.loads(read(schema_path(skill)))
        for task, spec in tasks.items():
            need = [task_file(skill, task), os.path.join(BASE, "rubrics", task + ".md")]
            if TRUTH_IN_RUBRIC:
                need.append(task_file(skill, task, ".truth.md"))
            missing = [f for f in need if not os.path.exists(f)]
            problems.extend("missing " + f for f in missing)
            if missing:
                continue
            rub = read(os.path.join(BASE, "rubrics", task + ".md"))
            for cid in spec["criteria"]:
                if "`%s`" % cid not in rub:
                    problems.append("%s: criterion %s not in rubric" % (task, cid))
            for cid in spec["critical"]:
                if cid not in spec["criteria"]:
                    problems.append("%s: critical %s not a criterion" % (task, cid))
    if problems:
        print("\n".join("PROBLEM: " + p for p in problems))
        return 1
    js = jobs(runs)
    print("plan: %d executor calls + %d judge calls (runs=%d)" % (len(js), len(js), runs))
    if ROUND not in ("r1", "r2"):
        for skill, tasks in TASKS.items():
            n = len(tasks) * len(ARMS) * runs
            print("  %-20s %2d tasks x %d arms x %d runs = %3d executor + %3d judge = %3d calls%s" % (
                skill, len(tasks), len(ARMS), runs, n, n, 2 * n,
                "  (optional)" if skill in getattr(SPEC, "OPTIONAL", ()) else ""))
        print("  total model calls: %d" % (2 * len(js)))
    for skill in TASKS:
        print("  %-20s sys-prompt chars  A=%d  B=%d  C=%d" % (skill, *(len(system_prompt(skill, a)) for a in ARMS)))
    print("example executor argv (prompt/system elided):",
          json.dumps([a if len(a) < 60 else "<%d chars>" % len(a) for a in exec_argv("MODEL", "P" * 99, "S" * 99)]))
    rec = run_judge("MODEL", PILOT[0], PILOT[1], "B", 1, dry=True)
    j = rec["judge"]
    print("judge.py --dry ok=%s isolation-argv has --tools '': %s" % (
        j.get("ok"), "--tools" in (j.get("argv") or [])))
    pct, at = quota_pct()
    print("quota.json five_hour=%s%% (at %s, stop at %d%%)" % (pct, at, QUOTA_STOP_PCT))
    return 0


def do_pilot(model):
    ex = run_executor(model, PILOT[0], PILOT[1], "B", 1)
    print(json.dumps({k: v for k, v in ex.items() if k != "output"}, indent=1, ensure_ascii=False))
    print("--- output head ---\n" + (ex.get("output") or "")[:1200])
    if ex.get("status") != "ok":
        return 1
    jr = run_judge(model, PILOT[0], PILOT[1], "B", 1)
    print(json.dumps(jr, indent=1, ensure_ascii=False))
    return 0 if jr.get("status") == "ok" else 1


def do_run(model, runs, conc, seed):
    js = jobs(runs)
    rng = random.Random(seed)
    order = js[:]
    rng.shuffle(order)
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=conc) as pool:
        list(pool.map(lambda j: run_executor(model, *j), order))
    print("executor phase done in %.0fs" % (time.time() - t0), flush=True)
    order = js[:]
    rng.shuffle(order)  # judge order independent of executor order and of arm
    t1 = time.time()
    with cf.ThreadPoolExecutor(max_workers=conc) as pool:
        list(pool.map(lambda j: run_judge(model, *j), order))
    print("judge phase done in %.0fs" % (time.time() - t1), flush=True)
    if STOP_REASON:
        print("stopped early: " + "; ".join(STOP_REASON))
    return 0


def spent_usd(runs):
    tot = 0.0
    for job in jobs(runs):
        e, j = load(exec_path(*job)) or {}, load(judge_path(*job)) or {}
        tot += e.get("cost_usd_equiv") or 0
        tot += (j.get("judge") or {}).get("total_cost_usd_equivalent") or 0
    return tot


def do_run_phased(model, runs, conc, seed, budget):
    """Round 2+: one target at a time, executor phase then judge phase, each shuffled. Stops on
    quota (exit 75 / rejected), on 5h utilization >= QUOTA_STOP_PCT, or when the cumulative
    USD-equivalent of cached + new calls exceeds the budget."""
    rng = random.Random(seed)
    targets = list(TASKS)
    t0 = time.time()

    def guarded(fn):
        def call(job):
            if STOP.is_set():
                return {"status": "not_run"}
            with LOCK:
                over = budget is not None and spent_usd(runs) > budget
            if over:
                stop("budget: spent > US$%.2f" % budget)
                return {"status": "not_run"}
            return fn(model, *job)
        return call

    for target in targets:
        js = [j for j in jobs(runs) if j[0] == target]
        for phase, fn in (("executor", run_executor), ("judge", run_judge)):
            order = js[:]
            rng.shuffle(order)
            t1 = time.time()
            with cf.ThreadPoolExecutor(max_workers=conc) as pool:
                list(pool.map(guarded(fn), order))
            print("%s %s phase done in %.0fs (spent so far US$%.2f)" % (target, phase, time.time() - t1,
                                                                      spent_usd(runs)), flush=True)
    print("all phases done in %.0fs" % (time.time() - t0), flush=True)
    if STOP_REASON:
        print("stopped early: " + "; ".join(STOP_REASON))
    return 0


# --------------------------------------------------------------------------- report

def fmt(x, nd=1):
    return "–" if x is None else ("%.*f" % (nd, x))


def do_report(out_path, model, runs, cmdline):
    sys.path.insert(0, HERE)
    if ROUND != "r1":
        from report_r2 import build_report_r2  # noqa: E402
        extra = {} if ROUND == "r2" else {"spec": SPEC}
        text = build_report_r2(TASKS, ARMS, runs, model, load, exec_path, judge_path, REPO, cmdline,
                               {a: {s: len(system_prompt(s, a)) for s in TASKS} for a in ARMS}, BASE,
                               judge_model=JUDGE_MODEL if JUDGE_DIR != "judge" else None, **extra)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote " + out_path)
        return 0
    from report import build_report  # noqa: E402
    text = build_report(TASKS, ARMS, runs, model, load, exec_path, judge_path, REPO, cmdline,
                        {a: {s: len(system_prompt(s, a)) for s in TASKS} for a in ARMS},
                        judge_model=JUDGE_MODEL if JUDGE_DIR != "judge" else None)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote " + out_path)
    return 0


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--dry", action="store_true")
    p.add_argument("--pilot", action="store_true")
    p.add_argument("--run", action="store_true")
    p.add_argument("--report")
    p.add_argument("--model")
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--seed", type=int, default=20261017)
    p.add_argument("--round", default="r1", choices=("r1", "r2", "r3"))
    p.add_argument("--budget", type=float, help="r2+: stop when cached+new USD-equivalent exceeds this")
    p.add_argument("--judge-model", help="judge with a different model; verdicts go to results/judge-<id>/")
    p.add_argument("--only", help="comma-separated skills/targets to run in this process")
    p.add_argument("--skip", help="comma-separated skills/targets to leave out (r3: ponytail-ref is optional)")
    a = p.parse_args(argv)
    configure(a.round)
    configure_only(a.only)
    configure_skip(a.skip)
    configure_judge(a.judge_model, a.model)
    if a.dry:
        return do_dry(a.runs)
    if not a.model:
        p.error("--model is required outside --dry")
    if a.concurrency > 4:
        p.error("--concurrency is capped at 4")
    if a.pilot:
        return do_pilot(a.model)
    if a.run:
        if a.round == "r1":
            return do_run(a.model, a.runs, a.concurrency, a.seed)
        return do_run_phased(a.model, a.runs, a.concurrency, a.seed, a.budget)
    if a.report:
        return do_report(a.report, a.model, a.runs, "python3 scripts/evals/outcome/driver.py " + " ".join(argv))
    p.error("pick one of --dry, --pilot, --run, --report")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
