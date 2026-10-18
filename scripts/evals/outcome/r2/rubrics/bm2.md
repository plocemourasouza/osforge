## Task-specific criteria (task: debug request with a stack trace)

- `root_cause` (critical): states that the API returns `[]` (not `{ orders: [] }`) when there are no
  orders, so `data.orders` is undefined for users with no orders (new accounts).
- `fix_at_source` (critical): the proposed fix makes the API always return `{ orders }`. A client-side
  guard alone fails; a client guard in addition to the source fix passes.
- `fit_to_mode`: structured as diagnosis (symptom/root cause) -> fix -> prevention; does not ask for
  information already given.
- `prevention`: proposes a concrete prevention (typed/validated response contract, test for the empty
  case).
- `no_padding`: no padding passages.
