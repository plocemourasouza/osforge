---
description: Helper — Resolves ambiguities and gaps in the specification or design before proceeding to the next phase. Use whenever a .specs/ artifact has fields marked as "NEEDS CLARIFICATION", "?", or "TBD". Triggers: "clarify", "clear up", "gaps", "ambiguity", "what does this mean", "/spec-clarify [feature]".
---

## Required context
Read before executing:
- `.specs/features/[feature]/discovery.md` (if it exists)
- `.specs/features/[feature]/spec.md` (if it exists)
- `.specs/features/[feature]/design.md` (if it exists)
- `.specs/memory/constitution.md` (existing standards and decisions)

## Phase: Helper — Clarification

## Expected output
In-place update of the artifacts in `.specs/features/[feature]/` with the gaps resolved.

## Process

The argument passed after `/spec-clarify` is the target feature. If empty, ask which feature to clarify.

1. **Gap sweep**: Read all of the feature's artifacts and identify:
   - Fields with "NEEDS CLARIFICATION", "TBD", "?", "TODO"
   - Vague Acceptance Criteria (without a measurable or verifiable criterion)
   - Design fields with no recorded decision (e.g., schema with no defined types, contract with no examples)
   - Unvalidated assumptions that impact the implementation

2. **Group by urgency**:
   - **Blockers**: gaps that prevent starting the next phase
   - **Important**: gaps that cause rework if not resolved now
   - **Non-blocking**: can be resolved during implementation

3. **Formulate precise questions** (maximum 5 per round):
   - One question per gap
   - Include context on why it matters
   - Suggest options when possible (makes for a faster decision)

4. **Record answers**: After receiving the user's answers, update the artifacts in place:
   - Replace "NEEDS CLARIFICATION" with the decision made
   - Add date and rationale in the "Decisions" section of design.md (if it exists)
   - Update AC fields with measurable criteria

5. **Confirm resolution**: List the resolved gaps and those still pending. If all blocking gaps have been resolved, suggest the next phase.

## Rules
- Never advance to the next phase with unresolved blocking gaps
- For non-blocking gaps, record the default decision with a note explaining the choice
- Prefer asking a few well-formulated questions over a long list — the user pays a cognitive cost per question
- If the gap can be resolved from the project context (constitution.md, existing code), resolve it without asking
