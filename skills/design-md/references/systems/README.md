# Curated Design Systems

Brand-grade `DESIGN.md` exemplars curated into the `design-md` skill. Each file is a
complete, real-world design contract that follows the 9-section schema and ends with an
**Agent Prompt Guide** — the section written *for an AI agent to consume* when generating UI.

Use these as **reference and inspiration**, not as drop-in themes. When a new project needs
an identity, study 2-3 of these (pick by category proximity), then author the project's own
`DESIGN.md` from `../template.md`. Never copy a brand wholesale — extract the *patterns*
(warm-neutral discipline, ring-shadow depth, single-weight serif headings) and re-decide the
values for the project at hand.

## License & Attribution

All files in this directory are curated from **open-design** by nexu-io
(<https://github.com/nexu-io/open-design>), licensed **Apache-2.0**. Content is preserved
verbatim from the upstream `design-systems/<brand>/DESIGN.md` files; each file carries a
two-line attribution header (`Source:` + `Inspired by`). Brand names and trade dress belong
to their respective owners — these documents are *interpretations* of public brand
aesthetics for design-education purposes, signalled by the "Inspired by" framing upstream.

Apache-2.0 requires preserving the license notice and attribution; both are satisfied by the
per-file headers and this README. The full upstream `LICENSE` text lives in the source repo.

## Curated Brands (15)

| File | Category | Character |
| --- | --- | --- |
| `claude.md` | AI & LLM | Warm terracotta accent, parchment canvas, single-weight serif, ring shadows. |
| `linear-app.md` | Productivity & SaaS | Ultra-minimal, precise, purple accent, dense functional UI. |
| `stripe.md` | Fintech & Crypto | Signature purple gradients, weight-300 elegance, trust-by-restraint. |
| `apple.md` | Media & Consumer | Premium white space, SF Pro, cinematic imagery, calm hierarchy. |
| `vercel.md` | Developer Tools | Black-and-white precision, Geist font, sharp contrast. |
| `notion.md` | Productivity & SaaS | Warm minimalism, serif headings, soft surfaces, low chroma. |
| `figma.md` | Design & Creative | Vibrant multi-color, playful-yet-professional, expressive. |
| `raycast.md` | Developer Tools | Sleek dark chrome, vibrant gradient accents, command-bar density. |
| `supabase.md` | Backend & Data | Dark emerald theme, code-first, terminal energy. |
| `airbnb.md` | E-Commerce & Retail | Warm coral accent, photography-driven, rounded friendly UI. |
| `tesla.md` | Automotive | Radical subtraction, full-viewport photography, near-zero chrome. |
| `theverge.md` | Media & Consumer | Acid-mint + ultraviolet, Manuka display, rave-flyer story tiles. |
| `wired.md` | Media & Consumer | Broadsheet density, custom serif display, mono kickers, ink-blue links. |
| `atelier-zero.md` | Editorial · Studio | Collage-driven, warm paper, oversized display type, hairline rules. |
| `kami.md` | Editorial & Print | Parchment canvas, ink-blue accent, serif hierarchy — print, not UI. |

### Schema variants you'll see here

The upstream parser keys on the `## [digit].` prefix only, so two heading dialects coexist:

- **Variant A (most files):** `Visual Theme & Atmosphere · Color Palette & Roles ·
  Typography Rules · Component Stylings · Layout Principles · Depth & Elevation · Do's and
  Don'ts (or Accessibility) · Responsive Behavior · Agent Prompt Guide`. This is the
  dominant brand-grade convention. `notion.md` swaps section 8 to "Accessibility & States".
- **Variant B (canonical spec — `atelier-zero.md`):** `Visual Theme & Atmosphere · Color ·
  Typography · Spacing & Grid · Layout & Composition · Components · Motion & Interaction ·
  Voice & Brand · Anti-patterns`.

Both satisfy the same contract. The OSForge `template.md` uses the **canonical spec
(Variant B)** because it maps 1:1 onto the token layers in `../schema.md`. See `../schema.md`
for the section-by-section contract and the A↔B cross-map.

## What makes these "brand-grade" (and worth studying)

1. **Real hex everywhere** — no `#REPLACE_ME`, no `currentColor` placeholders.
2. **Roles, not just colors** — every hue is named *and* assigned a job (CTA, tertiary text,
   border-soft), so an agent never guesses.
3. **An Agent Prompt Guide** — quick color reference + ready-to-paste component prompts +
   an iteration recipe. This is the payload an agent reads to actually build.
4. **Specific anti-patterns** — "no cool blue-grays anywhere", not "avoid bad design".
5. **Dark mode as genuine override**, not a duplicated block.
