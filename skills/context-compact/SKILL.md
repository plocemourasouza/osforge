---
name: context-compact
description: >
  Structured conversation compaction when reaching ~70% of the context window.
  Use when: user says "compress context", "compact", "summary", "near the
  limit", "context full", "save state", "/compact", "/clear", or when the
  token counter passes 140k. Produces a 9-section summary with an analysis
  scratchpad. Replaces destructive /clear with intelligent preservation.
version: 1.0.0
inspired_by: Leonxlnx/agentic-ai-prompt-research (Prompt 21 — Compact Service)
metadata:
  source: "agentic-ai-prompt-research"
  category: "meta"
allowed-tools: Read
---

# Context Compact — Conversation Summarization

> When context > 70%, do NOT use `/clear` (destructive). Use this structured
> 9-section protocol that preserves the essentials in ~5k tokens.

## Quick Start

**Example 1 — explicit request:**
> User: *"compact context, we're near the limit"*
> The skill generates a structured 9-section summary (~5k tokens) that replaces the entire conversation, preserving requests, decisions, files touched, and the work in progress — without losing the thread of execution.

**Example 2 — proactive:**
> The token counter passes 140k in the middle of a refactor.
> The skill suggests a **Partial Compact (Mode 3)**: it summarizes the older messages and keeps the recent ones intact, freeing up space without touching the "now".

**Mini-flow (3 steps):**
1. **Choose the mode** — Full (everything becomes a summary), Partial Recent (preserves the beginning) or Partial Up-To (preserves the end). See "3 modes of operation".
2. **Run the protocol** — emit the NO_TOOLS_PREAMBLE, do the `<analysis>` scratchpad, then fill in the 9-section template (Steps 1–3 in "Execution protocol").
3. **Verify and persist** — check the "Verification" checklist and save via `osforge-db set-resume` for cross-session recovery.

## When to activate

| Trigger | Action |
|---|---|
| Context > 70% (140k of 200k tokens) | Suggest compact to the user BEFORE it saturates |
| Context > 85% (170k) | Compact mandatory — inform the user |
| User says "compress", "compact", "near the limit" | Immediate compact |
| Big topic change mid-session | Offer "compact old context, keep recent" |

## 3 modes of operation

### Mode 1: Full Compact
The entire conversation becomes a summary. Use when you are about to start a completely new phase.

### Mode 2: Partial Compact (Recent)
Recent messages become a summary, but old context is kept intact. Use when the beginning of the session has critical information that must NOT be summarized.

### Mode 3: Partial Compact (Up-To / Older)
Old messages become a summary, recent messages stay intact. Use when you are in the middle of an execution and need to make space — it preserves the "now".

## Execution protocol

### Step 1: NO_TOOLS_PREAMBLE (CRITICAL)

ALWAYS start with this preamble to prevent the model from calling tools during the summary:

```
CRITICAL: Respond with TEXT ONLY. Do NOT call any tools.

- Do NOT use Read, Bash, Grep, Glob, Edit, Write, or ANY other tool.
- You already have all the context you need in the conversation above.
- Tool calls will be REJECTED and will waste your only turn — you will fail the task.
- Your entire response must be plain text: an <analysis> block followed by a <summary> block.
```

### Step 2: Analysis Scratchpad

Before the final summary, do a chronological analysis in `<analysis>` tags:

```xml
<analysis>
1. Chronologically, analyze each message and section:
   - Explicit user requests and intents
   - Your approach to addressing each request
   - Key decisions, technical concepts, code patterns
   - Specific details: file names, complete code snippets,
     function signatures, file edits
   - Errors encountered and how they were fixed
   - Specific user feedback (extra attention)
2. Double-check for technical accuracy and completeness
</analysis>
```

The `<analysis>` is a scratchpad — it will be discarded before the summary reaches the next context.

### Step 3: 9-section summary (template)

