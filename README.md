# 🔨 OSForge

**Curated agent skills, agents, rules, hooks, commands, and a full AI specialist library for AI-powered development.**

OSForge is a production-grade AI development framework with **47 on-demand skills**, **12 specialized agents**, **10 always-on rules**, **9 spec commands**, **Python hooks**, and **121 business specialists** — optimized for the **Next.js + TypeScript + Prisma + Supabase + Bun** stack. Built for Claude Code and Cursor.

> *"Forging the development environment for AI-powered teams."*

📖 **[Full usage guide → USAGE.md](USAGE.md)**

---

## Why OSForge?

AI coding agents are only as good as the context they receive. OSForge solves three problems:

1. **Context efficiency** — 47 skills in ~9.5K base tokens (3.4% of 200K window). Everything else loads on-demand.
2. **Stack-specific patterns** — Every skill is tailored for Next.js App Router + Prisma + Supabase + shadcn/ui.
3. **Quality gates built-in** — TDD enforcement, security auditing, insecure defaults detection, and Python hooks that run at zero token cost.

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

### 47 Skills (on-demand)

| # | Skill | Category |
|---|---|---|
| 1 | TDD Workflow (RED-GREEN-REFACTOR) | Core |
| 2 | Verification Before Completion | Core |
| 3 | Security Best Practices | Security |
| 4 | Coding Guidelines (Karpathy Rules) | Core |
| 5 | Product-Driven Spec Development (PDD) | Core |
| 6 | React & Next.js Performance | Performance |
| 7 | PostgreSQL & Supabase Optimization | Performance |
| 8 | Frontend UI System (shadcn/ui) | Frontend |
| 9 | Git Workflow | Core |
| 10 | Predictive Failure Analysis | Meta |
| 11 | Core Web Vitals | Performance |
| 12 | Accessibility (WCAG 2.1) | Frontend |
| 13 | SEO | Frontend |
| 14 | Doc Sanitization | Docs |
| 15 | Agent Skills Search | Meta |
| 16 | Prisma Expert | Stack |
| 17 | Next.js + Supabase Auth | Stack |
| 18 | E2E Testing (Playwright) | Testing |
| 19 | Stripe Integration | Stack |
| 20 | Bun Development | Stack |
| 21 | MCP Builder | Meta |
| 22 | i18n & Localization | Stack |
| 23 | GDPR / LGPD Data Handling | Compliance |
| 24 | Insecure Defaults Detection | Security |
| 25 | Differential Review | Security |
| 26 | Dispatching Parallel Agents | Meta |
| 27 | Claude API & Agent SDK (TypeScript) | API |
| 28 | Claude CI/CD Actions | CI/CD |
| 29 | Smart Model Dispatch | Optimization |
| 30 | Context7 Docs-First | Meta |
| 31 | Smart Hooks (Python) | DX |
| 32 | llmfit Advisor (Local LLM Hardware Fit) | Optimization |
| 33 | The Agency (121 AI Specialists) | Meta |
| 34 | Spec Builder (Collaborative) | Planning |
| 35 | PRD Builder (Collaborative) | Planning |
| 36 | Architecture Builder (ADR) | Planning |
| 37 | Epic Decomposer | Planning |
| 38 | Story Executor | Planning |
| 39 | Adversarial Review | Quality |
| 40 | Code Review (OSForge Stack) | Quality |
| 41 | Edge Case Hunter | Quality |
| 42 | Elicitation Engine | Quality |
| 43 | Readiness Gate | Quality |
| 44 | Context Distillator | Context |
| 45 | Project Context Generator | Context |
| 46 | Doc Shard | Context |
| 47 | Editorial Review | Context |

### 12 Agents (on-demand)

