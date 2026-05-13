# Plan Writing

**Trigger:** task planning, plan breakdown, structured planning, implementation plan

---

## Purpose

Structured task planning framework. Small focused tasks, clear verification criteria, dependency identification, and logical ordering.

---

## Plan Structure

```markdown
# Implementation Plan: [Feature/Task Name]

## Goal
[One sentence: what does "done" look like?]

## Prerequisites
- [ ] [Prereq 1]
- [ ] [Prereq 2]

## Tasks

### Phase 1: [Phase Name]

#### Task 1.1: [Task Name]
**Files:** `path/to/file.ts`
**Verify:** [How to confirm this is done]
**Depends on:** None

#### Task 1.2: [Task Name]
**Files:** `path/to/file.ts`
**Verify:** [How to confirm this is done]
**Depends on:** Task 1.1

### Phase 2: [Phase Name]
[Continue with tasks...]

## Verification
[Final verification steps to confirm everything works]

## Rollback
[How to undo if something goes wrong]
```

---

## Task Sizing Rules

### Too Big
```
"Implement authentication system"
"Build the dashboard"
"Add payment processing"
```

### Right Size
```
"Create User model in Prisma schema"
"Add POST /api/auth/login endpoint"
"Create LoginForm component with email/password fields"
"Add Stripe webhook handler for subscription events"
```

### Guideline
If a task touches more than 2-3 files or takes more than 30 minutes, break it down further.

---

## Verification Criteria

Every task needs a verification step:

| Task Type | Verification |
|-----------|--------------|
| Schema change | `bun prisma db push` succeeds |
| API endpoint | `curl` or test returns expected response |
| Component | Renders without errors, matches design |
| Test | `bun test [file]` passes |
| Type change | `bun tsc --noEmit` passes |

---

## Dependency Types

### Hard Dependency
Task B cannot start until Task A is complete.
```
Task A: Create User model
Task B: Create users API route (depends on A)
```

### Soft Dependency
Task B is easier if Task A is done, but not required.
```
Task A: Set up test utilities
Task B: Write user tests (easier with A, but can mock)
```

### Parallel
Tasks can be done in any order.
```
Task A: Create login page
Task B: Create signup page
(Both independent)
```

---

## Phase Organization

Group tasks into logical phases:

```
Phase 1: Foundation
- Database schema
- Core types
- Base utilities

Phase 2: Backend
- API endpoints
- Business logic
- Validation

Phase 3: Frontend
- Components
- Pages
- State management

Phase 4: Integration
- Wire up frontend to backend
- Error handling
- Loading states

Phase 5: Polish
- Edge cases
- Performance
- Accessibility
```

---

## Common Patterns

### Feature Implementation
```
1. Schema/types
2. API endpoints
3. Server components/actions
4. Client components
5. Tests
6. Documentation
```

### Bug Fix
```
1. Reproduce (write failing test)
2. Identify root cause
3. Fix
4. Verify test passes
5. Check for regressions
```

### Refactor
```
1. Characterization tests (capture current behavior)
2. Incremental changes
3. Verify tests still pass
4. Clean up
```

---

## Anti-Patterns

### Avoid
```
- Vague tasks: "Improve performance"
- No verification: "Update the code"
- Hidden complexity: "Add feature X" (actually 10 subtasks)
- Missing dependencies: Tasks in wrong order
```

### Instead
```
- Specific: "Add database index on users.email"
- Verifiable: "Query time < 100ms (check with EXPLAIN ANALYZE)"
- Broken down: Each task is atomic
- Ordered: Dependencies explicitly listed
```
