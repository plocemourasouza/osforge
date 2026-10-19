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
15. [Evals — medir em vez de achar](#15-evals--medir-em-vez-de-achar)
16. [Session config reference](#16-session-config-reference)

---

## Getting Started — Ordem de Leitura

Novo no OSForge? Leia nesta ordem:

1. **Este USAGE.md §1-2** — instalação e deploy
2. **[`claude-code/SKILLS.md`](claude-code/SKILLS.md)** — índice de triggers das 177 skills
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
./deploy.sh --no-archify    # Skip the pinned Archify install (system-diagrams falls back to Mermaid)
./deploy.sh --doctor        # Report managed files that are missing/edited and hooks that drifted; writes nothing
./deploy.sh --uninstall     # Remove what OSForge installed and you did not edit; restore settings (--dry-run to preview)
./deploy.sh --restore=ID    # Put back the backups taken by run ID (see ~/.claude_backups/)
./deploy.sh --force         # Overwrite managed files you edited (backup first)
./deploy.sh --adopt         # Take over files of yours that collide with OSForge's (backup first)
./deploy.sh --force-hooks   # Overwrite a managed hook entry you edited in settings.json
```

### The deploy has a memory (ADR-015, stage 3)

Everything the deploy writes is recorded in `~/.osforge/install-state.json` — one SHA-256 per
file, each managed hook entry by id (`event|matcher|script`), the previous value of every
settings key it sets, and the MCP servers it added. Every later run consults that record, so:

- a file it wrote and you did not touch is updated; a file it wrote and **you edited** is kept
  (your version is backed up to `~/.claude_backups/<run>/`; `--force` overwrites);
- a file that exists and **is not OSForge's** is skipped with a warning (`--adopt` takes it
  over, with backup). A file that matches an *older* revision of the repo is recognised as a
  legacy install and simply updated;
- a skill, agent or command that **left the repo** is removed — only if it is still byte-identical
  to what was installed. Your own skills in `~/.claude/skills/` and the ones installed with
  `install-skill --global` are never deleted (no more `rsync --delete`);
- your hooks in `settings.json` — even under `~/.claude/hooks/` — are never touched. A managed
  hook entry you edited by hand **aborts the deploy** with the diff (`--force-hooks` overrides);
- a second run with nothing changed writes nothing and takes no backup (idempotent);
- `--doctor` exits 1 and lists what drifted; `--uninstall` leaves only your files, removes the
  managed hook entries, restores the settings keys it had set, removes the MCP servers it had
  added, and keeps your data (`~/.osforge/osforge.db`, `config.json`).

`tests/test-deploy-lifecycle.sh` runs the real `deploy.sh` against a seeded temporary HOME and
checks all of the above by execution (61 checks, ~1 min, offline). `OSFORGE_DEPLOY_LEGACY=1`
selects the old copy/rsync path for one release.

### What the deploy does

**Claude Code (`~/.claude/`)**
- Copies `CLAUDE.md` and `SKILLS.md`
- Syncs 25 agents (orchestrator + 24 specialists) to `~/.claude/agents/`
- Copies 9 `spec-*` commands to `~/.claude/commands/`
- Installs 11 hooks to `~/.claude/hooks/` (plus the shared `hooks/lib/`)
- Merges the managed hook entries into `~/.claude/settings.json` by id (yours are preserved) and the MCP servers into `~/.claude.json` (non-destructive)

**Cursor (`~/.cursor/`)**
- Copies `SKILLS.md`
- Syncs agents to `~/.cursor/agents/`
- Copies 14 rules (12 `.mdc` + 2 `.md`) to `~/.cursor/rules/`
- Copies hook scripts

**Archify (third-party, pinned)**
- Downloads `tt-a1i/archify` at the tag in `ARCHIFY_VERSION` (top of `deploy.sh`) into `~/.claude/skills/archify` and `~/.cursor/skills/archify` (slim: no `test/`, no rendered example HTML), runs `doctor`. Idempotent; needs Node ≥ 18 and network. Skip with `--no-archify`; upgrade by editing the tag.

**Dependency check**
The script warns if `llmfit` or Archify is not installed and provides the install command.

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
- `system-diagrams` — Verified architecture/workflow/sequence/dataflow/lifecycle diagrams via Archify (`validate → deliver` receipt); wired into `/spec-design`, ADRs, TDDs, runbooks
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

### Agent reference (25 agents: orchestrator + 24 specialists)

| Agent | When to use |
|---|---|
| `orchestrator` | **Start here** — intake, triage, multi-phase planning, routing, tracking, course correction |
| `planner` | New projects and major features — task breakdown, file structure, agent assignment, dependency graph (waves), stories |
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
| `product-owner` | Requirements, user stories, acceptance criteria, prioritization (MoSCoW/RICE), backlog, MVP scope, PRDs |
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

The 14 rules (12 `.mdc` + 2 `.md`: `artifact-chain`, `orchestrator-awareness`) are active in Cursor sessions. Eleven are always on; the three **stack rules** — `nextjs-patterns`, `typescript-strict`, `code-style` — carry `alwaysApply: false` and load only when a file matching their `globs` is in context, so a Markdown-only or Python session does not pay for them (R-11, B-024). Taking them to Claude Code as `~/.claude/rules/` stays conditional on confirming, with `scripts/measure-context.py` in a real session, that `paths:` is honoured there.

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

### What each hook does (11 hooks)

**`canvas-autostart.sh`** (SessionStart)
- Inicia o OSForge Canvas em `localhost:4242` se ainda não estiver rodando
- Permite que Claude escreva artefatos JSON e o viewer os renderize em tempo real via SSE

**`session-resume.sh`** (SessionStart)
- Resolve o projeto com `hooks/lib/project_id.py`: `OSFORGE_PROJECT` → raiz git registrada
  (`bind-project --root=.`; vale para subdiretórios e worktrees) → hash do remote → basename
- Injeta o `resume` e as tarefas abertas **deste** projeto, num envelope explícito de dados
  (não instruções), com teto (`OSFORGE_RESUME_MAX_CHARS`, 1200) e sem segredos (`hooks/lib/scrub.py`).
  O board cross-project não é mais injetado (B-019)

**`protect-tests.sh`** (PostToolUse — Write | Edit | MultiEdit)
- No Claude Code, injeta `additionalContext` quando um arquivo de teste é alterado, lembrando a
  Iron Law do TDD (teste só muda para descrever comportamento, nunca para passar); no Cursor só loga
- Log em `~/.osforge/logs/hooks.log` (nunca em `/tmp`)

**`observe-capture.py`** (PostToolUse — Edit | Write | MultiEdit | Bash)
- Grava observações de comportamento do Claude para alimentar o ciclo `evolve`
- Permite que padrões de sessão virem skills automaticamente

**`scan-secrets.sh` → `scan-secrets.py`** (PreToolUse — Bash; Cursor `beforeShellExecution`)
- Bloqueia `git commit`/`git push` quando o **diff staged** adiciona algo com cara de credencial
  (`sk-…`, `ghp_…`, `AKIA…`, token Slack, credencial em URL, bloco PEM, `password = …`), e
  `rm -rf` apontado para `/`, `~`, `$HOME` ou diretório pai
- Lê o payload dos dois harnesses (`tool_input.command` no Claude Code, `command` no Cursor) e
  responde no contrato de cada um. Fixture com chave falsa: `osforge:allow-secret` na linha.
  Kill-switch: `OSFORGE_SCAN_SECRETS=off`. Teste offline: `tests/test-scan-secrets.sh`

**`gateguard.py`** (PreToolUse — Bash; UserPromptSubmit)
- Fact-forcing: bloqueia **somente** o irreversível/compartilhado:
  `rm -rf`, `git push --force`, `git reset --hard`, `git clean -f`, SQL `DROP`/`TRUNCATE`/`DELETE`
  (SQL só conta quando o comando invoca um cliente de banco: `psql`, `mysql`, `prisma db execute`…)
- Matcher restrito a Bash — não gatea Edit/Write
- **Liberação por confirmação do usuário** (hook UserPromptSubmit, mesmo script): quando você
  responde com uma autorização explícita — "tem permissão", "pode executar/apagar", "autorizo",
  "vai em frente", "go ahead", "you have my permission" — ou com uma afirmativa curta como
  mensagem inteira ("sim", "pode", "ok", "vai", "yes"), o gate libera **até a sua próxima mensagem**
  (teto de 15 min, `OSFORGE_GATEGUARD_GRANT_TTL` em segundos). **A liberação só vale como
  resposta a uma negação**: sem nada negado nos últimos 10 min na sessão, "ok"/"sim"/"proceed"
  são conversa e não abrem o gate (B-001; `OSFORGE_GATEGUARD_LEGACY_GRANT=1` restaura o
  comportamento antigo por uma versão). `gateguard: sessão liberada` continua explícito e não
  precisa de negação. O agente recebe um
  `additionalContext` avisando que não precisa apresentar os fatos. Negações nunca liberam
  ("não pode apagar", "don't do it"); um afirmativo perdido numa mensagem longa também não.
  - `gateguard: sessão liberada` (ou `gateguard off`) → abre o gate até o fim da sessão
  - `gateguard: ativa` / "revogo a permissão" → fecha na hora
  - A liberação é por sessão (`session_id`): outra sessão continua gateada
- Kill-switch: `OSFORGE_GATEGUARD=off` desativa para automações CI
- Loga negativas e liberações em `~/.osforge/gateguard/denials.log`
  (`BASH-DESTRUCTIVE`, `GRANT-GRANT`/`GRANT-SESSION`/`GRANT-REVOKE`, `GRANT-ALLOW`)
- Testes: `tests/test-gateguard-sql.sh` (detector SQL) e `tests/test-gateguard-grant.sh` (liberação)

**`notify-done.sh`** (Stop)
- Envia notificação macOS via AppleScript quando o agente para normalmente (`stop_hook_active=false`;
  a versão anterior tinha a lógica invertida — B-007); silencioso fora do macOS; log em `~/.osforge/logs/hooks.log`

**`context-threshold.py`** (UserPromptSubmit)
- Lê o `message.usage` da última resposta no transcript (input + cache_read + cache_creation = o
  contexto real enviado ao modelo) e injeta o aviso do Context Budget **uma vez por faixa por
  sessão**: ≥120k "salve estado e termine o passo", ≥150k "pare de abrir trabalho novo, termine o passo, handoff, compacte". Lê só o fim
  do transcript (~1 ms). `OSFORGE_CONTEXT_BANDS=120000,150000`; kill-switch `OSFORGE_CONTEXT_THRESHOLD=off` (B-021)

**`canvas-feedback.py`** (Stop)
- Se o usuário enviou feedback no Canvas para um artefato **deste projeto** (id prefixado com o
  slug) que o agente ainda não leu, bloqueia o Stop **uma vez** com o conteúdo (decisões,
  checklist, form, comentário — sem segredos); o Stop seguinte passa. Respeita `stop_hook_active`,
  passa se o servidor está fora do ar; entregas registradas em `<data dir>/.delivered.json`.
  Kill-switch: `OSFORGE_CANVAS_FEEDBACK=off`. Padrão do `plan-canvas-pending.js` do ECC (MIT), reimplementado (B-020)

**`session-save.py`** (Stop)
- Lê o **fim** do transcript (últimos 4 MB) e grava `set-resume` com as últimas 8 mensagens,
  arquivos editados e ferramentas — segredos removidos antes de gravar (B-019)
- Mesma identidade de projeto do `session-resume` (B-018); só grava em projeto registrado
- Grava também os tokens da sessão por modelo (`osforge-db add-usage`, uma vez por `message.id`);
  `osforge-db usage <slug>`, `board` e `stats` mostram o total do projeto (B-022)

---

## 9. osforge-db — Local SQLite State

Persistent state management for OSForge projects via SQLite local database. No server, no network — pure Python built-in.

### How it works

After deploy, `osforge-db` is available at `~/.local/bin/osforge-db`. The global database lives at `~/.osforge/osforge.db` (`OSFORGE_DB=<path>` overrides it — used by the tests) and accumulates state across all projects on your machine.

**Bind a project to its folder once**, so every hook recognises it from any subdirectory,
worktree or clone — and two folders with the same name never share state:
```bash
cd ~/Development/my-project
osforge-db upsert-project my-project "Descrição" standard active --root=. --remote=auto
# ou, para um projeto já registrado:
osforge-db bind-project my-project --root=. --remote=auto
```
Projects registered before this still resolve by folder name; binding is what makes
`My_Proj` ≠ `my_proj-clone` and `src/deep/` = the project root.

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
# Full-text search in all decisions (FTS5). Agent rule: 4-8 keywords, English plus the
# pt-BR terms the user used, code identifiers and file names; retry once with synonyms.
osforge-db search "oauth autenticação callback redirect_uri auth/callback.ts"
osforge-db search "Prisma RLS multi-tenant" --project=linkme-tur

# Temporal recall: whole days, both ends inclusive (UTC)
osforge-db search "cache do catálogo" --since=2026-10-01 --until=2026-10-31

# List decisions by category / period
osforge-db list-decisions my-project --category=security --limit=10
osforge-db list-decisions my-project --since=2026-09-01 --until=2026-09-30

# Full status
osforge-db status my-project

# All active projects
osforge-db list-projects
```

**How the lexical search reads a query.** Words only (unicode-aware, lowercased); pt-BR and
English stopwords, words every decision shares ("decidimos", "decided") and words under 3
characters are dropped; each remaining word is quoted (so `-`, `:`, `*`, `NEAR`, `AND/OR/NOT`
are never operators) and the words are **OR-ed**, ranked by bm25. A query made only of
dropped words falls back to its raw words (`search "UI"` still works). Matching is
accent-insensitive (`funcoes` finds "funções"): the index uses `unicode61 remove_diacritics 2`,
and an index created before that is rebuilt once, automatically, on the next `osforge-db` call.

**`--json` rows** of `search`, `search-hybrid` and `list-decisions` share one shape:
`{id, project, category, created_at, content}` (`search` also keeps `slug`, an alias of
`project`; `search-hybrid` adds `degraded`, below).

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

### Workbench vs brain (ADR-017)

Memory is split in two, by what it is for:

| | **Workbench** — SQLite `~/.osforge/osforge.db` | **Brain** — Qdrant collection `osforge_brain` |
|---|---|---|
| Holds | projects, phases, tasks, blockers, resume, usage, calls, board, observations/instincts, and `decisions` as the per-project execution log | long-term knowledge: `decision`, `knowledge`, `technique`, `methodology` |
| Read by | `resume`, `board`, `status`, `list-decisions`, `search` | `recall` |
| Runtime | `osforge-db` itself, stdlib only | `~/.osforge/venv` (fastembed + qdrant-client + onnxruntime, pinned) |
| Source of truth | the SQLite file | the journal `~/.osforge/brain.jsonl` (append-only); the collection is a derived index |

```bash
# Record knowledge (journal first — secrets scrubbed by hooks/lib/scrub.py — then indexed)
osforge-db remember "Partial indexes on deleted_at make soft-delete filters cheap" --kind=technique --global --tags=postgres
osforge-db remember "Checkout keeps Stripe as the only gateway" --kind=decision --project=my-project
# add-decision does this for you: SQLite row + brain record (kind=decision, source add-decision:<id>)

# Query: 4-8 keywords, English plus the user's pt-BR terms; --since/--until for time questions
osforge-db recall "rate limit API key chave limite requisições" --project=my-project
osforge-db recall "cache catálogo catalog Redis" --since=2026-10-01 --until=2026-10-31 --json
osforge-db recall "grill plan question" --kind=methodology --mode=keyword   # BM25 only

osforge-db forget 3f2a91c0              # id or unique prefix: tombstone in the journal + delete the point
osforge-db brain status                 # store, embedder, journal live/forgotten, indexed points
osforge-db brain rebuild                # recreate the collection from the journal (batch_size=1)
osforge-db brain migrate                # SQLite decisions → brain, idempotent (source key); deploy runs it
osforge-db brain health [--timeout=0.3] # one `brain:` line when degraded, else silent (session-resume uses it)
```

**How `recall` ranks.** Dense first (embeddinggemma-300m, cosine): rows above the floor
(`brain_min_score`, default 0.30 for gemma) are the answer. Nothing above the floor → the BM25
sparse vector (fastembed `Qdrant/bm25`, Portuguese stemmer) answers instead. `--mode=keyword`
is BM25 only; `--mode=hybrid` is RRF of both, opt-in only — the design bench measured plain RRF
lowering gemma's hit@1 (14→12); this implementation's hybrid (dense floor inside its prefetch)
tied dense at 14/14 on the same data, so it gains nothing and dense stays the default. Filters (`--kind`, `--project`, `--global`,
`--since`, `--until`) go inside the query filter and inside each prefetch, never after ranking.
`--project=x` returns x only; `--global` returns only project-less memories.
JSON rows: `id, kind, project, tags, created_at, score, content` (+ `source`, `mode`, `degraded`).

**Degradation is never silent.** No venv, model missing, store down, or the local store locked
by another process → `recall` scans the journal lexically (same term builder as `search`:
stopwords dropped, OR, accent-insensitive), prints `note: brain degraded (<reason>) — lexical
fallback`, and sets `degraded` in every JSON row. `remember`/`forget` always journal first; if the
index step fails they say so in one line and `brain rebuild` catches up. `add-decision` never
fails because of the brain: one line, and the SQLite row is already committed.

**Store selection** (`brain_store` in `~/.osforge/config.json`, or `OSFORGE_BRAIN_STORE`):
`server` = Qdrant at `qdrant_url` (default `http://localhost:6333`); `local` = qdrant-client local
mode at `~/.osforge/brain/qdrant` (`OSFORGE_BRAIN_PATH`; single process — a concurrent call falls
back lexically; payload indexes are no-ops there). Unset → `server` when `./deploy.sh
--with-qdrant` provisioned Qdrant or the URL answers within 300 ms, else `local`; the deploy
writes the choice to config.json once so it never flips between runs.

**Install.** `./deploy.sh` creates `~/.osforge/venv` (`python3 -m venv` + pinned
`fastembed==0.9.0 qdrant-client==1.19.1 onnxruntime==1.31.0`), downloads the model once into
`~/.osforge/models`, and runs `brain migrate`. Offline or pip failure → one skip line, the
deploy goes on; `--no-brain` skips it; `--dry-run` only reports it. `osforge-db` re-runs brain
work in that venv's python as a subprocess, so `osforge-db` stays stdlib-only and importable
without any of it.

**Model and license.** Default `brain_model: "gemma"` — `google/embeddinggemma-300m`, 768d,
in-process ONNX on CPU, no Ollama. It is distributed under the **Gemma Terms of Use**, not an
OSI licence. License-clean alternative: `"brain_model": "e5-large"` (`intfloat/multilingual-e5-large`,
MIT, 1024d; set it, re-run `./deploy.sh` to fetch it, then `osforge-db brain rebuild`). Measured
on 124 real decisions / 14 pt-BR questions: dense hit@1 14/14, hit@5 14/14; ~1.3 s per
fresh-process `recall` (≈1.1 s of it import + model init); ~1.0 GB peak RSS; migrate of 124
decisions ~7 s with `batch_size=1` (the default batch of 256 pads to 6.8 GB RSS). Disk: venv
~240 MB + model ~1.2 GB (fp32 ONNX).

| Variable | Default | |
|---|---|---|
| `OSFORGE_BRAIN` | `on` | `off` = add-decision stops remembering, health stays silent (config `brain`) |
| `OSFORGE_BRAIN_STORE` | auto | `server` \| `local` (config `brain_store`) |
| `OSFORGE_BRAIN_PATH` | `~/.osforge/brain/qdrant` | local store path (config `brain_path`) |
| `OSFORGE_QDRANT_URL` | `http://localhost:6333` | server URL (config `qdrant_url`) |
| `OSFORGE_BRAIN_EMBED` | `gemma` | `gemma` \| `e5-large` \| `fake` (deterministic hash, tests/CI) (config `brain_model`) |
| `OSFORGE_BRAIN_PYTHON` | `~/.osforge/venv/bin/python` | brain interpreter |
| `OSFORGE_BRAIN_MODELS` | `~/.osforge/models` | fastembed cache |
| `OSFORGE_BRAIN_MIN_SCORE` | per model (gemma 0.30) | dense floor (config `brain_min_score`) |

`--scope=local` decisions are not copied to the brain (their ids would collide with the global
workbench's in the one global journal). Eval: `scripts/evals/memory/run.py --mode=brain`
(README there); tests: `tests/test-brain.sh`.

### Memória vetorial (3-tier) — legacy

**Legacy.** The `vec_memory` table, the `osforge_memory` collection, `embed*`,
`search-semantic`, `search-hybrid`, `vec-*` and `memory-health` below keep working unchanged for
compatibility; nothing deletes them. New memory goes to the brain (above).

O `osforge-db` suporta busca semântica sobre decisões e contexto de projeto via embeddings. Degradação graciosa: sem embedder ativo, cai automaticamente para FTS5 lexical.

**Query expansion (agent rule).** The lexical leg (OR-FTS5, bm25, stopwords, accent-insensitive)
matches words, so the words you search with decide what you find: 4–8 keywords, English plus the
pt-BR terms the user used, code identifiers and file names; `--since/--until` for time questions;
if the first search misses, one retry with synonyms. Measured on real decisions (14 private
questions, FTS only): natural questions hit@5 11/14, the same rewritten as keywords 14/14 (the
rewrites were made knowing the target: an optimistic bound).

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
osforge-db search-hybrid "cache" --project=my-project --since=2026-10-01   # both legs filtered before RRF

# Inicializar backend vetorial
osforge-db vec-init

# Ver status do backend (provider, modelo, coleção, contagem de vetores, cobertura)
osforge-db vec-status

# One-line hint when the memory is degraded; silent when healthy (the session-resume hook uses it)
osforge-db memory-health [--timeout=0.3]
```

**Coverage.** Only decisions with a vector for the active model take part in the vector leg.
`vec-status` prints `coverage: <embedded>/<total> decisions embedded` (JSON: `coverage`,
`embedder_reachable`). `add-decision` embeds the new decision when the embedder answers; when
it does not, the decision is still saved and a warning names `embed-backfill`.
`embed-backfill` embeds only what is missing (idempotent). It is manual: `./deploy.sh` no
longer runs it — the deploy indexes the brain (ADR-017), not this legacy Ollama path.

**Degradation is visible.** If the embedder is unreachable (or nothing is embedded yet),
`search-hybrid` still answers from FTS5 and says so: a first line
`note: degraded to FTS-only (<why>) …` in normal output, and a `degraded` field in every `--json`
row — `null` when both legs ran (and with the provider `off`, which is a choice, not a
degradation), else `embedder-unreachable` or `no-embeddings`. At session start the
`session-resume` hook adds one `memory: …` line to the injected resume when the embedder is
unreachable or under 80% of the decisions are embedded (probe capped at
`OSFORGE_RESUME_PROBE_TIMEOUT`, default 0.3 s; fail-open). Provider `off` produces no hint.

**Recall eval.** `scripts/evals/memory/` (synthetic fixture, hit@1/hit@5; README there).
`tests/test-memory-recall.sh` runs it offline (FTS only) with two floors: natural questions
hit@5 ≥ 80%, agent-style keyword rewrites (`--set=expanded`) hit@5 ≥ 95%.

**Variáveis de ambiente:**

| Variável | Padrão | Opções |
|---|---|---|
| `OSFORGE_EMBED` | `ollama` | `ollama` \| `off` \| `mock` \| `voyage` \| `openai` |
| `OSFORGE_EMBED_MODEL` | `bge-m3` | qualquer modelo Ollama ou API |
| `OSFORGE_VECTOR` | `sqlite` | `sqlite` \| `qdrant` |
| `OSFORGE_QDRANT_URL` | `http://localhost:6333` | URL do Qdrant |
| `OSFORGE_OLLAMA_URL` | `http://localhost:11434` | Ollama endpoint (config key `ollama_url`) |
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

# 3. Populando histórico existente (o deploy também roda isto quando o embedder responde)
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

The Agency é um catálogo de 121 especialistas de negócio (contábil, jurídico, marketing, financeiro, HR, operações) acessíveis via skill `agency`. Não confundir com os 25 agentes de engenharia (§4) — estes são especialistas de domínio para problemas de negócio, não de código.

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
| Topo — Opus | `claude-opus-5-5` | Arquitetura, planejamento complexo, security review |
| Topo — Fable | `claude-fable-5-1` | Decomposição, raciocínio longo, análise de ADR |
| Medio — Sonnet | `claude-sonnet-5-5` | Implementação, debug, review, testes |
| Rápido — Haiku | `claude-haiku-5-5` | Boilerplate, i18n, stubs, docs, CRUD simples |
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

## 15. Evals — medir em vez de achar

Três suítes. Todas exigem `--model` e rodam cada caso `--runs` vezes (padrão 3); todas
aceitam `--dry`, que lista os casos, valida os arquivos e **não chama modelo nenhum** —
é o `--dry` que roda no CI, a rodada paga é sempre decisão sua.

| Suíte | Pergunta que responde | Comando |
|---|---|---|
| `scripts/run-trigger-eval.sh` | a skill dispara quando deve **e só quando deve**? (5 positivas + 5 negativas por skill, 15 skills) | `--model X --split eval` |
| `scripts/test-orchestrator-routing.sh` | o orquestrador alcança agente, skill e tier? | `--model X --id r01` |
| `scripts/test-skill-triggering.sh` | as skills core disparam sem o nome no prompt? | `--model X --skill tdd-workflow` |

```bash
./scripts/run-trigger-eval.sh --dry                  # 170 casos (73 no split eval); diz quanto custaria
./scripts/run-trigger-eval.sh --model claude-sonnet-4-6 --split eval --runs 3     --report docs/evals/$(date +%F)-claude-sonnet-4-6-trigger.md
```

**PASS é `k = N`.** `0 < k < N` é **FLAKY** e reprova: um caso que acerta 2 de 3 não está
verde, está instável — e é essa lista que o experimento de estabilidade consome.
`--home DIR` roda contra um deploy limpo em vez do seu `~/.claude` vivo; `--report`
grava o resultado em `docs/evals/` com SHA, modelo, comando, tokens e tempo
(`docs/evals/README.md`). Sem `--report`, o resultado morre no terminal.

**Custo:** cada caso são `--runs` chamadas de API. `--dry` imprime o total antes.
A lógica de veredito roda offline em `./tests/test-assertions.sh` (67 casos, custo zero):
é lá que se pega regressão de asserção sem depender de o modelo se comportar.

### Qualidade e controle (Pacote 01, ADR-016)

**Casos v2.** Cada caso de trigger tem `category` (`positivo` · `vizinho` · `irrelevante` ·
`negacao`) e `critical`; o relatório agrega por categoria, então um FLAKY diz *onde* a skill
falha. `--dry` agora reprova caso órfão (skill inexistente) ou malformado — antes isso só
aparecia na rodada paga. Validação offline: `./tests/test-eval-cases.sh`.

**O harness respeita a cota.** Uma rejeição de cota no meio da rodada não vira mais uma
cascata de FLAKY/FAIL: o harness para, marca o resto como `NOT RUN`, sai com **exit 75** e
grava `quota_at_start`/`quota_at_end` no relatório. Também para *antes* do próximo bloco
se a janela já passou de `OSFORGE_EVAL_QUOTA_STOP` (padrão 85%). Suíte: `./tests/test-harness-quota.sh`.

**Aviso de janela ao modelo.** O `context-threshold` também avisa o modelo quando a janela
de 5 h passa de 80% e de 95% — uma vez por faixa por janela (`OSFORGE_QUOTA_BANDS`;
desliga com `OSFORGE_QUOTA_THRESHOLD=off`). A fonte
é `~/.osforge/quota.json`, alimentado por **uma linha opcional** no *seu* script de
statusline (o OSForge não o gerencia):

```bash
printf '%s' "$input" | python3 "$HOME/.claude/hooks/quota-record.py" >/dev/null 2>&1 &
```

Sem essa linha (ou com auth por API key, onde `rate_limits` vem nulo) o aviso fica em
silêncio — e também na extensão do VS Code, que não executa o statusline (visto em
2026-09-29); lá sobra só a fonte do transcript, que registra a rejeição quando ela acontece. Rejeições registradas no transcript também alimentam o arquivo. Detalhes:
`docs/HOOKS.md`. Suíte: `./tests/test-quota.sh`.

**Auditoria por chamada.** Tabela `calls` no `osforge-db`, uma linha por chamada de modelo
(sessão principal e subagentes). O custo equivalente em API é **derivado na consulta** a
partir de `claude-code/pricing.json` (datado) — nunca armazenado, então corrigir o preço
corrige o histórico.

```bash
osforge-db backfill-calls [slug]          # importa dos transcripts existentes
osforge-db calls --project=osforge --since=7d --by=model
osforge-db prune-calls --older-than=90d   # retenção
```

Suíte: `./tests/test-calls.sh`.

**Juiz isolado** (`scripts/lib/judge.py`). Mede *qualidade* (review achou o problema certo?
plano proporcional?), não trigger. Roda na assinatura — **nunca `--bare`**, que força
cobrança por API key — sem ferramentas, sem MCP, sem o seu `CLAUDE.md`, num diretório vazio;
o isolamento é verificado a cada chamada pelo evento `system/init`. Saída: uma linha JSON
validada contra o schema; exit 75 em rejeição de cota. O contrato roda offline em
`./tests/test-judge.sh`; o uso real espera o experimento **E-J0** (1–3 chamadas curtas,
autorizadas à parte).

**Os helpers que rodam na sua máquina** (`install-skill`, `install-mcp`, em `~/.local/bin`)
têm a sua própria suíte, `./tests/test-installers.sh` (22 verificações), que inclui rodá-los
num shell **sem os builtins do bash 4** — o `/bin/bash` do macOS é 3.2, e foi exatamente
assim que um `mapfile` deixou o `install-skill` quebrado sem nenhum gate perceber (`bash -n`
só faz o parse). `python3 scripts/check-portability.py`, no preflight do deploy e no CI,
impede a classe inteira.

---

## 16. Session config reference

Reference material moved out of `claude-code/CLAUDE.md` (audit N3): it explains how the config is
built, but it does not need to be in context on every turn to change behaviour. `claude-code/CLAUDE.md`
keeps a one-line pointer here.

### Memory hierarchy (load order; last wins)
1. **Managed** `/etc/claude-code/CLAUDE.md` — corporate global.
2. **User** `~/.claude/CLAUDE.md` — personal global (deployed from `claude-code/CLAUDE.md`).
3. **Project** `<repo>/CLAUDE.md` or `<repo>/.claude/CLAUDE.md` — shared, versioned.
4. **Local** `<repo>/CLAUDE.local.md` — private per-project, `.gitignore`-able.

Supports `@include <file>` (composition) and `paths:` frontmatter (conditional injection by glob of touched files).
Conflict = the more specific level wins. Details in the `memory-hierarchy.mdc` rule.

### Prompt cache strategy

To maximize cache hits on the Anthropic API, content splits into two blocks:

- **🔒 Cacheable prefix (stable):** identity + safety (`~/.claude/CLAUDE.md`, top), `settings.json` (permissions/hooks),
  the style spine inside `@SKILLS.md` (TypeScript strict, code style — the `.mdc` rules themselves reach Cursor only), the skills index (`@SKILLS.md`, 177 skills).
  **Keep it stable** — changing it invalidates every session's cache.
- **🌊 Dynamic suffix (changes per session):** on-demand loaded skills, memory (`CLAUDE.local.md`, `.osforge/`),
  environment context (OS/dir/git), language preferences, active MCP instructions, context-window guidelines.

### MCP servers (context-scoped)
MCP tool schemas are the biggest context cost — scope them tightly.
- **Global (loads every session):** only **Context7** (library docs) — transversal + cheap. `mcp/claude-code.json`.
- **Per-project:** `github · supabase · prisma · nextjs · shadcn · browser` — connect only where used, via
  `scripts/install-mcp.sh <stack>` (writes the project's `.mcp.json`). Templates in `mcp/stacks/`.
- **Anti-bloat settings** (deployed from `claude-code/settings-base.json` → `~/.claude/settings.json`):
  `disableClaudeAiConnectors: true` (keeps claude.ai account connectors — Gmail, Drive, Figma, Higgsfield… — **out** of
  Claude Code) and `env.ENABLE_TOOL_SEARCH=true` (defers large tool schemas, loading them on demand — `true`, not `auto`, because of the local proxy; rationale and measurement in `claude-code/settings-base.json`).
- **Cleanup:** deploy merges MCPs additively and never prunes; remove accumulated/dead globals with
  `scripts/prune-global-mcps.sh` (`--dead` drops `MCP_DOCKER` + `Prisma-Remote`).

---

*Questions or contributions: open an issue at [github.com/plocemourasouza/osforge](https://github.com/plocemourasouza/osforge)*
