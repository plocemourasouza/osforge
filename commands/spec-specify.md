---
description: Phase 1 — Creates the detailed technical specification of a feature: functional requirements, non-functional requirements, acceptance criteria, and use cases. Use after /spec-discover or when the problem is already validated. Triggers: "specify", "specify feature", "write spec", "technical requirements", "/spec-specify [feature]".
---

## Required context
Read before executing:
- `.specs/features/[feature]/discovery.md` — validated problem and hypothesis
- `.specs/memory/constitution.md` — project principles and standards
- `.specs/project/STATE.md` (if it exists) — context from previous sessions

## Phase: Phase 1 — Specify

## Expected output
`.specs/features/[feature-name]/spec.md`

## Process

1. **Identify feature**: If the argument after `/spec-specify` names the feature, use it. Otherwise, check which feature has the most recent `discovery.md` or ask.

2. **Check constitution**: If `.specs/memory/constitution.md` exists, verify that the feature respects the defined principles. If it violates any, flag it before continuing.

3. **Ask specification questions** (maximum 4, only if genuinely ambiguous):
   - What are the main user flows?
   - Are there external integrations involved?
   - What are the acceptable performance constraints?
   - How should error states be handled?

4. **Create `spec.md`**:

```markdown
# Spec: [Feature Name]
**Feature:** [feature-name] | **Date:** [YYYY-MM-DD] | **Status:** Draft
**Reference:** [discovery.md]

## Context
[2-3 sentences summarizing the problem and hypothesis from the discovery]

## Functional Requirements
### FR-01: [Requirement name]
- **Description:** [What the system must do]
- **User:** [Who performs this action]
- **Main flow:** [Happy path steps]
- **Alternative flows:** [Accepted variations]
- **Errors and exceptions:** [What happens when it fails]

### FR-02: ...

## Non-Functional Requirements
- **Performance:** [e.g., response time < 200ms for 95% of requests]
- **Security:** [validations, required authentication, RLS]
- **Accessibility:** [minimum WCAG level, keyboard behavior]
- **Availability:** [expected uptime, acceptable degradation]

## Acceptance Criteria
Given that [context], when [action], then [expected result].

- [ ] AC-01: Given that [condition], when [action], then [result]
- [ ] AC-02: ...
- [ ] AC-ERROR-01: Given that [error condition], when [action], then [error behavior]

## Out of Scope
- [Item that could be confused as included but isn't]
- [Related feature that will be handled separately]

## Dependencies
- [External API, service, or feature that must exist first]

## Constitution Check
- [ ] Respects [constitution principle 1]
- [ ] Respects [principle 2]
- [ ] Does not introduce exceptions to the defined quality standards
```

5. **Confirm**: Present the created spec. Flag any ambiguity that remained unresolved. Suggest next step: `/spec-design [feature-name]`.

## Rules
- Acceptance Criteria must be verifiable — no "the system should be fast"
- Each AC must map to a test that can be written
- Constitution check is mandatory if constitution.md exists
- Do not specify implementation — that's for /spec-design
