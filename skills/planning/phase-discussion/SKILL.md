---
name: phase-discussion
description: >
  Captura decisões de implementação de uma fase ANTES do planejamento técnico,
  eliminando zonas cinzentas que causam retrabalho. ACIONE antes de planejar
  qualquer fase com UI, API, sistema de conteúdo ou reorganização de dados.
  Use com "discutir fase", "discuss phase", "decisões da fase", "contexto da fase",
  "antes de planejar", "o que decidir antes", "fase N". Produz CONTEXT.md que
  alimenta o spec-builder, arch-builder e story-executor.
trigger: discutir fase|discuss phase|decisões da fase|contexto da fase|antes de planejar|fase \d
model-tier: sonnet
---

# Phase Discussion

## Papel

Facilitador que extrai as preferências do usuário antes que qualquer código
seja planejado ou escrito. O roadmap tem frases. Frases não são suficientes
para construir o que o usuário imagina. Esta skill preenche esse gap.

Inspirado no padrão `discuss-phase` do GSD (get-shit-done).

---

## Quando usar

- Antes de `spec-builder`, `arch-builder` ou `story-executor` para qualquer fase
- Quando a fase envolve decisões de UX, estrutura de API, ou organização de dados
- Quando o usuário diz "quero que fique assim" sem detalhar como
- Antes de qualquer fase com interface visual

---

## Processo

### 1. Identificar a fase

Ler a descrição da fase no roadmap/épico. Se não existir um artefato formal,
pedir ao usuário: "Me descreva em 2-3 frases o que essa fase entrega."

### 2. Identificar zonas cinzentas por tipo de fase

Analisar a fase e identificar quais categorias se aplicam:

**Fases com features visuais (UI/UX)**
- Layout e densidade: lista, grid, card, tabela, misto?
- Interações: hover, drag-drop, inline edit, modal, slide-over?
- Estados vazios: placeholder, skeleton, call-to-action?
- Mobile: responsivo ou desktop-first por ora?
- Navegação: breadcrumb, tabs, sidebar, steps?

**Fases com APIs ou CLIs**
- Formato de resposta: JSON flat, nested, enveloped?
- Tratamento de erros: codes, mensagens, stack trace exposto?
- Paginação: cursor, offset, sem paginação?
- Autenticação: JWT, API key, sessão, pública?
- Versionamento: `/v1/`, header, sem versão?

**Fases com sistemas de conteúdo**
- Estrutura: hierárquica, flat, tags, categorias?
- Tom: formal, conversacional, técnico?
- Profundidade: resumido, detalhado, expansível?
- Fluxo: linear, não-linear, ramificado?

**Fases com organização/migração de dados**
- Critério de agrupamento: por data, categoria, usuário, status?
- Tratamento de duplicatas: merge, manter ambos, marcar?
- Exceções: como lidar com registros que não se encaixam?
- Rollback: reversível ou one-way?

### 3. Conduzir a discussão

Para cada zona cinzenta identificada:
1. Apresentar as opções concretas (não abstratas)
2. Indicar qual seria o padrão razoável e por quê
3. Perguntar a preferência do usuário
4. Registrar a decisão

**Modo compacto (`--batch`):** agrupar até 3 perguntas relacionadas numa só
resposta esperada, para usuários que preferem responder em bloco.

Continuar até que todas as zonas cinzentas relevantes estejam resolvidas
ou o usuário explicitamente disser "suficiente, prosseguir".

### 4. Gerar CONTEXT.md

```markdown
---
type: osforge-phase-context
phase: "{N} — {título da fase}"
created_at: {data}
feeds: [spec-builder, arch-builder, story-executor]
---

# Phase {N} Context: {título}

## Decisões Tomadas

### Visual / UX
- **Layout:** {decisão} — Razão: {justificativa do usuário}
- **Interações:** {decisão}
- **Mobile:** {decisão}

### API / Backend
- **Formato de resposta:** {decisão}
- **Paginação:** {decisão}
- **Autenticação:** {decisão}

### Dados
- **Agrupamento:** {decisão}
- **Duplicatas:** {decisão}

## Decisões Adiadas (v2+)
- {item que o usuário explicitamente colocou fora do escopo}

## Restrições Identificadas
- {qualquer constraint técnica ou de negócio mencionada}

## Notas Livres
{observações que não cabem nas categorias acima}
```

Salvar em `.osforge/phases/{N}-CONTEXT.md`.

---

## Integração com outros skills

O `CONTEXT.md` gerado deve ser carregado explicitamente pelos skills seguintes:

- **`spec-builder`** → lê CONTEXT.md para gerar ACs alinhados às decisões
- **`arch-builder`** → lê CONTEXT.md para tomar decisões de arquitetura informadas
- **`story-executor`** → lê CONTEXT.md para implementar o que o usuário imaginou

Sempre mencionar no handoff: "Carregar `.osforge/phases/{N}-CONTEXT.md`
antes de planejar esta fase."

---

## Regras

- Nunca assumir uma decisão — sempre perguntar quando há ambiguidade
- Não entrar em detalhes de implementação nesta etapa (isso é para o arch-builder)
- Manter foco nas PREFERÊNCIAS do usuário, não nas soluções técnicas
- Se o usuário disser "qualquer coisa serve" → registrar o padrão razoável como decisão
- Máximo de 15 minutos de discussão — se estiver passando disso, agrupar as perguntas restantes
