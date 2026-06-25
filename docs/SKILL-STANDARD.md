# OSForge Skill Authoring Standard — unified

**What this is:** the single standard that **merges the ties** between `mattpocock/skills` and OSForge and **brings/adapts what Matt wins**, so Claude Code interprets any skill with maximum clarity (= predictability).
**How it's used:** becomes the "Skill Writing Guide" that `skill-creator` points to, validated by `scripts/test-skill-triggering.sh`.
**Status:** specification + examples. Nothing applied to the repo yet.

> **Authoring language:** this document — and all OSForge repo content — is written in **English** (see §0.1).

---

## 0. Single principle (the ruler)

> A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same *process* every run — is the root virtue. (adapted from `writing-great-skills`)

Everything below serves it, on two axes: **ACTIVATION** (pick the right skill) and **EXECUTION** (run the same way, knowing when it's done).

## 0.1 Language policy (NEW — applies repo-wide)

Two rules, kept separate:

1. **Authoring = English.** All OSForge content is written in English: `SKILL.md` bodies and descriptions, agents, rules, `CLAUDE.md`, `SKILLS.md`, commands, ADRs, code comments. One language removes the mixed pt-BR/English inconsistency and aligns with the model's strongest priors (leading words like *seam*, *red*, *tight* are English anyway). This **supersedes** the previous repo convention ("prose largely pt-BR — match that").

2. **Runtime = the user's language.** The agent **replies in whatever language the user writes in**. User writes pt-BR → answer in pt-BR; user writes English → answer in English. This is a global behavior rule in `CLAUDE.md`, independent of the content being English.

**Drop-in `CLAUDE.md` rule:**
```md
## Language
- All repository content (skills, agents, rules, CLAUDE.md, SKILLS.md, commands, ADRs, comments) is authored in ENGLISH.
- ALWAYS reply to the user in the language they wrote in (e.g., user writes Brazilian Portuguese → reply in Brazilian Portuguese). Translate as needed; never force the user into English.
```

**Honest cross-lingual caveat (matters for ACTIVATION):** if every description becomes English but users prompt in pt-BR, triggering must rely on the model's *semantic* (cross-lingual) matching, not lexical keyword overlap. Two mitigations: (a) keep `Keywords:` rich enough that intent is unambiguous; (b) the triggering harness MUST include pt-BR user prompts as test cases, so we verify English descriptions still fire on Portuguese input. See §5.A.

---

## 1. What TIES → merged into one structure

Both sides use the same body techniques (Iron Law, anti-patterns, numbered process, "when NOT to use"). Merged, they become the **canonical SKILL.md body**:

```
# <Title> (<leading word>)

**Iron Law:** <ONE inviolable rule, UPPERCASE, anchored on a leading word>

## When NOT to use
<cases that look similar but aren't — mirrors the description's "Do NOT use for">

## Process
### 1. <step>
<action> → **Done when:** <CHECKABLE and, where it matters, EXHAUSTIVE criterion>
### 2. <step>
...

## Anti-patterns
| WRONG | RIGHT |
|---|---|
| <bad pattern> | <good pattern> |

## References  (progressive disclosure)
- `<file>.md` — <what it holds; loaded only when the pointer fires>
```

Robustness rules (from `writing-great-skills`):
- **Completion criterion** on every step: the agent must tell *done* from *not-done*. "every modified model accounted for" (exhaustive) > "produce a change list" (vague → *premature completion*).
- **Leading word**: a pretrained concept (`red`, `tight`, `tracer bullet`, `seam`) repeated to anchor behavior in few tokens.

---

## 2. What Matt WINS → brought/adapted

| Item | Decision | How it lands in OSForge |
|---|---|---|
| Predictability theory (`writing-great-skills`) | **Bring whole** | This document + a meta skill, referenced by `skill-creator` |
| Explicit invocation axis (`disable-model-invocation`) | **Bring whole** | Official frontmatter field (Claude Code already supports it) |
| Leading words | **Adapt** | Mandatory section of the guide; auditable |
| Completion criterion | **Adapt** | "Done when:" on every step (see §1) |
| Router skill (`ask-matt`) | **Adapt** | Thin layer over the orchestrator |
| `codebase-design` (glossary-as-contract) | **Bring adapted** | New skill with OSForge frontmatter + `inspired_by` |
| `grilling` | **Bring adapted** | Light primitive + 2 rules in `CLAUDE.md` |

---

## 3. Unified frontmatter (merges both sides)

Combines OSForge's activation pattern + Matt's invocation axis + OSForge's execution routing. **All labels in English:**

```yaml
---
name: <slug>
description: "<summary, leading word first>. Use when: <1 trigger per branch, no synonyms>. Keywords: <terms>. Do NOT use for: <explicit disambiguation vs sibling skills>."

# Invocation axis (CONSCIOUS DECISION — from Matt):
disable-model-invocation: true   # ONLY if ORCHESTRATOR (user-invoked). Omit if DISCIPLINE (model-invoked).

# Execution routing (OSForge strength — keep):
model: sonnet                    # sonnet | opus | haiku
context: fork                    # if it runs isolated
agent: general-purpose           # if it delegates to a subagent
allowed-tools: Read, Grep, Glob, Edit

metadata:
  version: "1.0.0"
  inspired_by: <org/repo (skill)>     # if adapted from a third party (MIT)
  source: <org/repo>
---
```

Description golden rule (Matt): **one trigger per branch**, leading word first, no identity that already lives in the body.

> Note: this replaces the legacy `ACIONE quando / Não acione para` (pt-BR) labels with `Use when / Do NOT use for` (English), per §0.1.

---

## 4. Audit checklist (Matt's failure modes, operationalized)

- [ ] **Premature completion** — does every step have a checkable "Done when:"?
- [ ] **No-op** — any line the model already obeys by default? ("be thorough" → delete or replace with a strong leading word like "relentless")
- [ ] **Duplication** — same meaning in two places? (single source of truth)
- [ ] **Sprawl** — too long? → push reference to a linked file (progressive disclosure)
- [ ] **Sediment** — stale layers nobody removes? → prune aggressively
- [ ] **Activation** — has `Use when` + `Keywords` + `Do NOT use for`? Invocation axis decided?
- [ ] **Language** — body and description in English? (§0.1)

---

## 5. Examples resolving the honest caveats

### 5.A — "standardizing touches many skills → risky mega-diff" (now also a translation pass)

The language switch means each skill is **standardized AND translated pt-BR→English in the same batch**. Use the harness OSForge already has (`scripts/test-skill-triggering.sh` + `skill-triggering-cases.tsv`):

```
1. Standardize + translate ONE batch (e.g., the 3 skills in §6).
2. Add triggering cases — INCLUDING pt-BR user prompts — to skill-triggering-cases.tsv.
3. Run: ./scripts/test-skill-triggering.sh
4. Green (activation didn't regress, incl. cross-lingual)? Commit. Red? Fix the description.
5. Next batch.
```

Batches by increasing risk: (1) the 3 in §6 → (2) `engineering`/`stack` → (3) `agency` (121 skills, largest volume) → (4) the rest. Never a single 142-skill diff. The pt-BR test prompts are the safety net for the English-description / Portuguese-user gap.

### 5.B — "without a single template, inconsistency returns"

**Solution: `SKILL.template.md` as the source of truth** (delivered alongside). `skill-creator` copies it as the starting point and audits against it. One place defines the shape.

### 5.C — "third-party attribution (MIT)"

**Solution: `inspired_by`/`source` frontmatter**, as already done in `ui-design-intelligence`. Example for `codebase-design`:

```yaml
metadata:
  version: "1.0.0"
  inspired_by: mattpocock/skills (codebase-design)
  license_note: "Adapted under MIT; concepts from Ousterhout/Feathers"
```

---

## 6. BEFORE/AFTER examples (the real §5 defects + the language switch)

### 6.1 `systematic-debugging` — missing negative trigger + pt-BR → English

**BEFORE (real):**
> "Debugging sistemático em 4 fases com análise de causa raiz. ACIONE quando: bug difícil de reproduzir, crash sem stacktrace claro… Keywords: debug, bug, error, crash, fix, issue, not working, broken, regression, investigate."

**AFTER (unified standard, English):**
> "Diagnosis loop for hard bugs and performance regressions (leading word: **feedback loop**). Use when: a bug is hard to reproduce, behavior is intermittent, a regression has no obvious cause, or deep root-cause investigation is needed. Keywords: debug, crash, intermittent, regression, root cause. Do NOT use for: trivial bug with an obvious stack trace (fix directly), type/lint error (clean-code), an already-red test with a clear cause (tdd-workflow)."

Changed: added `Do NOT use for` (disambiguates from `clean-code`/`tdd-workflow`); leading word "feedback loop" up front; keywords pruned of synonyms (one branch, not six); English.

### 6.2 `tdd-workflow` — already English but duplicated branch, no negatives

**BEFORE (real):**
> "Enforces Test-Driven Development (RED-GREEN-REFACTOR) workflow. Use when implementing any feature, bugfix, or behavior change. … Triggers on tasks involving new features, bug fixes, refactoring…"

**AFTER:**
> "Test-first discipline with the **RED**-GREEN-REFACTOR loop. Use when: building a feature or fixing a bug test-first, or the user mentions TDD / test-first / red-green. Keywords: TDD, test-first, red-green-refactor. Do NOT use for: throwaway prototype, generated code (Prisma Client, shadcn), pure UI styling."

Changed: collapsed "feature/bugfix/behavior change/new features/bug fixes/refactoring" (one branch written 6× → *duplication*) into one; leading word **RED**; added exceptions as `Do NOT use for`.

### 6.3 No-op pruning

**BEFORE:** "Be thorough and carefully analyze the code before making changes."
**AFTER:** *(deleted)* — the agent already does this by default; the line pays tokens to change nothing. If real emphasis is needed, use a leading word: "Investigate **relentless**ly until the feedback loop goes red."

### 6.4 `codebase-design` brought in with OSForge frontmatter

```yaml
---
name: codebase-design
description: "Shared vocabulary for designing deep modules (leading words: seam, depth, adapter). Use when: designing or improving a module's interface, deciding where a seam goes, making code testable or AI-navigable, or when another skill needs the deep-module vocabulary. Keywords: deep module, seam, interface, depth, adapter, testability, architecture refactor. Do NOT use for: pragmatic code cleanup (clean-code), stack/ADR decisions (technical-design-doc-creator)."
model: sonnet
allowed-tools: Read, Grep, Glob
metadata:
  version: "1.0.0"
  inspired_by: mattpocock/skills (codebase-design)
---
```
(body: glossary-as-contract "use these terms exactly", deletion test, "the interface is the test surface", DEEPENING.md + DESIGN-IT-TWICE.md adapted to `dispatching-parallel-agents`.)

### 6.5 `grilling` — the 2 rules as a global rule in `CLAUDE.md`

```md
## Alignment before building (grilling)
- Ask ONE question at a time — multiple at once is bewildering.
- If the answer is in the code, explore the code instead of asking.
- For each question, offer your recommended answer.
```

---

## 7. Adoption plan (phased, not executed yet)

1. **Commit 1 — foundation:** add `SKILL-STANDARD.md` + `SKILL.template.md`; point `skill-creator` to them.
2. **Commit 2 — global rules:** Language policy (§0.1) + grilling block in `CLAUDE.md`; update the legacy "prose largely pt-BR" line.
3. **Commit 3 — pilot batch:** standardize + translate the 3 skills in §6; add cases (incl. pt-BR prompts) to the harness; run `test-skill-triggering.sh`; green → commit.
4. **Commit 4+ — by category** (engineering → stack → agency → rest), each validated by the harness.
5. **In parallel:** bring `codebase-design` and `grilling` as skills (§2).

Each step is small, reversible, and validated — never a mega-diff.

---

## 8. Result in one sentence

A **single template + a predictability guide**, all repo content in **English** with replies in the **user's language**, where **activation** uses OSForge's Use-when/Keywords/Do-NOT-use pattern with Matt's description rigor, **execution** uses the canonical structure (Iron Law + completion criteria + anti-patterns) with leading words, and **routing** uses OSForge's execution frontmatter + Matt's invocation axis — all auditable by the failure modes and validated by the harness that already exists.