```markdown
<summary>

## 1. Primary Request and Intent
All explicit user requests, with intent captured in full.
Include ALL of them, not just the last. E.g.:
- "Integrate taste-skill into OSForge" (turn 5)
- "Audit OBSIDIAN for performance and a11y" (turn 23)
- "Apply fixes via prompt" (turn 31)

## 2. Key Technical Concepts
Technologies, frameworks, patterns discussed:
- OSForge framework (122 skills, 26 agents, 12 rules)
- Anti-AI-slop directives (Inter ban, pure #000 ban, etc)
- Taste design dials (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY)
- Lighthouse Core Web Vitals (LCP, FCP, CLS)
- Chrome MCP for browser automation

## 3. Files and Code Sections
Files examined/modified/created, WITH complete code snippets:

**Modified:**
- `claude-code/SKILLS.md` (added 8 design skills to Design & UX table)
- `rules/anti-ai-slop.mdc` (expanded from 9 to 40 rules)

**Created:**
- `skills/taste-design-dials/SKILL.md` (261 lines)
- `skills/aesthetic-modes/SKILL.md` (254 lines)
[etc — list ALL]

```typescript
// Relevant snippets that will be needed to continue
const decision = classifier.classify({...})
```

## 4. Errors and Fixes
Errors encountered and resolution:
- `index.lock` in .git → resolved with `rm -f .git/index.lock`
- Server localhost:4567 went down → user restarted it on :8000
- web_fetch URLs outside provenance → solved by cloning via bash

## 5. Problem Solving
Problems solved and troubleshooting in progress:
- ✅ taste-skill integration (5 skills + routing rules)
- ✅ Deploy to ~/.claude/ and ~/.cursor/
- ✅ Audit OBSIDIAN (FCP 6.5s bottleneck identified)
- 🔄 In progress: agentic-ai-prompt-research patterns integration

## 6. All User Messages
EVERY non-tool-result user message (critical for intent drift tracking):
- "Remember our OSForge project?"
- "we have it on github..."
- "I want to add this knowledge to the project..."
- "do it"
- "the /mcp command didn't work"
- "I want you to run the commands..."
- "Here's the link to the generated result..."
- "You didn't convince me why Auto Mode Critique (17) doesn't..."
- "Perfect, let's move forward"
[continue listing ALL — even short ones]

## 7. Pending Tasks
Pending work:
- [ ] Implement tool-safety-classifier skill
- [ ] Implement config-critique skill
- [ ] Implement context-compact skill (in progress NOW)
- [ ] Implement stuck-recovery skill
- [ ] Create memory-hierarchy.mdc rule
- [ ] Enrich orchestrator/AGENT.md with Coordinator patterns
- [ ] Update SKILLS.md router + README

## 8. Current Work
PRECISE description of the work in progress BEFORE the compaction:
I am creating 4 new SKILL.md files in OSForge based on the prompts from
agentic-ai-prompt-research (Leon Lin). I just finished
`tool-safety-classifier` (Prompt 12), now I am writing
`context-compact` (this file — Prompt 21). Next:
config-critique (P17), stuck-recovery (P26). Then enrichments
in the orchestrator and CLAUDE.md, then commit + push.

## 9. Optional Next Step
IMMEDIATE next step if aligned with recent requests:
Finish writing context-compact/SKILL.md (this file),
save it with the Write tool, then move on to skills/config-critique/SKILL.md.

</summary>
```

## Mode 2 (Partial Recent) — adaptation

Replace the initial instruction with:
```
Your task is to create a detailed summary of the RECENT portion of the conversation —
the messages that follow earlier retained context. The earlier messages are being kept
intact and do NOT need to be summarized. Focus your summary on what was discussed,
learned, and accomplished in the recent messages only.
```

## Mode 3 (Partial Up-To / Older) — adaptation

Replace the initial instruction with:
```
Your task is to create a detailed summary of this conversation. This summary will be
placed at the start of a continuing session; newer messages that build on this context
will follow after your summary (you do not see them here). Summarize thoroughly so
that someone reading only your summary and then the newer messages can fully understand
what happened and continue the work.
```

And in the sections:
- Section 8 becomes "Work Completed" (not "Current Work")
- Section 9 becomes "Context for Continuing Work"

## Integration with osforge-db

OSForge has local SQLite (`~/.osforge/osforge.db`). Use it to PERSIST the summary:

```bash
# After generating the summary, save it persistently:
osforge-db set-resume <project-slug> "$(cat summary.md)"

# A future session recovers it in 50 tokens via:
osforge-db resume <project-slug>
```

This means that **compaction does not destroy** the context — it remains available for future sessions via osforge-db, even after it has left the current context window.

## Custom instructions support

If the project has `compact-instructions.md` in `.osforge/`, include it in the prompt:

```
There may be additional summarization instructions provided in the included context.
If so, remember to follow these instructions when creating the above summary.
```

Useful for projects with specific terminology that must be preserved literally.

## Anti-patterns

- ❌ Skipping the `<analysis>` block — you will forget something
- ❌ Summarizing only the last N messages "because it's easier" — it breaks intent tracking
- ❌ Omitting section 6 (All User Messages) — it is the defense against intent drift
- ❌ Using a Tool during summarization — it will fail with maxTurns: 1
- ❌ `<analysis>` in the final output (it must be stripped — only the user needs to see `<summary>`)

## Verification

- [ ] All 9 sections filled in (even if some with "N/A")
- [ ] Section 3 includes COMPLETE code snippets (not placeholders)
- [ ] Section 6 lists EVERY user message
- [ ] No tool calls in the output
- [ ] Total: 3-7k tokens (not < 1k, not > 10k)
- [ ] Resume restorable: another session can continue by reading only the summary

---

## Related Skills

- `context-distillator` — sibling skill for radical distillation (~500 tokens)
- `osforge-db` — cross-session persistence (recovery via `osforge-db resume`)
- `project-context` — initial project context generation
- `editorial-review` — post-summary cleanup if needed
