# E-J0 -- isolation sanity probes for judge.py

Four checks from SPEC-L02 (`docs/intake/laya/SPEC-L02-juiz-isolado.md`, section "Experimento
E-J0"): (1) the call completes with `ANTHROPIC_API_KEY` unset -- proves subscription usage, not
API billing; (2) `system/init` reports empty `tools`/`mcp_servers`; (3) a contamination probe
the judge should NOT be able to answer from the user's own `CLAUDE.md`; (4) a valid
`structured_output`, noting whether a `rate_limit_event` turned up (feeds L-01).

`driver.py` defaults to `--dry`: it builds and prints each probe's `judge.py` invocation and
calls no model. Real calls cost 1-3 short messages on the subscription quota and require
explicit opt-in, decided by the user, not by this script:

```
python3 driver.py --run --model <id>
```

If probe 2 or 3 fails, the spec's fallback is to try `--settings <empty file>` in place of
`--setting-sources ""` in `judge.py`, repeat, and if it still fails, not adopt the judge (record
why in SPEC-L02).
