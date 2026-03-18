# Regras de Compressão

## STRIP — Remover completamente
- Transições: "Como mencionado", "Vale notar", "Além disso", "Conforme discutido"
- Retórica: "Isso é revolucionário", "O mais interessante é", "É importante destacar"
- Hedging: "Acreditamos", "Provavelmente", "Talvez", "Parece que"
- Auto-referência: "Este documento descreve", "Conforme acima", "Como veremos"
- Conhecimento comum: "Vercel é uma plataforma cloud", "MIT é licença open-source", "TypeScript é um superset de JavaScript"
- Introduções repetidas do mesmo conceito
- Parágrafos de transição entre seções
- Formatação decorativa (bold para ênfase, linhas horizontais, emojis)
- Filler: "A fim de", "Deve-se notar que", "O fato de que", "É necessário que"
- Saudações e fechamentos formais
- Disclaimers genéricos

## PRESERVE — Manter sempre
- Números, datas, versões, percentuais específicos
- Named entities (produtos, empresas, pessoas, tecnologias)
- Decisões + rationale (comprimido: "Decisão: X. Razão: Y")
- Alternativas rejeitadas + motivo (comprimido: "Rejeitado: X. Razão: Y")
- Constraints explícitos e não-negociáveis
- Dependências e relações de ordenação
- Questões em aberto e itens não resolvidos
- Limites de escopo (in/out/deferred)
- Critérios de sucesso e como são validados
- Segmentos de usuário e o que sucesso significa para cada
- Riscos com sinais de severidade
- Conflitos entre documentos fonte
- Variáveis de ambiente e configurações
- URLs, endpoints, connection strings
- Regras de negócio com condicionais

## TRANSFORM — Mudar forma para eficiência
- Prosa longa → bullet denso com mesma informação
- "Decidimos usar X porque Y e Z" → "X (rationale: Y, Z)"
- Labels de categoria repetidos → agrupar sob heading único
- "Risco: ... Severidade: alta" → "RISCO ALTO: ..."
- Condicionais → forma "Se X → Y"
- Explicações multi-sentença → comprimido com semicolons
- Listas de itens curtos relacionados → bullet único com semicolons
- "X é usado para Y" → "X: Y" (quando contexto é claro)
- Enumerações verbosas → listas entre parênteses: "platforms (Cursor, Claude Code, Windsurf)"
- Tabelas com muitas colunas → bullets com key:value
- Code blocks com comentários → code sem comentários (o bullet acima explica)

## DEDUPLICAÇÃO
- Mesmo fato em múltiplos docs → manter versão com mais contexto
- Mesmo conceito em diferentes níveis de detalhe → manter o detalhado
- Listas sobrepostas → merge em lista única sem duplicatas
- Docs discordantes → notar conflito: "Doc A: X; Doc B: Y — não resolvido"
- Executive summary + expansão posterior → manter apenas expansão
- Framing introdutório repetido → capturar uma vez sob tema mais relevante
