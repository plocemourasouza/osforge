---
name: orchestrator-awareness
description: >
  Always-on rule that guarantees activation of the Orchestrator when needed
  and respect for the progressive artifact system.
type: always-on
version: 1.0.0
---

# Rule: Orchestrator Awareness

## Orchestrator Activation

- When the user starts a conversation about development (new project, feature,
  bug, improvement), check whether the Orchestrator should be activated.
- If there is a `.osforge/status.yaml` with work in-progress: ALWAYS inform the
  user before any action: "There is work in progress: {project} — phase
  {current_phase}. Resume or start new?"
- For development demands involving more than 1 file or design
  decisions: suggest activating the Orchestrator for structured planning.
- For trivial quick fixes (1 file, zero ambiguity): do not impose the Orchestrator
  unless the user asks.

## Artifact System

- Never start implementing a STANDARD or COMPLEX feature without an approved
  spec/story (except when the user makes an explicit override).
- Planning artifacts must have frontmatter with `type`, `status` and `created`.
- When an artifact references another, use paths relative to the project.
- Artifact status: draft → ready → in-progress → complete.
- Never change an artifact with `complete` status without the user's approval.

## Tracking

- If `.osforge/status.yaml` exists, keep it updated on every phase change.
- If it does not exist and the work justifies it (STANDARD+), suggest creating it.
- Never delete entries from the status — mark them as `skipped` or `cancelled`.
