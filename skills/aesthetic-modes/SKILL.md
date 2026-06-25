---
name: aesthetic-modes
description: >
  Three distinct visual modes for projects with a strong identity:
  EDITORIAL_MINIMALIST (Notion/Linear, warm monochrome), INDUSTRIAL_BRUTALIST
  (Swiss + CRT terminal), SOFT_PREMIUM (Apple-tier, glassmorphism nested cards).
  Use when: the user asks for "editorial minimalist style", "brutalist",
  "industrial", "soft UI", "Apple-tier", "Linear style", "Notion style",
  "warm monochrome", "blueprint UI", "terminal UI", or describes a specific
  visual mood that fits one of these 3 paradigms.
version: 1.0.0
inspired_by: >
  Leonxlnx/taste-skill (minimalist-skill + brutalist-skill + soft-skill) — MIT, 10k+ stars
metadata:
  source: "Leonxlnx/taste-skill"
  category: "frontend-quality"
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Aesthetic Modes — 3 Premium Design Paradigms

Pick ONE mode per project and commit. Never alternate or mix within the same interface.
Each mode has its own complete typographic, chromatic, and motion architecture.

---

## Mode 1: EDITORIAL_MINIMALIST

> *"Document-style interfaces analogous to top-tier workspace platforms (Notion, Linear).
> Warm monochrome, typographic contrast, flat bento grids, muted pastels."*

### When to use
- Knowledge tools, documentation platforms, internal SaaS, content-heavy products
- Audience values clarity + craft over spectacle
- Brand wants "quiet sophistication"

### Color Palette
- **Canvas:** `#FFFFFF` or warm bone `#F7F6F3` / `#FBFBFA`
- **Surface:** `#FFFFFF` or `#F9F9F8`
- **Borders:** ultra-light `#EAEAEA` or `rgba(0,0,0,0.06)` (1px exactly)
- **Body text:** off-black `#111111` or `#2F3437` (NEVER pure `#000`), line-height `1.6`
- **Muted text:** `#787774`
- **Spot pastels (sparingly, semantic only):**
  - Pale Red `#FDEBEC` / text `#9F2F2D`
  - Pale Blue `#E1F3FE` / text `#1F6C9F`
  - Pale Green `#EDF3EC` / text `#346538`
  - Pale Yellow `#FBF3DB` / text `#956400`

### Typography
- **Body/UI:** `'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer'`
- **Editorial headlines/quotes:** `'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif'`
  - Tight tracking `-0.02em` to `-0.04em`, leading `1.1`
- **Mono (code/meta/keystrokes):** `'Geist Mono', 'SF Mono', 'JetBrains Mono'`

### Components
- **Bento cards:** `border: 1px solid #EAEAEA`, `border-radius: 8px` or `12px` max, padding `24-40px`
- **Buttons:** solid `#111111` bg + `#FFFFFF` text, radius `4-6px`, no shadow. Hover `#333333` or scale `0.98`
- **Tags:** pill `border-radius: 9999px`, `text-xs`, uppercase, `letter-spacing: 0.05em`, pastel bg
- **Accordions (FAQ):** strip containers — only `border-bottom: 1px solid #EAEAEA` between items
- **`<kbd>` keys:** `border: 1px solid #EAEAEA`, `border-radius: 4px`, `background: #F7F6F3`, mono font
- **Faux-OS chrome:** when mocking software, wrap in container with white top bar + 3 small gray circles (macOS controls)

### Motion (quiet sophistication)
- Scroll entry: `translateY(12px) + opacity:0 → 0` over `600ms cubic-bezier(0.16, 1, 0.3, 1)`. Use IntersectionObserver.
- Hover: cards lift with ultra-subtle shadow `0 0 0 → 0 2px 8px rgba(0,0,0,0.04)` over 200ms
- Stagger: `animation-delay: calc(var(--index) * 80ms)`
- Optional ambient: single slow radial blob (`20s+`, `opacity 0.02-0.04`) on fixed `pointer-events: none` layer

