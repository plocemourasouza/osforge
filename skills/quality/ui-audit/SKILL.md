---
name: ui-audit
description: "Retroactive visual quality audit of already-implemented frontend code. Use after any UI/UX phase, or when: 'the screen looks off', 'it's not how I wanted', 'review the UI', 'audit the frontend', 'check the visuals', 'check visual accessibility'. Keywords: audit ui, review ui, audit ui, ui review, check visuals, check frontend, not how I imagined, bad visuals."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Glob, Grep
metadata:
  version: '1.1'
---

## Phase context
!`ls .osforge/phases/ 2>/dev/null | grep CONTEXT | head -5 || echo "No phase CONTEXT.md found — audit without reference to user decisions"`
!`find src app -name "*.tsx" -newer package.json 2>/dev/null | head -10 || echo "Recent components not auto-detected"`

# UI Audit

## Role

UI reviewer with a clinical eye. Evaluates already-implemented frontend code
against 6 pillars of visual quality, identifies gaps between what was
built and what the user imagined, and produces actionable fix plans.

Inspired by the `ui-review` pattern from GSD (get-shit-done).

---

## Inputs

- **Component files** — relevant `.tsx` files from the audited phase
- **Phase `CONTEXT.md`** (`.osforge/phases/{N}-CONTEXT.md`) — agreed decisions
- **Screenshot or description** — how the user imagined it vs. how it turned out (optional but valuable)

Always load the audited phase's CONTEXT.md if it exists — it contains the
decisions the user made and that must be verified.

---

## The 6 Pillars

### Pillar 1 — Visual Hierarchy
Does the user's eye know what's most important?

Check:
- Is there a clear visual anchor on each screen (title, primary CTA, key data)?
- Do typographic weight and size guide reading in the correct order?
- Are secondary elements visually subordinate?
- Is there no competition among multiple elements of equal prominence?

### Pillar 2 — Consistency
Does the system look like it was made by a single mind?

Check:
- Does spacing follow a consistent scale (not arbitrary values)?
- Are shadcn/ui component variants used correctly (not mixing `outline` and `ghost` without reason)?
- Does typography use design system tokens, not hard-coded values?
- Do colors follow semantic tokens (`primary`, `muted`, `destructive`) without unjustified exceptions?
- Are borders, radii, and shadows consistent throughout the feature?

### Pillar 3 — Feedback and States
Does the user know what's happening?

Check:
- Do loading states have an appropriate skeleton or spinner?
- Do error states have a useful message and a recovery action?
- Do destructive actions have confirmation?
- Do empty states have an explanation and a call-to-action?
- Do forms have inline validation with a clear message?
- Do async actions have immediate feedback (disabled button, loading state)?

### Pillar 4 — Responsiveness
Does it work across all relevant breakpoints?

Check:
- Does the layout not break on mobile (< 640px) and tablet (640–1024px)?
- Does text not overflow containers on smaller screens?
- Do long tables have horizontal scroll or mobile adaptation?
- Do touch targets have a minimum of 44px on mobile?
- Do images and grids have correct responsive behavior?

### Pillar 5 — Visual Accessibility
Can low-vision users use it?

Check:
- Does text contrast meet WCAG AA (4.5:1 for normal text, 3:1 for large text)?
- Are focus states visible on all interactive elements?
- Do icons without a label have an `aria-label` or tooltip?
- Do forms have a `<label>` associated with each input?
- Are colors not the only state indicator (e.g., red error WITHOUT icon)?

### Pillar 6 — Alignment with User Decisions
Does what was built reflect what was agreed in `phase-discussion`?

Check each decision recorded in `CONTEXT.md`:
- Was the chosen layout (card, list, grid) implemented correctly?
- Are the agreed interactions (modal, slide-over, inline) present?
- Was the visual tone (dense, spacious, minimalist) respected?
- Were explicitly deferred decisions (v2+) not accidentally implemented?

---

## Audit Process

### 1. Load context
- Read the phase CONTEXT.md if it exists
- Identify the `.tsx` files to audit
- If a screenshot is available: compare visually

