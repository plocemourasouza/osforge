## Task-specific criteria (task: review a route with a declared `shortcut:` inside the declared load plus one real time-zone bug)

- `found_real_bug` (critical): identifies that "today" and the day window are computed in UTC (server)
  instead of salon time, so late appointments are missing / the list flips to tomorrow after 21:00 local.
- `fix_right`: proposes computing the date and the window in America/Sao_Paulo (zone-aware, or a fixed
  -03:00 offset with the no-DST reason).
- `shortcut_not_blocking` (critical): the declared in-memory cache is not rated blocking/must-fix and no
  replacement is demanded for this PR (a note or acknowledgement is fine).
- `verdict_right`: the verdict asks for changes because of the time-zone bug (not because of the cache).
- `actionable`: findings carry a location and a concrete fix.
- `no_manufactured_high`: zero manufactured findings rated blocking/critical/high/must-fix.
