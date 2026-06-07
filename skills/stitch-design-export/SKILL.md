---
name: stitch-design-export
description: "OSForge enhancement layer sobre stitch-design-taste. Gera DESIGN.md para Google Stitch com tokens de osforge.config.json + Impeccable. ACIONE com stitch-design-taste quando: 'Google Stitch', 'DESIGN.md', 'exportar design system', 'Stitch prompt'. Exemplos concretos de uso: 'quero gerar as telas desse projeto no Google Stitch', 'cria um DESIGN.md com os tokens do projeto para o Stitch', 'exporta o design system OSForge para usar no Stitch', 'prepara o prompt de design antes de gerar screens no Stitch'."
version: 1.1.0
compose_with:
  upstream:
    - stitch-design-taste
  osforge:
    - ui-design-intelligence
metadata:
  source: "Leonxlnx/taste-skill + OSForge"
  role: "enhancement-layer"
  category: "design-tools"
allowed-tools: Read, Write, Edit, Glob
---

# Stitch Design Export — OSForge Enhancement Layer

> **Compose stack:**
> 1. Read `~/.claude/skills/stitch-design-taste/SKILL.md` — upstream semantic DESIGN.md spec
> 2. Apply **this skill** — merge OSForge project tokens + industry palette from `ui-design-intelligence`
> 3. Output path: project root `DESIGN.md` (or path user specifies)

Generates `DESIGN.md` files optimized for Google Stitch screen generation. Stitch interprets
design through "Visual Descriptions" — descriptive natural-language rules paired with precise
hex/typography/component values. This skill encodes premium anti-slop directives into that
semantic format **and** syncs with the active OSForge project when present.

