# CLAUDE.md

This file guides work **on the OSForge repo itself** (curating and deploying the config). It is **not** the
global session-instruction file — that is `claude-code/CLAUDE.md`, deployed to `~/.claude/CLAUDE.md`, which holds
the model/agent/skill **orchestration** the LLM follows in every session. Don't conflate the two: this file =
maintain the framework; `claude-code/CLAUDE.md` = how to behave in a session.

## What this repo is

OSForge is **not an application** — it is the source of truth for the user's global Claude Code (`~/.claude/`) and Cursor (`~/.cursor/`) configuration: **177 skills, 25 agents** (orchestrator + 24 specialists), **14 rules (deployed to Cursor), 9 `spec-*` commands, 1 global MCP server (Context7; the rest are per-project stacks in `mcp/stacks/`)**, 13 hooks, and the `osforge-db` SQLite state CLI (with local vector memory). There is no build or lint step; the offline test suite is `tests/` (see below) and the "build" is the deploy.

**ADR-001 (docs/DECISIONS.md): never edit `~/.claude/` or `~/.cursor/` directly.** All changes happen here, get committed, then deployed via `./deploy.sh`.

## Commands

```bash
./deploy.sh                  # Sync everything → ~/.claude/ and ~/.cursor/
./deploy.sh --dry-run        # Preview without changes (also prints the deploy-source guard verdict)
./deploy.sh --release        # Fetch tags, deploy the latest v* tag from a detached worktree in ~/.osforge/release/ (ADR-018)
./deploy.sh --force-branch   # Bypass the guard (needs: main + clean tree + HEAD at a v* tag); or OSFORGE_DEPLOY_FORCE_BRANCH=1
scripts/release.sh 5.3.0     # Release PR: bump VERSION, date CHANGELOG [Unreleased], branch release/x.y.z (--no-pr); CI tags after merge
./deploy.sh --claude-only    # or --cursor-only
./deploy.sh --with-qdrant    # Provision vector memory (Qdrant via Docker, opt-in); --no-qdrant forces SQLite
./deploy.sh --doctor         # What drifted since the last deploy (state in ~/.osforge/install-state.json)
./deploy.sh --uninstall      # Remove only what OSForge installed; --restore=ID puts a run's backups back

# Regenerate skill indexes after adding/changing skills (expected by recent workflow):
python3 scripts/_extract_index.py       # → INDICE-SKILLS.json (scans all SKILL.md files)
python3 scripts/_generate_index_md.py   # → docs/INDICE-SKILLS.md (reads the JSON)

python3 scripts/_generate_manifest.py   # → MANIFEST block in claude-code/SKILLS.md (--check gates deploy)
python3 scripts/_generate_triggering_cases.py  # → scripts/skill-triggering-cases.generated.tsv (240 cases)

# Offline suites (1059 checks; none touches the live ~/.claude, none spends API):
./tests/test-assertions.sh              # Verdict logic of the eval harnesses (67)
./tests/hooks/run-contracts.sh          # Hook contracts: real commands × fixtures, both harnesses (77; deploy gate)
./tests/test-gateguard-grant.sh         # GateGuard grant lifecycle + denial attenuation (84)
./tests/test-deploy-lifecycle.sh        # Stateful deploy: nothing of yours is lost, idempotent, doctor/uninstall/restore, brain steps, no legacy embed-backfill, deploy-source guard + --release (96; ~1 min; CI)
./tests/test-session-continuity.sh      # One project identity; scoped resume, cap, cleanup and memory hint (40)
./tests/test-canvas-feedback.sh         # Canvas feedback drain (Stop) + server-side validation (34; the server part needs bun)
./tests/test-scan-secrets.sh            # scan-secrets on both payload formats, temporary git repo (33)
./tests/test-context-usage.sh           # Context warning from real usage + tokens per session/project (27)
./tests/test-gateguard-sql.sh           # GateGuard destructive-SQL detector (23)
./tests/test-installers.sh              # install-skill/install-mcp: the helpers that run on YOUR machine (22)
./tests/test-judge.sh                   # Isolated judge: argv/env/isolation/exit codes with a fake claude (81)
./tests/test-quality-guard.sh           # quality-guard (B-035): callers left open, duplicates, tests state, shadow/on/off, p95 budget, signals CLI (46)
./tests/test-monitor.sh                 # Monitor (B-036): contract numbers vs hand count, --discover, quality block, read-only, budget; /monitor page + /api/monitor, Host/Origin, SSE without reload loop, optional browser smoke; command centre: groups, live detection, inbox, runs, server actions with fake open/claude (108; the server part needs bun)
./tests/test-inbox.sh                   # inbox-deliver (B-041): panel messages reach the running agent once, subagents skipped, fast path even with messages pending elsewhere, 8k cap, gateguard blocks agents writing to it (26)
./tests/test-outcome-r3.sh              # Outcome eval r3 (Pacote 02): builds offline, --dry plans 396/288 calls, r1/r2 byte-identical (35)
./tests/test-eval-cases.sh              # Eval cases v2: category, criticals, orphans fail --dry (42)
./tests/test-trigger-detect.sh          # Trigger eval counts the real skill (not just the clone) and runs outside the repo (3)
./tests/test-quota.sh                   # quota.json: writes (statusline + harness streams), freshness, 80/95% warning once per band (37)
./tests/test-calls.sh                   # calls table: ingestion, derived cost, retention, backfill (26)
./tests/test-harness-quota.sh           # Harness stops on quota: NOT RUN, exit 75, quota_at_start/end, records the stream (20)
./tests/test-memory-recall.sh           # osforge-db memory: OR-FTS, accents + migration, --since/--until, coverage, degraded note, eval floor (53)
./tests/test-brain.sh                   # Brain (ADR-017): journal before upsert, scrub, remember/recall/forget, filters, migrate, rebuild, degraded fallback (79; the 39 store checks need qdrant-client via OSFORGE_TEST_BRAIN_PYTHON, else SKIP)

# Static gates (run in the deploy preflight and in CI):
python3 scripts/_generate_manifest.py --check   # MANIFEST in claude-code/SKILLS.md is current
python3 scripts/check-agents.py         # Agent frontmatter: scalar tools, model in the enum, read-only roles
python3 scripts/check-counts.py         # Numbers quoted in README/CLAUDE.md/USAGE match the tree
python3 scripts/check-unicode.py        # Invisible/bidi/tag Unicode in what reaches the context (--sources, --fix)
python3 scripts/check-portability.py    # bash 4+ / GNU-only in what gets deployed — `bash -n` does not catch it

# Evals (spend API; --dry lists and validates without calling a model — that is what CI runs):
./scripts/run-trigger-eval.sh --dry [--split eval]  # 15 skills × (5 positive + 5 negative)
./scripts/test-orchestrator-routing.sh --dry        # routing: agent, skill, tier
./scripts/test-skill-triggering.sh --dry            # core-skill triggering
#   real run: --model <id> --runs 3 [--home DIR] --report docs/evals/<date>-<model>-<suite>.md
#   PASS is k = N; 0 < k < N is FLAKY and fails. Format and open items: docs/evals/README.md

python3 scripts/buscar-skill.py <query> # Search skills locally
python3 scripts/osforge-db.py --help    # State CLI (deployed as `osforge-db` in ~/.local/bin)
bun scripts/canvas/server.ts            # OSForge Canvas — local generative UI viewer (port 4242, see skills/osforge-canvas/); /monitor = portfolio of projects (B-036)
```

