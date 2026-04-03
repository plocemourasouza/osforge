# Design System Reference

Complete CSS design tokens for the visual breakdown. Copy this entire `:root` block into the HTML and adapt the accent color to suit the project's personality.

## Table of Contents
1. [Color Palette](#color-palette)
2. [Typography](#typography)
3. [Spacing & Layout](#spacing--layout)
4. [Shadows & Depth](#shadows--depth)
5. [Animations & Transitions](#animations--transitions)
6. [Navigation & Progress](#navigation--progress)
7. [Section Structure](#section-structure)
8. [Responsive Breakpoints](#responsive-breakpoints)
9. [Scrollbar & Background](#scrollbar--background)
10. [Code Blocks](#code-blocks)

---

## Color Palette

```css
:root {
  /* --- BACKGROUNDS --- */
  --color-bg:             #FAF7F2;       /* warm off-white, like aged paper */
  --color-bg-warm:        #F5F0E8;       /* slightly warmer for alternating sections */
  --color-bg-code:        #1E1E2E;       /* deep indigo-charcoal for code blocks */
  --color-text:           #2C2A28;       /* dark charcoal, easy on eyes */
  --color-text-secondary: #6B6560;       /* warm gray for secondary text */
  --color-text-muted:     #9E9790;       /* muted for labels, badges */
  --color-border:         #E5DFD6;       /* subtle warm border */
  --color-border-light:   #EEEBE5;       /* even lighter border */
  --color-surface:        #FFFFFF;       /* card surfaces */
  --color-surface-warm:   #FDF9F3;       /* warm card surface */

  /* --- ACCENT (adapt per project — pick ONE bold color) ---
     Default: vermillion. Alternatives: coral (#E06B56), teal (#2A7B9B),
     amber (#D4A843), forest (#2D8B55). Avoid purple gradients. */
  --color-accent:         #D94F30;
  --color-accent-hover:   #C4432A;
  --color-accent-light:   #FDEEE9;
  --color-accent-muted:   #E8836C;

  /* --- SEMANTIC --- */
  --color-success:        #2D8B55;
  --color-success-light:  #E8F5EE;
  --color-error:          #C93B3B;
  --color-error-light:    #FDE8E8;
  --color-info:           #2A7B9B;
  --color-info-light:     #E4F2F7;

  /* --- SECTION COLORS (assign to major parts of the plan) ---
     Each major component/phase gets a distinct color for diagrams and cards */
  --color-section-1:      #D94F30;       /* vermillion */
  --color-section-2:      #2A7B9B;       /* teal */
  --color-section-3:      #7B6DAA;       /* muted plum */
  --color-section-4:      #D4A843;       /* golden */
  --color-section-5:      #2D8B55;       /* forest */
}
```

**Rules:**
- Even-numbered sections use `--color-bg`, odd-numbered use `--color-bg-warm` (alternating backgrounds create visual rhythm)
- Section colors should be visually distinct for flow diagrams and cards
- Code blocks always use `--color-bg-code` with light text

---

## Typography

```css
:root {
  /* --- FONTS ---
     Display: bold, geometric, personality-driven. NOT Inter/Roboto/Arial.
     Body: readable with character. NOT system fonts.
     Mono: developer-friendly with clear character distinction. */
  --font-display:  'Bricolage Grotesque', Georgia, serif;
  --font-body:     'DM Sans', -apple-system, sans-serif;
  --font-mono:     'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

  /* --- TYPE SCALE (1.25 ratio) --- */
  --text-xs:   0.75rem;    /* 12px — labels, badges */
  --text-sm:   0.875rem;   /* 14px — secondary text, code */
  --text-base: 1rem;       /* 16px — body text */
  --text-lg:   1.125rem;   /* 18px — lead paragraphs */
  --text-xl:   1.25rem;    /* 20px — screen headings */
  --text-2xl:  1.5rem;     /* 24px — sub-section titles */
  --text-3xl:  1.875rem;   /* 30px — section subtitles */
  --text-4xl:  2.25rem;    /* 36px — section titles */
  --text-5xl:  3rem;       /* 48px — hero text */
  --text-6xl:  3.75rem;    /* 60px — section numbers */

  /* --- LINE HEIGHTS --- */
  --leading-tight:  1.15;  /* headings */
  --leading-snug:   1.3;   /* subheadings */
  --leading-normal: 1.6;   /* body text */
  --leading-loose:  1.8;   /* relaxed reading */
}
```

**Google Fonts link (put in `<head>`):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400;1,9..40,500&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

**Rules:**
- Section numbers: `--text-6xl`, font-display, weight 800, `--color-accent` with 15% opacity
- Section titles: `--text-4xl`, font-display, weight 700
- Sub-headings: `--text-xl` or `--text-2xl`, font-display, weight 600
- Body text: `--text-base` or `--text-lg`, font-body, `--leading-normal`
- Code: `--text-sm`, font-mono
- Labels/badges: `--text-xs`, font-mono, uppercase, letter-spacing 0.05em

---

## Spacing & Layout

```css
:root {
  --space-1:  0.25rem;   /* 4px */
  --space-2:  0.5rem;    /* 8px */
  --space-3:  0.75rem;   /* 12px */
  --space-4:  1rem;      /* 16px */
  --space-5:  1.25rem;   /* 20px */
  --space-6:  1.5rem;    /* 24px */
  --space-8:  2rem;      /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-20: 5rem;      /* 80px */
  --space-24: 6rem;      /* 96px */

  --content-width:      800px;   /* standard reading width */
  --content-width-wide: 1000px;  /* for flow diagrams and side-by-side layouts */
  --nav-height:         50px;
  --radius-sm:  8px;
  --radius-md:  12px;
  --radius-lg:  16px;
  --radius-full: 9999px;
}
```

**Section layout:**
```css
.section {
  min-height: 100dvh;       /* fallback: 100vh */
  scroll-snap-align: start;
  padding: var(--space-16) var(--space-6);
  padding-top: calc(var(--nav-height) + var(--space-12));
}
.section-content {
  max-width: var(--content-width);
  margin: 0 auto;
}
```

---

## Shadows & Depth

```css
:root {
  --shadow-sm:  0 1px 2px rgba(44, 42, 40, 0.05);
  --shadow-md:  0 4px 12px rgba(44, 42, 40, 0.08);
  --shadow-lg:  0 8px 24px rgba(44, 42, 40, 0.1);
  --shadow-xl:  0 16px 48px rgba(44, 42, 40, 0.12);
}
```

Use warm-tinted RGBA (44, 42, 40) — never pure black shadows.

---

## Animations & Transitions

```css
:root {
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast:   150ms;
  --duration-normal: 300ms;
  --duration-slow:   500ms;
  --stagger-delay:   120ms;
}
```

**Scroll-triggered reveal pattern:**
```css
.animate-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity var(--duration-slow) var(--ease-out),
              transform var(--duration-slow) var(--ease-out);
}
.animate-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger children */
.stagger-children > .animate-in {
  transition-delay: calc(var(--stagger-index, 0) * var(--stagger-delay));
}
```

**JS for stagger indexes:**
```javascript
document.querySelectorAll('.stagger-children').forEach(parent => {
  Array.from(parent.children).forEach((child, i) => {
    child.style.setProperty('--stagger-index', i);
  });
});
```

**Intersection Observer (trigger reveals):**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });

document.querySelectorAll('.animate-in').forEach(el => observer.observe(el));
```

---

## Navigation & Progress

**HTML structure:**
```html
<nav class="nav">
  <div class="progress-bar" role="progressbar" aria-valuenow="0"></div>
  <div class="nav-inner">
    <span class="nav-title">Plan Title</span>
    <div class="nav-dots">
      <button class="nav-dot" data-target="section-1" data-tooltip="Section 1 Name"
              role="tab" aria-label="Section 1"></button>
      <!-- one per section -->
    </div>
  </div>
</nav>
```

**CSS:**
```css
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--nav-height);
  background: rgba(250, 247, 242, 0.95);
  backdrop-filter: blur(10px);
  z-index: 100;
  border-bottom: 1px solid var(--color-border-light);
}
.nav-inner {
  max-width: var(--content-width-wide);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 var(--space-6);
}
.nav-title {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: var(--text-sm);
  color: var(--color-text);
}
.progress-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-accent);
  transition: width 100ms linear;
  z-index: 101;
}
.nav-dots {
  display: flex;
  gap: var(--space-3);
}
.nav-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid var(--color-text-muted);
  background: transparent;
  cursor: pointer;
  padding: 0;
  transition: all var(--duration-fast);
}
.nav-dot.active {
  border-color: var(--color-accent);
  background: var(--color-accent);
  box-shadow: 0 0 8px rgba(217, 79, 48, 0.3);
}
.nav-dot.visited {
  background: var(--color-accent);
  border-color: var(--color-accent);
}
```

**Progress bar JS:**
```javascript
const progressBar = document.querySelector('.progress-bar');
function updateProgressBar() {
  const scrollTop = window.scrollY;
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / scrollHeight) * 100;
  progressBar.style.width = progress + '%';
}
window.addEventListener('scroll', () => {
  requestAnimationFrame(updateProgressBar);
}, { passive: true });
```

**Keyboard navigation:**
```javascript
document.addEventListener('keydown', (e) => {
  if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { nextSection(); e.preventDefault(); }
  if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { prevSection(); e.preventDefault(); }
});
```

**Dot click navigation:**
```javascript
document.querySelectorAll('.nav-dot').forEach(dot => {
  dot.addEventListener('click', () => {
    const target = document.getElementById(dot.dataset.target);
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
});
```

**Active dot tracking:**
```javascript
const sections = document.querySelectorAll('.section');
const dots = document.querySelectorAll('.nav-dot');
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const index = Array.from(sections).indexOf(entry.target);
      dots.forEach((d, i) => {
        d.classList.remove('active');
        if (i < index) d.classList.add('visited');
      });
      if (dots[index]) dots[index].classList.add('active');
    }
  });
}, { rootMargin: '-30% 0px -70% 0px' });
sections.forEach(s => sectionObserver.observe(s));
```

---

## Section Structure

**HTML template for each section:**
```html
<section class="section" id="section-N" style="background: var(--color-bg or --color-bg-warm)">
  <div class="section-content">
    <header class="section-header animate-in">
      <span class="section-number">0N</span>
      <h1 class="section-title">Section Title</h1>
      <p class="section-subtitle">One-line description of what this section covers</p>
    </header>

    <div class="section-body">
      <div class="screen animate-in">
        <h2 class="screen-heading">Sub-heading</h2>
        <p>Content...</p>
        <!-- Visual elements: flow diagrams, cards, code blocks, etc. -->
      </div>

      <div class="screen animate-in">
        <!-- Next screen -->
      </div>
    </div>
  </div>
