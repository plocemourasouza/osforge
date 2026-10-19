#!/usr/bin/env python3
"""Memory recall eval for osforge-db: hit@1 / hit@5 of natural-language questions.

Default: builds a throwaway database from the synthetic fixture (decisions.tsv) and asks
questions.tsv. Never touches ~/.osforge: every run uses its own temp dir for OSFORGE_DB,
OSFORGE_CONFIG and HOME. With --db, a COPY of the given database is queried instead
(the original is never opened for writing) and --questions holds numeric decision ids.

Modes:
  fts     OSFORGE_EMBED=off, `search` (lexical leg only). Fully offline.
  hybrid  OSFORGE_EMBED=ollama, `search-hybrid` (RRF of FTS5 + vector). Needs a reachable
          Ollama with the embedding model; when it is not reachable the run is SKIPPED
          (exit 0, one line saying so). The fixture is embedded with `embed-backfill` first.
  brain   `recall` against a temp qdrant LOCAL store filled by `brain migrate` (ADR-017).
          Embedder from OSFORGE_BRAIN_EMBED (default fake: deterministic, no model, what CI
          runs); `gemma`/`e5-large` use the real model when it is cached. Interpreter:
          OSFORGE_BRAIN_PYTHON, else ~/.osforge/venv/bin/python; models: OSFORGE_BRAIN_MODELS,
          else ~/.osforge/models (both only read). Missing interpreter, qdrant-client or
          model → SKIP (exit 0). Gold matches the row's source key (sqlite decision id).
          --recall=dense|keyword|hybrid picks the recall mode (default dense). Prints the
          median wall time of one `osforge-db recall` call (fresh process, model load included).

Sets (fixture only):
  natural   questions.tsv: questions as a person asks them.
  expanded  questions-expanded.tsv: the same questions as an agent rewrites them before
            searching (4-8 keywords, English plus pt-BR terms, code/file names).

Usage:
  python3 scripts/evals/memory/run.py [--mode=fts|hybrid|brain] [--set=natural|expanded] [--top=5] [--floor=0.8]
                                      [--recall=dense|keyword|hybrid]
                                      [--db=PATH --questions=PATH] [--verbose]
Exit: 0 = hit@5 >= floor (or no floor), 1 = below floor, 2 = usage/setup error.
"""
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ODB = os.path.join(REPO, "scripts", "osforge-db.py")
sys.path.insert(0, os.path.join(REPO, "scripts"))
import osforge_brain  # noqa: E402  (stdlib side only: source keys, model markers)


def parse_args(argv):
    opts = {"mode": "fts", "top": "5", "floor": None, "db": None,
            "questions": None, "verbose": False, "set": "natural", "recall": "dense"}
    for a in argv:
        if a == "--verbose":
            opts["verbose"] = True
        elif a.startswith("--") and "=" in a:
            k, v = a[2:].split("=", 1)
            if k not in opts:
                sys.exit(f"unknown flag --{k}")
            opts[k] = v
        else:
            sys.exit(f"unknown argument {a!r}\n{__doc__}")
    if opts["mode"] not in ("fts", "hybrid", "brain"):
        sys.exit("--mode must be fts, hybrid or brain")
    if opts["recall"] not in ("dense", "keyword", "hybrid"):
        sys.exit("--recall must be dense, keyword or hybrid")
    if opts["set"] not in ("natural", "expanded"):
        sys.exit("--set must be natural or expanded")
    if bool(opts["db"]) != bool(opts["questions"]):
        sys.exit("--db and --questions go together")
    return opts


def read_tsv(path, min_cols):
    rows = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln.strip() or ln.startswith("#"):
                continue
            cols = ln.split("\t")
            if len(cols) < min_cols:
                sys.exit(f"{path}: expected >= {min_cols} TAB columns: {ln!r}")
            rows.append(cols)
    return rows


def odb(env, *args):
    return subprocess.run([sys.executable, ODB, *args], env=env,
                          capture_output=True, text=True, timeout=120)


