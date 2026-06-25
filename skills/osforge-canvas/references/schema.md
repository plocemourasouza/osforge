---
name: osforge-canvas-schema
description: OSForge Canvas v1 schema — format of JSON artifacts that Claude writes to outputs/canvas/artifacts/.
---

# OSForge Canvas — Schema v1

## Flow Overview

```
Claude
  │  writes (or overwrites) JSON artifact
  ▼
outputs/canvas/artifacts/<id>.json
  │  SSE notifies change
  ▼
scripts/canvas/server.ts (Bun)
  │  serves the viewer over HTTP
  ▼
Browser (viewer)
  │  user interacts with interactive blocks
  │  (checklist, form, decision)
  ▼
outputs/canvas/feedback/<artifact-id>.json
  │  Claude reads feedback
  ▼
Claude (next iteration)
```

**Pseudo-streaming via revision:** Claude writes the file early with partial blocks and keeps overwriting (`revision` incremented on each write). The viewer detects changes via SSE and reloads without a manual refresh.

---

## Envelope

```json
{
  "$schema": "osforge-canvas/v1",
  "id": "kebab-case-slug",
  "title": "Readable artifact title",
  "accent": "vermillion",
  "createdAt": "2026-06-10T14:30:00Z",
  "revision": 1,
  "blocks": []
}
```

| Field | Type | Rule |
|-------|------|-------|
| `$schema` | `"osforge-canvas/v1"` | Fixed literal, identifies the version |
| `id` | string (kebab-case) | Unique slug, also part of the file name |
| `title` | string | Displayed in the viewer header |
| `accent` | enum | Theme color; see palette below |
| `createdAt` | ISO 8601 | Timestamp of the first write; does not change on revisions |
| `revision` | integer ≥ 1 | Claude increments on each overwrite; viewer uses it to detect change |
| `blocks` | array | Sequence of blocks; may be incomplete in intermediate revisions |

### Accent Palette (inherited from visual-planner)

| Value | Hex | Typical use |
|-------|-----|------------|
| `vermillion` | `#D94F30` | Default — general engineering, product |
| `teal` | `#2A7B9B` | Data, infra, backend |
| `coral` | `#E06B56` | Consumer, UX, front-end |
| `forest` | `#2D8B55` | DevTools, CLI, OSS |
| `amber` | `#D4A843` | Fintech, analytics, BI |

---

## Blocks

Every block **must** have a unique `id` (kebab-case) within the artifact. The `id` is the addressing key in the feedback file.

### 1. `heading`

Section or sub-section within the artifact.

```json
{
  "type": "heading",
  "id": "phase-1",
  "level": 2,
  "text": "Phase 1 — Preparation"
}
```

| Field | Type | Values |
|-------|------|---------|
| `level` | integer | `2` (main section) or `3` (sub-section) |
| `text` | string | Heading text |

---

### 2. `markdown`

Free-text block in Markdown. Supports lists, bold, italics, inline code, links.

```json
{
  "type": "markdown",
  "id": "general-context",
  "md": "The goal is to **migrate legacy sessions** to JWT + refresh token, keeping compatibility with v1 clients."
}
```

| Field | Type | Values |
|-------|------|---------|
| `md` | string | Markdown source (GFM) |

---

### 3. `cards`

Grid of cards with a title, optional badge, and Markdown body.

```json
{
  "type": "cards",
  "id": "benefits",
  "columns": 3,
  "items": [
    { "title": "Stateless", "badge": "JWT", "md": "Eliminates session DB lookups on every request." },
    { "title": "Refresh Token", "badge": "Security", "md": "Automatic rotation; granular per-user revocation." },
    { "title": "Multi-device", "md": "Each device receives its own refresh token." }
  ]
}
```

| Field | Type | Values |
|-------|------|---------|
| `columns` | integer | `2`, `3`, or `4` |
| `items[].title` | string | Card title |
| `items[].badge` | string? | Colored label in the top-right corner (optional) |
| `items[].md` | string | Body in Markdown |

---

### 4. `table`

Structured table with header and rows.

```json
{
  "type": "table",
  "id": "auth-endpoints",
  "columns": ["Endpoint", "Method", "Change", "Breaking?"],
  "rows": [
    ["/auth/login", "POST", "Returns access + refresh token", "No"],
    ["/auth/refresh", "POST", "New endpoint", "No"],
    ["/auth/logout", "POST", "Revokes refresh token", "No"],
    ["/auth/session", "GET", "Removed", "**Yes**"]
  ]
}
```

| Field | Type | Values |
|-------|------|---------|
| `columns` | string[] | Column names |
| `rows` | string[][] | Each row is an array of cells; supports inline Markdown |

---

### 5. `checklist`

Interactive checklist. The user can check/uncheck items; the state is saved in the feedback.

```json
{
  "type": "checklist",
  "id": "acceptance-criteria",
  "title": "Acceptance Criteria",
  "items": [
    { "id": "unit-tests", "text": "Coverage ≥ 80% in the auth modules", "checked": false },
    { "id": "zero-downtime", "text": "Deploy with no interruption (blue-green)", "checked": false },
    { "id": "docs-updated", "text": "OpenAPI updated with the new endpoints", "checked": false }
  ]
}
```

| Field | Type | Values |
|-------|------|---------|
| `title` | string? | Optional title above the list |
| `items[].id` | string | kebab-case; key in the feedback |
| `items[].text` | string | Item text |
| `items[].checked` | boolean | Initial state |

---

### 6. `form`

Interactive form with text, textarea, select, and checkbox fields. Allows collecting structured input from the user.

