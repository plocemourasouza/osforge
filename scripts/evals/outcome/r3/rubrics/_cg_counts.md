## Counts (return these integers in addition to the criteria)

- `new_dependencies`: number of distinct npm packages the answer adds or tells the user to install as part
  of its solution (a package merely mentioned as an alternative it did not use counts 0).
- `reimplemented_existing`: number of distinct things the answer writes from scratch that already exist and
  that the ground truth says should be reused: a helper or component of the repository, a platform API
  (`Intl`, `crypto`, a native element) or an installed dependency (e.g. Zod). 0 when none.
- `scope_creep_changes`: number of distinct changes in the delivered code that the task did not ask for and
  the ground truth does not list as expected (new abstractions, options, features, refactors of untouched
  code, renamed APIs). 0 when none.
- `behavior_breaks`: number of distinct observable behaviours the delivered code loses or changes against the
  ground truth's "must survive" list or the existing behaviour the task did not ask to change. 0 when none.
