# Changelog

All notable changes to OSForge are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/). Architectural decisions are the ADRs in
`docs/DECISIONS.md`; this file records *what shipped*, the ADRs record *why*.

`VERSION` holds the current version; `deploy.sh` prints it. Releases are annotated git tags
(`vX.Y.Z`) with a GitHub Release carrying the matching section of this file.

## [5.0.0] — 2026-09-10

First tagged release. Everything since v4.0 (2026-03-18, 126 commits). **Major** because four
changes break a v4.0 install: `spec:*` commands renamed to `spec-*` (ADR-008), `sources/`
restructured and dead weight removed (ADR-009), all repository content re-authored in English
(ADR-011), and the deploy now installs only the core allowlist instead of every skill
(Model A) — a v4.0 user re-running `./deploy.sh` gets a different `~/.claude/`.

### Added
- **Orchestrator as language boundary** — the always-active meta-agent transcribes intent to
  English, coordinates in English, replies in the user's language; checkpointed
  `DETECT → INTAKE → TRIAGE → PLAN → ROUTE → TRACK → CORRECT` state machine; QUICK / STANDARD /
  COMPLEX triage; mandatory, auditable **route line** enforced by the `route-guard` Stop hook
  (deterministic where prose hit its ceiling); routing eval harness (`scripts/routing-cases.tsv`,
  `test-orchestrator-routing.sh`).
- **Plan Mode standard** (ADR-013) — read-only plan as a parallel-dispatch manifest
  (`docs/PLAN.template.md`), tasks carrying `story · wave · depends_on · model · agent · skills ·
  files · done-when · verify`; checkpoint per wave by default; `dispatching-parallel-agents`.
- **osforge-db** — local SQLite state (`~/.osforge/osforge.db`): tasks/board with waves and
  blockers, decisions, session resume in ~50 tokens (`session-resume.sh` / `session-save.py`),
  FTS5 search across projects, `evolve` with instincts, hub/satellite multi-project operation.
- **Vector memory, 3-tier** (ADR-010) — Qdrant via Docker (`--with-qdrant`) → SQLite vectors →
  keyword fallback; Ollama embeddings.
- **OSForge Canvas** — local generative UI (Bun, `localhost:4242`): specs, plans and breakdowns
  rendered as cards/tables/dependency graphs/gantt/checklists with structured feedback and SSE
  live-reload; default presentation channel; session autostart hook.
- **Zero-token hooks** — GateGuard (fact-forcing gate for irreversible Bash), `scan-secrets`,
  `protect-tests`, `observe-capture` (real skill-usage instrumentation), `notify-done`,
  `canvas-autostart`, `session-resume` / `session-save`, `route-guard`; reconciling hook merge
  in `deploy.sh` (OSForge-managed entries authoritative, user hooks preserved).
- **GateGuard: user confirmation opens the gate** — `gateguard.py` also runs on
  `UserPromptSubmit`; an explicit authorization ("tem permissão", "pode executar", "autorizo",
  "go ahead") or a bare affirmative ("sim", "ok", "yes") grants until the user's next message
  (15 min cap, `OSFORGE_GATEGUARD_GRANT_TTL`); `gateguard: sessão liberada` / `gateguard: ativa`
  for session-wide open/close; negations never grant; allowances audited as `GRANT-ALLOW`.
- **GateGuard: SQL detector** — a destructive verb only counts inside a DB-client invocation
  (psql/mysql/prisma/…); coverage extended to `DROP SCHEMA|ROLE|INDEX|COLUMN|…`,
  `ALTER TABLE … DROP`, `prisma migrate reset`, `db push --force-reset`, `run db:reset`.
  23 measured cases locked in `tests/test-gateguard-sql.sh`, 67 in `tests/test-gateguard-grant.sh`.
- **Verified system diagrams** (ADR-014) — `tt-a1i/archify` (MIT, v2.16.0) installed **pinned**
  by `deploy.sh` (`ARCHIFY_VERSION`, `--with-archify` / `--no-archify`, slim 2.5 MB, `doctor`
  check); new core skill **`system-diagrams`**: when a diagram is due, which of the five types,
  where it lives (`.specs/…/diagrams/`), and what counts as accepted — the `deliver` receipt
  (9/9 checks + SHA-256). Wired into `/spec-design` (`## Diagrams` block), `architecture`,
  `arch-builder`, `technical-design-doc-creator`, `visual-planner`. The repo ships its own map:
  `docs/architecture/osforge.{architecture.json,html,png}`. Analysis: `docs/ANALISE-ARCHIFY.md`.
