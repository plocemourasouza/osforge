---
description: Helper — Generates a customized acceptance-criteria checklist for the current feature, based on spec.md and design.md. Use before considering the implementation complete or to generate QA criteria. Triggers: "checklist", "acceptance criteria", "QA checklist", "ready to test", "/spec-checklist [feature]".
---

## Required context
Read before executing:
- `.specs/features/[feature]/spec.md` — source of the Acceptance Criteria
- `.specs/features/[feature]/design.md` — contracts and technical edge cases
- `.specs/features/[feature]/tasks.md` (if it exists) — completed tasks
- `.specs/memory/constitution.md` — project quality standards

## Phase: Helper — Checklist

## Expected output
`.specs/features/[feature-name]/checklist.md`

## Process

The argument passed after `/spec-checklist` is the feature. If empty, ask which feature.

1. **Read spec.md in full** and extract all Acceptance Criteria.

2. **Read design.md** to identify technical edge cases not explicitly covered in the AC.

3. **Build a checklist in 5 categories**:

```markdown
# Checklist: [Feature Name]
**Feature:** [feature-name] | **Date:** [YYYY-MM-DD]
**References:** spec.md | design.md

## Functionality (Happy Path)
- [ ] [AC-01 rewritten as an executable check]
- [ ] [AC-02 rewritten as an executable check]
- [ ] [each AC from spec.md becomes at least one item here]

## Edge Cases & Errors
- [ ] Unauthenticated user → receives 401 or redirect to login
- [ ] Invalid input → error message shown in the correct field
- [ ] [edge cases specific to design.md]
- [ ] [error cases listed in the contracts]

## Security
- [ ] Server Action checks authentication before any operation
- [ ] Inputs validated with Zod at the entry point
- [ ] Sensitive data not exposed in error messages
- [ ] [context-specific checks: RLS, multi-tenancy, etc.]

## Performance
- [ ] No unnecessary fetch waterfalls
- [ ] Bundle size: no barrel imports in critical components
- [ ] [specific checks identified in the design]

## Code Quality
- [ ] `bun test` — 0 failures
- [ ] `bun run build` — exit 0, no TypeScript errors
- [ ] Lint passes with no errors (`bun run lint`)
- [ ] All ACs mapped to tasks in tasks.md have completed tasks
```

4. **Confirm**: Present the checklist. Ask whether there are additional criteria to include before starting implementation or validation.

## Rules
- Each checklist item must be verifiable without ambiguity (yes/no, pass/fail)
- Never use "works correctly" as a criterion — describe the expected behavior
- If spec.md has no clear AC for an expected behavior, record it in the checklist and flag it to update the spec
- The "Security" category is mandatory — never omit it, even for seemingly simple features
