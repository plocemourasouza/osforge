---
name: visual-planner
description: "Transforma documentos de planejamento em breakdowns HTML visuais e interativos. ACIONE quando: visualizar um plano, transformar spec em HTML, criar breakdown visual, apresentar PRD visualmente, gerar HTML interativo de arquitetura, tornar spec mais fácil de seguir. Keywords: visualizar plano, breakdown visual, HTML interativo, visualizar spec, visualizar PRD, apresentar arquitetura, visual breakdown, plan breakdown, turn spec into HTML, make plan visual, make this easier to follow."
model: sonnet
allowed-tools: Read, Write, Glob, Grep, Bash
metadata:
  version: '1.0'
  source: 'ethanplusai/visualplanner (adapted)'
  category: planning
  position: presentation-layer
---

## Contexto do projeto
!`[ -f project-context.md ] && head -30 project-context.md || echo "project-context.md não encontrado"`
!`ls docs/specs/ 2>/dev/null | head -5 && echo "Specs encontradas" || echo "Nenhuma spec em docs/specs/"`
!`ls .osforge/phases/ 2>/dev/null | head -5 && echo "Phases encontrados" || echo "Nenhum phase context"`

# Visual Planner

Transforma qualquer documento de planejamento em um breakdown HTML single-page, interativo e visualmente rico. O output é um arquivo HTML autocontido com navegação scroll-based, animações reveal, flow diagrams, seções expansíveis, e design system warm. Zero dependências além de Google Fonts.

**Invocação mínima:**
```
visual-planner docs/specs/auth-spec.md
```
ou em linguagem natural: "visualizar ./docs/specs/auth-spec.md".

## Integração com Pipeline OSForge

Esta skill é a **camada de apresentação** do pipeline de planejamento. Reconhece automaticamente os formatos de output das planning skills:

| Formato OSForge | Tipo de documento | Estrutura visual sugerida |
|---|---|---|
| `osforge-prd` | Product Requirements Document | Feature walkthrough com pattern cards |
| `osforge-spec` | Tech Spec com ACs | Phase-based com step cards e callout boxes |
| `osforge-architecture` | ADR / Architecture Doc | Architecture-first com arch diagrams |
| `osforge-epic` | Épicos decompostos | Flow diagram de stories + dependency map |
| `osforge-phase-context` | Decisões de fase | Cards por dimensão (Visual, API, Data, Security) |
| `osforge-clarifications` | Clarificações resolvidas | Comparison tables + callout boxes |
| Markdown genérico | Qualquer doc de planejamento | Auto-detect pelo conteúdo |

## Boas-vindas (primeira invocação)

Quando a skill é acionada sem documento especificado:

> **Posso transformar qualquer documento de planejamento em um breakdown visual interativo.**
>
> Me aponte um arquivo:
> - **Arquivo local** — ex: "visualizar ./docs/specs/auth-spec.md"
> - **Doc atual** — se já está olhando uma spec, diga "visualizar este plano"
> - **Output de planning skill** — specs, PRDs, épicos gerados pelo OSForge
>
> Vou ler o documento, escolher a melhor estrutura visual, e gerar um HTML que você pode abrir no browser, compartilhar, ou gravar a tela. Funciona em qualquer browser — sem setup.

## O Processo

### Fase 1: Analisar o Documento

Leia o documento inteiro. Extraia:

1. **Nome do projeto e descrição de uma linha** — para a hero section
2. **Tipo de documento** — determine a melhor estrutura visual:
   - **Phase-based** — fases de implementação sequenciais → seções numeradas
   - **Architecture-first** — design de sistema com componentes → diagrama de arquitetura primeiro, depois detalhes
   - **Feature walkthrough** — organizado por features voltadas ao usuário → seções feature por feature
   - **Narrative** — traça jornada do usuário ou fluxo de dados → seções em arco narrativo
   - **Mixed** — combinação → escolha o padrão dominante, entrelace os outros
3. **Seções principais** — viram as seções scrolláveis (mire em 4-8)
4. **Relacionamentos** — como as partes se conectam (viram flow diagrams)
5. **Detalhes técnicos** — snippets de código, estruturas de arquivo, specs de API (vão em expandable cards e code blocks)
6. **Decisões e restrições chave** — (viram callout boxes)
7. **Números e métricas** — contagens de arquivos, endpoints, itens de stack (viram stat badges)
8. **Tech stack** — linguagens, frameworks, serviços mencionados

