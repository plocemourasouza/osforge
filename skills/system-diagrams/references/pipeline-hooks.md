# system-diagrams — pipeline hooks

Where the OSForge flow calls this skill, what it must produce, and the exact receipt block. Keep the
steps in the commands/skills themselves to one line each — this file holds the detail.

## Engine location and version

- Engine: `~/.claude/skills/archify/` (Cursor: `~/.cursor/skills/archify/`), installed by
  `deploy.sh` at the tag pinned in `ARCHIFY_VERSION`. Check: `node <engine>/bin/archify.mjs doctor`.
- Report the version from `<engine>/skill-release.json` (`.version`) in every receipt line.
- Never `npm install` inside the engine; it has no runtime dependencies.

## Commands

```bash
E=~/.claude/skills/archify/bin/archify.mjs
node $E guide "<scenario>" --json                                   # type router (ambiguous cases)
node $E validate <type> <src>.json --quality showcase --json         # repair loop
node $E deliver  <type> <src>.json <out>.html --quality showcase --json   # acceptance + receipt
node $E compare architecture base.json head.json delta.html         # ADR before/after
node $E brands --json | grep '"id"'                                 # built-in brand IDs
```

Types: `architecture` · `workflow` (use `schema_version: 2` for new sources) · `sequence` ·
`dataflow` · `lifecycle`.

## Hooks by moment

### `/spec-design` (Phase 2)
- After writing the *Architecture* section of `design.md`, produce
  `.specs/features/<feature>/diagrams/<feature>.architecture.json` (+ `.html`) and, when the feature
  has a non-trivial request/data path, `<feature>.sequence.json` **or** `<feature>.dataflow.json`.
- Replace the placeholder "Text or Mermaid diagram" with the **Diagrams** block below.
- The confirmation checkpoint of `/spec-design` presents the HTML (Canvas or path) together with the
  design decisions.

### ADR (`architecture`, `planning/arch-builder`)
- A topology-changing ADR ships `system-overview.architecture.json` under `.specs/architecture/`.
- When the ADR *replaces* a topology, keep the previous JSON as `*.base.architecture.json`, author
  the new one as `*.head.architecture.json`, and deliver `compare` → `*.delta.html`. Reference all
  three in the ADR's **Consequences**.

### Technical Design Doc (`technical-design-doc-creator`)
- The **Technical Solution → Architecture Diagram** slot links the delivered HTML instead of
  holding a Mermaid block; the Mermaid block is allowed only under the step-5 fallback, labelled
  unverified.

### Runbooks / deployment (`deployment-procedures`, `operations`)
- `workflow` for the procedure (lanes = actors/systems, gates = approvals);
  `lifecycle` for a status/state machine (deploy states, job states).

### Presentation
- `visual-planner`: the *Architecture-first* structure embeds the delivered HTML via `<iframe>` or
  links it; it never redraws the map in CSS.
- `osforge-canvas`: the artifact JSON carries the HTML path as a link element at the approval
  checkpoint.

## Receipt block (paste into the source document)

```markdown
## Diagrams
- [<Title>](diagrams/<slug>.html) — `<type>`, Archify v<version>,
  spec `diagrams/<slug>.<type>.json` sha256 `<first 4>…<last 4>`, artifact sha256 `<first 4>…<last 4>`, <n>/<n> checks
```

Fields come verbatim from the `deliver` JSON: `specification.sha256`, `artifact.sha256`,
`validation.checksPassed`/`checkCount`. A line without these fields is a fallback, not a receipt.

## Presentation variants

```bash
python3 scripts/archify-presentation.py docs/architecture/<name>.html            # → <name>.presentation.html
python3 scripts/archify-presentation.py <name>.html --font "'Inter', system-ui, sans-serif"
```
Derived from the delivered artifact (sha256 stamped in an HTML comment); never referenced by a
receipt line. Glow/motion belong in the JSON (`visual_preset`, `animation`), not here.

## Repo hygiene

- Always version the `.json` (2–6 KB). The `.html` (~800 KB, self-contained viewer) is
  reproducible with `deliver`; projects that mind the size add `**/diagrams/*.html` to `.gitignore`
  and keep the receipt line as proof.
- `schema_version` is stored in the JSON; the engine keeps migrations under `migrations/`. After
  an engine upgrade, re-run `validate` on existing sources before touching them.