def build_fixture(env, db_file):
    """Fixture DB through the real CLI (embedding off), then pin created_at."""
    keys = {}
    build_env = dict(env, OSFORGE_EMBED="off", OSFORGE_BRAIN="off")
    odb(build_env, "init")
    rows = read_tsv(os.path.join(HERE, "decisions.tsv"), 5)
    for proj in sorted({r[1] for r in rows}):
        odb(build_env, "upsert-project", proj, f"synthetic fixture project {proj}")
    conn = sqlite3.connect(db_file)
    for key, proj, cat, created, content in (r[:5] for r in rows):
        r = odb(build_env, "add-decision", proj, content, f"--category={cat}")
        if r.returncode != 0:
            sys.exit(f"add-decision failed for {key}: {r.stderr.strip()}")
        did = conn.execute("SELECT max(id) FROM decisions").fetchone()[0]
        conn.execute("UPDATE decisions SET created_at=? WHERE id=?", (created, did))
        conn.commit()            # release the write lock before the next CLI write
        keys[key] = str(did)
    conn.close()
    return keys


def embedder_ready(env):
    r = odb(env, "--json", "memory-health", "--timeout=2")
    try:
        return bool(json.loads(r.stdout).get("embedder_reachable"))
    except (ValueError, AttributeError):
        return False


def brain_runtime():
    """(python, models dir, embed, None) or (.., .., .., skip reason). Resolved from the REAL
    home before HOME is swapped for the temp one; both paths are only read."""
    home = os.path.expanduser("~")
    py = os.environ.get("OSFORGE_BRAIN_PYTHON") or os.path.join(home, ".osforge", "venv", "bin", "python")
    models = os.environ.get("OSFORGE_BRAIN_MODELS") or os.path.join(home, ".osforge", "models")
    embed = (os.environ.get("OSFORGE_BRAIN_EMBED") or "fake").lower()
    if embed not in osforge_brain.EMBEDDERS:
        return py, models, embed, f"unknown OSFORGE_BRAIN_EMBED={embed!r}"
    if not os.path.exists(py):
        return py, models, embed, f"no brain interpreter at {py}"
    r = subprocess.run([py, "-c", "import qdrant_client"], capture_output=True)
    if r.returncode != 0:
        return py, models, embed, f"qdrant-client not importable by {py}"
    marker = osforge_brain.EMBEDDERS[embed][4]
    if marker:
        names = os.listdir(models) if os.path.isdir(models) else []
        if not any(marker in n for n in names) or not any(osforge_brain.BM25_MARKER in n for n in names):
            return py, models, embed, f"{embed} model not cached in {models}"
    return py, models, embed, None


