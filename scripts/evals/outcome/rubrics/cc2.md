## Task-specific criteria (task: review and restructure a deeply nested function)

Ground truth facts about the original `processOrder`:
- Check order: null order -> throw "No order"; no customer -> throw "Order has no customer";
  blocked -> status "blocked", notify "Your account is blocked", total 0 (checked BEFORE the empty
  items check); empty/missing items -> status "empty", total 0, no notify.
- Line totals: items with qty <= 0 are skipped. Tax multiplier by category x country (BR / not BR):
  food 1.07/1.12, electronics 1.18/1.2, other 1.1/1.15.
- Tier: gold -> x0.95 only if total > 500; platinum -> x0.9 if > 500 else x0.95; basic -> none.
- Coupon: WELCOME10 -> minus 10 only if total > 100; FREESHIP -> no change; any other non-empty
  coupon -> status "invalid_coupon", notify "Coupon <code> is invalid", return total 0 (before rounding).
- Then round to cents; > 10000 -> "needs_review" + notify under review; else "confirmed" + notify confirmed.
- It mutates the input (`order.status = ...`).

Criteria:
- `nesting`: identifies the deep nesting as a problem and restructures with guard clauses / early returns.
- `duplication`: identifies the duplicated tax computation (six near-identical branches) and
  consolidates it (e.g. a rate lookup), without changing any rate.
- `side_effect`: flags that the function mutates its input (`order.status`) as a side effect /
  hidden coupling, and either preserves it deliberately (and says so) or removes it with a note.
- `behavior` (critical): the restructured code preserves every fact listed above: same returns,
  same thrown messages, same `notify` calls under the same conditions, same check order (blocked
  before empty), same thresholds (strict `>`), same rounding point. Any deviation fails.
- `no_new_abstraction`: no class hierarchy, strategy pattern, plugin/registry or extra layers
  beyond small helper functions or a constant table that remove real duplication.
- `magic_numbers`: names or tabulates the magic numbers (rates, 500, 100, 10, 10000), or explicitly
  flags them.
