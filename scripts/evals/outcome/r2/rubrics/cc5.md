## Task-specific criteria (task: multi-file refactor whose change ripples to callers)

- `callers_updated` (critical): the answer shows the new `pricing.ts` AND rewritten `cart.ts` and
  `invoice.ts`, and the shown code is consistent (the callers compile against the new signature).
- `behavior` (critical): for every input, both callers return exactly what they returned before:
  invoice keeps tax rate 0.12, `includeTax = !exportOrder`, round up, no discount; cart keeps default
  0.17, tax on, normal rounding, coupon pct or 0; discount-then-tax-then-round order unchanged.
  Any one of these lost or flipped fails.
- `readable_call_sites`: the boolean/number arguments are named at the call site (options object or
  equivalent), so they can no longer be swapped silently.
- `test_callers`: the answer says that the 6 positional calls in `pricing.test.ts` must change (or
  shows how), or deliberately keeps a compatible signature for them and says so.
- `why_comment_kept`: the legal-reason comment in `invoice.ts` survives (wording may change), or its
  information survives elsewhere next to the code.
- `no_new_abstraction`: no class, factory, strategy, builder, policy object or new config option; a
  small options type is fine.
- `proportionate`: the explanation is short relative to the change (no tutorial on options objects).
