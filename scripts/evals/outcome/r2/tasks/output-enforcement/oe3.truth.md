Answer: it switches to the previously checked-out branch (like `cd -`; same as `git checkout -`,
i.e. `@{-1}`). If the previous checkout was a detached HEAD, `git switch -` refuses unless `--detach`
is given (an optional detail).
Expected length: one to three sentences. A trivial question deserves a short answer — headings,
multi-section explanations, tables, or a list of unrelated `git switch` options are over-length.
Deliverables expected: 1 (the answer).
