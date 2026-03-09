---
name: frontend-ui-system
description: Frontend UI development using shadcn/ui ecosystem with extended registries (Magic UI, Aceternity UI, mapcn). Leverages shadcn MCP and shadcn Studio extension for component discovery, installation, and composition. Use when building interfaces, landing pages, dashboards, forms, maps, animations, or any UI work. Triggers on component creation, UI design, layout building, animation effects, map integration, or when choosing between component libraries.
---

# Frontend UI System

Build interfaces using shadcn/ui as foundation + extended registries for animations, effects, and maps.

## Component Sources (Priority Order)

### 1. shadcn/ui — Foundation (always check first)
- **Site:** https://ui.shadcn.com
- **What:** Core primitives — buttons, forms, dialogs, tables, navigation, data display
- **Install:** `bunx shadcn@latest add <component>`
- **MCP:** Use Shadcn MCP to browse/search/install components via natural language
- **Studio:** shadcn Studio extension provides visual theme editing and component preview

### 2. Magic UI — Animations & Effects
- **Site:** https://magicui.design
- **What:** 150+ animated components — marquees, text animations, backgrounds, device mocks, special effects
- **Install:** `bunx shadcn@latest add "https://magicui.design/r/<component>"`
- **MCP:** `pnpm dlx @magicuidesign/cli@latest install cursor` (installs Magic UI MCP)
- **Dir:** `components/magicui/`
- **Best for:** Landing pages, hero sections, marketing sites, CTAs, visual polish

### 3. Aceternity UI — Premium Interactions
- **Site:** https://ui.aceternity.com
- **What:** 100+ components — 3D cards, parallax, hover effects, background beams, floating elements
- **Install:** `bunx shadcn@latest add @aceternity/<component>`
- **Registry config required** in `components.json`:
  ```json
  "registries": {
    "@aceternity": "https://ui.aceternity.com/registry/{name}.json"
  }
  ```
- **Search:** `bunx shadcn search @aceternity -q "<term>"`
- **Dir:** `components/aceternity/` or `components/ui/`
- **Best for:** Hero sections, product showcases, interactive cards, visual storytelling

### 4. mapcn — Map Components
- **Site:** https://mapcn.dev (docs: https://mapcn.vercel.app)
- **What:** MapLibre GL components — maps, markers, popups, routes, controls
- **Install:** `bunx shadcn@latest add "https://mapcn.dev/r/map"`
- **Dir:** `components/ui/map/`
- **No API key required** — uses CARTO free basemaps (auto dark/light theme)
- **Best for:** Store locators, dashboards with geo data, location-based features

## Decision Matrix — Which Source?

| Need | Source | Example Component |
|------|--------|-------------------|
| Form, dialog, table, nav | **shadcn/ui** | Form, DataTable, Sheet, Command |
| Text animation | **Magic UI** | TextAnimate, TypingAnimation, NumberTicker |
| Background effect | **Magic UI** or **Aceternity** | FlickeringGrid, BackgroundBeams |
| 3D card / hover effect | **Aceternity** | 3DCard, CardHoverEffect, SpotlightCard |
| Hero section background | **Aceternity** | AuroraBackground, Vortex, Meteors |
| Marquee / scroll animation | **Magic UI** | Marquee, ScrollBasedVelocity |
| Interactive map | **mapcn** | Map, MapMarker, MapPopup, MapRoute |
| Device mockup | **Magic UI** | Safari, iPhone, Android |
| Button with effect | **Magic UI** | ShimmerButton, RainbowButton |
| Bento grid layout | **Magic UI** | BentoGrid |
| Floating dock nav | **Aceternity** | FloatingDock |

## MCP Workflow

### Using Shadcn MCP (primary)
The Shadcn MCP allows natural language interaction:
- "Show me all available form components"
- "Install the combobox component"
- "What components exist for navigation?"

### Using Magic UI MCP (animations)
After installing: `pnpm dlx @magicuidesign/cli@latest install cursor`
- "Add a blur fade text animation"
- "Add a grid background pattern"
- "Add a vertical marquee of logos"

