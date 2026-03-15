# 🔨 OSForge

**Curated agent skills, agents, rules, hooks, and a full AI specialist library for AI-powered development.**

OSForge is a production-grade package of 31 skills, 7 specialized agents, 4 always-on rules, Python hooks, and **121 on-demand AI specialists** — optimized for the **Next.js + TypeScript + Prisma + Supabase + Bun** stack. Built for Claude Code and Cursor.

> *"Forging the development environment for AI-powered teams."*

---

## Why OSForge?

AI coding agents are only as good as the context they receive. OSForge solves three problems:

1. **Context efficiency** — Skills and agents load on-demand, not upfront. Zero idle token cost.
2. **Stack-specific patterns** — Every skill is tailored for Next.js App Router + Prisma + Supabase + shadcn/ui.
3. **Quality gates built-in** — TDD enforcement, security auditing, insecure defaults detection, and Python hooks that catch issues before they ship.

---

## Quick Start

```bash
# Clone
git clone https://github.com/plocemourasouza/osforge.git

# Copy to Claude Code
cp osforge/claude-code/SKILLS.md ~/.claude/SKILLS.md
cp -r osforge/claude-code/agents/ ~/.claude/agents/

# Copy to Cursor
cp osforge/claude-code/SKILLS.md ~/.cursor/SKILLS.md

# (Optional) Install hooks in your project
cp -r osforge/skills/smart-hooks/scripts/*.py your-project/.claude/hooks/
```

---

## What's Inside

### 31 Skills

| # | Skill | Category |
|---|---|---|
| 1 | TDD Workflow (RED-GREEN-REFACTOR) | Core |
| 2 | Verification Before Completion | Core |
| 3 | Security Best Practices | Security |
| 4 | Coding Guidelines (Karpathy Rules) | Core |
| 5 | Product-Driven Spec Development (PDD) | Core |
| 6 | React & Next.js Performance | Performance |
| 7 | PostgreSQL & Supabase Optimization | Performance |
| 8 | Frontend UI System (shadcn) | Frontend |
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


### 7 Agents

| Agent | Role |
|---|---|
| **planner** | Architecture, decomposition, story creation (★ Synkra-enhanced) |
| **debugger** | 10-step autonomous debugging |
| **code-reviewer** | Code quality + YAML-structured review output |
| **security-auditor** | Trail of Bits methodology |
| **frontend-engineer** | shadcn/ui + Server Components specialist |
| **backend-engineer** | Prisma + Supabase + Server Actions |
| **validator** | Spec critique + acceptance verification |

### 4 Always-On Rules

- **TypeScript Strict Mode** — `strict: true` + `noUncheckedIndexedAccess` + no `any`
- **Code Style** — Product thinking (PDD), naming conventions, import order
- **Commit Conventions** — Conventional commits enforced
- **TDD Enforcement** — No production code without failing test first

### Python Hooks (zero token cost)

- `pre_tool_use.py` — Blocks dangerous commands, protects `.env` files, audit logging
- `post_tool_use.py` — TypeScript quality gates (console.log, any, @ts-ignore)
- `pre_compact.py` — Conversation backup before context compaction
- `session_end.py` — Session logging + macOS notification

---

## 🏢 The Agency — 121 AI Specialists (on-demand)

OSForge includes **The Agency**: a curated library of 121 specialized AI agents covering every business and technical function. Each specialist loads only when activated — zero idle context cost.

### 10 Divisions

| Division | Specialists | When to use |
|---|---|---|
| 💻 **Engineering** | 23 | Código, arquitetura, segurança, DevOps, SRE, documentação |
| 🎨 **Design** | 8 | UI/UX, sistemas de design, identidade visual, pesquisa com usuários |
| 📢 **Marketing** | 26 | Conteúdo, SEO, redes sociais, growth hacking, ASO |
| 💰 **Paid Media** | 7 | Google/Meta Ads, PPC, tracking, auditoria de contas |
| 📊 **Product** | 5 | Roadmap, sprint, pesquisa de mercado, síntese de feedback |
| 🎬 **Project Management** | 6 | Planejamento, Jira/Git workflows, rastreamento de experimentos |
| 💼 **Sales** | 8 | Prospecção, discovery, qualificação, propostas, pipeline |
| 🛟 **Support & Ops** | 6 | Atendimento, analytics, compliance, resumos executivos |
| 🧪 **Testing** | 8 | QA, API testing, WCAG, performance, validação de entregáveis |
| 🎯 **Specialized** | 24 | Orquestração de agentes, compliance, blockchain, MCP builder |

