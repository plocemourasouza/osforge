---
description: Phase 0 — Discovers and validates the user's problem before specifying any solution. Ensures we are building the right thing. Use when starting any feature that affects the end user. Triggers: "discover", "what problem to solve", "why build", "validate hypothesis", "user problem", "/spec-discover [feature]".
---

## Required context
Read before executing:
- `.specs/memory/constitution.md` (if it exists)
- `.specs/project/PROJECT.md` (if it exists)
- `.specs/project/STATE.md` (previous sessions)

## Phase: Phase 0 — Discover (PDD)

## Expected output
`.specs/features/[feature-name]/discovery.md`

## Process

The argument passed after `/spec-discover` is the feature description. If empty, ask: "Which feature or problem do you want to explore?"

1. **Generate feature name**: 2-4 words in kebab-case extracting the most meaningful keywords.
   - "add authentication with Google" → `google-auth`
   - "fix timeout at checkout" → `fix-checkout-timeout`

2. **Create directory**: `.specs/features/[feature-name]/`

3. **Ask discovery questions** (maximum 4, only if needed):
   - Who is the user affected by this problem?
   - What evidence do we have that this is a real problem?
   - How will we know we solved the problem?
   - What is NOT in the MVP scope?

4. **Create `discovery.md`** with the structure below, using information from the input and inferences from context:

```markdown
# Discovery: [Feature Name]
**Feature:** [feature-name] | **Date:** [YYYY-MM-DD] | **Status:** Draft

## User Problem
- **Who suffers:** [specific persona]
- **What happens:** [current situation — concrete, observable pain]
- **Evidence:** [data, feedback, metrics, or observations]
- **Frequency:** [daily / weekly / occasional]

## Hypothesis
We believe that [proposed solution] will [expected result] for [persona]
because [evidence-based reason].

## Success Metrics
| Metric | Baseline (current) | Target | How to measure | Deadline |
|---------|------------------|--------|------------|-------|
| [primary] | [value] | [goal] | [how] | [weeks] |
| [secondary] | [value] | [goal] | [how] | [weeks] |

## Decision Criteria
- **Success:** [primary metric hits target on schedule]
- **Pivot:** [if metric < X% of target]
- **Abandon:** [if after Y weeks with no improvement]

## MVP Scope
- **Includes:** [minimal functionality to test the hypothesis]
- **Does NOT include:** [what can wait]

## Priority
Impact: [High/Medium/Low] × Confidence: [High/Medium/Low] / Effort: [High/Medium/Low]
Score: [compute: H=3, M=2, L=1 → (Impact × Confidence) / Effort]

## Alternatives Considered
- Do nothing: [consequence]
- [Alternative A]: discarded because [reason]
```

5. **Confirm**: Present the created discovery. Ask whether to proceed to `/spec-specify` or whether there are adjustments.

## Rules
- NEVER skip this phase for features that touch the end user
- For purely technical tasks (refactoring, infra, CI/CD), this phase is optional
- If there is no evidence of the problem, flag it and suggest collecting data before specifying
- If you cannot define a success metric, the scope is too vague — resolve it before moving forward
