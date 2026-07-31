# CONTEXT.md — format

Adapted from `mattpocock/skills` (grill-with-docs/CONTEXT-FORMAT.md), MIT.

## Shape

```md
# {Context name}

{One or two sentences: what this context is and why it exists.}

## Language

**Order**:
A customer's request for goods, from placement until fulfilment.
_Avoid_: Purchase, Transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, Payment request

**Customer**:
A person or organisation that places Orders.
_Avoid_: Client, Buyer, Account

## Relationships

- A **Customer** places many **Orders**
- An **Order** produces exactly one **Invoice** on fulfilment

## Flagged ambiguities

- "account" meant both the billing entity and the login identity — resolved:
  the billing entity is the **Customer**, the login identity is the **User**.

## Example dialogue

> **Dev:** When a Customer cancels an Order after the Invoice is issued, what happens?
> **Domain expert:** The Invoice is credited, not deleted — we keep the record.
> **Dev:** So "cancel" applies to the Order, and the Invoice gets a Credit Note?
> **Domain expert:** Right. We never cancel an Invoice.
```

## Rules

- **Be opinionated.** When several words exist for one concept, pick one and list the rest under
  `_Avoid_`. A glossary that accepts synonyms has failed at its only job.
- **Define what it IS, not what it does.** One or two sentences. A definition that runs to a
  paragraph is a spec in disguise.
- **Only domain-specific concepts.** Before adding a term ask: is this unique to this project, or
  general programming? Timeout, retry, DTO, repository — out, however much the code uses them.
- **Flag ambiguities explicitly**, with the resolution. The record of *what was confusing* is worth
  as much as the definition, because it stops the same argument recurring.
- **Show relationships** with cardinality where it is obvious.
- **Write the example dialogue.** It is the part that catches boundaries a list of definitions
  hides — two terms can each look well-defined and still collide in a real scenario.
- **Group under subheadings** when natural clusters appear; a flat list is fine while the glossary
  is small.

## Two levels

| Level | File | Scope | Cost |
|---|---|---|---|
| Global | `~/.claude/CONTEXT.md` | terms recurring across the portfolio | loaded every session — keep it short |
| Project | `<repo>/CONTEXT.md` | this codebase's domain | loaded when the project is open |

Source of the global file: `claude-code/CONTEXT.md` in the OSForge repo, deployed by `./deploy.sh`.
Edit it there, never in `~/.claude/`.

The more specific level wins. When a project redefines a global term, say so explicitly in the
project file:

```md
**Wave**:
In this repo, a marketing send window — NOT the OSForge dispatch group.
_Avoid_: batch. See the global glossary for the framework meaning.
```

A term reaching three projects with one meaning is a candidate for promotion to the global file —
ask before promoting, because every global entry is paid for in every session.

## Single vs multiple contexts

**Single context** — most repos: one `CONTEXT.md` at the root.

**Multiple contexts** — typically a monorepo: `CONTEXT-MAP.md` at the root points at each one and
states how they relate.

```md
# Context map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — issues invoices and processes payments

## Relationships

- **Ordering → Billing**: Ordering emits `OrderFulfilled`; Billing consumes it to issue an Invoice
- **Ordering ↔ Billing**: shared types for `CustomerId` and `Money`
```

Resolution order: `CONTEXT-MAP.md` exists → read it to find the contexts. Only a root `CONTEXT.md`
→ single context. Neither → create the root file lazily, when the first term is resolved.

## Where this sits among the other files

| File | Holds | Written by |
|---|---|---|
| `~/.claude/CONTEXT.md` | what things are called across the portfolio | `domain-modeling` (via the repo) |
| `<repo>/CONTEXT.md` | what things are called in this codebase | `domain-modeling` |
| ADR (`osforge-db add-decision`) | why a hard-to-reverse choice was made | `domain-modeling`, `codebase-design` |
| `.specs/features/<f>/` | what is being built now | `/spec-*` |
| `README.md` | how to run the thing | humans |

Keeping these apart is what stops `CONTEXT.md` from turning into a dumping ground — the failure
mode that makes a glossary unreadable and therefore unread.
