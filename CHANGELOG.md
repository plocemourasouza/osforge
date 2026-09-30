# Changelog

All notable changes to OSForge are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/). Architectural decisions are the ADRs in
`docs/DECISIONS.md`; this file records *what shipped*, the ADRs record *why*.

`VERSION` holds the current version; `deploy.sh` prints it. Releases are annotated git tags
(`vX.Y.Z`) with a GitHub Release carrying the matching section of this file.

## [Unreleased]

## [5.2.0] — 2026-09-29

Pacote 01 — quality and control before the first paid eval run (ADR-016, B-025–B-029).

### Added
- **Eval cases v2** (B-025): every trigger case carries `category` (`positivo` / `vizinho` /
  `irrelevante` / `negacao`) and `critical`; reports aggregate by category. 20 new cases,
  negation 2 → 15 (150 → 170; split `eval` 73). Routing cases mark the mandatory-dispatch
  (`!`) ones as critical; `expect_route` stays informative. `--dry` now fails on an orphan
  (missing skill) or malformed case instead of letting a paid run find it.
  `scripts/migrate-trigger-v2.py` did the one-off migration. `tests/test-eval-cases.sh` (39).
- **Harness respects the quota** (B-026): a quota rejection mid-run stops the harness; the
  remaining cases are reported `NOT RUN`, exit is 75, and the report records
  `quota_at_start`/`quota_at_end`. It also stops before the next block when the 5-hour window
  is past `OSFORGE_EVAL_QUOTA_STOP` (default 85). `tests/test-harness-quota.sh` (15).
- **Quota warning to the model** (B-027): `context-threshold` warns at 80% / 95% of the 5-hour
  window, once per band per window, and once per rejection (`OSFORGE_QUOTA_BANDS`,
  `OSFORGE_QUOTA_THRESHOLD=off`). Source is `~/.osforge/quota.json`, written by
  `hooks/quota-record.py` from one optional line in the user's own statusline script, and by
  `session-save` when the transcript holds a rejection. Hook count stays 11.
  `tests/test-quota.sh` (30).
- **Per-call audit** (B-028): `calls` table in `osforge-db` (`add-calls`, `calls`,
  `backfill-calls`, `prune-calls --older-than=90d`), main session and subagents. API-equivalent
  cost is derived at query time from the dated `claude-code/pricing.json` (deployed to
  `~/.claude/pricing.json`), never stored. `tests/test-calls.sh` (26).
- **Isolated judge** (B-029): `scripts/lib/judge.py` — a model-based judge on the subscription
  (never `--bare`), no tools, no MCP, no user `CLAUDE.md`, empty cwd; isolation verified on
  every call from `system/init`; structured verdict against a JSON schema; exit 75 on quota.
  Rubrics/fixtures in `scripts/evals/judge/`. Offline contract `tests/test-judge.sh` (77);
  E-J0 passed 4/4 on claude-sonnet-5 (2026-09-29); it showed `--json-schema` exposes a
  synthetic `StructuredOutput` tool, now the one tool the isolation check tolerates.
- **ADR-016** — the package's decision record.

### Fixed
- **Suite verdict ignored `ERROR`**: a run where every case errored (not logged in, API
  down) reported the suite as PASS. `suite_verdict` now returns INCOMPLETE (exit 2) when any
  case is ERROR and nothing measured failed. Found by the E1 pilot. `test-eval-cases` 39 → 42.
- **Trigger eval scored a real-skill call as a miss**: `run_eval.py` counted only its
  temporary clone `<skill>-skill-<uuid>`; a core skill is already native under the same
  description, so a model that invoked the real one failed every positive and passed every
  negative for free. `is_skill_trigger` now accepts clone and real skill in both the stream and
  the fallback path. The harness also ran `claude -p` from the OSForge repo, whose hub-session
  rules answered the query before any skill was considered; it now runs from a neutral temporary
  project. Found by the E1 trigger pilot (0/15). `tests/test-trigger-detect.sh` (3).
