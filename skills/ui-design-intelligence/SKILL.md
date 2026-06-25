---
name: ui-design-intelligence
description: "Design system spec adapted to the product and industry. Use when: the user mentions visual style, identity, palette, typography, visual tone, product type or industry (fintech, healthcare, saas, e-commerce, etc). Produces a complete design system spec. Keywords: visual style, visual identity, palette, typography, design system, visual tone, landing page, fintech, healthcare, e-commerce, saas dashboard, aesthetic, brand, colors, fonts."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Glob
metadata:
  inspired_by: nextlevelbuilder/ui-ux-pro-max-skill
---

# UI Design Intelligence

## Role

A design consultant with access to curated knowledge bases: visual styles,
palettes by industry, typographic pairs, UX guidelines, and chart types.
Stack-agnostic — adapts the recommendations for any framework or library.

---

## When to use

- When starting any feature with a significant visual component
- When the user wants the UI to "feel" like something specific (professional, playful,
  premium, minimalist, dark tech, etc.)
- Before calling `openui-genui-layout` — provide the design system as input
- To align multiple screens with a consistent visual identity
- When the product type implies the industry's visual expectations

---

## Process: Design System Generation

### 1. Collect inputs

From the user or the existing context:
- **Product type:** SaaS, e-commerce, fintech, healthcare, portfolio, landing page, dashboard, mobile app
- **Industry/niche:** accounting, legal, tourism, beauty, gaming, education, etc.
- **Style keywords:** words the user uses ("clean", "premium", "playful", "dark", "corporate")
- **Target stack:** Next.js + shadcn/ui, React + Tailwind, Vue, plain HTML, React Native, Flutter
- **Mode:** light / dark / system

If the user did not provide a style: infer it from the product type via `references/reasoning-rules.md` (rule by industry) and `references/styles.md`.

### 2. Parallel multi-domain search

Consult simultaneously (read the relevant sections of each reference):

```
[Parallel]
A → references/reasoning-rules.md  — rule by product/industry: pattern + style + color + typography + anti-patterns (STARTING POINT)
B → references/styles.md          — visual style + CSS tokens
C → references/color-palettes.md  — palette by industry/product
D → references/typography-pairs.md — compatible typographic pair
E → references/ux-guidelines.md   — UX guidelines critical for the context
F → references/chart-types.md     — chart types if it's a dashboard/analytics
```

When the product type matches a rule in `reasoning-rules.md`, use it as the backbone and refine with the other references.

### 3. Synthesize the design system spec

Produce a structured block:

```markdown
## Design System Spec — {Product Name}

### Visual Style
Name: {style} | Atmosphere: {1-sentence description}
References: {known products with this style}

### Color Palette
| Token          | Hex     | Use |
|----------------|---------|-----|
| --primary      | #...    | CTAs, links, accent elements |
| --primary-dark | #...    | Hover, pressed states |
| --background   | #...    | Main background |
| --surface      | #...    | Cards, modals, sidebars |
| --text-primary | #...    | Primary text |
| --text-muted   | #...    | Labels, placeholders, captions |
| --border       | #...    | Dividers, inputs |
| --success      | #...    | Positive feedback |
| --warning      | #...    | Alerts |
| --error        | #...    | Errors, destructive states |
| --accent       | #...    | Secondary accent elements |

### Typography
Heading: {font} | Body: {font} | Mono: {optional font}
Import: {CSS @import or Google Fonts link}
Scale: xs(12) sm(14) base(16) lg(18) xl(20) 2xl(24) 3xl(30) 4xl(36)

### Spacing Scale
4px base — use multiples: 4, 8, 12, 16, 24, 32, 48, 64, 96

### Radius System
sm: 4px | md: 8px | lg: 12px | xl: 16px | full: 9999px
Overall style: {sharp/rounded/very-rounded}

### Shadow System
{describe 2-3 shadow levels compatible with the style}

### Priority UX Guidelines
{3-5 most critical guidelines for this product type}

### Recommended Charts (if applicable)
{chart type → when to use → suggested library}

### Adaptation by Stack
**Next.js + shadcn/ui:** apply tokens as CSS variables in globals.css;
use shadcn variants mapped to the palette
**React + plain Tailwind:** extend tailwind.config with the tokens
**Vue/Nuxt:** CSS variables in the :root of app.vue
**React Native:** StyleSheet with the tokens; use expo-font for typography
**HTML + Tailwind:** CDN + inline CSS variables in :root
```

#### Short example of generated output

```markdown
## Design System Spec — PayFlow (fintech SaaS B2B)

### Visual Style
Name: Corporate Trust Minimal | Atmosphere: sober, precise, trustworthy
References: Stripe Dashboard, Mercury, Brex

### Color Palette
| Token          | Hex     | Use |
|----------------|---------|-----|
| --primary      | #0F4C81 | CTAs, links |
| --background   | #FAFBFC | Main background |
| --surface      | #FFFFFF | Cards, modals |
| --text-primary | #1A2330 | Primary text |
| --success      | #1E7F4F | Confirmed transactions |
| --error        | #C0392B | Payment failures |

### Typography
Heading: Geist | Body: Geist | Mono: JetBrains Mono (monetary values, tabular-nums)
Scale: xs(12) sm(14) base(16) lg(18) xl(20) 2xl(24) 3xl(30)

### Priority UX Guidelines
1. Monetary values always in a mono font with tabular-nums
2. Destructive states require two-step confirmation
3. Dense tables with subtle zebra striping, never cards for financial data
```

### 4. Handoff to dependent skills

At the end, state how the design system connects:

- **→ `openui-genui-layout`:** "Use this palette and typography when generating the OpenUI Lang plan and the components"
- **→ `ui-audit`:** "This spec is the reference for Pillar 2 (Consistency) and Pillar 6 (Alignment)"
- **→ `phase-discussion`:** "The style decisions here replace the phase's visual discussion"
- **→ `frontend-engineer`:** "Load this spec before implementing any component of the feature"

---

## References

- `references/reasoning-rules.md` — 161 rules by product/industry (design system engine v2.0)
- `references/styles.md` — 84 visual styles with tokens and when to use them
- `references/color-palettes.md` — 161 palettes by industry and product
- `references/typography-pairs.md` — 73 curated typographic combinations
- `references/ux-guidelines.md` — 99 UX guidelines with anti-patterns
- `references/chart-types.md` — 25 chart types for dashboards and analytics


## Gotchas

- **Generating a design system without collecting inputs**: never infer the style from the project name alone. Always ask for the product type, industry, and style keywords before generating — even if it seems obvious. "ContaFácil" might want to be serious and corporate or approachable and colorful.
- **Applying a generic "SaaS" spec**: SaaS is a huge category — fintech SaaS, healthcare SaaS, and gaming SaaS have completely different visual expectations. Always refine by industry/niche, not just by the business model.
- **Not handing off to `openui-genui-layout`**: the spec generated here must be explicitly passed as input to `openui-genui-layout` before any UI generation. Without it, the generated components won't follow the design system.
- **Hard-coded colors in the code**: the spec uses CSS variable tokens (`--primary`, `--background`, etc). If the developer implements with direct hex values (`#2563EB`), dark mode and dynamic theming break. Always map to shadcn CSS variables.
- **Typography without the correct `@import`**: when using Google Fonts, verify that the `@import` is in `globals.css` before referencing the family. Unloaded fonts silently fall back to the system.
- **An outdated spec after a change of direction**: if the user shifts from "premium fintech" to "an accessible product for small businesses" during development, the design system needs to be regenerated — not patched. Partially updated specs cause visual inconsistency.
