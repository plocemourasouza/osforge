---
name: aesthetic-boost
description: >
  Anti-AI-slop aesthetic boost. Invoke alongside any frontend skill to
  elevate visual quality. Activate when the user asks for "beautiful design",
  "striking visuals", "landing page", "hero section", "improve design",
  "strong visual identity", or any task that requires visually
  distinct output. Compact (~500 tokens) for minimal context overhead.
version: 1.0.0
inspired_by: anthropics/claude-code frontend-design plugin (MIT, 277K+ installs)
---

# Aesthetic Boost — Anti-AI-Slop Directive

> Models converge toward generic designs because of **distributional convergence**:
> high-probability tokens dominate sampling, and "safe" design choices
> (Inter, purple gradients, predictable layouts) are overrepresented in the training data.
> This skill is an **intentional perturbation** that shifts generation away from the center of the distribution.

## Before Coding

Commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme — brutally minimal, maximalist chaos, retro-futuristic,
  organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw,
  art deco/geometric, soft/pastel, industrial/utilitarian
- **Differentiation**: What makes it UNFORGETTABLE? What is the *one thing* they will remember?

**CRITICAL**: Intentionality, not intensity. Bold maximalism and refined minimalism
both work — what matters is executing the vision with precision.

## 5 Aesthetic Axes

1. **Typography**: Beautiful, unique, interesting fonts. FORBIDDEN: Inter, Roboto, Arial,
   system fonts. Pair display font + body font with high contrast. Weight extremes
   (100/200 vs 800/900). Scale jumps 3x+, not 1.5x. Google Fonts or local fonts.

2. **Color & Theme**: CSS variables for consistency. Dominant colors with sharp accents
   beat timid, uniform palettes. FORBIDDEN: purple gradients on a white background.

3. **Motion**: CSS-only for HTML. Motion library (framer-motion) for React.
   One orchestrated page load with staggered reveals (animation-delay) > scattered
   micro-interactions. Scroll-triggering and hover states that surprise.

4. **Spatial Composition**: Asymmetry. Overlap. Diagonal flow. Grid-breaking.
   Generous negative space OR controlled density. Not: generic bento grids.

5. **Backgrounds & Depth**: Gradient meshes, noise textures, geometric patterns,
   layered transparencies, dramatic shadows, decorative borders, grain overlays.
   Create atmosphere — never default to flat solid colors.

## Expected Output Examples (per axis)

1. **Typography** — display + body pairing with extreme contrast:
   ```css
   h1 { font-family: 'Fraunces', serif; font-weight: 900; font-size: clamp(3rem, 9vw, 8rem); letter-spacing: -0.04em; }
   body { font-family: 'Switzer', sans-serif; font-weight: 300; }
   ```
   *Visual effect:* massive, striking headline against a light body — unmistakable hierarchy, zero template feel.

2. **Color & Theme** — dominant + sharp accent via CSS variables:
   ```css
   :root { --ink: #1A1714; --canvas: #F4EFE6; --accent: #E63B1F; }
   ```
   *Visual effect:* warm monochrome palette with a single surgical red that guides the eye to the CTA.

3. **Motion** — orchestrated page load with stagger:
   ```css
   .reveal { animation: rise 700ms cubic-bezier(0.16,1,0.3,1) both; animation-delay: calc(var(--i) * 90ms); }
   @keyframes rise { from { opacity: 0; transform: translateY(24px); } }
   ```
   *Visual effect:* hero elements enter in a choreographed cascade, a premium-product feel.

4. **Spatial Composition** — asymmetric grid with overlap:
   ```css
   .hero { display: grid; grid-template-columns: 5fr 7fr; }
   .hero img { margin-top: -6rem; transform: rotate(-2deg); }
   ```
   *Visual effect:* the image invades the text column diagonally, breaking the predictability of the centered layout.

5. **Backgrounds & Depth** — atmosphere with mesh + grain:
   ```css
   .bg { background: radial-gradient(60% 80% at 20% 10%, #2E4036 0%, #0E0E0C 70%); }
   .grain { position: fixed; inset: 0; pointer-events: none; opacity: 0.04; background-image: url('noise.svg'); }
   ```
   *Visual effect:* dark background with an organic glow and film texture — depth instead of flat solid color.

## Anti-Convergence

NEVER use the same choices across projects. Vary between light/dark, different fonts,
different aesthetics. NEVER converge toward common "second-order" choices (Space Grotesk,
deep cyan, standard glassmorphism) — when escaping the obvious defaults, the model tends to fall
into a NEW set of equally generic defaults. Break that cycle.

If you notice pattern repetition within the same session → change radically.

## Complexity Matching (MANDATORY)

Code complexity MUST mirror the aesthetic vision:
- **Maximalist** → elaborate code, extensive animations, layered effects
- **Minimalist** → extreme restraint, millimeter precision in spacing/typography, subtle details
- **NEVER:** minimalist design with unnecessarily complex code, or ambitious design with lazy code
- Elegance comes from executing the vision with precision

## Brand Identity (If Available)

If the project has brand assets (dark/light logo, hex palette, defined fonts, visual concept):
- USE THEM as the foundation — the skill amplifies the existing identity
- Mention the assets in the prompt: "Use assets in /public/brand"
- Brand fonts > skill fonts

No brand assets → create an original, consistent aesthetic direction for the context.

> **Remember:** Claude is capable of extraordinary creative work. Don't hold back — show what
> can be created when you think outside the box and fully commit to a distinct vision.

---

## Related Skills (deep-dive when you need more than the compact primer)

- **`taste-design-dials`** — tunable 3-dial system (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY)
  + Creative Arsenal + Motion-Engine Bento 2.0 + complete AI Tells
- **`aesthetic-modes`** — 3 distinct paradigms (Editorial Minimalist / Industrial Brutalist / Soft Premium)
- **`redesign-audit`** — apply this boost to an existing project via audit and surgical upgrades
- **`frontend-design`** — design principles + UX psychology (read first)
- **`ui-design-intelligence`** — generate a design system spec adapted to the product and industry
- **`stitch-design-export`** — generate a DESIGN.md compatible with Google Stitch
