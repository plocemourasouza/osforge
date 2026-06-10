# Skills & Knowledge Base
Reference skills for Claude Code. Core skills always active; specialized skills loaded on-demand.

---

## Skill 1: TDD Workflow (RED-GREEN-REFACTOR)
**Trigger:** Any feature, bugfix, or behavior change.

**Iron Law:** `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`
Wrote code before the test? **Delete it. Start over.**

### Cycle
1. **RED** — Write ONE test for smallest behavior. Run it. Confirm it FAILS.
2. **GREEN** — Write MINIMUM code to pass. Nothing more.
3. **REFACTOR** — Clean up while green. Extract, rename, deduplicate.
4. **COMMIT** — `test: add test for X` → `feat: implement X`

### Right Size
- Too big: "User authentication system"
- Right: "Login returns JWT on valid credentials"

### Exceptions (ask first)
Throwaway prototypes, generated code (Prisma Client, shadcn), config files, pure UI styling.

### Test Protection
When tests FAIL, fix PRODUCTION CODE — NEVER modify tests to make them pass.
- NEVER alter assertions to match wrong output
- NEVER delete or `.skip` failing tests
- NEVER change expected values to match actual
- Only exception: genuine test bug or explicitly requested requirement change

---

## Skill 2: Verification Before Completion
**Trigger:** Before any completion claim, commit, or PR.

**Iron Law:** `NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE`

### Gate Function
1. IDENTIFY → What command proves this claim?
2. RUN → Execute full command (fresh, not cached)
3. READ → Full output, check exit code
4. VERIFY → Does output confirm claim?
5. ONLY THEN → Make the claim WITH evidence

### Evidence Table
| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| "Tests pass" | Test output: 0 failures | Previous run, "should pass" |
| "Build succeeds" | Build command: exit 0 | "looks good" |
| "Bug fixed" | Test original symptom: passes | Code changed, assumed fixed |
| "No regressions" | Full suite: all pass | Only new tests pass |
| "Types correct" | `tsc --noEmit`: exit 0 | No red squiggles |

### Correct Format
```
Verified:
- `bun run lint` → 0 errors, 0 warnings
- `bun run test` → 14 tests passed, 0 failed
- `bun tsc --noEmit` → exit 0
```

---

## Skill 3: Security Best Practices
**Trigger:** Server Actions, API routes, auth, env handling, database queries, code review, deployment.

### Operating Modes
1. **Passive (while coding):** Inject security patterns naturally as you write code
2. **Active (during review):** Detect vulnerabilities in existing code
3. **Full report (on demand):** Comprehensive security audit

### Core Rules (Fail-Secure)
- **Fail-secure, not fail-open:** `SECRET = env['KEY']` (crashes if missing) NOT `env.get('KEY') or 'default'`
- Auth at entry of every Server Action and API route
- Zod validation on ALL external input
- Authorization: verify user owns resource (not just authenticated)
- Generic errors to client, detailed errors to server logs only

### Framework-Specific
**Next.js:** Server Actions for mutations (built-in CSRF). Route Handlers need manual CSRF. Validate `redirect()` targets.
**React:** No `dangerouslySetInnerHTML` without sanitization. Use `httpOnly` cookies for tokens.
**Supabase:** RLS on all multi-tenant tables. Separate policies per operation. `$queryRaw` only.

### Env & Secrets
No defaults for secrets; `.env` in `.gitignore`; no secrets in client-side code; validate all env vars at startup.

---

## Skill 4: Coding Guidelines (Karpathy Rules)
**Trigger:** Always active — foundational coding discipline.

### Think Before Coding
- Surface all tradeoffs BEFORE implementation
- When unclear, ASK — don't assume
- Identify the simplest solution that meets requirements
- Define success criteria upfront

### Simplicity First
- No speculative features (YAGNI)
- No premature abstractions
- Prefer duplication over wrong abstraction
- Delete dead code immediately

### Surgical Changes
- Touch ONLY what's needed for the current task
- One logical change per commit
- Don't "improve" unrelated code while fixing a bug

