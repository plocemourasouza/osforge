---
name: taste-design-dials
description: "OSForge enhancement layer on top of the taste-skill with 3 adjustable dials (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY) plus Next.js App Router rules and OSForge structural constraints. Use when: 'raise motion to 8' or 'I want more minimal/more bold' (adjust dials), 'apply the taste dials to this OSForge project', 'compose the taste skill with the OSForge rules', 'premium design with configurable variance, motion, and density'. Keywords: dials, variance, motion intensity, density, OSForge, taste, enhancement layer, Next.js, premium design, anti-slop. Do NOT use for: standalone use of the taste skill outside OSForge projects (design-taste-frontend), DESIGN.md generation for Stitch (stitch-design-taste), pure GSAP motion (gpt-taste), technical Tailwind v4 patterns (tailwind-patterns)."
version: 1.1.0
compose_with:
  upstream:
    - design-taste-frontend
    - gpt-taste  # when MOTION_INTENSITY >= 8
  osforge:
    - osforge-design structural rules
    - aesthetic-boost
metadata:
  source: "Leonxlnx/taste-skill + OSForge"
  role: "enhancement-layer"
  category: "frontend-quality"
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Taste Design Dials — OSForge Enhancement Layer

> **Compose stack (mandatory in OSForge projects):**
> 1. Read `~/.claude/skills/design-taste-frontend/SKILL.md` — upstream visual quality + pre-flight
> 2. If `MOTION_INTENSITY >= 8`: also read `~/.claude/skills/gpt-taste/SKILL.md`
> 3. Apply **this skill** — dials + Next.js App Router + OSForge structural constraints
> 4. After build: `skills/quality/ui-audit` or `/impeccable polish <target>`

> **Override default LLM biases.** Premium UIs are not the median of training data.
> Pull every decision toward intention via three tunable dials.

## 1. Active Baseline (default values)

```
DESIGN_VARIANCE  = 8   (1=Symmetric/Predictable → 10=Asymmetric/Artsy Chaos)
MOTION_INTENSITY = 6   (1=Static → 10=Cinematic/GSAP scrolltelling)
VISUAL_DENSITY   = 4   (1=Art Gallery/Airy → 10=Cockpit/Packed Data)
```

Adapt these dynamically based on user prompt. Never ask the user to "edit the file" — listen
to the chat: "more minimal" → lower density; "I want strong animations" → raise motion; "more
bold" → raise variance.

## 2. Default Architecture (assume unless user specifies)

- **OSForge project check:** Read `osforge.config.json` + project `DESIGN.md` when present — tokens override defaults below.
- **Framework:** React / Next.js App Router. Default to Server Components.
- **RSC Safety:** Interactive UI extracted into isolated `'use client'` leaf components.
  Server Components render static layouts only.
- **State:** Local `useState`/`useReducer` for UI. Global state only for deep prop-drilling.
- **Styling:** Tailwind CSS. Check `package.json` for v3 vs v4 — never use v4 syntax in v3.
  For v4, use `@tailwindcss/postcss` or the Vite plugin (NOT `tailwindcss` in postcss.config).
- **Icons:** `@phosphor-icons/react` OR `@radix-ui/react-icons` — standardize one stroke-width.
- **Dependency Verification [MANDATORY]:** Before importing any 3rd-party lib (framer-motion,
  gsap, lucide-react, zustand), check `package.json`. If missing, output install command first.
- **Anti-Emoji [CRITICAL]:** NEVER use emojis in code, markup, alt text. Replace with icons
  or clean SVG primitives.

### Viewport Stability
- NEVER use `h-screen` for full-height heroes. ALWAYS `min-h-[100dvh]` (iOS Safari bug).
- Container layouts: `max-w-[1400px] mx-auto` or `max-w-7xl`.
- Grid over Flex math: NEVER `w-[calc(33%-1rem)]`. ALWAYS `grid grid-cols-1 md:grid-cols-3 gap-6`.

## 3. Anti-Bias Engineering Directives

