---
name: dispatching-parallel-agents
description: "Orquestra tasks paralelas em subagents independentes. ACIONE quando: 2+ tasks sem estado compartilhado, refatoração em múltiplos arquivos não relacionados, decomposição revela trabalho paralelizável, ou tasks com dependências parciais. Keywords: parallel, wave, dispatch, parallel agents, multiple tasks, independent, subagents."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: osforge
  version: '1.2'
  source: Superpowers (obra)
  inspired_by: gsd-build/get-shit-done (wave execution pattern)
---

# Dispatching Parallel Agents

## When to Parallelize
Use parallel agents when tasks are:
- **Independent** — no shared state between them
- **Non-sequential** — output of one doesn't feed into another
- **Bounded** — each has clear completion criteria

## Decision Matrix

| Scenario | Strategy | Why |
|----------|----------|-----|
| 3 independent API endpoints | ✅ Parallel | No shared state |
| Frontend + backend for same feature | ❌ Sequential | Backend API feeds frontend |
| Tests for 5 different modules | ✅ Parallel | Independent test suites |
| Migration + seed data | ❌ Sequential | Seed depends on schema |
| Code review + docs update | ✅ Parallel | Independent outputs |
| 10 file refactoring (same pattern) | ✅ Parallel | Each file is independent |

## Task Specification Format
Each parallel task MUST be self-contained with:

```markdown
## Task: [Name]
**Goal:** One sentence describing the deliverable
**Files:** List of files to create/modify
**Context:** Any shared knowledge needed (types, patterns, conventions)
**Acceptance:** How to verify completion
**Constraints:** What NOT to touch
```

## Execution Pattern (Claude Code)
```markdown
### Plan: Implement User Dashboard

I'll dispatch 3 parallel tasks:

**Task 1: Stats API**
- Create `app/api/dashboard/stats/route.ts`
- Query: project count, task completion rate, recent activity
- Test: `__tests__/api/dashboard-stats.test.ts`

**Task 2: Activity Feed Component**
- Create `components/dashboard/activity-feed.tsx`
- Server Component fetching from activity table
- Test: `__tests__/components/activity-feed.test.tsx`

**Task 3: Quick Actions Widget**
- Create `components/dashboard/quick-actions.tsx`
- Client Component with action buttons
- Test: `__tests__/components/quick-actions.test.tsx`

These are independent — no shared state. Dispatching in parallel.
```

## Merge Strategy
After all parallel tasks complete:
1. **Integration test** — verify tasks work together
2. **Import resolution** — connect components/APIs at the page level
3. **Type check** — `bun tsc --noEmit` to catch interface mismatches
4. **Visual verification** — check the composed result

## Anti-Patterns
- ❌ Parallelizing tasks that share a database migration
- ❌ Dispatching without clear file boundaries (merge conflicts)
- ❌ Parallel tasks with implicit ordering (A creates type, B uses it)
- ❌ More than 5 parallel tasks (coordination overhead > benefit)

## Context Embedding
Each task gets a minimal context package:
```markdown
**Shared Types:** (paste relevant interfaces)
**Naming Convention:** (paste from coding-guidelines)
**Test Pattern:** (paste TDD example from tdd-workflow)
```
This makes each task self-contained — the agent doesn't need to search for conventions.

## Integration with Planner
The `planner` agent identifies parallelizable tasks during decomposition:
- Simple tasks → sequential (no overhead)
- Moderate tasks → evaluate for parallel if >2 independent units
- Complex tasks → likely parallel after spec critique by `validator`

---

## Wave Execution (dependency-aware parallelism)

Use wave execution when tasks have **partial dependencies** — some are independent,
others depend on earlier results. Inspired by the GSD phase execution model.

### How waves work

Group tasks into waves based on their dependency graph:
- **Same wave** → run in parallel (no dependency between them)
- **Next wave** → waits for ALL tasks in the previous wave to complete
- **File conflicts** → put conflicting tasks in the same sequential plan or the same wave with non-overlapping files

```
WAVE 1 (parallel)           WAVE 2 (parallel)        WAVE 3
┌─────────────┐ ┌──────────┐  ┌──────────┐ ┌───────┐  ┌──────────┐
│ User schema │ │ Product  │  │ Orders   │ │ Cart  │  │ Checkout │
│ + migration │ │ schema   │  │ API      │ │ API   │  │ UI       │
└─────────────┘ └──────────┘  └──────────┘ └───────┘  └──────────┘
       │               │           ↑            ↑           ↑
       └───────────────┴───────────┴────────────┘           │
          Wave 2 tasks depend on Wave 1 schemas      Depends on both Wave 2 tasks
```

### Wave planning format

