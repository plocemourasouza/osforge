---
name: design-md
description: >
  PER-PROJECT brand identity contract in a DESIGN.md file — the 9-section
  document (Visual Theme, Color, Typography, Spacing, Layout,
  Components, Motion, Voice & Brand, Anti-patterns) with real hex tokens that an
  agent reads to generate UI consistent with that project's identity.
  Use when: user asks to "create per-project brand identity", "DESIGN.md",
  "project design tokens", "design contract", "project design system",
  "brand tokens", "standardize this project's look", "how this product should
  look", or is starting a new project that needs its own identity.
  Produces/reviews a versionable DESIGN.md in the project repo. Differs from
  aesthetic-modes (3 ready-made moods), ui-design-intelligence (per-industry spec) and
  stitch-design-export (export to Google Stitch): here the deliverable is the
  DESIGN.md CONTRACT itself, with a validatable schema (Lens A/B) and Agent Prompt Guide.
version: 1.0.0
metadata:
  source: "open-design (github.com/nexu-io/open-design), Apache-2.0"
  curated_systems: 15
allowed-tools: Read, Write, Edit, Glob, Grep
---

# design-md — Per-project brand contract

A `DESIGN.md` is the **identity contract of a project**: a single Markdown file,
versioned in the repo, that describes real colors, typography, spacing, components, motion,
voice and anti-patterns — and ends with an **Agent Prompt Guide** that a UI generation agent
consumes directly. It is the missing artifact between "I have a visual mood" and "every
generated component comes out consistent with the brand".

## When to use (and when not)

**Use when** the project needs its own durable identity, citable by hex — a real product
starting from scratch, or an existing one without a brand contract. The deliverable is the
`DESIGN.md` in the project repo.

**Do NOT use for:**
- A ready-made mood among 3 paradigms (minimalist/brutalist/soft) → `aesthetic-modes`.
- A design spec adapted to an industry (fintech/healthcare/saas) → `ui-design-intelligence`.
- Exporting a design system to Google Stitch → `stitch-design-export` / `stitch-design-taste`.
- One-off design decisions (picking a palette, a font) → `frontend-design`.
- Generic aesthetic styles (glassmorphism, bento, neobrutalism) already covered in
  `aesthetic-modes` — do **not** create a DESIGN.md just to reproduce a catalog style.

`design-md` is the level above: it produces the **contract**, not a one-off. The other skills inform
the *content* of the sections; this one defines the *form* and validates it.

## The 9 sections (the schema)

Every `DESIGN.md` has these nine headings, in this order. The parser matches only the prefix `## [digit].`
— text after the number is free (`## 4. Spacing & Grid` is valid).

| # | Section | What it documents |
| --- | --- | --- |
| 1 | **Visual Theme & Atmosphere** | Central metaphor, feeling, use cases, prior art (real products). |
| 2 | **Color** | Real hex + **role** of each color (CTA, surface, text 1/2/3, border, semantics). |
| 3 | **Typography** | Display/body/mono families, scale ≥4 tiers, weights, line-height, tracking + "Font labels" block. |
| 4 | **Spacing** | Base unit, scale, component padding, vertical section rhythm. |
| 5 | **Layout & Composition** | Grid, container max-width, whitespace, border-radius scale. |
| 6 | **Components** | Real CSS for 3-6 components, 100% via semantic tokens. |
| 7 | **Motion & Interaction** | Timings, easing by purpose, `:focus-visible`, `prefers-reduced-motion`. |
| 8 | **Voice & Brand** | Tone of voice, copy principles, named prior art. |
| 9 | **Anti-patterns** | What the brand is **not** — specific and bounded. |

Full section-by-section detail + the 4 token layers (A1-identity, A1-structure,
A2-fallback, B-slot, C-extensions) in **`references/schema.md`**.

### Two real heading variants

The brand-grade exemplars in `references/systems/` use a different dialect, equally
valid under the parsing contract:

- **Variant A (the majority):** Visual Theme · Color Palette & Roles · Typography Rules ·
  Component Stylings · Layout Principles · Depth & Elevation · Do's and Don'ts · Responsive
  Behavior · **Agent Prompt Guide**.
