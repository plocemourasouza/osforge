# 🔨 OSForge

**Framework de desenvolvimento AI-powered: skills, agents, rules, hooks, commands e uma biblioteca completa de especialistas.**

OSForge é a fonte da verdade para a configuração global do Claude Code (`~/.claude/`) e do Cursor (`~/.cursor/`). 169 skills on-demand, 27 agents especializados, 13 always-on rules, 9 spec commands, Python hooks, SQLite local state com task board cross-projeto, 121 especialistas de negócio, e UI generativa local — otimizado para **Next.js + TypeScript + Prisma + Supabase + Bun**, com suporte a mobile, game dev, Rust, Python e mais.

> *"Forging the development environment for AI-powered teams."*

📖 **[Guia completo de uso → USAGE.md](USAGE.md)** · 💡 **[Exemplos → docs/EXAMPLES.md](docs/EXAMPLES.md)** · 🗺️ **[Mapa de arquitetura → osforge-architecture.html](osforge-architecture.html)**

---

## Por que OSForge?

AI coding agents são tão bons quanto o contexto que recebem. OSForge resolve três problemas:

1. **Eficiência de contexto** — 169 skills em ~12K tokens base (~6% de 200K). Tudo mais carrega on-demand.
2. **Padrões específicos de stack** — Skills otimizadas para Next.js App Router + Prisma + Supabase + shadcn/ui, com cobertura ampliada para mobile, game dev, Rust, Python e cross-platform.
3. **Quality gates embutidos** — TDD enforcement, security auditing, red team, insecure defaults detection, Reality Check + Quality Control Loop em todo agente, e Python hooks a custo zero de tokens.
4. **Estado local SQLite** — `osforge-db` persiste estado de projeto, decisões, blockers e task board (waves, dependências, prioridades) com view cross-projeto. Retomada de sessão em ~50 tokens.
5. **OSForge Canvas** — UI generativa local: todo spec e plano aparece como artifact interativo no browser (cards, tabelas, dependency graphs, checklists, botões approve/edit/reject). Zero APIs externas.

---

## Quick Start

```bash
git clone https://github.com/plocemourasouza/osforge.git
cd osforge
./deploy.sh
```

`deploy.sh` sincroniza tudo para `~/.claude/` e `~/.cursor/` automaticamente. Veja [USAGE.md](USAGE.md) para opções manuais e avançadas.

**Próximos passos:**
- **Uso e workflows** → [USAGE.md](USAGE.md)
- **Índice de skills (169 skills + triggers)** → [claude-code/SKILLS.md](claude-code/SKILLS.md)
- **Orquestração de sessão e agents** → [claude-code/CLAUDE.md](claude-code/CLAUDE.md)

---

## What's Inside

### 169 Skills on-demand

Índice completo com triggers em [claude-code/SKILLS.md](claude-code/SKILLS.md). Categorias principais:

- **Core & Workflow** — TDD, Verification Before Completion, Security Best Practices, Coding Guidelines (Karpathy Rules), Git, Clean Code, Spec/PRD/Architecture builders, Epic Decomposer, Story Executor
- **Frontend & UI** — React + Next.js Expert (9 módulos), shadcn/ui, Tailwind v4, Frontend Design, Aesthetic Boost, Design Taste Dials, Aesthetic Modes (Editorial Minimalist / Industrial Brutalist / Soft Premium), Redesign Audit, Core Web Vitals, Accessibility (WCAG), i18n, SEO/GEO
- **Backend & Database** — Prisma Expert, PostgreSQL + Supabase, Auth (SSR), Stripe, API Patterns (REST/GraphQL/tRPC), Database Design, Node.js, Bun, Server Management
- **Security** — Red Team Tactics (MITRE ATT&CK), Vulnerability Scanner (OWASP), Insecure Defaults Detection, GDPR/LGPD; + 27 skills de offensive security (claude-red, authorized testing only)
- **Testing & Quality** — E2E Playwright, Testing Patterns, Adversarial Review, Code Review, Edge Case Hunter, UI Audit, Readiness Gate, Output Enforcement
- **Meta & Context** — Systematic Debugging, Performance Profiling, Smart Model Dispatch, llmfit Advisor, Context Distillator, osforge-db, OSForge Canvas, Stuck Recovery, Config Critique, Context Compact, Tool Safety Classifier, Evolve/Instinct
- **The Agency** — 121 especialistas AI em 10 divisões (Engineering, Design, Marketing, Paid Media, Product, Project Management, Sales, Support, Testing, Specialized) + 32 marketing execution workflows

### 27 Agents especializados

Todos incluem Reality Check (anti-auto-engano) e Quality Control Loop (verificação obrigatória). Roster completo em [USAGE.md](USAGE.md).

- **Orchestrator** — meta-agente: intake, triage, planejamento, routing para 26 agentes, tracking cross-session
- **Engineering** — frontend-engineer, backend-engineer, database-architect, mobile-developer, game-developer, devops-engineer, performance-optimizer
- **Quality & Security** — code-reviewer, code-refactorer, security-auditor, penetration-tester, test-engineer, qa-automation-engineer, validator
- **Planning & Product** — planner, system-architect, project-planner, product-manager, product-owner, product-strategy-advisor
- **Investigation** — debugger, explorer-agent, code-archaeologist
- **Docs & SEO** — documentation-writer, seo-specialist, git-commit-helper

### 11 Always-On Rules (Cursor)

