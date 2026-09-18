# CLAUDE.md

This file guides work **on the OSForge repo itself** (curating and deploying the config). It is **not** the
global session-instruction file — that is `claude-code/CLAUDE.md`, deployed to `~/.claude/CLAUDE.md`, which holds
the model/agent/skill **orchestration** the LLM follows in every session. Don't conflate the two: this file =
maintain the framework; `claude-code/CLAUDE.md` = how to behave in a session.

## What this repo is

OSForge is **not an application** — it is the source of truth for the user's global Claude Code (`~/.claude/`) and Cursor (`~/.cursor/`) configuration: **177 skills, 27 agents** (orchestrator + 26 specialists), **14 rules (deployed to Cursor), 9 `spec-*` commands, 1 global MCP server (Context7; the rest are per-project stacks in `mcp/stacks/`)**, 11 hooks, and the `osforge-db` SQLite state CLI (with local vector memory). There is no build or lint step; the offline test suite is `tests/` (see below) and the "build" is the deploy.

**ADR-001 (docs/DECISIONS.md): never edit `~/.claude/` or `~/.cursor/` directly.** All changes happen here, get committed, then deployed via `./deploy.sh`.

## Commands

```bash
./deploy.sh                  # Sync everything → ~/.claude/ and ~/.cursor/
./deploy.sh --dry-run        # Preview without changes
./deploy.sh --claude-only    # or --cursor-only
./deploy.sh --with-qdrant    # Provision vector memory (Qdrant via Docker, opt-in); --no-qdrant forces SQLite
./deploy.sh --doctor         # What drifted since the last deploy (state in ~/.osforge/install-state.json)
./deploy.sh --uninstall      # Remove only what OSForge installed; --restore=ID puts a run's backups back

# Regenerate skill indexes after adding/changing skills (expected by recent workflow):
python3 scripts/_extract_index.py       # → INDICE-SKILLS.json (scans all SKILL.md files)
python3 scripts/_generate_index_md.py   # → docs/INDICE-SKILLS.md (reads the JSON)

python3 scripts/_generate_manifest.py   # → MANIFEST block in claude-code/SKILLS.md (--check gates deploy)
python3 scripts/_generate_triggering_cases.py  # → scripts/skill-triggering-cases.generated.tsv (240 cases)

# Suítes offline (416 verificações; nenhuma toca o ~/.claude vivo, nenhuma gasta API):
./tests/test-assertions.sh              # Lógica de veredito dos harnesses de eval (60)
./tests/hooks/run-contracts.sh          # Contratos de hook: comandos reais × fixtures, dois harnesses (59; gate do deploy)
./tests/test-gateguard-grant.sh         # Ciclo de vida do grant do GateGuard + atenuação de negações (84)
./tests/test-deploy-lifecycle.sh        # Deploy com estado: nada seu se perde, idempotente, doctor/uninstall/restore (61; ~1 min; CI)
./tests/test-session-continuity.sh      # Uma identidade de projeto; resume com escopo, teto e limpeza (35)
./tests/test-canvas-feedback.sh         # Dreno do feedback do Canvas (Stop) + validação no servidor (34; parte do servidor precisa de bun)
./tests/test-scan-secrets.sh            # scan-secrets nos dois formatos de payload, repo git temporário (33)
./tests/test-context-usage.sh           # Aviso de contexto pelo uso real + tokens por sessão/projeto (27)
./tests/test-gateguard-sql.sh           # Detector de SQL destrutivo do GateGuard (23)

# Gates estáticos (rodam no preflight do deploy e no CI):
python3 scripts/_generate_manifest.py --check   # MANIFEST de claude-code/SKILLS.md em dia
python3 scripts/check-agents.py         # Frontmatter dos agentes: tools escalar, model no enum, papéis read-only
python3 scripts/check-counts.py         # Números citados em README/CLAUDE.md/USAGE batem com a árvore
python3 scripts/check-unicode.py        # Unicode invisível/bidi/tag no que chega ao contexto (--sources, --fix)

# Evals (consomem API; --dry lista e valida sem chamar modelo — é o que o CI roda):
./scripts/run-trigger-eval.sh --dry [--split eval]  # 15 skills × (5 positivas + 5 negativas)
./scripts/test-orchestrator-routing.sh --dry        # roteamento: agente, skill, tier
./scripts/test-skill-triggering.sh --dry            # triggering das skills core
#   rodada real: --model <id> --runs 3 [--home DIR] --report docs/evals/<data>-<modelo>-<suite>.md
#   PASS é k = N; 0 < k < N é FLAKY e reprova. Formato e pendências: docs/evals/README.md

python3 scripts/buscar-skill.py <query> # Search skills locally
python3 scripts/osforge-db.py --help    # State CLI (deployed as `osforge-db` in ~/.local/bin)
bun scripts/canvas/server.ts            # OSForge Canvas — local generative UI viewer (port 4242, see skills/osforge-canvas/)
```

