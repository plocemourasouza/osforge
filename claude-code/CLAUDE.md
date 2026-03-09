# Claude Code Configuration

## Agents
Specialized agents available in ~/.claude/agents/:

**Core Engineering**
- planner — Decomposes features into atomic tasks with TDD order + complexity detection
- debugger — 10-step root cause analysis with evidence hierarchy; zero context-switching from user
- code-reviewer — 7-dimension quality review + refactoring prioritization
- code-refactorer — Transforms messy/rushed code into clean, maintainable implementations
- validator — Adversarial spec conformance checker. Read-only, never modifies code.

**Architecture & Strategy**
- system-architect — Scalable system design, clean architecture, legacy refactoring
- backend-engineer — API design, data integrity, reliability patterns, Supabase/Prisma
- frontend-engineer — shadcn ecosystem, MCP-first component discovery, visual verification
- product-strategy-advisor — Build/kill decisions, feature prioritization, product-market fit

**Security & Process**
- security-auditor — Trail of Bits methodology, fail-secure defaults, RLS verification
- git-commit-helper — Conventional Commits: analyzes staged changes, generates semantic messages

## Skills & Knowledge
@SKILLS.md

The spec workflow is powered by the **tlc-spec-driven** SKILL (included in @SKILLS.md).
Execute each phase via the `spec:*` commands listed below.

## Commands (spec:* system)
Available in ~/.claude/commands/. Execute with `/spec:discover`, `/spec:specify`, etc.

| Command | Phase | Output |
|---------|-------|--------|
| `/spec:constitution` | Pré-projeto | `.specs/memory/constitution.md` |
| `/spec:discover` | Phase 0 — Discover | `.specs/features/[f]/discovery.md` |
| `/spec:specify` | Phase 1 — Specify | `.specs/features/[f]/spec.md` |
| `/spec:design` | Phase 2 — Design | `.specs/features/[f]/design.md` |
| `/spec:tasks` | Phase 3 — Tasks | `.specs/features/[f]/tasks.md` |
| `/spec:implement` | Phase 4 — Implement+Validate | atualiza `tasks.md` + cria `validation.md` |
| `/spec:measure` | Phase 5 — Measure | `.specs/features/[f]/measure.md` |
| `/spec:clarify` | Auxiliar | atualiza artefatos in-place |
| `/spec:checklist` | Auxiliar | `.specs/features/[f]/checklist.md` |

## MCP Servers
- **Shadcn** — Component discovery: search components, get installation commands, browse docs
- **Context7** — Library documentation and framework patterns in context
- **Github** — Repository operations, PRs, issues, file management
- **Supabase** — Database operations, migrations, RLS policy management
- **Browsermcp** — Browser automation for visual verification and testing

## Development Workflow (Agent Orchestration)

### Feature Nova (full cycle)
1. `/spec:discover` → `.specs/features/[f]/discovery.md` (problema + hipótese + métricas)
2. `/spec:specify` → `spec.md` (requisitos + acceptance criteria)
3. `/spec:design` → `.specs/features/[f]/design.md` (arquitetura + decisões técnicas)
4. [validator] → critique spec (QA gate pré-implementação — lê spec.md, aponta gaps)
5. `/spec:tasks` → `.specs/features/[f]/tasks.md` com critérios de verificação por task
6. [dev/you] → implement (TDD: red-green-refactor por story, usando `/spec:implement` → gera `validation.md`)
7. [code-reviewer] → review (7 dimensões de qualidade)
8. [validator] → validate against spec.md
9. `/spec:measure` → `.specs/features/[f]/measure.md` (resultados pós-deploy vs hipótese do discover)

### Bug Fix
1. [debugger] → 10-step root cause analysis
2. [dev/you] → fix (TDD: test que reproduz → fix → verify)
3. [code-reviewer] → review fix

### Security Review
1. [security-auditor] → full audit
2. [dev/you] → fix findings
3. [security-auditor] → re-audit findings

### Regra: Não pule etapas. Se a feature é trivial, o ciclo é rápido.
Se é complexa, pular etapas custa mais que seguir o ciclo.

## Insights Capture (todos os agentes)
Após completar qualquer feature ou fix significativo, atualize:
- `tasks/lessons.md` — O que aprendemos? Gotchas para futuro?
- `.specs/project/DECISIONS.md` — Se houve decisão arquitetural

Categorias para lessons.md:
- 🐛 **Gotcha:** pattern que causa bug não-óbvio
- 📐 **Pattern:** padrão que funcionou bem, replicar
- ⚡ **Performance:** otimização descoberta
- 🔒 **Security:** vulnerabilidade ou pattern seguro
- 🧠 **Context:** algo específico deste projeto que afeta futuras decisões

## Core Rules
- Read before Write/Edit — always confirm current state first
- Absolute paths only — never relative paths in scripts or automations
- Never auto-commit — always wait for explicit approval
- Never skip tests — run full suite after changes, not just affected tests
- Validate before execution, verify after completion with evidence
- Structured logs: { action, tenantId, userId, duration, error } — never log PII
- When context feels heavy: compress responses, show diffs not full files, omit recaps