### Goal-Driven Execution
- Define what "done" looks like before starting
- Loop: implement → verify → adjust until criteria met
- NEVER declare done without verification evidence (→ Skill 2)

---

## Context Budget (70% Rule)
**Always active.**

Above 70% of context window, the model silently degrades: ignores tools, hallucinates more, drops rules adherence, stops mid-task.

**Saturation signs:** generic/repetitive responses, skipped verifications, abrupt stops, rules ignored.

**Mandatory action:** STOP current task → save state to STATE.md → compact or new session → resume with minimal context.

**Budget (200k window):** <80k (40%) comfortable | 80-120k (40-60%) caution | 120-140k (60-70%) save state | >140k (70%+) STOP NOW.

---

## TypeScript Strict Mode (Global Rule)
**Always active for all TypeScript files.**

Every project MUST have `"strict": true` in tsconfig.json plus: `noUncheckedIndexedAccess`, `noImplicitReturns`, `noFallthroughCasesInSwitch`, `forceConsistentCasingInFileNames`.

Prohibitions: No `any` (use `unknown` + narrowing), no `@ts-ignore` without justification, no `enum` (use `as const`), no `export default` (use named exports).

---

## Code Style (Global Rule)
**Always active.**

### Product Thinking (PDD)
Before implementing any feature, ask: Does this solve the USER's problem or a TECHNICAL problem? Is there a simpler solution delivering 80% of the value?

### Conventions
Naming: Components PascalCase, hooks camelCase with `use` prefix, types PascalCase (no `I` prefix), constants UPPER_SNAKE_CASE.
Imports: React/Next → external libs → @/ aliases → relative → types. Always use path aliases.
Next.js: Server Components by default, `"use client"` only when needed, Server Actions for mutations.
No `console.log` in production, no `var`, no `enum`, no `export default`.

---

# On-Demand Skills Index

Skills below are loaded automatically when their trigger is detected. Each skill file contains full documentation.

## Stack OSForge
| Skill | Trigger | Load |
|-------|---------|------|
| Next.js + React | React, Next.js, performance, waterfalls, bundle | `skills/stack/nextjs-react.md` |
| PostgreSQL & Supabase | query, RLS, index, Supabase | `skills/stack/postgres-supabase.md` |
| Frontend UI (shadcn) | UI, componente, landing, shadcn, Magic UI | `skills/stack/frontend-ui.md` |
| Prisma Expert | schema, migration, Prisma | `skills/stack/prisma.md` |
| Supabase Auth | auth, RBAC, session, OAuth | `skills/stack/supabase-auth.md` |
| Stripe | payment, subscription, checkout, webhook | `skills/stack/stripe.md` |
| Bun | Bun.file, Bun.serve, Bun.$ | `skills/stack/bun.md` |
| i18n | multi-language, locale, translation | `skills/stack/i18n.md` |
| Tailwind | Tailwind, utility classes, responsive | `skills/stack/tailwind.md` |

## Workflow & Process
| Skill | Trigger | Load |
|-------|---------|------|
| Git Workflow | branch, commit, worktree, merge | `skills/workflow/git.md` |
| Spec Builder | spec, especificar, tech spec | `skills/workflow/spec-builder.md` |
| PRD Builder | prd, requisitos, requirements | `skills/workflow/prd-builder.md` |
| Architecture Builder | arquitetura, ADR, schema changes | `skills/workflow/architecture.md` |
| Epic Decomposer | épicos, stories, breakdown | `skills/workflow/epic-decomposer.md` |
| Story Executor | executar story, implementar story | `skills/workflow/story-executor.md` |
| Plan Writing | task planning, plan breakdown | `skills/workflow/plan-writing.md` |
| Finishing Branch | finalizar branch, merge, PR, ship | `skills/workflow/finishing-branch.md` |
| Receiving Review | feedback de review, changes requested | `skills/workflow/receiving-review.md` |
| Requirements Clarify | clarificar requisitos, ambiguous | `skills/workflow/requirements-clarify.md` |
| Doc Sanitization | /clean-docs, docs accumulating | `skills/workflow/doc-sanitization.md` |

