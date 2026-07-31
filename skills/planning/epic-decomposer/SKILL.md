---
name: epic-decomposer
description: >
  Decomposes specs, PRDs, or requirements into implementable epics and stories.
  Each story with testable ACs, tasks with file paths, and mapped dependencies.
trigger: epic|epics|stories|decompose|breakdown|create stories|sprint
model-tier: sonnet
---

# Epic Decomposer

## Role
Analytical Scrum Master. Turns abstract requirements into concrete,
implementable work items. Each story must be implementable in
isolation with a verifiable result.

## Inputs
- **spec or PRD** — Source of requirements (mandatory)
- **architecture** — Technical decisions that affect decomposition
- **project-context.md** — Codebase patterns and conventions

## Process

### 1. Analyze the Requirements Source
- Read the full spec/PRD
- Identify distinct functional domains
- Map dependencies between features
- Read the project's `CONTEXT.md`, so epics and stories are named in the canonical vocabulary

**Done when:** every functional requirement in the source is mapped to a domain. Exhaustive: a
requirement that never reaches an epic is a requirement that never gets built, and nothing later
in the chain will notice its absence.

### 2. Decompose into Epics
Group by functional domain:
- Each epic is a cohesive set of functionality
- Epics must be orderable by dependency
- Name them: `epic-{N}-{slug}` (e.g. `epic-1-auth`, `epic-2-billing`)

**Done when:** every domain from step 1 belongs to exactly one epic, and the dependency order
between epics has no cycle.

### 3. Decompose Epics into Stories
For each story:

```markdown
### Story {epic-N}-{M}: {descriptive title}

**Goal:** {1 sentence — what the user gains from this}

**Acceptance Criteria:**
- [ ] AC1: Given {ctx}, When {action}, Then {result}
- [ ] AC2: Given {ctx}, When {action}, Then {result}

**Tasks:**
1. `{file/path.ts}` — {specific action}
2. `{file/path.ts}` — {specific action}
3. `{file/path.test.ts}` — {tests for the ACs}

**Dependencies:** {story-ids that must be complete first}
**Complexity:** S | M | L
```

### 4. Decomposition Rules
- Each story must have 1 clear goal (single user-facing goal)
- Tasks must have explicit file paths
- ACs must be verifiable (Given/When/Then)
- No placeholders or TBDs
- Stories S: 1-3 tasks, M: 4-7 tasks, L: 8+ tasks (consider splitting)
- An L story should be reviewed — it may be an epic in disguise

**Done when:** every story satisfies every rule above, checked story by story. These rules are what
`readiness-gate` will test later; failing them here just moves the rework downstream, after the
artifacts have been read by other people.

### 5. Ordering
- Order stories by dependency within each epic
- Order epics by dependency among themselves
- The first epic is usually infrastructure/setup
- The last epic is usually polish/optimization

**Done when:** the dependency graph is acyclic and every story's declared dependencies exist. This
ordering becomes the wave plan for parallel dispatch, so a wrong edge here is executed, not caught.

### 6. Artifact Format
One file per epic:

```markdown
---
type: osforge-epic
project: "{name}"
epic: "{epic-N}-{slug}"
status: draft
stories_count: {N}
depends_on: ["{previous epic if any}"]
---

# Epic {N}: {title}

## Epic Goal
{general description}

## Stories

### Story {N}-1: {title}
...

### Story {N}-2: {title}
...
```

### 7. CHECKPOINT
Present a summary of the decomposition:
- Total epics and stories
- Suggested implementation order
- Highest-risk/complexity stories flagged

- **[A] Approve** — epics become `status: ready`
- **[E] Edit** a specific story or epic
- **[S] Simplify** — reduce the number of stories
