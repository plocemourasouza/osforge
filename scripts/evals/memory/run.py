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

Sets (fixture only):
  natural   questions.tsv: questions as a person asks them.
  expanded  questions-expanded.tsv: the same questions as an agent rewrites them before
            searching (4-8 keywords, English plus pt-BR terms, code/file names).

Usage:
  python3 scripts/evals/memory/run.py [--mode=fts|hybrid] [--set=natural|expanded] [--top=5] [--floor=0.8]
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

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ODB = os.path.join(REPO, "scripts", "osforge-db.py")


def parse_args(argv):
    opts = {"mode": "fts", "top": "5", "floor": None, "db": None,
            "questions": None, "verbose": False, "set": "natural"}
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
    if opts["mode"] not in ("fts", "hybrid"):
        sys.exit("--mode must be fts or hybrid")
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
    build_env = dict(env, OSFORGE_EMBED="off")
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


def main():
    opts = parse_args(sys.argv[1:])
    work = tempfile.mkdtemp(prefix="osforge-recall-")
    try:
        db_file = os.path.join(work, "recall.db")
        env = dict(os.environ, HOME=os.path.join(work, "home"), OSFORGE_DB=db_file,
                   OSFORGE_CONFIG=os.path.join(work, "config.json"), OSFORGE_VECTOR="sqlite")
        env.pop("OSFORGE_PROJECT", None)
        os.makedirs(env["HOME"])
        env["OSFORGE_EMBED"] = "off" if opts["mode"] == "fts" else "ollama"

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

        cmd = (["search"], "--limit=") if opts["mode"] == "fts" else (["search-hybrid"], "--top=")
        h1 = h5 = 0
        misses = []
        for cols in qrows:
            gold_raw, question = cols[0], cols[1]
            gold = {keys[g] if keys else g for g in gold_raw.split("|")}
            extra = []
            if len(cols) > 2 and cols[2]:
                extra.append(f"--since={cols[2]}")
            if len(cols) > 3 and cols[3]:
                extra.append(f"--until={cols[3]}")
            r = odb(env, "--json", *cmd[0], question, f"{cmd[1]}{opts['top']}", *extra)
            try:
                ids = [str(x.get("id")) for x in json.loads(r.stdout)]
            except (ValueError, AttributeError):
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
        print(f"mode={opts['mode']} set={opts['set'] if keys else 'custom'} db={label} n={n} hit@1={h1}/{n} ({pct(h1)}) "
              f"hit@5={h5}/{n} ({pct(h5)}) miss={misses}")
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
