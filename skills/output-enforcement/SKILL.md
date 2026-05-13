---
name: output-enforcement
description: >
  Garante output completo e exaustivo. Bane padrões de truncation ("// ... rest of code",
  "// TODO", "for brevity"), placeholders, e respostas pela metade. ACIONE quando o usuário
  pede arquivo completo, múltiplos componentes, refactor extenso, ou qualquer task longa
  onde compressão/preguiça do modelo seria falha crítica. Triggers: "completo", "todo o
  arquivo", "implementação inteira", "sem placeholders", "não corte", "exaustivo".
version: 1.0.0
inspired_by: Leonxlnx/taste-skill (output-skill) — MIT, 10k+ stars
metadata:
  source: "Leonxlnx/taste-skill"
  category: "meta-quality"
allowed-tools: Read, Write, Edit
---

# Full-Output Enforcement — Anti-Laziness Directive

## Baseline

Treat every task as production-critical. A partial output is a broken output.
Do NOT optimize for brevity — optimize for completeness.

- User asks for full file → deliver full file.
- User asks for 5 components → deliver 5 components.
- User asks for refactor of 10 functions → refactor all 10.
- No exceptions.

## Banned Output Patterns (HARD FAILURES)

### In code blocks
- `// ...`
- `// rest of code`
- `// implement here`
- `// TODO` (unless explicitly part of the deliverable)
- `/* ... */`
- `// similar to above`
- `// continue pattern`
- `// add more as needed`
- bare `...` standing in for omitted code

### In prose
- "Let me know if you want me to continue"
- "I can provide more details if needed"
- "for brevity"
- "the rest follows the same pattern"
- "similarly for the remaining"
- "and so on" (when replacing actual content)
- "I'll leave that as an exercise"

### Structural shortcuts
- Outputting a skeleton when the request was for a full implementation
- Showing first and last section while skipping the middle
- Replacing repeated logic with one example + a description
- Describing what code should do instead of writing it

## Execution Process

### 1. SCOPE
Read the full request. Count distinct deliverables expected (files, functions, sections, answers).
Lock that number explicitly.

> Example: "User asked for 3 React components + 1 test file + 1 README → SCOPE = 5 deliverables."

### 2. BUILD
Generate every deliverable completely. No partial drafts. No "you can extend this later."

### 3. CROSS-CHECK
Before output, re-read the original request. Compare deliverable count against SCOPE.
If anything is missing → add it before responding.

## Handling Long Outputs (when token limit looms)

When response approaches the token limit:

1. Do NOT compress remaining sections to squeeze them in.
2. Do NOT skip ahead to a conclusion.
3. Write at FULL QUALITY up to a clean breakpoint (end of function, end of file, end of section).
4. End with this exact marker:

```
[PAUSED — X of Y complete. Send "continue" to resume from: <next section name>]
```

On "continue" → pick up exactly where stopped. No recap. No repetition.

## Pre-Output Verification

Before finalizing ANY long response, verify:

- [ ] No banned patterns from the lists above appear ANYWHERE
- [ ] Every item the user requested is present and finished
- [ ] Code blocks contain runnable code, not descriptions of code
- [ ] Nothing was shortened to "save space"
- [ ] SCOPE count matches deliverables count
- [ ] If paused: clean breakpoint + exact resume marker

## When This Skill Activates

Auto-activate for:
- Multi-file refactors / generations
- Long code reviews where every issue must be addressed
- Documentation generation (README, API docs, ADRs)
- Multi-component generation (e.g., "create 5 components")
- Full-page implementations
- Migration tasks (rename, restructure, type-tighten)
- Any task where the user uses words like "completo", "todo", "inteiro", "exaustivo",
  "sem cortar", "sem placeholder", "no shortcuts"

## Interaction with Other Skills

- **`verification-before-completion`** — output-enforcement guarantees deliverables exist;
  verification-before-completion guarantees they work. Run both.
- **`tdd-workflow`** — output-enforcement applies to test files too. If 5 tests are needed,
  write all 5 — no `// similar test for case Y`.
- **`technical-design-doc-creator`** — every required section in the TDD must be fully written.

---

## Related Skills
- `verification-before-completion` — verify deliverables actually work
- `tdd-workflow` — TDD discipline including complete test suites
- `clean-code` — code quality standards for the output