```json
{
  "type": "form",
  "id": "rollout-parameters",
  "submitLabel": "Confirm strategy",
  "fields": [
    {
      "id": "strategy",
      "label": "Rollout strategy",
      "kind": "select",
      "options": ["big-bang", "canary", "shadow"],
      "value": "canary"
    },
    {
      "id": "notes",
      "label": "Additional notes",
      "kind": "textarea",
      "value": ""
    }
  ]
}
```

| Field | Type | Values |
|-------|------|---------|
| `submitLabel` | string? | Submit button text (default: "Submit") |
| `fields[].id` | string | kebab-case; key in the feedback |
| `fields[].label` | string | Label displayed above the field |
| `fields[].kind` | enum | `"text"`, `"textarea"`, `"select"`, `"checkbox"` |
| `fields[].options` | string[]? | Required when `kind = "select"` |
| `fields[].value` | any? | Initial value |

---

### 7. `decision`

Explicit decision block. Requires the user to approve, edit, or reject before continuing.

```json
{
  "type": "decision",
  "id": "architecture-approval",
  "prompt": "Is the JWT + refresh token architecture aligned with the security requirements?",
  "options": ["approve", "edit", "reject"],
  "commentRequiredFor": ["edit", "reject"]
}
```

| Field | Type | Values |
|-------|------|---------|
| `prompt` | string | Question or statement for the user to decide on |
| `options` | enum[] | Subset of `["approve", "edit", "reject"]` — at least one |
| `commentRequiredFor` | enum[] | Options that require a mandatory comment in the feedback |

---

### 8. `mermaid`

Diagram rendered as Mermaid.js.

```json
{
  "type": "mermaid",
  "id": "dependency-flow",
  "kind": "graph",
  "code": "graph LR\n  Schema-->Endpoints\n  Endpoints-->Cutover"
}
```

| Field | Type | Values |
|-------|------|---------|
| `kind` | enum | `"graph"` (flowchart/graph) or `"gantt"` |
| `code` | string | Valid Mermaid source; newlines as `\n` in the JSON |

---

## Feedback File

Generated by the viewer at `outputs/canvas/feedback/<artifact-id>.json` when the user submits any interactive block.

```json
{
  "artifactId": "auth-refactor-plan",
  "revision": 1,
  "submittedAt": "2026-06-10T15:00:00Z",
  "responses": {
    "acceptance-criteria": {
      "type": "checklist",
      "checked": ["unit-tests", "zero-downtime"]
    },
    "rollout-parameters": {
      "type": "form",
      "values": {
        "strategy": "canary",
        "notes": "Start with 5% of traffic, monitor for 24h."
      }
    },
    "architecture-approval": {
      "type": "decision",
      "action": "edit",
      "comment": "Add automatic refresh token rotation after each use."
    }
  },
  "comment": "Approved overall; adjust per the comments above."
}
```

| Field | Type | Rule |
|-------|------|-------|
| `artifactId` | string | Same `id` as the artifact envelope |
| `revision` | integer | Revision of the artifact the user viewed; Claude uses it to detect stale feedback |
| `submittedAt` | ISO 8601 | Submit timestamp |
| `responses` | object | Keys = `blockId`; value depends on the type (see below) |
| `comment` | string? | Optional general comment from the user |

### Formats per type in `responses`

| Type | Fields |
|------|--------|
| `checklist` | `{ type: "checklist", checked: string[] }` — array of checked `itemId`s |
| `form` | `{ type: "form", values: { [fieldId]: string } }` |
| `decision` | `{ type: "decision", action: "approve"\|"edit"\|"reject", comment?: string }` |

---

## Rules

1. **Unique IDs:** Every block `id` and item `id` (in checklist and form) must be unique within the artifact. Use descriptive kebab-case.
2. **Incremental revision:** Claude always overwrites the SAME file with `revision + 1`. Never creates a new file for an update.
3. **Pseudo-streaming:** It is allowed to write the file with incomplete `blocks` in intermediate revisions. The viewer reloads via SSE on each write.
4. **Immutable createdAt:** The `createdAt` field reflects the first write and is not changed in subsequent revisions.
5. **Stale feedback:** If `feedback.revision < artifact.revision`, Claude must indicate that the feedback refers to a previous revision.
6. **Default accent:** Omitting `accent` is equivalent to `"vermillion"`. Always include it explicitly for themed artifacts.

---

## Full Example

Minimal valid artifact with 3 block types:

```json
{
  "$schema": "osforge-canvas/v1",
  "id": "sprint-planning",
  "title": "Sprint Planning — Week 24",
  "accent": "forest",
  "createdAt": "2026-06-10T09:00:00Z",
  "revision": 1,
  "blocks": [
    {
      "type": "heading",
      "id": "goal",
      "level": 2,
      "text": "Sprint Goal"
    },
    {
      "type": "markdown",
      "id": "context",
      "md": "Ship the **notifications feature** to production with test coverage ≥ 85%."
    },
    {
      "type": "checklist",
      "id": "deliverables",
      "title": "Deliverables",
      "items": [
        { "id": "api-notif", "text": "Notifications API (REST)", "checked": false },
        { "id": "ui-notif", "text": "UI — notifications panel", "checked": false },
        { "id": "tests", "text": "E2E integration tests", "checked": false }
      ]
    },
    {
      "type": "decision",
      "id": "go-nogo",
      "prompt": "Is the sprint ready to start?",
      "options": ["approve", "edit", "reject"],
      "commentRequiredFor": ["edit", "reject"]
    }
  ]
}
```