### Rule 1 — Deterministic Typography
- **Display:** `text-4xl md:text-6xl tracking-tighter leading-none`
- **Banned fonts:** Inter, Roboto, Arial, Open Sans (for premium/creative contexts)
- **Allowed display fonts:** Geist, Outfit, Cabinet Grotesk, Satoshi
- **Dashboard rule:** Serifs BANNED in software UIs. Sans pairings only (Geist + Geist Mono,
  Satoshi + JetBrains Mono).
- **Body:** `text-base text-gray-600 leading-relaxed max-w-[65ch]`
- **2-Line Iron Rule (Hero):** H1 must NEVER exceed 2-3 lines. Use ultra-wide containers
  (`max-w-5xl`, `max-w-6xl`) + `clamp(3rem, 5vw, 5.5rem)`. 6-line wrap is a catastrophic failure.

### Rule 2 — Color Calibration
- **Max 1 accent color.** Saturation < 80%.
- **THE LILA BAN:** AI Purple/Blue aesthetic strictly BANNED. No purple glows, no neon gradients.
- **Neutral bases:** Zinc / Slate. Singular accent (Emerald, Electric Blue, Deep Rose).
- **Pure Black BAN:** Never `#000000`. Use Off-Black, Zinc-950, Charcoal.
- **Palette consistency:** Stick to one palette per project. No warm/cool gray fluctuation.

### Rule 3 — Layout Diversification
- **Anti-Center Bias:** Centered Hero/H1 BANNED when `DESIGN_VARIANCE > 4`. Force Split Screen
  (50/50), Left-Aligned with right asset, or Asymmetric Whitespace.
- **3-Column Equal Cards BANNED.** Use 2-column zig-zag, asymmetric grid, or horizontal scroll.
- **Bento `grid-flow-dense`:** mathematically interlock col-span/row-span. No empty cells.

### Rule 4 — Anti-Card Overuse
- For `VISUAL_DENSITY > 7`, generic card containers BANNED. Use `border-t`, `divide-y`, or
  negative space to group logic. Cards ONLY when elevation communicates hierarchy.
- When shadow IS used: tint to background hue (not generic black).

### Rule 5 — Interactive UI States (MANDATORY — OSForge 4 states)
LLMs default to "static successful states". You MUST implement full cycles per **osforge-design**:
- **Loading:** `loading.tsx` / `<Suspense>` + `<Skeleton>` mirroring layout (no generic spinners alone).
- **Empty:** `<EmptyState>` with icon + title + optional CTA.
- **Error:** `error.tsx` + `<Alert variant="destructive">` + retry; forms use `toast.error()`.
- **Success:** render content — no "Loaded successfully" toast.
- **Tactile Feedback:** On `:active`, use `-translate-y-[1px]` or `scale-[0.98]`.
- **Dialog/Sheet actions:** primary + cancel in `<DialogFooter>` / `<SheetFooter>` — never inside body.
- **i18n:** all user-facing strings via `t()` — no temporary hardcoded PT/EN.

### Rule 6 — Forms
Label ABOVE input. Helper text below input. Error text below input. Use `gap-2`.

## 4. Creative Proactivity (when MOTION_INTENSITY > 5)

### Magnetic Micro-physics
Buttons that pull slightly toward cursor.
**CRITICAL:** NEVER use React `useState` for continuous animations. Use Framer Motion's
`useMotionValue` + `useTransform` outside the render cycle (prevents mobile perf collapse).

### Perpetual Micro-Interactions
Embed infinite micro-animations (Pulse, Typewriter, Float, Shimmer, Carousel) in dashboard
components. Apply spring physics to ALL interactive elements: `type: "spring", stiffness: 100, damping: 20`.
**Performance critical:** memoize (React.memo), isolate in microscopic Client Components.

### Staggered Orchestration
Never mount lists/grids instantly. Use `staggerChildren` (Framer) or CSS cascade
(`animation-delay: calc(var(--index) * 100ms)`). Parent+Children MUST be in same Client tree.

