# Schema do `DESIGN.md` — contrato completo

Schema canônico do contrato de design por projeto, derivado de **open-design** (nexu-io,
Apache-2.0). Um `DESIGN.md` é o **contrato de marca de um projeto**: um documento Markdown
que um agente lê para gerar UI consistente com a identidade daquele projeto — cores reais,
tipografia, espaçamento, componentes, movimento, voz e anti-padrões.

Duas perguntas governam tudo aqui:

1. **Quem decide o valor?** — o autor da marca (camada A) ou o schema (camada B-slot, quando
   a marca não tem opinião).
2. **O que acontece se a marca omitir?** — obrigatório, fallback, ou alias.

---

## 1. O contrato de parsing

O parser extrai os headings via `## [0-9].*` — ele casa o **prefixo numérico**, não o texto
completo. Você pode anexar contexto depois do número (`## 4. Spacing & Grid`,
`## 4. Spacing and layout`). Só o prefixo `## [digit].` é obrigatório. Corpos de seção vazios
são aceitos (para tokens raramente usados, ex.: motion), mas os **nove headings numerados
precisam existir, na ordem**.

### Header do arquivo

```markdown
# Design System Inspired by YourBrand

> Category: Developer Tools
> Resumo de uma linha para o preview do picker.
```

- A primeira H1 vira o label exibido. O `> Category:` logo após a H1 determina o agrupamento.
- Categorias válidas: AI & LLM, Developer Tools, Productivity & SaaS, Backend & Data,
  Design & Creative, Fintech & Crypto, E-Commerce & Retail, Media & Consumer, Automotive,
  Editorial & Print, Retro & Nostalgic, Bold & Expressive, Modern & Minimal,
  Professional & Corporate.

---

## 2. As 9 seções (spec canônico)

| # | Heading canônico | O que documenta |
| --- | --- | --- |
| 1 | `Visual Theme & Atmosphere` | A "atmosfera": metáfora central, sensação, casos de uso, prior art (produtos reais). |
| 2 | `Color` | Paleta com hex reais + **roles** (CTA, surface, texto 1/2/3, border, semânticos). Bloco `:root` + dark via `[data-theme="dark"]`. |
| 3 | `Typography` | Famílias (display/body/mono), escala (≥4 tiers), pesos, line-height, tracking. Bloco "Font labels for catalog extraction". |
| 4 | `Spacing` | Unidade base, escala de espaçamento, padding de componente, ritmo vertical de seção. |
| 5 | `Layout & Composition` | Grid, container max-width, filosofia de whitespace, escala de border-radius. |
| 6 | `Components` | CSS real de 3-6 componentes (botões, cards, inputs, nav), todo via tokens semânticos. |
| 7 | `Motion & Interaction` | Timings, easing por propósito, `:focus-visible`, `prefers-reduced-motion` segmentado. |
| 8 | `Voice & Brand` | Tom de voz, princípios de copy, prior art nomeado. |
| 9 | `Anti-patterns` | O que a marca **não é** — específico e limitado (um por erro-chave). |

### Variante brand-grade (Variante A) — a que você mais vê

Os exemplares ricos em `systems/` usam um dialeto diferente, todos válidos pelo mesmo
contrato de parsing. Cross-map canônico → Variante A:

| Spec canônico (Variante B) | Variante A (brand-grade) |
| --- | --- |
| 1. Visual Theme & Atmosphere | 1. Visual Theme & Atmosphere |
| 2. Color | 2. Color Palette & Roles |
| 3. Typography | 3. Typography Rules |
| 4. Spacing | *(absorvido em 5. Layout Principles)* |
| 5. Layout & Composition | 5. Layout Principles |
| 6. Components | 4. Component Stylings |
| 7. Motion & Interaction | 6. Depth & Elevation |
| 8. Voice & Brand | 7. Do's and Don'ts (ou 8. Accessibility & States) |
| 9. Anti-patterns | 7. Do's and Don'ts (lado "Don't") |
| — | 8. Responsive Behavior |
| — | **9. Agent Prompt Guide** (sempre a última) |

