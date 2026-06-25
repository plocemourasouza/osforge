# User Story: [STORY-ID] [Feature Name]

## Product Context (mandatory)
- **Observed problem:** [what the user faces today — with concrete evidence]
- **Hypothesis:** [we believe X solves it because Y]
- **Discarded alternatives:** [what we considered and why we didn't go with it]
- **Risk if we don't:** [what happens if we don't implement it]

## Story
As a [specific persona, not "the user"],
I want [concrete action]
so that [measurable benefit].

## Product Priority
- User impact: [High / Medium / Low]
- Hypothesis confidence: [High / Medium / Low] — basis: [data / feedback / intuition]
- Technical effort: [High / Medium / Low]
- **Score:** (Impact × Confidence) / Effort = [value]

## Success Metrics
| Metric | Baseline (current) | Target | How to measure | Deadline |
|---------|------------------|--------|------------|-------|
| [primary] | [value] | [goal] | [event/query] | [weeks] |
| [secondary] | [value] | [goal] | [event/query] | [weeks] |

- **Success criterion:** [primary metric hits target]
- **Failure criterion:** [if < X% in Y weeks, pivot]

## Acceptance Criteria (technical)
- [ ] AC-1: [Verifiable criterion]
- [ ] AC-2: [Verifiable criterion]
- [ ] AC-3: [Verifiable criterion]

## Optimal Path (Happy Path)
1. User [initial action]
2. System [expected response]
3. User [next action]
4. Result: [expected final state]

## Edge Cases
| ID | Scenario | Input | Expected Output | Severity |
|----|---------|-------|-----------------|------------|
| EC-1 | Empty field | "" | Validation error message | High |
| EC-2 | Network timeout | >5s with no response | Retry with visual feedback | Medium |
| EC-3 | Invalid data | Unexpected format | Graceful fallback | High |

## Dependencies
- [Required feature or service]

## Completion Criterion
This story is **DONE** when:
- ALL technical acceptance criteria pass
- All High-severity edge cases are covered
- Automated tests exist for the happy path
- Code passed review (or the validator agent)
- **Success metrics are configured and a baseline recorded**
- **Analytics events implemented**
- **Metrics review date scheduled**
