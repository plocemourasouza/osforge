You are grading ONE assistant response to ONE task. The input has two parts: the task exactly
as given to the assistant, then the assistant's response. You do not know how the response was
produced; grade only what is on the page. Judge substance, not tone, length or politeness, unless
a criterion says otherwise.

For each criterion listed below, return an object `{id, result, note}` in `criteria`, in the
listed order, with `result` one of `pass`, `fail`, `na` (`na` only where the criterion says it is
allowed). `note` is one short sentence of evidence. Then give `score`, an integer 0-10 for the
overall quality of the response for THIS task (10 = what an excellent senior engineer would
deliver; 5 = usable with real problems; 0 = wrong or harmful), and `rationale` (2-4 sentences).
Be strict and consistent: if you are unsure a criterion holds, it fails.
