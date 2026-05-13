# Readiness Gate

**Trigger:** "readiness check", "pronto para implementar?", "quality gate", ou automaticamente antes do sprint loop em triage COMPLEX.

---

## Purpose

Quality gate pré-implementação. Valida alinhamento e completude entre PRD ↔ Architecture ↔ Épicos antes de iniciar coding.

---

## Checklist

### Requirements Coverage
- [ ] All functional requirements have matching stories
- [ ] All non-functional requirements have acceptance criteria
- [ ] Edge cases documented
- [ ] Error states defined

### Architecture Alignment
- [ ] ADRs created for major decisions
- [ ] Schema changes documented
- [ ] API contracts defined
- [ ] Integration points identified

### Stories Quality
- [ ] All stories have testable ACs
- [ ] Dependencies mapped
- [ ] No circular dependencies
- [ ] Reasonable scope (1-3 days each)

### Risks Mitigated
- [ ] High-risk items identified
- [ ] Mitigation strategies defined
- [ ] Fallback plans documented
- [ ] Blockers resolved

### Technical Readiness
- [ ] Development environment ready
- [ ] Access to required services
- [ ] Test data available
- [ ] CI/CD pipeline configured

---

## Decision Output

### GO
```markdown
## Readiness Gate: PASS ✅

All checks passed. Ready to begin implementation.

**Summary:**
- 12 stories, 45 tasks
- 3 ADRs created
- 2 schema migrations planned
- Est. 2 sprints

**First Sprint Focus:**
- Story 1: Auth foundation
- Story 2: User CRUD
- Story 3: Dashboard shell
```

### NO-GO
```markdown
## Readiness Gate: FAIL ❌

Cannot proceed. Issues must be resolved.

**Blocking Issues:**

1. **Missing API contract for payment integration**
   - Impact: Stories 7-9 cannot be estimated
   - Action: Schedule meeting with payment team

2. **Unclear requirement for multi-tenant isolation**
   - Impact: Schema design incomplete
   - Action: Clarify with product owner

**Recommendation:**
Pause for 1-2 days to resolve blockers before sprint starts.
```

---

## Integration Points

### Before Sprint
```
PRD complete?
  └── YES → Architecture complete?
        └── YES → Stories complete?
              └── YES → Readiness Gate
                    └── PASS → Begin Sprint
                    └── FAIL → Resolve Issues
```

### With Orchestrator
```
Orchestrator assigns: COMPLEX triage
  └── PRD Builder
  └── Architecture Builder
  └── Epic Decomposer
  └── **Readiness Gate** ← Here
  └── Story Executor (only if PASS)
```

---

## Partial Approval

For large features, can approve subset:
```markdown
## Readiness Gate: PARTIAL ⚠️

**Approved for Sprint 1:**
- Stories 1-4 (Auth & User Management)

**Blocked (defer to Sprint 2):**
- Stories 5-8 (Payment integration)
- Reason: Waiting on API contract

**Action Items:**
- [ ] Payment team contract by end of Sprint 1
- [ ] Reschedule Sprint 2 planning after contract
```