</section>
```

**CSS:**
```css
.section-number {
  font-family: var(--font-display);
  font-size: var(--text-6xl);
  font-weight: 800;
  color: var(--color-accent);
  opacity: 0.15;
  line-height: 1;
  display: block;
  margin-bottom: var(--space-2);
}
.section-title {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: 700;
  line-height: var(--leading-tight);
  color: var(--color-text);
  margin: 0 0 var(--space-3);
}
.section-subtitle {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  line-height: var(--leading-normal);
  margin: 0;
}
.section-header {
  margin-bottom: var(--space-12);
}
.screen {
  margin-bottom: var(--space-10);
}
.screen-heading {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 600;
  margin: 0 0 var(--space-4);
}
```

---

## Responsive Breakpoints

```css
/* Tablet */
@media (max-width: 768px) {
  :root {
    --text-4xl: 1.875rem;
    --text-5xl: 2.25rem;
    --text-6xl: 3rem;
  }
  .flow-diagram { flex-direction: column; }
  .flow-arrow { transform: rotate(90deg); }
  .pattern-cards { grid-template-columns: 1fr 1fr; }
}

/* Mobile */
@media (max-width: 480px) {
  :root {
    --text-4xl: 1.5rem;
    --text-5xl: 1.875rem;
    --text-6xl: 2.25rem;
  }
  .section { padding: var(--space-8) var(--space-4); }
  .pattern-cards { grid-template-columns: 1fr; }
  .flow-steps { flex-direction: column; }
  .flow-arrow { transform: rotate(90deg); }
}
```

---

## Scrollbar & Background

```css
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: var(--radius-full);
}