### How to activate a specialist

```
# Step 1 — Find the right division
"Leia skills/agency/SKILL.md"

# Step 2 — Browse the division's agents
"Leia skills/agency/engineering/SKILL.md"

# Step 3 — Activate the specialist
"Ative o Security Engineer"
```

### High-risk agents (⚠️ checkpoint required)

Four agents can execute autonomous actions with real-world impact. They have a mandatory human approval checkpoint built into their `.md` file — they will always present a plan and wait for explicit confirmation before acting:

- `specialized/accounts-payable-agent.md` — autonomous payments (crypto, fiat, stablecoins)
- `marketing/marketing-carousel-growth-engine.md` — autonomous social media publishing
- `specialized/report-distribution-agent.md` — automated email/report distribution
- `specialized/agentic-identity-trust.md` — inter-agent trust configuration

> Source: [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (MIT) — game-development division excluded.


---

## Architecture

```
osforge/
├── claude-code/
│   ├── SKILLS.md          # Condensed skill triggers (~6.7K tokens)
│   ├── agents/            # 7 agent definitions (.md)
│   └── rules/             # 4 always-on rules (.mdc)
├── skills/                # 37 SKILL.md files (loaded on-demand)
│   ├── agency/            # 121 AI specialists across 10 divisions
│   │   ├── SKILL.md       # Router — identifica divisão e agente
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
│   ├── claude-api-typescript/
│   ├── smart-hooks/
│   ├── prisma-expert/
│   ├── stripe-integration/
│   └── ... (37 total)
└── _skills/               # Source repositories index (770 skills)
```

### Token Budget

| Component | Tokens | Loaded |
|---|---|---|
| SKILLS.md (31 triggers + 4 rules) | ~6,709 | Always |
| Agent definitions (7) | ~958 | On invoke |
| Agency router (SKILL.md) | ~2,000 | On invoke |
| Agency division index (1 of 10) | ~1,500 | On invoke |
| Agency specialist (1 of 121) | ~2,000–4,000 | On invoke |
| SKILL.md files (37) | ~15,000 | On invoke |
| Reference files (claude-api) | ~20,000 | On invoke |
| Python hooks | 0 | Runtime (no tokens) |

---

## Stack Compatibility

OSForge is optimized for:

- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript (strict mode)
- **ORM:** Prisma
- **Database:** PostgreSQL via Supabase
- **Auth:** Supabase Auth (SSR)
- **UI:** shadcn/ui + Tailwind CSS
- **Runtime:** Bun
- **Deployment:** Vercel
- **Payments:** Stripe
- **Testing:** Playwright + Bun test
- **AI Tools:** Claude Code, Cursor

---

## MCP Servers (Recommended)

OSForge works best with these MCP servers configured:

```jsonc
// .mcp.json
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
    }
  }
}
```

---

## Origins

OSForge was built by curating and consolidating 770+ agent skills from 12 sources:

- Anthropic (official skills + claude-api)
- Superpowers (SDD workflow)
- Trail of Bits (security methodology)
- Vercel (React/Next.js performance)
- Supabase (Postgres optimization)
- Context Engineering principles
- msitarzewski/agency-agents (121 specialists — The Agency)
- And 5 other community sources

Each skill was evaluated for stack relevance, token efficiency, and superiority over alternatives.

---

## License

MIT — See [LICENSE](LICENSE)

## Author

**Paulo Souza** — [@plocemourasouza](https://github.com/plocemourasouza)

*Forging the development environment for AI-powered teams.*