### Banned in this mode
- Inter, Roboto, Open Sans
- Generic thin-line Lucide/Feather/Heroicons (use Phosphor Bold/Fill or Radix)
- Tailwind heavy shadows (`shadow-md/lg/xl`) — shadows must be ultra-diffuse opacity < 0.05
- Primary-colored backgrounds for large sections
- Gradients, neon, 3D glassmorphism (subtle navbar blur ok)
- `rounded-full` on large containers
- Emojis anywhere

---

## Mode 2: INDUSTRIAL_BRUTALIST

> *"Raw mechanical interfaces fusing Swiss typographic print with CRT terminal aesthetics.
> Rigid grids, extreme type scale contrast, utilitarian color, analog degradation."*

### When to use
- Data-heavy dashboards (telemetry, ops, control panels)
- Editorial / portfolio sites that need to feel like declassified blueprints
- Audience expects technical precision and rejects consumer UI patterns

### Two sub-archetypes — pick ONE
#### 2a. Swiss Industrial Print (light)
- **Background:** `#F4F4F0` or `#EAE8E3` (matte unbleached paper)
- **Foreground:** `#050505` to `#111111` (carbon ink)
- **Accent:** `#E61919` or `#FF2A2A` (aviation/hazard red) — ONLY accent

#### 2b. Tactical Telemetry / CRT Terminal (dark)
- **Background:** `#0A0A0A` or `#121212` (deactivated CRT — NEVER pure `#000`)
- **Foreground:** `#EAEAEA` (white phosphor)
- **Accent:** same red `#E61919` / `#FF2A2A`
- **Optional terminal green `#4AF626`:** ONE specific element only (status indicator) — never general text

### Typography
- **Macro headers:** Neue Haas Grotesk Black, Inter Extra Bold/Black, Archivo Black, Roboto Flex Heavy,
  Monument Extended. `clamp(4rem, 10vw, 15rem)`, tracking `-0.03em` to `-0.06em`, leading `0.85-0.95`,
  ALL UPPERCASE.
- **Micro (data/telemetry):** JetBrains Mono, IBM Plex Mono, Space Mono, VT323, Courier Prime.
  `10-14px`, tracking `0.05-0.1em`, leading `1.2-1.4`, UPPERCASE for metadata/IDs/coordinates.
- **Disruption (rare):** high-contrast serif (Playfair Display) with halftone/dither post-processing.

### Layout
- **Blueprint Grid:** CSS Grid. Elements anchored to tracks. NO floating.
- **Visible compartmentalization:** solid `1-2px` borders delineating zones. Full-width `<hr>` between units.
- **Bimodal density:** extreme data density adjacent to vast negative space framing macro-type.
- **Geometry:** ABSOLUTE rejection of `border-radius` — all corners 90°.

### UI Symbology
- ASCII framing: `[ DELIVERY SYSTEMS ]`, `< RE-IND >`, `>>>`, `///`, `\\\\`
- Industrial markers: `®`, `©`, `™` as geometric elements (not legal text)
- Crosshairs `+` at grid intersections
- Repeating vertical lines (barcodes), warning stripes, randomized strings (`REV 2.6`, `UNIT / D-01`)

### Textural Post-Processing
- **Halftone/1-bit dithering:** SVG radial dot patterns with `mix-blend-mode: multiply`
- **CRT scanlines (dark mode):**
  ```css
  repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)
  ```
- **Mechanical noise:** global low-opacity SVG noise filter on DOM root

### Web Engineering
- `display: grid; gap: 1px;` with contrasting parent/child backgrounds → razor-thin perfect dividers
- Semantic HTML: `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>` for telemetry accuracy
- `clamp()` for macro-typography across viewports

---

## Mode 3: SOFT_PREMIUM

> *"$150k agency-level digital experiences. Haptic depth, cinematic spatial rhythm,
> obsessive micro-interactions, flawless fluid motion. Apple-esque / Linear-tier."*

### When to use
- Premium SaaS, AI products, creative agency sites
- Audience expects "Awwwards" level craft
- Brand needs to feel expensive and considered

