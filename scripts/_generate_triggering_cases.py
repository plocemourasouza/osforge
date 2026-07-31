#!/usr/bin/env python3
"""
Harvest triggering test cases from skill frontmatter.

The premise
-----------
Every skill already ships its own test cases: the phrases after `Use when:` and
the quoted trigger phrases inside the description were written by the author as
"this is when I should fire". Nobody ever ran them. 174 skills, ~25 hand-written
cases — the gap is not for lack of material, it is for lack of harvesting.

So a generated case is deliberately the skill's OWN wording, not a paraphrase.
That makes a failure sharp: if a skill does not fire on the exact phrase its
author wrote as its trigger, the description is broken. No ambiguity about
whether the test prompt was fair.

Output
------
`scripts/skill-triggering-cases.generated.tsv`, same 2-column format as the
hand-written file (skill_name<TAB>prompt), so the harness reads either.

The hand-written `skill-triggering-cases.tsv` stays authoritative for the
critical skills: those prompts are naive user phrasing that shares no words with
the description, which is a strictly harder — and more realistic — test.

Usage
-----
    python3 scripts/_generate_triggering_cases.py
    python3 scripts/_generate_triggering_cases.py --per-skill 3
    python3 scripts/_generate_triggering_cases.py --stdout
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS_DIR = BASE / "skills"
OUT = BASE / "scripts" / "skill-triggering-cases.generated.tsv"
HAND = BASE / "scripts" / "skill-triggering-cases.tsv"

sys.path.insert(0, str(BASE / "scripts"))
from _extract_index import extract_frontmatter  # noqa: E402

MIN_LEN = 26           # shorter than this is a bare keyword, not a prompt
MAX_LEN = 160
MIN_WORDS = 4

# Fragments that talk ABOUT the skill instead of describing a user's situation.
# They make unfair cases: a FAIL would be the test's fault, not the skill's.
NOT_A_PROMPT = re.compile(
    r"^(another skill|the agent|the orchestrator|when another|use this|invoked by"
    r"|this skill|it |they )", re.I
)
META = re.compile(r"\b(this skill|these \d|the skill|paradigms?|frontmatter|sub-?agent)\b", re.I)

# Conectivos que sobram ao fatiar uma lista longa de cláusulas. O `[:,]?` cobre
# o "when:" órfão que sobra quando a description escreve "Use when: user asks…".
LEAD = re.compile(r"^(or|and|when|whenever|if|after|before|user|the user)\b[:,]?\s+", re.I)

# Uma cláusula que emenda em exemplo vira fragmento quando o exemplo é cortado
# ("… extensive docs — e.g."). Corta antes do exemplo.
EXAMPLE = re.compile(r"\s*[—\-–(,;]\s*(e\.g\.?|i\.e\.?|ex\.|por exemplo|such as)\b.*$", re.I)

# Sobrou pontuação de emenda no fim → a cláusula foi cortada no meio.
DANGLING = re.compile(r"[—\-–:,;/(]\s*$|\b(e\.g|i\.e|etc|ex)\.?\s*$", re.I)


def quoted_phrases(desc: str) -> list[str]:
    """
    Trigger phrases the author put in quotes — e.g. "improve accessibility".
    These are the best generated cases: already written as user speech.
    """
    out = []
    for m in re.finditer(r"[\"'“”]([^\"'“”]{8,120}?)[\"'“”]", desc):
        p = m.group(1).strip()
        if p and not p.endswith(":") and " " in p:
            out.append(p)
    return out


def use_when_clauses(desc: str) -> list[str]:
    m = re.search(r"Use when:?\s*(.+?)(?:\s*Keywords?:|\s*Do NOT|$)", desc, re.I | re.S)
    if not m:
        m = re.search(r"(?:Triggers? on|Trigger):?\s*(.+?)(?:\s*Keywords?:|\s*Do NOT|$)", desc, re.I | re.S)
    if not m:
        return []
    body = re.sub(r"\s+", " ", m.group(1))
    parts = re.split(r"\s*[;,]\s+(?=[a-zA-Z])", body)
    return [p.strip().rstrip(".") for p in parts if p.strip()]


def carry(clause: str) -> str:
    """
    Embrulha uma cláusula de `Use when:` numa mensagem de usuário.

    Cláusula solta chega como fragmento e o modelo responde ao fragmento, não
    ao pedido. Observado duas vezes em rodadas reais:
      "a response came back truncated"  -> "Workdir empty, session fresh — no
                                            truncated response here."
      "a document exceeds the context…" -> "Message look like cut-off fragment"
    Nos dois casos a skill não disparou porque não havia pedido nenhum. O
    embrulho preserva o vocabulário do gatilho e devolve a forma de pergunta.
    """
    clause = clause[0].lower() + clause[1:] if clause[:1].isupper() else clause
    return f"I need help with this: {clause}. What's the right approach?"


def make_cases(name: str, desc: str, per_skill: int) -> list[str]:
    cands: list[str] = []
    seen: set[str] = set()

    # Frases entre aspas já são fala de usuário e vão verbatim; cláusulas
    # precisam do embrulho.
    quoted = quoted_phrases(desc)
    for p in quoted + use_when_clauses(desc):
        is_quoted = p in quoted
        p = LEAD.sub("", p.strip().strip("`").strip()).strip()
        # A trigger ends at the first sentence break; what follows is identity
        # ("Produces a 9-section summary…"), which no user would type.
        p = p.split(". ")[0].strip()
        p = EXAMPLE.sub("", p).strip()
        if DANGLING.search(p):
            continue
        # Splitting a clause list can cut inside parentheses, leaving "(lsof" —
        # a prompt no human would send, so the case would be unfair.
        if p.count("(") != p.count(")"):
            continue
        if not (MIN_LEN <= len(p) <= MAX_LEN):
            continue
        if len(p.split()) < MIN_WORDS:
            continue
        if NOT_A_PROMPT.match(p) or META.search(p):
            continue
        # A prompt naming the skill would test nothing.
        if name.lower().replace("-", " ") in p.lower() or name.lower() in p.lower():
            continue
        key = p.lower()
        if key in seen:
            continue
        seen.add(key)
        cands.append(p if is_quoted else carry(p))
        if len(cands) >= per_skill:
            break

    return cands


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--per-skill", type=int, default=2, help="max cases per skill (default 2)")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()

    hand_skills = set()
    if HAND.exists():
        for line in HAND.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#") and "\t" in line:
                hand_skills.add(line.split("\t", 1)[0].strip())

    lines = [
        "# skill-triggering-cases.generated.tsv — GENERATED, do not hand-edit.",
        "# Source: scripts/_generate_triggering_cases.py (harvests each skill's own",
        "# `Use when:` clauses and quoted trigger phrases).",
        "#",
        "# A FAIL here means the skill does not fire on the wording its own author",
        "# chose as its trigger — that is a defect in the description, not in the test.",
        "# The hand-written skill-triggering-cases.tsv is the harder suite: naive user",
        "# phrasing that shares no vocabulary with the description.",
        "#",
        "# Format: skill_name<TAB>prompt",
        "",
    ]

    total = 0
    covered = 0
    skipped: list[str] = []
    for sf in sorted(SKILLS_DIR.rglob("SKILL.md")):
        # Buckets de ciclo de vida ficam fora da suíte: uma skill aposentada
        # falhando o teste é ruído, não sinal.
        if any(p.startswith("_") for p in sf.relative_to(SKILLS_DIR).parts[:-1]):
            continue
        content = sf.read_text(encoding="utf-8", errors="replace")
        name, desc = extract_frontmatter(content)
        name = (name or sf.parent.name).strip()
        cases = make_cases(name, desc or "", args.per_skill)
        if not cases:
            skipped.append(name)
            continue
        covered += 1
        for c in cases:
            lines.append(f"{name}\t{c}")
            total += 1

    body = "\n".join(lines) + "\n"

    if args.stdout:
        print(body)
        return 0

    OUT.write_text(body, encoding="utf-8")
    n_skills = sum(
        1 for sf in SKILLS_DIR.rglob("SKILL.md")
        if not any(p.startswith("_") for p in sf.relative_to(SKILLS_DIR).parts[:-1])
    )
    print(f"{OUT.relative_to(BASE)}")
    print(f"  {total} cases from {covered}/{n_skills} skills ({args.per_skill} max each)")
    print(f"  {len(skipped)} skills yielded nothing usable — their description has no")
    print(f"  quotable trigger phrase and no `Use when:` clause long enough to be a prompt.")
    print(f"  That list IS the description-quality backlog:")
    for s in skipped[:15]:
        print(f"    {s}")
    if len(skipped) > 15:
        print(f"    … +{len(skipped) - 15} more")
    print(f"\n  {len(hand_skills)} skills also have hand-written cases (harder suite).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