Deploy behavior worth knowing:
- **Deploy-source guard (ADR-018):** from a git checkout, `./deploy.sh` refuses unless the branch is `main`, the tree is clean and HEAD is exactly at a `v*` tag — use `--release` (any branch) or `--force-branch`. `--doctor`/`--uninstall`/`--restore` are not guarded. `.github/workflows/release.yml` tags `v$VERSION` and publishes the GitHub Release when a VERSION bump reaches `main` with green CI.
- Removing a skill dir here removes it from `~/.claude/skills/` and `~/.cursor/skills/` on the next deploy — **only if the installed copy is still byte-identical to what the deploy wrote**. Your own skills, and anything installed with `install-skill --global`, are never deleted (there is no `rsync --delete` on this path any more).
- Hooks (`hooks/hooks-claude-code.json` → `~/.claude/settings.json`) merge **by id** (`event|matcher|script`), three-way: a managed entry still equal to what was recorded is replaced, one **you edited** aborts the deploy with both versions (`--force-hooks`), an event the repo dropped disappears, and your own entries — including under `~/.claude/hooks/` — are never touched. MCPs (`mcp/claude-code.json` → `~/.claude.json`) merge non-destructively (union). Deploy reports MCP drift between repo and live config.
- Backups go to `~/.claude_backups/<run_id>/<path relative to HOME>`, and only when something is actually overwritten or kept — an idempotent second run writes nothing and creates no backup. `./deploy.sh --restore=<run_id>` puts a run's backups back.
- Pre-flight gates (abort the deploy): manifest drift, `tests/hooks/run-contracts.sh`, `scripts/check-agents.py`, `scripts/check-counts.py`, `scripts/check-unicode.py`, `scripts/check-portability.py`. CI (`.github/workflows/ci.yml`) runs the same set plus `bash -n`/`py_compile`, a dry-run deploy in an empty HOME and `tests/test-deploy-lifecycle.sh`.
- Evals: `--model` is required outside `--dry`, each case runs `--runs` times (default 3) and the report goes to `docs/evals/` (`docs/evals/README.md` explains the format and lists what is still narrative). PASS is `k = N`; `0 < k < N` is FLAKY and fails.
- The deploy keeps state (`scripts/osforge-state.py`, `~/.osforge/install-state.json`): it never overwrites a file you edited, never deletes a skill/hook of yours, and can `--doctor`/`--uninstall`/`--restore`. `OSFORGE_DEPLOY_LEGACY=1` = old path, one release.

