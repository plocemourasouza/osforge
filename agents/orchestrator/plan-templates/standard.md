# Plan Template: STANDARD

## Plan: {title}
**Complexity:** STANDARD
**Phases:** 4-6 (adapt as needed)

### Phase 1: Technical Specification
- **Objective:** Define requirements, scope, and acceptance criteria
- **Skill:** `skills/planning/spec-builder`
- **Artifact:** `{output_dir}/tech-spec-{slug}.md`
- **Size:** Small to Medium

### Phase 2: Architecture Check (if schema/API changes)
- **Objective:** Validate technical decisions against the project's stack
- **Skill:** `skills/planning/arch-builder`
- **Artifact:** ADRs section in the spec or `{output_dir}/arch-decisions-{slug}.md`
- **Size:** Small
- **Condition:** Skip if the change does not affect schema, API, or existing patterns

### Phase 3: Decomposition into Stories
- **Objective:** Break the spec into implementable and ordered stories
- **Skill:** `skills/planning/epic-decomposer`
- **Artifact:** `{output_dir}/stories/{slug}/` (1 file per story)
- **Size:** Small to Medium

### Phase 4-N: Implementation (loop per story)
- **Objective:** Implement each story in dependency order
- **Skill:** `skills/planning/story-executor` → execution skills
- **Artifact:** Code + tests per story
- **Size:** Varies per story (S/M/L)

For each story:
1. Implement the story's tasks
2. Code review (`skills/quality/code-review`)
3. If approved → next story
4. If changes requested → fix and re-review

#### Parallelism metadata per task

Each task generated for this plan MUST include the YAML block below right after the `### TN:` header:

```yaml
id: T<N>
depends_on: []      # ids of prerequisite tasks (e.g., [T1, T2])
wave: 1             # execution wave derived from depends_on
parallel_ok: true   # false if it touches a file shared with another task in the same wave
```

Derivation rules:
- Tasks with no predecessors → `wave: 1`.
- Tasks whose latest predecessor is in wave N → `wave: N+1`.
- Tasks in the same wave with `parallel_ok: true` are dispatched in parallel by the orchestrator.
- Two tasks that edit the same file → `parallel_ok: false` or different waves.

### Final Phase: Quality Review
- **Objective:** Adversarial validation of the complete set
- **Skill:** `skills/quality/adversarial-review` + `skills/quality/edge-case-hunter`
- **Artifact:** Consolidated review report
- **Size:** Medium

### Checkpoints
- After Phase 1: approve the spec
- After Phase 2: approve the architecture decisions (if applicable)
- After Phase 3: approve the decomposition into stories before implementing
- After each story: code review
- After the Final Phase: approve for merge/deploy

### Notes
- If the spec exceeds ~1600 tokens, consider splitting or reclassifying as COMPLEX
- Stories should be independent enough for isolated review
- If ambiguity arises in the requirements during implementation → course correction
