---
description: Phase 3 — Gera o plano de tarefas atômicas com ordem de dependência e critérios de verificação por task. Use após /spec-design. Gatilhos: "tasks", "gerar tarefas", "plano de implementação", "decompor em tasks", "/spec-tasks [feature]".
---

## Contexto necessário
Leia antes de executar:
- `.specs/features/[feature]/spec.md` — acceptance criteria (cada AC vira ao menos 1 task)
- `.specs/features/[feature]/design.md` — contratos, schema, arquitetura
- `.specs/memory/constitution.md` — padrões de qualidade (cobertura de testes, etc.)

## Fase: Phase 3 — Tasks

## Saída esperada
`.specs/features/[feature-name]/tasks.md`

## Processo

1. **Leia spec.md e design.md** na íntegra antes de gerar qualquer task.

2. **Prioridade por impacto no usuário**:
   ```
   Score = (Impacto × Confiança) / Esforço
   H=3, M=2, L=1
   ```
   - Score > 4 → Fazer primeiro
   - Score 2-4 → Fazer neste ciclo
   - Score < 2 → Backlog

3. **Estrutura de cada task**: Atômica de 2-5 minutos. Especificar paths exatos. Sem ambiguidade sobre o que "feito" significa.

4. **Criar `tasks.md`**:

```markdown
# Tasks: [Feature Name]
**Feature:** [feature-name] | **Data:** [YYYY-MM-DD] | **Estimativa:** [total]
**Referências:** spec.md | design.md

## Resumo
- Total de tasks: [N]
- Estimativa total: [X horas / Y dias]
- Dependências externas: [migrations, serviços, aprovações necessárias]

## Tasks

### Setup & Foundation
- [ ] **T-01**: Criar migration `[nome]` para [tabela/campo]
  - Arquivo: `prisma/migrations/[timestamp]_[nome]/migration.sql`
  - Critério: `bun prisma migrate dev` executa sem erro
  - Estimativa: 15min

- [ ] **T-02**: Gerar Prisma Client após migration
  - Comando: `bun prisma generate`
  - Critério: sem erros de tipo em `src/generated/prisma`
  - Estimativa: 5min

### Lógica de Negócio (TDD — escrever testes antes)
- [ ] **T-03**: Escrever teste para [Server Action]
  - Arquivo: `src/actions/__tests__/[feature].actions.test.ts`
  - Critério: teste falha (RED) — verificar com `bun test`
  - Estimativa: 20min

- [ ] **T-04**: Implementar [Server Action]
  - Arquivo: `src/actions/[feature].actions.ts`
  - Contrato: ver design.md seção "Server Actions"
  - Critério: teste T-03 passa (GREEN) — verificar com `bun test`
  - Estimativa: 30min

- [ ] **T-05**: Refatorar [Server Action] se necessário
  - Critério: todos os testes passam + código segue padrões da constitution
  - Estimativa: 15min

### Interface (componentes)
- [ ] **T-06**: Criar componente `[Nome]` (Server Component)
  - Arquivo: `src/components/[feature]/[Nome].tsx`
  - Props: ver design.md seção "Componentes React"
  - Critério: renderiza sem erros em desenvolvimento
  - Estimativa: 45min

### Integração
- [ ] **T-07**: Conectar componente com Server Action
  - Critério: AC-01 do spec.md pode ser verificado manualmente
  - Estimativa: 20min

### Validação Final
- [ ] **T-08**: Rodar suite completa de testes
  - Comando: `bun test`
  - Critério: 0 failures, 0 skipped
  - Estimativa: 5min

- [ ] **T-09**: Build de produção
  - Comando: `bun run build`
  - Critério: exit 0, sem erros TypeScript
  - Estimativa: 5min

## Mapeamento AC → Tasks
| Acceptance Criteria | Tasks que validam |
|---|---|
| AC-01 | T-03, T-04, T-07 |
| AC-02 | T-05, T-06 |
| AC-ERROR-01 | T-03 (caso de erro) |
```

5. **Confirmar**: Apresente a lista de tasks. Para features complexas, pergunte se o usuário quer decompor mais alguma task antes de iniciar.

## Regras
- Toda task deve ter critério de verificação executável (comando + saída esperada)
- Tasks de teste SEMPRE antes de tasks de implementação (TDD)
- Nunca agrupe "implementar X e Y" numa task — uma responsabilidade por task
- O mapeamento AC → Tasks garante que nenhum acceptance criteria fique sem cobertura