| Agent | Role |
|---|---|
| **orchestrator** | Intake, triage, planning, routing, tracking, course correction (always-active meta-agent) |
| **planner** | Architecture, decomposition, story creation (★ Synkra-enhanced) |
| **debugger** | 10-step autonomous debugging |
| **code-reviewer** | Code quality + YAML-structured review output |
| **code-refactorer** | Refactoring patterns and clean code |
| **security-auditor** | Trail of Bits methodology |
| **frontend-engineer** | shadcn/ui + Server Components specialist |
| **backend-engineer** | Prisma + Supabase + Server Actions |
| **validator** | Spec critique + acceptance verification |
| **system-architect** | System design and ADRs |
| **product-strategy-advisor** | Product strategy and roadmap |
| **git-commit-helper** | Conventional commits and release notes |

### 10 Always-On Rules (Cursor)

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

### 9 Spec Commands (Claude Code)

Slash commands for spec-driven development (`/spec:*`):

| Command | Purpose |
|---|---|
| `/spec:discover` | Explore problem space and gather requirements |
| `/spec:specify` | Write formal specification |
| `/spec:design` | Technical design and ADR |
| `/spec:tasks` | Break down into implementable tasks |
| `/spec:implement` | Execute implementation with guardrails |
| `/spec:clarify` | Clarification loop for ambiguous specs |
| `/spec:checklist` | Pre-ship quality checklist |
| `/spec:constitution` | Define project principles and constraints |
| `/spec:measure` | Define and track success metrics |

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
| 📢 Marketing | 26 | Conteúdo, SEO, redes sociais, growth hacking, ASO |
| 💰 Paid Media | 7 | Google/Meta Ads, PPC, tracking, auditoria de contas |
| 📊 Product | 5 | Roadmap, sprint, pesquisa de mercado, síntese de feedback |
| 🎬 Project Management | 6 | Planejamento, Jira/Git workflows, rastreamento de experimentos |
| 💼 Sales | 8 | Prospecção, discovery, qualificação, propostas, pipeline |
| 🛟 Support & Ops | 6 | Atendimento, analytics, compliance, resumos executivos |
| 🧪 Testing | 8 | QA, API testing, WCAG, performance, validação de entregáveis |
| 🎯 Specialized | 24 | Orquestração, compliance SOC2/ISO, blockchain, MCP builder |