- **Case verdict `ERROR` masked measured misses**: `0 hits · 2 completed misses · 1 error` was
  ERROR (→ suite INCOMPLETE) instead of FAIL. `case_verdict` in `harness-assertions.sh`, shared
  by the routing and skill-triggering harnesses, returns ERROR only when no run was measured.
  E1 routing `r16`. `test-assertions` 60 → 67.
- **`db-state-sync` ran its own example on load**: the documented shell-injection example
  (`!` + backticked `osforge-db resume PROJECT_SLUG`) sat inside a fenced block, and the skill
  loader executes that syntax even there — every load ran `resume` for a literal `PROJECT_SLUG`.
  The example now spells the bang as `<BANG>`.

### Changed
- Offline suites: 441 → 644 checks; CI runs the six new suites.

## [5.1.0] — 2026-09-18

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

### Added (stage 4 — measured context and tokens)
- **Context Budget warning from real usage** (B-021, R-06): `hooks/context-threshold.py`
  (UserPromptSubmit) reads `message.usage` of the last assistant turn (input + cache_read +
  cache_creation) from the transcript tail and injects one warning per band per session —
  ≥120k "save state, finish the step", ≥150k "STOP, hand off, compact". ~1 ms on a 30 MB
  transcript. `OSFORGE_CONTEXT_BANDS`, `OSFORGE_CONTEXT_THRESHOLD=off`. The SKILLS.md
  "Context Budget" section now points at the hook instead of asking the model to guess. 11 hooks.
- **Tokens per session and project** (B-022, R-10): `osforge-db` table `usage` (upsert by
  project + session + model), `add-usage`, `usage <slug>`; totals in `board` (text and
  `--json`, whose per-project value is now `{tasks, usage}`) and `stats`. `session-save.py`
  computes them at Stop, once per `message.id` (the JSONL repeats a message per content block).
- **`tests/test-context-usage.sh`** (27 checks): 100k/125k/155k → 0/1/2 warnings, no repeat
  within a band, new session warns again, timing, guards; usage dedup by id, per-model split,
  upsert on repeated Stop, totals in board/stats. Contract case CC-14. In CI.

### Changed (stage 3/4 — small items)
- **Adversarial review without a quota** (B-004, E-A42): `adversarial-review` v1.2 drops "minimum
  of 10 issues" and "zero findings is suspicious"; adds the four-question pre-report gate, proof
  for Critical/Important, "zero findings is a valid result" with the list of areas worked, and a
  false-positive list. `code-reviewer` agent points at the gate. Textual adaptation from ECC's
  `agents/code-reviewer.md` (MIT) recorded in the new `THIRD_PARTY_NOTICES`, which also credits
  zunoworks/gateguard (via ECC) for the GateGuard design and mattpocock/skills. Experiment E4
  still measures whether the reviewer got lenient.
- **GateGuard attenuates repeated denials** (B-024/R-02): after three consecutive denials without
  a grant the message becomes one line with the ordinal (the full block repeated on every denial
  induced retry loops upstream); the count resets on a grant. 5 new cases in
  `tests/test-gateguard-grant.sh`.
- **Invisible-unicode check** (B-024/R-16): `scripts/check-unicode.py` (zero-width, bidi, variation
  selectors, Unicode Tag block, fillers, invisible math operators; `U+FE0F` after a pictograph or
  in a keycap is tolerated) in the deploy preflight and CI; `--sources` for the vendored tree,
  `--fix` to strip. Tree is clean.
- **Stack rules load by glob** (B-024/R-11): `nextjs-patterns`, `typescript-strict` and
  `code-style` are `alwaysApply: false` in Cursor; 11 rules stay always-on. `check-counts.py`
  checks both numbers. Bringing rules to Claude Code stays conditional on measuring `paths:`.
