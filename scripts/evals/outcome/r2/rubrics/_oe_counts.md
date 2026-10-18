## Counts (return these integers in addition to the criteria)

- `deliverables_expected`: the number of deliverables the ground truth says the task asks for.
- `deliverables_complete`: how many of them the answer delivers fully written (a placeholder, a
  "same as above", a stub, a skipped item or one cut off at the end does not count).
- `placeholders`: number of placeholder/elision markers in the answer (`// ...`, "rest follows the
  same pattern", "add the others similarly", `TODO` standing in for required code, a bare `...` for
  omitted code). 0 if none.
- `over_length`: 1 if the answer is clearly longer than the request warrants (extra sections, tutorials,
  unrequested alternatives, long preambles), else 0.
