---
name: edge-case-hunter
description: "Exhaustive edge-case hunt via systematic enumeration of branches and boundaries, reporting in JSON only the paths without handling. Use when: asked for edge cases or boundary conditions of a diff/file/function, verifying null/empty inputs and off-by-one before merging, checking race conditions and division by zero, validating date/timezone/unicode handling, auditing a PR for unguarded paths. Keywords: edge case, boundary, branch, null, off-by-one, overflow, race condition, unhandled path, guard, hunt. Do NOT use for: general code quality review (use code-review-checklist) nor refinement of specs and documents (use elicitation-engine)."
trigger: edge case|boundary|hunt edges|caça edge
model-tier: sonnet
---

# Edge Case Hunter

## Method
Exhaustive path enumeration — walk through each branch mechanically,
do NOT hunt by intuition. Report ONLY paths and conditions without handling.
Silently discard the handled ones. Do NOT editorialize — findings only.

## Inputs
- **content** — Diff, full file, or function
- **also_consider** (optional) — Additional areas to consider

## Scope
- If diff: analyze ONLY the diff hunks; list boundaries directly
  reachable from the changed lines that have no explicit guard
- If file/function: treat the whole content as scope
- Ignore the rest of the codebase unless the content references external functions

## Execution

### 1. Receive Content
- If empty or undecodable → return error JSON and stop

### 2. Exhaustive Path Analysis
Walk through ALL branching paths and boundary conditions:
- Control flow: conditionals, loops, error handlers, early returns
- Domain boundaries: value transitions, states, conditions

Edge classes derived from the content (not a fixed checklist):
- Missing else/default/catch
- null/undefined/empty string/empty array inputs
- Off-by-one in loops and slices
- Arithmetic overflow/underflow and division by zero
- Implicit type coercion (especially in == comparisons)
- Race conditions and concurrent access
- Timeout gaps and network failures
- Empty array vs 1 item vs many items
- Unicode and special characters in strings
- Date/timezone edge cases
- Cross-platform file/path separators

### 3. Validate Completeness
Revisit each edge class from Step 2.
Add any new unhandled paths found.

### 4. Output — JSON Array

```json
[{
  "location": "file:start-end",
  "trigger_condition": "description in up to 15 words",
  "guard_snippet": "minimal code sketch that closes the gap",
  "potential_consequence": "what can go wrong in up to 15 words"
}]
```

An empty array `[]` is valid when no unhandled path is found.
No extra text, no explanations, no markdown wrapping.

## Halt Conditions
- Empty input → return `[{"location":"N/A","trigger_condition":"Input empty","guard_snippet":"Provide content","potential_consequence":"No analysis"}]`
