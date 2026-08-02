---
name: context-distillator
description: "Lossless compression of long documents for optimized LLM consumption, preserving 100% of the factual information and eliminating textual overhead. Use when: compress this long doc, distill the context before passing it to another skill, a PRD/spec/architecture too large for the context window, consolidating multiple docs into a single distillate, preparing lean context for implementation or review. Keywords: distill, compress, distillate, context, lossless, tokens, condense. Do NOT use for: lossy summarization aimed at humans, writing new documents, or translation."
trigger: distill|compress|compress context|distillate
model-tier: sonnet
---

# Context Distillator

## Objective
Produce hyper-compressed documents (distillates) from sources,
preserving every fact, decision, constraint, and relationship while eliminating
overhead that humans need and LLMs don't.

**A distillate is a SECONDARY SOURCE** — an account of the sources, not the sources. It records
what this run believed mattered; whatever it filtered out is invisible to every reader downstream.
So: state the sources in the frontmatter (already required) so a consumer can always go back, and
tell consumers plainly that a claim which DECIDES something must be checked against the primary
source. A distillate is for orientation and recall, never the last word on a fact that carries
weight.

## Inputs
- **source_paths** (required) — File/directory paths to distill
- **downstream_consumer** (optional) — Skill that will consume it ("implementation", "architecture", "review")
- **output_path** (optional) — Where to save. Default: `{source}-distillate.md`

## Process

### 1. Source Analysis
- Read all source files completely
- Classify type: PRD, architecture, spec, code, config, docs
- Estimate total size in tokens

**Done when:** every source file was read end to end. Skimming here is invisible in the output —
the distillate looks equally confident whether or not it saw the last third of a document.

### 2. Entity Extraction
Extract ALL discrete information:
- Facts and data (numbers, dates, versions, percentages)
- Decisions made + rationale
- Rejected alternatives + reason
- Requirements and constraints (explicit and implicit)
- Dependencies and relationships between entities
- Named entities (products, technologies, people)
- Open questions and unresolved items
- Scope boundaries (in/out/deferred)
- Success and validation criteria
- Risks with severity

**Done when:** every category above was swept across every source — exhaustive, category by
category. This is the only lossy step in the skill: anything not extracted here cannot be
recovered downstream, because the distillate replaces the sources rather than accompanying them.

### 3. Deduplication
Apply the rules in `./compression-rules.md`:
- Same fact in multiple docs → keep the version with the most context
- Same concept at different levels of detail → keep the detailed one
- Overlapping lists → merge without duplicates
- Conflicting docs → note the conflict: "Doc A says X; Doc B says Y — unresolved"

### 4. Filtering (if downstream_consumer is provided)
For each item: "Does the downstream skill need this?"
- Eliminate clearly irrelevant items
- When in doubt, KEEP — err toward preservation
- NEVER eliminate: decisions, rejected alternatives, open questions, constraints

**Done when:** every dropped item was dropped by an explicit judgement, not by running out of
attention. The four protected classes are still present in full — verify by counting them before
and after, since this is where silent loss happens.

### 5. Thematic Grouping
Organize into themes derived from the content (not a fixed template).
Common themes: core/problem, solution/approach, stack/technical decisions,
scope, success criteria, risks, open questions.

### 6. Language Compression
Apply `./compression-rules.md` item by item:
- Eliminate transitions, hedging, rhetoric, self-reference
- Preserve numbers, names, versions, decisions
- Each bullet self-contained and understandable in isolation
- Explicit relationships: "X because Y", "X blocks Y"

### 7. Output Format

```yaml
---
type: osforge-distillate
sources:
  - "{relative path source 1}"
  - "{relative path source 2}"
downstream_consumer: "{consumer or 'general'}"
created: "{date}"
token_estimate: {approx count}
compression_ratio: "{X:1}"
---
```

Body: dense bullets grouped by thematic `##` headings.
No prose, no paragraphs — bullets only.
No decorative formatting. Semicolons for short related items.

**Done when:** every entity that survived step 4 appears in the body. A distillate is judged by
what it did NOT lose; a smaller ratio achieved by dropping content is not compression, it is
deletion wearing compression's name.

### 8. Splitting (if distillate > ~5000 tokens)
Create a `{base}-distillate/` directory:
- `_index.md` — Orientation + manifest + cross-cutting items
- `01-{topic}.md` — Self-contained section with header "Part N of M"
- `02-{topic}.md`

### 9. Report
Report: "Compressed {N} sources ({X} tokens) → distillate ({Y} tokens).
Ratio: {X/Y}:1. Saved to {path}."
