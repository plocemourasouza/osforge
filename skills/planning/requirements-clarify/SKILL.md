---
name: requirements-clarify
description: "Structured requirements clarification BEFORE the technical plan. Use when: a spec has vague or underspecified areas, the user said 'it can be anything', the requirements leave room for multiple interpretations, BEFORE spec-builder on new demands. Keywords: clarify requirements, requirements clarification, underspecified, ambiguous requirements, clarify, before the plan, clarify requirements."
model: sonnet
allowed-tools: Read, Write, Glob
metadata:
  author: osforge
  version: '1.0'
  source: github/spec-kit (MIT)
  adapted_by: osforge
---

## Context
!`[ -f project-context.md ] && head -15 project-context.md || echo "project-context.md not found"`
!`ls .osforge/designs/ 2>/dev/null | head -5 && echo "Designs found" || echo "No design document found"`

# Requirements Clarify

## Role

Coverage-based clarification facilitator. Systematically identifies
the underspecified areas of a demand and resolves them before the technical
plan is generated — preventing spec and implementation rework.

Adapted from the `/speckit.clarify` pattern of github/spec-kit.

---

## When to use

- Before `spec-builder` for demands with vague terms
- When brainstorming produced an approved design but with gaps
- Whenever the user uses words like "work well", "be fast", "integrate with X", "somehow", without detailing
- For complex features with multiple stakeholders or alternative flows

**Examples of vague words and the concrete question that resolves them:**

| Vague word | Clarification question |
|---|---|
| "work well" | What latency is acceptable? What error rate is tolerated? |
| "fast" | How many ms response? P50 or P95? |
| "many users" | How many concurrent users? 100, 10k, 1 million? |
| "integrate with X" | Via REST API, webhook, or manual import? Sync or async? |
| "secure" | Who can access what? Does it need auditing or encryption at rest? |
| "somehow" | What are the 2-3 possible ways and what is the selection criterion? |

**Do not use** for: clear mechanical tasks, bugs with a known cause, trivial extensions with an established pattern.

---

## Process

### 1. Analyze the demand across coverage dimensions

Check coverage in each dimension:

**Functional**
- Is the happy path complete and gap-free?
- Are the alternative flows (error states, edge cases) defined?
- Are the business rules explicit or implicit?

**Data**
- What data is needed for each action?
- What is the expected format of inputs and outputs?
- Are there limits on volume, size, or frequency?

**User / UX**
- Who are the users and what is the usage context?
- What level of visual feedback is needed (loading, error, success)?
- Are there accessibility or internationalization considerations?

**Integration**
- What external systems does this need to integrate with?
- What are the expected API contracts?
- Are there timing dependencies (sync vs async)?

**Security / Privacy**
- What data is sensitive?
- Who can view/edit what?
- Are there LGPD or auditing requirements?

### 2. Generate clarification questions

For each identified gap, formulate a specific and actionable question:

```markdown
## Clarification Questions — {feature}

**Functional (3 questions)**
1. {specific question with context}
   *Why it matters: without this, the spec may generate incorrect ACs for {case X}*

2. {question about an alternative flow}
   *Why it matters: {impact on implementation}*

**Data (2 questions)**
3. {question about data format/limit}

**UX (1 question)**
4. {question about needed visual feedback}

**Security (1 question)**
5. {question about access/permissions}
```

Present the questions in groups by dimension. Maximum 8-10 questions total — prioritize the most impactful ones.

### 3. Process answers

For each answer received:
- Record the decision
- Identify whether the answer generates new questions (maximum 2 rounds of follow-up)
- Mark the area as "clarified" ✅

### 4. Generate the Clarifications Record

After all answers, consolidate into:

```markdown
---
type: osforge-clarifications
feature: "{name}"
clarified_at: {date}
feeds: [spec-builder]
---

# Clarifications: {feature name}

## Decisions Made

### Functional
- **{area}:** {decision} — recorded on {date}
- **{area}:** {decision}

### Data
- **{area}:** {decision}

### UX
- **{area}:** {decision}

### Security
- **{area}:** {decision}

## Areas Explicitly Out of Scope
- {item the user confirmed is NOT in scope}

## Assumptions Made (without explicit confirmation)
- {assumption made because the user said "anything works"}
```

Save in `.osforge/designs/{feature-slug}-clarifications.md`.

Handoff: "Clarifications complete. Ready to call `spec-builder` with this document as additional input."

---

## Gotchas

- **Asking obvious questions**: questions that any developer would answer the same way do not need to be asked. Focus on the ambiguities that would lead to different implementation decisions from one implementer to another.
- **More than 10 questions at once**: overloads the user and signals that the demand is poorly understood. If you need more than 10, split into rounds.
- **Not recording assumptions made**: if the user said "anything works" for something important, record the assumption made explicitly. Implicit assumptions are the most common source of rework.
- **Indefinite second round of clarification**: maximum 2 rounds of follow-up. After that, what is still unclear should be recorded as an assumption and revisited in the spec phase.
- **Clarifying the obvious**: if the answer is universally "yes" for the OSForge stack (e.g.: "will it use TypeScript?"), do not ask — record it as an assumption directly.