## Testing
| Skill | Trigger | Load |
|-------|---------|------|
| E2E Testing (Playwright) | E2E, Playwright, visual regression | `skills/testing/e2e-playwright.md` |
| Testing Patterns | testing pyramid, unit test, integration | `skills/testing/patterns.md` |
| Predictive Failure | predict failures, production readiness | `skills/testing/predictive-failure.md` |

## Security
| Skill | Trigger | Load |
|-------|---------|------|
| Insecure Defaults | security hardening, env audit | `skills/security/insecure-defaults.md` |
| Differential Review | PR security review, git diff | `skills/security/differential-review.md` |
| Red Team | red team, offensive security, MITRE | `skills/security/red-team.md` |
| Vulnerability Scanner | vulnerability scan, OWASP | `skills/security/vulnerability.md` |

## Languages
| Skill | Trigger | Load |
|-------|---------|------|
| Rust | Rust, cargo, ownership, lifetimes | `skills/languages/rust.md` |
| Python | Python, FastAPI, Django, Flask | `skills/languages/python.md` |
| Bash/Linux | Bash, shell script, Linux | `skills/languages/bash.md` |
| PowerShell | PowerShell, Windows scripting | `skills/languages/powershell.md` |
| Node.js | Node.js, Express, async Node | `skills/languages/nodejs.md` |

## Design & UX
| Skill | Trigger | Load |
|-------|---------|------|
| Core Web Vitals | LCP, INP, CLS, Lighthouse | `skills/design/core-web-vitals.md` |
| Accessibility | WCAG, a11y, screen reader | `skills/design/accessibility.md` |
| Mobile Design | mobile app, touch targets, iOS/Android | `skills/design/mobile.md` |
| Frontend Design | design system, color theory, typography, UX psychology | `skills/frontend-design/SKILL.md` |
| UI Design Intelligence | identidade visual, paleta por indústria, fintech/healthcare/saas | `skills/ui-design-intelligence/SKILL.md` |
| Web Design Guidelines | UI accessibility audit, design compliance | `skills/web-design-guidelines/SKILL.md` |
| Aesthetic Boost | design bonito, visual marcante, anti-AI-slop, hero, landing | `skills/aesthetic-boost/SKILL.md` |
| Taste Design Dials | premium, awwwards, agência, GSAP, magnetic, perpetual motion, bento 2.0, double-bezel | `skills/taste-design-dials/SKILL.md` |
| Aesthetic Modes | minimalist editorial, brutalist industrial, soft premium, Notion style, Linear style, CRT terminal, Apple-tier | `skills/aesthetic-modes/SKILL.md` |
| Redesign Audit | redesenhar, modernizar UI, upgrade visual, tirar cara de AI, site parece template | `skills/redesign-audit/SKILL.md` |
| Stitch Design Export | Google Stitch, DESIGN.md, exportar design system | `skills/stitch-design-export/SKILL.md` |
| Tailwind Patterns | Tailwind v4, @theme, container queries, arbitrary values | `skills/tailwind-patterns/SKILL.md` |
| OpenUI / GenUI Layout | OpenUI Lang, GenUI, layout DSL, declarative UI plan | `skills/openui-genui-layout/SKILL.md` |

## SEO & GEO
| Skill | Trigger | Load |
|-------|---------|------|
| SEO | SEO, meta tags, sitemap, E-E-A-T | `skills/seo/seo.md` |
| GEO | GEO, AI search optimization, LLM visibility | `skills/seo/geo.md` |