## Architecture

### Deployed content (the product)
- `skills/` — One directory per skill, each with a `SKILL.md` (frontmatter: `name`, `description` with `Use when:` / `Keywords:` / `Do NOT use for:` triggers per `docs/SKILL-STANDARD.md`). Some skills have subdirectories with reference modules.
- `agents/` — One `.md` per agent. Exception: `agents/orchestrator/` is a directory; the deploy copies its `AGENT.md` to `agents/orchestrator.md` and its support files (`triage-rules*.md`, `plan-templates/`, `delegation-brief.md`) to `~/.claude/orchestrator/` — the paths the `AGENT.md` tells the model to load.
- `rules/` — `.mdc` files loaded as Cursor always-on global rules (Claude Code equivalents live inside `claude-code/CLAUDE.md`).
- `commands/` — `spec-*.md` slash commands. Unified spec system (ADR-003): commands are the execution interface; the `tlc-spec-driven` skill holds templates. Both operate on `.specs/` in target projects.
- `hooks/` — 13 shell/Python hook scripts (`canvas-autostart`, `session-resume`, `session-save`, `observe-capture`, `protect-tests`, `scan-secrets`, `gateguard`, `route-guard`, `notify-done`, `canvas-feedback`, `context-threshold`, `quality-guard`, `inbox-deliver`) + `hooks/lib/` (shared: `project_id.py` resolves one project identity for every hook, `scrub.py` removes secrets from anything persisted or re-injected, `defs.py` exported definitions and callers for `quality-guard`) + two configs: `hooks-claude-code.json` (Claude Code → settings.json) and `hooks.json` (Cursor, absolute `$HOME/.cursor/hooks/` paths per ADR-006). `hooks/validate.py` is a project template, not a hook, and is not deployed. Output contract: `docs/HOOKS.md`.
- `claude-code/CLAUDE.md` and `claude-code/SKILLS.md` — deployed as `~/.claude/CLAUDE.md` and `~/.claude/SKILLS.md`. `SKILLS.md` has two halves: a hand-written **spine** (global rules + the always-active disciplines) and a generated **MANIFEST** between `<!-- MANIFEST:START/END -->` markers, holding one line per non-core skill. Edit the spine by hand; regenerate the manifest with `scripts/_generate_manifest.py`. A skill outside both the core allowlist and the manifest does not exist at runtime.
- `claude-code/skills-core.txt` — the Model A allowlist: the only skills `deploy.sh` copies to `~/.claude/skills` (and `~/.cursor/skills`). Everything else is pulled per project via `scripts/install-skill.sh`. `--all-skills` restores the old deploy-everything behavior.
- `mcp/claude-code.json` — MCP server definitions.
- `scripts/osforge-db.py` — deployed to `~/.local/bin/osforge-db`; SQLite state at `~/.osforge/osforge.db` (global) or `.osforge/osforge.db` (per-project via `--scope=local`). Tracks projects, phases, tasks (`wave`/`depends_on` for parallel dispatch), decisions (FTS5), blockers; `board` = cross-project view. Also: **local vector memory** (`embed`, `embed-backfill`, `search-semantic`, `search-hybrid`, `vec-init`, `vec-status`; 3-tier Qdrant→SQLite→FTS5 selected via `~/.osforge/config.json`) and **observations/instincts** feeding `evolve`.
- `scripts/osforge_brain.py` — the **brain** (ADR-017), deployed next to `osforge-db` in `~/.local/bin`: long-term memory (`remember`/`recall`/`forget`/`brain *`) in Qdrant collection `osforge_brain` (dense embeddinggemma-300m via fastembed + sparse BM25), journal `~/.osforge/brain.jsonl` as source of truth. Stdlib side imported by `osforge-db`; heavy side runs in `~/.osforge/venv` (created by `deploy.sh`, `--no-brain` skips). The SQLite side is the **workbench**.
- `scripts/qdrant/` — `docker-compose.yml` (pinned `qdrant/qdrant:v1.18.2`, persistent volume at `~/.osforge/qdrant/storage`) + README for the opt-in vector backend. Provisioned by `./deploy.sh --with-qdrant`.
- `scripts/canvas/` — OSForge Canvas: local generative-UI service (single-file Bun server + single-file viewer, zero deps). Claude writes JSON artifacts to `<cwd>/outputs/canvas/artifacts/`, the viewer renders them as interactive UI (SSE live-reload), feedback lands in `outputs/canvas/feedback/` (runtime scratch, gitignored). Schema: `skills/osforge-canvas/references/schema.md`. The same server serves `/monitor` (`monitor.html`, layout adapted from Ponytail's board, MIT) with `/api/monitor` → `osforge-db monitor` (read-only portfolio of every project + the selected project's detail; B-036, ADR-019).

