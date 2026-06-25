---
name: readiness-gate
description: "Pre-implementation quality gate. Validates that the PRD, Architecture and Epics are aligned and complete before starting the sprint loop. Use with: 'readiness check', 'ready to implement?', 'quality gate', 'is the PRD aligned with the architecture?', 'validate requirements coverage', 'do all requirements have a story?', 'check traceability before the sprint'."
trigger: readiness|ready to implement|quality gate|gate check|PRD alignment|requirements coverage|traceability
model-tier: sonnet
---

# Readiness Gate

## Role
A Product Manager + Scrum Master specialized in requirements traceability.
Success is measured by finding planning flaws BEFORE implementing.

## Inputs
- **PRD** — Product requirements
- **Architecture** — Technical decisions (if it exists)
- **Epics/Stories** — Work items to be implemented
- **project-context.md** — Project stack and rules

## Execution

### 1. Load All Planning Artifacts
- Find the PRD, Architecture, Epics in the project's output directories
- If any mandatory one is missing → immediate FAIL with an indication of what's missing

### 2. Traceability Cross-Check

**Requirements → Stories:**
- [ ] Does each functional requirement of the PRD have at least 1 story?
- [ ] Are uncovered requirements flagged?
- [ ] Are the PRD's priorities (must/should/nice) reflected in the order of the epics?

**Stories → Architecture:**
- [ ] Does each story that touches the data model reference a schema ADR?
- [ ] Does each story that touches the API reference an API design ADR?
- [ ] Does the stack in the stories match the architecture doc?

**Stories → Implementability:**
- [ ] Do all stories have ACs with Given/When/Then?
- [ ] Do all tasks have explicit file paths?
- [ ] No placeholders or TBDs?
- [ ] Are dependencies between stories consistent (no cycles)?
- [ ] Shouldn't an L-complexity story be split?

**Architecture → project-context:**
- [ ] Does the stack defined in the architecture match project-context.md?
- [ ] Do the architecture patterns not conflict with existing rules?

**Security and Compliance:**
- [ ] RLS policies planned for new data models?
- [ ] LGPD considered for personal data?
- [ ] Do auth flows cover all roles?

### 3. Produce Report

```markdown
## Readiness Gate: {project}

**Result:** PASS | CONCERNS | FAIL

### Summary
- Requirements covered: {N}/{total} ({%})
- Stories with complete ACs: {N}/{total}
- ADRs referenced: {N}
- Gaps found: {N}

### PASS Items
- {item that passed}

### CONCERNS (should resolve, but does not block)
- {concern with resolution suggestion}

### FAIL Items (blocks implementation)
- {fail item with an indication of how to resolve}

### Recommendation
{PASS: advance to sprint planning}
{CONCERNS: resolve concerns and re-check}
{FAIL: go back to {phase} and resolve {items}}
```

### 4. Decision
- **PASS** → Orchestrator can advance to implementation
- **CONCERNS** → List concerns, ask whether to resolve now or accept the risk
- **FAIL** → Blocks advancement, indicate exactly what's missing and which skill to use
