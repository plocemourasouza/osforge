# Frontend UI System (shadcn Ecosystem)

**Trigger:** UI, componente, landing, shadcn, Magic UI, Aceternity, dashboard, form, animation

---

## Component Sources (priority order)

### 1. shadcn/ui — Core Primitives
```bash
bunx shadcn@latest add <component>
```
Use Shadcn MCP first to discover components.

### 2. Magic UI — 150+ Animations
```bash
bunx shadcn@latest add "https://magicui.design/r/<component>"
```
Directory: `components/magicui/`

### 3. Aceternity UI — Premium Effects
```bash
bunx shadcn@latest add @aceternity/<component>
```
Directory: `components/aceternity/`

### 4. mapcn — Maps (MapLibre)
```bash
bunx shadcn@latest add "https://mapcn.dev/r/map"
```
Directory: `components/ui/map/`
No API key required.

---

## Decision Matrix

| Need | Source |
|------|--------|
| Forms, tables, nav, dialogs | shadcn/ui |
| Text animation, number ticker | Magic UI |
| Background effects, gradients | Aceternity or Magic UI |
| 3D effects, hover cards | Aceternity |
| Maps, geolocation | mapcn |
| Charts | shadcn/ui (recharts) |

---

## Rules

### Client Components
Magic UI and Aceternity use Framer Motion — always add `"use client"`:
```tsx
"use client"
import { TextReveal } from "@/components/magicui/text-reveal"
```

### Heavy Animations
Use dynamic imports for heavy components:
```tsx
import dynamic from 'next/dynamic'

const HeavyAnimation = dynamic(
  () => import('@/components/aceternity/vortex'),
  { ssr: false }
)
```

### Component Hierarchy
Animated components are leaf nodes — never wrap RSC inside them:
```tsx
// WRONG
<AnimatedCard>
  <ServerComponent /> // Will break
</AnimatedCard>

// CORRECT
<AnimatedCard>
  {children} // Pass as children prop
</AnimatedCard>
```

### Theming
Always use CSS variables, never hardcode colors:
```tsx
// WRONG
<div className="bg-blue-500">

// CORRECT
<div className="bg-primary">
```

---

## Visual Verification Checklist

After implementing visual components, ALWAYS verify:

1. **Layout** — Matches design/spec
2. **Responsiveness**
   - Mobile: 375px
   - Tablet: 768px
   - Desktop: 1280px+
3. **States**
   - Loading
   - Empty
   - Error
   - Success
4. **Accessibility**
   - Tab navigation works
   - Screen reader labels present
   - Contrast ratios pass

NEVER declare a component "working" without visual evidence.

---

## Common Patterns

### Hero Section
```tsx
import { SparklesText } from "@/components/magicui/sparkles-text"
import { Button } from "@/components/ui/button"

export function Hero() {
  return (
    <section className="flex flex-col items-center gap-8 py-24">
      <SparklesText text="Welcome to Our App" />
      <p className="text-muted-foreground max-w-2xl text-center">
        Description here
      </p>
      <Button size="lg">Get Started</Button>
    </section>
  )
}
```

### Dashboard Layout
```tsx
import { SidebarProvider, Sidebar } from "@/components/ui/sidebar"

export function DashboardLayout({ children }) {
  return (
    <SidebarProvider>
      <Sidebar />
      <main className="flex-1 p-6">{children}</main>
    </SidebarProvider>
  )
}
```
