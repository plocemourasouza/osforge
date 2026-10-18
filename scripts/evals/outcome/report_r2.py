"""report_r2.py -- aggregate the cached round-2 outcome-eval results into a docs/evals/ report.

Called by `driver.py --report <out.md> --round r2`. Same layout as round 1 (report.py, left
untouched so round 1 regenerates byte-identically) plus the round-2 extras: per-target judge counts,
per-task output tokens, peak 5-hour utilization seen in the executor streams, and a per-call
appendix (exit, wall, tokens, cost). Only numbers computed from r2/results/ appear here; a cell
with no graded data prints a dash, never a guess. Python 3 stdlib only.
"""
import datetime
import os
import re
import statistics

from report import _f, _mean, _sd, _sh  # noqa: F401  (shared helpers from round 1)
import tasks_r2 as R

SECONDARY = {  # target -> (count, label) shown in the summary table
    "clean-code": ("scope_creep_changes", "scope-creep changes / answer"),
    "verification-before-completion": ("unverified_claims", "unverified claims / answer"),
    "behavioral-modes": ("padding_items", "padding passages / answer"),
    "output-enforcement": ("placeholders", "placeholders / answer"),
    "agent-planner": ("seeded_found", "hidden deps found / answer"),
    "agent-code-reviewer": ("manufactured_findings", "manufactured findings / answer"),
}


def _labels(target):
    return R.ARM_LABELS.get(target, R.ARM_LABELS["default"])


def _util(e):
    info = (e or {}).get("rate_limit_info") or {}
    u = ((info.get("unifiedWindows") or {}).get("five_hour") or {}).get("utilization")
    if not isinstance(u, (int, float)):
        return None
    return u * 100 if u <= 1 else u


