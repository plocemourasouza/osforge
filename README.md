# 🔨 OSForge

[![Version](https://img.shields.io/badge/version-5.0.0-blue)](CHANGELOG.md) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![Archify](https://img.shields.io/badge/diagrams-Archify_v2.16.0-8A2BE2)](docs/ANALISE-ARCHIFY.md)

**An AI-powered development framework: skills, agents, rules, hooks, commands, and a full library of specialists — the single source of truth for your global Claude Code (`~/.claude/`) and Cursor (`~/.cursor/`) configuration.**

27 specialized agents · 177 on-demand skills · 14 rules (Cursor: 11 always-on, 3 stack rules by file glob) · 9 spec commands · zero-token Python hooks · local SQLite state with a cross-project task board · 121 business specialists · local generative UI. Tuned for **Next.js + TypeScript + Prisma + Supabase + Bun**, with coverage for mobile, game dev, Rust, Python, and more.

> *"Forging the development environment for AI-powered teams."*

🔍 **[ECC audit & evolution backlog → docs/ANALISE-COMPARATIVA-ECC.md](docs/ANALISE-COMPARATIVA-ECC.md)** · 📖 **[Usage guide → USAGE.md](USAGE.md)** · 🗒️ **[Changelog → CHANGELOG.md](CHANGELOG.md)** · 💡 **[Examples → docs/EXAMPLES.md](docs/EXAMPLES.md)** · 🧭 **[Skill standard → docs/SKILL-STANDARD.md](docs/SKILL-STANDARD.md)** · 🗺️ **[Decisions → docs/DECISIONS.md](docs/DECISIONS.md)**

---

## Table of contents

- [Why OSForge](#why-osforge)
- [Architecture](#architecture)
  - [Source of truth → deploy → runtimes](#1-source-of-truth--deploy--runtimes)
  - [Orchestration & the language boundary](#2-orchestration--the-language-boundary)
  - [The four routing layers](#3-the-four-routing-layers)
  - [Spec-driven workflow](#4-spec-driven-workflow)
- [Quick start](#quick-start)
- [What's inside](#whats-inside)
- [Language & authoring standard](#language--authoring-standard)
- [Stack compatibility](#stack-compatibility)
- [Origins](#origins)
- [License](#license)

---

## Why OSForge

AI coding agents are only as good as the context they receive. OSForge solves five problems:

1. **Context efficiency** — 177 skills reachable from a fixed base (≈21k tokens by bytes/4 over the deployed files: `CLAUDE.md`, `SKILLS.md`, `CONTEXT.md`, core descriptions, agent descriptions — measured baseline in `scripts/measure-context.py`). Everything else loads on demand.
2. **Stack-specific patterns** — skills tuned for Next.js App Router + Prisma + Supabase + shadcn/ui, with broad coverage for mobile, game dev, Rust, Python, and cross-platform.
3. **Built-in quality gates** — TDD enforcement, security auditing, red-team tactics, insecure-defaults detection, a Reality Check + Quality Control loop in every agent, and zero-token Python hooks.
4. **Local SQLite state** — `osforge-db` persists project state, decisions, blockers, and a task board (waves, dependencies, priorities) with a cross-project view. Session resume in ~50 tokens.
5. **Generative UI** — OSForge Canvas renders every spec and plan as an interactive browser artifact (cards, tables, dependency graphs, checklists, approve/edit/reject). No external APIs.

---

## Architecture

OSForge is **not an application** — it is a curated configuration that turns a stock AI coding agent into an orchestrated, stateful, quality-gated system. Four ideas hold it together: a **single source of truth** that deploys to your runtimes, an **orchestrator** that plans and delegates, a **language boundary** that keeps the internals English while you work in your own language, and a **local state layer** that remembers across sessions.

### 0. The system maps — diagrams with receipts

The repo ships its own maps, produced by the `system-diagrams` skill through the pinned Archify engine (dogfooding ADR-014). Each one is a typed JSON source, a delivered self-contained interactive HTML (search, focus, route tracing, guided views, live theme/preset switch, PNG/SVG export) and a receipt. Sources and receipt copies live in `docs/architecture/`; the `*.presentation.html` siblings are derived variants (sans-serif, softer corners — `scripts/archify-presentation.py`) and are **not** receipts.

**System map** — source of truth → deploy → runtime, the quality/state layer, the pinned engine.

![OSForge v5.0 — system map](docs/architecture/osforge.png)

> `architecture` · Archify v2.16.0 · signal-flow + trace · **9/9 checks · 0 errors · 0 warnings** · spec `1ddc…afa9` · artifact `8d69…aa97`

**Agents & skills** — the four routing layers, the 26 specialists in four groups, the Model A distribution of the 177 skills; full rosters in the cards.

![OSForge v5.0 — agents & skills](docs/architecture/osforge-agents-skills.png)

> `architecture` · Archify v2.16.0 · signal-flow + trace · **9/9 · 0 · 0** · spec `eb40…3c3f` · artifact `7e1f…359c`

**The spec-\* cycle** — swim-lanes for User, Orchestrator, specialist agents (waves), gates/state/artifacts and the Stop & recover lane; six phases, the Canvas checkpoints, the Archify receipt inside `/spec-design`, GateGuard and the user-confirmation grant.

![OSForge v5.0 — the spec-* cycle](docs/architecture/osforge-spec-cycle.png)

> `workflow` (schema v2) · Archify v2.16.0 · signal-flow + trace · **9/9 · 0 · 0** · spec `3012…64f0` · artifact `11fc…e4d4`

Regenerate any of them with `node ~/.claude/skills/archify/bin/archify.mjs deliver <type> docs/architecture/<name>.<type>.json docs/architecture/<name>.html --quality showcase --json`, then `python3 scripts/archify-presentation.py docs/architecture/<name>.html` for the presentation variant.

### 1. Source of truth → deploy → runtimes

The repo is authoritative. Nothing is edited in `~/.claude/` directly (ADR-001); changes are committed here and pushed out by `./deploy.sh`.

```mermaid
flowchart LR
  subgraph REPO["OSForge repo — single source of truth"]
    direction TB
    SK["177 skills"]
    AG["27 agents"]
    RU["14 rules"]
    CM["9 spec commands"]
    HK["11 hooks"]
    MC["1 global MCP + per-project stacks"]
    DBCLI["osforge-db CLI"]
  end
  REPO -->|"./deploy.sh (com estado: nada seu é sobrescrito)"| HOME["~/.claude/ + ~/.cursor/"]
  HOME --> CC["Claude Code"]
  HOME --> CU["Cursor"]
  DBCLI -->|"~/.local/bin"| STATE[("~/.osforge/osforge.db<br/>SQLite + vector memory")]
  CC --> STATE
  CU --> STATE
```

### 2. Orchestration & the language boundary

The **orchestrator** is an always-active meta-agent and the system's single **translation boundary** (ADR-011): it understands your input in any language, transcribes intent to English, coordinates the entire internal pipeline in English, and replies to you in your language.

```mermaid
flowchart TD
  U(["👤 User — any language (e.g. pt-BR)"])
  U -->|"input"| O["🧭 Orchestrator<br/>(language boundary)"]
  O -->|"transcribe intent → English"| PLAN["Plan · Spec · Tasks<br/>(English artifacts)"]
  PLAN --> ROUTE{"Route by wave"}
  ROUTE -->|"English prompt"| W1["Agent / Skill worker"]
  ROUTE -->|"English prompt"| W2["Agent / Skill worker"]
  ROUTE -->|"English prompt"| W3["Agent / Skill worker"]
  W1 -->|"English result"| SYN["Synthesize"]
  W2 -->|"English result"| SYN
  W3 -->|"English result"| SYN
  SYN -->|"reply in user's language"| U
  TRACK[("osforge-db<br/>state + decisions")]
  PLAN -.-> TRACK
  SYN -.-> TRACK
```

> **Rule of thumb:** if a worker, skill, file, or artifact reads it, it's English. If the user reads it, it's the user's language.

The orchestrator's own flow is a checkpointed state machine — nothing advances without explicit approval:

```mermaid
flowchart LR
  DETECT["0 · DETECT<br/>(silent classify)"] --> INTAKE["1 · INTAKE<br/>(grilling, 1 Q at a time)"]
  INTAKE --> TRIAGE["2 · TRIAGE<br/>(QUICK/STANDARD/COMPLEX)"]
  TRIAGE --> PLAN["3 · PLAN"]
  PLAN -->|"✅ approve"| ROUTE["4 · ROUTE<br/>(phase by phase)"]
  ROUTE --> TRACK["5 · TRACK<br/>(osforge-db)"]
  TRACK --> CORRECT["6 · CORRECT"]
  CORRECT -.->|"re-plan"| PLAN
```

### 3. The four routing layers

Every demand is resolved through four decisions — never skip triage.

```mermaid
flowchart TB
  subgraph L1["1 · Model routing (by complexity)"]
    T1["Top: opus / fable — planning, architecture, audit"]
    T2["Mid: sonnet — implementation, review, debugging"]
    T3["Fast: haiku — tests, docs, boilerplate, i18n"]
  end
  subgraph L2["2 · Agent selection"]
    A1["orchestrator → 26 specialists"]
  end
  subgraph L3["3 · Skill triggers (on-demand)"]
    S1["@SKILLS.md index → skills/.../SKILL.md"]
  end
  subgraph L4["4 · Spec workflow + parallel dispatch"]
    P1["discover → specify → design → tasks → implement → measure"]
    P2["waves: depends_on → parallel within a wave"]
  end
  L1 --> L2 --> L3 --> L4
```

### 4. Spec-driven workflow

Non-trivial features run the `spec-*` cycle; `tasks.md` carries `wave` + `depends_on`, so independent work dispatches in parallel and the `osforge-db` board tracks the waves.

```mermaid
flowchart LR
  D["/spec-discover"] --> SP["/spec-specify"] --> DE["/spec-design"] --> TA["/spec-tasks"]
  TA --> IM["/spec-implement<br/>(parallel waves)"] --> ME["/spec-measure"]
  TA -. artifacts .-> CANVAS["OSForge Canvas<br/>localhost:4242"]
  SP -. artifacts .-> CANVAS
```

---

## Quick start

```bash
git clone https://github.com/plocemourasouza/osforge.git
cd osforge
./deploy.sh
```

`deploy.sh` syncs everything to `~/.claude/` and `~/.cursor/` automatically (use `--dry-run` to preview, `--claude-only`/`--cursor-only` to scope, `--with-qdrant` to provision vector memory). See [USAGE.md](USAGE.md) for manual and advanced options.

**Next steps:**
- **Usage and workflows** → [USAGE.md](USAGE.md)
- **Skill index (177 skills + triggers)** → [claude-code/SKILLS.md](claude-code/SKILLS.md)
- **Session orchestration** → [claude-code/CLAUDE.md](claude-code/CLAUDE.md)
- **Authoring a new skill** → [docs/SKILL-STANDARD.md](docs/SKILL-STANDARD.md) + [docs/SKILL.template.md](docs/SKILL.template.md)

---

## What's inside

### 27 specialized agents

Every agent ships a Reality Check (anti-self-deception) and a Quality Control loop (mandatory verification). Full roster in [USAGE.md](USAGE.md).

- **Orchestrator** — meta-agent: intake, triage, planning, routing to 26 specialists, cross-session tracking, and the language boundary.
- **Engineering** — frontend-engineer, backend-engineer, database-architect, mobile-developer, game-developer, devops-engineer, performance-optimizer.
- **Quality & Security** — code-reviewer, code-refactorer, security-auditor, penetration-tester, test-engineer, qa-automation-engineer, validator.
- **Planning & Product** — planner, system-architect, project-planner, product-manager, product-owner, product-strategy-advisor.
- **Investigation** — debugger, explorer-agent, code-archaeologist.
- **Docs & SEO** — documentation-writer, seo-specialist, git-commit-helper.

### 177 on-demand skills

Full index with triggers in [claude-code/SKILLS.md](claude-code/SKILLS.md). Main categories:

- **Core & Workflow** — TDD, Verification Before Completion, Security Best Practices, Coding Guidelines (Karpathy Rules), Git, Clean Code, Spec/PRD/Architecture builders, Epic Decomposer, Story Executor.
- **Frontend & UI** — React + Next.js Expert (9 modules), shadcn/ui, Tailwind v4, Frontend Design, Aesthetic Boost, Design Taste Dials, Aesthetic Modes (Editorial Minimalist / Industrial Brutalist / Soft Premium), Redesign Audit, UI Design Intelligence, Core Web Vitals, Accessibility (WCAG), i18n, SEO/GEO.
- **Backend & Database** — Prisma Expert, PostgreSQL + Supabase, Auth (SSR), Stripe, API Patterns (REST/GraphQL/tRPC), Database Design, Node.js, Bun, Server Management.
- **Security** — Red Team Tactics (MITRE ATT&CK), Vulnerability Scanner (OWASP), Insecure Defaults Detection, GDPR/LGPD, plus offensive-security skills (authorized testing only).
- **Testing & Quality** — E2E Playwright, Testing Patterns, Adversarial Review, Code Review, Edge Case Hunter, UI Audit, Readiness Gate, Output Enforcement.
- **Meta & Context** — Systematic Debugging, Performance Profiling, Smart Model Dispatch, llmfit Advisor, Context Distillator, osforge-db, OSForge Canvas, System Diagrams (Archify), Stuck Recovery, Config Critique, Context Compact, Tool Safety Classifier, Evolve/Instinct.
- **The Agency** — 121 AI specialists across 10 divisions + 32 marketing execution workflows.

### 14 rules (Cursor: 11 always-on, 3 stack rules by file glob)

TypeScript Strict, Code Style, Product Thinking (PDD), TDD Enforcement, Next.js Patterns, Security Mindset, Intelligent Routing, Anti-AI-Slop, Commit Conventions, Agent Skills Reference, Memory Hierarchy, Artifact Chain, Orchestrator Awareness, Plan Mode. (Claude Code equivalents live inside `claude-code/CLAUDE.md`.)

### 9 spec commands (`/spec-*`)

`/spec-discover` · `/spec-specify` · `/spec-design` · `/spec-tasks` · `/spec-implement` · `/spec-clarify` · `/spec-checklist` · `/spec-constitution` · `/spec-measure`

### Hooks (zero token cost)

Run by the runtime — they consume no context tokens:

- **GateGuard** (`gateguard.py`, PreToolUse Bash + UserPromptSubmit) — blocks only the irreversible/shared (`rm -rf`, `git push --force`, `reset --hard`, `clean -f`, SQL `DROP/TRUNCATE/DELETE`). An explicit confirmation from the user ("tem permissão", "pode executar", "go ahead", or a bare "sim"/"yes") opens the gate until the user's next message (15 min cap, `OSFORGE_GATEGUARD_GRANT_TTL`); `gateguard: sessão liberada` opens it for the whole session; negations never count. Kill-switch `OSFORGE_GATEGUARD=off`. A turn grant is only accepted as an answer to a denial in the last 10 min; a bare "ok" with nothing denied does not open the gate.
- **scan-secrets** (`scan-secrets.sh` → `scan-secrets.py`) — blocks a commit/push whose staged diff adds a credential-looking line, and `rm -rf` aimed at `/`, `~` or a parent directory; reads both the Claude Code and the Cursor payload shapes.
- **protect-tests** (`protect-tests.sh`) — warns when a test file is altered.
- **observe → evolve** (`observe-capture.py`) — records session observations for `osforge-db evolve`.
- **Auto-resume** (`session-resume.sh` / `session-save.py`) — SessionStart injects `osforge-db resume`; Stop writes `set-resume` automatically.
- **Canvas autostart** (`canvas-autostart.sh`) — boots the Canvas server (port 4242) when needed.

### osforge-db — local SQLite state + memory

A Python CLI over a local SQLite database (`~/.osforge/osforge.db`). No server, no network. Persists projects, phases, tasks (`wave`/`depends_on`), decisions with FTS5 full-text search, and blockers. Session resume in ~50 tokens via `osforge-db resume <slug>`; cross-project view via `osforge-db board`. Optional 3-tier vector memory (Qdrant → SQLite cosine → FTS5) for semantic recall.

### OSForge Canvas — local generative UI

A local Bun service at `localhost:4242`. The agent writes versioned JSON artifacts; the browser renders cards, tables, dependency graphs, gantt, checklists, and decision buttons with SSE live-reload. Feedback returns as structured JSON. Default for every spec and plan — opt out with "text only".

---

## Language & authoring standard

OSForge separates **authoring language** from **runtime language**:

- **Authoring = English.** All repository content (skills, agents, rules, `CLAUDE.md`, `SKILLS.md`, commands, ADRs, comments) is written in English — one language maximizes the model's predictability and removes mixed-language drift.
- **Runtime = the user's language**, via the orchestrator translation boundary (see [Architecture §2](#2-orchestration--the-language-boundary)).

New skills follow a single standard — [`docs/SKILL-STANDARD.md`](docs/SKILL-STANDARD.md) — built from [`docs/SKILL.template.md`](docs/SKILL.template.md). It merges OSForge's activation pattern (`Use when` / `Keywords` / `Do NOT use for`) and execution-routing frontmatter (`model` / `context` / `agent` / `allowed-tools`) with an explicit invocation axis (orchestrator vs. discipline), leading words, checkable completion criteria, and a failure-mode audit. Activation is validated by measurement, not by eye: `scripts/run-trigger-eval.sh` runs 5 queries where the skill **must** fire and 5 where it **must not** (a description that fires at everything costs context in every session), each 3 times, and writes the result to [`docs/evals/`](docs/evals/README.md).

### Bundled subsystems

- **Design Taste System** — adapted from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT): three adjustable dials (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY), three per-project aesthetic modes, anti-AI-slop rules, GSAP scrollytelling, Bento 2.0, double-bezel cards, micro-physics.
- **Agentic AI patterns** — adapted from [Leonxlnx/agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research): `tool-safety-classifier`, `context-compact`, `config-critique`, `stuck-recovery`, `memory-hierarchy`, the Coordinator Protocol in the orchestrator, and a documented prompt-cache boundary.
- **UI Design Intelligence** — adapted from [nextlevelbuilder/ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT): 161 industry reasoning rules, 161 palettes, 84 styles, 73 typographic pairs.
- **The Agency** — 121 business specialists in 10 divisions + 32 marketing execution workflows. Architecture: Agent (persona — *who I am*) + Workflow (execution — *what I do*); 4 agents require mandatory human approval before any autonomous action.
- **llmfit Advisor** — detects your hardware and recommends which local LLMs fit (quantization, speed, fit scoring across 497 models). Source: [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) (MIT).
- **System Diagrams (Archify)** — verified architecture / workflow / sequence / data-flow / lifecycle diagrams as self-contained interactive HTML, accepted only with a `deliver` receipt (9/9 checks + SHA-256). The engine [tt-a1i/archify](https://github.com/tt-a1i/archify) (MIT) is installed pinned by `deploy.sh` (`ARCHIFY_VERSION`, `--no-archify` to skip); the core skill `system-diagrams` wires it into `/spec-design`, ADRs, TDDs, and runbooks. Analysis: `docs/ANALISE-ARCHIFY.md`.

---

## Stack compatibility

| Layer | Technology |
|---|---|
| Framework | Next.js `@latest` (App Router) · Node · Express · Vite · Astro |
| Language | TypeScript (strict) · Python · Ruby (Rails) · PHP · Java |
| ORM (default) | Prisma `@latest` |
| Database | PostgreSQL · Qdrant (vector) · SQLite |
| Auth | Better Auth · Supabase Auth (SSR) |
| UI | shadcn/ui + Tailwind CSS |
| Validation | Zod (schema validation, end-to-end types) |
| Runtime | Bun |
| Deployment | Vercel · AWS |
| Payments | Stripe · ASAAS |
| Testing | Playwright · Bun test · Jest · pytest |
| AI tools | Claude Code · Cursor |

**Accessory libraries** (commonly paired across the skills) — data/state: TanStack Query, SWR · forms: React Hook Form (+ Zod resolver) · charts: Recharts · theming: next-themes · icons: lucide-react · motion: Framer Motion, GSAP.

**MCP servers** — 1 global (Context7, `mcp/claude-code.json`); GitHub, Supabase, Shadcn, Browsermcp, next-devtools and Prisma are per-project stacks in `mcp/stacks/`, installed with `scripts/install-mcp.sh`.

---

## Origins

OSForge is a **curation**, not a fork. It distills **1100+ agent skills, commands, and patterns from 23 sources** into one coherent, English-authored, stack-tuned framework. Nothing is copied wholesale — every upstream is adapted to the OSForge standard, credited with `inspired_by`/`source` frontmatter, and the raw collections live disk-only under `sources/` (ADR-009). What each source contributed:

### Foundations & format

| Source | Contribution |
|---|---|
| [Anthropic](https://github.com/anthropics) | Skill format, core skills, brand guidelines |
| [GitHub spec-kit](https://github.com/github/spec-kit) · OpenSpec | Spec-driven workflow + the `constitution` pattern |
| BMAD-METHOD · GSD | Multi-phase planning and discovery discipline |
| superpowers · context-engineering | Context budgeting, progressive disclosure, prompt-cache strategy |

### Engineering, security & platform

| Source | Contribution |
|---|---|
| [Vercel Labs](https://github.com/vercel) | Next.js + React performance patterns |
| [Trail of Bits](https://github.com/trailofbits) | Security-audit methodology, threat modeling |
| [Supabase](https://github.com/supabase) · Prisma | Postgres, RLS, auth (SSR), ORM patterns |
| [Expo](https://github.com/expo) | Mobile / React Native coverage |
| [Cloudflare](https://github.com/cloudflare) · [Sentry](https://github.com/getsentry) | Edge/deploy and observability patterns |
| claude-red | Offensive-security tactics (authorized testing only) |

### Design, agentic patterns & business

| Source | Contribution |
|---|---|
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT) | Premium frontend taste system — dials, aesthetic modes, anti-AI-slop |
| [Leonxlnx/agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research) | Coordinator Protocol, tool-safety, context-compact, stuck-recovery |
| [nextlevelbuilder/ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT) | Design-system engine — 161 reasoning rules, 161 palettes, 84 styles |
| [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) | Skill-predictability theory feeding the OSForge skill standard |
| The Agency · Marketing Skills | 121 business specialists + 32 marketing execution workflows |
| [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) (MIT) | Local-LLM hardware fit advisor |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) (MIT) | Verified interactive system diagrams — engine behind `system-diagrams` (installed pinned, not vendored) |

> The 13 vendored collections (`sources/01-anthropic` … `sources/13-claude-red`) are the raw curation base — disk-only, never deployed. Every architectural decision is recorded as an ADR in **[docs/DECISIONS.md](docs/DECISIONS.md)** (currently 11 ADRs).

---

## License

MIT — see [LICENSE](LICENSE).

## Author

**Paulo Souza** — [@plocemourasouza](https://github.com/plocemourasouza)

*Forging the development environment for AI-powered teams.*
