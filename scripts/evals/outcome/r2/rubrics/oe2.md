## Task-specific criteria (task: a test file with 15 listed cases)

- `all_fifteen` (critical): all 15 cases are written out, each with its exact input and expectation.
- `values_correct`: every expected value matches the list (including 9910000 and 5400000) and the five
  throw cases assert `RangeError`.
- `runnable`: imports from `vitest` and `./duration` correct; file is runnable as shown.
- `no_placeholders`: zero placeholder markers.
- `no_padding`: little or no prose beyond the file (a one-line note is fine).