TypeScript Strict, Code Style, Product Thinking (PDD), TDD Enforcement, Next.js Patterns, Security Mindset, Intelligent Routing, Anti-AI-Slop, Commit Conventions, Agent Skills Reference, Memory Hierarchy, Artifact Chain, Orchestrator Awareness (13 = 11 `.mdc` + 2 `.md`). Lista completa em [USAGE.md](USAGE.md).

### 9 Spec Commands (`/spec-*`)

`/spec-discover` · `/spec-specify` · `/spec-design` · `/spec-tasks` · `/spec-implement` · `/spec-clarify` · `/spec-checklist` · `/spec-constitution` · `/spec-measure`

Ver [USAGE.md](USAGE.md) para o fluxo spec-driven completo.

### Hooks (custo zero de tokens)

Executados pelo runtime — não consomem tokens de contexto:

- **GateGuard** (`gateguard.py`, PreToolUse Bash) — bloqueia só o irreversível/compartilhado (`rm -rf`, `git push --force`, `reset --hard`, `clean -f`, SQL `DROP/TRUNCATE/DELETE`); kill-switch `OSFORGE_GATEGUARD=off`
- **scan-secrets** (`scan-secrets.sh`, PreToolUse Bash) — bloqueia segredos antes de commit
- **protect-tests** (`protect-tests.sh`, PostToolUse) — alerta se um arquivo de teste foi alterado
- **observe→evolve** (`observe-capture.py`, PostToolUse) — grava observações p/ o `osforge-db evolve`
- **Auto-resume** (`session-resume.sh` / `session-save.py`) — SessionStart injeta `osforge-db resume`; Stop grava `set-resume` automático
- **Canvas autostart** (`canvas-autostart.sh`, SessionStart) — sobe o servidor Canvas (porta 4242) se necessário
- **observe→evolve** — captura padrões de sessão para evolução contínua das skills
- **scan-secrets** e **protect-tests** — previnem commits de segredos e alteração de testes

### osforge-db — Estado SQLite + Memória Local

CLI Python com banco SQLite (`~/.osforge/osforge.db`). Sem servidor, sem rede. Persiste projetos, fases, tasks (wave/depends_on), decisões com FTS5 full-text search, e blockers. Retomada de sessão em ~50 tokens via `osforge-db resume <slug>`. View cross-projeto via `osforge-db board`.

Ver comandos detalhados em [USAGE.md](USAGE.md).

### OSForge Canvas — UI Generativa Local

Serviço Bun local em `localhost:4242`. O agente escreve artifacts JSON versionados; o browser renderiza cards, tabelas, dependency graphs, gantt, checklists e botões de decisão com SSE live-reload. Feedback retorna como JSON estruturado. Default para todo spec e plano — opt-out com "só texto".

---

## Design Taste System

Integrado do [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT, 10k+ stars). Sistema completo de frontend premium com três dials ajustáveis (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY), 3 modos estéticos por projeto, e workflow de audit + upgrade cirúrgico para projetos existentes. Inclui anti-AI-slop rule com 40 anti-patterns, GSAP scrolltelling, Bento 2.0, double-bezel cards e micro-physics.

Ver detalhes em [USAGE.md](USAGE.md) e skills `taste-design-dials`, `aesthetic-modes`, `redesign-audit`.

## Agentic AI Patterns

Integrado do [Leonxlnx/agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research) (1.6k+ stars). Padrões de infraestrutura agentic: `tool-safety-classifier`, `context-compact`, `config-critique`, `stuck-recovery`, `memory-hierarchy.mdc`, Coordinator Protocol no orchestrator, e documentação de Cache Boundary para Anthropic API (~10% de redução de custo no prefixo estável).

## The Agency — 121 Especialistas AI

121 especialistas de negócio em 10 divisões, carregados on-demand. 32 marketing execution workflows (CRO, copywriting, SEO, paid ads, sales enablement, RevOps). Arquitetura: Agent (persona: *quem sou*) + Workflow (execução: *o que faço*). 4 agentes requerem aprovação humana obrigatória antes de qualquer ação autônoma.

Ver roster completo em [USAGE.md](USAGE.md) e `skills/agency/`.

## llmfit Advisor

Detecta seu hardware (RAM, CPU, GPU/VRAM) e recomenda quais LLMs locais rodam bem na sua máquina — quantização ótima, estimativas de velocidade e fit scoring para 497 modelos de 133 providers. Útil para dados LGPD-sensíveis e projetos sem budget de API.

> Fonte: [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) (MIT). Instalar: `brew install llmfit` ou `cargo install llmfit`.

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

**MCP Servers** — 8 MCPs configurados (Context7, GitHub, Supabase, Shadcn, Browsermcp, next-devtools, Prisma-Local, Prisma-Remote). Ver `mcp/claude-code.json`.

---

## Origins

Construído a partir de 1100+ agent skills, commands e padrões de 23 fontes curadas e adaptadas: Anthropic, BMAD-METHOD, GSD, taste-skill, agentic-ai-prompt-research, The Agency, Trail of Bits, Vercel Labs, Supabase, Expo, Marketing Skills, llmfit, UI-UX Pro Max, spec-kit, OpenSpec, claude-red, e outros. 10 ADRs documentam decisões arquiteturais em [docs/DECISIONS.md](docs/DECISIONS.md).

---

## License

MIT — See [LICENSE](LICENSE)

## Author

**Paulo Souza** — [@plocemourasouza](https://github.com/plocemourasouza)

*Forging the development environment for AI-powered teams.*
