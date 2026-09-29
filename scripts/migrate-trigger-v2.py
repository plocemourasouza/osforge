#!/usr/bin/env python3
"""
migrate-trigger-v2.py — one-shot migration of scripts/evals/trigger/*.json to
the osforge/trigger-eval/v2 schema (B-025 / N-01).

What it does
------------
Reads the human-reviewed labels in docs/intake/needle/rotulos-trigger.tsv
(columns: skill, id, categoria, rota_esperada, critico, query) and, for every
skill's JSON case file:

1. Stamps "category" (and "critical" / "expect_route" where present) onto
   each EXISTING case, matched by id. The query text must match — this is a
   safety check that the TSV row and the JSON case are the same case, not a
   relabeling by position.
2. Appends any NEW case ids found in the TSV (the ones that don't exist yet
   in the JSON file) with should_trigger=false — every new case in the TSV
   is a "vizinho" or "negacao", i.e. a negative — and files them into the
   right split: new "negacao" cases go to "eval" (what we want to measure),
   new "vizinho" cases go to "tune" (spec §3).
3. Bumps "$schema" to "osforge/trigger-eval/v2".

This is a ONE-SHOT script: it mutates scripts/evals/trigger/*.json in place.
Run it again and it's a no-op on an already-migrated set (idempotent), since
step 1 just re-stamps the same values and step 2 finds no new ids left.

Usage:
    python3 scripts/migrate-trigger-v2.py [--tsv PATH] [--cases-dir PATH] [--dry-run]
"""
import argparse
import csv
import json
import os
import sys

SCHEMA_V2 = "osforge/trigger-eval/v2"
VALID_CATEGORIES = {"positivo", "vizinho", "irrelevante", "negacao"}


def load_tsv(path):
    """Group TSV rows by skill, preserving file order."""
    by_skill = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        expected_header = ["skill", "id", "categoria", "rota_esperada", "critico", "query"]
        if header != expected_header:
            raise SystemExit(f"[ERRO] cabeçalho inesperado em {path}: {header}")
        for row in reader:
            if not row or not row[0].strip():
                continue
            skill, cid, cat, route, crit, query = (row + [""] * 6)[:6]
            if cat not in VALID_CATEGORIES:
                raise SystemExit(f"[ERRO] {path}: categoria desconhecida '{cat}' (skill={skill} id={cid})")
            by_skill.setdefault(skill, []).append({
                "id": cid.strip(),
                "category": cat.strip(),
                "route": route.strip(),
                "critical": crit.strip().lower() == "sim",
                "query": query,
            })
    return by_skill


def build_case_v2(existing, row):
    """Reconstruct a case dict in the v2 field order."""
    should_trigger = existing["should_trigger"] if existing else False
    out = {"id": row["id"], "should_trigger": should_trigger, "category": row["category"]}
    if row["critical"]:
        out["critical"] = True
    if row["route"] and row["route"] != "-":
        out["expect_route"] = row["route"]
    out["query"] = row["query"]
    return out


def migrate_file(path, rows, dry_run=False):
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)

    by_id = {c["id"]: c for c in doc["cases"]}
    new_cases = []
    changed = False

    for row in rows:
        existing = by_id.get(row["id"])
        if existing is not None:
            if existing["query"] != row["query"]:
                raise SystemExit(
                    f"[ERRO] {path}: caso {row['id']} — consulta do TSV difere da do JSON.\n"
                    f"  TSV : {row['query']!r}\n  JSON: {existing['query']!r}"
                )
            new_case = build_case_v2(existing, row)
            if existing != new_case:
                changed = True
            by_id[row["id"]] = new_case
        else:
            new_case = build_case_v2(None, row)
            by_id[row["id"]] = new_case
            new_cases.append(new_case)
            changed = True

    # Preserve original case ordering, then append new cases in TSV order.
    ordered_ids = [c["id"] for c in doc["cases"]] + [c["id"] for c in new_cases]
    doc["cases"] = [by_id[i] for i in ordered_ids]

    if doc.get("$schema") != SCHEMA_V2:
        doc["$schema"] = SCHEMA_V2
        changed = True

    # New cases join the split: negacao -> eval (what we measure), vizinho -> tune.
    for c in new_cases:
        target = "eval" if c["category"] == "negacao" else "tune"
        doc["split"][target].append(c["id"])

    if not changed:
        return False

    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return True


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tsv", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "docs", "intake", "needle", "rotulos-trigger.tsv"))
    ap.add_argument("--cases-dir", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "evals", "trigger"))
    ap.add_argument("--dry-run", action="store_true", help="report what would change, write nothing")
    args = ap.parse_args(argv)

    by_skill = load_tsv(args.tsv)

    touched, untouched, missing = [], [], []
    for skill, rows in sorted(by_skill.items()):
        path = os.path.join(args.cases_dir, f"{skill}.json")
        if not os.path.isfile(path):
            missing.append(skill)
            continue
        if migrate_file(path, rows, dry_run=args.dry_run):
            touched.append(skill)
        else:
            untouched.append(skill)

    if missing:
        print(f"[ERRO] sem arquivo de caso para: {', '.join(missing)}", file=sys.stderr)
        return 1

    verb = "seriam alteradas" if args.dry_run else "alteradas"
    print(f"migração v2: {len(touched)} skill(s) {verb}, {len(untouched)} já em dia.")
    if touched:
        print("  " + ", ".join(touched))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
