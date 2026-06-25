# Plan — <feature name>

> Produced in **Plan Mode** (read-only). This plan is a **dispatch manifest**: it binds every task to a
> model, agent, skills, and wave so multiple agents can execute it in parallel from a single plan.
> Authored in English (ADR-011); the user is replied to in their language.

**Triage:** QUICK | STANDARD | COMPLEX
**Slug:** `<kebab-slug>`  ·  **Source request:** <1-line of what the user asked>

## 1. Objective
<1–2 sentences: the outcome, in user/product terms.>

## 2. Feature structure
- **Modules / seams** (codebase-design vocabulary): <module → interface → seam>
- **Data model**: <new/changed models, relations, migrations>
- **API surface**: <routes / server actions / contracts>

## 3. User stories
- **US-01** — As a <role>, I want <capability> so that <value>.
  - AC: <testable acceptance criterion>
  - AC: <…>
- **US-02** — …

## 4. Roster (declared up front)
- **Models:** <e.g., sonnet (impl), haiku (tests)>
- **Agents:** <e.g., backend-engineer, test-engineer>
- **Skills:** <e.g., asaas-integration, prisma-expert, security-best-practices>

## 5. Task manifest
> Atomic, self-contained tasks. Each is dispatchable on its own.

### T-01 — <title>
- story:       US-01
- wave:        1
- depends_on:  []
- model:       sonnet            # haiku | sonnet | opus | fable (smart-model-dispatch)
- agent:       <agent-name>
- skills:      <skill>, <skill>
- files:       <path>, <path>
- done when:   <checkable, exhaustive criterion>
- verify:      <command / test that proves it>

### T-02 — <title>
- story:       US-01
- wave:        1
- depends_on:  []
- model:       haiku
- agent:       <agent-name>
- skills:      <skill>
- files:       <path>
- done when:   <…>
- verify:      <…>

### T-03 — <title>
- story:       US-02
- wave:        2
- depends_on:  [T-01]
- model:       sonnet
- agent:       <agent-name>
- skills:      <skill>, <skill>
- files:       <path>
- done when:   <…>
- verify:      <…>

## 6. Execution plan (waves)
- **Wave 1 (parallel):** T-01, T-02
- **Wave 2 (parallel):** T-03, T-04   ← starts only after Wave 1 closes
- **Wave 3:** T-05
> Default autonomy: **checkpoint per wave** — report results and stop for review before the next wave.

## 7. Risks & rollback
- <risk> → <mitigation / rollback step>

## 8. Out of scope
- <explicitly excluded>

## 9. Verification (whole feature)
- <end-to-end check: full suite green, typecheck exit 0, e2e of the main flow, etc.>
