---
name: stuck-recovery
description: >
  Detects agent stuck patterns (loops, repetitions, scope drift, a tool
  failing 3x+) and runs surgical recovery: saves state to osforge-db, identifies
  root cause, proposes a reset with minimal context preserved. Use when: the user
  says "stuck", "loop", "it's not working", "try again", "this
  isn't making progress", "forget what you were doing", or when the agent
  detects internal signs of saturation (same tool failing 3x, no
  progress over N turns).
version: 1.0.0
inspired_by: Leonxlnx/agentic-ai-prompt-research (Prompt 26 — Stuck Skill, reframed)
metadata:
  source: "agentic-ai-prompt-research"
  category: "meta"
allowed-tools: Read, Bash, Glob, Grep
---

# Stuck Recovery — Agent Loop Detection + State Save + Reset

> The original Claude Code Stuck Skill is process diagnosis (CPU, zombies, FDs).
> This skill is **agent** diagnosis — it detects semantic loops and proposes recovery
> without losing the work done.

## Prerequisites

This skill depends on two external pieces (via Bash, listed in `allowed-tools`):

- **`osforge-db`** (CLI) — state/blocker/resume persistence in Phases 2 and 4. Verify with `command -v osforge-db`. Without it, SAVE degrades to a WIP commit + a local notes file.
- **`context-compact`** (OSForge skill) — used in Option B (compact reset). Without it, skip straight to Option A or C.

## Signs of being stuck (detection)

### External signs (the user speaks)
- "It's not working"
- "You're stuck"
- "Try again a different way"
- "You're in a loop"
- "Forget it, let's go back"
- "This isn't making progress"

### Internal signs (self-detection)
| Sign | Threshold |
|---|---|
| Same tool failing consecutively | ≥ 3 times |
| Same file being read with no action | ≥ 5 times in 10 turns |
| No measurable progress | 10+ turns without completing an atomic task |
| Past ~150k tokens without closing a phase | deep in the dumb zone |
| "verify → fail → retry" loop with no change of approach | ≥ 2 cycles |
| Drift from the original scope | topic diverges without user approval |
| Tool errors growing (not shrinking) | error rate > 30% in the last 10 calls |

## Recovery protocol (4 phases)

### Phase 1: STOP — Stop before it gets worse

Stop before spending more context. Tell the user plainly which sign fired, how much context is
in use, when the last atomic task was completed and what pattern you are repeating — then
propose the recovery instead of trying once more "just to see" or moving on to the next sub-task.

### Phase 2: SAVE — Preserve the work

Save the COMPLETE state to `osforge-db` before the reset:

```bash
osforge-db set-phase <project-slug> "<current-phase>" in-progress
osforge-db set-resume <project-slug> "<precise stopping point; modified files>"

osforge-db add-blocker <project-slug> "<description of what is blocking>"

# Persist the current summary via context-compact if applicable
```

List the modified files in the resume note. Propose a WIP commit if the work should be
checkpointed, but make it only with the user's approval (global rule: never auto-commit).

### Phase 3: DIAGNOSE — Identify the root cause

Replay what the last 5–10 turns did (tools called, errors returned, intent), find the turn
where the work derailed, and categorize the cause:

| Cause | Symptom | Fix |
|---|---|---|
| **Context saturation** | Loops + forgetting | `context-compact` → resume |
| **Wrong approach** | Same error persists even after retry | Change the approach completely, don't try variations |
| **Missing context** | Wrong decisions due to lack of info | Spawn `explorer-agent` to map |
| **Tool misuse** | Right tool, wrong parameters | Re-read tool description |
| **Spec drift** | Agent left the original scope | Return to the spec, discard off-scope work |
| **External blocker** | Server down, broken API, missing dep | Notify the user, stop until resolved |

Then state explicitly what will be DIFFERENT on the next attempt:
- Approach: <X instead of Y>
- Context: <I'll load Z first>
- Verification: <I'll check W before declaring it done>

### Phase 4: RECOVER — Surgical reset with minimal context

3 options, choose based on the diagnosis:

#### Option A: Soft reset (same session)
If context is not saturated and the cause is diagnosable:
- Announce the reset to the user
- Clear bad assumptions from the mental context
- Reformulate the approach
- Continue

#### Option B: Compact reset (same session, compacted context)
If context is ~120–150k tokens but you want to continue:
1. Invoke the `context-compact` skill
2. Compact everything up to the stuck point
3. Restart with summary + new approach

#### Option C: Hard reset (new session)
If context is past ~150k tokens or the approach is fundamentally wrong:
1. `osforge-db set-resume <slug> "<specific next step>"`
2. Tell the user: "I'll ask you to open a new session"
3. The new session starts with `osforge-db resume <slug>` → 50 tokens

## Decision tree

```
Detected stuck
    │
    ├─ Context < ~120k tokens?
    │   ├─ YES → Option A (soft reset)
    │   └─ NO  ↓
    │
    ├─ Context ~120–150k tokens?
    │   ├─ YES → Option B (compact reset)
    │   └─ NO  ↓
    │
    └─ Context > ~150k tokens OR approach fundamentally wrong?
        └─ Option C (hard reset via osforge-db)
```

## Communication to the user

Be transparent about the loop, the diagnosis and the proposed recovery, then ask for approval. For example:
```
🛑 I detected we've been in a loop for the last 6 messages (trying to run `tsc`, which fails because of an import that doesn't exist).

Diagnosis: missing context — I didn't check `package.json` before assuming the dep was installed.

Proposed recovery:
1. Save the current state (in progress: fix for the TS error in validate.ts:42)
2. Invoke `explorer-agent` to map the real deps
3. Continue with the corrected approach (install dep OR adjust import)

Can you approve? If not, do you prefer: (a) I try another approach now, or (b) we save and you open a fresh new session?
```

## Anti-patterns

- ❌ Keep trying after 3 consecutive failures
- ❌ Silent reset (the user gets lost)
- ❌ Reset without saving state (loses work)
- ❌ Misdiagnose and re-apply the same solution
- ❌ Hide that you're stuck to "look competent"
- ❌ Try more tools as a solution for a lack of approach

## Post-recovery verification

After the reset, the next turn should produce:
- [ ] An outcome different from the original loop
- [ ] The approach changed (not just the parameters)
- [ ] The pre-recovery state is accessible via `osforge-db resume`
- [ ] The user knows what changed and why

## Integration with OSForge

`stuck-recovery` complements existing skills:
- `systematic-debugging` — for a reproducible bug found during Diagnose
- `context-compact` — used in Option B (compact reset)
- `osforge-db` — state persistence in all options
- `verification-before-completion` — gate before declaring recovery successful

---

## Related Skills

- `systematic-debugging` — used internally in the Diagnose phase
- `context-compact` — recovery option B
- `osforge-db` — cross-session persistence
- `verification-before-completion` — post-recovery gate
- `predictive-failure` — anticipates getting stuck before it happens

**Exhaustiveness bar** — a recovery is done when the 4 phases of the protocol ran in order, the Decision tree verdict is recorded, the user got the Communication message, and Post-recovery verification passed. Skipping phases is how the same stuck state returns in twenty minutes.
