# Plan Template: COMPLEX

## Plan: {title}
**Complexity:** COMPLEX
**Phases:** 7+ (adapt as needed)

### Phase 1: Requirements Definition (PRD)
- **Objective:** Define the problem, users, functional and non-functional requirements, MVP scope
- **Skill:** `skills/planning/prd-builder`
- **Artifact:** `{output_dir}/prd-{slug}.md`
- **Size:** Medium to Large
- **Facilitation:** Collaborative — guided questions, not autonomous generation

### Phase 2: Architecture
- **Objective:** Technical decisions, data model, API design, integrations
- **Skill:** `skills/planning/arch-builder`
- **Artifact:** `{output_dir}/architecture-{slug}.md` (with ADRs)
- **Size:** Medium
- **Input:** PRD from Phase 1 + project-context.md

### Phase 3: Decomposition into Epics and Stories
- **Objective:** Turn requirements into implementable work items
- **Skill:** `skills/planning/epic-decomposer`
- **Artifact:** `{output_dir}/epics/{slug}/` (1 file per epic with stories)
- **Size:** Medium to Large
- **Input:** PRD + Architecture

### Phase 4: Quality Gate — Readiness Check
- **Objective:** Validate that PRD, Architecture, and Epics are aligned and complete
- **Skill:** `skills/quality/readiness-gate`
- **Artifact:** Readiness report (PASS / CONCERNS / FAIL)
- **Size:** Small
- **Decision:**
  - PASS → advance to implementation
  - CONCERNS → resolve concerns and re-check
  - FAIL → go back to the phase that failed

### Phase 5: Sprint Planning
- **Objective:** Sequence stories by dependency and priority
- **Skill:** Orchestrator (inline — no separate skill needed)
- **Artifact:** Update `.osforge/status.yaml` with the story sequence
- **Size:** Small

### Phase 6-N: Implementation (sprint loop)
- **Objective:** Implement stories in sequence
- **Skill:** `skills/planning/story-executor` → execution skills
- **Artifact:** Code + tests per story

For each story:
1. Create/refine story context (`skills/planning/story-executor`)
2. Implement tasks
3. Code review (`skills/quality/code-review`)
4. If approved → update status → next story
5. If changes requested → fix and re-review

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
- **Objective:** Complete adversarial review + edge case analysis
- **Skill:** `skills/quality/adversarial-review` + `skills/quality/edge-case-hunter`
- **Artifact:** Consolidated review report + list of edge cases
- **Size:** Medium to Large

### Checkpoints
- After Phase 1: approve the PRD (are all requirements covered?)
- After Phase 2: approve the architecture (do the decisions make sense?)
- After Phase 3: approve the decomposition (are stories implementable?)
- After Phase 4: readiness gate must PASS
- After each story: code review
- After the Final Phase: approve for merge/deploy

### Notes
- If the PRD is too large (>5000 tokens), use `context-distillator` to compress it
- If large docs appear, use `doc-shard` to split them
- Course correction can happen at any point — return to the Orchestrator
- For projects with compliance (LGPD, TSE), include a compliance review as a sub-phase
- For multi-tenant projects, include an RLS review as a sub-phase
