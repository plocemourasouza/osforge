---
description: Auxiliar — Resolve ambiguidades e lacunas na especificação ou no design antes de prosseguir para a próxima fase. Use sempre que um artefato de .specs/ tiver campos marcados como "NEEDS CLARIFICATION", "?", ou "A definir". Gatilhos: "clarify", "esclarecer", "lacunas", "ambiguidade", "o que significa", "/spec:clarify [feature]".
---

## Contexto necessário
Leia antes de executar:
- `.specs/features/[feature]/discovery.md` (se existir)
- `.specs/features/[feature]/spec.md` (se existir)
- `.specs/features/[feature]/design.md` (se existir)
- `.specs/memory/constitution.md` (padrões e decisões existentes)

## Fase: Auxiliar — Clarification

## Saída esperada
Atualização in-place dos artefatos em `.specs/features/[feature]/` com as lacunas resolvidas.

## Processo

O argumento passado após `/spec:clarify` é a feature alvo. Se vazio, pergunte qual feature clarificar.

1. **Varredura de lacunas**: Leia todos os artefatos da feature e identifique:
   - Campos com "NEEDS CLARIFICATION", "A definir", "?", "TODO", "TBD"
   - Acceptance Criteria vagos (sem critério mensurável ou verificável)
   - Campos de design sem decisão registrada (ex: schema sem tipos definidos, contrato sem exemplos)
   - Premissas não validadas que impactam a implementação

2. **Agrupar por urgência**:
   - **Bloqueadores**: lacunas que impedem o início da próxima fase
   - **Importantes**: lacunas que geram retrabalho se não resolvidas agora
   - **Não-bloqueadoras**: podem ser resolvidas durante implementação

3. **Formular perguntas precisas** (máximo 5 por rodada):
   - Uma pergunta por lacuna
   - Incluir contexto de por que importa
   - Sugerir opções quando possível (facilita decisão rápida)

4. **Registrar respostas**: Após receber as respostas do usuário, atualize os artefatos in-place:
   - Substitua "NEEDS CLARIFICATION" pela decisão tomada
   - Adicione data e justificativa na seção de "Decisões" do design.md (se existir)
   - Atualize campos de AC com critérios mensuráveis

5. **Confirmar resolução**: Liste as lacunas resolvidas e as ainda pendentes. Se todas as lacunas bloqueadoras foram resolvidas, sugira a próxima fase.

## Regras
- Nunca avance para a próxima fase com lacunas bloqueadoras não resolvidas
- Para lacunas não-bloqueadoras, registre a decisão padrão com uma nota explicando a escolha
- Prefira fazer poucas perguntas bem formuladas a uma lista longa — o usuário tem custo cognitivo por pergunta
- Se a lacuna puder ser resolvida pelo contexto do projeto (constitution.md, código existente), resolva sem perguntar
