#!/usr/bin/env python3
"""build_variants.py -- build the per-arm system-prompt texts of an outcome-eval round.

Every round reads its sources from a PINNED git revision (`git show <rev>:<path>`), never from the
working tree, so a later edit under skills/ or agents/ cannot change a past round's variants.

  python3 build_variants.py               # round r1 (default) -> variants/
  python3 build_variants.py --round r2    # round r2           -> r2/variants/
  python3 build_variants.py --round r3    # round r3           -> r3/variants/

Round 1 (rev 58c47e3, the commit the round-1 report was run on): arm B = the SKILL.md body
(frontmatter stripped); arm C = the same body with the prompt audit's cuts applied.
Round 2 (rev 656aaf0): see R2_TARGETS -- arm C is either a set of cuts, or (clean-code) the
previous text from an older revision; for the agent targets arm A is the body WITHOUT the
boilerplate block, B the full body, C = A + one line.
Round 3 (rev fd2e1ff): see build_r3 -- arm C = arm B + the P-01/P-02 text; repo-audit B is the draft
under r3/drafts/; mapa-repo C appends a repository exports map; ponytail-ref B is the vendored
Ponytail SKILL.md (sha256-pinned).
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


# =========================================================================== round 3
# docs/intake/ponytail/MEDICAO-r3.md. Skills read from R3_REV (HEAD of main when r3 was prepared).
# The P-01/P-02 texts below ARE the deliverable of those proposals (English, ADR-011): the skills
# under skills/ are only edited if their arm C wins.
R3_REV = "fd2e1ff"
R3_DIR = os.path.join(HERE, "r3")
R3_OUT = os.path.join(R3_DIR, "variants")

# coding-guidelines + P-01 (SPEC-P01): the solution ladder and "never cut" under section 2,
# one line under section 5.
P01_LADDER = """Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### Solution ladder

Before writing code, stop at the first rung that solves the whole task:

1. Does it need to exist? Leave out what nobody asked for, and name it in one line.
2. Does it already exist in this repository (a helper, component, service, pattern)? Use it the way
   the surrounding code does.
3. Does the standard library or the platform solve it (`Intl`, `crypto.randomUUID()`,
   `URLSearchParams`, `structuredClone`, `<input type="date">`, `<dialog>`)? Use it, unless the project
   has its own: the house component beats the native one.
4. Does an already-installed dependency solve it (Zod, the Supabase client, Prisma's
   `upsert`/`$transaction`)? Use it. Never add a dependency for a few lines.
5. Only then: the minimum code that works.

### Never cut when simplifying

Validation at a trust boundary (user input, webhooks, Server Actions), error handling that prevents
data loss, security and authorization checks, accessibility, and anything the user asked for.

A shortcut with a known limit gets a one-line comment: `shortcut: <the limit>, <when to replace it>`.
Code review treats that comment as a recorded decision, not as a finding."""
CODING_GUIDELINES_P01 = [
    ('Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.', P01_LADDER),
    ("- New code that conflicts with code 30 lines away is a silent regression.\n",
     "- New code that conflicts with code 30 lines away is a silent regression.\n"
     "- Fixing a bug: find every caller of the function you touch and fix the cause once, in the shared code.\n"),
]

# code-review: the dynamic-context lines (!`cmd`) are rendered to what Claude Code would inject in
# the eval's empty, non-git cwd -- applied to B and C alike, so the arms differ only by P-02.
CODE_REVIEW_RENDER = [
    ('!`git log --oneline -10 2>/dev/null || echo "Git not available or not initialized"`\n'
     '!`git diff --stat HEAD 2>/dev/null | tail -5 || echo "Diff not available"`\n',
     "Git not available or not initialized\n"),
]
P02_VERDICT_OLD = """**Verdict:** APPROVED | CHANGES_REQUESTED
**Files reviewed:** {N}
**Findings:** {N}

### Issues (must be resolved)
1. {issue with location and suggestion}

### Suggestions (recommended)
1. {suggestion}

