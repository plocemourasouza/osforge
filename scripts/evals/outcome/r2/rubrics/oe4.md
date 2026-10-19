## Task-specific criteria (task: twenty-item migration list)

- `all_twenty` (critical): all 20 items are present, numbered, each with real code.
- `behaviour_kept`: rewrites preserve behaviour for the inputs shown; at most one behaviour difference
  that is not noted (e.g. #19 not lowercasing the rest, #20 mutating `users` in place, #8 wrong chunks).
- `edge_notes_targeted`: notes appear only where behaviour actually differs (e.g. #11 `Object.groupBy`
  version, #20 mutation/stability), not on every line.
- `format_followed`: one line of code per item as requested.
- `no_placeholders`: zero placeholder markers.