def build_report_r2(TASKS, ARMS, runs, model, load, exec_path, judge_path, repo, cmdline, sys_chars, base):
    sha = _sh(["git", "rev-parse", "--short", "HEAD"], repo)
    branch = _sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
    dirty = _sh(["git", "status", "--porcelain", "--", "skills/", "agents/"], repo)
    cli = _sh(["claude", "--version"], repo)
    log_path = os.path.join(base, "results", "run.log")
    phases, stops = [], []
    if os.path.exists(log_path):
        for line in open(log_path, encoding="utf-8"):
            m = re.match(r"(\S+) (executor|judge) phase done in (\d+)s", line)
            if m:
                phases.append("%s %s %ss" % m.groups())
            if line.startswith("STOP:") or line.startswith("stopped early"):
                stops.append(line.strip())
    n_jobs = sum(len(t) for t in TASKS.values()) * len(ARMS) * runs

    L = []
    w = L.append
    w("# Skill outcome eval, round 2 — %s — %s" % (model, datetime.date.today().isoformat()))
    w("")
    w("| Field | Value |")
    w("|---|---|")
    w("| Suite | `outcome` round 2 (`--round r2`): no-skill vs current vs reduced/previous; agents: without vs with the boilerplate block |")
    w("| Executor model | `%s` |" % model)
    w("| Judge model | `%s` via `scripts/lib/judge.py` (blind, isolated) |" % model)
    w("| Repo | `%s` on `%s`; `skills/` + `agents/` %s; variants pinned to `656aaf0` (clean-code C from `0fb36cd`) |"
      % (sha, branch, "clean" if not dirty else "DIRTY"))
    w("| CLI | `%s` |" % cli)
    w("| Runs per cell | %d (%d targets, %d tasks × 3 arms × %d = %d executor + %d judge calls planned) |"
      % (runs, len(TASKS), sum(len(t) for t in TASKS.values()), runs, n_jobs, n_jobs))
    w("| Command | `%s` (run: `driver.py --run --round r2 --model %s --runs %d --concurrency 4 --budget 40`) |"
      % (cmdline, model, runs))
    w("| Wall time | %s (concurrency 4; per target: executor phase, then judge phase) |"
      % ("; ".join(phases) if phases else "?"))
    w("| Early stop | %s |" % ("; ".join(stops) if stops else "none"))

    # ---- status accounting
    ex_status, jd_status = {}, {}
    cost = {"exec": 0.0, "judge": 0.0}
    utils = []
    calls = []
    for target, tasks in TASKS.items():
        for task in tasks:
            for arm in ARMS:
                for r in range(1, runs + 1):
                    e = load(exec_path(target, task, arm, r)) or {"status": "not_run"}
                    j = load(judge_path(target, task, arm, r)) or {"status": "not_run"}
                    ex_status[e["status"]] = ex_status.get(e["status"], 0) + 1
                    jd_status[j["status"]] = jd_status.get(j["status"], 0) + 1
                    cost["exec"] += e.get("cost_usd_equiv") or 0
                    jj = j.get("judge") or {}
                    cost["judge"] += jj.get("total_cost_usd_equivalent") or 0
                    u = _util(e)
                    if u is not None:
                        utils.append(u)
                    calls.append((target, task, arm, r, e, j))
    w("| Peak 5-hour utilization seen | %s (from executor `rate_limit_event`s; judge.py reports only allowed/rejected; stop threshold 80%%) |"
      % (("%.0f%%" % max(utils)) if utils else "–"))
    w("")
    w("**Call status.** Executor: %s. Judge: %s. Subscription quota, cost shown as the CLI's "
      "USD-equivalent: executor %.2f, judge %.2f, total %.2f."
      % (", ".join("%s %d" % kv for kv in sorted(ex_status.items())),
         ", ".join("%s %d" % kv for kv in sorted(jd_status.items())), cost["exec"], cost["judge"],
         cost["exec"] + cost["judge"]))
    w("")
    w("**How to read.** A run *passes* a task when every critical criterion of that task's rubric "
      "passes. Per task and arm, **PASS** is k = N, **FLAKY** 0 < k < N, **FAIL** k = 0 "
      "(docs/evals/README.md). *Score* is the judge's 0–10. *Run spread* = max − min of the per-run "
      "mean score (mean over the target's tasks of run r, r = 1..3): the run-to-run noise of that arm. A "
      "delta is called **real** only when |Δ| exceeds the larger run spread of the two arms compared.")
    w("")
    w("**Arm semantics differ by target.** Skills: A = a one-line neutral note only, B = note + current "
      "SKILL.md body, C = note + the audit-reduced body (for `clean-code`, C = the *previous* text, "
      "`0fb36cd`, so B − C measures v3.0 against v2.0). Agents (`agent-*`, H17): every arm carries the "
      "agent body; A = body **without** the \"Reality Check\" and \"Quality Control Loop\" sections, "
      "B = full current body, C = A + one line (\"Before delivering, confirm the output answers the "
      "original request and say where you are uncertain.\"). So for agents B − A is the value of the "
      "boilerplate block, and C − B asks whether one line can replace it.")
    w("")

    summary = []
    for target, tasks in TASKS.items():
        lab = _labels(target)
        w("## %s" % target)
        w("")
        cell = {}
        for task in tasks:
            for arm in ARMS:
                rows = []
                for r in range(1, runs + 1):
                    j = load(judge_path(target, task, arm, r)) or {}
                    e = load(exec_path(target, task, arm, r)) or {}
                    v = (j.get("judge") or {}).get("verdict") if j.get("status") == "ok" else None
                    rows.append((r, v, e))
                cell[(task, arm)] = rows

        def run_passes(task, v):
            crit = TASKS[target][task]["critical"]
            res = {c["id"]: c["result"] for c in v["criteria"]}
            return all(res.get(c) == "pass" for c in crit)

        stats = {}
        for arm in ARMS:
            scores, run_means, outs, ins, walls = [], [], [], [], []
            k = n = 0
            for r in range(1, runs + 1):
                rs = []
                for task in tasks:
                    _, v, e = cell[(task, arm)][r - 1]
                    if e.get("status") == "ok":
                        u = e.get("usage") or {}
                        outs.append(u.get("output", 0))
                        ins.append(u.get("input", 0) + u.get("cache_read", 0) + u.get("cache_create", 0))
                        walls.append(e.get("wall_s") or 0)
                    if v is None:
                        continue
                    scores.append(v["score"])
                    rs.append(v["score"])
                    n += 1
                    k += run_passes(task, v)
                if len(rs) == len(tasks):
                    run_means.append(statistics.mean(rs))
            stats[arm] = {"scores": scores, "mean": _mean(scores), "sd": _sd(scores),
                          "spread": (max(run_means) - min(run_means)) if len(run_means) > 1 else None,
                          "run_means": run_means, "k": k, "n": n, "out": _mean(outs), "in": _mean(ins),
                          "wall": _mean(walls)}
        w("| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | "
          "Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |")
        w("|---|---|---|---|---|---|---|---|---|---|---|")
        for arm in ARMS:
            s = stats[arm]
            w("| %s | %d | %s | %s | %s | %s | %d/%d | %d | %s | %s | %s |" % (
                lab[arm], len(s["scores"]), _f(s["mean"], 2), _f(s["sd"], 2),
                " / ".join(_f(x, 2) for x in s["run_means"]) or "–", _f(s["spread"], 2), s["k"], s["n"],
                sys_chars[arm][target], _f(s["in"], 0), _f(s["out"], 0), _f(s["wall"], 0)))
        w("")

        def delta(x, y):
            if stats[x]["mean"] is None or stats[y]["mean"] is None:
                return None, None, None
            d = stats[x]["mean"] - stats[y]["mean"]
            noise = max(stats[x]["spread"] or 0, stats[y]["spread"] or 0)
            return d, noise, abs(d) > noise
        dBA, nBA, rBA = delta("B", "A")
        dCB, nCB, rCB = delta("C", "B")
        dCA, nCA, rCA = delta("C", "A")
        w("| Delta | Value | Noise bound (max run spread) | Real? |")
        w("|---|---|---|---|")
        for name, d, nb, real in (("B − A", dBA, nBA, rBA), ("C − B", dCB, nCB, rCB), ("C − A", dCA, nCA, rCA)):
            w("| %s | %s | %s | %s |" % (name, _f(d, 2), _f(nb, 2), "–" if real is None else ("yes" if real else "no")))
        w("")
        thing = "block" if target.startswith("agent-") else "skill"
        if dBA is None:
            verdict = "not measured"
        elif rBA and dBA > 0:
            verdict = "%s helps (B > A beyond run spread)" % thing
        elif rBA and dBA < 0:
            verdict = "%s hurts (B < A beyond run spread)" % thing
        else:
            verdict = "%s neutral (B − A within run spread)" % thing
        if dCB is None:
            cverdict = "not measured"
        elif rCB and dCB > 0:
            cverdict = "C > B beyond run spread"
        elif not rCB:
            cverdict = "C ≈ B within noise"
        else:
            cverdict = "C < B beyond run spread"
        w("**Computed verdict:** %s. **Arm C:** %s." % (verdict, cverdict))
        w("")

        # per task
        w("### Per task (k/N runs passing criticals · mean score · mean output tokens)")
        w("")
        w("| Task | %s | %s | %s |" % (lab["A"], lab["B"], lab["C"]))
        w("|---|---|---|---|")
        for task in tasks:
            cells = []
            for arm in ARMS:
                vs = [v for _, v, _ in cell[(task, arm)] if v is not None]
                outs = [(e.get("usage") or {}).get("output", 0) for _, _, e in cell[(task, arm)]
                        if e.get("status") == "ok"]
                if not vs:
                    cells.append("NOT RUN")
                    continue
                k = sum(run_passes(task, v) for v in vs)
                lb = "PASS" if k == len(vs) == runs else ("FAIL" if k == 0 else "FLAKY")
                if len(vs) < runs and k == len(vs):
                    lb = "INCOMPLETE"
                cells.append("%s %d/%d · %s · %s tok" % (lb, k, len(vs), _f(_mean([v["score"] for v in vs]), 1),
                                                         _f(_mean(outs), 0)))
            w("| `%s` | %s |" % (task, " | ".join(cells)))
        w("")

        # per criterion
        w("### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)")
        w("")
        w("| Criterion | A | B | C |")
        w("|---|---|---|---|")
        for task, spec in tasks.items():
            for cid in spec["criteria"]:
                cells = []
                for arm in ARMS:
                    p = f = 0
                    for _, v, _ in cell[(task, arm)]:
                        if v is None:
                            continue
                        res = {c["id"]: c["result"] for c in v["criteria"]}.get(cid)
                        p += res == "pass"
                        f += res == "fail"
                    cells.append("%d/%d" % (p, p + f) if p + f else "–")
                w("| `%s.%s`%s | %s |" % (task, cid, "*" if cid in spec["critical"] else "", " | ".join(cells)))
        w("")

        # judge counts
        counts = R.COUNTS[target]
        w("### Judge counts (mean per graded answer; per task in brackets)")
        w("")
        w("| Count | A | B | C |")
        w("|---|---|---|---|")
        for cnt in counts:
            cells = []
            for arm in ARMS:
                allv, per = [], []
                for task in tasks:
                    tv = [v[cnt] for _, v, _ in cell[(task, arm)] if v is not None and cnt in v]
                    allv += tv
                    per.append("%s %s" % (task, _f(_mean(tv), 1)))
                cells.append("%s (%s)" % (_f(_mean(allv), 2), ", ".join(per)))
            w("| `%s` | %s |" % (cnt, " | ".join(cells)))
        w("")
        sec_cnt = SECONDARY[target][0]
        sec = {}
        for arm in ARMS:
            vals = [v[sec_cnt] for task in tasks for _, v, _ in cell[(task, arm)] if v is not None and sec_cnt in v]
            sec[arm] = _mean(vals)
        summary.append((target, stats, verdict, cverdict, dBA, dCB, sec))

    w("## Summary")
    w("")
    w("| Target | A mean ± run spread | B mean ± run spread | C mean ± run spread | B − A | C − B | Verdict | Arm C | Key secondary (A / B / C) |")
    w("|---|---|---|---|---|---|---|---|---|")
    for target, st, verdict, cverdict, dBA, dCB, sec in summary:
        w("| `%s` | %s | %s | %s | %s | %s | %s | %s | %s: %s |" % (
            target, *("%s ± %s" % (_f(st[a]["mean"], 2), _f(st[a]["spread"], 2)) for a in ARMS),
            _f(dBA, 2), _f(dCB, 2), verdict.split(" (")[0], cverdict, SECONDARY[target][1],
            " / ".join(_f(sec[a], 2) for a in ARMS)))
    w("")
    analysis = os.path.join(base, "analysis.md")
    if os.path.exists(analysis):
        w("## Interpretation and limitations (hand-written, from the tables above)")
        w("")
        w(open(analysis, encoding="utf-8").read().strip())
        w("")

    w("## Appendix — per-call record")
    w("")
    w("Executor: status, exit, wall s, output tokens, USD-equiv. Judge: status, exit, wall s, USD-equiv, score.")
    w("")
    w("| Target | Task | Arm | Run | Exec | Exit | Wall | Out tok | Exec $ | Judge | Exit | Wall | Judge $ | Score |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for target, task, arm, r, e, j in calls:
        jj = j.get("judge") or {}
        v = jj.get("verdict") or {}
        w("| %s | %s | %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            target, task, arm, r, e.get("status"), e.get("exit", "–"), _f(e.get("wall_s"), 0),
            (e.get("usage") or {}).get("output", "–"), _f(e.get("cost_usd_equiv"), 3), j.get("status"),
            j.get("judge_exit", "–"), _f(j.get("wall_s"), 0), _f(jj.get("total_cost_usd_equivalent"), 3),
            v.get("score", "–") if j.get("status") == "ok" else "–"))
    w("")
    return "\n".join(L) + "\n"
