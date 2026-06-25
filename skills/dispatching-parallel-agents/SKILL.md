---
name: dispatching-parallel-agents
description: "Orchestrates parallel tasks across independent subagents. Use when: 2+ tasks with no shared state, refactoring across multiple unrelated files, decomposition reveals parallelizable work, or tasks with partial dependencies. Keywords: parallel, wave, dispatch, parallel agents, multiple tasks, independent, subagents."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: osforge
  version: '1.2'
  source: Superpowers (obra)
  inspired_by: gsd-build/get-shit-done (wave execution pattern)
---

# Dispatching Parallel Agents

## When to Parallelize
Use parallel agents when tasks are:
- **Independent** — no shared state between them
- **Non-sequential** — output of one doesn't feed into another
- **Bounded** — each has clear completion criteria

## Decision Matrix

| Scenario | Strategy | Why |
|----------|----------|-----|
| 3 independent API endpoints | ✅ Parallel | No shared state |
| Frontend + backend for same feature | ❌ Sequential | Backend API feeds frontend |
| Tests for 5 different modules | ✅ Parallel | Independent test suites |
| Migration + seed data | ❌ Sequential | Seed depends on schema |
| Code review + docs update | ✅ Parallel | Independent outputs |
| 10 file refactoring (same pattern) | ✅ Parallel | Each file is independent |

## Task Specification Format
Each parallel task MUST be self-contained with:

```markdown
## Task: [Name]
**Goal:** One sentence describing the deliverable
**Files:** List of files to create/modify
**Context:** Any shared knowledge needed (types, patterns, conventions)
**Acceptance:** How to verify completion
**Constraints:** What NOT to touch
```

## Execution Pattern (Claude Code)
```markdown
### Plan: Implement User Dashboard

I'll dispatch 3 parallel tasks:

**Task 1: Stats API**
- Create `app/api/dashboard/stats/route.ts`
- Query: project count, task completion rate, recent activity
- Test: `__tests__/api/dashboard-stats.test.ts`

**Task 2: Activity Feed Component**
- Create `components/dashboard/activity-feed.tsx`
- Server Component fetching from activity table
- Test: `__tests__/components/activity-feed.test.tsx`

**Task 3: Quick Actions Widget**
- Create `components/dashboard/quick-actions.tsx`
- Client Component with action buttons
- Test: `__tests__/components/quick-actions.test.tsx`

These are independent — no shared state. Dispatching in parallel.
```

## Merge Strategy
After all parallel tasks complete:
1. **Integration test** — verify tasks work together
2. **Import resolution** — connect components/APIs at the page level
3. **Type check** — `bun tsc --noEmit` to catch interface mismatches
4. **Visual verification** — check the composed result

## Anti-Patterns
- ❌ Parallelizing tasks that share a database migration
- ❌ Dispatching without clear file boundaries (merge conflicts)
- ❌ Parallel tasks with implicit ordering (A creates type, B uses it)
- ❌ More than 5 parallel tasks (coordination overhead > benefit)

## Context Embedding
Each task gets a minimal context package:
```markdown
**Shared Types:** (paste relevant interfaces)
**Naming Convention:** (paste from coding-guidelines)
**Test Pattern:** (paste TDD example from tdd-workflow)
```
This makes each task self-contained — the agent doesn't need to search for conventions.

## Integration with Planner
The `planner` agent identifies parallelizable tasks during decomposition:
- Simple tasks → sequential (no overhead)
- Moderate tasks → evaluate for parallel if >2 independent units
- Complex tasks → likely parallel after spec critique by `validator`

---

## Wave Execution (dependency-aware parallelism)

Use wave execution when tasks have **partial dependencies** — some are independent,
others depend on earlier results. Inspired by the GSD phase execution model.

### How waves work

Group tasks into waves based on their dependency graph:
- **Same wave** → run in parallel (no dependency between them)
- **Next wave** → waits for ALL tasks in the previous wave to complete
- **File conflicts** → put conflicting tasks in the same sequential plan or the same wave with non-overlapping files

```
WAVE 1 (parallel)           WAVE 2 (parallel)        WAVE 3
┌─────────────┐ ┌──────────┐  ┌──────────┐ ┌───────┐  ┌──────────┐
│ User schema │ │ Product  │  │ Orders   │ │ Cart  │  │ Checkout │
│ + migration │ │ schema   │  │ API      │ │ API   │  │ UI       │
└─────────────┘ └──────────┘  └──────────┘ └───────┘  └──────────┘
       │               │           ↑            ↑           ↑
       └───────────────┴───────────┴────────────┘           │
          Wave 2 tasks depend on Wave 1 schemas      Depends on both Wave 2 tasks
```

