Deliverables expected: 15 test cases, each its own `it(...)` (or `it.each` rows only if every one of
the 15 rows is written out explicitly with its exact input and expectation), with the exact inputs and
expected values above. Values check: 2h45m10s = 7,200,000 + 2,700,000 + 10,000 = 9,910,000;
1.5h = 5,400,000. Throw cases must assert `RangeError` (e.g. `expect(() => parseDuration("")).toThrow(RangeError)`).
Import: `import { describe, it, expect } from "vitest"` and `import { parseDuration } from "./duration"`.
A case is complete only if it is written out; "add the rest similarly" or a loop over a partial list
does not count for the missing cases.
