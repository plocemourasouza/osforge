---
name: smart-model-dispatch
description: "Claude model router. Use when: spawning subagents via Agent tool, implementing a feature with multiple mixed-complexity subtasks, optimizing API cost, planning a sprint with parallel tasks. Keywords: model routing, opus sonnet haiku, cost optimization, smart dispatch, parallel agents, which model, model selection. Trigger on any mention of 'which model', 'use opus', 'use haiku', 'cost', 'dispatch agents'."
model: sonnet
allowed-tools: Read, Bash, Glob
metadata:
  author: osforge
  version: '1.1'
  inspired_by: andersonlimadev/smart-dispatch
---

# Smart Model Dispatch

## Principle
Use the most powerful model only where reasoning depth matters. Route mechanical tasks to cheaper/faster models. The Agent tool's `model` parameter enables per-subagent model selection.

**Requirement:** this skill depends on the **Agent tool** (subagent spawning) to work — it is what accepts the `model` parameter and lets you route each subtask to the right tier. If the Agent tool is not available in the environment, there is no way to dispatch to different models; in that case, just recommend the appropriate tier for the user to run manually.

## Model Tiers

### 🔴 Opus (`claude-opus-5-5`) — $4/$20 per 1M tokens
For the hardest planning and synthesis, `claude-fable-5-1` ($10/$50) sits above it.
**When:** Task requires deep reasoning, architectural decisions, or multi-step analysis where errors compound.

| Agent/Skill | Use Opus When |
|---|---|
| `planner` | Always — architecture, decomposition, story creation |
| `validator` (critique mode) | Always — spec critique requires deep analysis |
| `security-auditor` | Threat modeling, RLS policy design, attack surface analysis |
| `technical-design-doc-creator` | Always — ADRs, system design docs |
| `prisma-expert` | Migration strategies for >20 tables, schema redesign |
| `nextjs-supabase-auth` | Multi-org RBAC design, auth flow architecture |
| `stripe-integration` | Billing architecture, webhook flow design |

### 🟡 Sonnet (`claude-sonnet-5-5`) — $2/$10 per 1M tokens
**When:** Task requires solid implementation skills but the approach is already defined.

| Agent/Skill | Use Sonnet When |
|---|---|
| `debugger` | 10-step debugging, root cause analysis |
| `code-reviewer` | PR review, code quality analysis |
| `frontend-engineer` | Component implementation with business logic |
| `backend-engineer` | API routes, Server Actions, data layer |
| `differential-review` | Security-focused PR review |
| `e2e-testing-patterns` | Writing Playwright test flows |
| `tdd-workflow` | RED-GREEN-REFACTOR cycle execution |
| `react-performance` | Performance optimization implementation |
| `mcp-builder` | Building MCP server tools and resources |
| `claude-ci-actions` | Setting up GitHub Actions workflows |

### 🟢 Haiku (`claude-haiku-5-5`) — $0.10/$0.50 per 1M tokens (prompts up to 100K)
**When:** Task is mechanical, repetitive, or follows a clear template. No complex reasoning needed.

| Task Type | Examples |
|---|---|
| Boilerplate generation | Prisma models from spec, API route scaffolding, component shells |
| Style files | Tailwind configs, CSS modules, theme tokens |
| i18n translation files | messages/pt-BR.json, messages/en.json |
| Test stubs | Unit test skeletons, mock factories, fixture data |
| Documentation | JSDoc comments, README updates, changelog entries |
| Data transformations | CSV→JSON, format conversions, seed data |
| Commit messages | Conventional commit format from diff |
| Simple CRUD | Basic form components, list views, detail pages without complex logic |
| `docs-writer` | Generating docs from existing code |
| `doc-sanitization` | PII removal, content filtering |
| `seo` | Meta tags, structured data, sitemap entries |
| `accessibility` | aria-label additions, WCAG fixes |
| `git-workflow` | Branch creation, merge prep, tag management |

## Dispatch Patterns

### Feature Implementation (Full Stack)
```
"Implement the Billing feature for Red Caveat Jus"

1. [opus]   planner → decompose into stories, define architecture
2. [opus]   validator → critique the plan, identify gaps
3. [sonnet] backend-engineer → implement Prisma schema + Server Actions
4. [sonnet] stripe-integration → webhook handler + checkout
5. [sonnet] frontend-engineer → pricing page + billing portal UI
6. [haiku]  → generate i18n keys, test stubs, seed data
7. [sonnet] tdd-workflow → write integration tests
8. [sonnet] code-reviewer → final review
```

