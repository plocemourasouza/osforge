# Dispatching Parallel Agents

**Trigger:** 2+ independent tasks without shared state, large multi-file refactoring, parallelizable work units.

---

## Decision Matrix

| Condition | Action |
|-----------|--------|
| Tasks share state/files | Sequence |
| Tasks have dependencies | Sequence with waves |
| Tasks are independent | Parallelize |
| >5 parallel tasks | Split into waves |

---

## Task Specification Format

Each parallel task MUST be self-contained:

```yaml
task:
  id: "task-1"
  goal: "Implement user authentication API"
  files:
    - src/app/api/auth/route.ts
    - src/lib/auth.ts
  context: |
    Stack: Next.js 15, Supabase Auth
    Pattern: Server Actions for mutations
  acceptance:
    - POST /api/auth/login returns JWT
    - POST /api/auth/logout clears session
    - Tests pass
```

---

## Execution Pattern

```typescript
// Dispatch parallel tasks
const tasks = [
  { agent: 'implementer', task: authTask, model: 'sonnet' },
  { agent: 'implementer', task: dashboardTask, model: 'sonnet' },
  { agent: 'docWriter', task: readmeTask, model: 'haiku' },
]

const results = await Promise.all(
  tasks.map(t => dispatchAgent(t))
)

// Merge results
await mergeStrategy(results)
```

---

## Merge Strategy

```
1. Integration test → Verify all components work together
2. Import resolution → Fix any conflicting imports
3. Type check → Ensure types are consistent
4. Full test suite → Confirm no regressions
```

---

## Wave Execution

For tasks with partial dependencies:

```
Wave 1 (parallel):
  - Database schema migration
  - API types generation

Wave 2 (parallel, after Wave 1):
  - API endpoints implementation
  - Frontend components

Wave 3 (parallel, after Wave 2):
  - Integration tests
  - Documentation
```

---

## Git Worktrees for Parallel Work

```bash
# Create isolated worktrees
git worktree add ../project-auth feature/auth
git worktree add ../project-dashboard feature/dashboard

# Each agent works in isolation
# After completion:
git worktree remove ../project-auth
git worktree remove ../project-dashboard
```

---

## Anti-Patterns

1. **Shared migrations** — Never parallelize DB migrations
2. **Implicit ordering** — Always explicit dependencies
3. **>5 parallel tasks** — Diminishing returns, harder to merge
4. **Shared mutable state** — Race conditions guaranteed
5. **No acceptance criteria** — Can't verify completion
