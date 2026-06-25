---
name: autorefine-skill
description: "Iterative autonomous refinement with autoresearch loop + meta-optimization + cross-domain transfer. Use when (e.g. 'improve my frontend skill'): user asks to 'improve a skill', 'optimize skill X', 'skill Y is not working well', 'iterate on a skill', 'autorefine', 'refine code', 'optimize performance', 'improve metric X', 'meta-optimize', 'transfer learning', 'apply a pattern from another project'. Generalized to any artifact with a measurable metric — skills, code, prompts, configs, docs. Keywords: improve skill, refine skill, optimize, autorefine, autonomous iteration, autoresearch, improvement loop, self-improving, guard, verify, meta-optimization, transfer, cross-domain."
model: sonnet
allowed-tools: Read, Write, Bash, Glob, Grep
metadata:
  author: osforge
  version: '3.0'
  inspired_by: 'karpathy/autoresearch, uditgoenka/autoresearch, alfonsograziano/auto-agent, facebookresearch/HyperAgents'
  changelog: 'v3.0 — meta-optimization of skills (self-improvement loop) + multi-domain transfer via osforge-db. v2.0 — verify+guard separation, osforge-db memory, domain generalization, eval packages'
---

## Project state
!`osforge-db list-projects --status=active 2>/dev/null | head -3 || echo "no active project"`
!`osforge-db search "autorefine" 2>/dev/null | head -5 || echo "no autorefine history"`
!`osforge-db search "meta-review" 2>/dev/null | head -3 || echo "no prior meta-reviews"`
!`osforge-db search "transfer-candidate" 2>/dev/null | head -3 || echo "no transfer candidates"`

# AutoRefine v3

## Principle

Apply Karpathy's autonomous research loop to **any artifact with a measurable metric**: skills, code, prompts, configs, documentation. The agent formulates a hypothesis → applies an atomic change → verifies with a mechanical metric → protects against regressions with a guard → keeps or reverts → records in the database → repeats.

**constraint + mechanical metric + autonomous iteration = compounding gains**

v3 adds two layers inspired by HyperAgents (Meta Research):
- **Meta-optimization**: the loop analyzes its own success/failure patterns and adjusts the autorefine SKILL.md
- **Cross-domain transfer**: hypotheses validated in one project propagate to similar projects via osforge-db
---

## Two operation modes

### Skill Mode (refine an OSForge SKILL.md)
The original mode: iterate over a skill's content to improve its outputs.
Artifact: `skills/<name>/SKILL.md`. Metric: approval on test prompts.

### Generic Mode (any artifact with a metric)
An expanded mode inspired by generalized autoresearch: iterate over any file/set of files where a mechanical metric exists.

Examples:
- **Code**: `npm test -- --coverage` → improve test coverage
- **Performance**: `lighthouse --output=json` → improve Core Web Vitals
- **Bundle**: `bun build && du -sh dist/` → reduce size
- **Prompt**: `python eval.py` → improve accuracy on a dataset
- **Config**: `bun run bench` → improve throughput

---

## Initial setup

Before starting the loop, collect from the user:

### 1. Scope

| Question | Example |
|---|---|
| Which artifact to refine? | `skills/frontend-design/SKILL.md` or `src/lib/auth.ts` |
| What is the problem/objective? | "the skill generates code without TypeScript" or "p95 latency above 200ms" |
| Which files may be modified? | Explicit list (scope constraint) |
| Which files are read-only? | Guard files — never modified |
### 2. Verify + Guard (mandatory separation)

```
Verify: <command that measures the main metric>
Guard:  <command that ensures nothing else broke>
```

**Verify** = "Did the metric improve?" — it is the optimization objective.
**Guard** = "Did anything else break?" — it is the safety net.

| Scenario | Verify | Guard | Decision |
|---|---|---|---|
| ✅ improves | ✅ passes | ✅ passes | **KEEP** |
| ✅ improves | ✅ passes | ❌ fails | **REWORK** (max 2 attempts, then DISCARD) |
| ❌ worsens | ❌ fails | ✅ passes | **DISCARD** |
| ❌ worsens | ❌ fails | ❌ fails | **DISCARD + immediate rollback** |

Examples of verify/guard pairs:

| Domain | Verify | Guard |
|---|---|---|
| OSForge Skill | `python eval_skill.py --prompts=3` | `grep -c "allowed-tools" SKILL.md` (frontmatter intact) |
| Test coverage | `bun test --coverage \| grep Stmts` | `bun tsc --noEmit` (types not broken) |
| API performance | `bun run bench:api \| grep p95` | `bun test` (functionality intact) |
| Bundle size | `bun build && du -sh dist/` | `bun test && bun tsc --noEmit` |
| Prompt engineering | `python eval.py --metric=accuracy` | `python eval.py --metric=safety` (safety ≥ baseline) |

If the guard is not defined by the user, the default is: `exit 0` (no guard). But **always suggest** a relevant guard.
### 3. Budget and test prompts

| Configuration | Default |
|---|---|
| Iterations | 5 (max 10) |
| Test prompts (skill mode) | 2-3 real examples |
| Metric direction | higher-is-better or lower-is-better |

### 4. Mandatory snapshot

```bash
cp -r <artifact-dir> <artifact-dir>-snapshot-$(date +%Y%m%d%H%M)
```

### 5. Load hypothesis memory

```bash
# Search prior autorefine iterations on this artifact
osforge-db search "autorefine <artifact-name>" 2>/dev/null

# v3: Also search transfer candidates from other projects
osforge-db search "transfer-candidate <domain>" 2>/dev/null
```

If prior hypotheses exist that failed, **never repeat them**. List the known failed hypotheses before formulating new ones.

If there are **transfer candidates** from other projects in the same domain, list them as priority hypotheses (already validated in a similar context).

---

## The Loop (modify → verify → guard → keep/discard → log → repeat)
### Iron rules

| # | Rule | Implementation |
|---|---|---|
| 1 | Loop until budget runs out | Bounded: N iterations, then stop |
| 2 | Read before writing | Understand the full context before modifying |
| 3 | One change per iteration | Atomic and traceable — if it breaks, you know why |
| 4 | Mechanical verification only | Numbers, not subjective judgment |
| 5 | Automatic rollback | Failure → revert via git or snapshot |
| 6 | Simplicity wins | Same result + less code = KEEP |
| 7 | Git is memory | Commits prefixed `experiment:` preserve history |
| 8 | When stuck, think harder | Re-read, combine near-misses, try a radical approach |

### Structure of each iteration

```
Iteration N:
  1. [haiku]  Read the current artifact + git log + memory (hypotheses that already failed)
  1b.[haiku]  Query transfer-candidates from the same domain (v3)
  2. [haiku]  Formulate hypothesis: "if I modify X, metric Y will improve because Z"
  3. [haiku]  Apply ONE atomic modification
  4. [haiku]  git commit -m "experiment: <summarized hypothesis>"
  5. [haiku]  Run Verify → collect metric
  6. [haiku]  Run Guard → verify nothing broke
  7. [sonnet] Decide: KEEP / REWORK / DISCARD (see table above)
  8. [sonnet] If DISCARD → git revert HEAD
     [sonnet] If REWORK → try to adjust (max 2x), then DISCARD
  9. Record in log + osforge-db
  9b.If KEEP → assess eligibility for transfer (v3)
```
### Model per step (smart-model-dispatch)

| Step | Model | Reason |
|---|---|---|
| Reading + hypothesis + modification | Haiku | Mechanical, low cost |
| Verify + guard execution | Haiku | Running commands |
| Evaluation + decision | Sonnet | Requires judgment |
| Final synthesis (report) | Sonnet | Pattern analysis |
| Meta-review (v3) | Sonnet | Aggregated cross-session analysis |
| Transfer decision (v3) | Sonnet | Assess generalization |

Use Opus only if the criterion is ambiguous and requires reasoning about architectural tradeoffs.

---

## Iteration log (TSV + markdown)

### TSV (machine-readable)

Maintain `autorefine-results.tsv` in the artifact directory:

```tsv
iteration	commit	metric	delta	guard	status	hypothesis	transfer_eligible
0	a1b2c3d	85.2	0.0	pass	baseline	initial state	-
1	b2c3d4e	87.1	+1.9	pass	keep	add explicit TypeScript types to output rules	yes
2	-	86.5	-0.6	pass	discard	refactor section ordering (no improvement)	-
3	c4d5e6f	89.3	+2.2	pass	keep	add code block examples for each pattern	yes
4	d5e6f7g	91.0	+1.7	fail	rework	aggressive minification broke guard tests	-
4b	e6f7g8h	90.8	+1.5	pass	keep	conservative minification (guard-safe)	no
```
### Markdown (human-readable)

Maintain `autorefine-log.md` during the process:

```markdown
# AutoRefine Log — <artifact-name>
Date: <date>
Budget: <N> iterations
Verify: <command>
Guard: <command>
Direction: higher-is-better | lower-is-better

## Iteration 1
- Hypothesis: ...
- Modification: ...
- Metric: X → Y (delta: +Z)
- Guard: pass | fail
- Result: KEEP | DISCARD | REWORK
- Reason: ...
- Transfer eligible: yes | no | - (reason)

## Final result
- Best version: iteration N
- Initial metric: X
- Final metric: Y (delta: +Z, improvement of W%)
- Hypotheses that worked: ...
- Hypotheses that failed: ...
- Transfer candidates: N hypotheses marked
```

---
## Cross-session memory (osforge-db)

At the end of each autorefine session, persist the learnings:

```bash
# Record each KEEP hypothesis as a decision
osforge-db add-decision <project-slug> \
  "autorefine(<artifact>): KEEP — <summarized hypothesis> (metric +<delta>)" \
  --category=arch

# Record each DISCARD hypothesis as a decision
osforge-db add-decision <project-slug> \
  "autorefine(<artifact>): DISCARD — <summarized hypothesis> (reason: <reason>)" \
  --category=arch

# Record the final result
osforge-db add-decision <project-slug> \
  "autorefine(<artifact>): result — metric <initial> → <final> (+<delta>%) in <N> iterations" \
  --category=arch

# v3: Record transfer candidates
osforge-db add-decision <project-slug> \
  "transfer-candidate(<domain>): <summarized hypothesis> — validated on <artifact> (metric +<delta>)" \
  --category=transfer

# v3: Record meta-review
osforge-db add-decision <project-slug> \
  "meta-review: <N> sessions analyzed — patterns: <list of patterns found>" \
  --category=meta
```

In the next session, the loop queries `osforge-db search "autorefine <artifact>"` and avoids repeating hypotheses that already failed. This creates **institutional learning** — the agent does not make the same mistakes across sessions.
---

## Crash recovery

| Failure | Response |
|---|---|
| Syntax error in the artifact | Immediate fix, do not count as an iteration |
| Runtime error in verify/guard | Try a fix (max 3x), then skip |
| Command timeout | Revert, try a smaller variant |
| Guard breaks after verify passes | REWORK (max 2x), then DISCARD |
| Process interrupted | Snapshot preserves state; `osforge-db resume` resumes |

---

## Stopping conditions

End the loop before exhausting the budget if:

1. **Convergence** — 3 consecutive KEEP iterations with no further measurable improvement
2. **Saturation** — 100% of criteria approved for 2 consecutive iterations
3. **Persistent regression** — 3 consecutive DISCARD iterations (the improvement hypothesis is wrong; stop and discuss with the user)
4. **Budget exhausted** — N iterations completed

Progress printed every 5 iterations (if budget > 5).
---

## 🧠 Meta-optimization (v3 — Idea A: Self-Improvement Loop)

> Inspired by HyperAgents (Meta Research): the system that improves artifacts
> should also improve itself. Pragmatic metacognition without Docker/GPU.

### Concept

After **N accumulated sessions** in osforge-db (threshold: 10 sessions or 50+ recorded hypotheses), AutoRefine analyzes its own success/failure patterns and generates concrete adjustments to this SKILL.md. This is second-order self-improvement — it does not optimize the artifact, it optimizes **how** it optimizes artifacts.

### When to trigger

The meta-review is triggered automatically when:

```bash
# Count accumulated sessions
SESSIONS=$(osforge-db search "autorefine" 2>/dev/null | grep -c "result")
HYPOTHESES=$(osforge-db search "autorefine" 2>/dev/null | grep -c "KEEP\|DISCARD")

# Threshold: 10+ sessions OR 50+ hypotheses
if [ "$SESSIONS" -ge 10 ] || [ "$HYPOTHESES" -ge 50 ]; then
  echo "META-REVIEW eligible"
fi
```

It can also be triggered manually: `"meta-optimize autorefine"`, `"review autorefine patterns"`, `"autorefine self-improve"`.
### Meta-review process (5 phases)

#### Phase 1: Aggregated data collection

```bash
# Extract all autorefine records
osforge-db search "autorefine" --json 2>/dev/null > /tmp/autorefine-history.json

# Expected structure per session:
# - artifact, domain, mode (skill/generic)
# - KEEP hypotheses: description, delta, domain
# - DISCARD hypotheses: description, reason, domain
# - result: initial metric → final, % improvement
```

#### Phase 2: Pattern analysis [sonnet]

The agent analyzes the corpus and answers:

| Question | Example insight |
|---|---|
| Which **hypothesis types** have the highest KEEP rate? | "Strong-typing hypotheses: 78% KEEP vs 34% average" |
| Which **hypothesis types** always fail? | "Section reordering: 0/12 KEEP — never improves the metric" |
| Which **domain** responds best to autorefine? | "Skills: +18% average vs Code: +7% average" |
| Is there a correlation between **change size** and success? | "Changes <20 lines: 62% KEEP; >50 lines: 11% KEEP" |
| Which **verify+guard combinations** work best? | "tsc+test: 89% guard-pass vs test-only: 64%" |
| How many iterations per session is optimal? | "Marginal gain drops after iteration 4 in 80% of cases" |
| Is REWORK worth it? | "REWORK→KEEP: 38% of the time — worth keeping" |
#### Phase 3: Generate adjustment proposals

Based on the patterns, the agent generates **concrete proposals** to modify this SKILL.md:

```markdown
## Meta-Review Proposal #1
Pattern: "Reordering hypotheses never work (0/12)"
Adjustment: Add to the Iron Rules: "Rule 9: Do not formulate pure section-reordering hypotheses"
Estimated impact: Saves ~2 iterations/session (avoids dead ends)
Confidence: high (12 samples, 0% success)

## Meta-Review Proposal #2
Pattern: "Marginal gain drops after iteration 4"
Adjustment: Reduce default budget from 5 to 4 iterations
Estimated impact: Reduces cost by 20% with no significant loss of gain
Confidence: medium (80% of cases, but 20% still gain on the 5th)

## Meta-Review Proposal #3
Pattern: "Changes >50 lines almost always fail"
Adjustment: Add to setup: "WARN if the iteration diff exceeds 50 lines"
Estimated impact: Flags over-scoped hypotheses before verify
Confidence: high (89% correlation)
```

#### Phase 4: Apply adjustments (with approval)

**NEVER apply meta-adjustments automatically.** Always present the proposals to the user and ask for explicit approval before modifying the SKILL.md. Each approved proposal generates:

```bash
# Backup before meta-adjustment
cp skills/autorefine-skill/SKILL.md skills/autorefine-skill/SKILL.md.pre-meta-$(date +%Y%m%d)

# Apply the approved modification
# ... (editing SKILL.md)

# Commit with the meta: prefix
git commit -m "meta(autorefine): <adjustment description> — based on <N> sessions"
```
#### Phase 5: Record the meta-review in osforge-db

```bash
osforge-db add-decision global \
  "meta-review(autorefine): analyzed <N> sessions, <M> hypotheses. Patterns: <list>. Adjustments applied: <list of approved proposals>" \
  --category=meta
```

### Meta-optimization guardrails

| Rule | Reason |
|---|---|
| Max 1 meta-review per week | Avoids over-fitting on insufficient data |
| Min 10 sessions between meta-reviews | Ensures a statistically relevant sample |
| Proposals need ≥5 supporting samples | Avoids generalizing from isolated cases |
| Mandatory backup before each meta-adjustment | Reversible if the adjustment worsens performance |
| Meta-adjustments are always presented, never auto-applied | The human decides what changes in the process |
| Keep a meta-review history in osforge-db | Track the evolution of the skill itself over time |

### Meta-optimization metrics

After 3+ meta-reviews, compare:

```
KEEP rate before the meta-adjustment vs after
Average iterations per session before vs after
% of budget used before vs after
Average time per session before vs after (if available)
```

If a meta-adjustment **worsens** the aggregate metrics, revert it and record it as "meta-discard" in osforge-db.
---

## 🔄 Cross-Domain Transfer (v3 — Idea B: Knowledge Propagation)

> Inspired by HyperAgents' multi-domain evaluation: validate that improvements
> transfer across similar contexts. An optimization that works in one project
> should not die there — it should propagate to projects in the same domain.

### Concept

When a hypothesis is KEEP with a significant delta, AutoRefine assesses whether it is **generalizable** — whether the underlying insight applies to other projects in the same domain. If so, it marks it as `transfer-candidate` in osforge-db. In the next autorefine session on a similar project, these hypotheses appear as **priority suggestions** (already validated in another context).

### Domain taxonomy