### Positives
1. {something that turned out well}
```"""
P02_VERDICT_NEW = """**Verdict:** APPROVED | CHANGES_REQUESTED
**Assumed load:** {who and what runs this code (one user, one team, many instances) and where that came from}
**Files reviewed:** {N}
**Findings:** {N}

### Issues (must be resolved)
1. {issue with location and suggestion}
   If not fixed: {one sentence: the consequence for the user or the data}

### Suggestions (recommended)
1. {suggestion}

### Positives
1. {something that turned out well}

Not verified: {one line: what mattered and could not be checked}
```"""
# code-review + P-02 (SPEC-P02): connected code in scope, declared load, proof rule, consequence lines.
CODE_REVIEW_P02 = [
    ("- Load project-context.md and the project's `CONTEXT.md` glossary\n",
     "- Load project-context.md and the project's `CONTEXT.md` glossary\n"
     "- When a change alters a function's signature, return value or behaviour (or renames a field, column\n"
     "  or export), search the whole repository for every caller, including files outside the diff, and\n"
     "  review them too\n"
     "- State the expected load, taken from the README, the deploy config or project-context.md (one user,\n"
     "  one team, many processes or instances). Judge scale findings against that load and say it in the report\n"),
    ("**Done when:** the review covers the whole diff since the agreed point — every modified file\n"
     "named, none silently skipped.",
     "**Done when:** the review covers the diff and the code it reaches — every modified file\n"
     "named, none silently skipped, and every caller of a changed signature, return value or behaviour\n"
     "checked, inside or outside the diff."),
    ("**Done when:** each divergence found is tied to the file and line that shows it.",
     "**Proof rule:** every finding needs a concrete case (\"this input or situation leads to this wrong\n"
     "result\"). No case, no finding. A `shortcut: <limit>, <when to replace it>` comment is a recorded\n"
     "decision, not a finding, unless the declared load already exceeds its limit.\n\n"
     "**Done when:** each divergence found is tied to the file and line that shows it."),
    (P02_VERDICT_OLD, P02_VERDICT_NEW),
]

# repo-audit (P-03): B = the draft skill (not installed yet), C = the one-line alternative.
REPO_AUDIT_DRAFT = os.path.join(R3_DIR, "drafts", "repo-audit", "SKILL.md")
REPO_AUDIT_LINE = "List the most serious problems first, each with a concrete case and file:line.\n"

# ponytail-ref (optional, D-P1): Ponytail's SKILL.md body verbatim, vendored with its license.
PONYTAIL_SKILL = os.path.join(R3_DIR, "vendor", "ponytail", "SKILL.md")
PONYTAIL_SHA256 = "9badd22a32e19cb884e46dfa8d3aae82bb81dfa5484105b8b4f0262df823a509"
PONYTAIL_HEADER = """<!--
Ponytail skills/ponytail/SKILL.md, body verbatim (frontmatter stripped), from
https://github.com/DietrichGebert/ponytail at 09c434ab73ca43761c5d8b0c5d341926c2fba710.
Used only as an outcome-eval variant (round r3, target ponytail-ref); not deployed.
MIT License, Copyright (c) 2026 DietrichGebert. Full text: r3/vendor/ponytail/LICENSE, THIRD_PARTY_NOTICES.
driver.py drops this comment from the system prompt; the arm sees only the body below.
-->
"""

# mapa-repo: the exports of the fictional salon app the cg tasks live in, rendered in the format of
# Ponytail's hooks/ponytail-map.js (buildMap) -- one line per folder, shared code first, at most 3
# names per file (1 when the folder has more than 8 files), 30 per line, 2000-char budget. Only names
# and folders: the map says THAT a helper exists, not its signature.
REPO_EXPORTS = [
    ("app/(account)/bookings/actions.ts", ["cancelBooking", "CancelState"]),
    ("app/(account)/bookings/page.tsx", ["BookingsPage"]),
    ("app/(account)/profile/actions.ts", ["updateProfile", "ProfileState"]),
    ("app/(account)/profile/page.tsx", ["ProfilePage"]),
    ("app/(booking)/book/actions.ts", ["createBooking", "BookingState"]),
    ("app/(booking)/book/page.tsx", ["BookPage"]),
    ("app/(shop)/cart/actions.ts", ["addToCart", "removeLine", "checkout"]),
    ("app/(shop)/cart/cart-form.tsx", ["CartForm"]),
    ("app/(shop)/checkout/actions.ts", ["placeOrder"]),
    ("app/(shop)/orders/[id]/confirmation/page.tsx", ["ConfirmationPage"]),
    ("app/(shop)/products/page.tsx", ["ProductsPage"]),
    ("app/api/slots/route.ts", ["GET"]),
    ("app/api/webhooks/payflow/route.ts", ["runtime", "POST"]),
    ("components/account/cancel-booking-button.tsx", ["CancelBookingButton"]),
    ("components/account/profile-form.tsx", ["ProfileForm"]),
    ("components/booking/booking-form.tsx", ["BookingForm"]),
    ("components/booking/service-picker.tsx", ["ServicePicker"]),
    ("components/booking/staff-picker.tsx", ["StaffPicker"]),
    ("components/shop/add-to-cart-button.tsx", ["AddToCartButton"]),
    ("components/shop/cart-summary.tsx", ["CartSummary"]),
    ("components/shop/product-card.tsx", ["ProductCard"]),
    ("components/shop/product-grid.tsx", ["ProductGrid"]),
    ("components/ui/badge.tsx", ["Badge", "badgeVariants"]),
    ("components/ui/button.tsx", ["Button", "buttonVariants"]),
    ("components/ui/card.tsx", ["Card", "CardHeader", "CardTitle", "CardContent"]),
    ("components/ui/dialog.tsx", ["Dialog", "DialogTrigger", "DialogContent", "DialogTitle"]),
    ("components/ui/form-message.tsx", ["FormMessage"]),
    ("components/ui/icon-button.tsx", ["IconButton"]),
    ("components/ui/input.tsx", ["Input"]),
    ("components/ui/label.tsx", ["Label"]),
    ("emails/order-receipt.tsx", ["OrderReceipt"]),
    ("lib/auth.ts", ["getSession", "requireUser", "requireStaff"]),
    ("lib/cart.ts", ["cartTotalCents", "getCart"]),
    ("lib/db.ts", ["prisma"]),
    ("lib/format.ts", ["formatCurrency", "formatDateTime", "formatPhone"]),
    ("lib/money.ts", ["toCents", "fromCents", "sumCents"]),
    ("lib/orders.ts", ["createOrder"]),
    ("lib/receipt.ts", ["buildReceipt"]),
    ("lib/slots.ts", ["Slot", "listSlotsForDay", "nextFreeSlot"]),
    ("lib/supabase/client.ts", ["createClient"]),
    ("lib/supabase/middleware.ts", ["updateSession"]),
    ("lib/supabase/server.ts", ["createClient"]),
    ("lib/types.ts", ["CartLineWithProduct", "OrderWithItems"]),
    ("lib/utils.ts", ["cn"]),
    ("middleware.ts", ["middleware", "config"]),
]
MAP_SHARED = ("util", "helper", "lib", "common", "shared", "service", "component", "hook", "core", "model",
              "schema", "api")


def repo_map(exports, budget=2000):
    """Python port of ponytail-map.js buildMap() for a fixed file -> exported-names table."""
    files = sorted(exports, key=lambda fe: (not any(w in fe[0].lower() for w in MAP_SHARED), fe[0]))
    dirs = {}
    for path, names in files:
        d = os.path.dirname(path) or "."
        dirs.setdefault(d, []).append(names)
    lines, used, skipped = [], 0, 0
    for d, per_file in dirs.items():
        names = []
        for n in per_file:
            for x in n[:1 if len(per_file) > 8 else 3]:
                if x not in names:
                    names.append(x)
        line = "%s/: %s%s" % (d, ", ".join(names[:30]), ", ..." if len(names) > 30 else "")
        if used + len(line) > budget:
            skipped += 1
            continue
        lines.append(line)
        used += len(line) + 1
    return ("Codebase map (what already exists; reuse it, read a file only when you need its details):\n"
            + "\n".join(lines) + ("\n(%d more folders not listed)" % skipped if skipped else ""))


def build_r3():
    import hashlib
    os.makedirs(R3_OUT, exist_ok=True)
    arms = {}
    rel = "skills/coding-guidelines/SKILL.md"
    warn_if_tree_differs(R3_REV, rel)
    cg = strip_frontmatter(git_show(R3_REV, rel))
    cg_c = apply_cuts("coding-guidelines", cg, CODING_GUIDELINES_P01)
    arms["coding-guidelines"] = {"B": cg, "C": cg_c}

    rel = "skills/quality/code-review/SKILL.md"
    warn_if_tree_differs(R3_REV, rel)
    cr = apply_cuts("code-review (render)", strip_frontmatter(git_show(R3_REV, rel)), CODE_REVIEW_RENDER)
    arms["code-review"] = {"B": cr, "C": apply_cuts("code-review", cr, CODE_REVIEW_P02)}

    with open(REPO_AUDIT_DRAFT, encoding="utf-8") as fh:
        draft = fh.read()
    arms["repo-audit"] = {"B": strip_frontmatter(draft), "C": REPO_AUDIT_LINE}

    arms["mapa-repo"] = {"B": cg_c, "C": cg_c.rstrip("\n") + "\n\n" + repo_map(REPO_EXPORTS) + "\n"}

    with open(PONYTAIL_SKILL, "rb") as fh:
        raw = fh.read()
    if hashlib.sha256(raw).hexdigest() != PONYTAIL_SHA256:
        sys.exit("%s changed: it must stay byte-identical to upstream 09c434a (sha256 %s)"
                 % (PONYTAIL_SKILL, PONYTAIL_SHA256))
    arms["ponytail-ref"] = {"B": PONYTAIL_HEADER + strip_frontmatter(raw.decode("utf-8")), "C": cg_c}

    for name, texts in arms.items():
        for arm, text in texts.items():
            write_variant(R3_OUT, name, arm, text)
        print("%-20s %s" % (name, "  ".join("%s=%6d" % (a, len(t)) for a, t in sorted(texts.items()))))
    print("repo-audit B from %s (sha256 %s)" % (os.path.relpath(REPO_AUDIT_DRAFT, REPO),
                                                hashlib.sha256(draft.encode("utf-8")).hexdigest()[:12]))


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--round", default="r1", choices=("r1", "r2", "r3"))
    a = p.parse_args(argv)
    {"r1": build_r1, "r2": build_r2, "r3": build_r3}[a.round]()


if __name__ == "__main__":
    main(sys.argv[1:])
