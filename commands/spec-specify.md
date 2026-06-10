---
description: Phase 1 — Cria a especificação técnica detalhada de uma feature: requisitos funcionais, não-funcionais, acceptance criteria e casos de uso. Use após /spec-discover ou quando o problema já está validado. Gatilhos: "specify", "especificar feature", "escrever spec", "requisitos técnicos", "/spec-specify [feature]".
---

## Contexto necessário
Leia antes de executar:
- `.specs/features/[feature]/discovery.md` — problema e hipótese validados
- `.specs/memory/constitution.md` — princípios e padrões do projeto
- `.specs/project/STATE.md` (se existir) — contexto de sessões anteriores

## Fase: Phase 1 — Specify

## Saída esperada
`.specs/features/[feature-name]/spec.md`

## Processo

1. **Identificar feature**: Se o argumento após `/spec-specify` nomeia a feature, use-o. Caso contrário, verifique qual feature tem `discovery.md` mais recente ou pergunte.

2. **Verificar constitution**: Se `.specs/memory/constitution.md` existe, verifique se a feature respeita os princípios definidos. Se violar algum, sinalize antes de continuar.

3. **Fazer perguntas de especificação** (máximo 4, só se genuinamente ambíguo):
   - Quais são os fluxos principais do usuário?
   - Há integrações externas envolvidas?
   - Quais são as restrições de performance aceitáveis?
   - Como tratar estados de erro?

4. **Criar `spec.md`**:

```markdown
# Spec: [Feature Name]
**Feature:** [feature-name] | **Data:** [YYYY-MM-DD] | **Status:** Draft
**Referência:** [discovery.md]

## Contexto
[2-3 frases resumindo o problema e hipótese do discovery]

## Requisitos Funcionais
### RF-01: [Nome do requisito]
- **Descrição:** [O que o sistema deve fazer]
- **Usuário:** [Quem executa esta ação]
- **Fluxo principal:** [Passos do happy path]
- **Fluxos alternativos:** [Variações aceitas]
- **Erros e exceções:** [O que acontece quando falha]

### RF-02: ...

## Requisitos Não-Funcionais
- **Performance:** [ex: response time < 200ms para 95% das requests]
- **Segurança:** [validações, autenticação necessária, RLS]
- **Acessibilidade:** [WCAG nível mínimo, comportamento com teclado]
- **Disponibilidade:** [uptime esperado, degradação aceitável]

## Acceptance Criteria
Dado que [contexto], quando [ação], então [resultado esperado].

- [ ] AC-01: Dado que [condição], quando [ação], então [resultado]
- [ ] AC-02: ...
- [ ] AC-ERROR-01: Dado que [condição de erro], quando [ação], então [comportamento de erro]

## Fora do Escopo
- [Item que poderia ser confundido como incluído mas não está]
- [Feature relacionada que será tratada separadamente]

## Dependências
- [API externa, serviço, feature que deve existir antes]

## Constitution Check
- [ ] Respeita [princípio 1 da constitution]
- [ ] Respeita [princípio 2]
- [ ] Não introduz exceções aos padrões de qualidade definidos
```

5. **Confirmar**: Apresente a spec criada. Sinalize qualquer ambiguidade que ficou não-resolvida. Sugira próximo passo: `/spec-design [feature-name]`.

## Regras
- Acceptance Criteria devem ser verificáveis — nada de "o sistema deve ser rápido"
- Cada AC deve mapear para um teste que pode ser escrito
- Constitution check é obrigatório se constitution.md existe
- Não especifique implementação — isso é para /spec-design
