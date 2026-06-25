---
name: editorial-review
description: >
  Editorial review of technical documents in 2 modes: prose (clinical
  copy-editing) and structure (reorganization and simplification).
  Use with "editorial review", "review prose", "review structure", "review writing",
  "confusing document", "flabby writing", "verbose text", "this doc is poorly organized".
trigger: editorial|review prose|review structure|review writing
model-tier: sonnet
---

# Editorial Review

## Operating Modes

Detect the mode from the trigger or ask if ambiguous.

### Prose Mode (default)
Clinical copy-editor. Review the text for communication problems.

**Checklist:**
- **Clarity:** Ambiguous sentences, dangling modifiers, vague references
- **Conciseness:** Unnecessary words, redundancies, circumlocutions
- **Consistency:** Varying terminology, inconsistent formats, shifting tone
- **Precision:** Vague claims that should be specific, numbers without a source
- **Tone:** Register shifts, excessive passive voice, unnecessary jargon
- **Grammar:** Technical language errors, agreement, government

**Output:**
```markdown
## Editorial Review — Prose

### Issues Found: {N}

1. **[Line ~{N}]** {type}: "{problematic excerpt}"
   → Suggestion: "{proposed correction}"

2. **[Section {name}]** {type}: {description}
   → Suggestion: {correction}
...
```

### Structure Mode
Structural editor. Propose reorganization without rewriting.

**Analysis:**
- **Cuts:** Sections that can be removed without loss of comprehension
- **Reorganization:** Sections out of logical order (reading dependency)
- **Merge:** Sections that cover the same topic and should be combined
- **Split:** Sections that try to cover too many subjects
- **Simplification:** Unnecessarily deep heading hierarchies
- **Gaps:** Information expected but absent given the document type

**Output:**
```markdown
## Editorial Review — Structure

### Restructuring Plan

1. **CUT** section "{name}" — Reason: {justification}
2. **MOVE** section "{name}" after "{other}" — Reason: {justification}
3. **MERGE** sections "{A}" and "{B}" — Reason: {justification}
4. **SPLIT** section "{name}" into "{sub-A}" and "{sub-B}" — Reason: {justification}
5. **GAP** missing section about "{topic}" — Reason: {justification}

### Proposed Structure
{outline of the new structure with headings}
```

## Fundamental Rule
Do NOT rewrite the document — only list findings and suggestions.
The user decides what to apply.
