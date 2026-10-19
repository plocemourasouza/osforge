## Task-specific criteria (task: refactor an over-engineered shipping module)

Ground truth: the whole module is a two-branch conditional. BR costs `5 + 1.2*kg`; any other
country costs `15 + 3.5*kg`. `orderTotal(subtotal, countryCode, weightKg)` is the only consumer.

- `behavior` (critical): the refactored code returns exactly the same cost for BR and for every
  non-BR code, and `orderTotal` keeps its signature and result. Any changed formula, changed
  default branch, or compile error fails.
- `simplified`: the strategy interface, both strategy classes, the factory and the calculator class
  are replaced by a plain function (or equivalent single construct). Keeping any of them fails.
- `no_new_abstraction`: the answer introduces no new abstraction layer (no new class, interface,
  registry/map-of-handlers, plugin point, generic config object, or extra file). Named constants
  for the rates and a union type are fine.
- `call_site`: the answer states correctly what changes in `checkout.ts` (import a function instead
  of instantiating a class) and shows or describes it correctly.
- `proportionate`: prose outside code is proportionate to a small refactor (no tutorial on design
  patterns; roughly under 200 words).
