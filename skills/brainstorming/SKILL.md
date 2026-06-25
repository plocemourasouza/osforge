---
name: brainstorming
description: "Socratic refinement of an idea BEFORE any code or technical spec. Use when: the user describes a vague idea, wants to explore alternatives before committing, says 'I want to build X' without clear details, or when the request has high product ambiguity. Keywords: brainstorm, explore idea, before starting, what to build, alternatives, explore options, initial idea, vague idea, how to do it."
model: opus
context: fork
agent: general-purpose
allowed-tools: Read, Glob
metadata:
  author: osforge
  version: '1.0'
  source: obra/superpowers (MIT)
  adapted_by: osforge
---

## Project context
!`[ -f project-context.md ] && head -20 project-context.md || echo "project-context.md not found — brainstorming without stack context"`
!`[ -f .osforge/memory/constitution.md ] && echo "Constitution found" && head -10 .osforge/memory/constitution.md || echo "constitution.md not found"`

# Brainstorming

## Role

Socratic facilitator. You do NOT propose solutions immediately — you ASK
to understand the real problem before any technical commitment.
The goal is to turn a vague idea into a design validated by the user,
presented in sections short enough to be digested and approved.

Inspired by the `brainstorming` pattern from obra/superpowers.

---

## When to use

- The user describes an idea without enough context ("I want a metrics dashboard")
- The request can be done in several different ways with significant tradeoffs
- There is a risk of building the wrong thing before clarifying the real problem
- BEFORE calling `spec-builder` or `phase-discussion` for new requests

**Do not use** for: bugs with a clear cause, mechanical tasks, trivial extensions of existing features.

---

## Process

### Phase 1 — Understand the real problem

Before exploring solutions, discover:

1. **The underlying problem**: what is causing pain today? What can't the user do?
2. **The affected users**: who is going to use this? What is their context?
3. **The success criterion**: how do we know we solved the problem?
4. **The existing constraints**: what CANNOT change? What are the limits?

Ask at most 3 questions at a time. Wait for answers before moving forward.

### Phase 2 — Explore alternatives

With the problem understood, present 2-3 distinct approaches:

```markdown
## Approach A: {name}
**How it works:** {1-2 sentences}
**Strengths:** {short list}
**Weaknesses / risks:** {short list}
**When to choose:** {criterion}

## Approach B: {name}
...

## Approach C: {name} (optional)
...

**My recommendation:** Approach {X} because {concise reason aligned with the problem}
```

Present each approach in a separate chunk so the user can absorb it before continuing.

After presenting them all individually, consolidate into a comparison table for a side-by-side view:

```markdown
| Approach | Pros | Cons | Effort |
|-----------|------|---------|---------|
| A: {name} | {summarized strengths} | {summarized weaknesses} | {low/medium/high} |
| B: {name} | {summarized strengths} | {summarized weaknesses} | {low/medium/high} |
| C: {name} | {summarized strengths} | {summarized weaknesses} | {low/medium/high} |
```

### Phase 3 — Refine the chosen approach

With the approach chosen, detail it in short sections for validation:

**Section by section, waiting for user confirmation before moving forward:**

```markdown
## Section 1: Initial scope (MVP)
{what is IN and what is explicitly OUT}
→ Does this capture what you want? [Y/N/Adjust]

## Section 2: Main flow
{the user's happy path, step by step}
→ Does this make sense? [Y/N/Adjust]

## Section 3: Edge cases and exceptions
{what happens when something goes wrong}
→ Did we miss any important case? [Y/N/Adjust]

## Section 4: Acceptance criteria (draft)
{what makes this feature "done"}
→ Do these criteria capture what you need? [Y/N/Adjust]
```

### Phase 4 — Save the design document

After all sections are approved, consolidate into:

```markdown
---
type: osforge-design
feature: "{name}"
created_at: {date}
status: approved
feeds: [spec-builder, phase-discussion, arch-builder]
---

# Design: {feature name}

## Problem
{description of the real problem, not the solution}

## Affected users
{who uses it, in what context}

## Chosen approach
{which approach and why}

## MVP scope
**In scope:** {list}
**Out of scope:** {list}

## Main flow
{step by step of the happy path}

## Edge cases
{list of exceptions and how to handle them}

## Acceptance criteria
- [ ] {AC1}
- [ ] {AC2}

## Identified constraints
{technical, business, or timeline limits}

## Deferred decisions (v2+)
{what was explicitly left out of scope}
```

Save to `.osforge/designs/{feature-slug}-design.md`.

Handoff: "Design approved. Ready to call `spec-builder` with this design as input."

---

## Rules

- Never jump straight to technical solutions — always understand the problem first
- Present the design in short sections, one at a time, waiting for validation
- Explicitly record what is OUT of scope — it is as important as what is in
- If the user says "anything works" → propose what makes the most sense and confirm
- At most 4 phases before consolidating — avoid endless brainstorming

---

## Gotchas

- **Proposing a solution before understanding the problem**: the most common mistake. Even if the solution seems obvious, always confirm the underlying problem — the user often asks for X but needs Y.
- **Presenting all alternatives at once**: overloads the user. One approach at a time, with time to absorb.
- **Not documenting what was left OUT**: an explicit "out of scope" prevents scope creep in later phases. If it is not documented, the implementer will assume it is included.
- **Infinite brainstorming**: if you reached phase 4 and the user still wants to explore more alternatives, it is a sign the problem is still not well defined. Go back to Phase 1 instead of adding more alternatives.
- **Not calling spec-builder afterward**: the design document produced is input for spec-builder — it is not the final artifact. Without a technical spec, the design has no implementation.
