# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

OSForge is **not an application** — it is the source of truth for the user's global Claude Code (`~/.claude/`) and Cursor (`~/.cursor/`) configuration: ~153 curated skills, 26 agents, 13 always-on rules, 9 `spec-*` commands, hooks, MCP config, and the `osforge-db` SQLite state CLI. There is no build, lint, or test suite. The "build" is the deploy.

**ADR-001 (docs/DECISIONS.md): never edit `~/.claude/` or `~/.cursor/` directly.** All changes happen here, get committed, then deployed via `./deploy.sh`.

## Commands

```bash
./deploy.sh                  # Sync everything → ~/.claude/ and ~/.cursor/
./deploy.sh --dry-run        # Preview without changes
./deploy.sh --claude-only    # or --cursor-only

# Regenerate skill indexes after adding/changing skills (expected by recent workflow):
python3 scripts/_extract_index.py       # → INDICE-SKILLS.json (scans all SKILL.md files)
python3 scripts/_generate_index_md.py   # → docs/INDICE-SKILLS.md (reads the JSON)

python3 scripts/buscar-skill.py <query> # Search skills locally
python3 scripts/osforge-db.py --help    # State CLI (deployed as `osforge-db` in ~/.local/bin)
bun scripts/canvas/server.ts            # OSForge Canvas — local generative UI viewer (port 4242, see skills/osforge-canvas/)
```

Deploy behavior worth knowing:
- `skills/` is synced with `rsync --delete` — removing a skill dir here removes it from `~/.claude/skills/` and `~/.cursor/skills/` on next deploy.
- Hooks (`hooks/hooks-claude-code.json` → `~/.claude/settings.json`) and MCPs (`mcp/claude-code.json` → `~/.claude.json`) are merged **non-destructively** (union; existing user entries preserved). Deploy reports MCP drift between repo and live config.
- Critical files are backed up to `~/.claude_backups/` before overwrite.

## Architecture

### Deployed content (the product)
- `skills/` — One directory per skill, each with a `SKILL.md` (frontmatter: `name`, `description` with `ACIONE quando:` trigger phrases). Some skills have subdirectories with reference modules.
- `agents/` — One `.md` per agent. Exception: `agents/orchestrator/` is a directory; deploy copies its `AGENT.md` to `agents/orchestrator.md`.
- `rules/` — `.mdc` files loaded as Cursor always-on global rules (Claude Code equivalents live inside `claude-code/CLAUDE.md`).
- `commands/` — `spec-*.md` slash commands. Unified spec system (ADR-003): commands are the execution interface; the `tlc-spec-driven` skill holds templates. Both operate on `.specs/` in target projects.
- `hooks/` — Shell/Python hook scripts + two configs: `hooks-claude-code.json` (Claude Code, merged into settings.json) and `hooks.json` (Cursor, absolute `$HOME/.cursor/hooks/` paths per ADR-006).
- `claude-code/CLAUDE.md` and `claude-code/SKILLS.md` — deployed as `~/.claude/CLAUDE.md` and `~/.claude/SKILLS.md`. **To change the user's global instructions or the on-demand skills index, edit these files here.** `SKILLS.md` is the trigger index loaded into every session — a new skill is only discoverable after being added to it.
- `mcp/claude-code.json` — MCP server definitions.
- `scripts/osforge-db.py` — deployed to `~/.local/bin/osforge-db`; SQLite state at `~/.osforge/osforge.db` (global) or `.osforge/osforge.db` (per-project via `--scope=local`). Tracks projects, phases, tasks (`wave`/`depends_on` for parallel dispatch), decisions (FTS5), blockers; `board` = cross-project view.
- `scripts/canvas/` — OSForge Canvas: local generative-UI service (single-file Bun server + single-file viewer, zero deps). Claude writes JSON artifacts to `<cwd>/outputs/canvas/artifacts/`, the viewer renders them as interactive UI (SSE live-reload), feedback lands in `outputs/canvas/feedback/` (runtime scratch, gitignored). Schema: `skills/osforge-canvas/references/schema.md`.

### Source material (not deployed, gitignored)
- `sources/01-anthropic/` … `sources/13-claude-red/` — vendored upstream skill collections, the raw curation sources (Anthropic, superpowers, Vercel, Trail of Bits, Supabase, Expo, Cloudflare, Sentry, Claude-Red, etc.). Disk-only (ADR-009).
- `sources/_taste-skill-source/` — taste-skill upstream from Leonxlnx/taste-skill; OSForge enhancement layers compose on top, never replace it.
- `docs/` — `DECISIONS.md` (ADRs — read before structural changes), `EXAMPLES.md`, `AGENT_FLOW.md`, `INDICE-SKILLS.md` (generated).
- `INDICE-SKILLS.json` (root) — generated skill index; regenerate, don't hand-edit.

## Workflow for changes

1. Adding/editing a skill: create/edit `skills/<name>/SKILL.md` with proper frontmatter and `ACIONE quando:` triggers → add/update its row in `claude-code/SKILLS.md` → regenerate indexes → `./deploy.sh`.
2. Curating from upstream: source lives in the numbered dirs; the converted/curated version goes in `skills/`. Don't deploy source dirs.
3. Architectural decisions about the framework itself get an ADR in `docs/DECISIONS.md`.
4. Skill/agent/rule prose is largely Portuguese (pt-BR) with English technical terms — match that.

## Multi-project operation

OSForge itself is intended to be the **hub session**: open it when planning, reviewing portfolio state, or writing specs — never for executing code that lives in another repo. Each target project gets its own **satellite session** opened in its own directory. At session start, the satellite loads context with `osforge-db resume <slug>` (~50 tokens); at session end it saves progress with `osforge-db set-resume <slug> "..."` and `osforge-db set-task <slug> <id> done`. The hub registers work via `osforge-db add-task` and monitors all projects via `osforge-db board`. One session → one working directory; mixing projects in a single session pollutes context, duplicates permission prompts, and degrades resume accuracy. See **USAGE.md §10** for the full pattern, commands, and a worked example.
