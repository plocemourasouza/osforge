---
name: tlc-spec-driven
description: Product-driven planning with 5 phases - Discover, Specify, Design, Tasks, Implement+Validate+Measure. Creates atomic tasks with verification criteria and maintains persistent memory across sessions. Stack-agnostic. Use when starting projects, planning features, implementing with verification, tracking decisions across sessions. Triggers on "initialize project", "map codebase", "discover", "specify feature", "design", "tasks", "implement", "validate", "measure", "pause work", "resume work".
metadata:
  author: github.com/felipfr (extended with PDD integration)
  version: "2.0.0"
---

# Tech Lead's Club - Product-Driven Spec Development

Plan and implement products with precision. User problems first. Granular tasks. Clear dependencies. Measurable outcomes.

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐   ┌───────────────────┐   ┌──────────┐
│ DISCOVER │ → │ SPECIFY  │ → │  DESIGN  │ → │  TASKS  │ → │ IMPLEMENT+VALIDATE│ → │ MEASURE  │
└──────────┘   └──────────┘   └──────────┘   └─────────┘   └───────────────────┘   └──────────┘
 User           Technical       Architecture   Atomic         Code + Tests            Success
 problem +      requirements +  + decisions    tasks +        + verification          metrics +
 hypothesis +   acceptance      + trade-offs   prioritization evidence                feedback loop
 metrics        criteria                       by impact
```

## PDD Principle (Product Driven Development)

Before solving technically, ask:
- **Does this solve the USER's problem or the TECHNICAL problem?**
- Is there a simpler solution that delivers 80% of the value?
- How will the user perceive this change?
- If nobody uses this feature, was it time well spent?

PDD does not replace technical rigor — it DIRECTS technical rigor to where it matters.

The sections below detail each phase in the order they are executed. Each phase defines the artifacts (`.md` files) it produces; the consolidated file structure and the full workflow appear after the phases.

---

## Phase 0: DISCOVER (PDD)

**Trigger:** "discover", "which problem to solve", "why build", "validate hypothesis"

**Purpose:** Ensure we are building the right thing BEFORE specifying the solution.

**Output:** `.specs/features/[feature]/discovery.md` — a document with the feature's problem, hypothesis, and success metrics.

### Discovery Template

```markdown
# Discovery: [Feature Name]

## User Problem
- **Who suffers:** [specific persona, not "the user"]
- **What happens:** [current situation — concrete, observable pain]
- **Evidence:** [data, feedback, metrics, observations that prove the problem]
- **Frequency:** [daily / weekly / occasional]

## Hypothesis
We believe that [proposed solution] will [expected outcome] for [persona]
because [evidence-based reason].

## Success Metrics
| Metric | Baseline (current) | Target | How to measure | Deadline |
|---------|------------------|--------|------------|-------|
| [primary] | [current value] | [goal] | [tool/event] | [weeks] |
| [secondary] | [current value] | [goal] | [tool/event] | [weeks] |

## Success/Failure Criteria
- **Success:** [primary metric hits target within the deadline]
- **Pivot:** [if metric < X% of target, change approach]
- **Abandon:** [if after Y weeks with no improvement, do not proceed]

## MVP Scope (smallest experiment that validates the hypothesis)
- Includes: [minimal features to test the hypothesis]
- Does NOT include: [what can wait until after validation]

