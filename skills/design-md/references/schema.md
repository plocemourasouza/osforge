# `DESIGN.md` schema — complete contract

Canonical schema of the per-project design contract, derived from **open-design** (nexu-io,
Apache-2.0). A `DESIGN.md` is a **project's brand contract**: a Markdown document
that an agent reads to generate UI consistent with that project's identity — real colors,
typography, spacing, components, motion, voice, and anti-patterns.

Two questions govern everything here:

1. **Who decides the value?** — the brand author (layer A) or the schema (B-slot layer, when
   the brand has no opinion).
2. **What happens if the brand omits it?** — required, fallback, or alias.

---

## 1. The parsing contract

The parser extracts headings via `## [0-9].*` — it matches the **numeric prefix**, not the full
text. You can append context after the number (`## 4. Spacing & Grid`,
`## 4. Spacing and layout`). Only the `## [digit].` prefix is required. Empty section bodies
are accepted (for rarely used tokens, e.g. motion), but the **nine numbered headings
must exist, in order**.

### File header

```markdown
# Design System Inspired by YourBrand

> Category: Developer Tools
> One-line summary for the picker preview.
```

- The first H1 becomes the displayed label. The `> Category:` right after the H1 determines the grouping.
- Valid categories: AI & LLM, Developer Tools, Productivity & SaaS, Backend & Data,
  Design & Creative, Fintech & Crypto, E-Commerce & Retail, Media & Consumer, Automotive,
  Editorial & Print, Retro & Nostalgic, Bold & Expressive, Modern & Minimal,
  Professional & Corporate.

---

## 2. The 9 sections (canonical spec)

| # | Canonical heading | What it documents |
| --- | --- | --- |
| 1 | `Visual Theme & Atmosphere` | The "atmosphere": central metaphor, feel, use cases, prior art (real products). |
| 2 | `Color` | Palette with real hex + **roles** (CTA, surface, text 1/2/3, border, semantics). `:root` block + dark via `[data-theme="dark"]`. |
| 3 | `Typography` | Families (display/body/mono), scale (≥4 tiers), weights, line-height, tracking. "Font labels for catalog extraction" block. |
| 4 | `Spacing` | Base unit, spacing scale, component padding, vertical section rhythm. |
| 5 | `Layout & Composition` | Grid, container max-width, whitespace philosophy, border-radius scale. |
| 6 | `Components` | Real CSS for 3-6 components (buttons, cards, inputs, nav), all via semantic tokens. |
| 7 | `Motion & Interaction` | Timings, easing by purpose, `:focus-visible`, targeted `prefers-reduced-motion`. |
| 8 | `Voice & Brand` | Tone of voice, copy principles, named prior art. |
| 9 | `Anti-patterns` | What the brand **is not** — specific and limited (one per key mistake). |

### Brand-grade variant (Variant A) — the one you see most

The rich exemplars in `systems/` use a different dialect, all valid under the same
parsing contract. Canonical → Variant A cross-map:

| Canonical spec (Variant B) | Variant A (brand-grade) |
| --- | --- |
| 1. Visual Theme & Atmosphere | 1. Visual Theme & Atmosphere |
| 2. Color | 2. Color Palette & Roles |
| 3. Typography | 3. Typography Rules |
| 4. Spacing | *(absorbed into 5. Layout Principles)* |
| 5. Layout & Composition | 5. Layout Principles |
| 6. Components | 4. Component Stylings |
| 7. Motion & Interaction | 6. Depth & Elevation |
| 8. Voice & Brand | 7. Do's and Don'ts (or 8. Accessibility & States) |
| 9. Anti-patterns | 7. Do's and Don'ts ("Don't" side) |
| — | 8. Responsive Behavior |
| — | **9. Agent Prompt Guide** (always last) |

The key difference of Variant A: **section 9 is always the Agent Prompt Guide** (see §6 below),
and it folds "Spacing" into "Layout Principles" + adds "Responsive Behavior" and
"Depth & Elevation" as first-class sections. For a new project, pick **one**
variant and stick with it; `template.md` uses the canonical spec (Variant B).

---

## 3. The 4 token layers

Every shared token fits into a layer. This is what separates "a list of colors" from
a **token system**.

| Layer | Who decides | If omitted | Examples |
| --- | --- | --- | --- |
| **A1-identity** | brand | guard fails | `--bg`, `--fg`, `--accent`, `--font-display` |
| **A1-structure** | brand | guard fails | type scale, `--container-max`, `--section-y-*` |
| **A2-fallback** | brand (with fallback) | guard fails today; derive script fills in tomorrow | `--motion-fast`, `--success`, `--space-4`, `--font-mono` |
| **B-slot** | brand or schema-suggested alias | guard fails — brand must declare (as collapsed `var(--sibling)`, or richer independent value) | `--fg-2 → var(--fg)`, `--surface-warm → var(--surface)` |

Tokens outside the shared schema are **C-extensions** (per-brand allowlist, e.g.
`BRAND_EXTENSIONS[brand]`, or prefixes like `--tag-bg-*`).

