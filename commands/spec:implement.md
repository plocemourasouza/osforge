---
description: Phase 4 — Executa a implementação e validação da feature seguindo TDD e o plano de tasks.md. Processa tasks em ordem de dependência, escreve testes antes do código, e valida ao concluir. Gatilhos: "implement", "implementar", "executar tasks", "desenvolver", "codificar", "/spec:implement [feature]".
---

## Contexto necessário
Leia antes de executar:
- `.specs/features/[feature]/tasks.md` — lista de tasks a executar
- `.specs/features/[feature]/spec.md` — acceptance criteria (referência durante implementação)
- `.specs/features/[feature]/design.md` — contratos, schema, arquitetura
- `.specs/memory/constitution.md` — padrões, convenções e princípios do projeto

## Fase: Phase 4 — Implement + Validate (PDD)

## Saída esperada
- Código implementado conforme design.md
- Tasks marcadas como `[x]` em `.specs/features/[feature]/tasks.md`
- `.specs/features/[feature]/validation.md` ao concluir

## Processo

O argumento passado após `/spec:implement` é a feature. Se vazio, pergunte qual feature implementar. Se não houver `tasks.md`, execute `/spec:tasks` antes.

### Antes de iniciar
1. Leia `tasks.md` e identifique a primeira task não concluída
2. Verifique se há dependências externas não resolvidas (migrations pendentes, serviços, aprovações)
3. Se houver tasks com "NEEDS CLARIFICATION", execute `/spec:clarify` antes de prosseguir

### Por task
Execute cada task rigorosamente em ordem de dependência:

**Para tasks de teste (prefixo T-0X com "escrever teste"):**
1. Escreva o teste conforme especificado
2. Execute: confirm RED — o teste deve falhar pelo motivo correto
3. Registre: marque `[ ]` com nota `(RED confirmado)`

**Para tasks de implementação (código de produção):**
1. Escreva o código mínimo para passar o teste
2. Execute: confirm GREEN — o teste deve passar
3. Refatore se necessário (REFACTOR) mantendo GREEN
4. Marque `[x]` na task com evidência: `(bun test — 0 failures)`

**Para tasks sem teste associado (setup, config, migration):**
1. Execute a task
2. Verifique conforme o critério listado na task
3. Marque `[x]` com evidência do critério cumprido

### Ao concluir todas as tasks
1. Execute a suite completa: `bun test` → deve ter 0 failures
2. Execute build: `bun run build` → deve ter exit 0
3. Execute lint: `bun run lint` → deve ter 0 errors
4. Crie `.specs/features/[feature]/validation.md`:

```markdown
# Validation: [Feature Name]
**Data:** [YYYY-MM-DD] | **Status:** VALIDATED

## Evidências de Verificação
- Testes: `bun test` — [N] passed, 0 failures, 0 skipped
- Build: `bun run build` — exit 0
- Lint: `bun run lint` — 0 errors

## Acceptance Criteria Verificados
| AC | Status | Como verificado |
|---|---|---|
| AC-01 | ✅ PASS | [forma de verificação] |
| AC-02 | ✅ PASS | [forma de verificação] |

## Decisões Tomadas Durante Implementação
- [decisão 1 e justificativa]
- [decisão 2 e justificativa]

## Pendências (se houver)
- [item pendente e motivo]
```

5. Sugira `/spec:measure` para registrar métricas pós-deploy.

## Regras
- **NUNCA declare concluído sem evidência de verificação fresca**
- TDD é obrigatório para toda lógica de negócio — não pule o ciclo RED-GREEN-REFACTOR
- Se um teste não pode ser escrito para uma funcionalidade, questione se o design está claro o suficiente
- Commits só com autorização explícita do usuário
- Se encontrar bloqueador durante implementação, pare e descreva o bloqueador — não improvise solução que desvie do design