### Fase 2: Construir o HTML

Gere um único arquivo HTML. Leia `references/design-system.md` para os tokens CSS completos. Leia `references/interactive-elements.md` para os padrões de implementação.

**Ordem de build:**

1. **Foundation primeiro** — Shell HTML com todas as seções (vazias), CSS design system completo dos references, navigation bar com progress tracking, keyboard navigation, e animações scroll-triggered. Após este passo: um skeleton funcional navegável.

2. **Hero section** — Nome do projeto, descrição de uma linha, stats chave (como badges), e overview visual do que o plano cobre.

3. **Uma seção por vez** — Preencha conteúdo e elementos visuais de cada seção. Não tente escrever todas de uma vez. Construa Seção 1, depois Seção 2, etc.

4. **Polish pass** — Após todas as seções, passe final de consistência visual.

**Nome do arquivo de output:** `{project-name}-breakdown.html` (slugificado do título do documento)

### Fase 3: Abrir e Apresentar

Após gerar o HTML, abra no browser para o usuário revisar.

---

## Filosofia de Conteúdo

### Visual First — Agressivamente

O ponto é que isso é mais fácil de seguir que o documento bruto. Siga estas regras:

**Limites de texto:**
- Max **2-3 frases** por bloco de texto. Se está escrevendo a quarta frase, pare e converta em elemento visual.
- Cada seção deve ser **pelo menos 50% visual** — flow diagrams, cards, code blocks, badges, step cards.

**Converter texto em visuais:**
- Lista de 3+ itens → **pattern cards** com ícones
- Sequência de passos → **step cards** ou **flow diagram com setas**
- "Componente A conecta ao Componente B" → **flow diagram**
- Descrições de arquitetura → **layouts box-and-arrow** com zonas color-coded
- Estruturas de arquivo/diretório → **visual file tree**
- Detalhes técnicos que sobrecarregam → **expandable detail cards** (resumo visível, detalhes no clique)
- Números chave → **stat badges**
- Comparações → **colunas side-by-side**

### Fiel ao Fonte

- Use a linguagem e termos do documento original — não reescreva ou reinterprete
- Preserve precisão técnica — simplifique a **apresentação**, não o **conteúdo**
- Não adicione informação que não está no documento fonte
- Não pule seções porque são técnicas — use expandable cards para detalhes densos

### "O Quê" Antes do "Como"

Cada seção deve abrir com o que essa parte do plano faz ou alcança, depois ir nos detalhes. O leitor deve poder scrollar rápido e pegar a essência, ou desacelerar e expandir cards para profundidade.

### Resumos em Linguagem Simples

Para cada seção principal, escreva um resumo de 1-2 frases que capture a essência. Isso aparece como subtítulo da seção. O conteúdo técnico original vai no corpo e expandable cards abaixo.

---

## Estrutura de Seção

Cada bloco principal do documento de planejamento vira uma seção:

```
Seção N
├── Número da seção (grande, cor accent)
├── Título da seção (heading bold)
├── Subtítulo da seção (resumo de 1 linha)
├── Corpo
│   ├── Elemento visual (flow diagram, cards, file tree, etc.)
│   ├── Texto breve (2-3 frases max por bloco)
│   ├── Expandable detail cards (para conteúdo mais profundo)
│   ├── Code blocks (se existem snippets técnicos)
│   └── Callout boxes (para decisões/restrições chave)
└── Review toolbar (thumbs up, thumbs down, botão de comentário)
```

**Mire em 4-8 seções totais.** Se o documento tem mais headings, agrupe os relacionados. Se tem menos, divida seções grandes em subpartes lógicas.

---

## Elementos Obrigatórios

Todo breakdown deve incluir:

1. **Hero section** — Nome do projeto, descrição, stat badges chave
2. **Pelo menos um flow diagram** — mostrando como partes principais se conectam
3. **Pelo menos um set de pattern/feature cards** — para listar componentes, features, ou tech stack
4. **Expandable detail cards** — para qualquer seção com conteúdo técnico denso
5. **Callout boxes** — para decisões chave, restrições, ou trade-offs do plano
6. **Progress bar e dot navigation** — sempre presentes
7. **Review system em cada seção** — thumbs up/down + comentário + botão Copy Review

---

## Sistema de Review

Cada seção inclui uma toolbar de review para feedback sobre o plano. Isto é OBRIGATÓRIO — inclua em todo HTML gerado.

