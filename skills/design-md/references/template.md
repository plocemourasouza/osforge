# Design System Inspired by <YOUR PROJECT>

> Category: <Developer Tools | Productivity & SaaS | Fintech & Crypto | Media & Consumer | Editorial & Print | Modern & Minimal | ...>
> <One-line summary for the preview — atmosphere + accent + use case.>

<!--
  TEMPLATE — blank DESIGN.md (canonical spec, 9 sections).
  Fill in each section. Delete the <!-- ... --> comments when done.
  Key rules (Lens A, blocking):
    - The 9 numbered sections MUST exist, in this order.
    - Real hex (#RRGGBB) — no #REPLACE_ME, currentColor, or var name.
    - Every CSS var inside :root {}. Dark mode via [data-theme="dark"] (override, not copy).
    - :focus-visible on every interactive element. prefers-reduced-motion targeted (never *).
    - Text/data ≥ 4.5:1 contrast against the PAIRED background.
  ALWAYS end with section 9 (Agent Prompt Guide) — it is the payload the agent consumes.
  Study 2-3 exemplars in references/systems/ before filling in. Don't copy; extract patterns.
-->

## 1. Visual Theme & Atmosphere

<!--
  The central metaphor and the feeling. What is this product "like" emotionally?
  Use cases. Prior art — REAL products that share this DNA (not "good design").
  30-40 lines. End with "Key Characteristics:" (bullets).
-->

**Key Characteristics:**
- <...>
- <...>

## 2. Color

<!--
  Palette with REAL hex + role of each color (not just "primary/secondary").
  Minimum roles: CTA/brand, background, surface, text 1/2/3, border, semantics (success/warn/error).
  Verify 4.5:1 of each text against the paired background.
-->

### Roles
- **<Name> (`#______`)**: <role — e.g.: primary CTA>
- **<Name> (`#______`)**: <page background>
- **<Name> (`#______`)**: <elevated surface / card>
- **<Name> (`#______`)**: <primary text>
- **<Name> (`#______`)**: <secondary text>
- **<Name> (`#______`)**: <tertiary text / metadata>
- **<Name> (`#______`)**: <default border>
- **Success (`#______`)** · **Warning (`#______`)** · **Error (`#______`)**

```css
:root {
  /* A1-identity */
  --bg: #______;
  --fg: #______;
  --accent: #______;
  --surface: #______;

  /* text roles */
  --fg-2: #______;   /* secondary (or var(--fg) if there is no tier) */
  --fg-3: #______;   /* tertiary/meta */

  /* border + semantics (A2) */
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

<!-- Families (display/body/mono). Scale with ≥4 tiers. Weights, line-height, tracking. -->

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

<!-- Base unit, scale, component padding, section vertical rhythm. -->

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

<!-- Grid, container max-width, whitespace philosophy, border-radius scale. -->

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
  REAL CSS for 3-6 components (buttons, cards, inputs, nav). Everything via semantic tokens —
  ZERO hardcoded hex in component CSS. Include :focus-visible.
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

<!-- Timings, easing by purpose, prefers-reduced-motion targeted. -->

```css
:root {
  --motion-fast: 100ms ease-in;
  --motion-base: 150ms ease-out;
  --motion-slow: 300ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .<animating-element> { animation: none; transition-duration: 0.01ms !important; }
}
```

## 8. Voice & Brand

<!-- Tone of voice, copy principles, named prior art. -->

- **Tone**: <...>
- **Copy principles**: <...>
- **Prior art**: <real products/systems — name them>

## 9. Anti-patterns

<!-- What the product is NOT. Specific and bounded (one per key mistake). -->

- Don't <specific and bounded rule — e.g.: "use cool blue-grays; every neutral is warm">
- Don't <...>
- Don't <...>

## 10. Agent Prompt Guide

<!--
  THE PAYLOAD. Section written FOR the agent to consume when generating UI.
  (Numbered 10 only because the canonical spec already used 1-9; in brand-grade exemplars
   this is section 9. What matters is that it exists and is the last one.)
-->

### Quick Color Reference
- Brand CTA: "<Name> (#______)"
- Page Background: "<Name> (#______)"
- Card Surface: "<Name> (#______)"
- Primary Text: "<Name> (#______)"
- Secondary Text: "<Name> (#______)"
- Borders: "<Name> (#______)"

### Example Component Prompts
- "Create a hero on <Background (#______)> with a __px <Display Font> weight ___ headline,
  line-height ___. Body in <Secondary (#______)> at __px <Body Font>. CTA button in
  <Accent (#______)> with <Bg-color> text, __px radius."
- "Design a card on <Surface (#______)> with a 1px <Border (#______)> border, __px radius.
  Title in <Display Font> at __px, description in <Secondary (#______)> at __px."

### Iteration Guide
1. One component at a time.
2. Cite specific color names — "use <Secondary> (#______)", not "make it gray".
3. Always specify the variant (warm vs cool, serif vs sans).
4. For shadows, name the system type (ring shadow, whisper shadow) — not a generic "drop shadow".
5. Specify the background — "on <Background (#______)>".
