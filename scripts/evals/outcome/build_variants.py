#!/usr/bin/env python3
"""build_variants.py -- build the per-arm system-prompt texts of an outcome-eval round.

Every round reads its sources from a PINNED git revision (`git show <rev>:<path>`), never from the
working tree, so a later edit under skills/ or agents/ cannot change a past round's variants.

  python3 build_variants.py               # round r1 (default) -> variants/
  python3 build_variants.py --round r2    # round r2           -> r2/variants/

Round 1 (rev 58c47e3, the commit the round-1 report was run on): arm B = the SKILL.md body
(frontmatter stripped); arm C = the same body with the prompt audit's cuts applied.
Round 2 (rev 656aaf0): see R2_TARGETS -- arm C is either a set of cuts, or (clean-code) the
previous text from an older revision; for the agent targets arm A is the body WITHOUT the
boilerplate block, B the full body, C = A + one line.
Every cut is an exact old->new replacement asserted to match ONCE, so a source edit that moves
the text makes this script fail loudly instead of silently producing C == B.

Files under skills/ and agents/ are never written. Python 3 stdlib only.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "variants")
R1_REV = "58c47e3"

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


def git_show(rev, rel):
    proc = subprocess.run(["git", "show", "%s:%s" % (rev, rel)], cwd=REPO, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        sys.exit("git show %s:%s failed: %s" % (rev, rel, proc.stderr.strip()))
    return proc.stdout


def warn_if_tree_differs(rev, rel):
    path = os.path.join(REPO, rel)
    if os.path.exists(path) and open(path, encoding="utf-8").read() != git_show(rev, rel):
        print("note: working-tree %s differs from %s; the variant uses %s" % (rel, rev, rev))


def write_variant(out_dir, name, arm, text):
    with open(os.path.join(out_dir, "%s.%s.md" % (name, arm)), "w", encoding="utf-8") as fh:
        fh.write(text)


def build_r1():
    os.makedirs(OUT, exist_ok=True)
    for name, rel in SKILLS.items():
        body = strip_frontmatter(git_show(R1_REV, rel))
        reduced = apply_cuts(name, body, CUTS[name])
        for arm, text in (("B", body), ("C", reduced)):
            write_variant(OUT, name, arm, text)
        print("%-20s B=%6d chars  C=%6d chars  (%+d)" % (name, len(body), len(reduced),
                                                        len(reduced) - len(body)))


# =========================================================================== round 2
R2_REV = "656aaf0"
R2_OUT = os.path.join(HERE, "r2", "variants")

# verification-before-completion -- audit cuts: drop the moralising ("dishonesty", "lying"), fold
# the Red Flags list into one line, fix the deploy-path-dependent cp. Iron Law, Gate Function and
# the evidence table are kept verbatim.
VBC_RED_FLAGS_OLD = """## Red Flags — STOP Immediately

You are about to violate this skill if you catch yourself:

- Using **"should"**, "probably", "seems to", "likely works"
- Expressing satisfaction before verification: "Great!", "Perfect!", "Done!"
- About to commit or push without running the test suite
- Trusting a previous run as evidence for current state
- Relying on partial verification ("lint passes so types must be fine")
- Thinking "just this once" or "it's a small change"
- Feeling tired and wanting to wrap up"""
VBC_RED_FLAGS_NEW = """## Red Flags

Treat as unverified: 'should work', 'probably', a previous run's result, partial checks (lint passing ≠ types pass)."""
VERIFICATION = [
    ("Claiming work is complete without verification is dishonesty, not efficiency.",
     "A completion claim is only as good as the output that backs it."),
    ("Skip any step = lying, not verifying.", "A skipped step means the claim is unverified."),
    (VBC_RED_FLAGS_OLD, VBC_RED_FLAGS_NEW),
    ("cp ~/.claude/hooks/validate.py .scripts/validate.py", "cp <osforge-repo>/hooks/validate.py .scripts/validate.py"),
]

# behavioral-modes -- audit cuts: the CRITICAL/NO-caps bullets of IMPLEMENT become two plain
# lines; the summary placeholder says what a summary is for; the "NOT:" counter-example goes.
BEHAVIORAL = [
    ("- **CRITICAL: Use `clean-code` skill standards** - concise, direct, no verbose explanations\n",
     "- Follow clean-code: solve the problem directly; comment only where the code cannot say why.\n"),
    ("- **NO tutorial-style explanations** - just code\n"
     "- **NO unnecessary comments** - let code self-document\n"
     "- **NO over-engineering** - solve the problem directly\n"
     "- **NO RUSHING** - Quality > Speed. Read ALL references before coding.\n",
     "- Read the relevant references before coding; ask only about genuine ambiguities.\n"),
    ("[Brief summary, max 1-2 sentences]", "[Short summary of what changed and anything the user must do]"),
    ('**NOT:**\n```\n"Building [feature]...\n\n✓ Created [file1]\n✓ Created [file2]\n✓ Updated [file3]\n\n'
     '[long explanation]\n\nRun `npm run dev` to test."\n```\n\n', ""),
]

