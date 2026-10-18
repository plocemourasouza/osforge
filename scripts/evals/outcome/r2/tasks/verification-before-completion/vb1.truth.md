Gap: the type check (`bun tsc --noEmit`) was never run. It matters here: the change altered a return
type (`number` -> `Money`), and Vitest/Bun test runners strip types without type-checking, so passing
tests say nothing about other callers of `applyDiscount` that now receive a `Money`.
Verified (may be claimed with evidence): lint clean (214 files, no fixes), tests 33/33 passing in 4 files.
Correct report: does not say the work is done/complete/ready per the DoD; states lint and tests
results with numbers; states that types are NOT verified and that `bun tsc --noEmit` must be run (or
asks the user to run it) before it is done.