> ⚠️ Four agents require mandatory human approval before any autonomous action. See [USAGE.md](USAGE.md#high-risk-agents).

---

## 🔍 llmfit Advisor — Local LLM Hardware Fit

Detects your hardware (RAM, CPU, GPU/VRAM) and recommends which local LLMs will actually run well on your machine — with optimal quantization, speed estimates, and fit scoring across 497 models from 133 providers.

**Requires:** `brew install llmfit` or `cargo install llmfit`

Key use cases: LGPD-sensitive data (Tressen/Red Caveat), OSystems clients without API budget, and high-volume repetitive dev tasks where local models eliminate API costs.

> Source: [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) (MIT)

---
## Architecture

```
osforge/
├── .osforge/              # Project status tracking (status.yaml)
├── claude-code/
│   ├── CLAUDE.md          # Entry point for Claude Code sessions
│   ├── SKILLS.md          # 47 skill triggers (~9.5K base tokens)
│   └── agents/            # 12 agent definitions (.md)
├── agents/                # Agent source files
├── rules/                 # 10 always-on rules (.mdc + .md) for Cursor
├── commands/              # 9 spec:* slash commands for Claude Code
├── skills/                # On-demand skill library
│   ├── agency/            # 121 AI specialists — The Agency
│   │   ├── SKILL.md       # Router — identifies division and agent
│   │   ├── engineering/   # SKILL.md + 23 agents
│   │   ├── design/        # SKILL.md + 8 agents
│   │   ├── marketing/     # SKILL.md + 26 agents
│   │   ├── paid-media/    # SKILL.md + 7 agents
│   │   ├── product/       # SKILL.md + 5 agents
│   │   ├── project-management/ # SKILL.md + 6 agents
│   │   ├── sales/         # SKILL.md + 8 agents
│   │   ├── support/       # SKILL.md + 6 agents
│   │   ├── testing/       # SKILL.md + 8 agents
│   │   └── specialized/   # SKILL.md + 24 agents
│   ├── llmfit-advisor/    # Local LLM hardware fit advisor
│   ├── smart-model-dispatch/  # Claude API tier routing
│   ├── smart-hooks/       # Python hooks source
│   ├── claude-api-typescript/ # Claude API + Agent SDK reference
│   ├── prisma-expert/
│   ├── stripe-integration/
│   ├── planning/           # 5 planning skills (spec, prd, arch, epics, story)
│   ├── quality/            # 5 quality skills (adversarial, code-review, edge-case, elicitation, readiness)
│   ├── context/            # 4 context skills (distillator, project-context, doc-shard, editorial)
│   └── ... (47 total)
├── hooks/                 # Python hooks + shell scripts + config
├── mcp/                   # MCP server configs (claude-code.json, cursor.json)
├── scripts/               # Utility scripts
├── docs/                  # Internal documentation
├── deploy.sh              # One-command sync to ~/.claude/ and ~/.cursor/
└── _skills/               # Source repositories index (770+ skills curated)
```

### Token Budget

| Component | Tokens | Loaded |
|---|---|---|
| SKILLS.md (47 triggers + 10 rules) | ~9,500 | Always |
| Agent definitions (12) | ~1,300 | On invoke |
| Agency router (SKILL.md) | ~2,000 | On invoke |
| Agency division index (1 of 10) | ~1,500 | On invoke |
| Agency specialist (1 of 121) | ~2,000–4,000 | On invoke |
| Individual SKILL.md files | ~500–3,000 each | On invoke |
| Python hooks | 0 | Runtime only |
| Orchestrator AGENT.md | ~3,500 | On invoke |
| Planning/Quality/Context skills | ~500–2,000 each | On invoke |
| **Base context usage** | **~9,500** | **4.7% of 200K** |

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

OSForge was built by curating 770+ agent skills from 15 sources, evaluated for stack relevance, token efficiency, and quality:

| Source | Repository | Focus |
|---|---|---|
| **Anthropic** | [anthropics/skills](https://github.com/anthropics/skills) ⭐ 63.9k | Official skills: docx, pdf, pptx, xlsx, mcp-builder, frontend-design |
| **Superpowers (obra)** | [obra/superpowers](https://github.com/obra/superpowers) ⭐ 45.3k | TDD workflow, spec-driven development, subagents |
| **claude-mem** | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) ⭐ 23.3k | Persistent memory for Claude Code |
| **Vercel Labs** | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) ⭐ 19.1k | React, Next.js performance, Core Web Vitals |
| **Context Engineering** | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) ⭐ 8.1k | Context engineering patterns |
| **Antigravity** | [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) ⭐ 7.4k | 634+ universal skills (curated subset) |
| **Trail of Bits** | [trailofbits/skills](https://github.com/trailofbits/skills) ⭐ 2.4k | Enterprise security auditing methodology |
| **Supabase** | [supabase/agent-skills](https://github.com/supabase/agent-skills) ⭐ 1.1k | PostgreSQL optimization, Supabase patterns |
| **Expo** | [expo/skills](https://github.com/expo/skills) ⭐ 878 | Mobile Expo / React Native |
| **Cloudflare** | [cloudflare/skills](https://github.com/cloudflare/skills) ⭐ 233 | Workers, Agents SDK, Durable Objects |
| **Sentry** | [getsentry/skills](https://github.com/getsentry/skills) ⭐ 173 | Code review, PR workflow |
| **The Agency** | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) ⭐ 31k | 121 AI specialists across 10 business divisions |
| **llmfit** | [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) ⭐ 6.5k | Hardware-aware local LLM recommendations |
| **BMAD-METHOD** | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) ⭐ 35.4k | Orchestration patterns: intake, triage, multi-phase planning, quality gates, artifact chains |
| **Curated lists** | [VoltAgent](https://github.com/VoltAgent/awesome-agent-skills) / [travisvn](https://github.com/travisvn/awesome-claude-skills) | Awesome lists used for discovery and curation |

---

## License

MIT — See [LICENSE](LICENSE)

## Author

**Paulo Souza** — [@plocemourasouza](https://github.com/plocemourasouza)

*Forging the development environment for AI-powered teams.*