### Source material (not deployed, gitignored)
- `sources/01-anthropic/` … `sources/13-claude-red/` — vendored upstream skill collections, the raw curation sources (Anthropic, superpowers, Vercel, Trail of Bits, Supabase, Expo, Cloudflare, Sentry, Claude-Red, etc.). Disk-only (ADR-009).
- `sources/_taste-skill-source/` — taste-skill upstream from Leonxlnx/taste-skill; OSForge enhancement layers compose on top, never replace it.
- `docs/` — `DECISIONS.md` (ADRs — read before structural changes), `EXAMPLES.md`, `AGENT_FLOW.md`, `INDICE-SKILLS.md` (generated).
- `INDICE-SKILLS.json` (root) — generated skill index; regenerate, don't hand-edit.

## Workflow for changes

1. Adding/editing a skill: start from `docs/SKILL.template.md` and follow `docs/SKILL-STANDARD.md` — `Use when:` / `Keywords:` / `Do NOT use for:` triggers, the invocation axis, and a checkable body → regenerate indexes (`_extract_index.py`, `_generate_index_md.py`, `_generate_manifest.py`) → validate with `scripts/test-skill-triggering.sh` → `./deploy.sh`. The `SKILLS.md` manifest is **generated, never hand-edited**; `deploy.sh` aborts if it drifts. Deciding a skill is core (always native) is a separate call: add it to `claude-code/skills-core.txt`.
2. Curating from upstream: source lives in the numbered dirs; the converted/curated version goes in `skills/`. Don't deploy source dirs.
3. Architectural decisions about the framework itself get an ADR in `docs/DECISIONS.md`.
4. Language (ADR-011): all repo content (skills, agents, rules, `CLAUDE.md`, `SKILLS.md`, commands, ADRs, comments) is authored in **English**. At runtime the agent replies in the user's language. Legacy pt-BR skills are migrated to English in harness-validated batches (see `docs/SKILL-STANDARD.md` §5.A).

## Multi-project operation

OSForge itself is intended to be the **hub session**: open it when planning, reviewing portfolio state, or writing specs — never for executing code that lives in another repo. Each target project gets its own **satellite session** opened in its own directory. At session start, the satellite loads context with `osforge-db resume <slug>` (~50 tokens); at session end it saves progress with `osforge-db set-resume <slug> "..."` and `osforge-db set-task <slug> <id> done`. The hub registers work via `osforge-db add-task` and monitors all projects via `osforge-db board`. One session → one working directory; mixing projects in a single session pollutes context, duplicates permission prompts, and degrades resume accuracy. See **USAGE.md → Multi-project operation** for the full pattern, commands, and a worked example.
