#!/usr/bin/env python3
"""Mede o Needle 3 contra os casos de trigger do OSForge (somente leitura no repo).

Uso: needle_eval.py <repo_osforge> <saida.json> [cenarios...]
Cenarios: A = 47 core, descricao inteira · B = 47 core, 1a frase · C = 15 avaliadas, inteira
Controle de idioma: en_eval.py (os 75 positivos traduzidos, en_positives.tsv).
Registro da medicao de 2026-09-24: ../EVIDENCIAS.md (EV-N-M01 a EV-N-M09).
"""
import glob, json, math, os, re, statistics, sys, time, unicodedata

REPO, OUT = sys.argv[1], sys.argv[2]
SCEN = sys.argv[3:] or ["A", "B", "C"]
import needle


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip().strip("'\"")
    lines, grab = [], False
    for ln in fm.splitlines():
        if re.match(r"^description:", ln):
            grab = True
            rest = ln.split(":", 1)[1].strip()
            if rest and rest not in (">", "|", ">-", "|-"):
                lines.append(rest)
            continue
        if grab:
            if re.match(r"^[A-Za-z_][\w-]*:", ln):
                break
            lines.append(ln.strip())
    return name, " ".join(x for x in lines if x).strip().strip("'\"")


def short(desc):
    return re.split(r"(?<=[.!?])\s", desc, maxsplit=1)[0][:200]


core = [l.strip() for l in open(os.path.join(REPO, "claude-code/skills-core.txt"), encoding="utf-8")
        if l.strip() and not l.startswith("#")]
skills = {}
for rel in core:
    p = os.path.join(REPO, "skills", rel, "SKILL.md")
    if os.path.isfile(p):
        n, d = frontmatter(p)
        skills[n] = {"rel": rel, "desc": d}

cases = []
for f in sorted(glob.glob(os.path.join(REPO, "scripts/evals/trigger/*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    for c in d["cases"]:
        cases.append({"skill": d["skill"], "id": c["id"], "pos": bool(c["should_trigger"]), "q": c["query"]})
evaluated = sorted({c["skill"] for c in cases})

san = lambda n: re.sub(r"[^A-Za-z0-9_]", "_", n)
unsan = {san(n): n for n in skills}


def tools_for(names, variant):
    return [{"name": san(n), "description": skills[n]["desc"] if variant == "full" else short(skills[n]["desc"]),
             "parameters": {"type": "object", "properties": {}}} for n in names]


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p / 100 * (len(xs) - 1))))] if xs else None


def names_of(calls):
    if isinstance(calls, dict):
        calls = [calls]
    return [unsan.get(str(c.get("name")), str(c.get("name"))) for c in (calls or []) if isinstance(c, dict)]


def run_scenario(key):
    names = sorted(skills) if key in ("A", "B") else [s for s in evaluated if s in skills]
    variant = "short" if key == "B" else "full"
    T = tools_for(names, variant)
    t0 = time.perf_counter()
    agent = needle.Needle(tools=T, stateless=True,
                          tool_index_path=os.path.join(os.path.dirname(os.path.abspath(OUT)), f"idx_{key}.idx"))
    init_ms = (time.perf_counter() - t0) * 1000
    rows = []
    for c in cases:
        t = time.perf_counter()
        try:
            r, err = agent.complete(c["q"]), None
        except Exception as e:
            r, err = {}, str(e)[:200]
        rows.append({**c, "ms": round((time.perf_counter() - t) * 1000, 1), "type": r.get("type"),
                     "calls": names_of(r.get("function_calls")), "suppressed": names_of(r.get("suppressed_calls")),
                     "conf": r.get("confidence"), "err": err})
    agent.close()
    return {"scenario": key, "n_tools": len(T), "variant": variant, "init_ms": round(init_ms, 1), "rows": rows}


