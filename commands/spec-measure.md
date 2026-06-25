---
description: Phase 5 — Measures the real impact of the feature against the metrics defined in discovery.md. Run after production deploy or at the end of a validation cycle. Triggers: "measure", "measure impact", "post-deploy metrics", "feature result", "ROI", "/spec-measure [feature]".
---

## Required context
Read before executing:
- `.specs/features/[feature]/discovery.md` — success metrics defined before implementation
- `.specs/features/[feature]/spec.md` — acceptance criteria as a baseline
- `.specs/features/[feature]/validation.md` (if it exists) — implementation evidence

## Phase: Phase 5 — Measure (PDD)

## Expected output
`.specs/features/[feature-name]/measure.md`

## Process

The argument passed after `/spec-measure` is the feature. If empty, ask which feature to measure.

1. **Read `discovery.md`** and extract the success metrics defined in the "Success Metrics" table.

2. **Collect data**: Ask the user for the current values of the metrics (production data, analytics, feedback). If metrics have not been collected yet, record them as "Pending" with a suggestion on how to collect them.

3. **Create `measure.md`**:

```markdown
# Measure: [Feature Name]
**Feature:** [feature-name] | **Deploy:** [deploy date] | **Measured on:** [YYYY-MM-DD]

## Result vs Hypothesis

### Original Hypothesis
[copy from discovery.md]

### Verdict
**[✅ VALIDATED / ⚠️ PARTIAL / ❌ REFUTED / ⏳ AWAITING DATA]**
[1-2 sentences explaining the verdict]

## Metrics
| Metric | Baseline | Target | Result | Δ% | Status |
|---------|----------|--------|-----------|-----|--------|
| [primary] | [baseline] | [target] | [result] | [%] | ✅/⚠️/❌ |
| [secondary] | [baseline] | [target] | [result] | [%] | ✅/⚠️/❌ |

## Analysis
### What worked
- [observation 1]

### What didn't work
- [observation 1]

### Surprises
- [unexpected behavior, positive or negative]

## Decision
- [ ] **Continue** — expand rollout, planned iteration
- [ ] **Pivot** — [alternative hypothesis to test]
- [ ] **Abandon** — [reason and what was learned]
- [ ] **Wait** — [deadline for reevaluation: YYYY-MM-DD]

## Next Steps
- [action 1 with owner and deadline]
- [action 2 with owner and deadline]

## Learnings for the Project
[relevant insight for future decisions — will be extracted into tasks/lessons.md]
```

4. **Extract learnings**: If the measure.md contains relevant insights, update (or create) `tasks/lessons.md` in the project with the learned lesson.

5. **Archive feature**: If the verdict is "Abandon" or "Continue with no near-term iteration", move the directory to `.specs/features/_archived/[feature-name]/`.

## Rules
- If there is no production data available, record "Pending" and set a review date — do not invent numbers
- Metrics missing from discovery.md are a process failure — record it in measure.md as a lesson
- The verdict must be honest, even if the result is negative — features that teach something have value
- Learnings extracted into lessons.md must be actionable ("Never X" or "Always Y" or "When Z, do W")
