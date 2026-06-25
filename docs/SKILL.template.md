---
# ─────────────────────────────────────────────────────────────────────
# OSForge SKILL.template.md — single source of truth for authoring skills
# Fill in, delete the comments, validate with scripts/test-skill-triggering.sh
# LANGUAGE: all repo content is written in ENGLISH (replies to the user follow
# the user's language — that is a runtime rule in CLAUDE.md, not here).
# ─────────────────────────────────────────────────────────────────────

name: <kebab-case-slug>

# DESCRIPTION — the ACTIVATION axis. Rules:
#  • leading word up front (a concept the model already holds from pretraining)
#  • Use when: ONE trigger per branch (do not repeat the same idea with synonyms)
#  • Keywords: search terms, no duplication of the triggers
#  • Do NOT use for: EXPLICIT disambiguation against sibling skills (REQUIRED)
description: "<short summary with leading word>. Use when: <branch 1>, <branch 2>, <branch 3>. Keywords: <t1, t2, t3>. Do NOT use for: <case → sibling-skill>, <case → sibling-skill>."

# INVOCATION AXIS — conscious decision (from mattpocock/writing-great-skills):
#  • ORCHESTRATOR (user-invoked): fires only when the user types it; zero context load.
#    → uncomment the line below. It must NOT be called by another orchestrator.
#  • DISCIPLINE (model-invoked): the agent may fire it on its own; description sits in context every turn.
#    → keep the line commented (default).
# disable-model-invocation: true

# EXECUTION ROUTING (OSForge strength — fill what applies):
model: sonnet              # sonnet | opus | haiku
# context: fork            # uncomment if the skill runs in an isolated context
# agent: general-purpose   # uncomment if it delegates to a subagent
allowed-tools: Read, Grep, Glob, Edit

metadata:
  version: "1.0.0"
  # inspired_by: <org/repo (skill)>     # if adapted from a third party
  # source: <org/repo>
  # license_note: "<e.g., Adapted under MIT>"
---

# <Title> (<leading word>)

**Iron Law:** `<ONE INVIOLABLE RULE IN UPPERCASE, ANCHORED ON A LEADING WORD>`
<!-- e.g.: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST -->

## When NOT to use
<!-- mirrors the description's "Do NOT use for" — cases that look similar but aren't -->
- <case> → use `<sibling-skill>`
- <case> → use `<sibling-skill>`

## Process
<!-- ordered steps; each ends on a CHECKABLE completion criterion -->
### 1. <step>
<action>
**Done when:** <checkable and, where it matters, exhaustive condition>

### 2. <step>
<action>
**Done when:** <checkable condition>

## Anti-patterns
| WRONG | RIGHT |
|---|---|
| <observed bad pattern> | <correct pattern> |

## References  (progressive disclosure — only what doesn't fit inline)
<!-- push long reference into linked files; loaded only when the pointer fires -->
- `references/<file>.md` — <what it holds>

<!--
AUDIT before publishing (failure modes):
[ ] Premature completion: does every step have a checkable "Done when:"?
[ ] No-op: any line the model already obeys by default? → delete
[ ] Duplication: same meaning in two places? → single source of truth
[ ] Sprawl: too long? → progressive disclosure
[ ] Activation: Use when + Keywords + Do NOT use for present? invocation axis decided?
[ ] Language: body and description in English?
[ ] Validate: ./scripts/test-skill-triggering.sh (green before committing)
-->
