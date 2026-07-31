---
name: domain-modeling
description: "Build and sharpen a project's **ubiquitous language** in CONTEXT.md — one canonical term per concept, aliases banned. Use when: naming a new concept or module, two words are being used for the same thing, a term is being used for two different things, the code and the conversation disagree about what something is called, or another skill needs the project's vocabulary before naming anything. Keywords: glossary, ubiquitous language, domain model, terminology, naming, CONTEXT.md, bounded context. Do NOT use for: architecture decisions and module seams (codebase-design), writing a spec (tlc-spec-driven), documenting an API (docs-writer), general renaming for style (clean-code)."
model: sonnet
allowed-tools: Read, Grep, Glob, Edit, Write
metadata:
  version: "1.0.0"
  inspired_by: mattpocock/skills (grill-with-docs, domain-modeling)
  source: mattpocock/skills
  license_note: "Adapted under MIT; concepts from Eric Evans, Domain-Driven Design"
---

# Domain Modeling (ubiquitous language)

**Iron Law:** `ONE CONCEPT, ONE WORD — A SECOND WORD FOR THE SAME THING IS A BUG`

A project's glossary is not documentation. It is the vocabulary the agent thinks in: when
`CONTEXT.md` says the thing is an **Order**, then the variable, the table, the test name, the
commit message and the conversation all say Order. That single decision is what stops an agent
from writing twenty words where one would do, and what makes a codebase navigable in one pass
instead of three.

## Where the glossary lives (two levels, same shape)

Mirrors the memory hierarchy of `CLAUDE.md`: the more specific level wins.

| Level | File | Holds | Loaded |
|---|---|---|---|
| **Global** | `~/.claude/CONTEXT.md` | vocabulary shared across the whole portfolio | every session |
| **Project** | `<repo>/CONTEXT.md` | this codebase's domain terms | when the project is open |
| **Multi-context** | `<repo>/CONTEXT-MAP.md` → per-context files | a monorepo with several domains | via the map |

The project file sits beside the README — readable and editable by hand, reachable by any agent
whether or not the project uses `.specs/`.

**A project term overrides a global one with the same name**, and that override is worth saying out
loud: it is either a legitimate local meaning (record it, note the divergence) or a collision that
should be renamed. Never resolve it silently — a word that means two things across two levels is
the overload failure one level up.

**Promotion:** a term that shows up with the same meaning in three or more projects belongs in the
global file. Ask before promoting; the global file is loaded in every session, so each entry is
paid for everywhere.

## When NOT to use

- Deciding where a module boundary goes, or how deep an interface is → `codebase-design`
- Turning a decision into a spec or tasks → `tlc-spec-driven`, `/spec-specify`
- Renaming for style, dead code, over-abstraction → `clean-code`
- Recording *why* a decision was made → an ADR (see `references/ADR-FORMAT.md`)

## Process

### 1. Find the context

Resolve in order: `~/.claude/CONTEXT.md` (already in context) → `<repo>/CONTEXT.md` →
`CONTEXT-MAP.md` if the repo has several bounded contexts, in which case read the map and infer
which context the topic belongs to, asking if it is unclear.

Create nothing yet. Files are created **lazily**, when the first term is actually resolved — an
empty glossary is worse than none, because it looks answered.

**Done when:** you can name the level and context you are working in, or you have established that
this project has no glossary yet.

### 2. Harvest the candidate terms

Take the terms from the conversation and from the code that names the same area. For each one, ask
which of the three cases it is:

- **New** — a concept with no entry yet
- **Collision** — two words in use for one concept (the Iron Law violation)
- **Overload** — one word covering two concepts, which is the more dangerous case because nothing
  looks wrong until someone builds the wrong thing

**Done when:** every term raised in this conversation is classified as new, collision, overload, or
already-canonical — with none left unexamined.

### 3. Challenge, one term at a time

For each unresolved term, ask **one question and wait** (see the grilling rule in `CLAUDE.md`).
Offer your recommended answer with the question.

- Term conflicts with the glossary → say so immediately: *"Your glossary defines cancellation as
  X, but you seem to mean Y — which is it?"*
- Term is vague or overloaded → propose the precise canonical word: *"You said account — do you
  mean the Customer or the User? Those are different things."*
- Relationship is being described → stress-test it with a concrete edge-case scenario until the
  boundary between two concepts is forced into the open.
- The code disagrees with what was said → surface the contradiction with the file: *"This cancels
  whole Orders, but you just said partial cancellation exists — which is right?"*

If the answer is in the codebase, go read the codebase instead of asking.

**Done when:** every term from step 2 has one canonical word, and every rejected alias is written
down as an alias rather than forgotten.

### 4. Write it down as it happens

Update the glossary the moment a term is resolved — never batch it to the end of the session, where
it silently becomes never. Write to the **project** file unless the term is portfolio-wide and the
user agrees to promote it. Format: `references/CONTEXT-FORMAT.md`.

Create `<repo>/CONTEXT.md` on the first resolved term that is specific to this codebase. Signals
that a project needs its own file: a word here means something different from the global glossary,
or the domain has concepts the portfolio vocabulary cannot express.

`CONTEXT.md` is a glossary and nothing else. No implementation detail, no spec, no scratchpad, no
task list. The moment it accumulates other content, people stop reading it.

**Done when:** `CONTEXT.md` contains every term resolved in this session, each with its aliases to
avoid, and contains nothing that is not a term.

### 5. Offer an ADR only when it earns one

A decision earns an ADR when **all three** hold:

1. **Hard to reverse** — changing your mind later costs something real
2. **Surprising without context** — a future reader will ask "why on earth this way?"
3. **A genuine trade-off** — there were real alternatives and one was chosen for stated reasons

Any one missing → no ADR. Record it via `osforge-db add-decision` (or `.specs/project/DECISIONS.md`
in projects without the DB) using the shape in `references/ADR-FORMAT.md`. OSForge already has one
home for decisions; do not create a second one.

**Done when:** either an ADR is recorded, or you can state which of the three tests the decision
failed.

## Anti-patterns

| WRONG | RIGHT |
|---|---|
| Glossary written in one big pass at the end of the project | Terms captured the moment they are resolved, one at a time |
| Entry defines what the thing *does* | Entry defines what the thing *is*, in one or two sentences |
| "Order (also called Purchase, Transaction)" | "**Order**: … _Avoid_: Purchase, Transaction" — one canonical word, the rest banned |
| General programming terms in the glossary (timeout, retry, DTO) | Only concepts specific to this domain |
| Implementation notes creep into CONTEXT.md | Glossary only; decisions go to an ADR, specs go to `.specs/` |
| Renaming code to match a term nobody agreed to | Term settled with the user first, then the code follows |

## References

- `references/CONTEXT-FORMAT.md` — the file format, single vs multi-context repos, worked example
- `references/ADR-FORMAT.md` — ADR shape and the three-part test for writing one at all
