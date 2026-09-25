#!/usr/bin/env python3
"""Controle de idioma: os mesmos 75 positivos, traduzidos para inglês (en_positives.tsv).

Uso: en_eval.py <repo_osforge> <saida.json>
"""
import json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
repo, out = sys.argv[1], sys.argv[2]
sys.argv = ["needle_eval.py", repo, out]
import needle_eval as ne  # noqa: E402  (lê argv na importação)

ne.cases = []
for ln in open(os.path.join(here, "en_positives.tsv"), encoding="utf-8"):
    s, i, q = ln.rstrip("\n").split("\t")
    ne.cases.append({"skill": s, "id": i, "pos": True, "q": q})
res = {"summaries": [], "scenarios": []}
for k in ("A", "C"):
    r = ne.run_scenario(k)
    res["scenarios"].append(r)
    res["summaries"].append(ne.summarize(r))
    print(json.dumps(res["summaries"][-1], ensure_ascii=False), flush=True)
res["baselines"] = ne.baselines()
print(json.dumps(res["baselines"], ensure_ascii=False), flush=True)
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
