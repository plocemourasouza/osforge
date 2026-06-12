---
name: design-md
description: >
  Contrato de identidade de marca POR PROJETO em um arquivo DESIGN.md — o
  documento de 9 seções (Visual Theme, Color, Typography, Spacing, Layout,
  Components, Motion, Voice & Brand, Anti-patterns) com tokens hex reais que um
  agente lê para gerar UI consistente com a identidade daquele projeto.
  ACIONE quando: usuário pede "criar identidade de marca por projeto", "DESIGN.md",
  "design tokens de projeto", "contrato de design", "design system do projeto",
  "tokens de marca", "padronizar o visual deste projeto", "como esse produto deve
  parecer", ou está iniciando um projeto novo que precisa de identidade própria.
  Produz/revisa um DESIGN.md versionável no repo do projeto. Difere de
  aesthetic-modes (3 moods prontos), ui-design-intelligence (spec por indústria) e
  stitch-design-export (export p/ Google Stitch): aqui o entregável é o CONTRATO
  DESIGN.md em si, com schema validável (Lens A/B) e Agent Prompt Guide.
version: 1.0.0
metadata:
  source: "open-design (github.com/nexu-io/open-design), Apache-2.0"
  curated_systems: 15
allowed-tools: Read, Write, Edit, Glob, Grep
---

# design-md — Contrato de marca por projeto

Um `DESIGN.md` é o **contrato de identidade de um projeto**: um único arquivo Markdown,
versionado no repo, que descreve cores reais, tipografia, espaçamento, componentes, movimento,
voz e anti-padrões — e termina com um **Agent Prompt Guide** que um agente de geração de UI
consome diretamente. É o artefato que falta entre "tenho um mood visual" e "todo componente
gerado sai consistente com a marca".

## Quando usar (e quando não)

**Use quando** o projeto precisa de identidade própria, durável, citável por hex — um produto
real começando do zero, ou um existente sem contrato de marca. O entregável é o
`DESIGN.md` no repo do projeto.

**Não use para:**
- Um mood pronto entre 3 paradigmas (minimalist/brutalist/soft) → `aesthetic-modes`.
- Spec de design adaptado a uma indústria (fintech/healthcare/saas) → `ui-design-intelligence`.
- Exportar um design system para Google Stitch → `stitch-design-export` / `stitch-design-taste`.
- Decisões de design pontuais (escolher uma paleta, um font) → `frontend-design`.
- Estilos de aesthetic genérico (glassmorphism, bento, neobrutalism) já cobertos em
  `aesthetic-modes` — **não** crie um DESIGN.md só para reproduzir um estilo de catálogo.

`design-md` é o nível acima: produz o **contrato**, não um one-off. Os outros skills informam
o *conteúdo* das seções; este define a *forma* e a valida.

## As 9 seções (o schema)

Todo `DESIGN.md` tem estes nove headings, nesta ordem. O parser casa só o prefixo `## [digit].`
— texto após o número é livre (`## 4. Spacing & Grid` é válido).

| # | Seção | O que documenta |
| --- | --- | --- |
| 1 | **Visual Theme & Atmosphere** | Metáfora central, sensação, casos de uso, prior art (produtos reais). |
| 2 | **Color** | Hex reais + **role** de cada cor (CTA, surface, texto 1/2/3, border, semânticos). |
| 3 | **Typography** | Famílias display/body/mono, escala ≥4 tiers, pesos, line-height, tracking + bloco "Font labels". |
| 4 | **Spacing** | Unidade base, escala, padding de componente, ritmo vertical de seção. |
| 5 | **Layout & Composition** | Grid, container max-width, whitespace, escala de border-radius. |
| 6 | **Components** | CSS real de 3-6 componentes, 100% via tokens semânticos. |
| 7 | **Motion & Interaction** | Timings, easing por propósito, `:focus-visible`, `prefers-reduced-motion`. |
| 8 | **Voice & Brand** | Tom de voz, princípios de copy, prior art nomeado. |
| 9 | **Anti-patterns** | O que a marca **não** é — específico e limitado. |

Detalhe completo seção a seção + as 4 camadas de tokens (A1-identity, A1-structure,
A2-fallback, B-slot, C-extensions) em **`references/schema.md`**.

### Duas variantes reais de heading

Os exemplares brand-grade em `references/systems/` usam um dialeto diferente, igualmente
válido pelo contrato de parsing:

- **Variante A (a maioria):** Visual Theme · Color Palette & Roles · Typography Rules ·
  Component Stylings · Layout Principles · Depth & Elevation · Do's and Don'ts · Responsive
  Behavior · **Agent Prompt Guide**.
