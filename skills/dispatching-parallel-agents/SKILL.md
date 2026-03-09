---
name: dispatching-parallel-agents
description: Orchestrate parallel subagent tasks for independent workloads. Trigger when facing 2+ independent tasks without shared state, large refactoring across multiple files, or when task decomposition reveals parallelizable work units.
metadata:
  author: osforge
  version: '1.0'
  source: Superpowers (obra)
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
