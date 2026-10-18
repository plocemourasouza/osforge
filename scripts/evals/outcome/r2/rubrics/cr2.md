## Task-specific criteria (task: review a clean diff)

- `no_blocking_findings` (critical): no finding is rated blocking/critical/warning/must-fix; the review
  does not request changes.
- `clear_verdict`: an explicit approve / LGTM verdict.
- `low_noise`: at most two optional suggestions, each labelled optional/minor, and each grounded in the
  code shown (e.g. calendar days vs 24h periods, one more boundary test).
- `shows_work`: briefly says what was checked (boundary, paid case, purity/testability) so the approval
  is credible.
