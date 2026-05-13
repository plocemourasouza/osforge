# Accessibility (WCAG 2.1)

**Trigger:** WCAG, a11y, screen reader, accessibility, keyboard navigation

---

## Core Principles (POUR)

- **P**erceivable — Information must be presentable
- **O**perable — Interface must be usable
- **U**nderstandable — Content must be comprehensible
- **R**obust — Content must work with assistive tech

---

## Semantic HTML

```tsx
// GOOD - Semantic elements
<nav>
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

<main>
  <article>
    <header>
      <h1>Article Title</h1>
    </header>
    <section>...</section>
  </article>
</main>

<aside>Related content</aside>

<footer>...</footer>

// BAD - Div soup
<div class="nav">
  <div class="nav-item" onclick="...">Home</div>
</div>
```

### Button vs Link
```tsx
// Button: triggers action
<button onClick={handleSubmit}>Submit</button>

// Link: navigates somewhere
<a href="/about">About</a>

// BAD
<div onClick={handleSubmit}>Submit</div>  // Not focusable, no keyboard
<a onClick={handleAction}>Do thing</a>    // Link that doesn't navigate
```

---

## Images

```tsx
// Meaningful image - descriptive alt
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2" />

// Decorative image - hide from screen readers
<img src="decorative.png" alt="" role="presentation" />
// Or in Next.js Image
<Image src="/bg.jpg" alt="" aria-hidden="true" />

// Complex image - long description
<figure>
  <img src="diagram.png" alt="Network architecture diagram" />
  <figcaption>
    Detailed description of the network architecture...
  </figcaption>
</figure>
```

---

## Forms

```tsx
// Labels are required
<label htmlFor="email">Email</label>
<input id="email" type="email" name="email" />

// Or implicit label
<label>
  Email
  <input type="email" name="email" />
</label>

// Error messages
<input
  id="email"
  type="email"
  aria-invalid={hasError}
  aria-describedby="email-error"
/>
{hasError && (
  <span id="email-error" role="alert">
    Please enter a valid email
  </span>
)}

// Required fields
<label htmlFor="name">
  Name <span aria-hidden="true">*</span>
</label>
<input id="name" required aria-required="true" />
```

---

## Focus Management

```tsx
// Visible focus indicator (don't remove!)
// In CSS
:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}

// Skip link
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>

// Focus trap for modals
import { FocusTrap } from '@headlessui/react'

<Dialog>
  <FocusTrap>
    <DialogContent>...</DialogContent>
  </FocusTrap>
</Dialog>

// Programmatic focus
const inputRef = useRef<HTMLInputElement>(null)
useEffect(() => {
  inputRef.current?.focus()
}, [isOpen])
```

---

## Color Contrast

| Element | Minimum Ratio |
|---------|---------------|
| Normal text | 4.5:1 |
| Large text (18px+ or 14px bold) | 3:1 |
| UI components & graphics | 3:1 |

```tsx
// Use tools to check
// - Chrome DevTools → Elements → Styles → Color picker
// - WebAIM Contrast Checker
// - axe DevTools

// Don't rely on color alone
// BAD
<span style={{ color: 'red' }}>Error</span>

// GOOD
<span style={{ color: 'red' }}>
  <ErrorIcon aria-hidden="true" /> Error: Invalid input
</span>
```

---

## Keyboard Navigation

```tsx
// Interactive elements must be keyboard accessible
// Tab: Move focus
// Enter/Space: Activate
// Arrow keys: Navigate within components
// Escape: Close/cancel

// Tab order follows DOM order
// Use tabindex carefully
tabIndex={0}   // Make focusable
tabIndex={-1}  // Programmatically focusable only
// Never use tabIndex > 0

// Custom keyboard handling
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick()
    }
  }}
>
  Custom Button
</div>
```

---

## ARIA Attributes

```tsx
// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Expanded/collapsed
<button aria-expanded={isOpen} aria-controls="menu">
  Menu
</button>
<ul id="menu" hidden={!isOpen}>...</ul>

// Loading states
<button aria-busy={isLoading} disabled={isLoading}>
  {isLoading ? 'Loading...' : 'Submit'}
</button>

// Roles
role="alert"        // Important, time-sensitive
role="status"       // Status updates
role="dialog"       // Modal dialogs
role="navigation"   // Navigation regions
role="tablist"      // Tab interfaces
```

---

## Testing

### Automated
```bash
# Lighthouse accessibility audit
npx lighthouse https://example.com --only-categories=accessibility

# axe-core
npx @axe-core/cli https://example.com

# In tests
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

test('has no accessibility violations', async () => {
  const { container } = render(<MyComponent />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### Manual
1. **Keyboard only**: Navigate without mouse
2. **Screen reader**: Test with VoiceOver/NVDA
3. **Zoom**: Test at 200% zoom
4. **Color**: Check contrast, colorblind simulation
5. **Motion**: Respect `prefers-reduced-motion`

---

## Screen Reader Only Text

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

```tsx
// Usage
<button>
  <TrashIcon aria-hidden="true" />
  <span className="sr-only">Delete item</span>
</button>
```
