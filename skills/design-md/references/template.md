# Design System Inspired by <YOUR PROJECT>

> Category: <Developer Tools | Productivity & SaaS | Fintech & Crypto | Media & Consumer | Editorial & Print | Modern & Minimal | ...>
> <Resumo de uma linha para o preview — atmosfera + accent + caso de uso.>

<!--
  TEMPLATE — DESIGN.md em branco (spec canônico, 9 seções).
  Preencha cada seção. Apague os comentários <!-- ... --> ao terminar.
  Regras-chave (Lens A, blocking):
    - As 9 seções numeradas PRECISAM existir, nesta ordem.
    - Hex reais (#RRGGBB) — nada de #REPLACE_ME, currentColor ou nome de var.
    - Toda var CSS dentro de :root {}. Dark mode via [data-theme="dark"] (override, não cópia).
    - :focus-visible em todo interativo. prefers-reduced-motion segmentado (nunca *).
    - Texto/dado ≥ 4.5:1 de contraste contra o fundo PAREADO.
  Termine SEMPRE com a seção 9 (Agent Prompt Guide) — é o payload que o agente consome.
  Estudar 2-3 exemplares em references/systems/ antes de preencher. Não copie; extraia padrões.
-->

## 1. Visual Theme & Atmosphere

<!--
  A metáfora central e a sensação. O que esse produto "é" emocionalmente?
  Casos de uso. Prior art — produtos REAIS que compartilham esse DNA (não "good design").
  30-40 linhas. Termine com "Key Characteristics:" (bullets).
-->

**Key Characteristics:**
- <...>
- <...>

## 2. Color

<!--
  Paleta com hex REAIS + role de cada cor (não só "primary/secondary").
  Roles mínimos: CTA/brand, background, surface, texto 1/2/3, border, semânticos (success/warn/error).
  Verifique 4.5:1 de cada texto contra o fundo pareado.
-->

### Roles
- **<Nome> (`#______`)**: <papel — ex.: CTA primário>
- **<Nome> (`#______`)**: <background da página>
- **<Nome> (`#______`)**: <surface elevada / card>
- **<Nome> (`#______`)**: <texto primário>
- **<Nome> (`#______`)**: <texto secundário>
- **<Nome> (`#______`)**: <texto terciário / metadata>
- **<Nome> (`#______`)**: <border padrão>
- **Success (`#______`)** · **Warning (`#______`)** · **Error (`#______`)**

```css
:root {
  /* A1-identity */
  --bg: #______;
  --fg: #______;
  --accent: #______;
  --surface: #______;

  /* roles de texto */
  --fg-2: #______;   /* secundário (ou var(--fg) se não houver tier) */
  --fg-3: #______;   /* terciário/meta */

  /* border + semânticos (A2) */
  --border: #______;
  --success: #______;
  --warning: #______;
  --error: #______;
}

[data-theme="dark"] {
  --bg: #______;
  --fg: #______;
  --accent: #______;
  --surface: #______;
  --fg-2: #______;
  --fg-3: #______;
  --border: #______;
}
```

## 3. Typography

<!-- Famílias (display/body/mono). Escala com ≥4 tiers. Pesos, line-height, tracking. -->

### Font Family
- **Display / Headings**: `<Font>`, fallback `<serif|sans>`
- **Body / UI**: `<Font>`, fallback `<sans>`
- **Mono / Code**: `<Font>`, fallback `ui-monospace, monospace`

### Hierarchy

| Role | Font | Size | Weight | Line Height | Tracking |
|------|------|------|--------|-------------|----------|
| Display | <Font> | __px | ___ | ___ | ___ |
| H1 | <Font> | __px | ___ | ___ | ___ |
| Body | <Font> | __px | ___ | ___ | ___ |
| Caption | <Font> | __px | ___ | ___ | ___ |

```
Font labels for catalog extraction:

Display: "<Font>", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif
Body: "<Font>", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif
Mono: "<Font>", ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace
```

## 4. Spacing

<!-- Unidade base, escala, padding de componente, ritmo vertical de seção. -->

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --section-y-sm: 48px;
  --section-y-lg: 96px;
}
```

## 5. Layout & Composition

<!-- Grid, container max-width, filosofia de whitespace, escala de border-radius. -->

```css
:root {
  --container-max: ____px;
  --radius-sm: __px;
  --radius-md: __px;
  --radius-lg: __px;
}
```

## 6. Components

<!--
  CSS REAL de 3-6 componentes (botões, cards, inputs, nav). Tudo via tokens semânticos —
  ZERO hex hardcoded no CSS de componente. Inclua :focus-visible.
-->

```css
.button-primary {
  background: var(--accent);
  color: var(--bg);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
}
.button-primary:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}
```

## 7. Motion & Interaction

<!-- Timings, easing por propósito, prefers-reduced-motion segmentado. -->

```css
:root {
  --motion-fast: 100ms ease-in;
  --motion-base: 150ms ease-out;
  --motion-slow: 300ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .<elemento-que-anima> { animation: none; transition-duration: 0.01ms !important; }
}
```

## 8. Voice & Brand

<!-- Tom de voz, princípios de copy, prior art nomeado. -->

- **Tom**: <...>
- **Princípios de copy**: <...>
- **Prior art**: <produtos/sistemas reais — nomeie>

## 9. Anti-patterns

<!-- O que o produto NÃO é. Específico e limitado (um por erro-chave). -->

- Don't <regra específica e limitada — ex.: "use cool blue-grays; toda neutra é warm">
- Don't <...>
- Don't <...>

## 10. Agent Prompt Guide

<!--
  O PAYLOAD. Section escrita PARA o agente consumir ao gerar UI.
  (Numerada 10 só porque o spec canônico já gastou 1-9; nos exemplares brand-grade
   esta é a seção 9. O importante é que ela exista e seja a última.)
-->

### Quick Color Reference
- Brand CTA: "<Nome> (#______)"
- Page Background: "<Nome> (#______)"
- Card Surface: "<Nome> (#______)"
- Primary Text: "<Nome> (#______)"
- Secondary Text: "<Nome> (#______)"
- Borders: "<Nome> (#______)"

### Example Component Prompts
- "Create a hero on <Background (#______)> with a __px <Display Font> weight ___ headline,
  line-height ___. Body in <Secondary (#______)> at __px <Body Font>. CTA button in
  <Accent (#______)> with <Bg-color> text, __px radius."
- "Design a card on <Surface (#______)> with a 1px <Border (#______)> border, __px radius.
  Title in <Display Font> at __px, description in <Secondary (#______)> at __px."

### Iteration Guide
1. Um componente por vez.
2. Cite nomes de cor específicos — "use <Secondary> (#______)", não "deixe cinza".
3. Especifique a variante sempre (warm vs cool, serif vs sans).
4. Para sombras, nomeie o tipo do sistema (ring shadow, whisper shadow) — não "drop shadow" genérico.
5. Especifique o fundo — "on <Background (#______)>".