```markdown
## Wave Execution Plan

### Wave 1 — Foundation (parallel)
**Task 1A: User Model**
- Files: `prisma/schema.prisma` (User model only)
- Goal: User + auth fields
- No dependencies

**Task 1B: Product Model**
- Files: `prisma/schema.prisma` (Product model only)
- Goal: Product + inventory fields
- No dependencies
⚠️ Note: Tasks 1A and 1B modify schema.prisma — coordinate to avoid conflicts
   by having each agent append their model block without touching the other's section.

### Wave 2 — APIs (parallel, after Wave 1)
**Task 2A: Orders API**
- Files: `app/api/orders/route.ts`
- Depends on: Wave 1 (User + Product models exist)

**Task 2B: Cart API**
- Files: `app/api/cart/route.ts`
- Depends on: Wave 1 (User + Product models exist)

### Wave 3 — UI (after Wave 2)
**Task 3A: Checkout Page**
- Files: `app/checkout/page.tsx`
- Depends on: Wave 2 (Orders API + Cart API complete)
```

---

### YAML-driven wave assembly (machine-readable plans)

Quando o plano de tasks contém blocos YAML com os campos `id`, `depends_on`, `wave` e `parallel_ok`, as waves DEVEM ser montadas a partir desses dados — não inferidas da prosa.

**Algoritmo de leitura:**

1. Coletar todos os blocos YAML do `tasks.md`.
2. Agrupar por `wave` (número inteiro).
3. Dentro de cada wave, separar tasks com `parallel_ok: true` (paralelizáveis) das com `parallel_ok: false` (sequenciais dentro da wave).
4. Verificar que `depends_on` de cada task aponta para tasks em waves anteriores (consistência).
5. Despachar cada wave completa antes de iniciar a próxima.

**Exemplo — leitura de YAML para Wave Execution Plan:**

```yaml
# tasks.md (excerto de blocos YAML)
- id: T1
  depends_on: []
  wave: 1
  parallel_ok: true

- id: T2
  depends_on: [T1]
  wave: 2
  parallel_ok: true

- id: T3
  depends_on: [T1]
  wave: 2
  parallel_ok: true

- id: T4
  depends_on: [T2, T3]
  wave: 3
  parallel_ok: true
```

Resultado do dispatch:

```
Wave 1 → despachar T1 (sozinho)
Wave 2 → despachar T2 + T3 em paralelo (ambos parallel_ok: true)
Wave 3 → despachar T4 após T2 e T3 concluírem
```

**Fallback (planos sem YAML):** se nenhum bloco YAML for encontrado, inferir waves a partir da prosa e dos campos `Depends on:` de cada task (comportamento anterior). Documentar que o plano não é machine-readable e sugerir adição do YAML.

### When to use waves vs flat parallel

| Scenario | Use |
|---|---|
| All tasks truly independent | Flat parallel (original pattern) |
| Some tasks depend on others | Wave execution |
| Linear pipeline (A→B→C→D) | Sequential — no parallelism benefit |
| Mixed: some parallel, some sequential | Wave execution |

### Fresh context per wave

Each wave's agents start with a clean 200K context window. Pass only what they need:
- Relevant schema excerpts (not the full Prisma file)
- Interfaces/types the task depends on
- Conventions from project-context.md

This keeps each agent fast and focused — no accumulated context degradation.


---

## Gotchas

- **Tasks que modificam o mesmo arquivo em paralelo**: se duas tasks precisam editar `prisma/schema.prisma` ou o mesmo componente, NÃO as paralelize — coloque-as sequenciais ou coordene via sections não sobrepostas. Conflito de merge é garantido.
- **Não fornecer tipos/interfaces compartilhadas**: cada agente paralelo recebe contexto mínimo. Se Tasks B e C dependem de um tipo criado por Task A, passe esse tipo explicitamente no prompt de B e C — eles não compartilham contexto entre si.
- **Mais de 5 tasks paralelas**: overhead de coordenação supera o benefício acima de 5 tasks simultâneas. Se precisar de mais, agrupe em waves de no máximo 5.
- **Dependência implícita**: "tarefa de seed data" parece independente mas depende de migrations completas. Mapeie dependências antes de paralelizar — cada wave deve documentar dependências explicitamente.
- **Não verificar integração pós-merge**: agents paralelos podem produzir interfaces incompatíveis entre si. Sempre rodar `bun tsc --noEmit` e integration tests após merge das tasks paralelas.
- **Wave 1 com schema**: se Wave 1 tem tasks em `prisma/schema.prisma`, cada agent deve trabalhar apenas no seu bloco de models sem tocar os blocos alheios — ou fazer o schema sempre sequencial.
