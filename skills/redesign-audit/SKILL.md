---
name: redesign-audit
description: >
  Audita projeto existente, identifica padrões AI-genéricos, e aplica upgrades
  cirúrgicos sem quebrar funcionalidade. ACIONE quando: usuário pede "redesenhar",
  "melhorar design atual", "upgrade visual", "modernizar UI", "tirar cara de AI",
  "site parece template", "deixar mais premium", "auditar e arrumar design".
  Funciona com QUALQUER stack (Tailwind, vanilla CSS, styled-components, etc).
version: 1.0.0
inspired_by: Leonxlnx/taste-skill (redesign-skill) — MIT, 10k+ stars
metadata:
  source: "Leonxlnx/taste-skill"
  category: "frontend-quality"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Redesign Audit — Upgrade Existing Projects to Premium

> Different from `ui-audit` (which is review-only). This skill **audits AND applies fixes**
> working with the existing stack — no rewrites.

## How This Works

```
1. SCAN     → Read codebase. Identify framework, styling method, current patterns.
2. DIAGNOSE → Run audit below. List every generic pattern + missing state.
3. FIX      → Apply targeted upgrades. Do NOT rewrite from scratch.
```

## The Audit (run through each section)

### Typography
- Browser defaults or Inter everywhere → swap to Geist, Outfit, Cabinet Grotesk, or Satoshi.
  For editorial: serif header + sans body.
- Headlines lack presence → increase display size, tighten letter-spacing, reduce line-height.
- Body text too wide → limit to ~65 characters per line. Increase line-height for readability.
- Only Regular(400)+Bold(700) used → add Medium(500) and SemiBold(600) for subtle hierarchy.
- Numbers in proportional font → use mono OR `font-variant-numeric: tabular-nums`.
- Missing letter-spacing adjustments → negative tracking for large headers, positive for small caps.
- All-caps subheaders everywhere → try lowercase italics, sentence case, or small-caps.
- Orphaned words → fix with `text-wrap: balance` or `text-wrap: pretty`.

### Color and Surfaces
- Pure `#000000` bg → replace with `#0a0a0a`, `#121212`, or dark navy.
- Oversaturated accents → keep saturation < 80%.
- More than one accent → pick one, remove rest.
- Mixing warm and cool grays → stick to one family.
- Purple/blue "AI gradient" → most common AI fingerprint. Replace with neutral base + single accent.
- Generic `box-shadow` (pure black) → tint shadow to match background hue.
- Flat zero-texture design → add subtle noise, grain, or micro-patterns.
- Perfectly even linear 45° gradients → use radial, mesh, or noise overlays.
- Inconsistent lighting direction → single consistent light source for all shadows.
- Random dark section in light page (or vice versa) → looks like copy-paste accident. Commit
  to one mode OR shift slightly within the same palette.
- Empty flat sections with no depth → add background imagery, subtle patterns, ambient gradients.
  Use `https://picsum.photos/seed/{name}/1920/1080` when no real assets.

### Layout
- Everything centered + symmetrical → break with offset margins, mixed aspect ratios.
- 3 equal card columns → most generic AI layout. Replace with 2-col zig-zag, asymmetric grid,
  horizontal scroll, or masonry.
- `height: 100vh` → replace with `min-height: 100dvh` (iOS Safari viewport bug).
- Complex flexbox `calc()` percentage math → use CSS Grid.
- No max-width container → add `1200-1440px` container with auto margins.
- Forced equal-height cards (flexbox) → allow variable heights or use masonry.
- Uniform border-radius everywhere → vary it (tighter inside, softer on containers).
- No overlap or depth → use negative margins for layering.
- Symmetrical vertical padding → bottom often needs slightly larger optically.
- Dashboard with mandatory left sidebar → try top nav, command menu, or collapsible panel.
- Missing whitespace → double the spacing.
- Buttons not bottom-aligned in card groups → pin to bottom for clean horizontal line.
- Feature lists at different Y positions in pricing tables → align titles/prices/lists across cols.
- Inconsistent vertical rhythm side-by-side → align shared elements across all items.
- Mathematical alignment that looks optically wrong → manual 1-2px optical adjustments.

### Interactivity and States
- No hover states → add background shift, scale, or translate.
- No active/pressed feedback → `scale(0.98)` or `translateY(1px)` on `:active`.
- Zero transition duration → add 200-300ms to interactive elements.
- Missing focus ring → visible focus indicators (accessibility requirement).
- No loading states → skeleton loaders matching layout (NOT generic circular spinners).
- No empty states → composed "getting started" view.
- No error states → clear inline error messages. NO `window.alert()`.
- Dead links (`href="#"`) → link real destinations or visually disable.
- No active nav indicator → style current page differently.
- Scroll jumping → add `scroll-behavior: smooth`.
- Animations on `top/left/width/height` → switch to `transform`/`opacity`.

