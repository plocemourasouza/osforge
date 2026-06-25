# Plan Template: QUICK

## Plan: {title}
**Complexity:** QUICK
**Phases:** 3

### Phase 1: Specification
- **Objective:** Define exactly what to do with acceptance criteria
- **Skill:** `skills/planning/spec-builder`
- **Artifact:** `{output_dir}/tech-spec-{slug}.md`
- **Size:** Small

### Phase 2: Implementation
- **Objective:** Execute the spec's tasks
- **Skill:** Relevant execution skills (identify by the type of change)
- **Artifact:** Code + tests
- **Size:** {estimate based on the spec}

### Phase 3: Review
- **Objective:** Validate the implementation
- **Skill:** `skills/quality/code-review`
- **Artifact:** Review report (approved or changes requested)
- **Size:** Small

### Checkpoints
- After Phase 1: approve the spec before implementing
- After Phase 3: verify that everything is covered

### Notes
- If complications arise during implementation, reclassify as STANDARD
- The spec should have at most ~1600 tokens (contained scope)
