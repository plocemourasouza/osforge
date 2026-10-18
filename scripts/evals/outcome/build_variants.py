#!/usr/bin/env python3
"""build_variants.py -- build the arm B (current) and arm C (reduced) system-prompt texts.

Arm B = the current SKILL.md body (frontmatter stripped), read from skills/ at build time.
Arm C = the same body with the prompt audit's proposed cuts applied. Every cut is an exact
old->new replacement asserted to match ONCE, so a SKILL.md edit that moves the text makes this
script fail loudly instead of silently producing a C that equals B.

SKILL.md files under skills/ are never written. Output: variants/<skill>.B.md, <skill>.C.md.
Python 3 stdlib only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "variants")

SKILLS = {
    "clean-code": "skills/clean-code/SKILL.md",
    "frontend-design": "skills/frontend-design/SKILL.md",
    "adversarial-review": "skills/quality/adversarial-review/SKILL.md",
}


def strip_frontmatter(text):
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        return text[end + 5:].lstrip("\n")
    return text


# --------------------------------------------------------------------------- clean-code cuts
# Audit: drop shouting (CRITICAL/MANDATORY/ANY/THINK FIRST in caps -> plain); drop the "Don't"
# prohibitions that restate KISS/YAGNI (Summary table); keep naming/function/structure rules
# and the anti-pattern table.
CLEAN_CODE = [
    ("> **CRITICAL SKILL** - Be **concise, direct, and solution-focused**.",
     "Be concise, direct, and solution-focused."),
    ("| **SRP** | Single Responsibility - each function/class does ONE thing |",
     "| **SRP** | Single Responsibility - each function/class does one thing |"),
    ("## Before Editing ANY File (THINK FIRST!)\n\n**Before changing a file, ask yourself:**",
     "## Before Editing a File\n\nBefore changing a file, check:"),
    ("> **Rule:** Edit the file + all dependent files in the SAME task.\n"
     "> **Never leave broken imports or missing updates.**",
     "Edit the file and its dependents in the same task, so no import or caller is left broken."),
    ("""## Summary

| Do | Don't |
|----|--------|
| Write code directly | Write tutorials |
| Let code self-document | Add obvious comments |
| Fix bugs directly | Write a tutorial before fixing |
| Inline small things | Create unnecessary files |
| Name things clearly | Use abbreviations |
| Keep functions small | Write 100+ line functions |

> The user wants working code plus enough context to trust it.""",
     "The user wants working code plus enough context to trust it."),
    ("## Self-Check Before Completing (MANDATORY)\n\n**Before saying \"task complete\", verify:**",
     "## Self-Check Before Completing\n\nBefore saying the task is complete, verify:"),
    ("> **Rule:** If ANY check fails, fix it before completing.",
     "If a check fails, fix it before completing."),
    ("Three sections checked reads exactly like six; the skipped one is where the debt lives.",
     ""),
]

# --------------------------------------------------------------------------- frontend-design cuts
# Audit: "CRITICAL: ASK BEFORE ASSUMING (MANDATORY)/STOP!" -> a plain clarify line; Selective
# Reading Rule (MANDATORY) -> plain; caps MUST/NEVER -> plain; KEEP the avoid-defaults table,
# extend it with named Opus defaults, replace the "Red/Neon Green" and "brutalist edges" rows
# with "derive from brand".
FD_OLD_TABLE_HEAD = """## CRITICAL: ASK BEFORE ASSUMING (MANDATORY)

> **STOP! If the user's request is open-ended, DO NOT default to your favorites.**

### When User Prompt is Vague, ASK:

**Color not specified?** Ask:
> "What color palette do you prefer? (blue/green/orange/neutral/other?)"

**Style not specified?** Ask:
> "What style are you going for? (minimal/bold/retro/futuristic/organic?)"

**Layout not specified?** Ask:
> "Do you have a layout preference? (single column/grid/asymmetric/full-width?)"

### DEFAULT TENDENCIES TO AVOID (ANTI-SAFE HARBOR):"""
FD_NEW_TABLE_HEAD = """## Clarify Before Assuming

If the request leaves brand, audience or style open, ask one or two short questions — or state
the assumptions you are making and proceed. Do not fill the gap with your usual defaults.

### Default Tendencies to Avoid"""

