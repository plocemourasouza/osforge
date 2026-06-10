# 🔨 OSForge

**Curated agent skills, agents, rules, hooks, commands, and a full AI specialist library for AI-powered development.**

OSForge is a production-grade AI development framework with **126 on-demand skills**, **26 specialized agents**, **13 always-on rules**, **9 spec commands**, **Python hooks**, **SQLite local state backend**, **121 business specialists**, and **32 marketing execution workflows** — optimized for the **Next.js + TypeScript + Prisma + Supabase + Bun** stack, with expanded support for mobile, game dev, Rust, Python, and more. Built for Claude Code and Cursor.

> *"Forging the development environment for AI-powered teams."*

📖 **[Full usage guide → USAGE.md](USAGE.md)** · 💡 **[10 usage examples → docs/EXAMPLES.md](docs/EXAMPLES.md)** · 🗺️ **[Architecture map → osforge-architecture.html](osforge-architecture.html)**

---

## Why OSForge?

AI coding agents are only as good as the context they receive. OSForge solves three problems:

1. **Context efficiency** — 153 skills in ~12K base tokens (~6% of 200K window). Everything else loads on-demand.
2. **Stack-specific patterns** — Core skills tailored for Next.js App Router + Prisma + Supabase + shadcn/ui, with expanded coverage for mobile, game dev, Rust, Python, and cross-platform.
3. **Quality gates built-in** — TDD enforcement, security auditing, red team tactics, insecure defaults detection, Reality Check + Quality Control Loop in every agent, and Python hooks at zero token cost.
4. **Local SQLite state** — `osforge-db` CLI persists project state, architectural decisions, and blockers locally. Session resumption in ~50 tokens via `osforge-db resume`. FTS5 full-text search across all decisions cross-project.

---

## Quick Start

```bash
git clone https://github.com/plocemourasouza/osforge.git
cd osforge
./deploy.sh
```

The `deploy.sh` script syncs everything to `~/.claude/` and `~/.cursor/` automatically. See [USAGE.md](USAGE.md) for manual setup and options.

---

## What's Inside

### 153 Skills (on-demand)

#### Core & Workflow
| # | Skill | Category |
|---|---|---|
| 1 | TDD Workflow (RED-GREEN-REFACTOR) | Core |
| 2 | Verification Before Completion | Core |
| 3 | Security Best Practices | Security |
| 4 | Coding Guidelines (Karpathy Rules) | Core |
| 5 | Product-Driven Spec Development (PDD) | Core |
| 6 | Git Workflow | Core |
| 7 | Clean Code Standards | Core |
| 8 | Best Practices | Core |

#### Frontend & UI
| # | Skill | Category |
|---|---|---|
| 9 | React & Next.js Performance | Performance |
| 10 | Next.js React Expert (9 optimization modules) | Performance |
| 11 | Frontend UI System (shadcn/ui) | Frontend |
| 12 | Frontend Design (colors, typography, animation, UX) | Frontend |
| 12b | Aesthetic Boost (anti-AI-slop, convergence breaking, complexity matching) | Frontend |
| 13 | Tailwind Patterns (v4) | Frontend |
| 14 | UI Design Intelligence (Styles, Palettes, Typography, UX, Charts) | Frontend |
| 15 | Web Design Guidelines (accessibility, UX rules) | Frontend |
| 15a | **Taste Design Dials** (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY dials, GSAP, magnetic, perpetual motion, Bento 2.0) | Frontend |
| 15b | **Aesthetic Modes** (3 modos: Editorial Minimalist / Industrial Brutalist / Soft Premium) | Frontend |
| 15c | **Redesign Audit** (auditoria + upgrades cirúrgicos em projeto existente) | Frontend |
| 15d | **Stitch Design Export** (DESIGN.md para Google Stitch) | Frontend |
| 16 | Core Web Vitals | Performance |
| 17 | Accessibility (WCAG 2.1) | Frontend |
| 18 | OpenUI/GenUI Layout | Frontend |
| 19 | i18n & Localization | Frontend |
| 20 | SEO | Frontend |
| 21 | SEO Fundamentals (E-E-A-T, structured data) | SEO |

#### Backend & Database
| # | Skill | Category |
|---|---|---|
| 22 | Prisma Expert | Stack |
| 23 | PostgreSQL & Supabase Optimization | Performance |
| 24 | Next.js + Supabase Auth | Stack |
| 25 | Stripe Integration | Stack |
| 26 | API Patterns (REST/GraphQL/tRPC + 10 reference modules) | Backend |
| 27 | Database Design (schema, indexing, ORM + 6 reference modules) | Backend |
| 28 | Node.js Best Practices | Backend |
| 29 | Bun Development | Stack |
| 30 | Server Management | Backend |

