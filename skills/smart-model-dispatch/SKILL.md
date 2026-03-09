---
name: smart-model-dispatch
description: "Automatically routes tasks to optimal Claude models (opus/sonnet/haiku) based on complexity, cost, and task type. TRIGGER when: implementing features with multiple subtasks, dispatching parallel agents, planning sprints with mixed complexity, or when the user mentions cost optimization, model routing, or smart dispatch. Also trigger when spawning subagents via Agent tool — each subagent should specify its optimal model."
metadata:
  author: osforge
  version: '1.0'
  inspired_by: andersonlimadev/smart-dispatch
---

# Smart Model Dispatch

## Principle
Use the most powerful model only where reasoning depth matters. Route mechanical tasks to cheaper/faster models. The Agent tool's `model` parameter enables per-subagent model selection.

## Model Tiers

### 🔴 Opus (`claude-opus-4-6`) — $5/$25 per 1M tokens
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

### 🟡 Sonnet (`claude-sonnet-4-6`) — $3/$15 per 1M tokens
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

### 🟢 Haiku (`claude-haiku-4-5`) — $1/$5 per 1M tokens
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
"Implementa a feature de Billing para Red Caveat Jus"

1. [opus]   planner → decompõe em stories, define arquitetura
2. [opus]   validator → critica o plano, identifica gaps
3. [sonnet] backend-engineer → implementa Prisma schema + Server Actions
4. [sonnet] stripe-integration → webhook handler + checkout
5. [sonnet] frontend-engineer → pricing page + billing portal UI
6. [haiku]  → gera i18n keys, test stubs, seed data
7. [sonnet] tdd-workflow → escreve testes de integração
8. [sonnet] code-reviewer → review final
```

### Bug Fix
```
"Corrige o bug de refresh token no auth"

1. [sonnet] debugger → reproduz, analisa, encontra root cause
2. [sonnet] backend-engineer → implementa fix
3. [haiku]  → atualiza testes, docs
4. [sonnet] code-reviewer → review do fix
```

### Security Audit
```
"Faz audit de segurança no módulo de pagamentos"

1. [opus]   security-auditor → threat model + attack surface
2. [opus]   insecure-defaults → scan de fail-open patterns
3. [sonnet] differential-review → review dos PRs recentes
4. [haiku]  → gera relatório formatado
```

### Parallel Dispatch (with dispatching-parallel-agents)
```
"Implementa 3 endpoints independentes"

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

## Cost Estimation Reference

| Task | Model | Est. Tokens | Est. Cost |
|---|---|---|---|
| Feature planning (opus) | opus | ~10K in / ~5K out | ~$0.18 |
| Implementation (sonnet) | sonnet | ~15K in / ~8K out | ~$0.17 |
| Boilerplate gen (haiku) | haiku | ~5K in / ~3K out | ~$0.02 |
| Full feature (mixed) | mixed | ~50K total | ~$0.50 |
| Same feature (all opus) | opus | ~50K total | ~$1.50 |

**Savings:** ~65% cost reduction using mixed routing vs all-opus for typical feature work.

## Rules

1. **Default to Sonnet** — When uncertain, Sonnet is the safe choice. It handles 70% of tasks well.
2. **Never downgrade security** — Security-auditor and threat modeling always use Opus.
3. **Opus for planning, Haiku for execution** — If the task is "decide WHAT to do", use Opus. If it's "do this specific thing", consider Haiku.
4. **Batch Haiku tasks** — Group multiple Haiku tasks (i18n + tests + docs) into a single subagent call.
5. **Escalate on failure** — If Haiku produces low-quality output, retry with Sonnet. If Sonnet fails, escalate to Opus.
6. **Context size matters** — Opus has 200K (1M beta). For tasks requiring >100K context, prefer Opus for better long-context performance.
