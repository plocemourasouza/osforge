## Task-specific criteria (task: plan a refactor with a hidden dependency)

- `found_token_incompat` (critical): the plan identifies that callers pass moment format tokens and that
  these must be translated to date-fns tokens (at least one concrete example such as `YYYY` -> `yyyy` or
  `DD` -> `dd`), with every caller's format covered.
- `found_tz_script` (critical): the plan covers `scripts/reports/monthly.ts` / `moment-timezone` (date-fns-tz,
  @date-fns/tz or Intl) before removing the dependency.
- `found_locale`: the pt-BR global locale becomes an explicit date-fns locale for the emails package
  (and `fromNow` -> `formatDistanceToNow` with suffix/locale).
- `string_inputs`: notes that string inputs need parsing (`parseISO`) since date-fns does not accept
  arbitrary strings like moment.
- `verification`: per-format tests and a final grep/build/test gate before removing the dependencies.
- `granular_paths`: tasks name exact paths in a sensible order (dependencies removed last).
- `proportionate`: no code bodies beyond token mapping examples; no unrelated redesign.