### Bug Fix
```
"Fix the refresh token bug in auth"

1. [sonnet] debugger → reproduce, analyze, find root cause
2. [sonnet] backend-engineer → implement fix
3. [haiku]  → update tests, docs
4. [sonnet] code-reviewer → review the fix
```

### Security Audit
```
"Run a security audit on the payments module"

1. [opus]   security-auditor → threat model + attack surface
2. [opus]   insecure-defaults → scan for fail-open patterns
3. [sonnet] differential-review → review recent PRs
4. [haiku]  → generate formatted report
```

### Parallel Dispatch (with dispatching-parallel-agents)
```
"Implement 3 independent endpoints"

Parallel [sonnet]:
  - Task A: /api/projects endpoint
  - Task B: /api/members endpoint  
  - Task C: /api/invitations endpoint

Sequential [haiku] after all complete:
  - Generate test stubs for all 3
  - Add i18n keys
  - Update API docs
```

## Agent Tool Model Parameter

When spawning subagents, specify the model:

```markdown
Use the Agent tool to spawn a subagent:
- Task: "Generate i18n translation files for the billing module"
- Model: haiku
- Tools: Read, Write, Glob
```

The Agent tool accepts a `model` parameter that routes to the specified tier.

## Cost Reference

Per-token prices live in `claude-code/pricing.json` (the source `osforge-db calls` uses). Cost scales with tier, but judge cost per task completed correctly, not per request: a cheaper tier that needs retries is not cheaper. No savings figure is claimed here until it is measured.

## Rules

1. **Default to Sonnet** — When uncertain, Sonnet is the safe choice for implementation work.
2. **Never downgrade security** — Security-auditor and threat modeling always use Opus.
3. **Opus for planning, Haiku for execution** — If the task is "decide WHAT to do", use Opus. If it's "do this specific thing", consider Haiku.
4. **Batch Haiku tasks** — Group multiple Haiku tasks (i18n + tests + docs) into a single subagent call.
5. **Escalate on failure** — If Haiku produces low-quality output, retry with Sonnet. If Sonnet fails, escalate to Opus.
6. **Context size matters** — Keep each subagent's brief small. Route by reasoning depth, not by window size: every current tier has a 1M window.

## Local Models Track (via llmfit-advisor)

OSForge supports a **local track** via Ollama as an alternative to the API track, especially for Haiku-eligible tasks, sensitive data, or clients without an API budget.

To identify which models run on the available hardware, use the `llmfit-advisor` skill:
```
Read skills/llmfit-advisor/SKILL.md
```

### When to use local vs API

| Criterion | Local (Ollama) | API (Claude) |
|---|---|---|
| Sensitive data (LGPD, accounting, legal) | ✅ prefer | ⚠️ avoid |
| High-volume Haiku-eligible tasks | ✅ economical | 💰 cost accumulates |
| Deep reasoning / architecture | ❌ no equivalent | ✅ Opus |
| Offline environment / client without API | ✅ only path | ❌ unavailable |
| Large context | ⚠️ limited by local model | ✅ 1M window |
| Latency-critical in production | ⚠️ depends on HW | ✅ consistent |

### Local model equivalents per tier

| Claude API | Local equivalent (use-case: coding) | Local equivalent (use-case: chat) |
|---|---|---|
| Haiku (mechanical) | `qwen2.5-coder:7b` / `phi4-mini` | `gemma2:9b` / `mistral:7b` |
| Sonnet (implementation) | `qwen2.5-coder:14b` / `llama3.1:8b` | `llama3.3:70b` (if HW supports it) |
| Opus (reasoning) | `deepseek-r1:32b` (partial) | No full equivalent |

> To find out which model fits the actual hardware: `llmfit recommend --json --use-case coding --limit 3`

---

## Gotchas

- **Haiku with ambiguity**: Haiku is for fully specified tasks. If the requirements are unclear, clarify first or use Sonnet.
- **Do not split up Haiku tasks**: call Haiku once with all mechanical tasks batched instead of multiple individual calls. Multiple isolated calls accumulate context-loading overhead.
- **Opus for review is rarely needed**: code review and debugging do well on Sonnet. Reserve Opus for architectural planning, threat modeling, and high-ambiguity decisions.
- **Do not escalate too early**: if Sonnet produced an unsatisfactory result, check whether the problem is prompt clarity before escalating to Opus. Vague prompts produce poor results at any tier.

**Exhaustiveness bar** — a dispatch decision is done when every subtask carries an explicit tier chosen from the Model Tiers table with the Rules applied — no task inherits the parent model by omission, which is how everything silently runs on the most expensive tier.