def main():
    opts = parse_args(sys.argv[1:])
    if opts["mode"] == "brain":
        bpy, bmodels, bembed, why = brain_runtime()
        if why:
            print(f"SKIP mode=brain: {why}")
            return 0
    work = tempfile.mkdtemp(prefix="osforge-recall-")
    try:
        db_file = os.path.join(work, "recall.db")
        env = dict(os.environ, HOME=os.path.join(work, "home"), OSFORGE_DB=db_file,
                   OSFORGE_CONFIG=os.path.join(work, "config.json"), OSFORGE_VECTOR="sqlite")
        env.pop("OSFORGE_PROJECT", None)
        os.makedirs(env["HOME"])
        env["OSFORGE_EMBED"] = "ollama" if opts["mode"] == "hybrid" else "off"
        if opts["mode"] == "brain":
            env.update(OSFORGE_BRAIN_PYTHON=bpy, OSFORGE_BRAIN_MODELS=bmodels,
                       OSFORGE_BRAIN_EMBED=bembed, OSFORGE_BRAIN_STORE="local",
                       OSFORGE_BRAIN_PATH=os.path.join(work, "brain-store"))
            for k in ("OSFORGE_BRAIN", "OSFORGE_BRAIN_COLLECTION"):
                env.pop(k, None)

        if opts["db"]:
            src = sqlite3.connect(f"file:{opts['db']}?mode=ro", uri=True)
            dst = sqlite3.connect(db_file)
            src.backup(dst)          # consistent copy, WAL included; source opened read-only
            src.close()
            dst.close()
            keys = None
            label = os.path.basename(opts["db"])
            qrows = read_tsv(opts["questions"], 2)
        else:
            keys = build_fixture(env, db_file)
            label = "fixture"
            qfile = "questions.tsv" if opts["set"] == "natural" else "questions-expanded.tsv"
            qrows = read_tsv(os.path.join(HERE, qfile), 2)

        if opts["mode"] == "hybrid":
            if not embedder_ready(env):
                print(f"SKIP mode=hybrid db={label}: embedder unreachable "
                      "(start Ollama with the embedding model to run this leg)")
                return 0
            if keys is not None:
                odb(env, "embed-backfill")

        if opts["mode"] == "brain":
            t0 = time.perf_counter()
            r = odb(env, "--json", "brain", "migrate")
            try:
                mig = json.loads(r.stdout)
            except ValueError:
                mig = {}
            if r.returncode != 0 or mig.get("degraded") or not mig.get("indexed"):
                print(f"FAIL mode=brain: brain migrate did not index ({(mig.get('degraded') or r.stderr.strip())[:200]})")
                return 1
            print(f"migrate: {mig['indexed']} decisions indexed in {time.perf_counter() - t0:.1f}s "
                  f"(embed={bembed}, batch_size=1)")

        cmd = {"fts": (["search"], "--limit="), "hybrid": (["search-hybrid"], "--top="),
               "brain": (["recall", f"--mode={opts['recall']}"], "--top=")}[opts["mode"]]
        h1 = h5 = 0
        misses = []
        walls = []
        for cols in qrows:
            gold_raw, question = cols[0], cols[1]
            gold = {keys[g] if keys else g for g in gold_raw.split("|")}
            extra = []
            if len(cols) > 2 and cols[2]:
                extra.append(f"--since={cols[2]}")
            if len(cols) > 3 and cols[3]:
                extra.append(f"--until={cols[3]}")
            t0 = time.perf_counter()
            r = odb(env, "--json", *cmd[0], question, f"{cmd[1]}{opts['top']}", *extra)
            walls.append(time.perf_counter() - t0)
            try:
                rows = json.loads(r.stdout)
                if opts["mode"] == "brain":
                    if any(x.get("degraded") for x in rows):
                        print(f"FAIL mode=brain: recall degraded ({rows[0]['degraded']})")
                        return 1
                    ids = [str(osforge_brain.decision_source_id(x.get("source"))) for x in rows]
                else:
                    ids = [str(x.get("id")) for x in rows]
            except (ValueError, AttributeError, TypeError):
                ids = []
            top_ids = ids[:int(opts["top"])]
            hit1 = bool(top_ids[:1]) and top_ids[0] in gold
            hit5 = bool(gold & set(top_ids))
            h1 += hit1
            h5 += hit5
            if not hit5:
                misses.append(gold_raw)
            if opts["verbose"]:
                mark = "1" if hit1 else ("5" if hit5 else "-")
                print(f"  [{mark}] {gold_raw:8} {question}  -> {top_ids}")

        n = len(qrows)
        pct = (lambda k: f"{100 * k / n:.0f}%") if n else (lambda k: "n/a")
        extra_info = ""
        if opts["mode"] == "brain":
            walls.sort()
            med = walls[len(walls) // 2] if walls else 0.0
            extra_info = f" embed={bembed} recall={opts['recall']} wall/call median={med:.2f}s"
        print(f"mode={opts['mode']} set={opts['set'] if keys else 'custom'} db={label} n={n} hit@1={h1}/{n} ({pct(h1)}) "
              f"hit@5={h5}/{n} ({pct(h5)}) miss={misses}{extra_info}")
        if opts["floor"] is not None and n:
            floor = float(opts["floor"])
            if h5 / n < floor:
                print(f"FAIL: hit@5 {h5 / n:.2f} below floor {floor:.2f}")
                return 1
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