A diferença chave da Variante A: **section 9 é sempre o Agent Prompt Guide** (ver §6 abaixo),
e ela dobra "Spacing" dentro de "Layout Principles" + adiciona "Responsive Behavior" e
"Depth & Elevation" como seções de primeira classe. Para um projeto novo, escolha **uma**
variante e mantenha-a; o `template.md` usa o spec canônico (Variante B).

---

## 3. As 4 camadas de tokens

Todo token compartilhado se encaixa numa camada. Isso é o que separa "uma lista de cores" de
um **sistema de tokens**.

| Camada | Quem decide | Se omitido | Exemplos |
| --- | --- | --- | --- |
| **A1-identity** | marca | guard falha | `--bg`, `--fg`, `--accent`, `--font-display` |
| **A1-structure** | marca | guard falha | escala de tipo, `--container-max`, `--section-y-*` |
| **A2-fallback** | marca (com fallback) | guard falha hoje; script de derive preenche amanhã | `--motion-fast`, `--success`, `--space-4`, `--font-mono` |
| **B-slot** | marca ou alias sugerido pelo schema | guard falha — marca precisa declarar (como `var(--sibling)` colapsado, ou valor independente mais rico) | `--fg-2 → var(--fg)`, `--surface-warm → var(--surface)` |

Tokens fora do schema compartilhado são **C-extensions** (allowlist por marca, ex.:
`BRAND_EXTENSIONS[brand]`, ou prefixos como `--tag-bg-*`).

### A1 — identidade e estrutura (obrigatório)

Os valores que *são* a marca. Sem eles não há contrato.

```css
:root {
  /* A1-identity */
  --bg: #f5f4ed;
  --fg: #141413;
  --accent: #c96442;
  --font-display: "Anthropic Serif", Georgia, serif;

  /* A1-structure */
  --container-max: 1200px;
  --section-y-lg: 120px;
  --text-display: 4rem;   /* 64px */
  --text-h1: 3.25rem;     /* 52px */
}
```

### A2 — opcional com fallback

Conceitualmente "opcional com default", mas como artefatos são gerados colando o `:root` de
uma marca num único `<style>` (sem stylesheet global), **toda marca deve declarar todo token
A2** hoje. Um `transition: var(--motion-fast)` quebra em silêncio se `--motion-fast` faltar.

```css
:root {
  --motion-fast: 100ms ease-in;
  --motion-base: 150ms ease-out;
  --success: #26de81;
  --space-4: 16px;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
}
```

### B-slot — tier mais rico, com alias sugerido

Componentes compartilhados referenciam tiers mais ricos via `var(--fg-2)`, `var(--meta)`,
`var(--surface-warm)`, `var(--border-soft)`. O campo `aliasTo` é o **default sugerido pelo
schema** — não um fallback de runtime. Uma marca sem opinião copia o alias verbatim:

```css
:root {
  --fg-2: var(--fg);              /* default: 2-level fg colapsado */
  --surface-warm: var(--surface); /* default */
}
```

Uma marca com o tier mais rico vincula valor independente:

```css
:root {
  --fg-2: #3d3d3a;        /* kami: dark warm */
  --surface-warm: #e8e6dc;/* kami: warm sand */
}
```

### C-extensions e o caminho de promoção

```
C-extension                    B-slot                       A2
(1 marca declara)              (≥2 marcas declaram,         (toda marca declara
                                algumas alias p/ sibling)    com default sensato)
```

Regras de promoção: **C→B-slot** quando ≥2 marcas declaram o mesmo nome E existe sibling para
alias. **C→A2** quando ≥2 marcas declaram E existe fallback cross-brand defensável. **B-slot→
A2** quando ≥2 marcas vinculam independentemente. **A2→A1** é raro (o valor antes
defaultável vira determinante da marca).

### Quando *não* adicionar token