- **Variant B (canonical spec — `atelier-zero`):** the 9 from the table above.

Pick **one** per project and keep it. The `references/template.md` uses Variant B (maps
1:1 onto the token layers). Cross-map A↔B in `references/schema.md §2`.

## The "Agent Prompt Guide" pattern (the section made FOR the agent)

The last section of the exemplars is written **for an agent to consume** in UI generation — it is not
documentation for a human. Three parts:

1. **Quick Color Reference** — each role → name + hex, in the format the agent cites:
   `Brand CTA: "Terracotta Brand (#c96442)"`.
2. **Example Component Prompts** — ready-to-paste prompts, citing exact hex/font/radius.
3. **Iteration Guide** — recipe (one component at a time, cite specific color names,
   name the system's shadow type, specify the background).

**This section is what distinguishes** a DESIGN.md that *describes* a brand from one an agent
*can build*. Without it the agent improvises values. Every new DESIGN.md ends with its own
Agent Prompt Guide.

## Review checklist

### Lens A — code correctness (BLOCKING)

Failing any item invalidates the file:

- [ ] The **9 numbered sections present, in order**.
- [ ] Colors are **real hex** (`#RRGGBB`/`#RGB`) — no `#REPLACE_ME`, `currentColor`,
      or CSS var name in place of the value.
- [ ] Every CSS var inside **`:root {}`** (except component-scoped override).
- [ ] **Dark mode via `[data-theme="dark"]`** as an override (different values), not a
      duplicated block.
- [ ] **`:focus-visible`** on every interactive element (button, link, input, clickable card).
- [ ] **`prefers-reduced-motion`** targets specific elements, never the global `*` selector.
- [ ] **"Font labels for catalog extraction"** block present (prefixes `Display:`/`Body:`/`Mono:`).
- [ ] **WCAG AA 4.5:1 contrast** of each text/data against the **paired** background (not against
      white by default; 3:1 only for large text 18px+/14px+ bold).
- [ ] Components use **semantic tokens**, zero hardcoded hex in component CSS.

### Lens B — substance (P3, not blocking but required for "brand-grade")

- [ ] Palette lists **all roles** used, not just primary/secondary.
- [ ] Type scale has **≥4 tiers** (Display, H1, Body, Caption).
- [ ] Components have **real CSS**, no Lorem Ipsum or `/* TODO */`.
- [ ] Anti-patterns **specific and bounded** ("no rounded corners > 4px"), not "avoid bad
      design".
- [ ] Dark mode is a **genuine override**, not a copy of the light block.
- [ ] Prior art names **real products/systems**, not "inspired by good design".
- [ ] Reasonable size: **300-600 lines** (below ~100 triggers a substance review).

## Workflow

1. **Study exemplars.** Open 2-3 in `references/systems/` by category/mood proximity
   (e.g.: editorial product → `claude`, `kami`, `notion`; dev tool → `vercel`, `linear-app`,
   `raycast`; consumer → `apple`, `airbnb`, `tesla`). Extract **patterns** (warm neutrals
   discipline, depth via ring-shadow, single-weight serif), not values.
2. **Decide the identity** of the project: central metaphor, accent, atmosphere, prior art.
3. **Fill in the `references/template.md`** → `DESIGN.md` in the project repo. Real hex from the
   start. One heading variant, consistent.
4. **End with the project's own Agent Prompt Guide.**
5. **Run the review** Lens A (blocking) → Lens B (substance).
6. **Version** the `DESIGN.md` in the repo. It is the contract; from here on every UI generation cites
   its roles/hex.

## Reference files

- **`references/schema.md`** — full section-by-section schema + the 4 token layers
  (A1/A2/B-slot/C) + promotion path C→B→A2→A1 + accessibility rules.
- **`references/template.md`** — blank `DESIGN.md`, 9 commented sections, ready to
  fill in.
- **`references/systems/`** — 15 curated brand-grade exemplars (claude, linear-app, stripe,
  apple, vercel, notion, figma, raycast, supabase, airbnb, tesla, theverge, wired,
  atelier-zero, kami). Source: open-design (nexu-io, Apache-2.0). See
  `references/systems/README.md` for index + license.
