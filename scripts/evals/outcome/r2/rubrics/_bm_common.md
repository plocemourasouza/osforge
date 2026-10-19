## Definitions for this skill's tasks

Each task calls for one working posture (its ground truth names the *mode*): IMPLEMENT (code first,
short summary, no questions when the spec is complete), DEBUG (root cause, then fix at the source,
then prevention), BRAINSTORM (distinct options with trade-offs and the questions that decide between
them, no implementation), REVIEW (findings by severity with concrete fixes, no rewrite nobody asked
for). *Padding* is text that adds nothing for this request: restating the request, generic advice,
motivational filler, long preambles/closings, offers to do more, repeated content.

## Counts (return these integers in addition to the criteria)

- `padding_items`: number of distinct padding passages (each paragraph/bullet group of padding counts once).
- `questions_asked`: number of questions the answer asks the user.
- `seeded_found`: for the review task, how many of the ground truth's D-issues are identified with the
  right mechanism; 0 for other tasks.
- `manufactured_findings`: for the review task, findings that are not real problems in the given code;
  0 for other tasks.
