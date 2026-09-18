# Changelog

All notable changes to OSForge are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/). Architectural decisions are the ADRs in
`docs/DECISIONS.md`; this file records *what shipped*, the ADRs record *why*.

`VERSION` holds the current version; `deploy.sh` prints it. Releases are annotated git tags
(`vX.Y.Z`) with a GitHub Release carrying the matching section of this file.

## [Unreleased]

### Added
- **ECC comparative audit (rev. 3)** — `docs/ANALISE-COMPARATIVA-ECC.md` with the evidence table
  `docs/ANALISE-COMPARATIVA-ECC-EVIDENCIAS.md` (78 permalinked findings, both repos at fixed SHAs)
  and the executable programme `docs/BACKLOG-EVOLUCAO.md` (24 items, 5 stages, 7 experiments).
- **ADR-015** — evolution programme: import mechanisms, not content; measure before adopting.
- `.out-of-scope/ecc-imports.md` — what was rejected from ECC and why.

### Fixed (stage 0 of `docs/BACKLOG-EVOLUCAO.md`)
- **GateGuard grant requires a pending denial** (B-001, E-A05): a turn grant ("ok", "sim",
  "proceed", "tem permissão") is accepted only within 10 min of a denial in the same session;
  otherwise it is logged as `GRANT-IGNORED-NO-PENDING-DENIAL` and nothing opens. Session grants
  stay explicit. `OSFORGE_GATEGUARD_LEGACY_GRANT=1` restores the old behaviour for one release.
  `tests/test-gateguard-grant.sh`: 67 → 79 cases.
- **`scan-secrets` works under Claude Code** (B-002, E-A01): rewritten as `hooks/scan-secrets.py`
  (the `.sh` is a wrapper); reads `tool_input.command` or `command`, answers in each harness's
  contract, scans the **staged diff content** with bounded patterns (`sk-`, `ghp_`, `AKIA`, Slack,
  URL credentials, PEM, `password =`), blocks root `rm -rf`; `osforge:allow-secret` for fixtures;
  `OSFORGE_SCAN_SECRETS=off`. New offline test `tests/test-scan-secrets.sh` (33 cases).
  `deploy_cursor` now copies `.py` hooks too.
- **`deploy.sh` on a fresh HOME** (B-003, E-A31, E-A33): tolerates a missing `~/.claude.json`,
  refuses to overwrite an invalid one, checks `rsync`/`python3` up front, gates the MCP drift
  check and every `mkdir`/`rm` behind `--dry-run` (dry-run now creates nothing), and drops every
  `_`-prefixed documentation key from `settings-base.json` before merging.

### Added (stage 1 — safety net)
- **Hook contract tests** (B-006): `tests/hooks/run-contracts.sh` runs the real command
  strings from `hooks/hooks-claude-code.json` and `hooks/hooks.json` against payload fixtures
  for both harnesses (52 checks) in a sandboxed HOME, asserting exit 0, JSON-or-empty stdout,
  the harness verdict and no writes to `/tmp`. Wired into the deploy preflight. Contract in
  `docs/HOOKS.md`.
- **Agent frontmatter validation** (B-009): `scripts/check-agents.py` (deploy preflight + CI):
  `tools` scalar with known names, `model` enum, read-only roles must not carry write tools.
  `planner`, `code-reviewer`, `security-auditor`, `validator`, `explorer-agent` and
  `system-architect` now declare `tools: Read, Grep, Glob, Bash`; `planner`, `validator` and
  `system-architect` are `model: opus` per the tier table; `validator` dropped a non-Claude-Code
  tools schema; `project-planner` gained `Write` (its body creates a file).
- **Count drift check** (B-008): `scripts/check-counts.py` fails when README, CLAUDE.md,
  `claude-code/CLAUDE.md` or USAGE quote a number that differs from the tree (skills, core,
  agents, rules, hooks, spec commands, global MCPs, `ENABLE_TOOL_SEARCH`).
- **Minimal CI** (B-008): `.github/workflows/ci.yml` on ubuntu + macos: syntax, fresh
  manifest/indexes, agents, counts, the five offline test suites, and a dry-run deploy in an
  empty HOME that must create nothing.

### Fixed (stage 1)
- `notify-done.sh` notified only when `stop_hook_active` was true, i.e. almost never (B-007,
  E-A13). `protect-tests.sh` now tells the model (additionalContext) instead of logging to
  `/tmp` (E-A12). `gateguard.py`, `route-guard.py` and `observe-capture.py` no longer crash on
  a payload that is not an object. No hook writes to `/tmp` any more: logs live in
  `~/.osforge/logs/` (`OSFORGE_LOG_DIR`).
- `route-guard.py` counted `echo skills/x/SKILL.md` in a Bash command, or a bare skill name in
  a subagent prompt, as evidence that the skill was loaded (E-A11). Only Read/Glob/Grep, a
  reading Bash command (`cat`, `sed`, `head`…) or a `SKILL.md` path in a dispatched prompt count.
- Documentation numbers (B-005): "~64 core" → 47, `ENABLE_TOOL_SEARCH=auto` → `true`,
  "8 hooks" → 9, "13 rules" → 14, "169 skills" → 177, "8 MCP servers" → 1 global + per-project
  stacks, "770+ skills" removed, the README's "~12K-token base" replaced by the measured method,
  "14 always-on rules" qualified as Cursor-only, and the root `CLAUDE.md` no longer says there is
  no test suite.

