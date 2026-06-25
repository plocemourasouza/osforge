---
name: elicitation-engine
description: "Iterative refinement of outputs (specs, PRDs, architectural decisions, any artifact) via an interactive menu of structured elicitation techniques. Use when: asked to refine this, improve or deepen a spec/PRD, dig deeper into a design decision, what questions am I missing, strengthen a weak section of a document before finalizing. Keywords: elicit, refine, refinement, deepen, improve output, spec, PRD, elicitation, dig deeper, iterate. Do NOT use for: edge-case hunting in code (use edge-case-hunter) nor code review (use code-review-checklist)."
trigger: elicit|refine output|dig deeper|melhorar spec|aprofundar
model-tier: sonnet
---

# Elicitation Engine

## Objective
Force reconsideration, refinement and improvement of a recent output
using structured elicitation techniques. Each technique attacks the
content from a different angle to reveal gaps, improve decisions,
and strengthen the quality of the artifact.

## Inputs
- **content** — Content/section to be refined (from the conversation context)
- **focus_area** (optional) — Specific area to focus the elicitation on

## Process

### 1. Load Methods
Read `./methods.csv` (fields: num, category, method_name, description, output_pattern)

### 2. Context Analysis
- Analyze current content: type, complexity, risks, creative potential
- Identify the weakest areas of the content that would benefit from elicitation

### 3. Intelligent Selection
1. Select 3 methods that best apply to the context and content type
2. Balance between foundational and specialized
3. Prioritize methods that attack the weakest identified areas

### 4. Present and Execute

```
**Elicitation Engine**
Choose (1-3), [r] Reshuffle, [x] Proceed:

1. {Method} — {short description}
2. {Method} — {short description}
3. {Method} — {short description}
r. New 3 methods
a. List all available methods
x. Finish with current content
```

**If 1-3:** Execute the selected method on the content.
  - Apply it creatively to the content/section being refined
  - Show the improved version with what the method revealed
  - Ask: "Apply changes? [Y] Yes / [N] No / {free-form instruction}"
  - If yes → apply to the artifact. If no → discard.
  - Re-present the menu for more elicitations

**If r:** Select 3 new diverse methods, present them.

**If a:** List all methods with descriptions in a compact table.
  Allow selection by number or name.

**If x:** Return the final refined content to the calling skill.

### 5. Accumulation
Each method accumulates on top of previous improvements.
Keep tracking what has been applied to avoid repetition.

## Integration
When invoked from within another skill (spec-builder, prd-builder, etc.):
1. Receive the content of the section being worked on
2. Run the elicitation loop
3. Return the refined content when the user selects 'x'
4. The calling skill continues with the improved content
