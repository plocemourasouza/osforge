---
name: doc-shard
description: >
  Split large markdown documents into smaller organized files
  with an index. Use when a document exceeds the context window or to
  organize extensive docs — e.g. a 10k-token guide, a spec with
  multiple sections, an extensive PRD. Use with "shard doc", "split document".
trigger: shard|split doc|split document|break up document
model-tier: haiku
---

# Document Sharder

## Objective
Split large markdown documents into smaller, organized files
with an index, for efficient consumption by LLMs and other skills.

## Inputs
- **source_path** — Path of the markdown document to split
- **split_level** (default: 2) — Heading level for the split (## = level 2)
- **output_dir** (optional) — Output directory. Default: `{source_name}-sharded/`

## Process

### 1. Analyze Document
- Read the source document completely
- Identify all headings at the specified level
- Map sections and approximate sizes in tokens
- Preserve the original frontmatter

### 2. Generate Shards
For each section at the specified level:
- Create file: `{NN}-{slug-do-heading}.md`
- Include a context header: `<!-- Part N of M — {original heading} -->`
- Include the section content with sub-headings preserved
- If an individual section > ~3000 tokens, subdivide at the next heading level

### 3. Generate Index
Create `_index.md`:

```markdown
---
type: osforge-shard-index
source: "{path of the original document}"
shards: {N}
created: "{date}"
total_tokens_estimate: {N}
---

# Index: {title of the original document}

## About
- {1-2 bullets describing the original document}

## Sections
| # | File | Topic | ~Tokens |
|---|------|-------|---------|
| 1 | `01-{slug}.md` | {1-line description} | ~{N} |
| 2 | `02-{slug}.md` | {1-line description} | ~{N} |
...

## Cross-Cutting
- {items that appeared in multiple sections}
```

### 4. Report
"Document split into {N} shards + index.
Loading _index.md (~{X} tokens) vs the full document (~{Y} tokens)
= {ratio}x more efficient for initial discovery."

## Rules
- Never lose content in the split — all text from the original must appear in some shard
- Keep internal references between sections when they exist
- The original's frontmatter goes to _index.md, not to the shards
- Shards must be self-contained — understandable without reading the others