### Liquid Glass (when glassmorphism needed)
Go beyond `backdrop-blur`. Add 1px inner border (`border-white/10`) + inner shadow
(`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) for physical edge refraction.

### Double-Bezel / Doppelrand (premium cards)
Never place cards flat on background. Nest enclosures:
- **Outer shell:** wrapper div with subtle background (`bg-black/5`), hairline ring
  (`ring-1 ring-black/5`), padding (`p-1.5`), large radius (`rounded-[2rem]`).
- **Inner core:** content container with own background, inset highlight, and mathematically
  calculated smaller radius (`rounded-[calc(2rem-0.375rem)]`).

## 5. Performance Guardrails

- **Hardware acceleration:** animate ONLY `transform` and `opacity`. Never `top/left/width/height`.
- **Grain/noise filters:** apply ONLY to `position: fixed; inset: 0; pointer-events: none` layers.
  NEVER on scrolling containers (continuous GPU repaints).
- **Backdrop-blur:** ONLY on fixed/sticky elements (navbars, overlays). NEVER on scrolling content.
- **Z-index discipline:** reserve for sticky nav, modals, overlays. No arbitrary `z-50` or `z-[9999]`.
- **GSAP vs Framer:** never mix in same component tree. Framer for UI/Bento interactions.
  GSAP/ThreeJS for isolated full-page scrolltelling or canvas backgrounds (strict useEffect cleanup).

## 6. Dial Definitions

### DESIGN_VARIANCE
- **1-3 (Predictable):** Flexbox `justify-center`, strict 12-col symmetric grids, equal padding.
- **4-7 (Offset):** `margin-top: -2rem` overlaps, varied aspect ratios (4:3 next to 16:9),
  left-aligned headers over center data.
- **8-10 (Asymmetric):** Masonry, CSS Grid with fractional units (`grid-template-columns: 2fr 1fr 1fr`),
  massive empty zones (`padding-left: 20vw`).
- **MOBILE OVERRIDE (4-10):** Any asymmetric layout above `md:` MUST collapse to strict
  single-column (`w-full`, `px-4`, `py-8`) below `768px`.

### MOTION_INTENSITY
- **1-3 (Static):** No auto animations. `:hover` and `:active` only.
- **4-7 (Fluid CSS):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay`
  cascades. Focus on `transform`/`opacity`. `will-change: transform` sparingly.
- **8-10 (Advanced Choreography):** Scroll-triggered reveals, parallax. Framer Motion hooks.
  NEVER `window.addEventListener('scroll')` — use IntersectionObserver or Framer `whileInView`.

### VISUAL_DENSITY
- **1-3 (Art Gallery):** Massive whitespace. Huge section gaps. Expensive/clean.
- **4-7 (Daily App):** Standard web spacing.
- **8-10 (Cockpit):** Tiny paddings. No card boxes — 1px lines separate data. MANDATORY: numbers
  in Monospace (`font-mono`).

## 7. AI Tells (forbidden patterns)

### Visual & CSS
- NO neon/outer `box-shadow` glows
- NO pure `#000000` (use Zinc-950, Charcoal, Off-Black)
- NO oversaturated accents
- NO excessive gradient text on large headers
- NO custom mouse cursors

### Typography
- NO Inter font for premium contexts
- NO oversized H1s screaming for attention — control hierarchy with weight+color
- NO serifs in dashboards/software UIs

### Layout
- NO complex flexbox `calc()` percentage math — use CSS Grid
- NO 3-column equal cards feature row

### Content & Data (Jane Doe Effect)
- NO generic names: "John Doe", "Sarah Chan", "Jack Su" — invent creative believable names
- NO generic avatars (no SVG eggs, no Lucide user icons)
- NO fake numbers: `99.99%`, `50%`, `1234567` — use organic (`47.2%`, `+1 (312) 847-1928`)
- NO startup slop names: "Acme", "Nexus", "SmartFlow" — invent premium contextual brands
- NO filler words: "Elevate", "Seamless", "Unleash", "Next-Gen"
- NO broken Unsplash links — use `https://picsum.photos/seed/{string}/W/H`
- NO meta-labels: "SECTION 01", "QUESTION 05", "ABOUT US" (cheap, unprofessional)

### Components
- shadcn/ui NEVER in generic default state — customize radii, colors, shadows

## 8. Creative Arsenal (high-end inspiration)

Pull from this library to break generic UI defaults:

### Navigation
- Mac OS Dock Magnification, Magnetic Button, Gooey Menu, Dynamic Island,
  Contextual Radial Menu, Floating Speed Dial, Mega Menu Reveal

### Layout
- Asymmetrical Bento, Z-Axis Cascade, Editorial Split, Masonry, Chroma Grid,
  Split Screen Scroll, Curtain Reveal

### Cards
- Parallax Tilt, Spotlight Border, Glassmorphism Panel (with inner refraction),
  Holographic Foil, Tinder Swipe Stack, Morphing Modal

### Scroll Animations
- Sticky Scroll Stack, Horizontal Scroll Hijack, Locomotive Scroll Sequence,
  Zoom Parallax, Scroll Progress Path, Liquid Swipe Transition

### Galleries
- Dome Gallery, Coverflow Carousel, Drag-to-Pan Grid, Accordion Image Slider,
  Hover Image Trail, Glitch Effect Image

### Typography
- Kinetic Marquee, Text Mask Reveal, Text Scramble (Matrix), Circular Text Path,
  Gradient Stroke Animation, Kinetic Typography Grid

### Micro-Interactions
- Particle Explosion Button, Liquid Pull-to-Refresh, Skeleton Shimmer,
  Directional Hover Aware Button, Ripple Click, Animated SVG Line Drawing,
  Mesh Gradient Background, Lens Blur Depth

## 9. Motion-Engine Bento 2.0 Paradigm

When generating SaaS dashboards or feature sections:

### Core Philosophy
- **Aesthetic:** High-end, minimal, functional.
- **Palette:** Background `#f9fafb`. Cards pure white `#ffffff` with `border-slate-200/50` 1px.
- **Surfaces:** `rounded-[2.5rem]` for major containers. Diffusion shadow:
  `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`.
- **Typography:** Geist / Satoshi / Cabinet Grotesk. `tracking-tight` for headers.
- **Labels OUTSIDE cards** (below) for gallery-style presentation.
- **Padding:** `p-8` or `p-10` inside cards.

### 5-Card Archetypes
1. **Intelligent List:** vertical stack with infinite auto-sorting loop. Items swap via `layoutId`.
2. **Command Input:** search bar with multi-step Typewriter Effect + blinking cursor +
   shimmering loading gradient.
3. **Live Status:** breathing status indicators + pop-up notification with overshoot spring,
   3s stay, vanish.
4. **Wide Data Stream:** horizontal Infinite Carousel (`x: ["0%", "-100%"]`).
5. **Contextual UI:** staggered highlight on text + Float-in floating action toolbar.

## 10. Pre-Flight Check (run before output)

- [ ] Dependency verification passed (all imports exist in package.json)
- [ ] No banned fonts/icons/colors/layouts from Section 7
- [ ] Hero H1 fits in 2-3 lines (verified by max-w + clamp)
- [ ] Bento grid uses `grid-flow-dense` — zero empty cells
- [ ] Mobile collapse guaranteed: `w-full`, `px-4`, `max-w-7xl mx-auto`
- [ ] Full-height uses `min-h-[100dvh]`, NOT `h-screen`
- [ ] useEffect animations have cleanup functions
- [ ] Empty, loading, error states present
- [ ] CPU-heavy perpetual animations isolated in own Client Components
- [ ] Animation uses only `transform` + `opacity`
- [ ] `backdrop-blur` only on fixed/sticky elements

---

## Related Skills
- `design-taste-frontend` — **upstream base** (read first)
- `gpt-taste` — upstream motion engine when `MOTION_INTENSITY >= 8`
- `frontend-design` — design thinking + UX psychology
- `aesthetic-boost` — anti-AI-slop compact primer
- `aesthetic-modes` — Editorial / Brutalist / Soft Premium
- `redesign-audit` — brownfield upgrades with OSForge structural pass
- `ui-audit` — 6-pillar review after implementation
