---
name: autorefine-skill
description: "Refinamento autônomo iterativo de skills do OSForge. ACIONE quando: usuário pede 'melhorar uma skill', 'otimizar a skill X', 'a skill Y não está funcionando bem', 'iterar sobre skill', 'autorefine'. Também acionar quando uma skill existente produz outputs inconsistentes ou abaixo do esperado. Keywords: melhorar skill, refinar skill, otimizar skill, autorefine, iteração de skill, skill inconsistente, skill não dispara."
model: sonnet
allowed-tools: Read, Write, Bash, Glob
metadata:
  author: osforge
  version: '1.1'
  inspired_by: karpathy/autoresearch
---

# AutoRefine Skill

## Princípio

Aplicar o loop de pesquisa autônoma do autoresearch ao próprio OSForge: em vez de iterar sobre código de treinamento de LLM, iterar sobre `SKILL.md` de skills existentes. O agente modifica a skill, avalia o output, mantém ou descarta, e repete — dentro de um budget fixo de iterações.

O humano programa o **escopo da melhoria** (equivalente ao `program.md` do autoresearch). O agente itera sobre o **conteúdo da skill** (equivalente ao `train.py`). Você nunca toca nos arquivos de skill diretamente durante o loop — apenas avalia e decide manter ou reverter.

---

## Quando usar

- Uma skill produz outputs inconsistentes ou abaixo do esperado
- O usuário quer explorar variações de instrução de uma skill
- Uma skill foi integrada de repositório externo e precisa de adaptação ao padrão OSForge
- O usuário quer otimizar o campo `description` de uma skill para melhorar o triggering

---

## Setup inicial

Antes de iniciar o loop, colete do usuário:

1. **Qual skill refinar?** (nome do diretório em `skills/`)
2. **Qual o problema ou objetivo?** ("a skill gera código sem TypeScript", "quero que ela sempre produza OpenUI Lang antes do código", etc.)
3. **Quantas iterações?** Default: 5. Máximo recomendado: 10.
4. **Quais prompts de teste?** Peça 2–3 exemplos reais. Se o usuário não tiver, gere você mesmo e confirme antes de rodar.
5. **Critério de sucesso?** O que torna um output "melhor"? (Ex: "sempre inclui tipagem TypeScript", "nunca usa `any`", "sempre começa com bloco OpenUI Lang")

Snapshot obrigatório antes de qualquer modificação:
```bash
cp -r skills/<nome-da-skill> skills/<nome-da-skill>-snapshot-$(date +%Y%m%d%H%M)
```

---

## O Loop (modify → evaluate → keep/discard → repeat)

### Budget fixo

Cada iteração tem um **budget fixo de complexidade**: máximo de 1 modificação substancial por iteração. Não reescreva a skill inteira de uma vez — faça hipóteses pequenas e testáveis, como um pesquisador. Isso torna os resultados interpretáveis.

### Estrutura de cada iteração

```
Iteração N:
  1. [haiku]  Lê o SKILL.md atual
  2. [haiku]  Formula hipótese: "se eu adicionar/remover/reescrever X, o output Y vai melhorar porque Z"
  3. [haiku]  Aplica a modificação ao SKILL.md
  4. [haiku]  Executa os prompts de teste com a skill modificada
  5. [sonnet] Avalia os outputs contra o critério de sucesso
  6. [sonnet] Decide: KEEP (val melhorou) ou DISCARD (revert ao estado anterior)
  7. Registra no log de iterações
```

### Modelo por etapa (smart-model-dispatch)

| Etapa | Modelo | Razão |
|---|---|---|
| Leitura + hipótese | Haiku | Mecânico, baixo custo |
| Modificação do SKILL.md | Haiku | Segue padrão claro |
| Execução dos prompts de teste | Haiku | Geração de outputs |
| Avaliação dos outputs | Sonnet | Requer julgamento qualitativo |
| Decisão keep/discard | Sonnet | Raciocínio sobre critério de sucesso |
| Síntese final (relatório) | Sonnet | Análise do progresso |

Use Opus apenas se o critério de sucesso for ambíguo e exigir raciocínio profundo sobre tradeoffs arquiteturais.

### Log de iterações

Mantenha um arquivo `autorefine-log.md` dentro do diretório da skill durante o processo:

