# Claude Code Configuration

## Agents
Specialized agents available in ~/.claude/agents/:

**Core Engineering**
- orchestrator — Meta-agente: intake, triage (QUICK/STANDARD/COMPLEX), planejamento, routing, tracking cross-session via STATE.md
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
Execute each phase via the `spec-*` commands listed below.

## Prompt Cache Strategy

OSForge organiza memória em 2 zonas explícitas para maximizar cache hit no Anthropic API:

### 🔒 Cacheable Prefix (stable across sessions)
Esta seção raramente muda. Quando ela é estável, Anthropic API faz cache do prefixo
e cobra ~10% do preço normal por tokens repetidos. Pra OSForge, isso inclui:

- Identity + safety instructions (este arquivo, sections 1-3)
- Permission + hook configuration  (`~/.claude/settings.json`)
- Code style + error handling rules (`rules/typescript-strict.mdc`, `rules/code-style.mdc`)
- Tool preferences (este arquivo, MCP Servers section)
- Tone + style + output rules (anti-ai-slop, intelligent-routing)
- Skills index (@SKILLS.md — 122 triggers)

**Mantenha estas seções ESTÁVEIS.** Mudanças invalidam o cache de TODOS os usuários.

### 🔄 Cache Boundary

```
═══════════════════════════════════════════════════════
   CACHEABLE PREFIX ENDS HERE
═══════════════════════════════════════════════════════
   DYNAMIC SUFFIX BELOW (changes per session)
```

### 🌊 Dynamic Suffix (changes per session)
Esta seção muda toda sessão. Não tente cachear — desperdiça tokens:

- Available agents and skills (loaded on-demand via @include)
- Memory file contents (`CLAUDE.local.md`, `.osforge/status.yaml`)
- Environment context (OS, directory, git state)
- Language and output preferences (per-session)
- Active MCP server instructions (per-session)
- Context window management directives

### Hierarquia de carregamento

Loading order (último carregado = maior prioridade):
1. **Managed** (`/etc/claude-code/CLAUDE.md`) — corporate global
2. **User** (`~/.claude/CLAUDE.md`) — pessoal global (esse arquivo)
3. **Project** (`<repo>/CLAUDE.md`, `<repo>/.claude/CLAUDE.md`) — compartilhado
4. **Local** (`CLAUDE.local.md`) — privado per-project, `.gitignore`-able

Ver `rules/memory-hierarchy.mdc` para detalhes completos sobre `@include`,
frontmatter `paths` (conditional injection), e resolução de conflitos.

## Commands (spec-* system)
Available in ~/.claude/commands/. Execute with `/spec-discover`, `/spec-specify`, etc.

| Command | Phase | Output |
|---------|-------|--------|
| `/spec-constitution` | Pré-projeto | `.specs/memory/constitution.md` |
| `/spec-discover` | Phase 0 — Discover | `.specs/features/[f]/discovery.md` |
| `/spec-specify` | Phase 1 — Specify | `.specs/features/[f]/spec.md` |
| `/spec-design` | Phase 2 — Design | `.specs/features/[f]/design.md` |
| `/spec-tasks` | Phase 3 — Tasks | `.specs/features/[f]/tasks.md` |
| `/spec-implement` | Phase 4 — Implement+Validate | atualiza `tasks.md` + cria `validation.md` |
| `/spec-measure` | Phase 5 — Measure | `.specs/features/[f]/measure.md` |
| `/spec-clarify` | Auxiliar | atualiza artefatos in-place |
| `/spec-checklist` | Auxiliar | `.specs/features/[f]/checklist.md` |

## MCP Servers
- **Shadcn** — Component discovery: search components, get installation commands, browse docs
- **Context7** — Library documentation and framework patterns in context
- **Github** — Repository operations, PRs, issues, file management
- **Supabase** — Database operations, migrations, RLS policy management
- **Browsermcp** — Browser automation for visual verification and testing

## Development Workflow (Agent Orchestration)

### Fluxo Principal: Orchestrator (recomendado)

O orchestrator é o meta-agente que faz intake, triage e coordena todos os outros.
Acionar com: `"Read agents/orchestrator/AGENT.md"` ou descrever o que quer construir.

```
INTAKE → TRIAGE → PLAN → [APPROVE] → ROUTE → TRACK → [CORRECT]
```

**Ciclo completo para feature nova:**
```
1. brainstorming          → refinamento socrático ANTES de qualquer spec
                             salva design doc em .osforge/designs/
                             (pular para features triviais ou bem definidas)

2. requirements-clarify   → clarificação por dimensões de cobertura
                             (funcional, dados, UX, integração, segurança)
                             produz clarifications record antes do plano técnico

3. phase-discussion       → captura decisões de implementação por fase
                             (UI, API, dados) — produz .osforge/phases/N-CONTEXT.md

4. spec-builder           → tech spec com ACs testáveis
                             modo Delta/Brownfield para features existentes
                             CHECKPOINT: [A]prove / [E]dit / [R]efine

5. arch-builder           → ADRs e decisões de arquitetura (se schema/API changes)

6. epic-decomposer        → épicos e stories com tasks em XML canônico

7. story-executor         → implementa cada story
                             two-stage review por task: spec compliance → code quality

8. quality/code-review    → review com adversarial-review + edge-case-hunter

9. quality/ui-audit       → auditoria de 6 pilares para phases com UI

10. finishing-a-branch    → verificação pré-merge + menu M/P/K/D
```

**Ciclo para bug fix:**
```
1. systematic-debugging → 4 fases: reproduce → isolate → understand → fix
2. story-executor       → implementa fix com two-stage review
3. quality/code-review  → review do fix
```

**Ciclo para security review:**
```
1. security-auditor     → Trail of Bits methodology, threat modeling
2. story-executor       → fix findings
3. security-auditor     → re-audit
```

### Fluxo Alternativo: spec-* Commands (legacy, compatível)

Comandos slash disponíveis em `~/.claude/commands/`. Usam o sistema `tlc-spec-driven`.

| Command | Phase | Output |
|---------|-------|--------|
| `/spec-constitution` | Pré-projeto | `.specs/memory/constitution.md` |
| `/spec-discover` | Phase 0 — Discover | `.specs/features/[f]/discovery.md` |
| `/spec-specify` | Phase 1 — Specify | `.specs/features/[f]/spec.md` |
| `/spec-design` | Phase 2 — Design | `.specs/features/[f]/design.md` |
| `/spec-tasks` | Phase 3 — Tasks | `.specs/features/[f]/tasks.md` |
| `/spec-implement` | Phase 4 — Implement | atualiza `tasks.md` + `validation.md` |
| `/spec-measure` | Phase 5 — Measure | `.specs/features/[f]/measure.md` |
| `/spec-clarify` | Auxiliar | atualiza artefatos in-place |
| `/spec-checklist` | Auxiliar | `.specs/features/[f]/checklist.md` |

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
