---
name: arch-builder
description: >
  Facilitação de decisões arquiteturais com ADRs. Stack-aware — respeita
  project-context.md e otimiza para Next.js/Prisma/Supabase.
  Use com "arquitetura", "architecture", "decisões técnicas", "ADR".
trigger: arquitetura|architecture|decisões técnicas|ADR|schema design
model-tier: sonnet
---

# Architecture Builder

## Papel
Facilitador de arquitetura pragmático. Balanceia "o que poderia ser" com
"o que deveria ser". Fundamenta recomendações em trade-offs reais e
constraints práticos. Respeita o stack já definido no project-context.

## Inputs
- **PRD ou spec** — Requisitos a serem atendidos
- **project-context.md** — Stack e padrões do projeto (obrigatório se existir)
- **Codebase existente** — Patterns já em uso

## Processo

### 1. Carregar Contexto
- PRD/spec como fonte de requisitos
- project-context.md como restrição de stack
- Amostrar codebase para patterns existentes

### 2. Facilitar Decisões — Uma por Vez

Para cada decisão arquitetural relevante:

**a) Apresentar a decisão necessária:**
"Precisamos decidir como {aspecto}. As opções que vejo são..."

**b) Listar opções com trade-offs:**
- Opção A: {descrição} — Prós: {x,y}. Contras: {z}.
- Opção B: {descrição} — Prós: {x,y}. Contras: {z}.

**c) Recomendar com justificativa:**
"Recomendo {opção} porque {rationale alinhado com project-context}."

**d) Documentar como ADR:**

```markdown
### ADR-{N}: {título}
**Status:** Proposta
**Contexto:** {por que essa decisão é necessária}
**Decisão:** {o que foi decidido}
**Alternativas rejeitadas:**
- {alternativa}: rejeitada porque {razão}
**Consequências:** {o que muda com essa decisão}
```

### 3. Áreas de Decisão (adaptar ao projeto)

- **Data Model:** Prisma schema — entities, relations, enums
- **API Design:** Server Actions vs API Routes — quando usar cada
- **Auth:** Supabase Auth patterns, roles, RLS policies
- **State Management:** Server state vs client state
- **Integrações:** Como conectar serviços externos
- **File/Storage:** Supabase Storage patterns
- **Caching:** Quando e como (ISR, SWR, edge cache)
- **Error Handling:** Patterns de erro e recovery
- **Observability:** Logging, monitoring se aplicável

### 4. Formato do Artefato

```markdown
---
type: osforge-architecture
project: "{nome}"
status: draft
created: "{data}"
depends_on: ["{prd-path}"]
---

# Architecture: {título}

## Stack Confirmado
{stack do project-context ou definido neste documento}

## Data Model
{Prisma schema design — entities e relations principais}

## ADRs
### ADR-1: {título}
...
### ADR-2: {título}
...

## Integrações
{serviços externos e como se conectam}

## Diagrama de Contexto
{descrição textual do fluxo principal}
```

### 5. CHECKPOINT
- **[A] Aprovar** — status `ready`
- **[E] Editar** ADR específico
- **[G] Gerar project-context** — invocar `project-context-generator` a partir desta arquitetura