def summarize(res):
    rows = res["rows"]
    P = [r for r in rows if r["pos"]]
    N = [r for r in rows if not r["pos"]]
    hit = [r for r in P if r["skill"] in r["calls"]]
    conf_hit = [r["conf"] for r in hit if isinstance(r["conf"], (int, float))]
    conf_miss = [r["conf"] for r in P if r not in hit and isinstance(r["conf"], (int, float))]
    lat = [r["ms"] for r in rows]
    return {
        "scenario": res["scenario"], "n_tools": res["n_tools"], "variant": res["variant"], "init_ms": res["init_ms"],
        "pos": len(P), "neg": len(N), "pos_hit": len(hit),
        "pos_top1": sum(1 for r in P if r["calls"][:1] == [r["skill"]]),
        "pos_hit_incl_suppressed": sum(1 for r in P if r["skill"] in r["calls"] + r["suppressed"]),
        "pos_empty": sum(1 for r in P if not r["calls"]),
        "neg_false_trigger": sum(1 for r in N if r["skill"] in r["calls"]),
        "neg_empty": sum(1 for r in N if not r["calls"]),
        "neg_other_skill": sum(1 for r in N if r["calls"] and r["skill"] not in r["calls"]),
        "conf_mean_hit": round(statistics.mean(conf_hit), 3) if conf_hit else None,
        "conf_mean_miss": round(statistics.mean(conf_miss), 3) if conf_miss else None,
        "lat_p50_ms": pct(lat, 50), "lat_p95_ms": pct(lat, 95), "lat_max_ms": max(lat) if lat else None,
        "errors": sum(1 for r in rows if r["err"]),
    }


def fold(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))


STOP = set(("a o os as de da do das dos e em no na nos nas um uma uns umas para pra por com que se me meu minha "
            "isso esse essa esta este isto the a an of to and in for on with is are be this that it you your use "
            "when or").split())


def toks(s):
    return [t for t in re.findall(r"[a-z0-9]+", fold(s)) if t not in STOP and len(t) > 2]


def baselines():
    names = sorted(skills)
    P = [c for c in cases if c["pos"]]
    docs = {n: set(toks(n.replace("-", " ") + " " + skills[n]["desc"])) for n in names}
    df = {}
    for s in docs.values():
        for t in s:
            df[t] = df.get(t, 0) + 1

    def lex_rank(q):
        qt = set(toks(q))
        sc = {n: sum(math.log(1 + len(names) / df[t]) for t in qt & docs[n]) for n in names}
        return sorted(names, key=lambda n: -sc[n])

    agent = needle.Needle(tools=None, stateless=True)
    t = time.perf_counter()
    E = {n: agent.embed(skills[n]["desc"]) for n in names}
    emb_ms = (time.perf_counter() - t) * 1000 / len(names)

    def cos(a, b):
        return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)

    e1 = e5 = 0
    for c in P:
        qv = agent.embed(c["q"])
        rk = sorted(names, key=lambda n: -cos(qv, E[n]))
        e1 += rk[0] == c["skill"]
        e5 += c["skill"] in rk[:5]
    dim = len(next(iter(E.values())))
    agent.close()
    return {"positives": len(P),
            "lexical_top1": sum(1 for c in P if lex_rank(c["q"])[0] == c["skill"]),
            "lexical_top5": sum(1 for c in P if c["skill"] in lex_rank(c["q"])[:5]),
            "needle_embed_top1": e1, "needle_embed_top5": e5, "embed_dim": dim, "embed_ms_per_text": round(emb_ms, 1)}


if __name__ == "__main__":
    results = {"meta": {"needle": needle.__version__, "skills_core": len(skills), "cases": len(cases),
                        "evaluated_skills": evaluated}, "scenarios": [], "summaries": []}
    for k in SCEN:
        res = run_scenario(k)
        results["scenarios"].append(res)
        results["summaries"].append(summarize(res))
        print(json.dumps(results["summaries"][-1], ensure_ascii=False), flush=True)
    results["baselines"] = baselines()
    print(json.dumps(results["baselines"], ensure_ascii=False), flush=True)
    json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