- **Orchestrator support files are deployed** (B-023/E-A40): `triage-rules*.md`,
  `plan-templates/` and `delegation-brief.md` go to `~/.claude/orchestrator/` (and
  `~/.cursor/orchestrator/`); `AGENT.md` cites those paths and uses `model: sonnet` instead of
  the non-schema `always-active` / `model-tier` keys. The proportional-plan change waits for E3.

### Added (stage 2 — evals that mean something)
- **Model and repetitions pinned** (B-010, E-A45): both harnesses now require `--model`
  outside `--dry`, run every case `--runs` times (default 3) and report **k of N**. PASS is
  `k = N`; `0 < k < N` is **FLAKY** and fails the suite — one run cannot tell "the skill
  triggers" from "it triggered once". New `--home DIR` (run against a clean deploy instead of
  the live `~/.claude`), `--dry` (list and validate, calling no model) and `--report`.
- **Verdict by block, not by line** (B-010): `scripts/lib/stream_assert.py` parses the
  stream-json and requires the tool name and the path to be in the **same `tool_use` block**.
  A message whose text quoted `skills/x/SKILL.md` while a `Read` in the same message opened
  another file used to count as "skill reached". New `check_agent_dispatched`: routing cases
  whose contract is delegation (heavy `offensive-*` skills) carry `!` in the agent column and
  accept only a real subagent dispatch — announcing `@penetration-tester` and answering alone
  is not delegating.
- **Trigger eval connected** (B-011, E-A46): `scripts/run-trigger-eval.sh` drives the
  `run_eval.py` that already shipped in `skill-creator` and that nothing ever called. 15 core
  skills × (5 positive + 5 negative) = 150 hand-written cases in `scripts/evals/trigger/`,
  each file carrying its 60/40 `tune`/`eval` split — a description tuned against the eval half
  is tuned to the test. `--dry` validates (5+5 minimum, unique ids, no query shared between
  skills, split covering every case) and prints the cost: 450 API calls for the whole suite,
  180 for the `eval` split, 30 for one skill. The paid run awaits explicit authorisation.
- **Results are versioned** (B-012): `docs/evals/README.md` + `scripts/lib/eval_report.py`,
  behind `--report` on all three suites: repo SHA and version (marking a dirty tree), model id,
  HOME, exact command, tokens summed from the streams (once per `message.id`), duration, and
  the k-of-N table with the flaky list broken out for E1. The four loose "measured" numbers
  (three in `claude-code/CLAUDE.md`, one in `hooks/route-guard.py`) now say they are from
  2026-08 and unversioned, and are tabled under **Pendentes de versionamento** with the command
  that redoes each one.
- `tests/test-assertions.sh`: 26 → **60** offline checks, covering block precision, dispatch,
  the model requirement, `--dry` with no `claude` on PATH at all, k-of-N aggregation with a
  mock that hits once in three, report contents, and case-file validation. CI dry-runs the
  three suites.

### Fixed (outside the backlog — found while preparing the first CI run)
- **A generated file could never be recognised as OSForge's own**, so on a legacy install
  `SKILLS.md` — the manifest that drives skill discovery — would have been skipped forever as
  "yours" and frozen at whatever the old deploy left. The installed copy is the repo file with
  `__OSFORGE_SKILLS_ROOT__` expanded to this machine's path, so it is byte-identical to no git
  revision at all. A manifest entry can now carry `subst`, the transformation the deploy
  applies when generating the file; the legacy check applies the same transformation to each
  historical blob before comparing. Caught on a real legacy install (`--dry-run` reported it as
  a user-owned collision); three new checks in `tests/test-deploy-lifecycle.sh` (64 now) go red
  without the fix. This is a regression of the state path against the old deploy, which
  overwrote unconditionally — the kind that only shows up against a machine with history.
