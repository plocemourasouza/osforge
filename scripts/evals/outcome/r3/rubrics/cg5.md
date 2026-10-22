## Task-specific criteria (task: cart total rounds wrong; bug in the shared `lib/money.ts`, 3 callers, one with a local workaround)

- `fix_in_shared_helper` (critical): the fix is made once in `toCents` (rounding instead of flooring the
  float, or an exact conversion); per-caller patches instead of the helper fail.
- `handles_local_workaround` (critical): the `Math.ceil` workaround in `lib/receipt.ts` is found and
  replaced by the shared helper (or the stored `unitCents`), so the receipt matches the charge.
- `all_callers_checked`: the answer accounts for every caller (cart, checkout, receipt) and states which
  need no change.
- `regression_test`: adds tests with the failing values (e.g. 19.99 -> 1999, 1.10 -> 110).
- `no_scope_creep`: no money library, no Decimal-everywhere refactor, no renamed helpers, no unrelated edits.