### A1 — identity and structure (required)

The values that *are* the brand. Without them there is no contract.

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

### A2 — optional with fallback

Conceptually "optional with default", but since artifacts are generated by pasting a brand's
`:root` into a single `<style>` (no global stylesheet), **every brand must declare every A2
token** today. A `transition: var(--motion-fast)` breaks silently if `--motion-fast` is missing.

```css
:root {
  --motion-fast: 100ms ease-in;
  --motion-base: 150ms ease-out;
  --success: #26de81;
  --space-4: 16px;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
}
```

### B-slot — richer tier, with suggested alias

Shared components reference richer tiers via `var(--fg-2)`, `var(--meta)`,
`var(--surface-warm)`, `var(--border-soft)`. The `aliasTo` field is the **schema-suggested
default** — not a runtime fallback. A brand with no opinion copies the alias verbatim:

```css
:root {
  --fg-2: var(--fg);              /* default: collapsed 2-level fg */
  --surface-warm: var(--surface); /* default */
}
```

A brand with the richer tier binds an independent value:

```css
:root {
  --fg-2: #3d3d3a;        /* kami: dark warm */
  --surface-warm: #e8e6dc;/* kami: warm sand */
}
```

### C-extensions and the promotion path

```
C-extension                    B-slot                       A2
(1 brand declares)             (≥2 brands declare,          (every brand declares
                                some alias to sibling)       with a sensible default)
```

Promotion rules: **C→B-slot** when ≥2 brands declare the same name AND a sibling exists for
the alias. **C→A2** when ≥2 brands declare it AND a defensible cross-brand fallback exists. **B-slot→
A2** when ≥2 brands bind independently. **A2→A1** is rare (the formerly
defaultable value becomes a brand determinant).

### When *not* to add a token

Resist tokens that are: **component-internal** (a `.btn-primary` offset that nobody else
reads — inline the value), **one-off** (a hero's crop ratio), **speculative** ("maybe we'll
want `--motion-slow`"), or **already expressible** (`color-mix(...)` inline until ≥2 components
need the same tint).

---

## 4. CSS variables structure

### `:root` required

Every CSS variable inside `:root {}`. Loose declarations at the top of a section are
invalid. Exception: component-scoped overrides (`.card { --card-padding: 16px; }`) under
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

Never create separate light/dark blocks without the `[data-theme="dark"]` selector — it breaks the
semantic token system. Dark mode is a **genuine override** (different values), not a copy.

### Font labels for catalog extraction

Include it in the Typography section, exactly with the `Display:` / `Body:` / `Mono:` prefixes:

```
Font labels for catalog extraction:

Display: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif
Body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif
Mono: "JetBrains Mono", ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace
```

---

## 5. Accessibility (Lens A — blocking)

### WCAG AA contrast

Every text/data point must pass **4.5:1 minimum** against its background (4.5:1 normal text,
3:1 large text 18px+ or 14px+ bold). Test each foreground against the **paired background** — not
against white by default.

Common mistake: tertiary text on a dark surface. `#4A6080` over `#0A0A0A` = 2.1:1 (FAILS). Use
`#808086` over `#0A0A0A` = 4.54:1.

### Focus states

Every interactive component (buttons, links, inputs, clickable cards) needs
`:focus-visible`:

```css
.button-primary:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

### Targeted `prefers-reduced-motion`

Target specific properties/elements, never the global `*` selector:

```css
/* Correct */
@media (prefers-reduced-motion: reduce) {
  .alert-banner { animation-duration: 0.01ms !important; }
  .countdown { animation: none; }
}

/* Wrong — kills transitions across the entire site */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}
```

---

## 6. The "Agent Prompt Guide" section (the payload)

In the brand-grade exemplars, **section 9 is made FOR the agent to consume** when generating UI. It has three
parts:

1. **Quick Color Reference** — maps each role to its name + hex, in the format the agent
   cites: `Brand CTA: "Terracotta Brand (#c96442)"`.
2. **Example Component Prompts** — ready-to-paste prompts, each citing exact hex + font +
   radius: *"Create a hero on Parchment (#f5f4ed) with a 64px Anthropic Serif weight 500
   headline, line-height 1.10..."*.
3. **Iteration Guide** — recipe: one component at a time, cite specific color names,
   always specify the variant (warm/cool), describe serif vs sans explicitly.

Why it matters: the difference between a `DESIGN.md` that *describes* a brand and one an agent
*can build from* is this section. Without it, the agent improvises values. A new project's
`DESIGN.md` should end with its own Agent Prompt Guide.

---

## 7. Size and quality

A well-documented `DESIGN.md` typically has **300-600 lines**. Below ~100 lines
triggers a substance review (Lens B). Generic verbosity does not help.

| Area | Target lines |
| --- | --- |
| Color | 30-50 (palette tables + CSS blocks) |
| Components | 100-200 (3-6 components, fully specified) |
| Visual Theme | 30-40 (atmosphere + use cases + prior art) |
| Anti-patterns | 8-15 (one per key mistake) |
