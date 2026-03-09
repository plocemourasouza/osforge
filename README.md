# 🔨 OSForge

**Curated agent skills, agents, rules, and hooks for AI-powered development.**

OSForge is a production-grade package of 31 skills, 7 specialized agents, 4 always-on rules, and Python hooks — optimized for the **Next.js + TypeScript + Prisma + Supabase + Bun** stack. Built for Claude Code and Cursor.

> *"Forging the development environment for AI-powered teams."*

---

## Why OSForge?

AI coding agents are only as good as the context they receive. OSForge solves three problems:

1. **Context efficiency** — 31 skills in ~6.7K tokens (3.35% of 200K context window). Skills load on-demand, not upfront.
2. **Stack-specific patterns** — Every skill is tailored for Next.js App Router + Prisma + Supabase + shadcn/ui. No generic filler.
3. **Quality gates built-in** — TDD enforcement, security auditing, insecure defaults detection, and Python hooks that catch issues before they ship.

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

## Architecture

```
osforge/
├── claude-code/
│   ├── SKILLS.md          # Condensed skill triggers (~6.7K tokens)
│   ├── agents/            # 7 agent definitions (.md)
│   └── rules/             # 4 always-on rules (.mdc)
├── skills/                # 37 SKILL.md files (loaded on-demand)
│   ├── claude-api-typescript/
│   │   ├── SKILL.md
│   │   ├── typescript/    # Claude API + Agent SDK reference files
│   │   └── shared/        # Models, error codes, tool-use concepts
│   ├── smart-hooks/
│   │   ├── SKILL.md
│   │   └── scripts/       # Python hooks + config
│   ├── prisma-expert/
│   ├── stripe-integration/
│   ├── ... (37 total)
│   └── skill-creator/     # Skill eval system (3 agents, 9 scripts)
└── _skills/               # Source repositories index (770 skills)
```

### Token Budget

| Component | Tokens | Loaded |
|---|---|---|
| SKILLS.md (31 triggers + 4 rules) | ~6,709 | Always |
| Agent definitions (7) | ~958 | On invoke |
| SKILL.md files (37) | ~15,000 | On invoke |
| Reference files (claude-api) | ~20,000 | On invoke |
| Python hooks | 0 | Runtime (no tokens) |
| **Total potential** | **~42,667** | |
| **Context usage** | **3.35%** | of 200K window |

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

## Origins

OSForge was built by curating and consolidating 770+ agent skills from 12 sources:

- Anthropic (official skills + claude-api)
- Superpowers (SDD workflow)
- Trail of Bits (security methodology)
- Vercel (React/Next.js performance)
- Supabase (Postgres optimization)
- Context Engineering principles
- And 6 other community sources

Each skill was evaluated for stack relevance, token efficiency, and superiority over alternatives. Only the best patterns made it in.

## License

MIT — See [LICENSE](LICENSE)

## Author

**Paulo Souza** — [@plocemourasouza](https://github.com/plocemourasouza)

*Forging the development environment for AI-powered teams.*
