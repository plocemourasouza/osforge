# Visual Planner (Plan → Interactive HTML)

**Trigger:** Visualizar plano, breakdown visual, transformar spec em HTML, apresentar PRD visualmente, gerar HTML interativo, tornar spec mais fácil de seguir.

---

## Purpose

Camada de apresentação do pipeline de planejamento. Transforma qualquer documento de planejamento em um breakdown HTML single-page interativo.

---

## Supported Formats

| Format | Detected By |
|--------|-------------|
| `osforge-prd` | `type: prd` in frontmatter |
| `osforge-spec` | `type: spec` in frontmatter |
| `osforge-architecture` | `type: architecture` in frontmatter |
| `osforge-epic` | `type: epic` in frontmatter |
| `osforge-phase-context` | `type: phase-context` in frontmatter |
| **Generic markdown** | Any .md file |

---

## Visual Components

1. **Scroll-based navigation** — Sticky sidebar with section links
2. **Reveal animations** — Content fades in on scroll
3. **Flow diagrams** — Visual process flows
4. **Expandable cards** — Collapse/expand details
5. **Stat badges** — Key metrics highlighted
6. **Dependency graphs** — Task dependencies
7. **Status indicators** — Progress tracking
8. **Review system** — Comment and feedback
9. **Clipboard output** — Copy sections easily
10. **Responsive layout** — Works on all devices
11. **Dark mode** — System preference
12. **Print-friendly** — Clean print styles
13. **Search** — Find content quickly

---

## Design System

```css
/* Typography */
--font-heading: 'Bricolage Grotesque', sans-serif;
--font-body: 'DM Sans', sans-serif;

/* Colors (warm palette) */
--color-primary: #E07A5F;
--color-secondary: #3D405B;
--color-accent: #81B29A;
--color-background: #F4F1DE;
--color-text: #1A1A1A;
```

---

## Usage

```bash
# Generate HTML from spec
visual-planner generate docs/specs/auth-feature.md -o auth-visual.html

# With custom template
visual-planner generate docs/specs/auth-feature.md \
  --template custom.html \
  -o auth-visual.html
```

---

## Review System

Built-in review workflow:

1. **Read section** → Understand content
2. **Add comment** → Click to annotate
3. **Copy to clipboard** → Export feedback
4. **Iterate** → Update source, regenerate

---

## Integration

### From Spec Builder
```bash
# After spec is complete
visual-planner generate .specs/features/auth/spec.md
```

### CI/CD
```yaml
# Generate visual for PRs
- name: Generate Visual Plan
  run: |
    visual-planner generate docs/specs/*.md -o public/plans/
```

---

## Zero Dependencies

Only requires Google Fonts (loaded via CDN). No JavaScript frameworks, no build step. Single HTML file output.
