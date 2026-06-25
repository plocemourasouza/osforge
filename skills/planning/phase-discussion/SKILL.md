---
name: phase-discussion
description: "Captures implementation decisions for a phase BEFORE technical planning. Use when planning any phase with UI, API, content system, or data reorganization. Keywords: discuss phase, discuss phase, phase decisions, phase context, before planning, what to decide first, phase N, phase discussion."
model: sonnet
allowed-tools: Read, Write, Glob
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "Check that CONTEXT.md was saved in .osforge/phases/ before finishing."
metadata:
  version: '1.1'
---

## Project context
!`ls .osforge/phases/ 2>/dev/null && echo "Existing phases:" && ls .osforge/phases/ || echo "No CONTEXT.md from a previous phase found"`

# Phase Discussion

## Role

Facilitator that extracts the user's preferences before any code
is planned or written. The roadmap has sentences. Sentences are not enough
to build what the user imagines. This skill fills that gap.

Inspired by the `discuss-phase` pattern from GSD (get-shit-done).

---

## When to use

- Before `spec-builder`, `arch-builder`, or `story-executor` for any phase
- When the phase involves UX decisions, API structure, or data organization
- When the user says "I want it to look like this" without detailing how
- Before any phase with a visual interface

---

## Common pitfalls

- **Assuming decisions instead of asking**: the role of this skill is to ASK, not to DECIDE. Even if the "obvious" option seems clear, always present the alternatives and let the user choose — assumed decisions are the main cause of rework.
- **Going into implementation details**: phase-discussion captures the user's PREFERENCES, not technical choices. "Which database?" is not a question for this phase — "list or grid to display the items?" is. Implementation details go to arch-builder.
- **Not saving CONTEXT.md**: if the discussion happens but CONTEXT.md is not saved in `.osforge/phases/`, spec-builder and story-executor will not have access to the decisions. Always generate and save the file, even if the discussion was short.
- **Asking questions in sequence without batching**: long one-question-at-a-time sessions tire the user. Group up to 3 related questions into one response (implicit `--batch`). If the user already answered several gray areas spontaneously, do not repeat what has already been decided.
- **Using a previous phase's CONTEXT.md**: always create a new CONTEXT.md per phase with a name including the phase number (`2-CONTEXT.md`). Reusing a previous phase's file overwrites decisions that may be different.

---

## Process

### 1. Identify the phase

Read the phase description in the roadmap/epic. If no formal artifact exists,
ask the user: "Describe in 2-3 sentences what this phase delivers."

### 2. Identify gray areas by phase type

Analyze the phase and identify which categories apply:

**Phases with visual features (UI/UX)**
- Layout and density: list, grid, card, table, mixed?
- Interactions: hover, drag-drop, inline edit, modal, slide-over?
- Empty states: placeholder, skeleton, call-to-action?
- Mobile: responsive or desktop-first for now?
- Navigation: breadcrumb, tabs, sidebar, steps?

**Phases with APIs or CLIs**
- Response format: flat JSON, nested, enveloped?
- Error handling: codes, messages, exposed stack trace?
- Pagination: cursor, offset, no pagination?
- Authentication: JWT, API key, session, public?
- Versioning: `/v1/`, header, no version?

**Phases with content systems**
- Structure: hierarchical, flat, tags, categories?
- Tone: formal, conversational, technical?
- Depth: summarized, detailed, expandable?
- Flow: linear, non-linear, branched?

**Phases with data organization/migration**
- Grouping criterion: by date, category, user, status?
- Duplicate handling: merge, keep both, flag?
- Exceptions: how to handle records that do not fit?
- Rollback: reversible or one-way?

### 3. Conduct the discussion

For each identified gray area:
1. Present the concrete options (not abstract ones)
2. Indicate which would be the reasonable default and why
3. Ask the user's preference
4. Record the decision

**Compact mode (`--batch`):** group up to 3 related questions into a single
expected response, for users who prefer to answer in a block.

Continue until all relevant gray areas are resolved
or the user explicitly says "enough, proceed".

### 4. Generate CONTEXT.md

```markdown
---
type: osforge-phase-context
phase: "{N} — {phase title}"
created_at: {date}
feeds: [spec-builder, arch-builder, story-executor]
---

# Phase {N} Context: {title}

## Decisions Made

### Visual / UX
- **Layout:** {decision} — Reason: {user's justification}
- **Interactions:** {decision}
- **Mobile:** {decision}

### API / Backend
- **Response format:** {decision}
- **Pagination:** {decision}
- **Authentication:** {decision}

### Data
- **Grouping:** {decision}
- **Duplicates:** {decision}

## Deferred Decisions (v2+)
- {item the user explicitly placed out of scope}

## Identified Constraints
- {any technical or business constraint mentioned}

## Free Notes
{observations that do not fit the categories above}
```

Save in `.osforge/phases/{N}-CONTEXT.md`.

---

## Integration with other skills

The generated `CONTEXT.md` must be loaded explicitly by the following skills:

- **`spec-builder`** → reads CONTEXT.md to generate ACs aligned with the decisions
- **`arch-builder`** → reads CONTEXT.md to make informed architecture decisions
- **`story-executor`** → reads CONTEXT.md to implement what the user imagined

Always mention in the handoff: "Load `.osforge/phases/{N}-CONTEXT.md`
before planning this phase."

---

## Rules

- Never assume a decision — always ask when there is ambiguity
- Do not go into implementation details at this step (that is for arch-builder)
- Keep the focus on the user's PREFERENCES, not on technical solutions
- If the user says "anything works" → record the reasonable default as the decision
- Maximum of 15 minutes of discussion — if it is running over that, group the remaining questions
