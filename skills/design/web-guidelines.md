# Web Design Guidelines

**Trigger:** web design, UI guidelines, design compliance, design review

---

## Layout Principles

### Content Width
```css
.container {
  max-width: 1280px;     /* Content max */
  padding-inline: 1rem;  /* Mobile padding */
}

@media (min-width: 640px) {
  .container {
    padding-inline: 2rem;
  }
}

/* Text-heavy content */
.prose {
  max-width: 65ch;  /* Optimal line length */
}
```

### Grid System
```tsx
// 12-column grid
<div className="grid grid-cols-12 gap-6">
  <aside className="col-span-3">Sidebar</aside>
  <main className="col-span-9">Content</main>
</div>

// Responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

---

## Consistency Checklist

### Spacing
- [ ] Consistent padding/margin scale (4, 8, 16, 24, 32, 48...)
- [ ] Equal spacing between similar elements
- [ ] Adequate whitespace around content blocks

### Typography
- [ ] Max 2 font families
- [ ] Consistent heading hierarchy
- [ ] Body text 16px minimum
- [ ] Line length 45-75 characters
- [ ] Adequate line height (1.5-1.6 for body)

### Colors
- [ ] Defined color palette (primary, secondary, neutral)
- [ ] Consistent semantic colors (success, error, warning)
- [ ] Dark mode colors tested
- [ ] All text passes contrast requirements

### Components
- [ ] Buttons have consistent sizing
- [ ] Form elements have uniform styling
- [ ] Cards follow same pattern
- [ ] Icons are consistent size/style

---

## Form Design

### Labels
```tsx
// Always use labels
<label className="text-sm font-medium" htmlFor="email">
  Email
</label>
<input id="email" type="email" />

// Required indicator
<label>
  Name <span className="text-destructive">*</span>
</label>
```

### Error States
```tsx
<div>
  <label htmlFor="email">Email</label>
  <input
    id="email"
    className={cn(
      "border",
      hasError && "border-destructive focus:ring-destructive"
    )}
    aria-invalid={hasError}
    aria-describedby="email-error"
  />
  {hasError && (
    <p id="email-error" className="text-sm text-destructive mt-1">
      Please enter a valid email
    </p>
  )}
</div>
```

### Form Layout
```tsx
// Vertical (default, best for mobile)
<form className="space-y-4">
  <div>
    <label>Name</label>
    <input />
  </div>
  <div>
    <label>Email</label>
    <input />
  </div>
</form>

// Horizontal (wider screens)
<form>
  <div className="grid grid-cols-2 gap-4">
    <div>
      <label>First Name</label>
      <input />
    </div>
    <div>
      <label>Last Name</label>
      <input />
    </div>
  </div>
</form>
```

---

## Interactive States

### Buttons
```css
/* Default */
.btn { background: var(--primary); }

/* Hover */
.btn:hover { background: var(--primary-dark); }

/* Focus */
.btn:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}

/* Active/Pressed */
.btn:active { transform: scale(0.98); }

/* Disabled */
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading */
.btn[data-loading] {
  cursor: wait;
  opacity: 0.8;
}
```

### Links
```css
a {
  color: var(--primary);
  text-decoration: underline;
  text-underline-offset: 2px;
}

a:hover {
  text-decoration: none;
}

a:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}
```

---

## Loading States

### Skeleton Loading
```tsx
// Preserve layout during loading
function CardSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-48 bg-muted rounded-t-lg" />
      <div className="p-4 space-y-3">
        <div className="h-4 bg-muted rounded w-3/4" />
        <div className="h-4 bg-muted rounded w-1/2" />
      </div>
    </div>
  )
}
```

### Button Loading
```tsx
<button disabled={isLoading}>
  {isLoading ? (
    <>
      <Spinner className="mr-2 animate-spin" />
      Loading...
    </>
  ) : (
    'Submit'
  )}
</button>
```

---

## Empty States

```tsx
function EmptyState({ title, description, action }) {
  return (
    <div className="text-center py-12">
      <EmptyIcon className="mx-auto h-12 w-12 text-muted-foreground" />
      <h3 className="mt-4 text-lg font-medium">{title}</h3>
      <p className="mt-2 text-muted-foreground">{description}</p>
      {action && (
        <Button className="mt-6">{action}</Button>
      )}
    </div>
  )
}

// Usage
<EmptyState
  title="No projects yet"
  description="Get started by creating your first project."
  action="Create Project"
/>
```

---

## Error States

```tsx
// Page-level error
function ErrorPage({ error, reset }) {
  return (
    <div className="text-center py-12">
      <AlertCircle className="mx-auto h-12 w-12 text-destructive" />
      <h2 className="mt-4 text-lg font-medium">Something went wrong</h2>
      <p className="mt-2 text-muted-foreground">{error.message}</p>
      <Button onClick={reset} className="mt-6">
        Try again
      </Button>
    </div>
  )
}

// Inline error
function InlineError({ message }) {
  return (
    <div className="flex items-center gap-2 text-sm text-destructive">
      <AlertCircle className="h-4 w-4" />
      {message}
    </div>
  )
}
```

---

## Design Review Checklist

Before shipping:

- [ ] **Responsive**: Works on mobile (375px), tablet (768px), desktop
- [ ] **Consistent**: Spacing, colors, typography follow system
- [ ] **Accessible**: Contrast, focus states, semantic HTML
- [ ] **States**: Loading, empty, error states implemented
- [ ] **Interactive**: Hover, focus, active states defined
- [ ] **Performance**: Images optimized, lazy loading
- [ ] **Dark mode**: If supported, fully tested