### Wave planning format

```markdown
## Wave Execution Plan

### Wave 1 — Foundation (parallel)
**Task 1A: User Model**
- Files: `prisma/schema.prisma` (User model only)
- Goal: User + auth fields
- No dependencies

**Task 1B: Product Model**
- Files: `prisma/schema.prisma` (Product model only)
- Goal: Product + inventory fields
- No dependencies
⚠️ Note: Tasks 1A and 1B modify schema.prisma — coordinate to avoid conflicts
   by having each agent append their model block without touching the other's section.

### Wave 2 — APIs (parallel, after Wave 1)
**Task 2A: Orders API**
- Files: `app/api/orders/route.ts`
- Depends on: Wave 1 (User + Product models exist)

**Task 2B: Cart API**
- Files: `app/api/cart/route.ts`
- Depends on: Wave 1 (User + Product models exist)

### Wave 3 — UI (after Wave 2)
**Task 3A: Checkout Page**
- Files: `app/checkout/page.tsx`
- Depends on: Wave 2 (Orders API + Cart API complete)
```

---

### YAML-driven wave assembly (machine-readable plans)

When the task plan contains YAML blocks with the fields `id`, `depends_on`, `wave`, and `parallel_ok`, the waves MUST be assembled from that data — not inferred from prose.

**Reading algorithm:**

1. Collect all YAML blocks from `tasks.md`.
2. Group by `wave` (integer number).
3. Within each wave, separate tasks with `parallel_ok: true` (parallelizable) from those with `parallel_ok: false` (sequential within the wave).
4. Verify that each task's `depends_on` points to tasks in earlier waves (consistency).
5. Dispatch each complete wave before starting the next.

**Example — reading YAML for a Wave Execution Plan:**

```yaml
# tasks.md (excerto de blocos YAML)
- id: T1
  depends_on: []
  wave: 1
  parallel_ok: true

- id: T2
  depends_on: [T1]
  wave: 2
  parallel_ok: true

- id: T3
  depends_on: [T1]
  wave: 2
  parallel_ok: true

- id: T4
  depends_on: [T2, T3]
  wave: 3
  parallel_ok: true
```

Dispatch result:

```
Wave 1 → dispatch T1 (alone)
Wave 2 → dispatch T2 + T3 in parallel (both parallel_ok: true)
Wave 3 → dispatch T4 after T2 and T3 complete
```

**Fallback (plans without YAML):** if no YAML block is found, infer waves from the prose and the `Depends on:` fields of each task (previous behavior). Document that the plan is not machine-readable and suggest adding the YAML.

### When to use waves vs flat parallel

| Scenario | Use |
|---|---|
| All tasks truly independent | Flat parallel (original pattern) |
| Some tasks depend on others | Wave execution |
| Linear pipeline (A→B→C→D) | Sequential — no parallelism benefit |
| Mixed: some parallel, some sequential | Wave execution |

### Fresh context per wave

Each wave's agents start with a clean 200K context window. Pass only what they need:
- Relevant schema excerpts (not the full Prisma file)
- Interfaces/types the task depends on
- Conventions from project-context.md

This keeps each agent fast and focused — no accumulated context degradation.


---

## Gotchas

- **Tasks that modify the same file in parallel**: if two tasks need to edit `prisma/schema.prisma` or the same component, do NOT parallelize them — make them sequential or coordinate via non-overlapping sections. A merge conflict is guaranteed.
- **Not providing shared types/interfaces**: each parallel agent receives minimal context. If Tasks B and C depend on a type created by Task A, pass that type explicitly in the prompts for B and C — they do not share context with each other.
- **More than 5 parallel tasks**: coordination overhead exceeds the benefit above 5 simultaneous tasks. If you need more, group them into waves of at most 5.
- **Implicit dependency**: a "seed data task" looks independent but depends on completed migrations. Map dependencies before parallelizing — each wave must document dependencies explicitly.
- **Not verifying integration after merge**: parallel agents can produce interfaces incompatible with one another. Always run `bun tsc --noEmit` and integration tests after merging the parallel tasks.
- **Wave 1 with schema**: if Wave 1 has tasks in `prisma/schema.prisma`, each agent must work only on its own block of models without touching the others' blocks — or keep the schema always sequential.
