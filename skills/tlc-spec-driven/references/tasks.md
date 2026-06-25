# Phase 3: Tasks

**Goal**: Break into GRANULAR, ATOMIC tasks. Clear dependencies. Right tools. Parallel execution plan.

## Why Granular Tasks?

| Vague Task (BAD) | Granular Tasks (GOOD)             |
| ---------------- | --------------------------------- |
| "Create form"    | T1: Create email input component  |
|                  | T2: Add email validation function |
|                  | T3: Create submit button          |
|                  | T4: Add form state management     |
|                  | T5: Connect form to API           |
| "Implement auth" | T1: Create login form             |
|                  | T2: Create register form          |
|                  | T3: Add token storage utility     |
|                  | T4: Create auth API service       |
|                  | T5: Add route protection          |

**Benefits of granular:**

- **Agents don't err** - Single focus, no ambiguity
- **Easy to test** - Each task = one verifiable outcome
- **Parallelizable** - Independent tasks run simultaneously
- **Errors isolated** - One failure doesn't block everything

**Rule**: One task = ONE of these:

- One component
- One function
- One API endpoint
- One file change

---

## Process

### 1. Review Design

Read `.specs/[feature]/design.md` before creating tasks.

### 2. Break Into Atomic Tasks

**Task = ONE deliverable**. Examples:

- ✅ "Create UserService interface" (one file, one concept)
- ❌ "Implement user management" (too vague, multiple files)

### 3. Define Dependencies

What MUST be done before this task can start?

### 4. Create Execution Plan

Group tasks into phases. Identify what can run in parallel.

### 5. ASK About MCPs and Skills

**CRITICAL**: Before execution, ask the user:

> "For each task, which tools should I use?"
>
> **Available MCPs**: [list from project or user]
> **Available Skills**: [list from project or user]

---

## Template: `.specs/[feature]/tasks.md`

> **Machine-readable parallelism:** every task MUST include a YAML metadata block right after the header (`### TN:`). The block declares `id`, `depends_on`, `wave`, and `parallel_ok`.
> - **`wave`** is derived from the `depends_on` graph: tasks with no predecessors = wave 1; tasks that depend on wave N = wave N+1.
> - Tasks in the **same wave** with `parallel_ok: true` are dispatched in parallel by the orchestrator.
> - If two tasks in the same wave touch the same file, put them in different waves or in the same task — and mark `parallel_ok: false`.

```markdown
# [Feature] Tasks

**Design**: `.specs/[feature]/design.md`
**Status**: Draft | Approved | In Progress | Done

---

## Execution Plan

### Phase 1: Foundation (Sequential)

Tasks that must be done first, in order.

```
T1 → T2 → T3
```

### Phase 2: Core Implementation (Parallel OK)
After the foundation, these can run in parallel.

```
     ┌→ T4 ─┐
T3 ──┼→ T5 ─┼──→ T8
     └→ T6 ─┘
T7 ──────→
```

### Phase 3: Integration (Sequential)
Integrating everything.

```
T8 → T9
```

---

## Task Breakdown

### T1: [Create X Interface]

```yaml
id: T1
depends_on: []
wave: 1
parallel_ok: true
```

**What**: [One sentence: exact deliverable]
**Where**: `src/path/to/file.ts`
**Depends on**: None
**Reuses**: `src/existing/BaseInterface.ts`

**Tools**:

- MCP: `filesystem` (or NONE)
- Skill: NONE

**Done when**:

- [ ] Interface defined with all methods from design
- [ ] Types exported correctly
- [ ] No TypeScript errors

---

### T2: [Implement Y Service] [P]

```yaml
id: T2
depends_on: [T1]
wave: 2
parallel_ok: true
```

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts`
**Depends on**: T1
**Reuses**: `src/services/BaseService.ts` patterns

**Tools**:

- MCP: `filesystem`, `context7`
- Skill: NONE

**Done when**:

- [ ] Implements interface from T1
- [ ] Handles error cases from design
- [ ] Unit test passes

---

### T3: [Create Z Component] [P]

```yaml
id: T3
depends_on: [T1]
wave: 2
parallel_ok: true
```

**What**: [Exact deliverable]
**Where**: `src/components/ZComponent.tsx`
**Depends on**: T1
**Reuses**: `src/components/BaseComponent.tsx`

**Tools**:

- MCP: `filesystem`
- Skill: NONE

**Done when**:

- [ ] Component renders correctly
- [ ] Handles props from interface
- [ ] Follows existing component patterns

---

### T4: [Add A Feature to Y]

```yaml
id: T4
depends_on: [T2, T3]
wave: 3
parallel_ok: true
```

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts` (modify)
**Depends on**: T2, T3
**Reuses**: Existing service patterns

**Tools**:

- MCP: `filesystem`, `github`
- Skill: `api-design`

**Done when**:

- [ ] Feature works per acceptance criteria
- [ ] Integration test passes

---

## Parallel Execution Map

Visual representation of what can run simultaneously:

```
Wave 1 (Sequential — foundation):
  T1

Wave 2 (Parallel — T1 complete):
  ├── T2 [P]
  └── T3 [P]  } Dispatched simultaneously

Wave 3 (Sequential — T2 + T3 complete):
  T4 → T5 → ...
```

---

## Task Granularity Check

Before approving tasks, verify they are granular enough:

| Task                            | Scope         | Status       |
| ------------------------------- | ------------- | ------------ |
| T1: Create email input          | 1 component   | ✅ Granular  |
| T2: Add validation function     | 1 function    | ✅ Granular  |
| T3: Create form with all fields | 5+ components | ❌ Split it! |
| T4: Connect to API              | 1 function    | ✅ Granular  |

**Granularity check**:

- ✅ 1 component / 1 function / 1 endpoint = Good
- ⚠️ 2-3 related things in same file = OK if cohesive
- ❌ Multiple components or files = MUST split

---

## Tips

- **[P] = Parallel OK** - Mark tasks that can run simultaneously
- **Reuses = Token saver** - Always reference existing code
- **Tools per task** - MCPs and Skills prevent wrong approaches
- **Dependencies are gates** - Clear what blocks what
- **Done when = Testable** - If you can't verify it, rewrite it

---

## Task Verification Standards

Every task MUST include:

**Done when checklist:**

- Specific, testable outcomes
- Pass/fail criteria
- Test execution commands

**Verify section:**

- Commands to prove functionality
- Expected outputs
- Success indicators

**Structure:**

```markdown
### T1: [Task name]

```yaml
id: T1
depends_on: []
wave: 1
parallel_ok: true
```

**What:** [Deliverable]
**Where:** [File path]

**Done when:**

- [ ] [Specific outcome]
- [ ] [Specific outcome]
- [ ] Tests pass: [command]

**Verify:**
[Command to prove it works]
[Expected output/behavior]
```

**Quality check:**

- Can task be verified without human judgment?
- Is success criteria binary (pass/fail)?
- Can verification be automated?