```markdown
# AutoRefine Log — <nome-da-skill>
Data: <data>
Budget: <N> iterações
Critério: <critério de sucesso>

## Iteração 1
- Hipótese: ...
- Modificação: ...
- Resultado: KEEP | DISCARD
- Razão: ...

## Iteração 2
...

## Resultado final
- Melhor versão: iteração N
- Val score inicial: X/3 prompts aprovados
- Val score final: Y/3 prompts aprovados
- Resumo das mudanças que funcionaram: ...
```

Remova o `autorefine-log.md` após aprovação do usuário, ou mova para `skills/<nome>-snapshot-*/`.

---

## Métricas de avaliação

Adapte as métricas ao tipo de skill. Exemplos:

### Skills de geração de código
- [ ] Output sempre tem tipagem TypeScript válida
- [ ] Nenhum uso de `any` sem justificativa
- [ ] Imports organizados (external → internal → relative)
- [ ] Segue convenções do projeto (App Router, Server Actions, etc.)

### Skills de UI (openui-genui-layout)
- [ ] Sempre produz bloco OpenUI Lang antes do código
- [ ] Usa apenas componentes shadcn/ui nativos
- [ ] Seleciona padrão canônico correto para o contexto

### Skills de documentação
- [ ] Inclui todos os campos obrigatórios
- [ ] Tom e idioma consistentes
- [ ] Sem vazamento de informações internas

### Skills de análise
- [ ] Cobre todos os aspectos solicitados
- [ ] Cita fontes ou contexto quando necessário
- [ ] Conclui com recomendação acionável

---

## Condições de parada

Encerre o loop antes de esgotar o budget se:

1. **Convergência** — 3 iterações consecutivas resultaram em KEEP sem melhoria adicional mensurável
2. **Saturação** — 100% dos prompts de teste aprovados por 2 iterações consecutivas
3. **Regressão persistente** — 3 iterações consecutivas resultaram em DISCARD (a hipótese de melhoria está errada; pare e discuta com o usuário)
4. **Budget esgotado** — N iterações concluídas

---

## Relatório final

Ao encerrar o loop, apresente ao usuário:

```
## AutoRefine — Resultado Final

Skill: <nome>
Iterações executadas: N/budget
Prompts de teste aprovados: Y/total (era X/total)

### O que melhorou
- <mudança 1 que foi mantida>
- <mudança 2 que foi mantida>

### O que não funcionou
- <hipótese descartada 1>
- <hipótese descartada 2>

### Próximos passos sugeridos
- <sugestão baseada nas iterações descartadas>

O snapshot da versão original está em: skills/<nome>-snapshot-<timestamp>/
```

Ofereça fazer commit da versão refinada com mensagem convencional:
```
refine(skills): autorefine <nome-da-skill> — N iterações, val +X%
```

Aguarde aprovação explícita antes de commitar.


## Gotchas

- **Modificar muita coisa por iteração**: o loop funciona com hipóteses pequenas e testáveis. Reescrever o SKILL.md inteiro em uma iteração é o erro mais comum — torna impossível saber o que causou melhoria ou regressão.
- **Não fazer snapshot antes**: se esquecer o `cp -r skills/<nome> skills/<nome>-snapshot-...` antes de começar, não há como reverter para a versão original. O snapshot é obrigatório — não é opcional.
- **Critério de sucesso vago**: "ficar melhor" não é um critério. O critério precisa ser binário e verificável: "sempre inclui bloco TypeScript com tipos explícitos" ou "nunca gera código sem schema Zod". Critérios vagos produzem iterações inconsistentes.
- **Avaliar com Haiku**: a avaliação de qualidade (KEEP/DISCARD) deve usar Sonnet, não Haiku — Haiku não tem julgamento qualitativo suficiente para avaliar a diferença entre versões de skill. Só a geração de modificações usa Haiku.
- **Não commitar versão refinada sem aprovação**: sempre apresentar o relatório final e aguardar aprovação explícita antes de commitar. O commit da versão refinada é o artefato final — não uma ação intermediária automática.
- **Usar sem prompts de teste reais**: prompts de teste genéricos ("faça um componente") não revelam falhas específicas da skill. Sempre coletar ou gerar 2-3 prompts que representam casos de uso reais do usuário antes de iniciar o loop.
