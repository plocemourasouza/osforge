---
description: Phase 2 — Cria o design técnico: arquitetura, modelo de dados, contratos de API e decisões técnicas com trade-offs documentados. Use após /spec-specify. Gatilhos: "design", "arquitetura da feature", "modelo de dados", "contratos de API", "/spec-design [feature]".
---

## Contexto necessário
Leia antes de executar:
- `.specs/features/[feature]/spec.md` — requisitos e acceptance criteria
- `.specs/memory/constitution.md` — padrões de arquitetura do projeto
- `schema.prisma` (se existir) — modelo de dados atual
- `.specs/codebase/ARCHITECTURE.md` (se existir) — arquitetura atual

## Fase: Phase 2 — Design

## Saída esperada
`.specs/features/[feature-name]/design.md`

## Processo

1. **Carregar spec.md**: Leia os requisitos funcionais e acceptance criteria para guiar as decisões de design.

2. **Analisar schema atual**: Se `schema.prisma` existe, verifique o modelo de dados antes de propor alterações. Consulte Supabase MCP para verificar estado real se disponível.

3. **Criar `design.md`**:

```markdown
# Design: [Feature Name]
**Feature:** [feature-name] | **Data:** [YYYY-MM-DD] | **Status:** Draft
**Referência:** [spec.md]

## Arquitetura

### Fluxo de Dados
[Diagrama em texto ou Mermaid mostrando como os dados fluem]

### Componentes Envolvidos
- **[Componente/módulo]**: [responsabilidade nesta feature]
- Server Actions: [quais ações e em qual arquivo]
- API Routes: [apenas se integração externa — justificar por que não é Server Action]
- Componentes React: [Server vs Client — justificar cada Client Component]

## Modelo de Dados

### Alterações no Schema
```prisma
// Novas tabelas ou campos necessários
model [Nome] {
  id        String   @id @default(cuid())
  // ...
}
```

### Migrations necessárias
- [Descreva cada migration em linguagem natural]

### Políticas RLS (se Supabase)
- [Tabela]: [SELECT/INSERT/UPDATE/DELETE] para [role] quando [condição]

## Contratos

### Server Actions
```typescript
// src/actions/[feature].actions.ts
export async function [actionName](input: [InputType]): Promise<[ReturnType]>
```

### Tipos TypeScript
```typescript
// src/types/[feature].types.ts
type [Nome] = {
  // ...
}
```

## Decisões Técnicas

### Decisão 1: [Título]
- **Contexto:** [Por que esta decisão foi necessária]
- **Opções consideradas:**
  - A: [descrição] — Prós: [...] Contras: [...]
  - B: [descrição] — Prós: [...] Contras: [...]
- **Decisão:** [Qual opção e por quê]
- **Consequências:** [O que esta decisão implica para o futuro]

## Impacto em Features Existentes
- [Feature/componente afetado]: [como é impactado, se requer alteração]
- Sem impacto: [áreas verificadas e confirmadas sem impacto]

## Constitution Check
- [ ] Design respeita [princípio arquitetural da constitution]
- [ ] Não há exceção não-documentada aos padrões definidos
```

4. **Confirmar**: Apresente o design. Para decisões com trade-offs significativos, apresente as opções explicitamente e aguarde confirmação antes de gravar a decisão no arquivo. Sugira próximo passo: `/spec-tasks [feature-name]`.

## Regras
- Toda decisão com alternativas não-triviais deve ser documentada como ADR (Architecture Decision Record)
- Server Actions são o padrão; API Routes exigem justificativa explícita
- RLS é obrigatório para tabelas com dados multi-tenant
- Não implemente código nesta fase — apenas contratos e tipos
