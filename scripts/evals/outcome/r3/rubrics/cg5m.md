## Task-specific criteria (task: receipt total disagrees with the charge; `lib/money.ts` has the shared `toCents`/`sumCents` but its file is not in the prompt)

- `reuses_existing_helper` (critical): the receipt uses the existing `toCents` or `sumCents` imported
  from `@/lib/...` (the exact file name is not graded); inline rounding or a new helper fails, even when the answer could not have known
  about `lib/money.ts`.
- `fixes_rounding` (critical): the `Math.ceil` workaround is gone and the receipt gives 330 for
  3 x R$ 1,10 and 1999 for R$ 19,99.
- `no_new_money_helper`: no new cents-conversion function or money module is created.
- `regression_test`: adds a test with a failing value (3 x 1.10 or 19.99).
- `proportionate`: no unrequested features or abstractions; the explanation is short relative to the change.
