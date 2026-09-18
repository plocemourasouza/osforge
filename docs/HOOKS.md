# Hooks — output-channel contract and test discipline

Every hook in `hooks/` is a small program that the harness runs at a lifecycle event. It has
exactly three ways to talk, and it must never mix them (B-006, ADR-015; the ECC audit found
seven hooks whose "warnings" went to stderr and reached nobody — E-B17).

| Intent | Claude Code | Cursor |
|---|---|---|
| **Block** the action | PreToolUse: exit 0 + `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":…}}` · Stop: `{"decision":"block","reason":…}` | `beforeShellExecution`: `{"continue":false,"permission":"deny","userMessage":…,"agentMessage":…}` |
| **Tell the model** something | `{"hookSpecificOutput":{"hookEventName":<event>,"additionalContext":…}}` (SessionStart may also print plain text) | not available; log only |
| **Log** | a file under `~/.osforge/logs/` (`OSFORGE_LOG_DIR` overrides) | same |
| Allow / nothing to say | exit 0, **empty stdout** | `{"continue":true,"permission":"allow"}` |

Rules that every hook follows, and that `tests/hooks/run-contracts.sh` enforces:

1. **Exit 0, always.** A hook that crashes takes the session down with it. Unreadable JSON,
   a payload that is a list instead of an object, a 1 MB payload: all → allow, exit 0.
2. **stdout is empty or valid JSON.** Never echo the input back; never print debug text
   (use the log file, gated by `OSFORGE_HOOK_DEBUG=1`).
3. **Never write to `/tmp` or any predictable world-readable path.** Logs go to
   `~/.osforge/logs/`; state goes to `~/.osforge/<hook>/` (GateGuard) or the SQLite db.
4. **Read the payload of the harness you are running in.** Claude Code nests the tool
   input (`tool_input.command`, `tool_input.file_path`) and always sends `hook_event_name`;
   Cursor sends flat keys (`command`, `file_path`, `workspace_roots`). A hook wired in both
   `hooks/hooks-claude-code.json` and `hooks/hooks.json` must read both (`scan-secrets.py`
   is the reference).
5. **Every block message names the hook and its kill-switch** (`OSFORGE_GATEGUARD=off`,
   `OSFORGE_SCAN_SECRETS=off`, `OSFORGE_ROUTEGUARD=off`, `OSFORGE_OBSERVE_CAPTURE=0`), so
   neither the agent nor the user gets stuck behind a false positive.
6. **Fail open, except for the irreversible.** GateGuard denies a destructive Bash command
   when it cannot persist state; everything else allows and warns on stderr.

## Adding or changing a hook

1. Wire it in `hooks/hooks-claude-code.json` (and `hooks/hooks.json` if Cursor should run
   it). The deploy copies `hooks/*.sh` and `hooks/*.py` to both harnesses.
2. Add at least three lines to `tests/hooks/cases.tsv`: the positive verdict, the negative
   verdict, and a malformed payload. Add fixtures under `tests/hooks/fixtures/`; use
   `__HOME__` and `__FIXTURES__` tokens for paths.
3. Run `./tests/hooks/run-contracts.sh`. It runs the **real command string** from the hooks
   JSON, with `HOME`, `TMPDIR` and all state directories inside a sandbox, and fails on any
   of the rules above. The deploy preflight and CI run the same script.
4. Describe the hook in `USAGE.md` → "What each hook does" and bump the count that
   `scripts/check-counts.py` checks.

## Reading `tests/hooks/cases.tsv`

`id · harness · event · hook · fixture · expect`. `hook` is a substring of the command in the
hooks JSON (`*` = every hook of that event). `expect` is `deny | allow | block | context |
silent | any`; `any` checks only the invariants (exit 0, JSON-or-empty, no `/tmp` writes).
Run one group with `./tests/hooks/run-contracts.sh --only CC-4`.