# output-enforcement -- audit cuts: resolve the upstream through the manifest instead of a deploy
# path; the banned-pattern lists and "Do NOT optimize for brevity" become one line; "PT triggers".
OE_BANNED_OLD = """## Banned Output Patterns (HARD FAILURES)

### In code blocks
- `// ...`
- `// rest of code`
- `// implement here`
- `// TODO` (unless explicitly part of the deliverable)
- `/* ... */`
- `// similar to above`
- `// continue pattern`
- `// add more as needed`
- bare `...` standing in for omitted code

### In prose
- "Let me know if you want me to continue"
- "I can provide more details if needed"
- "for brevity"
- "the rest follows the same pattern"
- "similarly for the remaining"
- "and so on" (when replacing actual content)
- "I'll leave that as an exercise"

### Structural shortcuts
- Outputting a skeleton when the request was for a full implementation
- Showing first and last section while skipping the middle
- Replacing repeated logic with one example + a description
- Describing what code should do instead of writing it

"""
OUTPUT_ENFORCEMENT = [
    ("> 1. Read `~/.claude/skills/full-output-enforcement/SKILL.md` — upstream anti-truncation rules",
     "> 1. If the base rules are needed, resolve `full-output-enforcement` via the SKILLS.md manifest"),
    ("PT triggers", "trigger phrases"),
    ("Do NOT optimize for brevity — optimize for completeness.\n",
     "Write every requested deliverable in full. If you must stop at the output limit, stop at a clean "
     "boundary and emit the [PAUSED — X of Y complete …] marker.\n"),
    (OE_BANNED_OLD, ""),
]

# agents (H17) -- the two boilerplate sections at the end of every agent body.
AGENT_BLOCK = """## Reality Check (Anti-Self-Deception)

Before delivering ANY output, verify:

1. **Did I actually solve the problem?** — Re-read the original request. Does my output address it directly?
2. **Am I guessing?** — If uncertain about any technical detail, say so explicitly instead of fabricating.
3. **Is this the simplest solution?** — Could this be done with less code, fewer abstractions, or a more standard approach?
4. **Would I ship this?** — If this went to production right now, would I be confident? If not, what's missing?
5. **Am I being sycophantic?** — Am I agreeing with a bad approach just to be agreeable? Push back if needed.

## Quality Control Loop (MANDATORY)

Before completing ANY task:

1. **Re-read** the original request
2. **Compare** your output against the request — does it match?
3. **Verify** all code compiles/runs (don't assume)
4. **Check** for common mistakes: missing imports, wrong paths, hardcoded values, missing error handling
5. **Test** edge cases mentally: empty inputs, null values, concurrent access, network failures
6. **Confirm** naming conventions match the project's existing patterns
"""
AGENT_LINE = "Before delivering, confirm the output answers the original request and say where you are uncertain.\n"

# target -> (kind, source path, extra)
R2_TARGETS = {
    "clean-code": ("previous", "skills/clean-code/SKILL.md", "0fb36cd"),
    "verification-before-completion": ("cuts", "skills/verification-before-completion/SKILL.md", VERIFICATION),
    "behavioral-modes": ("cuts", "skills/behavioral-modes/SKILL.md", BEHAVIORAL),
    "output-enforcement": ("cuts", "skills/output-enforcement/SKILL.md", OUTPUT_ENFORCEMENT),
    "agent-planner": ("agent", "agents/planner.md", None),
    "agent-code-reviewer": ("agent", "agents/code-reviewer.md", None),
}


def build_r2():
    os.makedirs(R2_OUT, exist_ok=True)
    for name, (kind, rel, extra) in R2_TARGETS.items():
        warn_if_tree_differs(R2_REV, rel)
        body = strip_frontmatter(git_show(R2_REV, rel))
        if kind == "previous":
            arms = {"B": body, "C": strip_frontmatter(git_show(extra, rel))}
        elif kind == "cuts":
            arms = {"B": body, "C": apply_cuts(name, body, extra)}
        else:
            without = apply_cuts(name, body, [(AGENT_BLOCK, "")]).rstrip("\n") + "\n"
            arms = {"A": without, "B": body, "C": without + "\n" + AGENT_LINE}
        for arm, text in arms.items():
            write_variant(R2_OUT, name, arm, text)
        print("%-32s %s" % (name, "  ".join("%s=%6d" % (a, len(t)) for a, t in sorted(arms.items()))))


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--round", default="r1", choices=("r1", "r2"))
    a = p.parse_args(argv)
    build_r1() if a.round == "r1" else build_r2()


if __name__ == "__main__":
    main(sys.argv[1:])