## Alternatives Considered
- [Option A]: discarded because [reason]
- [Option B]: discarded because [reason]
- Do nothing: [risk if we don't implement it]

## Product Priority
Impact: [High/Medium/Low] × Confidence: [High/Medium/Low] / Effort: [High/Medium/Low]
Score: [H×H/L = very high ... L×L/H = very low]
```

### Discover Rules
- NEVER skip this phase for features that touch the end user
- For purely technical tasks (refactoring, infra, CI/CD), Discover is optional
- If there is no evidence of the problem, find it before specifying
- If you can't define a success metric, the scope is too vague

---

## Phase 1-3: SPECIFY → DESIGN → TASKS

These three phases produce, respectively, the artifacts `spec.md` (technical requirements + acceptance criteria), `design.md` (architecture + decisions + trade-offs), and `tasks.md` (prioritized atomic tasks).

(Keeps the existing workflow — see references/)

### Impact-First Prioritization (in the TASKS phase)

When multiple tasks exist, prioritize by user impact:

```
Priority = (User Impact × Confidence) / Technical Effort
```

| Factor | High (3) | Medium (2) | Low (1) |
|-------|----------|-----------|-----------|
| **Impact** | Affects all users or a critical flow | Affects a relevant segment | Affects few or an edge case |
| **Confidence** | Data/feedback confirm | Indirect evidence | Intuition / guess |
| **Effort** | > 1 week | 2-5 days | < 2 days |

**Score > 4:** Do first
**Score 2-4:** Do this cycle
**Score < 2:** Backlog (reassess later)

**Anti-pattern:** Do NOT prioritize by what is technically interesting. Prioritize by what delivers the most user value with the highest confidence.

---

## Phase 4: IMPLEMENT + VALIDATE

Code implementation with tests and verification evidence for each task.

(Keeps the existing workflow — see references/)

---

## Phase 5: MEASURE (PDD)

**Trigger:** "measure", "post-deploy", "check metrics", "did the feature work?"

**Purpose:** Close the loop — verify whether the Discover hypothesis was confirmed.

### Post-Deploy Checklist

```markdown
## Post-Deploy: [Feature Name]
Deploy date: [YYYY-MM-DD]

### Rollout
- [ ] Feature flag configured (canary/% rollout)
- [ ] Rollback plan documented
- [ ] Error monitoring active (Sentry/logs)

### Analytics
- [ ] Analytics events implemented for success metrics
- [ ] Dashboard/query created to track metrics
- [ ] Baseline recorded before deploy

### Scheduled Review
- [ ] Review date: [YYYY-MM-DD] (per the Discovery deadline)
- [ ] Owner: [name/role]

### Result (fill in on the review date)
- Primary metric: [baseline] → [current] (target was [X])
- Secondary metric: [baseline] → [current]
- Verdict: [ ] Success [ ] Pivot [ ] Abandon
- Learnings: [what we discovered]
- Next steps: [iterate / scale / remove]
```

### Measure Rules
- NEVER declare a feature "delivered" without metrics configured
- If measuring is not possible (infra, refactoring), record at least: build time, error rate, deploy frequency
- Metrics review is as important as code review
- Features with no evidence of impact are candidates for removal

---

## Project Structure

The artifacts produced by the phases above are organized in the `.specs/` directory. Besides the per-feature files (discovery.md, spec.md, design.md, tasks.md — defined in the phases), there are project-level files, described inline below:

```
.specs/
├── project/
│   ├── PROJECT.md      # Vision & goals
│   ├── ROADMAP.md      # Features & milestones
│   ├── STATE.md        # Memory between sessions
│   └── DECISIONS.md    # ADR log (architectural decisions)
├── codebase/           # Brownfield analysis (existing projects)
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── STRUCTURE.md
│   ├── TESTING.md
│   └── INTEGRATIONS.md
└── features/           # Feature specifications
    └── [feature]/
        ├── discovery.md    # ← NEW: Problem, hypothesis, metrics
        ├── spec.md
        ├── design.md
        ├── tasks.md
        └── stories/
```

## Templates

### User Stories
Before implementing features, create user stories using the template:
- Template: [templates/user-story.md](templates/user-story.md)
- Location: `.specs/features/[feature]/stories/`
- Create BEFORE implementation to guide acceptance testing
- MUST include Product Context and Success Metrics (PDD)

### Decision Log (ADR)
Record important architectural decisions:
- Template: [templates/decisions.md](templates/decisions.md)
- Location: `.specs/project/DECISIONS.md`
- Every decision with trade-offs must be recorded

## Workflow

With the phases and file structure defined, the full flow is:

**New project:**
1. Initialize project → PROJECT.md
2. Create roadmap → ROADMAP.md
3. **Discover** → discovery.md (problem + hypothesis + metrics)
4. Specify features → spec.md
5. Design → design.md
6. Tasks → tasks.md
7. Implement + Validate
8. **Measure** → check post-deploy metrics

**Existing codebase:**
1. Map codebase → 6 brownfield docs
2. Initialize project → PROJECT.md + ROADMAP.md
3. **Discover** → discovery.md
4. Specify features → existing workflow
5. Implement + Validate + **Measure**

## Commands

Each command is triggered by a trigger pattern and detailed in a reference file:

**Project-level:**

| Trigger Pattern | Reference |
|----------------|-----------|
| Initialize project, setup project | [project-init.md](references/project-init.md) |
| Create roadmap, plan features | [roadmap.md](references/roadmap.md) |
| Map codebase, analyze existing code | [brownfield-mapping.md](references/brownfield-mapping.md) |
| Record decision, log blocker | [state-management.md](references/state-management.md) |
| Pause work, end session | [session-handoff.md](references/session-handoff.md) |
| Resume work, continue | [session-handoff.md](references/session-handoff.md) |

**Feature-level:**

| Trigger Pattern | Reference |
|----------------|-----------|
| Discover, validate problem, why build | (inline — Phase 0 above) |
| Specify feature, define requirements | [specify.md](references/specify.md) |
| Design feature, architecture | [design.md](references/design.md) |
| Break into tasks, create tasks | [tasks.md](references/tasks.md) |
| Implement task, build | [implement.md](references/implement.md) |
| Validate, verify, test | [validate.md](references/validate.md) |
| Measure, post-deploy, check metrics | (inline — Phase 5 above) |

**Tools:**

| Trigger Pattern | Reference |
|----------------|-----------|
| Code analysis, search patterns | [code-analysis.md](references/code-analysis.md) |

## Code Analysis

Use available tools with graceful degradation. See [code-analysis.md](references/code-analysis.md).

## Output Behavior

**Model guidance:** After completing lightweight tasks (validation, state updates, session handoff), naturally mention once that such tasks work well with faster/cheaper models. Track in STATE.md under `Preferences` to avoid repeating. For heavy tasks (brownfield mapping, complex design), briefly note the reasoning requirements before starting.

Be conversational, not robotic. Don't interrupt workflow—add as a natural closing note. Skip if user seems experienced or has already acknowledged the tip.

---

The following sections cover operational concerns (gotchas): context management and logging failed attempts.

## Context Loading Strategy

**Base load (~15k tokens):**
- PROJECT.md (if exists)
- ROADMAP.md (when planning/working on features)
- STATE.md (persistent memory)

**On-demand load:**
- discovery.md (when planning new feature — Phase 0)
- Codebase docs (when working in existing project)
- spec.md (when working on specific feature)
- design.md (when implementing from design)
- tasks.md (when executing tasks)

**Never load simultaneously:**
- Multiple feature specs
- Multiple architecture docs
- Archived documents

**Target:** <40k tokens total context
**Reserve:** 160k+ tokens for work, reasoning, outputs

### Context Budget — The 70% Rule

Above 70% of the context window, the model degrades silently: it ignores tools,
hallucinates more, stops mid-task, loses adherence to rules. There is no explicit
error — just progressive degradation.

**Saturation signs (self-diagnosis):**
- Responses become generic or repetitive
- The agent "forgets" to run tests or verifications
- Tasks stop abruptly with no explanation
- Documented rules are ignored
- The agent starts cutting corners in defined processes

**Mandatory actions when saturation is detected:**

1. **STOP** the current task — do not continue in a degraded context
2. **Save state** to STATE.md:
   ```
   ## Context Reset — [YYYY-MM-DD HH:MM]
   - Task in progress: [description]
   - Last checkpoint: [what was completed]
   - Next step: [what's left]
   - Modified files: [list]
   - Tests passing: [yes/no/partial]
   ```
3. **Compact** or start a new session
4. **Resume** loading only: STATE.md + the specific task

**Prevention (before saturating):**
- Before complex tasks: unload unnecessary context
- One feature per session — don't mix features in the same context
- After completing a phase (Specify, Design, Tasks), save to a file and clear
- Sub-agents for research, code-review, and debugging (isolated context)
- If a task needs more than 3 specs, split the task

**Consumption estimate:**

| Item | Tokens (~) | Notes |
|------|-----------|-------|
| CLAUDE.md + SKILLS.md | ~5k | Fixed base |
| 1 skill activated | ~2-4k | On demand |
| 1 typical spec.md | ~1-3k | On demand |
| 1 full agent | ~3-5k | Isolated context (doesn't count) |
| MCP call + response | ~1-2k | Each call |
| Code file read | ~0.5-2k | Per file |
| Message history | accumulates | Main culprit |

**Practical budget (200k window):**
- 🟢 < 80k (~40%): comfortable zone, model operates well
- 🟡 80-120k (~40-60%): caution, avoid loading more context
- 🔴 120-140k (~60-70%): save state, prepare for compaction
- ⛔ > 140k (~70%+): STOP, compact NOW, degradation active

### Compression Mode (🟡 and 🔴 zones)

When context enters the yellow or red zone, automatically adopt:
- Concise responses with no preambles or recaps
- Show only diffs, never re-list entire files
- Don't repeat context already established in the conversation
- Omit "why" explanations when the user already has the context
- Prioritize action over inline documentation

### Story Loading per Phase

User stories (see Templates above) are ~725 tokens. Each phase needs only specific sections:

| Phase | Required story sections | Ignore |
|------|----------------------------|--------|
| **Discover/Specify** | Full story | — |
| **Design** | Acceptance criteria + edge cases + dependencies | Product context, priority, metrics |
| **Implement** | Acceptance criteria + happy path + edge cases | Product context, priority, metrics |
| **Measure** | Success metrics + completion criteria | Acceptance criteria, edge cases, happy path |

This reduces consumption from ~725 → ~350 tokens per story in the implementation phases.

## Attempts Log (when implementation fails)

When a task fails after a genuine attempt, record it in STATE.md:

```markdown
## Attempts — STORY-{N}: [title]

### Attempt 1 — [YYYY-MM-DD HH:MM]
- Approach: [what was tried]
- Result: [what happened]
- Root cause: [why it failed]
- Files touched: [list]
- Rollback: [git stash / git checkout -- files]

### Attempt 2 — [YYYY-MM-DD HH:MM]
- Approach: [different from the previous one]
- ...

### Decision
- [ ] Try a different approach: [description]
- [ ] Escalate complexity to architect review
- [ ] Simplify scope (remove edge cases)
```

### Attempts Rules
- After 3 failed attempts on the same task: STOP and review the spec/design
- Each attempt MUST use a different approach (repeating = waste)
- ALWAYS do a clean rollback before a new attempt (don't stack fixes)