Resista a tokens que são: **component-internal** (offset de `.btn-primary` que ninguém mais
lê — inline o valor), **one-off** (crop ratio de um hero), **especulativo** ("talvez a gente
queira `--motion-slow`"), ou **já expressável** (`color-mix(...)` inline até ≥2 componentes
precisarem do mesmo tint).

---

## 4. Estrutura de CSS variables

### `:root` obrigatório

Toda variável CSS dentro de `:root {}`. Declarações soltas no topo de uma seção são
inválidas. Exceção: overrides escopados a componente (`.card { --card-padding: 16px; }`) sob
Components.

### Dark mode via `[data-theme="dark"]`

```css
:root {
  --accent: #625DF5;
  --bg: #FFFFFF;
}

[data-theme="dark"] {
  --accent: #7B75FF;
  --bg: #0D0D0D;
}
```

Nunca crie blocos light/dark separados sem o seletor `[data-theme="dark"]` — quebra o sistema
de tokens semânticos. Dark mode é **override genuíno** (valores diferentes), não cópia.

### Font labels para extração de catálogo

Inclua na seção de Typography, exatamente com os prefixos `Display:` / `Body:` / `Mono:`:

```
Font labels for catalog extraction:

Display: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif
Body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif
Mono: "JetBrains Mono", ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace
```

---

## 5. Acessibilidade (Lens A — blocking)

### Contraste WCAG AA

Todo texto/dado precisa passar **4.5:1 mínimo** contra o seu fundo (4.5:1 texto normal,
3:1 texto grande 18px+ ou 14px+ bold). Teste cada foreground contra o **fundo pareado** — não
contra branco por default.

Erro comum: texto terciário em surface escura. `#4A6080` sobre `#0A0A0A` = 2.1:1 (FALHA). Use
`#808086` sobre `#0A0A0A` = 4.54:1.

### Focus states

Todo componente interativo (botões, links, inputs, cards clicáveis) precisa de
`:focus-visible`:

```css
.button-primary:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

### `prefers-reduced-motion` segmentado

Mire propriedades/elementos específicos, nunca o seletor global `*`:

```css
/* Correto */
@media (prefers-reduced-motion: reduce) {
  .alert-banner { animation-duration: 0.01ms !important; }
  .countdown { animation: none; }
}

/* Errado — mata transições do site inteiro */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}
```

---

## 6. A seção "Agent Prompt Guide" (o payload)

Nos exemplares brand-grade, a **seção 9 é feita PARA o agente consumir** ao gerar UI. Tem três
partes:

1. **Quick Color Reference** — mapeia cada role ao seu nome + hex, no formato que o agente
   cita: `Brand CTA: "Terracotta Brand (#c96442)"`.
2. **Example Component Prompts** — prompts prontos para colar, cada um citando hex + fonte +
   raio exatos: *"Create a hero on Parchment (#f5f4ed) with a 64px Anthropic Serif weight 500
   headline, line-height 1.10..."*.
3. **Iteration Guide** — receita: um componente por vez, citar nomes de cor específicos,
   sempre especificar a variante (warm/cool), descrever serif vs sans explicitamente.

Por que importa: a diferença entre um `DESIGN.md` que *descreve* uma marca e um que um agente
*consegue construir* é essa seção. Sem ela, o agente improvisa valores. Um `DESIGN.md` de
projeto novo deve terminar com um Agent Prompt Guide próprio.

---

## 7. Tamanho e qualidade

Um `DESIGN.md` bem documentado tem tipicamente **300-600 linhas**. Abaixo de ~100 linhas
dispara revisão de substância (Lens B). Verbosidade genérica não ajuda.

| Área | Linhas-alvo |
| --- | --- |
| Color | 30-50 (tabelas de paleta + blocos CSS) |
| Components | 100-200 (3-6 componentes, totalmente especificados) |
| Visual Theme | 30-40 (atmosfera + casos de uso + prior art) |
| Anti-patterns | 8-15 (um por erro-chave) |
