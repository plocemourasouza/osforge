# Story Executor

**Trigger:** executar story, implementar story, dev story

---

## Purpose

Coordena implementação de uma story seguindo suas tasks e ACs. Invoca skills corretos na ordem das tasks. Verifica ACs ao completar.

---

## Workflow

```
LOAD story → EXECUTE tasks in order → VERIFY ACs → REPORT
```

---

## Process

### 1. Load Story
```
1. Read story file
2. Verify dependencies are complete
3. Mark story as in_progress
4. Understand acceptance criteria
```

### 2. Execute Tasks
For each task in order:
```
1. Read current state of target files
2. Identify which skill applies:
   - Schema change → prisma skill
   - API route → nextjs-react skill
   - Auth logic → supabase-auth skill
   - UI component → frontend-ui skill
   - Test → testing skill
3. Implement following TDD workflow
4. Verify task completion
5. Commit (if approved)
```

### 3. TDD Per Task
```
RED:   Write failing test for task behavior
GREEN: Implement minimum code to pass
REFACTOR: Clean up while green
```

### 4. Verify ACs
```
For each acceptance criterion:
1. Create test scenario
2. Execute test
3. Verify expected result
4. Document evidence
```

### 5. Report
```
- Tasks completed: X/Y
- ACs verified: all | partial
- Tests added: N
- Files modified: [list]
- Ready for review: yes/no
```

---

## Skill Routing

| Task Type | Skill to Invoke |
|-----------|-----------------|
| Database schema | `prisma.md` |
| API endpoint | `nextjs-react.md` |
| Authentication | `supabase-auth.md` |
| UI component | `frontend-ui.md` |
| Payment | `stripe.md` |
| Test | `e2e-playwright.md` or `patterns.md` |
| i18n | `i18n.md` |

---

## Two-Stage Review Per Task

### Stage 1: Spec Compliance
```
- Does implementation match AC?
- Are edge cases handled?
- Is behavior correct?
```

### Stage 2: Code Quality
```
- TypeScript strict compliant?
- Tests adequate?
- Performance acceptable?
- Security patterns followed?
```

---

## Status Updates

```yaml
# Update story status
---
status: in_progress
started: 2024-01-15T10:30:00Z
tasks_completed:
  - task-1
  - task-2
current_task: task-3
blockers: []
---
```

---

## Blocker Handling

If blocked:
```
1. Document blocker in story file
2. Mark story as blocked
3. Identify what's needed to unblock
4. Escalate if external dependency
```

---

## Completion Checklist

Before marking story as done:
```
- [ ] All tasks completed
- [ ] All ACs verified with evidence
- [ ] Tests pass
- [ ] TypeScript compiles
- [ ] Lint passes
- [ ] No console.log debug statements
- [ ] Code reviewed (self or peer)
```

---

## Output

```markdown
## Story Execution Report

**Story:** [story-id]
**Started:** [timestamp]
**Completed:** [timestamp]

### Tasks
| Task | Status | Notes |
|------|--------|-------|
| Task 1 | Done | [any notes] |
| Task 2 | Done | |
| Task 3 | Done | |

### Acceptance Criteria
| AC | Status | Evidence |
|----|--------|----------|
| AC1 | Verified | Test: `test-name` passes |
| AC2 | Verified | Manual: [description] |

### Files Modified
- `path/to/file1.ts`
- `path/to/file2.ts`

### Tests Added
- `tests/feature.test.ts`

### Ready for Review
Yes — all ACs verified, tests pass
```