### Vibe Archetypes (Variance Engine — pick 1)
#### 3a. Ethereal Glass (SaaS / AI / Tech)
- Deepest OLED black `#050505`
- Radial mesh gradients (subtle glowing emerald/electric blue orbs, NOT purple)
- Vantablack cards with `backdrop-blur-2xl`, white/10 hairlines
- Wide geometric Grotesk typography

#### 3b. Editorial Luxury (Lifestyle / Real Estate / Agency)
- Warm creams `#FDFBF7`, muted sage, deep espresso
- High-contrast variable serif headers (Fraunces, Gambarino, Editorial New, Instrument Serif)
- Subtle CSS noise overlay (`opacity-[0.03]`) for physical paper feel

#### 3c. Soft Structuralism (Consumer / Health / Portfolio)
- Silver-grey or pure white
- Massive bold Grotesk typography
- Airy floating components with ultra-soft diffused ambient shadows

### Layout Archetypes (pick 1)
1. **Asymmetrical Bento** — masonry CSS Grid, varying card sizes (`col-span-8 row-span-2`
   next to stacked `col-span-4`)
2. **Z-Axis Cascade** — overlapping cards with varying depth, subtle `-2deg`/`3deg` rotations
   (REMOVE rotations + overlaps below `md:`)
3. **Editorial Split** — massive type left (`w-1/2`), scrollable horizontal pills right

### Banned in this mode
- Banned fonts: Inter, Roboto, Arial, Open Sans, Helvetica
- Available: Geist, Clash Display, PP Editorial New, Plus Jakarta Sans
- Banned icons: thick-stroked Lucide / FontAwesome / Material — use Phosphor Light / Remix Line
- Generic 1px solid gray borders
- Harsh dark drop shadows (`shadow-md`, `rgba(0,0,0,0.3)`)
- Edge-to-edge sticky navbars (use floating glass pills)
- Standard `linear` / `ease-in-out` transitions

### Components — Double-Bezel Architecture
Never place cards flat. Nest enclosures:
- **Outer shell:** wrapper div, subtle bg (`bg-black/5` or `bg-white/5`), hairline ring
  (`ring-1 ring-black/5` or `border border-white/10`), padding `p-1.5` or `p-2`,
  outer radius `rounded-[2rem]`
- **Inner core:** distinct bg, inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`),
  smaller radius (`rounded-[calc(2rem-0.375rem)]`)

### Nested CTA / Island Button
- Pills (`rounded-full px-6 py-3`)
- Trailing arrow `↗` nested in own circle wrapper (`w-8 h-8 rounded-full bg-black/5 dark:bg-white/10`)
  flush with main button's right inner padding

### Spatial Rhythm
- Macro-whitespace: section padding `py-24` to `py-40`
- Eyebrow tags: pill `rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em] font-medium`

### Motion — Fluid Dynamics
- Custom cubic-beziers: `transition-all duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]`
- **Fluid Island Nav:** floating glass pill detached from top (`mt-6 mx-auto w-max rounded-full`)
- **Hamburger morph:** lines rotate+translate to perfect 'X' (`rotate-45` + `-rotate-45`)
- **Menu modal expansion:** full-screen overlay `backdrop-blur-3xl bg-black/80` or `bg-white/80`
- **Staggered mask reveal:** nav links `translate-y-12 opacity-0 → 0` with `delay-100/150/200`
- **Magnetic buttons:** `active:scale-[0.98]` + nested icon `group-hover:translate-x-1 group-hover:-translate-y-[1px] scale-105`
- **Scroll entry:** `translate-y-16 blur-md opacity-0 → 0` over 800ms+
- Use IntersectionObserver or Framer Motion `whileInView` — NEVER `window.addEventListener('scroll')`

---

## Universal Constraints (apply in ALL modes)

### Mobile Override
- ANY asymmetric layout above `md:` MUST collapse below `768px` to:
  `w-full`, `px-4`, `py-8`, single column
- NEVER `h-screen` — always `min-h-[100dvh]`

### Performance Guardrails
- Animate ONLY `transform` and `opacity` (no `top/left/width/height`)
- `backdrop-blur` ONLY on fixed/sticky elements (never scrolling content)
- Grain/noise overlays ONLY on `position: fixed; pointer-events: none` layers
- Z-index discipline: only sticky nav, modals, overlays, tooltips
- Memoize CPU-heavy perpetual animations (`React.memo`), isolate in microscopic Client Components

### Content Quality
- No `John Doe`, `Acme Corp`, `Lorem Ipsum` — realistic contextual content
- No AI clichés: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve"
- No exclamation marks in success states
- No `Oops!` errors — be direct ("Connection failed. Please try again.")

---

## Example Outputs (per mode)

### EDITORIAL_MINIMALIST — example output
```html
<article style="background:#F7F6F3; border:1px solid #EAEAEA; border-radius:12px; padding:32px;">
  <span style="background:#E1F3FE; color:#1F6C9F; border-radius:9999px; font-size:11px;
    text-transform:uppercase; letter-spacing:0.05em; padding:2px 10px;">Docs</span>
  <h2 style="font-family:'Newsreader',serif; letter-spacing:-0.03em; line-height:1.1; color:#111;">Quiet, considered writing surface</h2>
  <p style="color:#787774; line-height:1.6;">Press <kbd>⌘K</kbd> to search.</p>
