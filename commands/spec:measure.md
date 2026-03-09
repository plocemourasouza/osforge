---
description: Phase 5 — Mede o impacto real da feature contra as métricas definidas no discovery.md. Execute após deploy em produção ou ao final de um ciclo de validação. Gatilhos: "measure", "medir impacto", "métricas pós-deploy", "resultado da feature", "ROI", "/spec:measure [feature]".
---

## Contexto necessário
Leia antes de executar:
- `.specs/features/[feature]/discovery.md` — métricas de sucesso definidas antes da implementação
- `.specs/features/[feature]/spec.md` — acceptance criteria como baseline
- `.specs/features/[feature]/validation.md` (se existir) — evidências da implementação

## Fase: Phase 5 — Measure (PDD)

## Saída esperada
`.specs/features/[feature-name]/measure.md`

## Processo

O argumento passado após `/spec:measure` é a feature. Se vazio, pergunte qual feature medir.

1. **Leia `discovery.md`** e extraia as métricas de sucesso definidas na tabela "Métricas de Sucesso".

2. **Coletar dados**: Pergunte ao usuário os valores atuais das métricas (dados de produção, analytics, feedback). Se métricas não foram coletadas ainda, registre como "Pendente" com sugestão de como coletar.

3. **Criar `measure.md`**:

```markdown
# Measure: [Feature Name]
**Feature:** [feature-name] | **Deploy:** [data do deploy] | **Medido em:** [YYYY-MM-DD]

## Resultado vs Hipótese

### Hipótese Original
[copiar da discovery.md]

### Veredicto
**[✅ VALIDADA / ⚠️ PARCIAL / ❌ REFUTAR / ⏳ AGUARDANDO DADOS]**
[1-2 frases explicando o veredicto]

## Métricas
| Métrica | Baseline | Target | Resultado | Δ% | Status |
|---------|----------|--------|-----------|-----|--------|
| [primária] | [baseline] | [target] | [resultado] | [%] | ✅/⚠️/❌ |
| [secundária] | [baseline] | [target] | [resultado] | [%] | ✅/⚠️/❌ |

## Análise
### O que funcionou
- [observação 1]

### O que não funcionou
- [observação 1]

### Surpresas
- [comportamento inesperado, positivo ou negativo]

## Decisão
- [ ] **Continuar** — ampliar rollout, iteração planejada
- [ ] **Pivotar** — [hipótese alternativa a testar]
- [ ] **Abandonar** — [motivo e o que foi aprendido]
- [ ] **Aguardar** — [prazo para reavaliação: YYYY-MM-DD]

## Próximos Passos
- [ação 1 com responsável e prazo]
- [ação 2 com responsável e prazo]

## Aprendizados para o Projeto
[insight relevante para decisões futuras — será extraído para tasks/lessons.md]
```

4. **Extrair aprendizados**: Se o measure.md contiver insights relevantes, atualize (ou crie) `tasks/lessons.md` no projeto com a lição aprendida.

5. **Arquivar feature**: Se o veredicto for "Abandonar" ou "Continuar sem iteração próxima", mova o diretório para `.specs/features/_archived/[feature-name]/`.

## Regras
- Se não há dados de produção disponíveis, registre "Pendente" e defina data de revisão — não invente números
- Métricas ausentes no discovery.md são uma falha de processo — registre no measure.md como lição
- O veredicto deve ser honesto, mesmo que o resultado seja negativo — features que ensinam têm valor
- Aprendizados extraídos para lessons.md devem ser acionáveis ("Nunca X" ou "Sempre Y" ou "Quando Z, faça W")
