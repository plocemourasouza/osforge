# 📖 OSForge — Usage Guide

Complete installation, configuration, and day-to-day usage instructions.

> **Looking for real-world scenarios?** See [docs/EXAMPLES.md](docs/EXAMPLES.md) for 10 practical usage examples covering quick fixes, full feature flows, UI design, security audits, LGPD-safe processing, and more.

---

## Table of Contents

1. [Installation](#1-installation)
2. [Automated Deploy](#2-automated-deploy)
3. [Skills — day-to-day usage](#3-skills--day-to-day-usage)
4. [Specialized Agents](#4-specialized-agents)
5. [Always-On Rules (Cursor)](#5-always-on-rules-cursor)
6. [Spec Commands](#6-spec-commands)
7. [Orchestrator — Intelligent Workflow](#7-orchestrator--intelligent-workflow)
8. [Python Hooks](#8-python-hooks)
9. [osforge-db — Local SQLite State](#9-osforge-db--local-sqlite-state)
10. [Operação Multi-projeto — Sessão-sede e Satélites](#10-operação-multi-projeto--sessão-sede-e-satélites)
11. [The Agency — 121 Specialists](#11-the-agency--121-specialists)
12. [Smart Model Dispatch](#12-smart-model-dispatch)
13. [Recommended MCPs](#13-recommended-mcps)
14. [High-Risk Agents](#14-high-risk-agents)

---

## Getting Started — Ordem de Leitura

Novo no OSForge? Leia nesta ordem:

1. **Este USAGE.md §1-2** — instalação e deploy
2. **[`claude-code/SKILLS.md`](claude-code/SKILLS.md)** — índice de triggers das 169 skills
3. **[`claude-code/CLAUDE.md`](claude-code/CLAUDE.md)** — orquestração de sessão, workflow de agentes, regras globais

> **1 sessão = 1 projeto.** Nunca misture projetos em uma única sessão Claude Code — polui o contexto, duplica prompts de permissão e degrada a precisão do `resume`. Abra uma sessão-sede em `~/Development/osforge` para planejamento e uma sessão-satélite por projeto para execução. Detalhes completos em [§10](#10-operação-multi-projeto--sessão-sede-e-satélites).

---

## 1. Installation

### Prerequisites

- Claude Code (`npm install -g @anthropic-ai/claude-code`) or Cursor
- Bun (`curl -fsSL https://bun.sh/install | bash`)
- Git

### Clone

```bash
git clone https://github.com/plocemourasouza/osforge.git
cd osforge
```

### Optional dependencies

```bash
# llmfit — local LLM recommendations (macOS)
brew tap AlexsJones/llmfit && brew install llmfit

# llmfit — via Rust (any platform)
cargo install llmfit
```

---

## 2. Automated Deploy

`deploy.sh` syncs everything to `~/.claude/` and `~/.cursor/` in a single command.

```bash
./deploy.sh                 # Full deploy (Claude Code + Cursor)
./deploy.sh --claude-only   # Claude Code only
./deploy.sh --cursor-only   # Cursor only
./deploy.sh --dry-run       # Simulate without applying changes
./deploy.sh --with-qdrant   # Also provision vector memory (Qdrant via Docker, opt-in)
./deploy.sh --no-qdrant     # Skip Qdrant; keep SQLite vector backend (no prompt)
```

### What the deploy does

**Claude Code (`~/.claude/`)**
- Copies `CLAUDE.md` and `SKILLS.md`
- Syncs 27 agents (orchestrator + 26 specialists) to `~/.claude/agents/`
- Copies 9 `spec-*` commands to `~/.claude/commands/`
- Installs 8 hooks to `~/.claude/hooks/`
- Non-destructive MCP merge into `~/.claude.json` (hooks OSForge-managed refletem o repo; hooks de usuário preservados)

**Cursor (`~/.cursor/`)**
- Copies `SKILLS.md`
- Syncs agents to `~/.cursor/agents/`
- Copies 13 rules (11 `.mdc` + 2 `.md`) to `~/.cursor/rules/`
- Copies hook scripts

**Dependency check**
The script warns if `llmfit` is not installed and provides the install command.

### Manual deploy (without script)

```bash
# Claude Code
cp claude-code/CLAUDE.md ~/.claude/CLAUDE.md
cp claude-code/SKILLS.md ~/.claude/SKILLS.md
cp -r agents/ ~/.claude/agents/
cp -r commands/ ~/.claude/commands/
cp hooks/*.py ~/.claude/hooks/

# Cursor
cp claude-code/SKILLS.md ~/.cursor/SKILLS.md
cp -r agents/ ~/.cursor/agents/
cp -r rules/ ~/.cursor/rules/
```

---

## 3. Skills — day-to-day usage

Skills load on-demand — only when you need them. `SKILLS.md` keeps condensed triggers in the base context (~9.5K tokens). Each skill's full `SKILL.md` is only read when activated.

### How to activate a skill

Just describe what you need. Claude identifies and applies the skill automatically via trigger phrases in `SKILLS.md`. You can also activate explicitly:

```
"Read skills/tdd-workflow/SKILL.md"
"Use the security best practices skill"
"Activate smart-model-dispatch"
```

### Skills reference by category

**Core**
- `tdd-workflow` — Strict RED-GREEN-REFACTOR cycle
- `verification-before-completion` — Checklist before declaring a task done
- `coding-guidelines` — Karpathy rules + stack conventions
- `best-practices` — General quality standards
- `git-workflow` — Branching, commits, PRs

**Stack**
- `prisma-expert` — Schema, migrations, optimized queries
- `nextjs-supabase-auth` — SSR auth with Supabase
- `stripe-integration` — Webhooks, checkout, billing
- `bun-development` — Bun runtime, scripts, workspaces
- `frontend-ui-system` — shadcn/ui, Tailwind, components
- `i18n-localization` — next-intl, messages, pluralization

**Performance**
- `react-performance` — Memoization, Suspense, lazy loading
- `postgres-optimization` — Indexes, queries, explain analyze
- `core-web-vitals` — LCP, CLS, INP, Vercel metrics

**Security**
- `security-best-practices` — OWASP top 10, input validation
- `security-threat-model` — Systematic threat modeling
- `insecure-defaults` — Detects fail-open patterns
- `differential-review` — Security-focused PR review
- `gdpr-data-handling` — LGPD/GDPR compliance

**Meta / Agency**
- `smart-model-dispatch` — Opus/Sonnet/Haiku routing
- `llmfit-advisor` — Local LLMs by hardware fit
- `dispatching-parallel-agents` — Parallel agent orchestration
- `agent-skills-search` — Find available skills
- `context7-docs-first` — Up-to-date docs via Context7 MCP
- `mcp-builder` — Build MCP servers
- `skill-creator` — Create and evaluate new skills
- `autorefine-skill` — Autonomous iterative skill refinement (modify→evaluate→keep/discard loop)
- `smart-hooks` — Python quality hooks

**API**
- `claude-api-typescript` — Claude SDK, tool use, streaming
- `claude-ci-actions` — GitHub Actions with Claude

**Testing**
- `e2e-testing-patterns` — Playwright, Page Object Model

**Docs**
- `docs-writer` — Clear technical documentation
- `doc-sanitization` — PII removal, content sanitization
- `technical-design-doc-creator` — ADRs, design docs
- `tlc-spec-driven` — Full spec-driven development

**Planning** (Orchestrator skills)
- `planning/phase-discussion` — Capture implementation decisions by phase type BEFORE planning (produces CONTEXT.md)
- `planning/spec-builder` — Collaborative tech-spec facilitation with testable ACs
- `planning/prd-builder` — Collaborative PRD facilitation (problem, users, metrics, MVP)
- `planning/arch-builder` — Architecture decisions with ADRs, stack-aware
- `planning/epic-decomposer` — Decompose specs/PRDs into epics and stories
- `planning/story-executor` — Execute story implementation coordinating OSForge skills (XML task format)

**Quality** (Orchestrator skills)
- `quality/adversarial-review` — Cynical adversarial review of any artifact
- `quality/code-review` — Structured code review adapted to OSForge stack
- `quality/edge-case-hunter` — Systematic edge case enumeration
- `quality/elicitation-engine` — Iterative output refinement with structured techniques
- `quality/readiness-gate` — Pre-implementation quality gate (GO/NO-GO)
- `quality/ui-audit` — 6-pillar retroactive visual quality audit of implemented frontend code

**Context** (Orchestrator skills)
- `context/context-distillator` — Lossless document compression for LLMs
- `context/project-context-generator` — Generates project-context.md from codebase
- `context/doc-shard` — Splits large markdown docs into organized shards
- `context/editorial-review` — Editorial review: prose (copy-editing) or structure (reorganization)

**Frontend / Design**
- `accessibility` — WCAG 2.1, aria, screen readers
- `seo` — Meta tags, structured data, sitemap
- `ui-design-intelligence` — Design system spec agnóstico de stack: 67 estilos visuais, paletas por indústria, 57 pares tipográficos, 99 diretrizes UX, 25 tipos de chart

**Optimization**
- `predictive-failure` — Early risk analysis
- `vercel-deploy` — Deploy, env vars, edge config

---

## 4. Specialized Agents

Agents are personalities with a defined mission. Activated explicitly or via the frontmatter `description` field (Claude Code suggests them automatically).

### Activating an agent

```
"Use the planner to decompose this feature"
"Activate the security-auditor"
"I want the debugger to investigate this bug"
```

### Agent reference (27 agents: orchestrator + 26 specialists)

| Agent | When to use |
|---|---|
| `orchestrator` | **Start here** — intake, triage, multi-phase planning, routing, tracking, course correction |
| `planner` | Start of any feature — decomposition, architecture, stories |
| `system-architect` | System design, ADRs, architecture decisions |
| `backend-engineer` | Prisma schema, Server Actions, APIs, Supabase |
| `frontend-engineer` | shadcn/ui components, Server/Client Components, UX |
| `debugger` | Bug investigation in 10 structured steps |
| `code-reviewer` | PR review with YAML-structured output |
| `code-refactorer` | Refactoring, clean code, technical debt reduction |
| `security-auditor` | Threat modeling, security audit (Trail of Bits methodology) |
| `validator` | Critiques specs, validates acceptance criteria |
| `product-strategy-advisor` | Roadmap, prioritization, product decisions |
| `git-commit-helper` | Conventional commits, changelogs, release notes |
| `database-architect` | Schema design, indexing strategy, query optimization |
| `devops-engineer` | CI/CD, containers, infrastructure, deployment pipelines |
| `documentation-writer` | Technical docs, READMEs, API docs, changelogs |
| `mobile-developer` | React Native, Expo, mobile UX, iOS/Android patterns |
| `performance-optimizer` | Profiling, Lighthouse, bundle analysis, Core Web Vitals |
| `penetration-tester` | Offensive security, OWASP, red-team exercises |
| `qa-automation-engineer` | Test strategy, Playwright, test pyramid, coverage |
| `test-engineer` | Unit/integration tests, TDD guidance |
| `product-manager` | Requirements, user stories, backlog, product process |
| `product-owner` | Acceptance criteria, sprint goals, stakeholder alignment |
| `project-planner` | Project timelines, milestones, risk tracking |
| `seo-specialist` | Meta tags, structured data, Core Web Vitals for SEO, GEO |
| `code-archaeologist` | Legacy code analysis, reverse-engineering undocumented systems |
| `explorer-agent` | Open-ended research, technology evaluation, discovery |
| `game-developer` | Game loops, multiplayer, physics, game engine patterns |

### Combined usage pattern (full feature)

**With Orchestrator (recommended):**
```
1. orchestrator     → Intake, triage (QUICK/STANDARD/COMPLEX), generates plan
2. phase-discussion → Capture decisions per phase (STANDARD+) → produces CONTEXT.md
3. spec-builder     → Collaborative tech-spec with ACs (reads CONTEXT.md)
4. arch-builder     → Architecture decisions + ADR (if schema/API changes)
5. epic-decomposer  → Decompose into stories with XML-format tasks (STANDARD+)
6. readiness-gate   → Quality gate before coding (COMPLEX)
7. story-executor   → Implements each story; waves via dispatching-parallel-agents
8. code-review      → Review with adversarial-review + edge-case-hunter
9. ui-audit         → 6-pillar visual audit for UI phases
10. orchestrator    → Tracks progress in .osforge/status.yaml + STATE.md
```

**Without Orchestrator (direct):**
```
1. planner          → Decomposes into stories and defines architecture
2. validator        → Critiques the plan, identifies gaps
3. backend-engineer → Implements schema + Server Actions
4. frontend-engineer → Implements UI
5. code-reviewer    → Final review
6. security-auditor → Audit if sensitive data is involved
```

---

## 5. Always-On Rules (Cursor)

The 13 rules (11 `.mdc` + 2 `.md`: `artifact-chain`, `orchestrator-awareness`) are automatically active in all Cursor sessions. No activation needed.

| Rule | Effect |
|---|---|
| `typescript-strict` | Enforces `strict: true`, prohibits `any`, `enum`, `export default` |
| `tdd-enforcement` | No production code without a failing test first |
| `code-style` | Naming conventions, import order, product thinking |
| `commit-conventions` | Conventional commits enforced |
| `nextjs-patterns` | Server Components by default, `"use client"` only when necessary |
| `product-thinking` | User decision before technical decision |
| `security-mindset` | Zero-trust, fail-safe, no hardcoded secrets |
| `agent-skills-reference` | How to load and use OSForge skills |
| `orchestrator-awareness` | Check `.osforge/status.yaml` for WIP; route complex demands through Orchestrator |
| `artifact-chain` | Planning artifacts need frontmatter (`type`, `status`, `depends_on`); never skip checkpoints |
| `intelligent-routing` | Silent domain detection + automatic agent selection on every message |
| `anti-ai-slop` | Anti-patterns to avoid generic "AI-slop" output; concrete, non-hedged prose/design |
| `memory-hierarchy` | 4-layer config loading (Managed/User/Project/Local); `@include`, `paths` frontmatter |

---

## 6. Spec Commands

9 `/spec-*` commands available in Claude Code for spec-driven development.

```bash
# Full feature flow
/spec-discover    # Explore the problem, gather requirements
/spec-specify     # Write formal specification
/spec-design      # Technical design + ADR
/spec-tasks       # Break down into implementable tasks
/spec-implement   # Execute implementation with guardrails
/spec-checklist   # Pre-ship quality checklist

# Utilities
/spec-clarify     # Clarification loop for ambiguous specs
/spec-constitution # Define project principles and constraints
/spec-measure     # Define and track success metrics
```

### Usage example

```
/spec-discover "OFX reconciliation module"
→ Claude explores requirements, raises questions, maps the domain

/spec-specify
→ Generates formal spec with use cases, business rules, acceptance criteria

/spec-design
→ Prisma schema, Server Actions, data flow, ADR for key decisions

/spec-tasks
→ Prioritized task list ready for implementation

/spec-implement
→ Implements following the spec, with continuous verification

/spec-checklist
→ Validates everything was done before the PR
```

---


## 7. Orchestrator — Intelligent Workflow

The Orchestrator is OSForge's meta-agent — the "brain" that understands demands, plans solutions, and coordinates execution across all other skills and agents.

### When to use

The Orchestrator activates automatically when you describe a project, feature, problem, or any development demand. You can also activate it explicitly:

```
"Read agents/orchestrator/AGENT.md"
"Use the orchestrator to plan this feature"
```

### Triage levels

| Level | When | Example |
|---|---|---|
| **QUICK** | 1-3 files, zero ambiguity, known pattern | "Add dark mode toggle", "Fix the 404 on /pricing" |
| **STANDARD** | Multi-file, known domain, may need schema changes | "Add Stripe subscription module", "Implement team invites" |
| **COMPLEX** | New system, ambiguous requirements, multiple stakeholders | "Build a B2B marketplace", "Migrate auth to SSO" |

### Workflow phases

```
INTAKE → TRIAGE → PLAN → [APPROVE] → ROUTE → TRACK → [CORRECT]
```

1. **INTAKE** — Understands the demand, checks for work in progress (`.osforge/status.yaml`), loads `project-context.md`, asks clarifying questions (max 5)
2. **TRIAGE** — Classifies as QUICK/STANDARD/COMPLEX with justification. User can override.
3. **PLAN** — Generates multi-phase plan from templates (`plan-templates/{level}.md`). Presents for approval.
4. **APPROVE** — User chooses: **[A]** Approve / **[E]** Edit / **[S]** Simplify
5. **ROUTE** — Executes phase by phase, invoking the right skills. Checkpoint after each phase.
6. **TRACK** — Maintains `.osforge/status.yaml` as source of truth for project state.
7. **CORRECT** — Handles mid-flight changes: analyzes impact, proposes adjusted plan, requests approval.

### Skill mapping by triage

**QUICK:** spec-builder → execute → code-review

**STANDARD:** spec-builder → arch-builder (if needed) → epic-decomposer → story-executor loop → code-review → adversarial-review + edge-case-hunter

**COMPLEX:** prd-builder → arch-builder → epic-decomposer → readiness-gate → story-executor sprint loop → code-review → adversarial-review + edge-case-hunter

### Project tracking

The Orchestrator maintains two state files in the project root:

**`.osforge/status.yaml`** — phases, artefacts and pipeline state (structured, machine-readable).

**`.osforge/STATE.md`** — cross-session memory: architectural decisions, active blockers, and exact resumption point. Always read at session start; always updated at session end.

```yaml
project: "subscription-module"
triage: standard
status: active
phases:
  - name: "Spec"
    status: complete
    skill: "skills/planning/spec-builder"
    artifact: "docs/specs/subscription-module.md"
  - name: "Stories"
    status: in-progress
    skill: "skills/planning/epic-decomposer"
    artifact: null
corrections: []
```

When resuming a session, the Orchestrator detects existing work and offers to continue.

### Utility skills (any triage)

| Need | Skill |
|---|---|
| Compress large context | `context/context-distillator` |
| Generate project constitution | `context/project-context-generator` |
| Split large document | `context/doc-shard` |
| Refine any output | `quality/elicitation-engine` |
| Review document prose/structure | `context/editorial-review` |

---

## 8. Python Hooks

Hooks run as external processes — **zero token cost**. Configured via `hooks/hooks-claude-code.json`. O merge no `settings.json` é **reconciliador**: hooks OSForge-managed refletem sempre o repo; hooks do próprio usuário são preservados (union, nunca sobrescreve).

### Installation

```bash
# Via deploy.sh (automatic)
./deploy.sh

# Manual
cp hooks/*.py hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*
```

### What each hook does (8 hooks)

**`canvas-autostart.sh`** (SessionStart)
- Inicia o OSForge Canvas em `localhost:4242` se ainda não estiver rodando
- Permite que Claude escreva artefatos JSON e o viewer os renderize em tempo real via SSE

**`session-resume.sh`** (SessionStart)
- Detecta se o `cwd` é um projeto registrado no `osforge-db`
- Injeta automaticamente `osforge-db resume <slug>` + `board` no início da sessão (~50 tokens)

**`protect-tests.sh`** (PostToolUse — Write | Edit | MultiEdit)
- Alerta e loga quando um arquivo de teste foi alterado
- Lembrete: testes devem falhar por lógica de negócio, nunca ajustados para passar

**`observe-capture.py`** (PostToolUse — Edit | Write | MultiEdit | Bash)
- Grava observações de comportamento do Claude para alimentar o ciclo `evolve`
- Permite que padrões de sessão virem skills automaticamente

**`scan-secrets.sh`** (PreToolUse — Bash)
- Bloqueia commits que contenham segredos/secrets antes de chegar ao `git push`
- Varre por padrões: API keys, tokens, senhas em variáveis, credentials hardcoded

**`gateguard.py`** (PreToolUse — Bash)
- Fact-forcing: bloqueia **somente** o irreversível/compartilhado:
  `rm -rf`, `git push --force`, `git reset --hard`, `git clean -f`, SQL `DROP`/`TRUNCATE`/`DELETE`
- Matcher restrito a Bash — não gatea Edit/Write
- Kill-switch: `OSFORGE_GATEGUARD=off` desativa para automações CI
- Loga todas as negativas em `~/.osforge/gateguard/denials.log`

**`notify-done.sh`** (Stop)
- Envia notificação macOS via AppleScript ao término da sessão

**`session-save.py`** (Stop)
- Parseia o transcript da sessão e grava `set-resume` automático no `osforge-db`
- Garante que o contexto da sessão não se perde entre janelas

---

## 9. osforge-db — Local SQLite State

Persistent state management for OSForge projects via SQLite local database. No server, no network — pure Python built-in.

### How it works

After deploy, `osforge-db` is available at `~/.local/bin/osforge-db`. The global database lives at `~/.osforge/osforge.db` and accumulates state across all projects on your machine.

```bash
# Add to ~/.zshrc or ~/.bashrc if not already there:
export PATH="$HOME/.local/bin:$PATH"
```

### Daily workflow

**Starting a session** — load context in ~50 tokens:
```bash
osforge-db resume my-project
# → fase=spec-builder | resume=Próximo: ACs do módulo de checkout
```

**During work** — record progress:
```bash
# Mark phase complete with artifact path
osforge-db set-phase my-project "spec-builder" complete \
  skills/planning/spec-builder docs/specs/billing.md

# Record architectural decision
osforge-db add-decision my-project \
  "Usar cursor-based pagination para tabelas >10K registros" \
  --category=arch

# Register a blocker
osforge-db add-blocker my-project \
  "Modelo de precificação não definido" \
  --waiting="decisão de produto"
```

**Ending a session** — mandatory before closing:
```bash
osforge-db set-resume my-project \
  "Próximo: arch-builder — schema do módulo de billing, relação com orgs"
```

### Search across all projects

```bash
# Full-text search in all decisions (FTS5)
osforge-db search "autenticação OAuth"
osforge-db search "Prisma RLS multi-tenant" --project=linkme-tur

# List decisions by category
osforge-db list-decisions my-project --category=security --limit=10

# Full status
osforge-db status my-project

# All active projects
osforge-db list-projects
```

### Scopes

| Scope | Path | Quando usar |
|---|---|---|
| global (padrão) | `~/.osforge/osforge.db` | Histórico cross-project, decisões não-sensíveis |
| local | `.osforge/osforge.db` | Projetos com dados sensíveis (Essent, Rede Essent Jus) |

```bash
# Usar escopo local
osforge-db --scope=local add-decision meu-projeto "RLS: clientes só veem orgs próprias"
```

### Migrating from status.yaml

```bash
osforge-db import-yaml .osforge/status.yaml meu-projeto
```

### Decision categories

| Category | Use |
|---|---|
| `arch` | Architecture and stack decisions (default) |
| `product` | Product scope and priority decisions |
| `ux` | Interface and experience decisions |
| `data` | Schema, migration, data model decisions |
| `security` | Auth, LGPD, security decisions |

### Memória vetorial (3-tier)

O `osforge-db` suporta busca semântica sobre decisões e contexto de projeto via embeddings. Degradação graciosa: sem embedder ativo, cai automaticamente para FTS5 lexical.

**Subcomandos de embedding e busca:**

```bash
# Embeddar um registro específico
osforge-db embed decisions <id> "texto a embeddar"

# Popula embeddings para todo o histórico de decisões
osforge-db embed-backfill --source=decisions

# Busca semântica pura (top-N mais próximos)
osforge-db search-semantic "autenticação multi-tenant" --top=5

# Busca híbrida — RRF (Reciprocal Rank Fusion) combinando FTS5 + vetor
osforge-db search-hybrid "RLS Supabase por organização" --top=5

# Inicializar backend vetorial
osforge-db vec-init

# Ver status do backend (provider, modelo, coleção, contagem de vetores)
osforge-db vec-status
```

**Variáveis de ambiente:**

| Variável | Padrão | Opções |
|---|---|---|
| `OSFORGE_EMBED` | `ollama` | `ollama` \| `off` \| `mock` \| `voyage` \| `openai` |
| `OSFORGE_EMBED_MODEL` | `bge-m3` | qualquer modelo Ollama ou API |
| `OSFORGE_VECTOR` | `sqlite` | `sqlite` \| `qdrant` |
| `OSFORGE_QDRANT_URL` | `http://localhost:6333` | URL do Qdrant |
| `OSFORGE_COLLECTION` | `osforge_memory` | nome da coleção |

**Contrato `~/.osforge/config.json`:**

```json
{
  "vector_backend": "qdrant",
  "embed_provider": "ollama",
  "embed_model": "bge-m3",
  "qdrant_url": "http://localhost:6333",
  "collection": "osforge_memory"
}
```

**3 tiers — da maior qualidade ao mais simples:**

| Tier | Requisito | Indexação | Quando usar |
|---|---|---|---|
| **qdrant** | Docker + Ollama | HNSW (ANN rápido) | Produção, grandes históricos |
| **sqlite** | Apenas Ollama | Cosseno brute-force | Sem Docker, dev local |
| **off** | Nenhum | FTS5 lexical | Sem embedder disponível |

### Memória vetorial — setup (Qdrant + Ollama)

```bash
# 1. Instalar modelo de embedding multilíngue (acerta PT-BR)
ollama pull bge-m3

# 2. Deploy com Qdrant via Docker (sobe container, cria coleção, escreve config.json)
./deploy.sh --with-qdrant

# 3. Populando histórico existente
osforge-db embed-backfill --source=decisions

# Alternativa sem Docker (SQLite brute-force, com aviso de performance)
./deploy.sh --no-qdrant
```

Decisão registrada em **ADR-010** (`docs/DECISIONS.md`). Avaliação de modelos: `bge-m3` (multilíngue) escolhido por acertar 3/3 em PT-BR vs 1/3 do `nomic-embed-text`.

---

## 10. Operação Multi-projeto — Sessão-sede e Satélites

Quando você trabalha em vários projetos simultaneamente, misturar tudo em uma única sessão Claude Code polui o contexto com arquivos irrelevantes, mistura permissões de working directories diferentes e aumenta o custo sem ganho. O padrão **sessão-sede / sessões-satélite** resolve isso.

### Conceito

| Sessão | Working directory | Função |
|---|---|---|
| **Sede (hub)** | `~/Development/osforge` ou diretório de planejamento | Intake de demandas, brainstorm/specs, triage, visão de portfólio, preparação de briefs |
| **Satélite** | Diretório do projeto (`~/Development/meu-projeto`) | Execução das tasks — uma sessão por projeto |

A regra é simples: **uma sessão tem um working directory primário**. A sede nunca executa código de projetos externos; os satélites nunca planejam fora do escopo do próprio projeto.

### Papéis detalhados

**Sessão-sede**
- Mantém visão de portfólio via `osforge-db board`
- Recebe novas demandas, faz brainstorm, escreve specs
- Registra projetos e tasks no banco: `upsert-project`, `add-task`
- Prepara briefs de delegação em `agents/orchestrator/delegation-brief.md`
- Não toca em código de projetos — acessa apenas o próprio repo osforge

**Sessão-satélite**
- Abre no diretório do projeto-alvo
- Ao iniciar: carrega contexto compacto (~50 tokens) com `osforge-db resume <slug>`
- Executa as tasks registradas pela sede
- Ao pausar ou concluir: atualiza o banco para a sede enxergar o progresso

### Comandos de handoff

```bash
# ── SEDE: registrar trabalho para um satélite ──────────────────────────
osforge-db upsert-project linkme-tur "Portal B2B para agentes de turismo" standard active
osforge-db add-task linkme-tur "Implementar módulo de reservas" --phase="backend" --priority=p0
osforge-db add-task linkme-tur "UI da página de listagem de hotéis" --phase="frontend" --priority=p1

# ── SATÉLITE: iniciar sessão no projeto ───────────────────────────────
# (abrir terminal no diretório do projeto)
osforge-db resume linkme-tur
# → fase=backend | resume=Próximo: implementar endpoint POST /reservas

# ── SATÉLITE: atualizar progresso durante a sessão ────────────────────
osforge-db set-task linkme-tur 1 done
osforge-db set-task linkme-tur 2 in-progress

# ── SATÉLITE: encerrar sessão — OBRIGATÓRIO antes de fechar ───────────
osforge-db set-resume linkme-tur "Concluído: POST /reservas. Próximo: validação de disponibilidade"

# ── SEDE: conferir estado de todos os projetos ────────────────────────
osforge-db board
```

### Fluxo exemplo completo

```
SEDE:
  1. osforge-db upsert-project meu-saas "SaaS de gestão de assinaturas" standard active
  2. osforge-db add-task meu-saas "Schema Prisma — tabela subscriptions" --priority=p0
  3. osforge-db add-task meu-saas "Server Action: criar assinatura Stripe" --priority=p0
  4. osforge-db board   → confirma tasks visíveis

SATÉLITE (abre ~/Development/meu-saas):
  5. osforge-db resume meu-saas
     → fase=– | resume=–  (primeira vez)
  6. [executa task 1 — schema Prisma]
  7. osforge-db set-task meu-saas 1 done
  8. osforge-db set-resume meu-saas "Schema concluído. Próximo: task #2 — Server Action"
  [fecha sessão]

SEDE (retomada):
  9. osforge-db board
     → meu-saas:
       [done       ] #1 p1 Schema Prisma — tabela subscriptions
       [pending    ] #2 p0 Server Action: criar assinatura Stripe
```

### Por que não misturar numa sessão só?

- Contexto: arquivos de projetos diferentes competem pela janela de contexto
- Permissões: Claude Code pede permissão por working directory — misturar gera prompts duplicados
- Foco: uma sessão por projeto mantém o histórico de decisões limpo e o `resume` preciso
- Custo: contexto desnecessário consome tokens sem retorno

---

## 11. The Agency — 121 Specialists

The Agency é um catálogo de 121 especialistas de negócio (contábil, jurídico, marketing, financeiro, HR, operações) acessíveis via skill `agency`. Não confundir com os 27 agentes de engenharia (§4) — estes são especialistas de domínio para problemas de negócio, não de código.

```
"Read skills/meta/agency.md"
```

### Local LLM Advisor (llmfit)

Detecta o hardware real da máquina e recomenda quais modelos locais vão rodar bem, com quantização ideal e estimativas de velocidade.

### Installation

```bash
# macOS (recommended)
brew tap AlexsJones/llmfit && brew install llmfit

# Any platform (requires Rust)
cargo install llmfit

# Verify
llmfit --version
llmfit system    # View detected specs
```

### Essential commands

```bash
# View detected hardware (JSON)
llmfit --json system

# Top 5 general recommendations
llmfit recommend --json --limit 5

# Filter by use case
llmfit recommend --json --use-case coding    --limit 3
llmfit recommend --json --use-case reasoning --limit 3
llmfit recommend --json --use-case chat      --limit 3

# Only "perfect" or "good" fit models
llmfit recommend --json --min-fit good --limit 5

# Override VRAM when autodetect fails
llmfit --memory=24G recommend --json --limit 5

# Interactive TUI (default, no flags)
llmfit
```

### Understanding the output

| Field | Meaning |
|---|---|
| `fit_level` | `Perfect` (ideal) / `Good` (ok) / `Marginal` (tight) / `TooTight` (won't run) |
| `run_mode` | `GPU` (fast) / `CPU+GPU Offload` (mixed) / `CPU` (slow) |
| `best_quant` | Best quantization for the hardware (Q8_0 = max quality, Q2_K = most compressed) |
| `estimated_tps` | Estimated tokens per second |
| `is_moe` | Mixture-of-Experts — actual VRAM much lower than total parameter count |

**Rule:** Never recommend models with `fit_level: "TooTight"`.

### When to use local vs API

| Situation | Recommendation |
|---|---|
| Sensitive data — accounting, legal, HR records | ✅ **Always local** — data never leaves the environment |
| Clients without API budget | ✅ **Local** — llmfit finds the best viable model |
| High-volume repetitive tasks (boilerplate, i18n, stubs) | ✅ **Local** — eliminates accumulated API cost |
| Deep reasoning, architecture, complex analysis | ❌ **API (Opus)** — no complete local equivalent |
| Context >32K tokens | ❌ **API** — local models have limited windows |
| Latency-critical production use | ❌ **API** — more consistent |

### HuggingFace → Ollama mapping

| Model (llmfit) | Ollama tag | Best for |
|---|---|---|
| `Qwen/Qwen2.5-Coder-7B-Instruct` | `qwen2.5-coder:7b` | Light coding, boilerplate |
| `Qwen/Qwen2.5-Coder-14B-Instruct` | `qwen2.5-coder:14b` | Intermediate coding |
| `meta-llama/Llama-3.1-8B-Instruct` | `llama3.1:8b` | General chat |
| `meta-llama/Llama-3.3-70B-Instruct` | `llama3.3:70b` | Advanced general use |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` | `deepseek-r1:32b` | Reasoning |
| `google/gemma-2-9b-it` | `gemma2:9b` | Efficient chat |
| `microsoft/Phi-4-mini-instruct` | `phi4-mini` | Light tasks, fast |

### Install a model via Ollama

```bash
ollama pull qwen2.5-coder:7b
ollama pull phi4-mini
ollama list   # view installed models
```

### Activate in OSForge

```
"Read skills/llmfit-advisor/SKILL.md"
→ Detects hardware, recommends models, offers to configure Ollama
```

---

## 12. Smart Model Dispatch

Routes tasks to the optimal model tier — saving ~65% cost vs using Opus for everything.

```
"Read skills/smart-model-dispatch/SKILL.md"
```

### Tier summary

> IDs mudam com novos lançamentos — fonte canônica é a skill `smart-model-dispatch` (`skills/claude-ai/model-dispatch.md`).

| Tier | Model ID | When to use |
|---|---|---|
| Topo — Opus | `claude-opus-4-8` | Arquitetura, planejamento complexo, security review |
| Topo — Fable | `claude-fable-5` | Decomposição, raciocínio longo, análise de ADR |
| Medio — Sonnet | `claude-sonnet-4-6` | Implementação, debug, review, testes |
| Rápido — Haiku | `claude-haiku-4-5` | Boilerplate, i18n, stubs, docs, CRUD simples |
| Local | Ollama (via llmfit) | $0 — Haiku-eligible com dados sensíveis ou alto volume |

### Full feature dispatch pattern

```
[opus/fable] planner           → architecture + decomposition
[opus/fable] validator         → critiques the plan
[sonnet]     backend-engineer  → Prisma + Server Actions
[sonnet]     frontend-engineer → UI + components
[haiku]      →                   i18n keys, test stubs, seed data
[sonnet]     code-reviewer     → final review
[local]      →                   mechanical tasks with sensitive data
```

---

## 13. Recommended MCPs

### Claude Code (global — `~/.claude.json`)

```jsonc
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
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "your-pat" }
    }
  }
}
```

> ⚠️ Never put tokens in chat messages or versioned files. Use environment variables or the local `~/.claude.json` file.

### Cursor (project — `.cursor/mcp.json`)

See `mcp/cursor.json` in the repository.

---

## 14. High-Risk Agents

Four agents from The Agency can execute autonomous actions with real-world impact. Each has a **mandatory checkpoint block** embedded in its `.md` — they will never act without presenting a plan and waiting for explicit approval.

| Agent | Risk | File |
|---|---|---|
| Accounts Payable | Crypto/fiat/stablecoin payments | `skills/agency/specialized/accounts-payable-agent.md` |
| Carousel Growth Engine | Autonomous social media publishing | `skills/agency/marketing/marketing-carousel-growth-engine.md` |
| Report Distribution | Automated email/report distribution | `skills/agency/specialized/report-distribution-agent.md` |
| Agentic Identity & Trust | Inter-agent trust configuration | `skills/agency/specialized/agentic-identity-trust.md` |

### Usage protocol

1. The agent presents a full plan before any action
2. You respond explicitly: `"confirm"`, `"approve"` or `"yes, proceed"`
3. Without explicit confirmation → agent stops and asks again
4. Each action is timestamped for audit purposes

To use without the checkpoint in a controlled context, remove the `---⚠️ HIGH-RISK AGENT---` block from the beginning of the corresponding `.md` file.

---

*Questions or contributions: open an issue at [github.com/plocemourasouza/osforge](https://github.com/plocemourasouza/osforge)*