**Toolbar por seção:**
- Botão thumbs up (verde quando ativo)
- Botão thumbs down (vermelho quando ativo)
- Botão de comentário (abre textarea inline, fica azul quando tem comentário)
- Clicar na mesma reação novamente deseleciona (toggle)

**Botão flutuante "Copy Review":**
- Fixo no canto inferior direito, formato pill escuro
- Só visível após o usuário deixar pelo menos uma reação ou comentário
- Mostra badge com contagem de seções com feedback
- No clique: coleta todas reações + comentários, formata como markdown, copia para clipboard
- Mostra toast: "Review copiada — cole no Claude"

**Persistência localStorage:**
- Todo estado de review salva em localStorage com chave baseada no título da página
- Usuário pode fechar e reabrir a página e o feedback persiste
- Reações e comentários restauram no carregamento

**Formato de output do clipboard:**
```
# Plan Review: {Nome do Projeto}

## {Título da Seção}
- **Reação:** 👍 ou 👎
- **Comentário:** "nota do usuário aqui"

## {Título da Seção}
- **Reação:** 👎
- **Comentário:** "nota do usuário aqui"
```

Este formato é projetado para o usuário colar direto no Claude, que lê o feedback seção por seção e itera no plano.

Veja `references/interactive-elements.md` → seção Review System para implementação completa de HTML, CSS e JS.

---

## Regras de Implementação

- O arquivo deve ser completamente autocontido (única dependência externa: Google Fonts CDN)
- NÃO use scroll-snap — seções podem ser longas e snap dificulta alcançar review toolbars
- Use `min-height: 100dvh` com fallback `100vh` para seções
- Apenas anime `transform` e `opacity` para performance GPU
- Envolva todo JS em IIFE, use `passive: true` em scroll listeners, throttle com `requestAnimationFrame`
- Inclua keyboard navigation (arrow keys para mover entre seções)
- Inclua atributos ARIA para acessibilidade
- Backgrounds alternantes (`--color-bg` e `--color-bg-warm`) para ritmo visual
- Todos code blocks usam `white-space: pre-wrap` — sem scrollbars horizontais

---

## Seleção de Accent Color

Escolha uma accent color que combine com a personalidade do projeto:
- **Vermillion** (`#D94F30`) — default, funciona para maioria dos projetos
- **Teal** (`#2A7B9B`) — para planos heavy em data/infraestrutura/backend
- **Coral** (`#E06B56`) — para projetos consumer/social/criativos
- **Forest** (`#2D8B55`) — para developer tools, CLIs, open source
- **Amber** (`#D4A843`) — para fintech, analytics, dashboards

Evite gradientes roxos — parecem qualquer outro produto de AI.

---

## Gotchas

### Muros de Texto
Modo de falha #1. Se vir mais de 3 frases seguidas sem break visual, pare e converta algo em card, diagrama, ou seção expansível.

### Poucas Seções
Se tudo está comprimido em 2-3 seções enormes, a navegação scroll-based perde sentido. Quebre o plano em 4-8 pedaços digestíveis.

### Expandable Cards Não Usados
Conteúdo técnico denso (specs de API, estruturas de arquivo, requisitos detalhados) deve estar em expandable cards, não despejado no fluxo principal. O fluxo principal fica escaneável; detalhes estão a um clique.

### Scroll-Snap
Não use scroll-snap — seções podem ser longas e snap dificulta alcançar review toolbars.

### Flow Diagrams Faltando
Todo plano tem relações entre partes. Se não incluiu pelo menos um flow diagram, está faltando o elemento visual mais valioso.

---

## Quando usar visual-planner vs osforge-canvas

Para loops de revisão e aprovação interativos (feedback estruturado, formulários,
decisões por seção, round-trip Claude ↔ browser), prefira a skill `osforge-canvas`.
O visual-planner permanece a escolha certa para documentos HTML one-shot apresentáveis
sem coleta de feedback.

## Arquivos de Referência

Leia estes ANTES de escrever qualquer HTML:

- **`references/design-system.md`** — CSS custom properties completas, paleta de cores, escala tipográfica, spacing, shadows, animações, navegação, estrutura de módulos, breakpoints responsivos.
- **`references/interactive-elements.md`** — Padrões HTML/CSS/JS para: expandable cards, flow diagrams, step cards, callout boxes, code blocks, stat badges, pattern cards, file trees, icon rows, architecture diagrams, comparison tables, review system.