body {
  background: var(--color-bg);
  background-image: radial-gradient(
    ellipse at 20% 50%,
    rgba(217, 79, 48, 0.03) 0%,
    transparent 50%
  );
  font-family: var(--font-body);
  color: var(--color-text);
  margin: 0;
  line-height: var(--leading-normal);
}

html {
  scroll-snap-type: y proximity;
  scroll-behavior: smooth;
}
```

---

## Code Blocks

All code blocks wrap text — no horizontal scrollbars ever.

```css
pre, code {
  white-space: pre-wrap;
  word-break: break-word;
  overflow-x: hidden;
}

pre {
  background: var(--color-bg-code);
  color: #CDD6F4;
  padding: var(--space-6);
  border-radius: var(--radius-md);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  line-height: 1.7;
  box-shadow: var(--shadow-md);
  margin: var(--space-6) 0;
}
```

**Syntax highlighting (Catppuccin-inspired):**
```css
.code-keyword  { color: #CBA6F7; }  /* purple — if, else, return, function */
.code-string   { color: #A6E3A1; }  /* green — "strings" */
.code-function { color: #89B4FA; }  /* blue — function names */
.code-comment  { color: #6C7086; }  /* muted gray — // comments */
.code-number   { color: #FAB387; }  /* peach — numbers */
.code-property { color: #F9E2AF; }  /* yellow — object keys */
.code-operator { color: #94E2D5; }  /* teal — =, =>, +, etc. */
.code-tag      { color: #F38BA8; }  /* pink — HTML tags */
.code-attr     { color: #F9E2AF; }  /* yellow — HTML attributes */
.code-value    { color: #A6E3A1; }  /* green — attribute values */
```
