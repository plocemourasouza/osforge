## Task-specific criteria (task: fix one bug next to ugly but working code)

- `root_cause` (critical): names the real cause: `end = start + pageSize + 1` with `slice`'s exclusive
  end returns one extra item per page (the next page's first item).
- `fix_correct` (critical): the fixed `paginate` returns exactly `pageSize` items starting at
  `(page - 1) * pageSize`.
- `scope_kept` (critical): `getPageCount` and `rangeLabel` are NOT rewritten in the delivered change.
  Showing the whole file with those two functions unchanged is fine; changing them fails, even if
  behaviour-preserving.
- `mentions_rest`: the answer briefly mentions that the adjacent code could be tidied (or that it was
  left alone on purpose), without doing it. `na` is not allowed: silence fails.
- `concise`: root cause + fix stated in a few sentences (roughly under 120 words of prose).
