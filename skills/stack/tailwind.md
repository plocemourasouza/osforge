# Tailwind CSS Patterns

**Trigger:** Tailwind, utility classes, responsive design, Tailwind v4, CSS

---

## Tailwind v4 — CSS-First Config

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
  --color-brand-dark: #1d4ed8;
  --font-display: "Inter", sans-serif;
  --breakpoint-3xl: 1920px;
}
```

No more `tailwind.config.js` for basic customization.

---

## Responsive Patterns

### Mobile-First (default)
```tsx
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>
```

### Container Queries (v4)
```tsx
<div className="@container">
  <div className="@sm:flex @lg:grid @lg:grid-cols-2">
    Content adapts to container, not viewport
  </div>
</div>
```

### Common Breakpoints
- `sm:` — 640px+
- `md:` — 768px+
- `lg:` — 1024px+
- `xl:` — 1280px+
- `2xl:` — 1536px+

---

## Color System

### Using CSS Variables (recommended)
```tsx
<div className="bg-primary text-primary-foreground">
  Uses theme colors
</div>
```

### Opacity Modifier
```tsx
<div className="bg-black/50">50% opacity black</div>
<div className="text-white/80">80% opacity white</div>
```

### Dark Mode
```tsx
<div className="bg-white dark:bg-gray-900">
  Automatic dark mode
</div>
```

---

## Typography

### Font Size Scale
```tsx
<p className="text-xs">12px</p>
<p className="text-sm">14px</p>
<p className="text-base">16px</p>
<p className="text-lg">18px</p>
<p className="text-xl">20px</p>
<p className="text-2xl">24px</p>
```

### Font Weight
```tsx
<p className="font-normal">400</p>
<p className="font-medium">500</p>
<p className="font-semibold">600</p>
<p className="font-bold">700</p>
```

### Line Height
```tsx
<p className="leading-tight">1.25</p>
<p className="leading-normal">1.5</p>
<p className="leading-relaxed">1.625</p>
```

---

## Layout Patterns

### Flexbox
```tsx
// Center everything
<div className="flex items-center justify-center">

// Space between
<div className="flex items-center justify-between">

// Stack with gap
<div className="flex flex-col gap-4">
```

### Grid
```tsx
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

// Auto-fit
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
```

### Container
```tsx
<div className="container mx-auto px-4">
  Centered with padding
</div>
```

---

## Animation

### Built-in
```tsx
<div className="animate-spin">Spinning</div>
<div className="animate-pulse">Pulsing</div>
<div className="animate-bounce">Bouncing</div>
```

### Transitions
```tsx
<button className="transition-colors duration-200 hover:bg-primary">
  Smooth hover
</button>

<div className="transition-all duration-300 ease-in-out hover:scale-105">
  Scale on hover
</div>
```

### Custom Animation (v4)
```css
@theme {
  --animate-fade-in: fade-in 0.5s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

```tsx
<div className="animate-fade-in">Fades in</div>
```

---

## Component Extraction

### When to Extract
- Used 3+ times with same classes
- Complex class combinations
- Needs documentation

### Pattern: cn() helper
```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

```tsx
// Usage
<button className={cn(
  "px-4 py-2 rounded-md font-medium",
  "bg-primary text-primary-foreground",
  "hover:bg-primary/90",
  disabled && "opacity-50 cursor-not-allowed"
)}>
  Button
</button>
```

---

## Common Patterns

### Card
```tsx
<div className="rounded-lg border bg-card p-6 shadow-sm">
  Card content
</div>
```

### Input
```tsx
<input className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring" />
```

### Badge
```tsx
<span className="inline-flex items-center rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary">
  Badge
</span>
```

---

## Gotchas

### Don't use string concatenation
```tsx
// BAD - won't be detected by Tailwind
<div className={`text-${size}`}>

// GOOD - use complete class names
<div className={size === 'lg' ? 'text-lg' : 'text-sm'}>
```

### Arbitrary values
```tsx
<div className="top-[117px] w-[calc(100%-2rem)]">
  Custom values when needed
</div>
```
