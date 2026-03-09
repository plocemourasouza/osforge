# User Story: [STORY-ID] [Nome da Feature]

## Contexto de Produto (obrigatório)
- **Problema observado:** [o que o usuário enfrenta hoje — com evidência concreta]
- **Hipótese:** [acreditamos que X resolve porque Y]
- **Alternativas descartadas:** [o que consideramos e por que não seguimos]
- **Risco se não fizermos:** [o que acontece se não implementarmos]

## Story
Como [persona específica, não "o usuário"],
quero [ação concreta]
para que [benefício mensurável].

## Prioridade de Produto
- Impacto no usuário: [Alto / Médio / Baixo]
- Confiança na hipótese: [Alta / Média / Baixa] — base: [dados / feedback / intuição]
- Esforço técnico: [Alto / Médio / Baixo]
- **Score:** (Impacto × Confiança) / Esforço = [valor]

## Métricas de Sucesso
| Métrica | Baseline (atual) | Target | Como medir | Prazo |
|---------|------------------|--------|------------|-------|
| [primária] | [valor] | [meta] | [evento/query] | [semanas] |
| [secundária] | [valor] | [meta] | [evento/query] | [semanas] |

- **Critério de sucesso:** [métrica primária atinge target]
- **Critério de falha:** [se < X% em Y semanas, pivotar]

## Acceptance Criteria (técnicos)
- [ ] AC-1: [Critério verificável]
- [ ] AC-2: [Critério verificável]
- [ ] AC-3: [Critério verificável]

## Optimal Path (Happy Path)
1. Usuário [ação inicial]
2. Sistema [resposta esperada]
3. Usuário [próxima ação]
4. Resultado: [estado final esperado]

## Edge Cases
| ID | Cenário | Input | Expected Output | Severidade |
|----|---------|-------|-----------------|------------|
| EC-1 | Campo vazio | "" | Mensagem de erro de validação | Alta |
| EC-2 | Timeout de rede | >5s sem resposta | Retry com feedback visual | Média |
| EC-3 | Dados inválidos | Formato inesperado | Fallback gracioso | Alta |

## Dependências
- [Feature ou serviço necessário]

## Critério de Completude
Esta story está **DONE** quando:
- TODOS os acceptance criteria técnicos passam
- Todos os edge cases de severidade Alta estão cobertos
- Testes automatizados existem para o happy path
- Código passou em review (ou validator agent)
- **Métricas de sucesso estão configuradas e baseline registrada**
- **Eventos de analytics implementados**
- **Data de revisão de métricas agendada**