## Prerequisites
- Access to Google Stitch ([labs.google.com/stitch](https://labs.google.com/stitch))
- Upstream `stitch-design-taste` loaded (semantic spec authority)
- **OSForge:** read `osforge.config.json` → `design.register` overrides default dials/palette
- Optionally: Stitch MCP server for programmatic integration with Cursor/Antigravity/Gemini CLI

## What gets encoded
1. **Visual atmosphere** — mood, density, design philosophy
2. **Color calibration** — neutrals, accents, banned patterns + hex codes
3. **Typographic architecture** — font stacks, scale hierarchy, anti-patterns
4. **Component behaviors** — buttons, cards, inputs with interaction states
5. **Layout principles** — grid systems, spacing philosophy, responsive strategy
6. **Motion philosophy** — spring physics, perpetual micro-interactions, perf rules
7. **Anti-patterns** — explicit AI clichés to avoid

## Analysis & Synthesis Process

### 1. Define the atmosphere
Use evocative dimensions:
- **Density:** "Art Gallery Airy" (1-3) → "Daily App Balanced" (4-7) → "Cockpit Dense" (8-10)
- **Variance:** "Predictable Symmetric" (1-3) → "Offset Asymmetric" (4-7) → "Artsy Chaotic" (8-10)
- **Motion:** "Static Restrained" (1-3) → "Fluid CSS" (4-7) → "Cinematic Choreography" (8-10)

Default baseline: Variance 8, Motion 6, Density 4. Adapt to user vibe.

### 2. Map color palette
For each color provide: **Descriptive Name** + **Hex Code** + **Functional Role**.

**Constraints:**
- Max 1 accent. Saturation < 80%.
- THE LILA BAN — AI Purple/Blue neon strictly forbidden.
- Absolute neutral bases (Zinc / Slate) + singular high-contrast accent.
- One palette per output — no warm/cool gray fluctuation.
- Never pure `#000000` — Off-Black / Zinc-950 / Charcoal.

### 3. Establish typography rules
- **Display:** track-tight, controlled scale. Hierarchy via weight+color, not size.
- **Body:** relaxed leading, max 65 characters per line.
- **Inter is BANNED** for premium/creative contexts. Use Geist, Outfit, Cabinet Grotesk, Satoshi.
- **Generic serifs BANNED** (Times New Roman, Georgia, Garamond, Palatino). If serif needed:
  Fraunces, Gambarino, Editorial New, Instrument Serif only.
- **Serif always BANNED** in dashboards/software UIs.
- **Dashboard:** Sans pairings only (Geist + Geist Mono, Satoshi + JetBrains Mono).
- **High-density override:** density > 7 → all numbers in monospace.

### 4. Define the Hero section
- **Inline Image Typography:** embed small contextual photos directly between words in headline,
  inline at type-height, rounded — acting as visual punctuation. SIGNATURE technique.
- **No overlapping:** every element occupies its own clean spatial zone.
- **No filler UI text:** "Scroll to explore", "Swipe down", scroll arrows, bouncing chevrons BANNED.
- **Asymmetric structure:** centered Hero layouts BANNED when variance > 4.
- **CTA restraint:** max 1 primary CTA. No secondary "Learn more" links.

### 5. Component stylings
- **Buttons:** tactile push on `:active`. No neon outer glows. No custom mouse cursors.
- **Cards:** ONLY when elevation communicates hierarchy. Tint shadows to background hue.
  High-density → replace with border-top dividers or negative space.
- **Inputs:** label above, helper optional, error below. Standard gap spacing.
- **Loading:** skeletal loaders matching layout dimensions (NO circular spinners).
- **Empty states:** composed compositions indicating how to populate.
- **Error states:** clear inline error reporting.

### 6. Layout principles
- No overlapping elements — clean spatial separation always.
- Centered Hero BANNED when variance > 4 — force Split Screen, Left-Aligned, or Asymmetric Whitespace.
- 3 equal cards horizontally BANNED — 2-col Zig-Zag, asymmetric grid, or horizontal scroll.
- CSS Grid > Flexbox math — never `calc()` percentage hacks.
- Max-width containment (~1400px centered).
- Full-height MUST use `min-h-[100dvh]`, never `h-screen`.

### 7. Responsive rules
- **Mobile-First Collapse (< 768px):** all multi-column → single column. No exceptions.
- **No horizontal scroll** on mobile (critical failure).
- **Typography:** `clamp()` for headlines. Body min `1rem`/`14px`.
- **Touch targets:** min `44px`.
- **Inline typography images:** stack below headline on mobile.
- **Navigation:** desktop horizontal → mobile clean menu.
- **Spacing:** vertical gaps reduce proportionally (`clamp(3rem, 8vw, 6rem)`).

### 8. Motion philosophy
- **Spring physics default:** `stiffness: 100, damping: 20` — premium weighty feel.
- **Perpetual micro-interactions:** every active component loops infinitely (Pulse, Typewriter,
  Float, Shimmer).
- **Staggered orchestration:** cascade delays for waterfall reveals — never mount lists instantly.
- **Performance:** animate ONLY `transform` and `opacity`. Grain/noise on fixed pseudo-elements only.

### 9. Anti-patterns (encode as "NEVER DO" in DESIGN.md)
- No emojis anywhere
- No `Inter` font
- No generic serifs (Times New Roman, Georgia, Garamond)
- No pure `#000000`
- No neon/outer glow shadows
- No oversaturated accents
- No excessive gradient text on large headers
- No custom mouse cursors
- No overlapping elements
- No 3-column equal card layouts
- No generic names ("John Doe", "Acme", "Nexus")
- No fake round numbers (`99.99%`, `50%`)
- No AI copywriting clichés ("Elevate", "Seamless", "Unleash", "Next-Gen")
- No filler UI text ("Scroll to explore", scroll arrows)
- No broken Unsplash links — use `picsum.photos` or SVG avatars
- No centered Hero for high-variance projects

## Output Template

```markdown
# Design System: [Project Title]

## 1. Visual Theme & Atmosphere
(Evocative 2-3 sentence description. Example:
"A restrained, gallery-airy interface with confident asymmetric layouts and fluid
spring-physics motion. The atmosphere is clinical yet warm — like a well-lit
architecture studio.")

## 2. Color Palette & Roles
- **Canvas White** (#F9FAFB) — Primary background surface
- **Pure Surface** (#FFFFFF) — Card and container fill
- **Charcoal Ink** (#18181B) — Primary text, Zinc-950 depth
- **Muted Steel** (#71717A) — Secondary text, metadata
- **Whisper Border** (rgba(226,232,240,0.5)) — Card borders, 1px structural lines
- **[Accent Name]** (#XXXXXX) — Single accent for CTAs, active, focus rings
(Max 1 accent. Saturation < 80%. No purple/neon.)

## 3. Typography Rules
- **Display:** [Font Name] — Track-tight, controlled scale, weight-driven hierarchy
- **Body:** [Font Name] — Relaxed leading, 65ch max-width, neutral secondary
- **Mono:** [Font Name] — Code, metadata, timestamps, high-density numbers
- **Banned:** Inter, generic system fonts, serifs in dashboards

## 4. Component Stylings
- **Buttons:** Flat, no outer glow. Tactile -1px translate on active. Accent fill primary,
  ghost outline secondary.
- **Cards:** Generously rounded (2.5rem). Diffused whisper shadow. Used only when elevation
  serves hierarchy. High-density: border-top dividers instead.
- **Inputs:** Label above, error below. Focus ring in accent. No floating labels.
- **Loaders:** Skeletal shimmer matching exact layout dimensions. No circular spinners.
- **Empty States:** Composed illustrated compositions — never "No data" text.

## 5. Layout Principles
Grid-first responsive architecture. Asymmetric splits for Hero. Strict single-column collapse
below 768px. Max-width containment. No flexbox percentage math. Generous internal padding.

## 6. Motion & Interaction
Spring physics for all interactive elements. Staggered cascade reveals. Perpetual micro-loops on
active dashboard components. Hardware-accelerated transforms only. Isolated Client Components for
CPU-heavy animations.

## 7. Anti-Patterns (Banned)
No emojis. No Inter. No pure black. No neon glows. No 3-column equal grids. No AI copywriting
clichés. No generic placeholder names. No broken image links. No scroll arrows. No custom cursors.
```

## Best Practices for Stitch Output
- **Be Descriptive:** "Deep Charcoal Ink (#18181B)" — not just "dark text"
- **Be Functional:** explain what each element is used for
- **Be Consistent:** same terminology throughout
- **Be Precise:** exact hex codes, rem values, pixel values in parentheses
- **Be Opinionated:** this is NOT a neutral template — enforce the curated aesthetic

## Common Pitfalls
- Using Tailwind jargon ("rounded-xl") instead of semantic ("generously rounded corners")
- Omitting hex codes or only using descriptive names
- Forgetting functional roles
- Vague atmosphere descriptions
- Ignoring the anti-pattern list (these are what make output premium)
- Defaulting to "safe" designs instead of enforcing the curated direction

---

## Related Skills
- `stitch-design-taste` — **upstream base** (read first)
- `ui-design-intelligence` — industry palette + OSForge token merge
- `taste-design-dials` — dials encoded into DESIGN.md
- `aesthetic-modes` — pick a mode before generating DESIGN.md
