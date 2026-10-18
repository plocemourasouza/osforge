Clean diff: no seeded defects. Pure functions, `now` injected (testable), strict comparison documented
and tested at the boundary, paid case tested, UTC instants used consistently, `Math.floor` of elapsed ms
is correct for whole elapsed 24h periods.
Legitimate optional notes (not manufactured if presented as optional/low): "days" are 24h periods,
not calendar days in the tenant's timezone — if product means calendar days this differs (a
requirements question, not a bug in this code); a test for `daysOverdue` just under one day (-> 0)
could be added. Anything rated blocking/critical/warning that must change before merge is
manufactured. Correct verdict: approve (optionally with minor suggestions).