| Domain | Identifiers | Artifact examples |
|---|---|---|
| `nextjs-frontend` | Next.js, React, Tailwind, components | `src/components/`, `src/app/` |
| `api-backend` | API routes, tRPC, Prisma, endpoints | `src/server/`, `src/api/` |
| `database` | Prisma schema, migrations, queries | `prisma/schema.prisma` |
| `devops` | Docker, CI/CD, deploy, infra | `Dockerfile`, `.github/workflows/` |
| `skill-osforge` | OSForge SKILL.md | `skills/*/SKILL.md` |
| `prompt-eng` | Prompts, system messages, templates | `prompts/`, `*.prompt.md` |
| `config` | Configs, env, settings | `*.config.*`, `.env*` |
| `docs` | Documentation, READMEs, specs | `docs/`, `*.md` |

The domain is inferred automatically from the artifact's path and content. If ambiguous, ask the user.
### Transfer eligibility criteria

A KEEP hypothesis is eligible for transfer if **all** conditions are true:

| Criterion | Reason |
|---|---|
| Delta ≥ 1.5% (higher-is-better) or ≥ 1.5% reduction (lower-is-better) | Improvement must be significant, not noise |
| Guard passed without REWORK | If REWORK was needed, the hypothesis has edge cases |
| The hypothesis is **about the pattern**, not the specific artifact | "Add explicit types" transfers; "Rename variable X to Y" does not |
| The artifact's domain is in the taxonomy | Classification is needed for matching |

### Generalization assessment [sonnet]

For each eligible KEEP hypothesis, the agent answers:

```
Hypothesis: "add code blocks with examples for each pattern"
Original artifact: skills/frontend-design/SKILL.md
Domain: skill-osforge

Generalization questions:
1. Does this hypothesis depend on something specific to this artifact? → No
2. Could other artifacts in the "skill-osforge" domain benefit? → Yes
3. Can the hypothesis be formulated generically? → "Skills with concrete code examples
   have +15-25% approval on test prompts"

Decision: TRANSFER ✅
Generic formulation: "Add ≥1 code block per pattern section in skills that define patterns"
Target domain: skill-osforge
```
### Recording transfer-candidates

```bash
# Record a transfer candidate
osforge-db add-decision <project-slug> \
  "transfer-candidate(<domain>): <generic hypothesis> — validated on <artifact> (metric +<delta>%, guard pass)" \
  --category=transfer

# Real example:
osforge-db add-decision my-saas \
  "transfer-candidate(skill-osforge): add ≥1 code block per pattern section — validated on skills/frontend-design/SKILL.md (metric +22%, guard pass)" \
  --category=transfer
```

### Consuming transfer-candidates (in the loop setup)

In setup step 5 ("Load memory"), in addition to searching for failed hypotheses, search for candidates:

```bash
# Identify the current artifact's domain
DOMAIN=$(# infer from path + content)

# Search transfer candidates for this domain
osforge-db search "transfer-candidate($DOMAIN)" 2>/dev/null
```

If candidates exist, present them to the user:

```
📦 Hypotheses transferred from other projects (domain: skill-osforge):

1. [+22%] "Add ≥1 code block per pattern section"
   Origin: my-saas / skills/frontend-design/SKILL.md
   
2. [+18%] "Include an anti-patterns section with examples of what NOT to do"
   Origin: other-project / skills/api-design/SKILL.md

Would you like to use any as a priority hypothesis? (y/N)
```

Transferred hypotheses enter as the **first iterations** of the loop (before new hypotheses), since they already have prior validation.
### Transfer validation

A transferred hypothesis still needs to pass the normal loop (verify + guard). Possible results:

| Result in the new project | Action |
|---|---|
| KEEP with a similar delta (±30% of the original) | **TRANSFER CONFIRMED** — record as cross-project validation |
| KEEP with a smaller delta | **PARTIAL TRANSFER** — works but with less impact |
| DISCARD | **TRANSFER FAILED** — the pattern does not generalize to this context |

```bash
# Record the transfer result
osforge-db add-decision <new-project-slug> \
  "transfer-result(<domain>): <CONFIRMED|PARTIAL|FAILED> — '<hypothesis>' from <origin-project> → delta <original> vs <current>" \
  --category=transfer
```

### Transfer-candidate maturity

As a candidate is tested in more projects, its confidence grows:

| Validations | Status | Behavior |
|---|---|---|
| 1 (origin) | 🟡 candidate | Suggested as "experimental" |
| 2 (1 confirmation) | 🟢 validated | Suggested as "recommended" |
| 3+ (multiple confirmations) | 🔵 proven | Auto-applied if `--auto-transfer` is active |
| 1+ FAILED without CONFIRMED | 🔴 revoked | Removed from suggestions |

