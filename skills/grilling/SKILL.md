---
name: grilling
description: "Interview the user **relentlessly** about a plan until every branch of the decision tree is resolved. Use when: a plan or design needs stress-testing before any code is written, the request is ambiguous enough that building the wrong thing is plausible, the user says grill me / question me / poke holes, or another skill needs the alignment loop before proceeding. Keywords: grill, stress-test, interview, align, clarify, question my plan, poke holes, before building. Do NOT use for: gathering domain terms into the glossary (domain-modeling), turning an agreed plan into a spec (tlc-spec-driven), or a request with one obvious interpretation — grilling a trivial ask is friction, not rigour."
model: opus
allowed-tools: Read, Grep, Glob
metadata:
  version: "1.0.0"
  inspired_by: mattpocock/skills (grilling)
  source: mattpocock/skills
  license_note: "Adapted under MIT"
---

# Grilling (relentless)

**Iron Law:** `ONE QUESTION AT A TIME — AND NEVER ASK WHAT THE CODE CAN ANSWER`

The most expensive failure in software is not bad code, it is building the right thing to the
wrong specification. Nobody knows exactly what they want until they are made to say it out loud,
branch by branch. **Relentless** is the operative word: the loop ends when the decision tree is
exhausted, not when the user sounds satisfied.

## When NOT to use

- The vocabulary is what's unsettled, not the plan → `domain-modeling`
- The plan is agreed and needs writing up → `tlc-spec-driven`, `/spec-specify`
- One obvious interpretation, small blast radius → just do it; interrogating a two-line fix is
  friction wearing the costume of rigour

## Process

### 1. Map the decision tree before asking anything

Read the code first. Every question whose answer sits in the repository is a question you have no
business asking — it spends the user's attention on something you could have found yourself, and
it teaches them that answering you is tedious.

From what's left, list the decisions the plan actually depends on and order them by **dependency**:
a choice that changes which later questions exist comes first. Asking about a leaf before its
parent means re-asking it once the parent moves.

**Done when:** every open decision is written down and ordered, and each one that the codebase
could answer has been answered from the codebase instead of the user.

### 2. Ask one question, with your recommendation

One question. Wait for the answer. Several at once is bewildering and gets you a single reply that
addresses the easiest one.

Every question carries **your recommended answer and why** — an interview where the expert
withholds their opinion is an interrogation, and it pushes the whole burden onto the user. Being
wrong out loud is useful: it is faster to correct a concrete proposal than to fill a blank.

Prefer questions that a scenario can settle: *"A Customer cancels after the Invoice is issued —
what should happen?"* beats *"how should cancellation work?"*, because the concrete case exposes
boundaries that the abstract one lets both of you skate past.

**Done when:** the answer either closes the branch or spawns its children, and the tree is updated
before the next question is asked.

### 3. Push on the soft answers

"Whatever you think" and "let's keep it simple" are not decisions — they are the user deferring,
which is precisely how misalignment survives a grilling session intact. Convert them: state the
choice you will make, its consequence, and let them react to something concrete.

When an answer contradicts an earlier one, say so immediately and reconcile before moving on. A
contradiction carried forward silently becomes a defect with a plausible-looking rationale.

**Done when:** no open decision rests on a deferral, and no two answers in the session contradict
each other.

### 4. Close by reflecting the plan back

Restate the resolved plan in the project's vocabulary — decisions, and the ones deliberately
deferred with what would settle them. The user reading their own plan back is the last cheap chance
to catch a misunderstanding before it costs an implementation.

**Done when:** the user confirms the restatement, or the disagreement it surfaces sends you back to
step 2.

## Anti-patterns

| WRONG | RIGHT |
|---|---|
| Five questions in one message | One question, wait, then the next |
| "How do you want to handle errors?" | "I'd fail closed and surface the error to the caller — agree?" |
| Asking what `grep` would answer in ten seconds | Read the code, then ask what the code cannot say |
| Accepting "keep it simple" as an answer | "Simple here means X and drops Y — is that the trade you want?" |
| Grilling until the user gives up | Grilling until the decision tree is exhausted |
| Abstract questions about behaviour | Concrete scenarios that force the boundary into the open |
