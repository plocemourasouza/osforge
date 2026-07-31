# ADR — format and the test for writing one at all

Adapted from `mattpocock/skills` (grill-with-docs/ADR-FORMAT.md), MIT.

## The three-part test

Write an ADR only when **all three** hold. Any one missing → no ADR, and saying so out loud is
part of the job.

1. **Hard to reverse** — changing your mind later costs real work or real money.
2. **Surprising without context** — a future reader will ask "why on earth was this done this way?"
3. **A genuine trade-off** — real alternatives existed and one was chosen for stated reasons.

Failing the test is the normal case. "We used Zod because we already use Zod" is not an ADR. The
value of the record collapses the moment everything becomes one.

## Where it goes

OSForge already has a home for decisions — do not create a second one:

```bash
osforge-db add-decision <slug> "<title>" --context "..." --decision "..." --consequences "..."
```

Projects without the DB: append to `.specs/project/DECISIONS.md`. The OSForge repo itself uses
`docs/DECISIONS.md` for decisions about the framework.

## Shape

```md
## ADR-00N: {Decision in one line, in the ubiquitous language}

**Status:** accepted | superseded by ADR-00M | proposed
**Date:** YYYY-MM-DD

### Context
What was true that forced a choice. Constraints, pressures, what was already committed to.
Written so someone who was not in the room can reconstruct the situation.

### Decision
What was chosen, stated actively: "We store Orders as an append-only event log."

### Alternatives considered
- **{Alternative}** — why it was rejected. One line each.
  An ADR with no alternatives failed test 3 and should not exist.

### Consequences
What this makes easy, and what it makes hard. The second half is the one people skip and the one
future readers need — an ADR that lists only benefits reads as advocacy, not as a record.
```

## Rules

- **Use the glossary.** An ADR written in words that are not in `CONTEXT.md` either uses the wrong
  words or reveals a term that belongs in the glossary. Both are worth fixing on the spot.
- **One decision per ADR.** Two decisions in one record cannot be superseded independently.
- **Never edit an accepted ADR to change its decision.** Write a new one and mark the old one
  superseded. The trail of what was believed and when is the artefact.
- **Record a rejection when it will otherwise be re-proposed.** "We are not doing X, because Y" is
  a legitimate ADR when Y is not obvious — it is what stops the same suggestion returning every
  quarter. Ephemeral reasons ("no time right now") do not qualify.