- **Unified skill standard** (ADR-011, `docs/SKILL-STANDARD.md` + `docs/SKILL.template.md`) —
  `Use when / Keywords / Do NOT use for` triggers, invocation axis
  (`disable-model-invocation`), Iron Law, `Done when:` completion criteria on every step of
  the 47 core skills, exhaustiveness bars on reference-shaped skills, lifecycle buckets
  (`_deprecated/`, `_in-progress/`, `.out-of-scope/`).
- **Skill triggering harness** — `scripts/test-skill-triggering.sh` + hand-written naive
  pt-BR cases + cases harvested from every skill's own `Use when` (344 generated), per-case
  workdir, offline verdict tests (`tests/test-assertions.sh`), real context-cost measurement
  from harness logs (`scripts/measure-context.py`).
- **Ubiquitous language** — global `CONTEXT.md` + per-project glossary, `domain-modeling`,
  `codebase-design` (deep modules, seams, deletion test), `grilling` (one question at a time)
  as a global alignment rule; smart-zone context budget and primary-vs-secondary source rules.
- **Stack coverage policy** (ADR-012, `docs/STACK-COVERAGE.md`) — Context7 for volatile API
  facts, lean skills for durable discipline: `asaas-integration`, `better-auth`, `aws-deploy`,
  `llm-structured-output`; `context7-docs-first` rule.
- **Skill library growth** — antigravity-kit (32 skills, 15 agents), obra/superpowers,
  github/spec-kit + OpenSpec, GSD patterns, Anthropic frontend-design research
  (`aesthetic-boost`, anti-AI-slop rule), taste-skill (5 design skills + dials),
  agentic-ai-prompt-research (`tool-safety-classifier`, `context-compact`, `config-critique`,
  `stuck-recovery`), ui-ux-pro-max v2 (161 rules, 161 palettes, 84 styles), 32 marketing
  workflows in The Agency, `visual-planner`, `autorefine-skill` v3, `humanizer`, `design-md`,
  `llmfit-advisor`, Karpathy extensions in `coding-guidelines` — **177 skills, 27 agents,
  14 rules, 9 spec commands, 10 hooks, 14 ADRs**.
- `docs/EXAMPLES.md`, `docs/ANALISE-COMPARATIVA-MATTPOCOCK.md`, `docs/ANALISE-ARCHIFY.md`,
  `CHANGELOG.md`, `VERSION`.

### Changed
- **Deploy Model A** — only `claude-code/skills-core.txt` (47 skills) goes global, **flattened**
  (nested core skills were invisible at runtime — 17 of 46, measured); every other skill is
  indexed in the generated **MANIFEST** block of `SKILLS.md` and pulled per project with
  `scripts/install-skill.sh`. `deploy.sh` aborts when the manifest drifts. 20 visual generators
  demoted from the allowlist (~3.2k tokens/session).
- **Context budget** — `ENABLE_TOOL_SEARCH=true` (−21k tokens/session, no MCP removed); MCP
  servers context-scoped; prompt-cache strategy documented.
- README rewritten in English with Mermaid architecture, language boundary, credited Origins
  tables; `USAGE.md` restructured; agents deduplicated against skills; model ids updated.
- GateGuard matcher restricted to Bash; overwrite-redirect and `git commit --amend` /
  `checkout` removed from the destructive set (routine local work); denials logged.

### Removed
- Layer-3 project-local agents/skills/commands (ADR-002), `.cursorrules` in projects (ADR-007),
  legacy `spec:*` command names, obsolete docs and dead weight (ADR-009), pt-BR legacy prose.

### Fixed
- Manifest skill-root resolution in satellite projects; harness survival on first FAIL,
  macOS `timeout`/`gtimeout`, bash 3.2 assertion lib; Qdrant/Ollama checks; index polluted by
  `sources/`; GateGuard false positives measured in real sessions.

## [4.0.0] — 2026-03-18 (untagged)
Orchestrator layer + 14 planning/quality/context skills (`arch-builder`, `prd-builder`,
`spec-builder`, `epic-decomposer`, `story-executor`, `adversarial-review`, `readiness-gate`,
`ui-audit`, `project-context-generator`, …); intelligent routing from antigravity-kit;
`ui-design-intelligence`; `AGENT_FLOW.md`.

## [3.1.0] — 2026-03-09 (untagged)
31 skills, 7 agents, 4 rules, first Python hooks; repository established as the single source
of truth for `~/.claude/` and `~/.cursor/` (ADR-001).

[5.0.0]: https://github.com/plocemourasouza/osforge/releases/tag/v5.0.0
