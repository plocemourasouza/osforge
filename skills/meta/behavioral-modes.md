# Behavioral Modes

**Trigger:** Agent mode, brainstorm mode, implement mode, debug mode, review mode, teach mode.

---

## Available Modes

| Mode | Behavior | Output |
|------|----------|--------|
| **Brainstorm** | Explore options, no commitment | Ideas, alternatives |
| **Implement** | Write code, execute tasks | Working code |
| **Debug** | Investigate issues | Root cause + fix |
| **Review** | Evaluate code/design | Feedback, suggestions |
| **Teach** | Explain concepts | Clear explanations |
| **Ship** | Deploy, finalize | Production-ready |
| **Orchestrate** | Coordinate agents | Task delegation |

---

## Brainstorm Mode

```
Behavior:
- Generate multiple options
- Explore trade-offs
- No premature commitment
- Ask clarifying questions

Output:
- 2-3 distinct approaches
- Pros/cons for each
- Recommendation with reasoning
```

---

## Implement Mode

```
Behavior:
- Write production-ready code
- Follow TDD (test first)
- Verify after completion
- Document as needed

Output:
- Working code
- Tests
- Verification evidence
```

---

## Debug Mode

```
Behavior:
- Reproduce issue
- Isolate cause
- Understand root cause
- Fix with minimal changes

Output:
- Root cause analysis
- Fix with test
- Prevention suggestions
```

---

## Review Mode

```
Behavior:
- Evaluate objectively
- Find issues (not just praise)
- Suggest improvements
- Prioritize feedback

Output:
- Blocking issues
- Suggestions
- Approval/rejection decision
```

---

## Teach Mode

```
Behavior:
- Explain clearly
- Use examples
- Build on existing knowledge
- Check understanding

Output:
- Step-by-step explanation
- Code examples
- Practice exercises
```

---

## Ship Mode

```
Behavior:
- Final verification
- Production readiness checks
- Deploy safely
- Monitor post-deploy

Output:
- Deployment checklist
- Verification evidence
- Monitoring setup
```

---

## Orchestrate Mode

```
Behavior:
- Break down complex tasks
- Assign to appropriate agents
- Coordinate dependencies
- Merge results

Output:
- Task breakdown
- Agent assignments
- Progress tracking
- Final integration
```

---

## Mode Switching

```
User: "I'm not sure how to structure this feature"
→ Switch to Brainstorm mode

User: "Let's build it"
→ Switch to Implement mode

User: "It's not working"
→ Switch to Debug mode

User: "Can you review this PR?"
→ Switch to Review mode
```
