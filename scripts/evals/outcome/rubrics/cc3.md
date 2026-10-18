## Task-specific criteria (task: fix a bug and explain it)

Ground truth: `ids.forEach(async ...)` does not await the async callbacks; `forEach` ignores the
returned promises, so `return total` runs before any `await db.getItem` resolves and the function
resolves with 0. (Also: rejections inside the callbacks are unhandled.)

- `root_cause` (critical): the explanation names the real root cause: `forEach` does not wait for
  async callbacks, so the function returns before the additions happen. Explanations blaming
  something else (e.g. closures, `let`, db returning strings) fail.
- `fix_correct` (critical): the fixed code returns the correct sum: e.g. `Promise.all` over the ids
  then summing, or a `for...of` loop with `await`. Code that still races or does not compile fails.
- `signature`: the exported signature `totalStock(ids: string[]): Promise<number>` is unchanged.
- `concise_explanation`: the root cause is stated in a few sentences, without a long tutorial
  (roughly under 150 words of prose).
- `no_scope_creep`: no unrelated changes (no new caching layer, retry logic, logging framework,
  new abstractions). A brief optional note about sequential vs parallel or error propagation is fine.