```bash
# Query a candidate's maturity
osforge-db search "transfer-result" 2>/dev/null | grep "<hypothesis>" | \
  awk '{confirmed+=/CONFIRMED/; failed+=/FAILED/} END {print confirmed, failed}'
```

`proven` candidates (3+ validations) can be promoted to **iron rules** or **gotchas** in this SKILL.md by the meta-review (Idea A), closing the A↔B cycle.
---

## Final report

When ending the loop:

```
## AutoRefine v3 — Final Result

Artifact: <name>
Mode: Skill | Generic
Domain: <taxonomy domain>
Iterations: N/budget
Metric: <initial> → <final> (delta: +X, improvement: Y%)
Guard: <N> passes, <M> fails, <K> reworks

### Hypotheses that worked (KEEP)
| # | Hypothesis | Delta | Guard | Transfer |
|---|----------|-------|-------|----------|
| 1 | <description> | +1.9 | pass | ✅ eligible |
| 3 | <description> | +2.2 | pass | ✅ eligible |
| 4b | <description> | +1.5 | pass | ❌ specific |

### Hypotheses that failed (DISCARD)
| # | Hypothesis | Reason |
|---|----------|-------|
| 2 | <description> | no measurable improvement |
| 4 | <description> | guard failure (tests broke) |

### Transfers applied in this session
| Hypothesis | Origin | Original delta | Delta here | Status |
|---|---|---|---|---|
| <description> | <project> | +22% | +19% | CONFIRMED |

### Transfer candidates generated
| Generic hypothesis | Domain | Delta |
|---|---|---|
| <description> | skill-osforge | +2.2 |
### Persisted memory
- <N> decisions recorded in osforge-db
- <M> transfer candidates marked
- The next session will query failed hypotheses + transfer-candidates automatically
- Meta-review eligible? <yes/no> (sessions: X/10, hypotheses: Y/50)

### Suggested next steps
- <suggestion based on observed patterns>
- <suggestion of transfer-candidates to test in other projects>
```

Offer to commit with a conventional message:
```
refine(<scope>): autorefine <artifact> — N iterations, metric +X%, <M> transfers
```

Wait for explicit approval before committing.

---

## Gotchas

### Modifying too much per iteration
The loop works with atomic hypotheses. Rewriting the entire artifact in a single iteration makes it impossible to know what caused improvement or regression.

### Verify without Guard
Optimizing a metric without a guard is like driving without brakes — the metric improves but everything else breaks. Always define a guard, even a simple one (`bun test` or `tsc --noEmit`).

### Repeating failed hypotheses
Without cross-session memory, the agent repeats the same hypotheses that already failed. Always query `osforge-db search "autorefine <artifact>"` before formulating hypotheses.

### Not taking a snapshot first
The snapshot is mandatory. Without it, there is no way to revert to the original version.
### Vague success criterion
"Get better" is not a criterion. The criterion must be mechanical and binary — a command that returns a number or pass/fail.

### Evaluating with Haiku
The KEEP/DISCARD decision must use Sonnet. Haiku generates modifications; Sonnet judges results.

### Guard files in the modification scope
Files used by the guard can NEVER be in the modification scope. If the guard is `bun test`, the test files are read-only.

### (v3) Transferring hypotheses without checking the domain
A `nextjs-frontend` hypothesis does not transfer to `database`. Always check domain compatibility before suggesting a transfer.

### (v3) Auto-applying meta-adjustments without approval
Meta-optimization changes the improvement process itself. **Always** present proposals to the user. Never modify the SKILL.md automatically.

### (v3) Trusting transfer-candidates with 1 validation
A candidate with 1 validation is 🟡 experimental. It needs 2+ cross-project confirmations to be 🟢 validated. Do not treat it as a rule until there is sufficient evidence.

---

## Full A ↔ B cycle

```
Autorefine session
  → KEEP hypotheses with a significant delta
    → Generalization assessment [Idea B]
      → transfer-candidate in osforge-db
        → Next session in another project of the same domain
          → Transferred hypothesis as priority
            → Validation: CONFIRMED / PARTIAL / FAILED
              → Mature candidate (proven) after 3+ confirmations
                → Meta-review [Idea A] promotes it to a proven pattern
                  → New iron rule or gotcha in this SKILL.md
                    → All future sessions benefit
```

The two ideas feed each other: **B generates data** (transfer results), **A analyzes that data** (meta-review) and **crystallizes the patterns** (adjusts the SKILL.md). OSForge gets smarter with every autorefine session, in any project.