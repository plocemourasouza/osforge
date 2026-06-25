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

- **`osforge-db`** (CLI) — state/blocker/resume persistence in Phases 2 and 4. Verify with `osforge-db --version`. Without it, SAVE degrades to a WIP commit + a local notes file.
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
| Context > 85% without closing a phase | imminent saturation |
| "verify → fail → retry" loop with no change of approach | ≥ 2 cycles |
| Drift from the original scope | topic diverges without user approval |
| Tool errors growing (not shrinking) | error rate > 30% in the last 10 calls |

## Recovery protocol (4 phases)

### Phase 1: STOP — Stop before it gets worse

When stuck is detected:

```
🛑 STUCK DETECTED

Sign: <which sign fired>
Context: <X% / 200k>
Last completed atomic task: <how many turns ago>
Observed pattern: <1-line description>

I'll pause and propose recovery before spending more context.
```

**DO NOT**:
- Try one more time "just to see"
- Jump to the next sub-task
- Pretend you're making progress

### Phase 2: SAVE — Preserve the work

Save the COMPLETE state to `osforge-db` before the reset:

```bash
osforge-db set-phase <project-slug> "<current-phase>" in_progress \
  --resume "<precise description of the stopping point>" \
  --artifacts "<modified files, paths>"

osforge-db add-blocker <project-slug> "<description of what is blocking>"

# Persist the current summary via context-compact if applicable
```

Ensure ALL modified files are committed (even in a WIP commit):
```bash
git add -A && git commit -m "wip: stuck recovery checkpoint at <task>"
```

### Phase 3: DIAGNOSE — Identify the root cause

Apply the systematic-debugging skill (4 phases) **within the session itself**:

#### Phase 1: Reproduce
List exactly what was happening in the last 5-10 turns:
- Which tools were called
- Which errors they returned
- What the agent tried to do
- What the agent SHOULD have done

#### Phase 2: Isolate
Identify the EXACT turn where the agent started to derail:
- Was it a wrong decision at which point?
- Was it a false assumption about what?
- Was it missing context about what?

#### Phase 3: Understand
Categorize the root cause:

| Cause | Symptom | Fix |
|---|---|---|
| **Context saturation** | Loops + forgetting | `context-compact` → resume |
| **Wrong approach** | Same error persists even after retry | Change the approach completely, don't try variations |
| **Missing context** | Wrong decisions due to lack of info | Spawn `explorer-agent` to map |
| **Tool misuse** | Right tool, wrong parameters | Re-read tool description |
| **Spec drift** | Agent left the original scope | Return to the spec, discard off-scope work |
| **External blocker** | Server down, broken API, missing dep | Notify the user, stop until resolved |

#### Phase 4: Fix
Explicitly define what will be DIFFERENT on the next attempt:
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
If context > 70% but you want to continue:
1. Invoke the `context-compact` skill
2. Compact everything up to the stuck point
3. Restart with summary + new approach

#### Option C: Hard reset (new session)
If context > 90% or the approach is fundamentally wrong:
1. `osforge-db set-resume <slug> "<specific next step>"`
2. Tell the user: "I'll ask you to open a new session"
3. The new session starts with `osforge-db resume <slug>` → 50 tokens

## Decision tree

```
Detected stuck
    │
    ├─ Context < 70%?
    │   ├─ YES → Option A (soft reset)
    │   └─ NO  ↓
    │
    ├─ Context 70-90%?
    │   ├─ YES → Option B (compact reset)
    │   └─ NO  ↓
    │
    └─ Context > 90% OR approach fundamentally wrong?
        └─ Option C (hard reset via osforge-db)
```

## Communication to the user

**ALWAYS** be transparent:
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
- `systematic-debugging` (4 phases) — used inside Phase 3 (Diagnose)
- `context-compact` — used in Option B (compact reset)
- `osforge-db` — state persistence in all options
- `verification-before-completion` — gate before declaring recovery successful

## Expected frequency

In a healthy session: **0-1 invocations per 2-3 hours of intense work**.

More than that indicates:
- A poorly defined spec (needs `spec-clarify`)
- A poorly mapped codebase (needs `explorer-agent`)
- A fundamentally wrong approach (needs `brainstorming`)

---

## Related Skills

- `systematic-debugging` — used internally in the Diagnose phase
- `context-compact` — recovery option B
- `osforge-db` — cross-session persistence
- `verification-before-completion` — post-recovery gate
- `predictive-failure` — anticipates getting stuck before it happens