FRONTEND_DESIGN = [
    ("## Selective Reading Rule (MANDATORY)\n\n**Read REQUIRED files always, OPTIONAL only when needed:**",
     "## Selective Reading\n\nRead the required file first; read the optional ones only when the task needs them:"),
    ("| [references/ux-psychology.md](references/ux-psychology.md) | **REQUIRED** | Always read first! |",
     "| [references/ux-psychology.md](references/ux-psychology.md) | Required | Read first |"),
    ("> **ux-psychology.md = ALWAYS READ. Others = only if relevant.**\n", ""),
    (FD_OLD_TABLE_HEAD, FD_NEW_TABLE_HEAD),
    ("| **Deep Cyan / Fintech Blue** | Safe harbor from purple ban | Why not Red, Black, or Neon Green? |",
     "| **Deep Cyan / Fintech Blue** | Safe harbor from purple ban | Derive the palette from the brand |"),
    ("| **Rounded everything** | Generic/Safe | Where can I use sharp, brutalist edges? |",
     "| **Rounded everything** | Generic/Safe | Derive the shape language from the brand |\n"
     "| **Cream / beige / off-white page background** | Current default \"tasteful\" look | Use the brand's own neutrals |\n"
     "| **One italic or serif accent word in the headline** | Signature AI-landing tell | Keep the headline in one voice |\n"
     "| **01 / 02 / 03 numbered section labels** | Decorative numbering with no meaning | Label sections by content |\n"
     "| **Monospace uppercase eyebrow labels** | Borrowed dev-tool aesthetic | Only if the brand is technical |\n"
     "| **Pill-shaped buttons and badges everywhere** | Default rounding | Match the brand's shape language |"),
    ("> **\"Every 'safe' structure you choose brings you one step closer to a generic template. TAKE RISKS.\"**",
     "Each safe default you pick moves the design closer to a generic template."),
    ("## 1. Constraint Analysis (ALWAYS FIRST)\n\nBefore any design work, ANSWER THESE or ASK USER:",
     "## 1. Constraint Analysis (first)\n\nBefore design work, answer these from the brief, or ask:"),
    ("4. **ASK USER** if not specified", "4. Ask the user if not specified"),
    ("### AI Tendency Patterns (AVOID!)", "### AI Tendency Patterns"),
    ("- **Purple/violet everything (PURPLE BAN)**", "- **Purple/violet everything**"),
    ("   └── If unclear → ASK (don't default!)", "   └── If unclear → ask or state assumptions"),
    ("   └── If unclear → ASK", "   └── If unclear → ask"),
    ("This skill exists to **break that convergence**. Every design MUST\n> be a unique expression",
     "This skill exists to break that convergence. Each design should\n> be an expression"),
    ("### Complexity Matching (MANDATORY)\n\nCode complexity MUST mirror the aesthetic vision:",
     "### Complexity Matching\n\nCode complexity should mirror the aesthetic vision:"),
    ("- **NEVER:** a minimalist design with unnecessary complex code, or an ambitious design with lazy code",
     "- Avoid a minimalist design with unnecessarily complex code, or an ambitious design with lazy code"),
    ("> **IMPORTANT**\n> For Next.js 16+ projects", "> For Next.js 16+ projects"),
    ("**Avoid the Modern SaaS Safe Harbor!**", "Avoid the modern SaaS safe harbor."),
    ("applied when Constraint Analysis ran FIRST (always), the ASK-BEFORE-ASSUMING questions were asked "
     "when the prompt was vague, and each principle family the deliverable touches (UX, Layout, Color, "
     "Typography, Effects) was consulted per the Selective Reading Rule — only the relevant families, "
     "but ALL of the relevant ones.",
     "applied when constraint analysis ran first, open questions were asked (or assumptions stated) "
     "when the prompt was vague, and each principle family the deliverable touches (UX, Layout, Color, "
     "Typography, Effects) was consulted."),
]

# --------------------------------------------------------------------------- adversarial-review cuts
# Audit: replace the "cynical, jaded ... EXPECT ... ASSUME problems exist" persona with a
# skeptical, experienced reviewer that reports only what survives the pre-report gate.
ADVERSARIAL_REVIEW = [
    ("""A cynical, jaded reviewer with zero tolerance for sloppy work.
The content was submitted by someone careless and you EXPECT to find
problems. Be skeptical of everything. Look for what is MISSING, not just what
is wrong. Precise, professional tone — no personal attacks.""",
     """A skeptical, experienced reviewer. Assume nothing is correct until you have checked it.
Look for what is missing, not just what is wrong. Report only what survives the pre-report
gate below. Precise, professional tone."""),
    ("Review with extreme skepticism — ASSUME problems exist.",
     "Check each area below; do not take correctness on trust."),
    ("- HALT if the areas of attack for this content type were not all worked — finish them before reporting",
     "- Finish all areas of attack for this content type before reporting"),
    ("Prioritization is mandatory — not optional.", "Always prioritize."),
]

CUTS = {
    "clean-code": CLEAN_CODE,
    "frontend-design": FRONTEND_DESIGN,
    "adversarial-review": ADVERSARIAL_REVIEW,
}


def apply_cuts(name, text, cuts):
    for i, (old, new) in enumerate(cuts):
        n = text.count(old)
        if n != 1:
            sys.exit("%s cut #%d: expected exactly 1 match, found %d:\n%s" % (name, i, n, old[:120]))
        text = text.replace(old, new)
    return text


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, rel in SKILLS.items():
        with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
            body = strip_frontmatter(fh.read())
        reduced = apply_cuts(name, body, CUTS[name])
        for arm, text in (("B", body), ("C", reduced)):
            with open(os.path.join(OUT, "%s.%s.md" % (name, arm)), "w", encoding="utf-8") as fh:
                fh.write(text)
        print("%-20s B=%6d chars  C=%6d chars  (%+d)" % (name, len(body), len(reduced),
                                                        len(reduced) - len(body)))


if __name__ == "__main__":
    main()
