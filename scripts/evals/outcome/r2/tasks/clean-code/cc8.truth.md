Root cause: in `paginate`, `end = start + pageSize + 1`; `Array.prototype.slice` excludes `end`, so
each page returns `pageSize + 1` items, and the extra item is the first item of the next page — page 2
therefore starts with the last item shown on page 1.
Fix: `end = start + pageSize` (equivalently `items.slice(start, start + pageSize)`); `start` is already
correct (`(page - 1) * pageSize`).

Scope: `getPageCount` (nested ifs, `var`, `!=`) and `rangeLabel` (`let`, `==`, string concatenation)
are ugly but behave correctly. They are out of scope for this bug: a correct answer leaves them as
they are (at most mentions them briefly as optional follow-ups). Rewriting them in the same change is
scope creep, even if the rewrite is behaviour-preserving. Rewriting `paginate` lightly (e.g. computing
start as `(page - 1) * pageSize`) is fine.