### Added (stage 3 — the deploy has a memory)
- **`scripts/osforge-state.py` + `~/.osforge/install-state.json`** (B-014, E-A27–E-A30): every
  file the deploy writes is recorded with its SHA-256, every managed hook entry by id
  (`event|matcher|script`), every settings key with its previous value, every MCP server it
  added. `deploy.sh` now *enqueues* what it wants to write and `osforge-state.py apply` decides
  per file: missing → copy; recorded and untouched → update; recorded and **edited by you** →
  keep yours, back it up to `~/.claude_backups/<run>/`, warn (`--force` overwrites); not
  recorded and different → **yours, skipped** (`--adopt` takes over, with backup); identical to
  an older git revision of the repo → legacy install, updated. Absent from the repo → removed
  only if still byte-identical to what was installed, and only under the roots this run deployed
  (`--claude-only` never prunes `~/.cursor`). No `rsync --delete` anywhere on this path.
- **Hooks merged by id, three-way** (B-015): your hook entries in `settings.json` — including
  the ones under `~/.claude/hooks/` — are never touched; a managed entry you edited aborts the
  deploy with both versions (`--force-hooks`); an event the repo dropped disappears; the file is
  written atomically and only when something changed. Same for `settings-base.json` and
  `~/.claude.json` (MCPs): no more timestamped backup on every run.
- **`--doctor`, `--uninstall [--dry-run]`, `--restore=<run_id>`** (B-016): doctor exits 1 and
  lists missing/edited files and drifted hooks; uninstall removes only what OSForge installed
  and you did not edit, drops the managed hook entries, restores the settings keys it had set,
  removes the MCP servers it had added, keeps your data; restore copies a run's backups back.
  `hooks/validate.py` (a project template) is no longer deployed as a hook (E-A33).
- **`tests/test-deploy-lifecycle.sh`** (B-017): the real `deploy.sh` against a seeded temporary
  HOME (your hook, skill, `--global` skill, `CLAUDE.md`, settings/env/MCP, a legacy-installed
  hook) — 61 checks: nothing of yours is lost, second run byte-identical with no new backup,
  drift kept + backed up, `--force`/`--restore` round-trip, edited hook aborts, retired core skill
  removed while yours stay, uninstall leaves only your files, dry-run on an empty HOME creates
  nothing. Runs in CI (not in the deploy preflight: ~1 min).
- `OSFORGE_DEPLOY_LEGACY=1` keeps the previous copy/rsync path for one release.

### Added (stage 3 — session continuity)
- **One project identity for every hook** (B-018, E-A19, E-A20, E-A26): `hooks/lib/project_id.py`
  resolves `OSFORGE_PROJECT` → registered git root (subdirectories and worktrees included) →
  remote hash (ssh/https spellings, credentials stripped) → normalised basename. `osforge-db`
  gained `projects.root_path` / `remote_hash` (idempotent migration), `bind-project <slug>
  --root=. --remote=auto`, the same flags on `upsert-project`, both fields in
  `list-projects --json`, and finally honours `OSFORGE_DB`. `observe-capture`, `session-save`
  and `session-resume` all use the library; observations and resume land on the same key.
- **Guarded resume** (B-019, E-A14, E-A21–E-A24): `session-resume.sh` injects the resume
  inside an explicit *data, not instructions* envelope, capped at `OSFORGE_RESUME_MAX_CHARS`
  (1200), scrubbed by `hooks/lib/scrub.py`, plus the **open tasks of this project only** — the
  cross-project board is gone from satellite sessions. `session-save.py` reads the **end** of
  the transcript (last 4 MB, last 8 user messages) instead of the first 2000 lines and scrubs
  secrets before `set-resume`; `observe-capture.py` scrubs the Bash command before recording
  it. `search-hybrid --project` now filters the vector leg through the database, so a
  decision from another project no longer leaks in.
- **`tests/test-session-continuity.sh`** (35 checks, offline): same-name folders with
  different remotes → different slugs; subdirectory, worktree and re-spelled clone → same
  slug; injection text and a key stored in the resume come back as data / `[redacted:key]`;
  another project's task never appears; a 6000-line transcript yields the *last* messages; the
  vector filter goes red on the previous code (mock embeddings). In CI.

### Added (stage 3 — canvas feedback loop)
- **Stop hook drains Canvas feedback** (B-020, E-A43): `hooks/canvas-feedback.py` blocks the
  Stop once, with the content (decisions, checked items, form values, comment — scrubbed),
  when the user submitted feedback for an artifact of **this project** that the agent has not
  seen; delivery is recorded in `<data dir>/.delivered.json`, `stop_hook_active` is respected,
  a server that is down means pass, `OSFORGE_CANVAS_FEEDBACK=off` disables. Pattern from ECC's
  `plan-canvas-pending.js` (MIT), re-implemented for the OSForge data model. The skill's
  "read the file next turn" prose is now backed by the hook. 10 hooks.
- **Canvas server validates against the artifact** (E-A44): POST `/api/feedback/:id` now
  answers 404 for a missing artifact, 409 for a `revision` that is not the artifact's current
  one, 400 for a `revision` < 1, an unknown block, a response whose type differs from the
  block's, an unknown checklist item or form field, a `decision.action` outside
  approve|edit|reject or not offered by the block, or a required comment missing; 403 for a
  browser `Origin` that is not this loopback server (`null` included); 413 above 256 KB. Only
  the validated fields are persisted, with `receivedAt`.
- **`tests/test-canvas-feedback.sh`** (34 checks): the hook against a seeded data dir and a
  fake health endpoint (no Bun), then the real `server.ts` on a random port for every 4xx above
  and the real hook against it. Contract cases CC-49/CC-50; the contract runner now points the
  hook at a dead port and a sandbox DB so it never touches a live Canvas.

### Known defects (found by the audit, open until later stages ship)

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
