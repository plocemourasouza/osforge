## Task-specific criteria (task: clean a file of noise without changing behavior)

Ground truth: removable noise = restating comments ("This is the currency code type", "DEBUG flag",
"function to format amount", "divide cents by 100", "check debug", "return formatted", "parse the
int", "helper to get today's date"); the commented-out `formatAmountOld`; the always-false `DEBUG`
flag and its `console.log` block; the unreachable `return 0` after `throw`; the unused `today()`
function and its now-unused `date-fns` import; the unused `roundHalfEven()` and its now-unused
`decimal.js` import. The comment explaining v2 vs v1 webhook formats is a meaningful "why" comment.

- `behavior` (critical): `formatAmount` and `parseWebhookAmount` keep identical signatures and
  outputs for all inputs (including throwing the same error message on NaN), and both stay exported.
- `comments_removed`: the restating comments are removed (at most one trivial one left).
- `why_comment_kept`: the v2/v1 webhook-format comment (or an equivalent explanation) is kept.
- `dead_code_removed`: ALL of these are removed: `formatAmountOld` comment block, `DEBUG` + its
  block, unreachable `return 0`, `today()` + `date-fns` import, `roundHalfEven()` + `decimal.js` import.
  Missing any one fails.
- `no_additions`: no new functionality, abstractions, validation or dependencies are added.
- `accurate_list`: the list of removals matches what was actually removed.
