# Frontend Design

**Trigger:** design system, color theory, typography, animation, UX

---

## Color Systems

### HSL-Based Design
```css
:root {
  /* Primary - adjust hue for different colors */
  --primary-h: 220;
  --primary-s: 90%;
  --primary-l: 50%;

  --primary: hsl(var(--primary-h), var(--primary-s), var(--primary-l));
  --primary-light: hsl(var(--primary-h), var(--primary-s), 70%);
  --primary-dark: hsl(var(--primary-h), var(--primary-s), 30%);
}
```

### Semantic Colors
```css
:root {
  /* Brand */
  --primary: hsl(220, 90%, 50%);
  --secondary: hsl(280, 80%, 50%);

  /* Feedback */
  --success: hsl(142, 76%, 36%);
  --warning: hsl(38, 92%, 50%);
  --error: hsl(0, 84%, 60%);
  --info: hsl(199, 89%, 48%);

  /* Neutral */
  --background: hsl(0, 0%, 100%);
  --foreground: hsl(0, 0%, 9%);
  --muted: hsl(0, 0%, 96%);
  --muted-foreground: hsl(0, 0%, 45%);
  --border: hsl(0, 0%, 90%);
}

/* Dark mode */
.dark {
  --background: hsl(0, 0%, 9%);
  --foreground: hsl(0, 0%, 95%);
  /* ... */
}
```

---

## Typography

### Type Scale (Major Third - 1.25)
```css
:root {
  --text-xs: 0.64rem;    /* 10.24px */
  --text-sm: 0.8rem;     /* 12.8px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.25rem;    /* 20px */
  --text-xl: 1.563rem;   /* 25px */
  --text-2xl: 1.953rem;  /* 31.25px */
  --text-3xl: 2.441rem;  /* 39px */
  --text-4xl: 3.052rem;  /* 48.8px */
}
```

### Font Pairing
```
Headings: Inter, Satoshi, Cabinet Grotesk
Body: Inter, Source Sans, Open Sans

Rule: Max 2 fonts per project
```

### Line Height
```css
/* Tighter for headings */
h1, h2, h3 {
  line-height: 1.2;
}

/* Comfortable for body */
p, li {
  line-height: 1.6;
}
```

---

## Spacing

### 8px Grid System
```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
}
```

### Consistent Spacing
```tsx
// Use spacing scale consistently
<Card className="p-6">        {/* 24px padding */}
  <CardHeader className="mb-4"> {/* 16px margin */}
    ...
  </CardHeader>
  <CardContent className="space-y-4"> {/* 16px gap */}
    ...
  </CardContent>
</Card>
```

---

## Animation

### Timing Functions
```css
:root {
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

### Duration Guidelines
| Type | Duration |
|------|----------|
| Micro-interactions | 100-200ms |
| Transitions | 200-300ms |
| Page transitions | 300-500ms |
| Complex animations | 500-1000ms |

### Entrance Animations
```tsx
// Fade in
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.2 }}
>

// Slide up
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3, ease: 'easeOut' }}
>

// Scale
<motion.div
  initial={{ opacity: 0, scale: 0.95 }}
  animate={{ opacity: 1, scale: 1 }}
  transition={{ duration: 0.2 }}
>
```

### Respect User Preferences
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Shadows & Depth

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
}

/* Elevation levels */
.card { box-shadow: var(--shadow-md); }
.dropdown { box-shadow: var(--shadow-lg); }
.modal { box-shadow: var(--shadow-xl); }
```

---

## Component Patterns

### Card
```tsx
<div className="rounded-lg border bg-card p-6 shadow-sm">
  <div className="space-y-4">
    <h3 className="text-lg font-semibold">Title</h3>
    <p className="text-muted-foreground">Description</p>
  </div>
</div>
```

### Button Variants
```tsx
// Primary
<button className="bg-primary text-primary-foreground hover:bg-primary/90">

// Secondary
<button className="bg-secondary text-secondary-foreground hover:bg-secondary/80">

// Outline
<button className="border border-input bg-background hover:bg-accent">

// Ghost
<button className="hover:bg-accent hover:text-accent-foreground">

// Destructive
<button className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
```

### Input
```tsx
<input className="
  h-10 w-full rounded-md border border-input
  bg-background px-3 py-2 text-sm
  placeholder:text-muted-foreground
  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
  disabled:cursor-not-allowed disabled:opacity-50
" />
```

---

## Visual Hierarchy

1. **Size**: Larger = more important
2. **Color**: High contrast = important
3. **Weight**: Bolder = important
4. **Space**: More whitespace = more attention
5. **Position**: Top-left (LTR) gets seen first

```tsx
// Clear hierarchy
<article>
  <h1 className="text-4xl font-bold mb-2">Main Title</h1>
  <p className="text-muted-foreground mb-8">Subtitle or meta</p>
  <div className="prose">
    <p>Body content...</p>
  </div>
</article>
```