- **CI would have failed on its first run**, on a file that is *supposed* to be invalid: the
  syntax step validated every `*.json`, including `tests/hooks/fixtures/claude-code/payload-garbage.json`,
  the deliberately malformed payload `run-contracts.sh` uses to prove the hooks fail open.
  The fixtures directory is now excluded, with the reason in the workflow.
- **The deploy no longer demands `rsync`** (B-003 added the check; B-014 removed the need).
  Nothing on the state path calls it any more — only the legacy path and the third-party
  Archify install do. A machine without `rsync` was refused even for `--dry-run`, which would
  not have written anything. Now: `python3` is required, `rsync` only under
  `OSFORGE_DEPLOY_LEGACY=1`, and its absence just skips Archify with a warning. Verified by
  running a real deploy with no `rsync` at all: 160 files, 47 core skills.
  `tests/test-deploy-lifecycle.sh` now always shadows `rsync` with a stub that fails, so the
  "was not called" assertion means something on a machine that has it (every CI runner does).
- **`install-skill` was broken on macOS** and nothing could have caught it: the script is
  deployed to `~/.local/bin` and is the on-demand half of Model A, but it used `mapfile`,
  a bash 4+ builtin that does not exist in the `/bin/bash` 3.2 shipped by macOS. `bash -n`
  only parses, so the CI syntax step, the deploy preflight and every existing test passed.
  Replaced with a portable read loop; `--list` also stopped creating an empty
  `.claude/skills` in whatever directory it was called from (a query should not write).
- **`scripts/check-portability.py`** (deploy preflight + CI) fails on bash 4+ builtins
  (`mapfile`, `readarray`, `declare -A`, `${v,,}`, case fallthrough) and GNU-only flags
  (`grep -P`, `stat -c`, `sed -i` without a suffix, `date -d`, `readlink -f`, `sha256sum`,
  `timeout`) in anything that runs on the user's machine, unless the line already degrades
  (`|| …`, `command -v`, `2>/dev/null`) or carries an explicit `# portable-ok: <reason>`.
- **`tests/test-installers.sh`** (22 checks): the two installers against temp projects —
  search, install in cwd / `--target` / `--global`, ambiguous and unknown terms, running
  from `~/.local/bin` via the `~/.osforge/repo-path` anchor, `OSFORGE_REPO` precedence, the
  `.mcp.json` merge preserving your own servers, and both scripts in a shell with the bash-4
  builtins disabled. Reintroducing the `mapfile` turns 3 of them red.
- **The first CI run reprovou o lifecycle nos dois runners — e não era o deploy.**
  `actions/checkout` clona raso (1 commit) e o caso "instalação legada de um arquivo
  GERADO" precisa de uma revisão anterior do arquivo. A guarda do teste comparava o arquivo
  já semeado (com a raiz expandida) com o do repo (ainda com o token): a substituição
  sozinha já os faz diferentes, então ela semeava o arquivo de hoje e o chamava de revisão
  antiga. Agora compara o blob antigo com o arquivo atual do repo e exige commits distintos
  — num clone raso os dois casos legados são pulados honestamente (60 ok), com histórico
  completo rodam (64 ok) — e o CI clona com `fetch-depth: 0`, para que o reconhecimento de
  instalação legada seja de fato exercitado lá.

### Still open from the audit
- **B-013 (E1, stability)** is ready to run and waits only on cost authorisation: pilot 6 API
  calls, routing 48, trigger `eval` split 180 (commands in `docs/BACKLOG-EVOLUCAO.md`).
- Proportional plan (B-023/E-A38) after E3; `~/.claude/rules/` after measuring `paths:` (R-11);
  GateGuard Edit/Write gate (E-A08) after E6; instincts loop (R-09) after E5.

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

[5.2.0]: https://github.com/plocemourasouza/osforge/releases/tag/v5.2.0
[5.1.0]: https://github.com/plocemourasouza/osforge/releases/tag/v5.1.0
[5.0.0]: https://github.com/plocemourasouza/osforge/releases/tag/v5.0.0
