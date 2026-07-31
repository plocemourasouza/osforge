---
description: Phase 3 — Generates the atomic task plan with dependency order and per-task verification criteria. Use after /spec-design. Triggers: "tasks", "generate tasks", "implementation plan", "break down into tasks", "/spec-tasks [feature]".
---

## Required context
Read before executing:
- `.specs/features/[feature]/spec.md` — acceptance criteria (each AC becomes at least 1 task)
- `.specs/features/[feature]/design.md` — contracts, schema, architecture
- `.specs/memory/constitution.md` — quality standards (test coverage, etc.)

## Phase: Phase 3 — Tasks

## Expected output
`.specs/features/[feature-name]/tasks.md`

## Process

1. **Read spec.md and design.md** in full before generating any task.

2. **Prioritize by user impact**:
   ```
   Score = (Impact × Confidence) / Effort
   H=3, M=2, L=1
   ```
   - Score > 4 → Do first
   - Score 2-4 → Do this cycle
   - Score < 2 → Backlog

3. **Structure of each task**: Atomic, 2-5 minutes. Specify exact paths. No ambiguity about what "done" means.

3a. **Slice vertically (tracer bullets)**: a group of tasks must cut through ALL integration
   layers end-to-end — schema, action, UI, test — so something is demoable when it closes. Never
   slice horizontally ("all migrations, then all actions, then all UI"): a horizontal layer is
   only verifiable against imagined callers, which is how integration bugs survive to the end.

3b. **Declare autonomy per task — HITL or AFK**:
   - **AFK** — fully specified, an agent can execute and verify it with no human in the loop.
   - **HITL** — needs a human decision or review mid-flight (design approval, ambiguous contract,
     irreversible migration).
   Parallel wave dispatch runs AFK tasks unattended; a wave containing a HITL task stops at it.
   Mislabeling HITL as AFK is how an agent makes an architectural decision alone at 2am — when in
   doubt, HITL. Prefer redesigning a task to make it genuinely AFK over relabeling it.

3c. **Declare `wave` and `depends_on`** on every task — this is what `osforge-db` and the parallel
   dispatcher consume. Same wave = provably independent (no shared files, no dependency edge).

4. **Create `tasks.md`**:

```markdown
# Tasks: [Feature Name]
**Feature:** [feature-name] | **Date:** [YYYY-MM-DD] | **Estimate:** [total]
**References:** spec.md | design.md

## Summary
- Total tasks: [N]
- Total estimate: [X hours / Y days]
- External dependencies: [migrations, services, approvals required]

## Tasks

### Setup & Foundation
- [ ] **T-01**: Create migration `[name]` for [table/field]
  - File: `prisma/migrations/[timestamp]_[name]/migration.sql`
  - Criterion: `bun prisma migrate dev` runs without error
  - Estimate: 15min
  - wave: 1 · depends_on: [] · mode: AFK

- [ ] **T-02**: Generate Prisma Client after migration
  - Command: `bun prisma generate`
  - Criterion: no type errors in `src/generated/prisma`
  - Estimate: 5min

### Business Logic (TDD — write tests first)
- [ ] **T-03**: Write test for [Server Action]
  - File: `src/actions/__tests__/[feature].actions.test.ts`
  - Criterion: test fails (RED) — verify with `bun test`
  - Estimate: 20min

- [ ] **T-04**: Implement [Server Action]
  - File: `src/actions/[feature].actions.ts`
  - Contract: see design.md section "Server Actions"
  - Criterion: test T-03 passes (GREEN) — verify with `bun test`
  - Estimate: 30min

- [ ] **T-05**: Refactor [Server Action] if needed
  - Criterion: all tests pass + code follows the constitution standards
  - Estimate: 15min

### Interface (components)
- [ ] **T-06**: Create component `[Name]` (Server Component)
  - File: `src/components/[feature]/[Name].tsx`
  - Props: see design.md section "React Components"
  - Criterion: renders without errors in development
  - Estimate: 45min

### Integration
- [ ] **T-07**: Connect component with Server Action
  - Criterion: AC-01 of spec.md can be verified manually
  - Estimate: 20min

### Final Validation
- [ ] **T-08**: Run the full test suite
  - Command: `bun test`
  - Criterion: 0 failures, 0 skipped
  - Estimate: 5min

- [ ] **T-09**: Production build
  - Command: `bun run build`
  - Criterion: exit 0, no TypeScript errors
  - Estimate: 5min

## AC → Tasks Mapping
| Acceptance Criteria | Validating tasks |
|---|---|
| AC-01 | T-03, T-04, T-07 |
| AC-02 | T-05, T-06 |
| AC-ERROR-01 | T-03 (error case) |
```

5. **Confirm**: Present the task list. For complex features, ask whether the user wants to break down any task further before starting.

## Rules
- Every task must have an executable verification criterion (command + expected output)
- Every task declares `wave`, `depends_on` and `mode: AFK|HITL` — the dispatcher consumes these
- Slices are vertical (tracer bullets through all layers), never horizontal by layer
- Test tasks ALWAYS before implementation tasks (TDD)
- Never group "implement X and Y" into one task — one responsibility per task
- The AC → Tasks mapping ensures no acceptance criterion is left without coverage
