---
description: Phase 4 — Executes the implementation and validation of the feature following TDD and the tasks.md plan. Processes tasks in dependency order, writes tests before code, and validates upon completion. Triggers: "implement", "implement feature", "execute tasks", "develop", "code it", "/spec-implement [feature]".
---

## Required context
Read before executing:
- `.specs/features/[feature]/tasks.md` — list of tasks to execute
- `.specs/features/[feature]/spec.md` — acceptance criteria (reference during implementation)
- `.specs/features/[feature]/design.md` — contracts, schema, architecture
- `.specs/memory/constitution.md` — project standards, conventions, and principles

## Phase: Phase 4 — Implement + Validate (PDD)

## Expected output
- Code implemented according to design.md
- Tasks marked as `[x]` in `.specs/features/[feature]/tasks.md`
- `.specs/features/[feature]/validation.md` upon completion

## Process

The argument passed after `/spec-implement` is the feature. If empty, ask which feature to implement. If there is no `tasks.md`, run `/spec-tasks` first.

### Before starting
1. Read `tasks.md` and identify the first incomplete task
2. Check whether there are unresolved external dependencies (pending migrations, services, approvals)
3. If there are tasks with "NEEDS CLARIFICATION", run `/spec-clarify` before proceeding

### Per task
Execute each task strictly in dependency order:

**For test tasks (prefix T-0X with "write test"):**
1. Write the test as specified
2. Run: confirm RED — the test must fail for the correct reason
3. Record: mark `[ ]` with a note `(RED confirmed)`

**For implementation tasks (production code):**
1. Write the minimal code to pass the test
2. Run: confirm GREEN — the test must pass
3. Refactor if needed (REFACTOR) while keeping GREEN
4. Mark `[x]` on the task with evidence: `(bun test — 0 failures)`

**For tasks with no associated test (setup, config, migration):**
1. Execute the task
2. Verify against the criterion listed in the task
3. Mark `[x]` with evidence of the criterion met

### Upon completing all tasks
1. Run the full suite: `bun test` → must have 0 failures
2. Run build: `bun run build` → must have exit 0
3. Run lint: `bun run lint` → must have 0 errors
4. Create `.specs/features/[feature]/validation.md`:

```markdown
# Validation: [Feature Name]
**Date:** [YYYY-MM-DD] | **Status:** VALIDATED

## Verification Evidence
- Tests: `bun test` — [N] passed, 0 failures, 0 skipped
- Build: `bun run build` — exit 0
- Lint: `bun run lint` — 0 errors

## Verified Acceptance Criteria
| AC | Status | How verified |
|---|---|---|
| AC-01 | ✅ PASS | [verification method] |
| AC-02 | ✅ PASS | [verification method] |

## Decisions Made During Implementation
- [decision 1 and rationale]
- [decision 2 and rationale]

## Pending Items (if any)
- [pending item and reason]
```

5. Suggest `/spec-measure` to record post-deploy metrics.

## Rules
- **NEVER declare completion without fresh verification evidence**
- TDD is mandatory for all business logic — do not skip the RED-GREEN-REFACTOR cycle
- If a test cannot be written for a piece of functionality, question whether the design is clear enough
- Commits only with explicit user authorization
- If you hit a blocker during implementation, stop and describe the blocker — do not improvise a solution that deviates from the design