</article>
```
*Visual effect:* warm bone canvas, hairline-bordered bento card, serif headline against muted gray body — feels like a Notion/Linear document, calm and crafted.

### INDUSTRIAL_BRUTALIST — example output
```html
<section style="background:#0A0A0A; color:#EAEAEA; font-family:'JetBrains Mono',monospace;">
  <h1 style="font-family:'Archivo Black'; font-size:clamp(4rem,10vw,12rem);
    letter-spacing:-0.04em; line-height:0.9; text-transform:uppercase;">RE-IND</h1>
  <hr style="border:1px solid #EAEAEA;" />
  <p style="font-size:11px; letter-spacing:0.08em;">[ UNIT / D-01 ] >>> STATUS: <span style="color:#E61919;">ARMED</span> REV 2.6</p>
</section>
```
*Visual effect:* CRT-black panel with massive uppercase macro-type, telemetry mono micro-text, ASCII framing and a single hazard-red accent — reads like a declassified control console, zero rounded corners.

### SOFT_PREMIUM — example output
```html
<div class="rounded-[2rem] bg-white/5 ring-1 ring-white/10 p-1.5"><!-- outer shell -->
  <div class="rounded-[calc(2rem-0.375rem)] bg-[#0B0B0C] shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)] p-8"><!-- inner core -->
    <span class="rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em]">New</span>
    <h2 class="font-['Clash_Display'] text-5xl">Ship faster, feel expensive</h2>
    <button class="rounded-full px-6 py-3 bg-white text-black active:scale-[0.98]">Get started
      <span class="w-8 h-8 rounded-full bg-black/5 inline-flex items-center justify-center">↗</span></button>
  </div>
</div>
```
*Visual effect:* nested double-bezel glass card on OLED black with inner highlight, pill CTA with islanded arrow — haptic, Apple/Linear-tier depth that feels engineered, not decorated.

---

## Mode Selection Decision Tree

```
What does the user describe?
├── "minimal", "editorial", "Notion", "Linear", "clean", "warm", "document"
│   → EDITORIAL_MINIMALIST
├── "brutalist", "industrial", "Swiss", "blueprint", "terminal", "CRT",
│   "telemetry", "data-heavy", "raw", "mechanical"
│   → INDUSTRIAL_BRUTALIST
├── "premium", "Apple-tier", "agency", "$150k", "haptic", "glassmorphism",
│   "Linear-tier", "Awwwards", "luxury", "ethereal"
│   → SOFT_PREMIUM
└── unclear / mixed signals
    → ASK: "Which mood fits best — quiet editorial, raw industrial, or premium glass?"
```

---

## Related Skills
- `taste-design-dials` — 3-dial tuning system (use AFTER picking a mode)
- `frontend-design` — design principles, UX psychology, anti-patterns
- `aesthetic-boost` — compact anti-slop primer
- `ui-design-intelligence` — full design system spec generation
- `frontend-ui-system` — shadcn/ui + Magic UI + Aceternity component sources
