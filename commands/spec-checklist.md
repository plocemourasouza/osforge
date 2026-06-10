---
description: Auxiliar — Gera checklist customizado de critérios de aceite para a feature atual, baseado no spec.md e no design.md. Use antes de considerar a implementação concluída ou para gerar critérios de QA. Gatilhos: "checklist", "critérios de aceite", "QA checklist", "pronto para testar", "/spec-checklist [feature]".
---

## Contexto necessário
Leia antes de executar:
- `.specs/features/[feature]/spec.md` — fonte dos Acceptance Criteria
- `.specs/features/[feature]/design.md` — contratos e edge cases técnicos
- `.specs/features/[feature]/tasks.md` (se existir) — tasks concluídas
- `.specs/memory/constitution.md` — padrões de qualidade do projeto

## Fase: Auxiliar — Checklist

## Saída esperada
`.specs/features/[feature-name]/checklist.md`

## Processo

O argumento passado após `/spec-checklist` é a feature. Se vazio, pergunte qual feature.

1. **Leia spec.md na íntegra** e extraia todos os Acceptance Criteria.

2. **Leia design.md** para identificar edge cases técnicos não cobertos explicitamente no AC.

3. **Construir checklist em 5 categorias**:

```markdown
# Checklist: [Feature Name]
**Feature:** [feature-name] | **Data:** [YYYY-MM-DD]
**Referências:** spec.md | design.md

## Funcionalidade (Happy Path)
- [ ] [AC-01 reescrito como verificação executável]
- [ ] [AC-02 reescrito como verificação executável]
- [ ] [cada AC do spec.md vira ao menos um item aqui]

## Edge Cases & Erros
- [ ] Usuário não autenticado → recebe 401 ou redirect para login
- [ ] Input inválido → mensagem de erro exibida no campo correto
- [ ] [edge cases específicos do design.md]
- [ ] [casos de erro listados nos contratos]

## Segurança
- [ ] Server Action verifica autenticação antes de qualquer operação
- [ ] Inputs validados com Zod no entry point
- [ ] Dados sensíveis não expostos em mensagens de erro
- [ ] [verificações específicas do contexto: RLS, multi-tenancy, etc.]

## Performance
- [ ] Sem waterfalls de fetch desnecessários
- [ ] Bundle size: sem barrel imports em componentes críticos
- [ ] [verificações específicas identificadas no design]

## Qualidade de Código
- [ ] `bun test` — 0 failures
- [ ] `bun run build` — exit 0, sem erros TypeScript
- [ ] Lint passa sem erros (`bun run lint`)
- [ ] Todos os ACs mapeados para tasks em tasks.md têm tasks concluídas
```

4. **Confirmar**: Apresente o checklist. Pergunte se há critérios adicionais a incluir antes de iniciar a implementação ou validação.

## Regras
- Cada item do checklist deve ser verificável sem ambiguidade (sim/não, passa/falha)
- Nunca use "funciona corretamente" como critério — descreva o comportamento esperado
- Se o spec.md não tem AC clara para um comportamento esperado, registre no checklist e sinalize para atualizar o spec
- A categoria "Segurança" é obrigatória — nunca omita mesmo para features aparentemente simples