### Combined workflow
1. Ask Shadcn MCP → check if shadcn/ui has the component
2. If not found or need animation/effect → check Magic UI or Aceternity
3. If need maps → use mapcn directly

## Architecture Rules

### Directory Structure
```
components/
├── ui/              # shadcn/ui core (DO NOT modify originals)
│   ├── button.tsx
│   ├── form.tsx
│   ├── map/         # mapcn components
│   │   ├── map.tsx
│   │   ├── map-marker.tsx
│   │   └── map-controls.tsx
│   └── ...
├── magicui/         # Magic UI components (separate folder)
│   ├── marquee.tsx
│   ├── bento-grid.tsx
│   └── ...
├── aceternity/      # Aceternity UI components (separate folder)
│   ├── background-beams.tsx
│   ├── 3d-card.tsx
│   └── ...
└── custom/          # Project-specific compositions
    └── hero-section.tsx
```

### Client Component Rules
- **All** Magic UI and Aceternity components require `"use client"` (they use Framer Motion)
- Use `next/dynamic` with `ssr: false` for heavy animation components:
  ```tsx
  const BackgroundBeams = dynamic(
    () => import('@/components/aceternity/background-beams'),
    { ssr: false }
  )
  ```
- Keep animated components as **leaves** — don't wrap Server Components inside them

### Composition Pattern
```tsx
// ✅ Server Component page with animated client leaves
export default async function LandingPage() {
  const features = await getFeatures() // Server-side fetch
  
  return (
    <>
      <Suspense fallback={<Skeleton className="h-screen" />}>
        <HeroSection />          {/* Client: Aceternity background */}
      </Suspense>
      <FeatureGrid features={features} />  {/* Server: shadcn cards */}
      <Suspense fallback={<Skeleton className="h-64" />}>
        <TestimonialMarquee />   {/* Client: Magic UI marquee */}
      </Suspense>
    </>
  )
}
```

### Customization Rules
1. **shadcn/ui:** Customize via CVA variants + `cn()`, or create wrappers in `components/custom/`
2. **Magic UI / Aceternity:** Edit source directly — they're copy-paste owned code
3. **mapcn:** Customize map styles via MapLibre style specs on the `styles` prop
4. **Theme:** Always use CSS variables (`--primary`, `--muted`, etc.) — never hardcode colors
5. **shadcn Studio:** Use the extension for visual theme editing and live preview

## Common Recipes

### Landing Page Stack
```
Background:    Aceternity → AuroraBackground or BackgroundBeams
Hero text:     Magic UI → TextAnimate or TypingAnimation
CTA button:    Magic UI → ShimmerButton or RainbowButton
Features:      Magic UI → BentoGrid + shadcn/ui Cards
Testimonials:  Magic UI → Marquee + shadcn/ui Avatar
Pricing:       shadcn/ui → Card + Table
Footer nav:    shadcn/ui → NavigationMenu
```

### Dashboard Stack
```
Layout:        shadcn/ui → Sidebar + Tabs + Breadcrumb
Data tables:   shadcn/ui → DataTable (TanStack)
Charts:        shadcn/ui → Charts (Recharts)
Maps:          mapcn → Map + MapMarker + MapPopup
Numbers:       Magic UI → NumberTicker
Loading:       Magic UI → AnimatedList
Forms:         shadcn/ui → Form + React Hook Form + Zod
```

## Pre-Flight Checklist

Before creating any UI component:
- [ ] Checked shadcn/ui via MCP (has it already?)
- [ ] Checked project `components/ui/` (already installed?)
- [ ] If animation needed → checked Magic UI catalog
- [ ] If premium effect needed → checked Aceternity catalog
- [ ] If map needed → checked mapcn
- [ ] Component is Client only if it uses hooks/motion
- [ ] Heavy animation uses `next/dynamic` with `ssr: false`
- [ ] Colors use theme CSS variables
- [ ] Responsive tested (mobile-first)