## Claude & AI
| Skill | Trigger | Load |
|-------|---------|------|
| Claude API & Agent SDK | @anthropic-ai/sdk, tool use, streaming | `skills/claude-ai/api-sdk.md` |
| Claude CI/CD Actions | @claude in PRs, automated review | `skills/claude-ai/ci-actions.md` |
| Smart Model Dispatch | subagents, parallel dispatch, cost | `skills/claude-ai/model-dispatch.md` |
| Context7 Docs-First | docs, latest, version-sensitive | `skills/claude-ai/context7.md` |
| Smart Hooks | quality gates, pre-commit, audit | `skills/claude-ai/smart-hooks.md` |
| llmfit Advisor | local LLM, Ollama, hardware fit | `skills/claude-ai/llmfit.md` |

## Meta & Utilities
| Skill | Trigger | Load |
|-------|---------|------|
| Agent Skills Search | buscar skill, domain patterns | `skills/meta/skills-search.md` |
| MCP Builder | MCP server, expose API as tool | `skills/meta/mcp-builder.md` |
| GDPR/LGPD | consent, data rights, privacy | `skills/meta/gdpr-lgpd.md` |
| Parallel Agents | parallel tasks, dispatching | `skills/meta/parallel-agents.md` |
| The Agency | especialista, expert não coberto | `skills/meta/agency.md` |
| App Builder | scaffolding, new project, boilerplate | `skills/meta/app-builder.md` |
| API Patterns | REST, GraphQL, tRPC | `skills/meta/api-patterns.md` |
| Game Development | game, game loop, multiplayer | `skills/meta/game-dev.md` |
| Systematic Debugging | debug methodology, root cause | `skills/meta/debugging.md` |
| Performance Profiling | profiling, Lighthouse, bundle analysis | `skills/meta/profiling.md` |
| Database Design | schema design, database selection | `skills/meta/database-design.md` |
| Deployment | deployment, rollback, blue-green | `skills/meta/deployment.md` |
| Server Management | process management, monitoring | `skills/meta/server-mgmt.md` |
| Documentation Templates | README, API docs, changelog | `skills/meta/doc-templates.md` |
| Lint and Validate | linting, ESLint, Prettier | `skills/meta/lint-validate.md` |
| Code Review | code review, revisar código, PR | `skills/meta/code-review.md` |
| Behavioral Modes | brainstorm mode, implement mode | `skills/meta/behavioral-modes.md` |
| DB State Sync | osforge-db, salvar estado | `skills/meta/db-state-sync.md` |
| Visual Planner | visualizar plano, HTML interativo | `skills/meta/visual-planner.md` |
| OSForge Canvas | canvas, abre no canvas, mostra no browser, revisar interativamente, aprovar antes de implementar | `skills/osforge-canvas/SKILL.md` |
| AutoRefine | melhorar skill, autorefine, otimizar | `skills/meta/autorefine.md` |
| Adversarial Review | adversarial, revisão cínica | `skills/meta/adversarial-review.md` |
| Edge Case Hunter | edge cases, boundary conditions | `skills/meta/edge-case-hunter.md` |
| Elicitation Engine | elicitar, refinar output | `skills/meta/elicitation.md` |
| Readiness Gate | readiness check, quality gate | `skills/meta/readiness-gate.md` |
| Context Distillator | distill, comprimir contexto | `skills/meta/context-distillator.md` |
| Project Context | project context, constituição | `skills/meta/project-context.md` |
| Doc Shard | shard doc, dividir documento | `skills/meta/doc-shard.md` |
| Editorial Review | editorial review, review prose | `skills/meta/editorial-review.md` |
| Output Enforcement | completo, todo o arquivo, exaustivo, sem placeholder, no `// ...`, no `// TODO` | `skills/output-enforcement/SKILL.md` |
| Tool Safety Classifier | modo automático, yolo mode, headless, CI mode, auto-approve, sem confirmação | `skills/tool-safety-classifier/SKILL.md` |
| Context Compact | comprimir contexto, compactar, summary, perto do limite, context full, save state, /compact | `skills/context-compact/SKILL.md` |
| Config Critique | revisar minha skill, validar minha rule, verificar conflito de hooks, lint config | `skills/config-critique/SKILL.md` |
| Stuck Recovery | stuck, travado, loop, não está funcionando, esquece o que estava fazendo | `skills/stuck-recovery/SKILL.md` |
