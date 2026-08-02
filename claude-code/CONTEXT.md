# OSForge — global ubiquitous language

The vocabulary shared across every project in this portfolio. Deployed to `~/.claude/CONTEXT.md`
and loaded in every session, so it is deliberately **short**: only terms that recur across
projects and that have been actively confused at some point. A project's own domain terms belong
in that project's `CONTEXT.md`, not here.

Skill that maintains this: `domain-modeling`. Format: that skill's `references/CONTEXT-FORMAT.md`.

## Language

**Skill**:
A directory with a `SKILL.md` under `skills/`, holding one discipline the agent can run.
_Avoid_: ability, tool, capability, module

**Core skill**:
A Skill listed in `claude-code/skills-core.txt`, deployed to `~/.claude/skills` and therefore
discoverable natively in every session. Everything else is reached through the Manifest.
_Avoid_: global skill, default skill, installed skill

**Manifest**:
The generated block in `SKILLS.md` holding one line per non-core Skill — a **context pointer** to
each. It is the only pointer to those skills: a skill outside both the core allowlist and the
Manifest does not exist at runtime.
_Avoid_: index, catalog, list

**Resolution**:
Reaching a non-core Skill through the Manifest — match a trigger, then read its `SKILL.md`.
Distinct from **invocation**, which is the Skill tool firing a core skill natively.
_Avoid_: loading, importing, calling

**Hub session**:
A session opened in the OSForge repo, for planning, portfolio review and framework work. Never for
executing code that lives in another repo.
_Avoid_: main session, control session

**Satellite session**:
A session opened in a target project's own directory. One session, one working directory.
_Avoid_: child session, worker session, sub-session

**Wave**:
A group of tasks with the same `wave` number in a task manifest, dispatched in parallel because
none of them blocks another. The next wave starts only when the previous one closes.
_Avoid_: batch, round, phase, sprint

**Spec**:
The artefacts under `.specs/features/<feature>/` produced by the `/spec-*` commands: what is being
built now. Distinct from a **Decision**, which records why a choice was made.
_Avoid_: PRD, design doc, ticket

**Decision**:
A hard-to-reverse, non-obvious choice recorded via `osforge-db add-decision` (or an ADR file).
_Avoid_: ADR when speaking generally, note, rationale

**Iron Law**:
The single inviolable rule at the top of a `SKILL.md`, written in uppercase. One per skill.
_Avoid_: rule, principle, constraint

**Leading word**:
A compact concept already in the model's pretraining, repeated through a skill so it anchors
behaviour in few tokens (_red_, _seam_, _tracer bullet_, _tight_).
_Avoid_: keyword, term, motif

## Industry vocabulary (canonical — do not invent synonyms)

Terms the wider AI-coding ecosystem already settled, adopted verbatim so OSForge speaks the same
language instead of coining parallel words. Source: `mattpocock/dictionary-of-ai-coding` (MIT).

**Context pointer**:
A cheap reference in context that lets the agent reach expensive content on demand — the Manifest
line is a context pointer. Pointer in context, target outside it.
_Avoid_: index entry, reference, link

**Smart zone / dumb zone**:
The stretch of a session where the agent is sharp, and the stretch after it where recall and
adherence degrade. Measured in TOKENS (dumb zone ~125–150k), not in share of the context window.
_Avoid_: context saturation, context full, 70% rule

**Attention budget**:
The finite attention a session has to spend across everything in its context. Unrelated work spends
it; this is why one task per session beats three.
_Avoid_: context budget when you mean attention

**Primary source**:
The thing itself — code, test, transcript, actual error. Complete, authoritative, expensive.
_Avoid_: the real code, ground truth

**Secondary source**:
An account of the thing — resume, spec, distillate, README. Cheap to load, records only what its
author believed mattered.
_Avoid_: summary, doc (when the distinction matters)

**Handoff artifact**:
The document that carries state from one session to the next, written for a reader with ZERO
context: absolute paths, decisions AND why, what is done, what is left.
_Avoid_: handoff doc, notes, state file

**Harness**:
The software around the model that runs the loop, holds tools and enforces limits — Claude Code
itself. Distinct from the MODEL, and from OSForge, which is configuration the harness loads.
_Avoid_: framework, runtime, agent (for the harness)

**Progressive disclosure**:
Keeping detail out of context until a pointer fires — a `SKILL.md` referencing `references/*.md`.
_Avoid_: lazy loading, on-demand docs

## Relationships

- A **Hub session** plans work; a **Satellite session** executes it — one project each
- A **Spec** produces tasks; tasks grouped by **Wave** are dispatched in parallel
- A **Skill** is either a **Core skill** (invoked natively) or reached by **Resolution**

## Flagged ambiguities

- "index" meant both the always-loaded trigger map and the generated `INDICE-SKILLS.json` —
  resolved: the runtime pointer is the **Manifest**; `INDICE-SKILLS.json` is the *skill index*, a
  build artefact used by `install-skill` and `buscar-skill.py`.
- "skill" was used for both a `SKILL.md` directory and the flat `.md` notes under `skills/<group>/` —
  resolved: only a directory with `SKILL.md` is a **Skill**; the flat files are *knowledge modules*.
