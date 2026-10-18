#!/usr/bin/env python3
"""compare_judges.py -- agreement between two judges over the same executor outputs.

    python3 scripts/evals/outcome/compare_judges.py --judge-dir judge-claude-fable-5-1

Reads results/judge/ (the original judge) and results/<judge-dir>/ for both rounds, pairs the
verdicts per (target, task, arm, run) and prints, per target: arm means under each judge, the
mean absolute score gap, how often the two judges agree on the B-vs-A and C-vs-B direction, and
the number of per-criterion pass/fail disagreements. Read-only: it never calls a model.
"""
import argparse
import glob
import json
import os
import statistics as st
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROUNDS = {"r1": os.path.join(HERE, "results"), "r2": os.path.join(HERE, "r2", "results")}


def verdicts(results, sub):
    out = {}
    for f in glob.glob(os.path.join(results, sub, "*", "*", "*.json")):
        with open(f, encoding="utf-8") as fh:
            r = json.load(fh)
        if r.get("status") != "ok":
            continue
        out[(r["skill"], r["task"], r["arm"], r["run"])] = r["judge"]["verdict"]
    return out


def arm_means(v, target):
    by = defaultdict(list)
    for (t, _task, arm, _run), x in v.items():
        if t == target:
            by[arm].append(x["score"])
    return {a: st.mean(s) for a, s in by.items()}


def sign(x, eps=0.25):
    return 0 if abs(x) < eps else (1 if x > 0 else -1)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--judge-dir", required=True)
    a = p.parse_args()
    print("| Round | Target | n pairs | Opus judge A/B/C | Fable judge A/B/C | mean abs gap | "
          "B−A direction agrees | C−B direction agrees | criterion flips |")
    print("|---|---|---|---|---|---|---|---|---|")
    for rnd, res in ROUNDS.items():
        o, f = verdicts(res, "judge"), verdicts(res, a.judge_dir)
        keys = sorted(set(o) & set(f))
        for target in sorted({k[0] for k in keys}):
            ks = [k for k in keys if k[0] == target]
            om = arm_means({k: o[k] for k in ks}, target)
            fm = arm_means({k: f[k] for k in ks}, target)
            gap = st.mean(abs(o[k]["score"] - f[k]["score"]) for k in ks)
            if not all(x in om and x in fm for x in "ABC"):
                print("| %s | %s | %d | incomplete — rerun after the judge finishes |||||||" % (rnd, target, len(ks)))
                continue
            agree_ba = sign(om["B"] - om["A"]) == sign(fm["B"] - fm["A"])
            agree_cb = sign(om["C"] - om["B"]) == sign(fm["C"] - fm["B"])
            flips = 0
            for k in ks:
                oc = {c["id"]: c.get("result") for c in o[k].get("criteria", [])}
                fc = {c["id"]: c.get("result") for c in f[k].get("criteria", [])}
                flips += sum(1 for cid in oc if cid in fc and oc[cid] != fc[cid])
            fmt = lambda m: "/".join("%.2f" % m.get(x, float("nan")) for x in "ABC")
            print("| %s | %s | %d | %s | %s | %.2f | %s | %s | %d |" % (
                rnd, target, len(ks), fmt(om), fmt(fm), gap,
                "yes" if agree_ba else "NO", "yes" if agree_cb else "NO", flips))


if __name__ == "__main__":
    main()
