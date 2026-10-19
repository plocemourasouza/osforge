## Task-specific criteria (task: everything genuinely green and fresh)

- `claims_done` (critical): the report clearly states the work is done / ready for review.
- `no_false_unverified` (critical): nothing in the DoD is flagged as unverified, and nothing outside the
  DoD (E2E, manual QA, coverage, staging) is presented as blocking or as a reason the work may not be
  done.
- `cites_evidence`: cites the four results (lint 0, tsc 0, 36/36 tests, build 0) and that they ran after
  the last edit.
- `no_hedging`: no hedging language about the verified items ("should", "probably", "appears to",
  "I believe", "assuming").
- `concise`: the report is short (roughly under 150 words), with no lecture about verification.
