"""report.py -- aggregate the cached outcome-eval results into a docs/evals/ markdown report.

Called by driver.py --report. Only numbers computed from results/ appear here; a cell with no
graded data prints a dash, never a guess. Python 3 stdlib only.
"""
import datetime
import os
import re
import statistics
import subprocess


def _sh(args, cwd):
    try:
        return subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                              text=True, timeout=30).stdout.strip()
    except Exception:  # noqa: BLE001 -- stamping is best-effort
        return "?"


def _f(x, nd=1):
    return "–" if x is None else "%.*f" % (nd, x)


def _mean(xs):
    return statistics.mean(xs) if xs else None


def _sd(xs):
    return statistics.stdev(xs) if len(xs) > 1 else None


def build_report(TASKS, ARMS, runs, model, load, exec_path, judge_path, repo, cmdline, sys_chars, judge_model=None):
    sha = _sh(["git", "rev-parse", "--short", "HEAD"], repo)
    branch = _sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
    dirty = _sh(["git", "status", "--porcelain", "--", "skills/"], repo)
    cli = _sh(["claude", "--version"], repo)
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "run.log")
    phases, stops = {}, []
    if os.path.exists(log_path):
        for line in open(log_path, encoding="utf-8"):
            m = re.match(r"(executor|judge) phase done in (\d+)s", line)
            if m:
                phases[m.group(1)] = int(m.group(2))
            if line.startswith("STOP:") or line.startswith("stopped early"):
                stops.append(line.strip())

    L = []
    w = L.append
    w("# Skill outcome eval — claude-opus-5-5 — %s" % datetime.date.today().isoformat())
    w("")
    w("| Field | Value |")
    w("|---|---|")
    w("| Suite | `outcome` (with-skill vs without-skill vs reduced-skill) |")
    w("| Executor model | `%s` |" % model)
    w("| Judge model | `%s` via `scripts/lib/judge.py` (blind, isolated) |" % (judge_model or model))
    w("| Repo | `%s` on `%s`; `skills/` %s |" % (sha, branch, "clean" if not dirty else "DIRTY"))
    w("| CLI | `%s` |" % cli)
    w("| Runs per cell | %d (3 skills × 4 tasks × 3 arms × %d = %d executor + %d judge calls planned) |"
      % (runs, runs, 36 * runs, 36 * runs))
    w("| Command | `%s` (run: `driver.py --run --model %s --runs %d --concurrency 4`) |" % (cmdline, model, runs))
    w("| Wall time | executor phase %ss, judge phase %ss (concurrency 4) |"
      % (phases.get("executor", "?"), phases.get("judge", "?")))
    w("| Early stop | %s |" % ("; ".join(stops) if stops else "none"))
    w("")

    # ---- status accounting
    ex_status, jd_status = {}, {}
    tot_cost = {"exec": 0.0, "judge": 0.0}
    for skill, tasks in TASKS.items():
        for task in tasks:
            for arm in ARMS:
                for r in range(1, runs + 1):
                    e = load(exec_path(skill, task, arm, r)) or {"status": "not_run"}
                    j = load(judge_path(skill, task, arm, r)) or {"status": "not_run"}
                    ex_status[e["status"]] = ex_status.get(e["status"], 0) + 1
                    jd_status[j["status"]] = jd_status.get(j["status"], 0) + 1
                    tot_cost["exec"] += e.get("cost_usd_equiv") or 0
                    tot_cost["judge"] += (j.get("judge") or {}).get("total_cost_usd_equivalent") or 0
    w("**Call status.** Executor: %s. Judge: %s. Subscription quota, cost shown as the CLI's "
      "USD-equivalent: executor %.2f, judge %.2f."
      % (", ".join("%s %d" % kv for kv in sorted(ex_status.items())),
         ", ".join("%s %d" % kv for kv in sorted(jd_status.items())), tot_cost["exec"], tot_cost["judge"]))
    w("")
    w("**How to read.** A run *passes* a task when every critical criterion of that task's rubric "
      "passes. Per task and arm, **PASS** is k = N, **FLAKY** 0 < k < N, **FAIL** k = 0 "
      "(docs/evals/README.md). *Score* is the judge's 0–10. *Run spread* = max − min of the per-run "
      "mean score (mean over the 4 tasks of run r, r = 1..3): the run-to-run noise of that arm. A "
      "delta is called **real** only when |Δ| exceeds the larger run spread of the two arms compared.")
    w("")

    summary = []
    for skill, tasks in TASKS.items():
        w("## %s" % skill)
        w("")
        cell = {}  # (task, arm) -> list of (run, verdict, exec)
        for task in tasks:
            for arm in ARMS:
                rows = []
                for r in range(1, runs + 1):
                    j = load(judge_path(skill, task, arm, r)) or {}
                    e = load(exec_path(skill, task, arm, r)) or {}
                    v = (j.get("judge") or {}).get("verdict") if j.get("status") == "ok" else None
                    rows.append((r, v, e))
                cell[(task, arm)] = rows

        def run_passes(task, v):
            crit = TASKS[skill][task]["critical"]
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
                {"A": "A control", "B": "B current", "C": "C reduced"}[arm], len(s["scores"]),
                _f(s["mean"], 2), _f(s["sd"], 2), " / ".join(_f(x, 2) for x in s["run_means"]) or "–",
                _f(s["spread"], 2), s["k"], s["n"], sys_chars[arm][skill], _f(s["in"], 0),
                _f(s["out"], 0), _f(s["wall"], 0)))
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
        if dBA is None:
            verdict = "not measured"
        elif rBA and dBA > 0:
            verdict = "skill helps (B > A beyond run spread)"
        elif rBA and dBA < 0:
            verdict = "skill hurts (B < A beyond run spread)"
        else:
            verdict = "skill neutral (B − A within run spread)"
        if dCB is None:
            cverdict = "not measured"
        elif rCB and dCB > 0:
            cverdict = "C > B beyond run spread — the audit's cuts are safe and improve this task set"
        elif not rCB:
            cverdict = "C ≈ B within noise — the audit's cuts are safe on this task set"
        else:
            cverdict = "C < B beyond run spread — the cuts cost quality"
        w("**Computed verdict:** %s. **Reduced variant:** %s." % (verdict, cverdict))
        w("")
        summary.append((skill, stats, verdict, cverdict, dBA, dCB))

        # per task
        w("### Per task (k/N runs passing criticals · mean score)")
        w("")
        w("| Task | A control | B current | C reduced |")
        w("|---|---|---|---|")
        for task in tasks:
            cells = []
            for arm in ARMS:
                vs = [v for _, v, _ in cell[(task, arm)] if v is not None]
                if not vs:
                    cells.append("NOT RUN")
                    continue
                k = sum(run_passes(task, v) for v in vs)
                lab = "PASS" if k == len(vs) == runs else ("FAIL" if k == 0 else "FLAKY")
                if len(vs) < runs and k == len(vs):
                    lab = "INCOMPLETE"
                cells.append("%s %d/%d · %s" % (lab, k, len(vs), _f(_mean([v["score"] for v in vs]), 1)))
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

        if skill == "frontend-design":
            w("### AI-default tells present (mean per graded page-task; lower is better)")
            w("")
            tells_all = {}
            w("| Arm | Mean tells / answer | Most frequent |")
            w("|---|---|---|")
            for arm in ARMS:
                counts, freq = [], {}
                for task in tasks:
                    for _, v, _ in cell[(task, arm)]:
                        if v is None:
                            continue
                        t = v.get("tells_present") or []
                        counts.append(len(t))
                        for x in t:
                            freq[x] = freq.get(x, 0) + 1
                tells_all[arm] = freq
                top = ", ".join("%s %d" % kv for kv in sorted(freq.items(), key=lambda kv: -kv[1])[:5]) or "none"
                w("| %s | %s (n=%d) | %s |" % (arm, _f(_mean(counts), 2), len(counts), top))
            w("")
            named = ["T1_cream_bg", "T2_italic_accent", "T3_numbered_labels", "T4_mono_eyebrow", "T5_pill_everywhere"]
            w("Named Opus defaults added to C's avoid-table (count of answers showing each): " + "; ".join(
                "%s A=%d B=%d C=%d" % (t, tells_all["A"].get(t, 0), tells_all["B"].get(t, 0), tells_all["C"].get(t, 0))
                for t in named) + ".")
            w("")
        if skill == "adversarial-review":
            w("### Recall of seeded defects and manufactured findings")
            w("")
            w("| Arm | Seeded recall | Manufactured findings (mean / answer) | Manufactured rated Critical/Important (total) | "
              "Total findings (mean) | `ar2` (clean spec) total findings (mean) |")
            w("|---|---|---|---|---|---|")
            for arm in ARMS:
                found = total = 0
                manu, manuh, tf, clean_tf = [], 0, [], []
                for task, spec in tasks.items():
                    for _, v, _ in cell[(task, arm)]:
                        if v is None:
                            continue
                        found += min(v["seeded_found"], spec["seeded"])
                        total += spec["seeded"]
                        manu.append(v["manufactured_findings"])
                        manuh += v["manufactured_high"]
                        tf.append(v["total_findings"])
                        if task == "ar2":
                            clean_tf.append(v["total_findings"])
                w("| %s | %s | %s | %d | %s | %s |" % (
                    arm, "%d/%d" % (found, total) if total else "–", _f(_mean(manu), 2), manuh,
                    _f(_mean(tf), 1), _f(_mean(clean_tf), 1)))
            w("")

    w("## Summary")
    w("")
    w("| Skill | A mean ± run spread | B mean ± run spread | C mean ± run spread | B − A | C − B | Verdict | C ≥ B? |")
    w("|---|---|---|---|---|---|---|---|")
    for skill, st, verdict, cverdict, dBA, dCB in summary:
        w("| `%s` | %s | %s | %s | %s | %s | %s | %s |" % (
            skill, *("%s ± %s" % (_f(st[a]["mean"], 2), _f(st[a]["spread"], 2)) for a in ARMS),
            _f(dBA, 2), _f(dCB, 2), verdict.split(" (")[0], cverdict.split(" —")[0]))
    w("")
    analysis = os.path.join(os.path.dirname(os.path.abspath(__file__)), ("analysis-%s.md" % judge_model if judge_model else "analysis.md"))
    if os.path.exists(analysis):
        w("## Interpretation and limitations (hand-written, from the tables above)")
        w("")
        w(open(analysis, encoding="utf-8").read().strip())
        w("")
    return "\n".join(L) + "\n"