### 2. Audit pillar by pillar
For each pillar, evaluate: ✅ OK | ⚠️ Attention | ❌ Problem

Record issues with:
- **Location:** file + approximate line
- **Description:** what's wrong and why
- **Impact:** High (blocks use) / Medium (degrades experience) / Low (cosmetic)
- **Suggested fix:** specific code or guidance

### 3. Generate report

```markdown
---
type: osforge-ui-audit
phase: "{N} — {title}"
audited_at: {date}
overall: OK | APPROVED WITH RESERVATIONS | REJECTED
---

# UI Audit — Phase {N}: {title}

## Executive Summary
{2-3 sentences: what's good, the main problems, recommended action}

## Result by Pillar

| Pillar | Status | Issues |
|---|---|---|
| 1. Visual Hierarchy | ✅/⚠️/❌ | {N} |
| 2. Consistency | ✅/⚠️/❌ | {N} |
| 3. Feedback and States | ✅/⚠️/❌ | {N} |
| 4. Responsiveness | ✅/⚠️/❌ | {N} |
| 5. Visual Accessibility | ✅/⚠️/❌ | {N} |
| 6. Alignment with Decisions | ✅/⚠️/❌ | {N} |

## Issues by Priority

### 🔴 High (fix before ship)
- [ ] **{file}:{approx line}** — {description} → {fix}

### 🟡 Medium (fix next sprint)
- [ ] **{file}:{approx line}** — {description} → {fix}

### 🟢 Low (backlog)
- [ ] **{file}:{approx line}** — {description} → {fix}

## Fix Plan

If there are High or Medium issues, offer:
- **Immediate fix:** list of tasks ready for `story-executor`
- **Estimate:** S/M/L of effort

## What turned out well
{acknowledge what was well implemented — avoid a purely negative report}
```

Save to `.osforge/phases/{N}-UI-AUDIT.md`.

---

## Expected Output Artifacts

At the end of the audit, the produced artifacts should be:

1. **Audit report** — `.osforge/phases/{N}-UI-AUDIT.md` in the format above (required), with an overall verdict, table by pillar, prioritized issues, and a fix plan.
2. **Evidence screenshots** (when available) — captures of the audited screens (desktop and mobile), attached or referenced in the report alongside the corresponding issue; e.g., `.osforge/phases/{N}-audit-screens/hero-mobile.png` showing overflowing text.
3. **Fix task list** — High/Medium items formatted as tasks ready for `story-executor`, with an S/M/L estimate.

---

## Integration with other skills

- **`openui-genui-layout`** → plans BEFORE implementation (design contract)
- **`ui-audit`** → audits AFTER implementation (quality verification)
- **`phase-discussion`** → the `CONTEXT.md` is the reference for Pillar 6
- **`story-executor`** → executes the fixes identified by the audit

The ideal flow is: `phase-discussion` → `openui-genui-layout` → implementation → `ui-audit`.


## Gotchas

- **Auditing without CONTEXT.md**: Pillar 6 (Alignment with Decisions) is unauditable without the phase CONTEXT.md. If it doesn't exist, the audit produces an incomplete report — mention this explicitly in the executive summary.
- **Marking everything as "Attention" out of caution**: being too conservative pollutes the report with false positives and makes the user ignore the real issues. Only mark ❌ when there's a clear, verifiable violation, not on suspicion.
- **Not prioritizing issues**: a report with 20 items without prioritization is useless. Always separate into High (blocks ship), Medium (experience degradation), and Low (cosmetic). The user needs to know where to focus.
- **Focusing only on code without seeing the visual result**: if possible, always ask for a screenshot or access the route in dev to see the real result — spacing, typography, and hierarchy issues are much easier to detect visually than by reading TSX code.
- **Not acknowledging what was done well**: purely negative reports demotivate and give the wrong impression of the overall state. The "What turned out well" section is mandatory — not optional.
- **Proposing fixes without estimating effort**: always include an S/M/L estimate for each group of fixes. The user needs to decide what to fix before ship vs. what goes to backlog.