Deploy behavior worth knowing:
- Removing a skill dir here removes it from `~/.claude/skills/` and `~/.cursor/skills/` on the next deploy — **only if the installed copy is still byte-identical to what the deploy wrote**. Your own skills, and anything installed with `install-skill --global`, are never deleted (there is no `rsync --delete` on this path any more).
- Hooks (`hooks/hooks-claude-code.json` → `~/.claude/settings.json`) merge **by id** (`event|matcher|script`), three-way: a managed entry still equal to what was recorded is replaced, one **you edited** aborts the deploy with both versions (`--force-hooks`), an event the repo dropped disappears, and your own entries — including under `~/.claude/hooks/` — are never touched. MCPs (`mcp/claude-code.json` → `~/.claude.json`) merge non-destructively (union). Deploy reports MCP drift between repo and live config.
- Backups go to `~/.claude_backups/<run_id>/<path relative to HOME>`, and only when something is actually overwritten or kept — an idempotent second run writes nothing and creates no backup. `./deploy.sh --restore=<run_id>` puts a run's backups back.
- Pre-flight gates (abort the deploy): manifest drift, `tests/hooks/run-contracts.sh`, `scripts/check-agents.py`, `scripts/check-counts.py`, `scripts/check-unicode.py`. CI (`.github/workflows/ci.yml`) runs the same set plus `bash -n`/`py_compile`, a dry-run deploy in an empty HOME and `tests/test-deploy-lifecycle.sh`.
- Evals: `--model` é obrigatório fora de `--dry`, cada caso roda `--runs` vezes (padrão 3) e o relatório vai para `docs/evals/` (`docs/evals/README.md` explica o formato e lista o que ainda é narrativa). PASS é `k = N`; `0 < k < N` é FLAKY e reprova.
- The deploy keeps state (`scripts/osforge-state.py`, `~/.osforge/install-state.json`): it never overwrites a file you edited, never deletes a skill/hook of yours, and can `--doctor`/`--uninstall`/`--restore`. `OSFORGE_DEPLOY_LEGACY=1` = old path, one release.

## Architecture

### Deployed content (the product)
- `skills/` — One directory per skill, each with a `SKILL.md` (frontmatter: `name`, `description` with `Use when:` / `Keywords:` / `Do NOT use for:` triggers per `docs/SKILL-STANDARD.md`). Some skills have subdirectories with reference modules.
- `agents/` — One `.md` per agent. Exception: `agents/orchestrator/` is a directory; the deploy copies its `AGENT.md` to `agents/orchestrator.md` and its support files (`triage-rules*.md`, `plan-templates/`, `delegation-brief.md`) to `~/.claude/orchestrator/` — the paths the `AGENT.md` tells the model to load.
- `rules/` — `.mdc` files loaded as Cursor always-on global rules (Claude Code equivalents live inside `claude-code/CLAUDE.md`).
- `commands/` — `spec-*.md` slash commands. Unified spec system (ADR-003): commands are the execution interface; the `tlc-spec-driven` skill holds templates. Both operate on `.specs/` in target projects.
- `hooks/` — 11 shell/Python hook scripts (`canvas-autostart`, `session-resume`, `session-save`, `observe-capture`, `protect-tests`, `scan-secrets`, `gateguard`, `route-guard`, `notify-done`, `canvas-feedback`, `context-threshold`) + `hooks/lib/` (shared: `project_id.py` resolves one project identity for every hook, `scrub.py` removes secrets from anything persisted or re-injected) + two configs: `hooks-claude-code.json` (Claude Code → settings.json) and `hooks.json` (Cursor, absolute `$HOME/.cursor/hooks/` paths per ADR-006). `hooks/validate.py` is a project template, not a hook, and is not deployed. Output contract: `docs/HOOKS.md`.
- `claude-code/CLAUDE.md` and `claude-code/SKILLS.md` — deployed as `~/.claude/CLAUDE.md` and `~/.claude/SKILLS.md`. `SKILLS.md` has two halves: a hand-written **spine** (global rules + the always-active disciplines) and a generated **MANIFEST** between `<!-- MANIFEST:START/END -->` markers, holding one line per non-core skill. Edit the spine by hand; regenerate the manifest with `scripts/_generate_manifest.py`. A skill outside both the core allowlist and the manifest does not exist at runtime.
- `claude-code/skills-core.txt` — the Model A allowlist: the only skills `deploy.sh` copies to `~/.claude/skills` (and `~/.cursor/skills`). Everything else is pulled per project via `scripts/install-skill.sh`. `--all-skills` restores the old deploy-everything behavior.
- `mcp/claude-code.json` — MCP server definitions.
- `scripts/osforge-db.py` — deployed to `~/.local/bin/osforge-db`; SQLite state at `~/.osforge/osforge.db` (global) or `.osforge/osforge.db` (per-project via `--scope=local`). Tracks projects, phases, tasks (`wave`/`depends_on` for parallel dispatch), decisions (FTS5), blockers; `board` = cross-project view. Also: **local vector memory** (`embed`, `embed-backfill`, `search-semantic`, `search-hybrid`, `vec-init`, `vec-status`; 3-tier Qdrant→SQLite→FTS5 selected via `~/.osforge/config.json`) and **observations/instincts** feeding `evolve`.
- `scripts/qdrant/` — `docker-compose.yml` (pinned `qdrant/qdrant:v1.18.2`, persistent volume at `~/.osforge/qdrant/storage`) + README for the opt-in vector backend. Provisioned by `./deploy.sh --with-qdrant`.
- `scripts/canvas/` — OSForge Canvas: local generative-UI service (single-file Bun server + single-file viewer, zero deps). Claude writes JSON artifacts to `<cwd>/outputs/canvas/artifacts/`, the viewer renders them as interactive UI (SSE live-reload), feedback lands in `outputs/canvas/feedback/` (runtime scratch, gitignored). Schema: `skills/osforge-canvas/references/schema.md`.

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