- **Variante B (spec canônico — `atelier-zero`):** as 9 da tabela acima.

Escolha **uma** por projeto e mantenha. O `references/template.md` usa a Variante B (mapeia
1:1 nas camadas de tokens). Cross-map A↔B em `references/schema.md §2`.

## O padrão "Agent Prompt Guide" (a seção feita PARA o agente)

A última seção dos exemplares é escrita **para um agente consumir** na geração de UI — não é
documentação para humano. Três partes:

1. **Quick Color Reference** — cada role → nome + hex, no formato que o agente cita:
   `Brand CTA: "Terracotta Brand (#c96442)"`.
2. **Example Component Prompts** — prompts prontos para colar, citando hex/fonte/raio exatos.
3. **Iteration Guide** — receita (um componente por vez, citar nomes de cor específicos,
   nomear o tipo de sombra do sistema, especificar o fundo).

**Esta seção é o que diferencia** um DESIGN.md que *descreve* uma marca de um que um agente
*consegue construir*. Sem ela o agente improvisa valores. Todo DESIGN.md novo termina com um
Agent Prompt Guide próprio.

## Checklist de review

### Lens A — correção de código (BLOQUEANTE)

Falhar qualquer item invalida o arquivo:

- [ ] As **9 seções numeradas presentes, na ordem**.
- [ ] Cores são **hex reais** (`#RRGGBB`/`#RGB`) — nada de `#REPLACE_ME`, `currentColor`,
      ou nome de CSS var no lugar do valor.
- [ ] Toda var CSS dentro de **`:root {}`** (exceto override escopado a componente).
- [ ] **Dark mode via `[data-theme="dark"]`** como override (valores diferentes), não bloco
      duplicado.
- [ ] **`:focus-visible`** em todo interativo (botão, link, input, card clicável).
- [ ] **`prefers-reduced-motion`** mira elementos específicos, nunca o seletor global `*`.
- [ ] Bloco **"Font labels for catalog extraction"** presente (prefixos `Display:`/`Body:`/`Mono:`).
- [ ] **Contraste WCAG AA 4.5:1** de cada texto/dado contra o fundo **pareado** (não contra
      branco por default; 3:1 só para texto grande 18px+/14px+ bold).
- [ ] Componentes usam **tokens semânticos**, zero hex hardcoded no CSS de componente.

### Lens B — substância (P3, não bloqueante mas exigido para "brand-grade")

- [ ] Paleta lista **todos os roles** usados, não só primary/secondary.
- [ ] Escala de tipo tem **≥4 tiers** (Display, H1, Body, Caption).
- [ ] Components tem **CSS real**, sem Lorem Ipsum ou `/* TODO */`.
- [ ] Anti-patterns **específicos e limitados** ("no rounded corners > 4px"), não "avoid bad
      design".
- [ ] Dark mode é **override genuíno**, não cópia do bloco light.
- [ ] Prior art nomeia **produtos/sistemas reais**, não "inspired by good design".
- [ ] Tamanho razoável: **300-600 linhas** (abaixo de ~100 dispara revisão de substância).

## Workflow

1. **Estude exemplares.** Abra 2-3 em `references/systems/` por proximidade de categoria/mood
   (ex.: produto editorial → `claude`, `kami`, `notion`; dev tool → `vercel`, `linear-app`,
   `raycast`; consumer → `apple`, `airbnb`, `tesla`). Extraia **padrões** (disciplina de
   neutras warm, depth por ring-shadow, serif de peso único), não valores.
2. **Decida a identidade** do projeto: metáfora central, accent, atmosfera, prior art.
3. **Preencha o `references/template.md`** → `DESIGN.md` no repo do projeto. Hex reais desde o
   início. Uma variante de heading, consistente.
4. **Termine com o Agent Prompt Guide** próprio do projeto.
5. **Rode o review** Lens A (bloqueante) → Lens B (substância).
6. **Versione** o `DESIGN.md` no repo. É o contrato; daqui pra frente toda geração de UI cita
   os roles/hex dele.

## Arquivos de referência

- **`references/schema.md`** — schema completo seção a seção + as 4 camadas de tokens
  (A1/A2/B-slot/C) + caminho de promoção C→B→A2→A1 + regras de acessibilidade.
- **`references/template.md`** — `DESIGN.md` em branco, 9 seções comentadas, pronto para
  preencher.
- **`references/systems/`** — 15 exemplares brand-grade curados (claude, linear-app, stripe,
  apple, vercel, notion, figma, raycast, supabase, airbnb, tesla, theverge, wired,
  atelier-zero, kami). Fonte: open-design (nexu-io, Apache-2.0). Ver
  `references/systems/README.md` para índice + licença.
