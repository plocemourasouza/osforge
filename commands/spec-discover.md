---
description: Phase 0 — Descobre e valida o problema do usuário antes de especificar qualquer solução. Garante que estamos construindo a coisa certa. Use ao iniciar qualquer feature que afete o usuário final. Gatilhos: "discover", "qual problema resolver", "por que construir", "validar hipótese", "problema do usuário", "/spec-discover [feature]".
---

## Contexto necessário
Leia antes de executar:
- `.specs/memory/constitution.md` (se existir)
- `.specs/project/PROJECT.md` (se existir)
- `.specs/project/STATE.md` (sessões anteriores)

## Fase: Phase 0 — Discover (PDD)

## Saída esperada
`.specs/features/[feature-name]/discovery.md`

## Processo

O argumento passado após `/spec-discover` é a descrição da feature. Se vazio, pergunte: "Qual feature ou problema você quer explorar?"

1. **Gerar nome da feature**: 2-4 palavras em kebab-case extraindo as keywords mais significativas.
   - "adicionar autenticação com Google" → `google-auth`
   - "corrigir timeout no checkout" → `fix-checkout-timeout`

2. **Criar diretório**: `.specs/features/[feature-name]/`

3. **Fazer perguntas de discovery** (máximo 4, só se necessário):
   - Quem é o usuário afetado por este problema?
   - Qual evidência temos de que este é um problema real?
   - Como saberemos que resolvemos o problema?
   - O que NÃO está no escopo do MVP?

4. **Criar `discovery.md`** com a estrutura abaixo, usando informações do input e inferências do contexto:

```markdown
# Discovery: [Feature Name]
**Feature:** [feature-name] | **Data:** [YYYY-MM-DD] | **Status:** Draft

## Problema do Usuário
- **Quem sofre:** [persona específica]
- **O que acontece:** [situação atual — dor concreta, observável]
- **Evidência:** [dados, feedback, métricas ou observações]
- **Frequência:** [diário / semanal / ocasional]

## Hipótese
Acreditamos que [solução proposta] vai [resultado esperado] para [persona]
porque [razão baseada em evidência].

## Métricas de Sucesso
| Métrica | Baseline (atual) | Target | Como medir | Prazo |
|---------|------------------|--------|------------|-------|
| [primária] | [valor] | [meta] | [como] | [semanas] |
| [secundária] | [valor] | [meta] | [como] | [semanas] |

## Critério de Decisão
- **Sucesso:** [métrica primária atinge target em prazo]
- **Pivotar:** [se métrica < X% do target]
- **Abandonar:** [se após Y semanas sem melhora]

## MVP Scope
- **Inclui:** [funcionalidades mínimas para testar hipótese]
- **NÃO inclui:** [o que pode esperar]

## Prioridade
Impacto: [Alto/Médio/Baixo] × Confiança: [Alta/Média/Baixa] / Esforço: [Alto/Médio/Baixo]
Score: [calcule: H=3, M=2, L=1 → (Impacto × Confiança) / Esforço]

## Alternativas Consideradas
- Não fazer nada: [consequência]
- [Alternativa A]: descartada porque [razão]
```

5. **Confirmar**: Apresente o discovery criado. Pergunte se deseja prosseguir para `/spec-specify` ou se há ajustes.

## Regras
- NUNCA pule esta fase para features que tocam o usuário final
- Para tasks puramente técnicas (refactoring, infra, CI/CD), esta fase é opcional
- Se não há evidência do problema, sinalize e sugira coletar dados antes de especificar
- Se não consegue definir métrica de sucesso, o escopo está vago demais — resolva antes de avançar