#### Mobile & Game
| # | Skill | Category |
|---|---|---|
| 31 | Mobile Design (touch psychology, platform-specific + references) | Mobile |
| 32 | Game Development (orchestrator + 10 sub-skills) | Game |
| 33 | App Builder (13 project templates) | Scaffolding |

#### Security & Compliance
| # | Skill | Category |
|---|---|---|
| 34 | Red Team Tactics (MITRE ATT&CK) | Security |
| 35 | Vulnerability Scanner (OWASP checklists) | Security |
| 36 | Insecure Defaults Detection | Security |
| 37 | Security Threat Model | Security |
| 38 | GDPR / LGPD Data Handling | Compliance |

#### Offensive Security — claude-red (27, on-demand)
> Curated/converted subset of [SnailSploit/Claude-Red](https://github.com/SnailSploit/Claude-Red) for our web/mobile/cloud AppSec. All passed the skill-metrics audit (median 11.96/12). Authorized testing only.

| Area | Skills |
|---|---|
| Web (16) | offensive-sqli, offensive-xss, offensive-ssrf, offensive-idor, offensive-file-upload, offensive-rce, offensive-race-condition, offensive-business-logic, offensive-graphql, offensive-ssti, offensive-xxe, offensive-deserialization, offensive-request-smuggling, offensive-open-redirect, offensive-parameter-pollution, offensive-waf-bypass |
| Auth (2) | offensive-jwt, offensive-oauth |
| Cloud / AI (2) | offensive-cloud, offensive-ai-security |
| Mobile / Recon (2) | offensive-mobile, offensive-osint |
| Code review / Fuzzing (2) | offensive-bug-identification, offensive-fuzzing |
| Exploit-dev / Utility (3) | offensive-toctou, offensive-reporting, offensive-fast-checking |

#### Testing & Quality
| # | Skill | Category |
|---|---|---|
| 39 | E2E Testing (Playwright) | Testing |
| 40 | Testing Patterns (pyramid, unit, integration) | Testing |
| 41 | Web App Testing (Playwright, visual regression) | Testing |
| 42 | Lint and Validate (ESLint, Prettier) | Testing |
| 43 | Code Review Checklist | Quality |
| 44 | Adversarial Review | Quality |
| 45 | Code Review (OSForge Stack) | Quality |
| 46 | Edge Case Hunter | Quality |
| 47 | Elicitation Engine | Quality |
| 48 | Readiness Gate | Quality |
| 49 | UI Audit (6-pillar Visual Quality Review) | Quality |
| 50 | Differential Review | Quality |

#### Planning & Ideation
| # | Skill | Category |
|---|---|---|
| 51 | Brainstorming (Socratic questioning) | Planning |
| 52 | Plan Writing (structured planning) | Planning |
| 53 | Spec Builder (Collaborative) | Planning |
| 54 | PRD Builder (Collaborative) | Planning |
| 55 | Architecture Builder (ADR) | Planning |
| 56 | Architecture Patterns (system design + 5 reference modules) | Planning |
| 57 | Epic Decomposer | Planning |
| 58 | Story Executor | Planning |
| 59 | Phase Discussion (Pre-planning Context Capture) | Planning |
| 60 | Behavioral Modes (agent personas) | Planning |

#### Languages & Runtime
| # | Skill | Category |
|---|---|---|
| 61 | Rust Pro (ownership, async, cargo) | Language |
| 62 | Python Patterns (FastAPI, Django, Flask) | Language |
| 63 | Bash Linux (shell scripting) | Language |
| 64 | PowerShell Windows | Language |

#### DevOps & Deploy
| # | Skill | Category |
|---|---|---|
| 65 | Deployment Procedures (blue-green, canary, rollback) | DevOps |
| 66 | Vercel Deploy | DevOps |
| 67 | Claude CI/CD Actions | DevOps |

#### Documentation & SEO
| # | Skill | Category |
|---|---|---|
| 68 | Documentation Templates (README, API docs, ADR) | Docs |
| 69 | Docs Writer | Docs |
| 70 | Technical Design Doc Creator | Docs |
| 71 | Doc Sanitization | Docs |
| 72 | GEO / GenAI Optimization (AI search visibility) | SEO |

#### Meta & Context
| # | Skill | Category |
|---|---|---|
| 73 | Systematic Debugging (4-phase methodology) | Meta |
| 74 | Performance Profiling (Lighthouse, bundle analysis) | Meta |
| 75 | Predictive Failure Analysis | Meta |
| 76 | Smart Model Dispatch | Optimization |
| 77 | llmfit Advisor (Local LLM Hardware Fit) | Optimization |
| 78 | Context Distillator | Context |
| 79 | Project Context Generator | Context |

> **Plus:** Doc Shard, Editorial Review, Agent Skills Search, Dispatching Parallel Agents, MCP Builder, Claude API & Agent SDK (TypeScript), Context7 Docs-First, Smart Hooks (Python), AutoRefine Skill, Skill Creator, The Agency (121 AI Specialists), **Output Enforcement** (anti-truncation/anti-placeholder modifier)

### 26 Agents (on-demand)

All agents include **Reality Check** (anti-self-deception) and **Quality Control Loop** (mandatory self-verification) sections.

#### Engineering & Code
| Agent | Role |
|---|---|
| **frontend-engineer** | shadcn/ui + Server Components specialist. Anti-cliché design rules. |
| **backend-engineer** | Prisma + Supabase + Server Actions |
| **database-architect** | Schema design, indexing, migrations, ORM selection |
| **mobile-developer** | React Native + Flutter, mobile-first design |
| **game-developer** | Game mechanics, engines, 2D/3D/multiplayer/VR-AR |
| **devops-engineer** | CI/CD, Docker, infra, pipelines, zero-downtime deploys |
| **performance-optimizer** | Core Web Vitals, profiling, bundle optimization |

#### Quality & Security
| Agent | Role |
|---|---|
| **code-reviewer** | Code quality + YAML-structured review output |
| **code-refactorer** | Refactoring patterns and clean code |
| **security-auditor** | Trail of Bits methodology (defensive) |
| **penetration-tester** | Offensive security, red team, MITRE ATT&CK |
| **test-engineer** | Testing strategies, TDD, test pyramid design |
| **qa-automation-engineer** | E2E with Playwright, CI pipelines, visual regression |

#### Planning & Product
| Agent | Role |
|---|---|
| **orchestrator** | Intake, triage (21 domains), planning, routing to 26 agents, tracking (always-active meta-agent) |
| **planner** | Architecture, decomposition, story creation (★ Synkra-enhanced) |
| **system-architect** | System design and ADRs |
| **project-planner** | Discovery, task planning, roadmap |
| **product-manager** | Requirements, user stories, prioritization |
| **product-owner** | Strategy, backlog, MVP definition |
| **product-strategy-advisor** | Product strategy and roadmap |

#### Investigation & Support
| Agent | Role |
|---|---|
| **debugger** | 10-step autonomous debugging |
| **explorer-agent** | Codebase analysis, onboarding, dependency mapping |
| **code-archaeologist** | Legacy code archaeology, understanding and modernizing old systems |
| **validator** | Spec critique + acceptance verification |

#### Documentation & SEO
| Agent | Role |
|---|---|
| **documentation-writer** | Technical docs, manuals, READMEs |
| **seo-specialist** | SEO, E-E-A-T, structured data, ranking optimization |
| **git-commit-helper** | Conventional commits and release notes |

### 13 Always-On Rules (Cursor)

- **TypeScript Strict Mode** — `strict: true` + `noUncheckedIndexedAccess` + no `any`
- **Code Style** — Product thinking (PDD), naming conventions, import order
- **Commit Conventions** — Conventional commits enforced
- **TDD Enforcement** — No production code without failing test first
- **Next.js Patterns** — App Router best practices, Server vs Client Components
- **Product Thinking** — User-first decisions before technical decisions
- **Security Mindset** — Zero-trust by default, fail-safe patterns
- **Agent Skills Reference** — How to load and use OSForge skills
- **Orchestrator Awareness** — Always check .osforge/status.yaml for work in progress; route complex demands through Orchestrator
- **Artifact Chain** — Every planning artifact must have frontmatter with type, status, depends_on; never advance phase without checkpoint approval
- **Intelligent Routing** — Silent domain detection + automatic agent + skill selection on every message (21 domains + design taste sub-routing)
- **Anti-AI-Slop** — 40 enforced rules preventing generic AI design (typography, color, layout, content, components, performance, meta)
- **Memory Hierarchy** — 4-layer CLAUDE.md system (Managed/User/Project/Local) with `@include` directive, frontmatter `paths` conditional injection, and explicit override semantics

### 9 Spec Commands (Claude Code)

Slash commands for spec-driven development (`/spec-*`):

| Command | Purpose |
|---|---|
| `/spec-discover` | Explore problem space and gather requirements |
| `/spec-specify` | Write formal specification |
| `/spec-design` | Technical design and ADR |
| `/spec-tasks` | Break down into implementable tasks |
| `/spec-implement` | Execute implementation with guardrails |
| `/spec-clarify` | Clarification loop for ambiguous specs |
| `/spec-checklist` | Pre-ship quality checklist |
| `/spec-constitution` | Define project principles and constraints |
| `/spec-measure` | Define and track success metrics |

### Python Hooks (zero token cost)

| Hook | Trigger | Purpose |
|---|---|---|
| `pre_tool_use.py` | Before any tool call | Blocks dangerous commands, protects `.env`, audit log |
| `post_tool_use.py` | After Write/Edit | TypeScript quality gates: `console.log`, `any`, `@ts-ignore` |
| `pre_compact.py` | Before context compaction | Conversation backup |
| `session_end.py` | Session end | Session logging + macOS notification |

---

## 🏢 The Agency — 121 AI Specialists (on-demand)

A curated library of 121 AI specialists covering every business and technical function. Each loads only when needed — zero idle context cost.

| Division | Agents | When to use |
|---|---|---|
| 💻 Engineering | 23 | Código, arquitetura, segurança, DevOps, SRE, documentação |
| 🎨 Design | 8 | UI/UX, sistemas de design, identidade visual, pesquisa com usuários |
| 📢 Marketing | 26 | Conteúdo, SEO, redes sociais, growth hacking, ASO + **25 workflows de execução** |
| 💰 Paid Media | 7 | Google/Meta Ads, PPC, tracking, auditoria de contas + **4 workflows de execução** |
| 📊 Product | 5 | Roadmap, sprint, pesquisa de mercado, síntese de feedback |
| 🎬 Project Management | 6 | Planejamento, Jira/Git workflows, rastreamento de experimentos |
| 💼 Sales | 8 | Prospecção, discovery, qualificação, propostas, pipeline + **3 workflows de execução** |
| 🛟 Support & Ops | 6 | Atendimento, analytics, compliance, resumos executivos |
| 🧪 Testing | 8 | QA, API testing, WCAG, performance, validação de entregáveis |
| 🎯 Specialized | 24 | Orquestração, compliance SOC2/ISO, blockchain, MCP builder |

> ⚠️ Four agents require mandatory human approval before any autonomous action. See [USAGE.md](USAGE.md#high-risk-agents).

### 32 Marketing Execution Workflows (on-demand)

Integrated from [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Each workflow provides a step-by-step execution framework that pairs with The Agency's agent personas.

**Architecture:** Agent (persona: *who I am*) + Workflow (execution: *what I do*).

| Category | Workflows | Location |
|---|---|---|
| CRO | page-cro, signup-flow-cro, onboarding-cro, form-cro, popup-cro, paywall-upgrade-cro | `skills/agency/marketing/workflows/` |
| Content & Copy | copywriting, copy-editing, content-strategy, email-sequence, lead-magnets, social-content | `skills/agency/marketing/workflows/` |
| SEO & Discovery | seo-audit, ai-seo, programmatic-seo, site-architecture, schema-markup, competitor-alternatives | `skills/agency/marketing/workflows/` |
| Growth & Retention | churn-prevention, free-tool-strategy, referral-program | `skills/agency/marketing/workflows/` |
| Strategy | marketing-ideas, marketing-psychology, launch-strategy, pricing-strategy | `skills/agency/marketing/workflows/` |
| Paid Media | paid-ads, ad-creative, analytics-tracking, ab-test-setup | `skills/agency/paid-media/workflows/` |
| Sales | cold-email, sales-enablement, revops | `skills/agency/sales/workflows/` |

All workflows reference `.osforge/marketing-context.md` as the shared context source. Full agent↔workflow mapping in `skills/agency/marketing/workflows/ROUTING.md`.

---

## 🔬 Agentic AI Patterns (agentic-ai-prompt-research integration)

Integrated from [Leonxlnx/agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research) (1.6k+ stars). Research-grade patterns extracted from observed Claude Code internal architecture.

### 4 New Skills

| Skill | Purpose | Inspired by Prompt |
|---|---|---|
| **`tool-safety-classifier`** | LLM-powered auto-approval gate for autonomous tool execution. 3 user-customizable sections (`allow` / `soft_deny` / `environment`). Injection defense: compact transcript excludes assistant text. | 12 — YOLO Classifier |
| **`context-compact`** | 9-section structured summarization when context > 70%. Three modes (full / partial-recent / partial-up-to). `NO_TOOLS_PREAMBLE` prevents tool calls during summary. `<analysis>` scratchpad stripped before delivery. | 21 — Compact Service |
| **`config-critique`** | LLM linter for user customizations (new SKILL.md, rules, hooks, agents). Evaluates in 4 axes: Clarity / Completeness / Conflicts / Actionability. Cross-references against baseline. | 17 — Auto Mode Critique |
| **`stuck-recovery`** | Detect agent loops (same tool failing 3x, no progress in N turns) + save state via osforge-db + propose surgical reset. 4-phase protocol: STOP → SAVE → DIAGNOSE → RECOVER. | 26 — Stuck Skill (reframed) |

### 1 New Rule + 2 Enrichments

- **`rules/memory-hierarchy.mdc`** (NEW) — Formalizes 4-layer CLAUDE.md system, `@include` directive (depth 5), frontmatter `paths` conditional injection, override resolution rules.
- **`agents/orchestrator/AGENT.md`** (enriched) — Added Coordinator Protocol section: synthesize-before-delegate, Continue vs Spawn decision matrix, parallelism rules, real verification philosophy, worker prompt guidance, `<task-notification>` XML format.
- **`claude-code/CLAUDE.md`** (enriched) — Documented Cacheable Prefix + Cache Boundary + Dynamic Suffix pattern for Anthropic API prompt caching (~10% cost reduction on stable prefix).

### Why This Matters

The taste-skill integration improved **output quality** (anti-slop, premium design).
This integration improves **agent infrastructure** — how agents coordinate, handle context limits, validate customizations, and recover from stuck states. Together they make OSForge production-ready for:

- **Long-running autonomous sessions** (auto-mode + context-compact + stuck-recovery)
- **Multi-agent orchestration** (Coordinator Protocol + parallelism rules)
- **Enterprise deployments** (memory-hierarchy with Managed layer)
- **Open-source contributions** (config-critique as PR review gate)

---

## 🎨 Design Taste System (taste-skill integration)

Integrated from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT, 10k+ stars). A complete premium frontend engineering toolkit that overrides default LLM design biases via three tunable dials, mode-specific paradigms, and audit-and-upgrade workflows.

### The 3-Dial System (`taste-design-dials`)

Premium frontend at the level of award-winning agency work — tunable on three independent axes:

| Dial | Range | What it controls |
|---|---|---|
| **DESIGN_VARIANCE** | 1 (Predictable Symmetric) → 10 (Artsy Chaos) | Layout asymmetry, grid breaking, negative space |
| **MOTION_INTENSITY** | 1 (Static) → 10 (Cinematic GSAP scrolltelling) | Animations, spring physics, perpetual loops |
| **VISUAL_DENSITY** | 1 (Art Gallery Airy) → 10 (Cockpit/Packed Data) | Spacing, card usage, information density |

Default baseline: `VARIANCE=8 · MOTION=6 · DENSITY=4`. Auto-adjusts to user prompt (*"mais minimal"* → lower density; *"animações fortes"* → raise motion).

**Includes:** Creative Arsenal (50+ premium components), Motion-Engine Bento 2.0 paradigm, double-bezel nested architecture, magnetic micro-physics, liquid glass refraction, GSAP scroll-pinning, AI Tells (forbidden patterns), and the full Pre-Flight Check matrix.

### The 3 Aesthetic Modes (`aesthetic-modes`)

Pick ONE per project and commit. Each mode has its own complete typographic, chromatic, and motion architecture:

| Mode | Vibe | Use for |
|---|---|---|
| **EDITORIAL_MINIMALIST** | Warm monochrome, document-style, typographic contrast | Notion/Linear-style products, knowledge tools, content-heavy SaaS |
| **INDUSTRIAL_BRUTALIST** | Swiss print or CRT terminal, rigid grids, hazard red accent | Data-heavy dashboards, telemetry, blueprint UIs, portfolios |
| **SOFT_PREMIUM** | Apple-tier, haptic depth, double-bezel cards, cinematic motion | Premium SaaS, AI products, agency sites, Awwwards-tier launches |

### Audit + Upgrade Loop (`redesign-audit`)

Different from review-only skills. This skill **audits AND applies fixes** working with the existing stack — no rewrites. Covers typography, color, layout, interactivity, content, components, iconography, code quality, and the 5 "things AI typically forgets" (legal links, back nav, 404, validation, skip links).

### Cross-Cutting Quality Modifiers

- **`output-enforcement`** — anti-laziness directive. Bans `// ... rest of code`, `// TODO`, `for brevity`. Enforces complete output via SCOPE-counting and clean `[PAUSED — X of Y complete]` breakpoints when token limit looms.
- **`stitch-design-export`** — generates `DESIGN.md` files compatible with [Google Stitch](https://labs.google.com/stitch) for semantic design system handoff.

### How auto-routing works

The `rules/intelligent-routing.mdc` rule silently detects design intent and bundles the right skills:

```
"crie uma landing page premium"
  → frontend-design + aesthetic-boost + taste-design-dials + (ask: which mood?)

"estilo Notion / minimalist editorial"
  → aesthetic-modes → EDITORIAL_MINIMALIST

"redesenhar nosso site"
  → redesign-audit → ui-audit (validation loop)

"refatora tudo isso sem placeholder"
  → output-enforcement modifier activates on any agent
```

Combined with the enhanced **`anti-ai-slop.mdc`** rule (40 enforced anti-patterns spanning typography, color, layout, content, components, performance, and meta), every frontend output is automatically gated against generic AI design.

---

## 🔍 llmfit Advisor — Local LLM Hardware Fit

Detects your hardware (RAM, CPU, GPU/VRAM) and recommends which local LLMs will actually run well on your machine — with optimal quantization, speed estimates, and fit scoring across 497 models from 133 providers.

**Requires:** `brew install llmfit` or `cargo install llmfit`

Key use cases: LGPD-sensitive data (Essent/Rede Essent Jus), OSystems clients without API budget, and high-volume repetitive dev tasks where local models eliminate API costs.

> Source: [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) (MIT)

---
## 🗄️ Local SQLite State — osforge-db

Persistent project state management via a local SQLite database (`~/.osforge/osforge.db`). No server, no network, no dependencies beyond Python's built-in `sqlite3`.

### What it stores

| Table | Content |
|---|---|
| `projects` | slug, description, triage, status |
| `phases` | per-phase status, skill used, artifact produced |
| `state` | current phase + resume point (session continuity) |
| `decisions` | architectural, product, UX, data, security decisions |
| `blockers` | active impediments + what they're waiting on |

`decisions` is backed by an **FTS5 virtual table** — full-text search across all decisions from all projects in milliseconds.

### Core commands

```bash
# Session start — load context in ~50 tokens
osforge-db resume my-project

# Record progress
osforge-db set-phase my-project "spec-builder" complete skills/planning/spec-builder docs/specs/feature.md
osforge-db add-decision my-project "Usar Prisma multi-tenant via organizationId" --category=arch

# Session end — mandatory
osforge-db set-resume my-project "Próximo: arch-builder — definir schema de billing"

# Cross-project semantic search
osforge-db search "autenticação OAuth multi-tenant"

# Full project status
osforge-db status my-project
```

### Shell injection in skills

```
# In any SKILL.md — injects ~50 tokens of precise context
!`osforge-db resume PROJETO_SLUG`
```

### Two scopes

- **Global** (`~/.osforge/osforge.db`) — cross-project state, decision history, no sensitive data
- **Local** (`.osforge/osforge.db`) — per-project, `.gitignore`-able for sensitive projects (Essent, Rede Essent Jus)

### Installed by deploy.sh

`deploy.sh` installs `osforge-db` to `~/.local/bin/` and initializes the global database automatically.

---

```
osforge/
├── .osforge/              # Project status tracking (status.yaml)
├── claude-code/
│   ├── CLAUDE.md          # Entry point for Claude Code sessions
│   ├── SKILLS.md          # 122 skill triggers (~12K base tokens)
│   └── agents/            # 26 agent definitions (.md)
├── agents/                # 26 agent source files (with Reality Check + Quality Control Loop)
│   ├── orchestrator/      # Meta-agent: AGENT.md + triage-rules + plan-templates
│   ├── frontend-engineer.md  # + Anti-Cliché Design Rules
│   ├── mobile-developer.md   # React Native + Flutter
│   ├── game-developer.md     # Game mechanics, multi-platform
│   ├── penetration-tester.md # Offensive security, red team
│   ├── code-archaeologist.md # Legacy code archaeology
│   ├── explorer-agent.md     # Codebase analysis, onboarding
│   └── ... (26 total)
├── rules/                 # 12 always-on rules (.mdc + .md) for Cursor
│   ├── intelligent-routing.mdc  # 27 domains, design taste sub-routing, automatic skill bundling
│   └── anti-ai-slop.mdc        # 40 enforced rules vs generic AI design
├── commands/              # 9 spec-* slash commands for Claude Code
├── skills/                # On-demand skill library (122 SKILL.md files)
│   ├── agency/            # 121 AI specialists — The Agency (10 divisions) + 32 marketing workflows
│   ├── app-builder/       # 13 project templates (Next.js, FastAPI, Flutter, Electron...)
│   ├── api-patterns/      # REST/GraphQL/tRPC + 10 reference modules
│   ├── game-development/  # Orchestrator + 10 sub-skills (2D, 3D, multiplayer, VR/AR...)
│   ├── mobile-design/     # Touch psychology, platform-specific + references
│   ├── frontend-design/   # Colors, typography, animation, UX + 7 references
│   ├── taste-design-dials/ # 3-dial tunable system (VARIANCE/MOTION/DENSITY) + Creative Arsenal + Bento 2.0
│   ├── aesthetic-modes/   # 3 modos: Editorial Minimalist / Industrial Brutalist / Soft Premium
│   ├── aesthetic-boost/   # Anti-AI-slop compact primer (~500 tokens)
│   ├── redesign-audit/    # Audit + cirurgia em projetos existentes
│   ├── stitch-design-export/ # DESIGN.md generator para Google Stitch
│   ├── output-enforcement/ # Anti-truncation / anti-placeholder modifier
│   ├── ui-design-intelligence/ # Design system spec por indústria (67 estilos, 161 paletas)
│   ├── architecture/      # System design patterns + 5 reference modules
│   ├── database-design/   # Schema, indexing, ORM + 6 reference modules
│   ├── nextjs-react-expert/ # 9 performance optimization modules
│   ├── red-team-tactics/  # MITRE ATT&CK offensive security
│   ├── vulnerability-scanner/ # OWASP checklists
│   ├── rust-pro/          # Ownership, async, cargo
│   ├── python-patterns/   # FastAPI, Django, Flask
│   ├── brainstorming/     # Socratic questioning + dynamic questioning
│   ├── planning/          # 6 planning skills (spec, prd, arch, epics, story, phase)
│   ├── quality/           # 6 quality skills (adversarial, code-review, edge-case, elicitation, readiness, ui-audit)
│   ├── context/           # 4 context skills (distillator, project-context, doc-shard, editorial)
│   └── ... (122 SKILL.md files total)
├── hooks/                 # Python hooks + shell scripts + config
├── mcp/                   # MCP server configs (claude-code.json, cursor.json)
├── scripts/               # Utility scripts
├── docs/                  # Internal documentation
├── osforge-architecture.html  # Interactive visual architecture map
├── deploy.sh              # One-command sync to ~/.claude/ and ~/.cursor/
└── sources/               # Upstream skill collections (gitignored — curation raw material)
```

### Token Budget

| Component | Tokens | Loaded |
|---|---|---|
| SKILLS.md (122 triggers + 12 rules) | ~12,000 | Always |
| Agent definitions (26) | ~1,500–3,000 | On invoke |
| Agency router (SKILL.md) | ~2,000 | On invoke |
| Agency division index (1 of 10) | ~1,500 | On invoke |
| Agency specialist (1 of 121) | ~2,000–4,000 | On invoke |
| Marketing workflow (1 of 32) | ~1,500–3,500 | On invoke |
| Individual SKILL.md files | ~500–3,000 each | On invoke |
| Complex skills with references | ~3,000–8,000 each | On invoke |
| Python hooks | 0 | Runtime only |
| Orchestrator AGENT.md (full routing tables) | ~5,500 | On invoke |
| Planning/Quality/Context skills | ~500–2,000 each | On invoke |
| **Base context usage** | **~12,000** | **6% of 200K** |

---

## Stack Compatibility

| Layer | Technology |
|---|---|
| Framework | Next.js 15+ (App Router) |
| Language | TypeScript (strict mode) |
| ORM | Prisma |
| Database | PostgreSQL via Supabase |
| Auth | Supabase Auth (SSR) |
| UI | shadcn/ui + Tailwind CSS |
| Runtime | Bun |
| Deployment | Vercel |
| Payments | Stripe |
| Testing | Playwright + Bun test |
| AI Tools | Claude Code, Cursor |

---

## MCP Servers (Recommended)

```jsonc
// .mcp.json (project) or ~/.claude.json (global)
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase@latest", "--read-only"],
      "env": { "SUPABASE_ACCESS_TOKEN": "your-token" }
    },
    "shadcn": {
      "command": "npx",
      "args": ["shadcn@latest", "mcp"]
    }
  }
}
```

See `mcp/claude-code.json` and `mcp/cursor.json` for full configs.

---

## Origins

OSForge was built by evaluating **1100+ agent skills, commands, and patterns across 23 sources**, curating e adaptando os mais relevantes em um framework unificado:

| Source | Repository | Focus |
|---|---|---|
| **Anthropic** | [anthropics/skills](https://github.com/anthropics/skills) ⭐ 63.9k | Official skills: docx, pdf, pptx, xlsx, mcp-builder, frontend-design |
| **Anthropic (Plugin)** | [anthropics/claude-code/plugins/frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) ⭐ 66.5k | Anti-convergence aesthetics, aesthetic-boost inspiration, complexity matching (277K+ installs) |
| **Antigravity** | [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) ⭐ 7.4k | 634+ universal skills (curated subset) |
| **Antigravity Kit** | [vudovn/antigravity-kit](https://github.com/vudovn/antigravity-kit) ⭐ 4.2k | 32 skills adapted (app-builder, api-patterns, game-dev, mobile-design, red-team, rust, python, etc.) + 15 agents + Reality Check/Quality Control Loop patterns |
| **autoresearch** | [karpathy/autoresearch](https://github.com/karpathy/autoresearch) ⭐ 39k | Autonomous research loop pattern (modify→evaluate→keep/discard→repeat) — inspired `autorefine-skill` |
| **BMAD-METHOD** | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) ⭐ 35.4k | Orchestration patterns: intake, triage, multi-phase planning, quality gates, artifact chains |
| **claude-mem** | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) ⭐ 23.3k | Persistent memory for Claude Code |
| **Cloudflare** | [cloudflare/skills](https://github.com/cloudflare/skills) ⭐ 233 | Workers, Agents SDK, Durable Objects |
| **Context Engineering** | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) ⭐ 8.1k | Context engineering patterns |
| **Curated lists** | [VoltAgent](https://github.com/VoltAgent/awesome-agent-skills) / [travisvn](https://github.com/travisvn/awesome-claude-skills) | Awesome lists used for discovery and curation |
| **Expo** | [expo/skills](https://github.com/expo/skills) ⭐ 878 | Mobile Expo / React Native |
| **GSD (get-shit-done)** | [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) ⭐ 34.3k | Phase discussion, wave execution, UI audit, STATE.md cross-session memory |
| **llmfit** | [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) ⭐ 6.5k | Hardware-aware local LLM recommendations |
| **Marketing Skills** | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) ⭐ 16.8k | 32 marketing execution workflows: CRO, copywriting, SEO, paid ads, sales enablement, RevOps |
| **Sentry** | [getsentry/skills](https://github.com/getsentry/skills) ⭐ 173 | Code review, PR workflow |
| **Supabase** | [supabase/agent-skills](https://github.com/supabase/agent-skills) ⭐ 1.1k | PostgreSQL optimization, Supabase patterns |
| **Superpowers (obra)** | [obra/superpowers](https://github.com/obra/superpowers) ⭐ 118k | brainstorming, finishing-a-branch, receiving-review, git worktrees, two-stage task review pattern |
| **taste-skill (Leonxlnx)** | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) ⭐ 10k | High-Agency Frontend — 3-dial tunable system (DESIGN_VARIANCE/MOTION_INTENSITY/VISUAL_DENSITY), GSAP scrolltelling, double-bezel cards, perpetual micro-physics, Bento 2.0 paradigm. Inspired `taste-design-dials`, `aesthetic-modes`, `redesign-audit`, `output-enforcement`, `stitch-design-export`. |
| **agentic-ai-prompt-research (Leonxlnx)** | [Leonxlnx/agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research) ⭐ 1.6k | Reverse-engineering research of Claude Code internal architecture. Reconstructed prompts for coordinator, classifier, compaction, memory hierarchy, stuck recovery. Inspired `tool-safety-classifier`, `context-compact`, `config-critique`, `stuck-recovery`, `memory-hierarchy.mdc` rule, Coordinator Protocol enrichment, Cache Boundary documentation. |
| **The Agency** | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) ⭐ 31k | 121 AI specialists across 10 business divisions |
| **Trail of Bits** | [trailofbits/skills](https://github.com/trailofbits/skills) ⭐ 2.4k | Enterprise security auditing methodology |
| **UI-UX Pro Max** | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) ⭐ 39k | Design intelligence database: 67 styles, 161 palettes, 57 font pairs, 99 UX guidelines, 25 chart types |
| **Vercel Labs** | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) ⭐ 19.1k | React, Next.js performance, Core Web Vitals |
| **spec-kit (GitHub)** | [github/spec-kit](https://github.com/github/spec-kit) ⭐ 81.4k | requirements-clarify, constitution.md pattern, artifact DAG |
| **OpenSpec (Fission-AI)** | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) ⭐ 23.8k | delta/brownfield spec pattern for incrementally extending existing features |
| **shanraisshan best-practice** | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) ⭐ 19.7k | frontmatter patterns (model, context:fork, allowed-tools), shell injection, Gotchas sections |

> **Breakdown:** 116 SKILL.md files · 26 specialized agents · 121 Agency specialists · 32 marketing execution workflows · 85 trigger entries · 12 always-on rules · 21 detectable domains · 13 project templates · 10 game sub-skills · 9 Next.js optimization modules · 33 GSD commands · ~50 BMAD orchestration patterns · 5 UI-UX Pro Max reference databases · 2 tool patterns (llmfit + autoresearch)

---

## License

MIT — See [LICENSE](LICENSE)

## Author

**Paulo Souza** — [@plocemourasouza](https://github.com/plocemourasouza)

*Forging the development environment for AI-powered teams.*