### Content
- Generic names: "John Doe", "Jane Smith" → diverse realistic names.
- Fake round numbers: `99.99%`, `50%`, `$100.00` → use `47.2%`, `$99`, `+1 (312) 847-1928`.
- Placeholder companies: "Acme", "Nexus", "SmartFlow" → invent contextual believable brands.
- AI cliché copywriting: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve",
  "Tapestry", "In the world of..." → write plain specific language.
- Exclamation marks in success messages → remove.
- "Oops!" errors → be direct ("Connection failed. Please try again.").
- Passive voice → use active ("We couldn't save your changes").
- All blog dates identical → randomize.
- Same avatar reused → unique assets per person.
- Lorem Ipsum → real draft copy.
- `Title Case On Every Header` → sentence case.

### Component Patterns
- Generic card (border + shadow + white bg) → remove border, or use only bg, or only spacing.
  Cards only when elevation communicates hierarchy.
- Always 1 filled + 1 ghost button → add text links or tertiary styles.
- "New"/"Beta" pill badges → try square badges, flags, or plain text labels.
- Accordion FAQ → try side-by-side, searchable help, or inline progressive disclosure.
- 3-card carousel testimonials with dots → masonry wall, embedded social, or rotating quote.
- Pricing table 3 towers → highlight recommended with color, not just height.
- Modals for everything → inline editing, slide-overs, or expandable sections.
- Avatar circles exclusively → try squircles or rounded squares.
- Sun/moon toggle always → dropdown, system preference, or in settings.
- Footer 4-column link farm → simplify to main paths + legally required.

### Iconography
- Lucide/Feather exclusively → use Phosphor, Heroicons, or custom.
- Cliché metaphors (rocket=launch, shield=security) → replace with less obvious icons
  (bolt, fingerprint, spark, vault).
- Inconsistent stroke widths → standardize to one weight.
- Missing favicon → always include branded favicon.
- Stock "diverse team" photos → real team photos or consistent illustration.

### Code Quality
- Div soup → use `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`.
- Inline styles mixed with classes → move to styling system.
- Hardcoded pixel widths → use `%`, `rem`, `em`, `max-width`.
- Missing alt text → describe meaningfully. Never `alt=""` on meaningful images.
- Arbitrary `z-index: 9999` → establish clean z-index scale.
- Commented dead code → remove before shipping.
- Import hallucinations → check `package.json` for actual existence.
- Missing `<title>`, `description`, `og:image`, social meta → add proper meta tags.

### Strategic Omissions (what AI typically forgets)
- No privacy/terms links → add in footer.
- No "back" navigation → every page needs a way back.
- No custom 404 → design helpful branded page.
- No form validation → client-side validation for emails/required/format.
- No "skip to content" link → essential for keyboard users.
- No cookie consent (if jurisdiction requires) → compliant banner.

## Upgrade Techniques (high-impact replacements)

### Typography
- Variable font weight/width animation on scroll/hover
- Outlined → fill text transitions
- Text mask reveals (massive type as window to video/imagery behind)

### Layout
- Broken grid / asymmetry (overlapping, bleeding, calculated randomness)
- Whitespace maximization for single-element focus
- Parallax card stacks (sticky + physical stacking on scroll)
- Split-screen scroll (opposing directions)

### Motion
- Smooth scroll with inertia (cinematic decoupled scroll)
- Staggered entry (Y-axis + opacity cascade, never mount all at once)
- Spring physics replacing linear easing
- Scroll-driven reveals through masks/wipes/draw-on SVG paths

### Surfaces
- True glassmorphism (1px inner border + inner shadow for edge refraction)
- Spotlight borders (illuminate under cursor)
- Grain/noise overlays (fixed pointer-events-none)
- Colored tinted shadows (background hue, not generic black)

## Fix Priority (for max impact / min risk)

```
1. FONT SWAP                  ← biggest instant lift, lowest risk
2. COLOR PALETTE CLEANUP      ← remove clashing/oversaturated
3. HOVER/ACTIVE STATES        ← makes interface feel alive
4. LAYOUT + SPACING           ← proper grid, max-width, consistent padding
5. REPLACE GENERIC COMPONENTS ← swap clichés for modern alternatives
6. LOADING/EMPTY/ERROR STATES ← makes it feel finished
7. TYPOGRAPHY SCALE POLISH    ← premium final touch
```

## Rules

- Work with existing stack. Do NOT migrate frameworks or styling libs.
- Do NOT break existing functionality. Test after each change.
- Before importing any new library: check `package.json` first.
- Tailwind users: check v3 vs v4 before modifying config.
- No framework: use vanilla CSS.
- Keep changes reviewable + focused. Small targeted improvements over big rewrites.
- After each upgrade: run `ui-audit` skill to verify accessibility + performance not regressed.

---

## Related Skills
- `ui-audit` — 6-pillar review (run AFTER applying redesign-audit fixes)
- `taste-design-dials` — premium design rules to apply during upgrade
- `aesthetic-modes` — pick a mode to align upgrades with
- `accessibility` — WCAG 2.1 compliance check
- `aesthetic-boost` — anti-AI-slop primer (always-active context)
