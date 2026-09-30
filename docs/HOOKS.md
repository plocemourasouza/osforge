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
   `OSFORGE_SCAN_SECRETS=off`, `OSFORGE_ROUTEGUARD=off`, `OSFORGE_OBSERVE_CAPTURE=0`,
   `OSFORGE_CANVAS_FEEDBACK=off`, `OSFORGE_CONTEXT_THRESHOLD=off`, `OSFORGE_QUOTA_THRESHOLD=off`), so
   neither the agent nor the user gets stuck behind a false positive.
6. **Fail open, except for the irreversible.** GateGuard denies a destructive Bash command
   when it cannot persist state; everything else allows and warns on stderr.
7. **One project identity, no secrets in or out** (B-018/B-019). A hook that needs the
   project slug calls `hooks/lib/project_id.py` (`OSFORGE_PROJECT` → registered git root →
   remote hash → normalised basename) — never `basename(pwd)` on its own. Anything a hook
   persists (command context, user message, resume) or re-injects goes through
   `hooks/lib/scrub.py`, and what comes back from the database is wrapped as *data*, capped,
   and scoped to the current project. `tests/test-session-continuity.sh` enforces this.

## Quota-window guard (B-027, SPEC-L01 Parte A) — not a lifecycle hook

`hooks/quota-record.py` looks like a hook (same directory, same coding rules) but is **not**
wired in `hooks/hooks-claude-code.json` or `hooks/hooks.json`, and `scripts/check-counts.py`'s
hook count does not see it (it only reads the hooks JSON) — the count stays 11. Reason: the
data it needs — the 5-hour/7-day usage percentages — only exists in the statusline's stdin
(EV-C01), and the statusline script is the user's own (`~/.claude/statusline-command.sh`),
outside this repo. OSForge does not manage it.

To feed the guard, add this line to your own statusline script (D-1 in SPEC-L01;
`>/dev/null 2>&1 &` so it never blocks or pollutes the status line, and the recorder itself is
silent and exits 0 on any error):

```bash
printf '%s' "$input" | python3 "$HOME/.claude/hooks/quota-record.py" >/dev/null 2>&1 &
```

It writes `~/.osforge/quota.json` (override: `OSFORGE_QUOTA_FILE`) — schema `osforge.quota.v1`,
see `hooks/lib/quota.py`'s module docstring. `hooks/session-save.py` feeds the same file
independently, on `Stop`: if the transcript's tail holds a rate-limit rejection line (EV-C04),
it records `rejected` there too, without needing the statusline.

The warning itself (A3) runs **inside** `context-threshold.py`'s `UserPromptSubmit` (D-2, so the
hook count doesn't move and there's one fewer process per prompt) but is a fully independent
check: own kill-switch `OSFORGE_QUOTA_THRESHOLD=off`, own bands (`OSFORGE_QUOTA_BANDS=80,95`),
own "already warned" state, keyed by the window's `resets_at` (not by session — the window
crosses sessions). It can appear in the same `additionalContext` as the context-budget warning,
one per line, or alone, or not at all.

## Adding or changing a hook

1. Wire it in `hooks/hooks-claude-code.json` (and `hooks/hooks.json` if Cursor should run
   it). The deploy copies `hooks/*.sh`, `hooks/*.py` and `hooks/lib/` to both harnesses.
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
