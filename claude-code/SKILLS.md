# Skills & Knowledge Base
Reference skills for Claude Code. Apply automatically based on context.

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
- ❌ Too big: "User authentication system"
- ✅ Right: "Login returns JWT on valid credentials"

### Exceptions (ask first)
Throwaway prototypes, generated code (Prisma Client, shadcn), config files, pure UI styling.

### Test Protection (TDD Enforcement)
When tests FAIL, fix PRODUCTION CODE — NEVER modify tests to make them pass.
- NEVER alter assertions to match wrong output
- NEVER delete or `.skip` failing tests
- NEVER change expected values to match actual
- Only exception: genuine test bug or explicitly requested requirement change

### Stack Patterns
```typescript
// Vitest: Write test FIRST
describe('PaymentService', () => {
  it('should reject expired cards', async () => {
    const result = await service.charge({ cardExp: '01/20', amount: 100 })
    expect(result.success).toBe(false)
    expect(result.error).toBe('CARD_EXPIRED')
  })
})
// THEN implement PaymentService.charge()
```

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
✅ Verified:
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
**Next.js:** Server Actions for mutations (built-in CSRF). Route Handlers need manual CSRF. Validate `redirect()` targets. Never expose internal IDs in URLs without authorization check.

**React:** No `dangerouslySetInnerHTML` without sanitization. No sensitive data in state/context. Use `httpOnly` cookies for tokens (never localStorage).

**TypeScript:** Enable strict mode. No `any` for user input. Use discriminated unions for auth states. Zod schemas for runtime validation.

**Supabase/Database:** RLS on all multi-tenant tables. Separate policies per operation. `$queryRaw` (never `$queryRawUnsafe`). Parameterized queries only. Tenant filter in every query.

### Env & Secrets
- No defaults for secrets; `.env` in `.gitignore`; no secrets in client-side code; validate all env vars at startup

### Rationalizations to Reject
| Excuse | Response |
|--------|----------|
| "Just a dev default" | If it reaches production, it's a vulnerability |
| "Prod overrides it" | Prove with code trace |
| "Behind auth" | Defense in depth |
| "Fix before release" | Fix now |

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
- If a function has one caller, don't abstract it
- Prefer duplication over wrong abstraction
- Delete dead code immediately

### Surgical Changes
- Touch ONLY what's needed for the current task
- One logical change per commit
- Don't "improve" unrelated code while fixing a bug
- If you see something unrelated to fix, note it — don't fix it now

### Goal-Driven Execution
- Define what "done" looks like before starting
- Loop: implement → verify → adjust until criteria met
- NEVER declare done without verification evidence (→ Skill 2)

---

## Skill 5: Product-Driven Spec Development (PDD + Spec-Driven)
**Trigger:** New features, complex tasks, multi-step implementations, "why build this", product validation.

### 6-Phase Process (PDD-enhanced)
0. **Discover** — User problem, hypothesis, success metrics, MVP scope
1. **Specify** — Requirements, constraints, acceptance criteria
2. **Design** — Architecture decisions, component structure, data flow
3. **Tasks** — Break into atomic units, prioritize by user impact
4. **Implement** — Execute tasks with verification at each step
5. **Measure** — Post-deploy metrics, feedback loop, iterate/pivot/abandon

### PDD Principle
Before coding, ask: Does this solve the USER's problem or a TECHNICAL problem? Is there a simpler solution delivering 80% of the value? What metric proves this worked?

### Discover Phase (before Specify)
For user-facing features, create `.specs/features/[feature]/discovery.md`:
- Who suffers and what happens (with evidence, not assumptions)
- Hypothesis: "We believe [solution] will [result] for [persona] because [evidence]"
- Success metrics with baseline, target, measurement method, and timeline
- MVP scope: smallest experiment that validates hypothesis
- Alternatives considered and why discarded

### Impact-First Prioritization (in Tasks phase)
Priority = (User Impact × Confidence) / Technical Effort. Anti-pattern: don't prioritize by what's technically interesting — prioritize by value delivered.

### Measure Phase (after Deploy)
Post-deploy checklist: feature flag/canary, error monitoring, analytics events, metrics dashboard, scheduled review date. Never declare a feature "delivered" without metrics configured. Features without evidence of impact are candidates for removal.

### Persistent Memory
Use `.specs/` directory for cross-session continuity:
```
.specs/
├── project/
│   ├── PROJECT.md, ROADMAP.md, STATE.md, DECISIONS.md
└── features/
    └── [feature]/
        ├── discovery.md  # Problem, hypothesis, metrics (PDD)
        ├── spec.md       # Requirements + acceptance criteria
        ├── design.md     # Technical design
        ├── tasks.md      # Atomic task list with status
        └── stories/      # User stories with product context
```

### User Stories (PDD-enhanced)
Stories MUST include: Product Context (problem observed with evidence, hypothesis, alternatives discarded, risk if not done), Success Metrics (baseline, target, how to measure, timeline), Acceptance Criteria (technical), and Completeness Criteria (includes metrics configured + review scheduled).

### Decision Log (ADR)
Record architectural decisions: Context → Options → Decision → Consequences. Every decision with trade-offs must be logged in DECISIONS.md.

### Context Budget (70% Rule)
Above 70% of context window, the model silently degrades: ignores tools, hallucinates more, drops rules adherence, stops mid-task. No error — just progressive degradation.

**Saturation signs:** generic/repetitive responses, skipped verifications, abrupt stops, rules ignored, shortcuts in defined processes.

**Mandatory action:** STOP current task → save state to STATE.md (task, last checkpoint, next step, modified files, test status) → compact or new session → resume with minimal context (STATE.md + specific task only).

**Prevention:** one feature per session, unload context after completing each phase, sub-agents for isolated tasks, split tasks needing 3+ specs.

**Budget (200k window):** 🟢 <80k (40%) comfortable | 🟡 80-120k (40-60%) caution | 🔴 120-140k (60-70%) save state | ⛔ >140k (70%+) STOP NOW.

**Compression mode (🟡/🔴 zones):** concise responses without preambles, show diffs only, don’t repeat established context, prioritize action over inline documentation.

**Story loading by phase:** Discover/Specify = full story | Design = criteria + edge cases + deps | Implement = criteria + happy path + edge cases | Measure = metrics + completeness only. Reduces ~725 → ~350 tokens per story in implementation phases.

---

## Skill 6: React & Next.js Performance
**Trigger:** Writing/reviewing React components, Next.js pages, data fetching, bundle optimization.

### CRITICAL — Waterfalls
- `Promise.all()` for independent fetches
- Move `await` into branches where actually used
- Suspense boundaries for progressive streaming

### CRITICAL — Bundle
- Direct imports (never barrel files)
- `next/dynamic` for heavy components with `ssr: false`
- Analytics/logging after hydration in `useEffect`

### HIGH — Server-Side
- Auth in all Server Actions
- `React.cache()` for per-request deduplication
- Minimize data serialized to client components

### MEDIUM — Re-renders
- Derive state with `useMemo`, not `useEffect` + `useState`
- Functional `setState` for stable callbacks
- `memo()` for expensive children

---

## Skill 7: PostgreSQL & Supabase Optimization
**Trigger:** Complex queries, migrations, slow queries, RLS, indexes.

### Core Rules
- `EXPLAIN ANALYZE` before approving complex queries
- `select` only needed fields (never `findMany()` without select)
- Avoid N+1 (use `include` with `select`)

### Indexing
- Multi-tenant: tenant_id first in composite indexes
- Partial indexes for active-only filters; always index foreign keys

### RLS
- All multi-tenant tables need RLS enabled
- Separate policies per operation (SELECT, INSERT, UPDATE, DELETE)
- Use `auth.jwt()` / `auth.uid()` — never trust client params

### Connections
- App: port 6543 (pooled via PgBouncer); Migrations: port 5432 (direct)

### Raw SQL When
Aggregations, JSON/JSONB ops, full-text search, pivot tables, window functions, recursive CTEs. Always `$queryRaw`.

---

## Skill 8: Frontend UI System (shadcn Ecosystem)
**Trigger:** Building UI, landing pages, dashboards, forms, maps, animations.

### Component Sources (priority)
1. **shadcn/ui** — Core primitives. `bunx shadcn@latest add <component>`. Use Shadcn MCP first.
2. **Magic UI** — 150+ animations. `bunx shadcn@latest add "https://magicui.design/r/<component>"`. Dir: `components/magicui/`
3. **Aceternity UI** — 100+ premium effects. `bunx shadcn@latest add @aceternity/<component>`. Dir: `components/aceternity/`
4. **mapcn** — Maps (MapLibre, no API key). `bunx shadcn@latest add "https://mapcn.dev/r/map"`. Dir: `components/ui/map/`

### Decision Matrix
| Need | Source |
|------|--------|
| Forms, tables, nav | shadcn/ui |
| Text animation | Magic UI |
| Background effect | Aceternity or Magic UI |
| 3D / hover | Aceternity |
| Maps | mapcn |

### Rules
- Magic UI / Aceternity: always `"use client"` (Framer Motion)
- Heavy animations: `next/dynamic({ ssr: false })`
- Animated components are leaf nodes — never wrap RSC inside them
- Theme: always CSS variables, never hardcode colors

### Visual Verification
After implementing visual components, ALWAYS verify:
- Layout matches design/spec
- Responsiveness: mobile (375px), tablet (768px), desktop (1280px+)
- States: loading, empty, error, success
- Accessibility: tab navigation, screen reader labels, contrast
NEVER declare a component "working" without visual evidence.

---

## Skill 9: Git Workflow
**Trigger:** Creating branches, parallel work, merges, version control for agent development.

### Branch Naming
`feature/`, `bugfix/`, `hotfix/`, `chore/`, `refactor/` + kebab-case description

### Conventional Commits (mandatory)
Format: `type(scope): description` — max 72 chars, lowercase, no period.
Types: feat, fix, refactor, docs, style, test, chore, perf, ci.
Breaking changes: `feat!:` or `BREAKING CHANGE:` footer.

### Git Worktrees for Parallel Agents
When multiple independent features need parallel implementation:
```bash
git worktree add ../project-feature-auth feature/auth
git worktree add ../project-feature-dashboard feature/dashboard
# Each agent works in its own isolated directory
# After: merge sequentially, resolve conflicts, test
git worktree remove ../project-feature-auth
```
Use worktrees (not branches) for parallel agents — branches share working directory and cause conflicts.

### Pre-Commit
- `tsc --noEmit` passes; `lint` passes; no `console.log` debug; no secrets in staging

---

## Skill 10: Predictive Failure Analysis
**Trigger:** After implementation + tests pass. "What could go wrong?", "predict failures", "production readiness", "pre-deploy".

Finds failures that tests DON'T catch — pattern matching against common production failure modes.

### Categories
1. **Race Conditions:** Double-click submit, async state out of order, missing debounce, useEffect without cleanup/abort
2. **Data Edge Cases:** Unicode in text fields, float precision, empty arrays, null in nested objects, timezone mismatches, monetary rounding
3. **Network:** Unhandled timeouts, retry without backoff, stale cache post-deploy, CORS prod vs dev, missing rate limiting
4. **State Management:** Memory leaks (useEffect no cleanup), stale closures, hydration mismatch, form state lost on back button
5. **Security in Production:** CSRF on Route Handlers, XSS via dangerouslySetInnerHTML, exposed stack traces, tokens in URL params
6. **UX Under Stress:** 10k+ items without virtualization, large uploads without progress, slow 3G experience, accessibility without mouse

### Output
For each issue: Severity (🔴🟠🟡🔵) × Probability + File:Line + Scenario + Impact + Suggested fix.
Only report issues with evidence in actual code. No theoretical problems.

---

## Skill 11: Core Web Vitals
**Trigger:** Performance optimization, LCP/INP/CLS issues, Lighthouse audits.

- **LCP** ≤ 2.5s: Optimize images (WebP/AVIF, sizes, priority), preload critical resources, minimize render-blocking CSS/JS
- **INP** ≤ 200ms: Break long tasks, use `requestIdleCallback`, debounce handlers, avoid synchronous layout
- **CLS** ≤ 0.1: Set explicit dimensions on images/videos, reserve space for dynamic content, avoid injecting content above viewport

Quick Wins: `<Image>` with `priority` for above-fold, `next/font` (no FOUT), `loading="lazy"` below-fold, preconnect to third-party origins.

---

## Skill 12: Accessibility (WCAG 2.1)
**Trigger:** UI implementation, component creation, code review, accessibility audit.

- Semantic HTML (`<nav>`, `<main>`, `<article>`, `<button>` not `<div onClick>`)
- All images: meaningful `alt` or `aria-hidden="true"` if decorative
- Form inputs: associated `<label>` elements
- Focus management: visible focus indicators, logical tab order
- Color contrast: 4.5:1 normal text, 3:1 large text
- Keyboard navigation: all interactive elements reachable and operable
- Testing: tab through flow, VoiceOver, `npx axe-cli` or Lighthouse a11y

---

## Skill 13: SEO
**Trigger:** Page creation, metadata, sitemap, structured data, crawlability.

- Unique `<title>` and `<meta name="description">` per page
- Open Graph + Twitter Card meta tags; canonical URLs
- `robots.txt` and `sitemap.xml`; structured data (JSON-LD)
- Semantic heading hierarchy (one `<h1>` per page)
- Next.js: `generateMetadata()`, `generateStaticParams()`, `next-sitemap`

---

## Skill 14: Doc Sanitization
**Trigger:** `/clean-docs`, docs accumulating, docs >30 days old.

### Permanent Docs (always maintain)
README.md, tasks/todo.md, tasks/lessons.md, docs/architecture.md, docs/features.md

### Temporary Docs (consolidate/remove after 30 days)
specs/*.md, plans/*.md, notes/*.md

### Process
1. Inventory → 2. Analyze → 3. Propose → 4. **Confirm (never delete without approval)** → 5. Execute → 6. Report

---

## Skill 15: Agent Skills Search
**Trigger:** Need specialized skills, best practices, or domain patterns.

```bash
python3 ~/Development/osforge/scripts/buscar-skill.py <term>
python3 ~/Development/osforge/scripts/buscar-skill.py --cat security
python3 ~/Development/osforge/scripts/buscar-skill.py --stats
```

Tiers: **Tier 1:** Anthropic, Superpowers, Vercel, Trail of Bits, Supabase. **Tier 2:** Context Engineering, Cloudflare, Sentry. **Tier 3:** Antigravity (634 skills), Expo, Curadoria.

---

## Skill 16: Prisma Expert
**Trigger:** Complex schema (>10 models), migration strategies, query performance, relation patterns, multi-tenant data isolation.

Covers: multi-tenant schema isolation, polymorphic relations (union pattern), soft delete, safe production migrations (additive-only, two-phase drops), N+1 prevention with eager loading, cursor-based pagination, interactive transactions with isolation levels, Prisma + Supabase integration (directUrl vs pooled).

---

## Skill 17: Next.js + Supabase Auth
**Trigger:** Auth middleware, multi-org RBAC, session management, token refresh, RLS-by-tenant, OAuth flows.

Covers: middleware auth guard with `createServerClient`, server-side `requireAuth()` helper, multi-org RBAC with role hierarchy, RLS policies for tenant isolation, token refresh via SSR cookies (never localStorage), OAuth with PKCE flow. Rule: always use `getUser()` not `getSession()` for auth checks.

---

## Skill 18: E2E Testing (Playwright)
**Trigger:** Cross-page flow testing, checkout flows, onboarding, visual regression, Playwright setup.

Covers: Playwright config for Next.js with Bun, Page Object Model pattern, auth state fixtures (login via API not UI), multi-step flow testing, visual regression with `toHaveScreenshot`, API mocking with `page.route`. Best practice: `getByRole`/`getByLabel` only, never CSS selectors.

---

## Skill 19: Stripe Integration
**Trigger:** Checkout, subscription billing, webhooks, pricing page, payment forms, refund logic.

Covers: Stripe Checkout sessions for subscriptions, webhook handler with signature verification, subscription sync to DB via `upsert`, customer portal for self-service billing, idempotent webhook processing. Rules: NEVER handle raw card data, always verify webhook signatures, use metadata to link Stripe ↔ user.

---

## Skill 20: Bun Development
**Trigger:** Bun-specific APIs (Bun.file, Bun.serve, Bun.$), workspace config, Bun test patterns, runtime edge cases.

Covers: Bun.file (fast I/O), Bun.serve (native HTTP), Bun.$ (shell tagged templates), bun:sqlite (built-in), workspace config, `bun test` patterns with mock. Gotchas: binary lockfile, native addon compatibility, snapshot format differences.

---

## Skill 21: MCP Builder
**Trigger:** Creating MCP servers for internal services, exposing APIs as MCP tools/resources, MCP architecture.

Covers: MCP server with `@modelcontextprotocol/sdk`, tool definitions with Zod schemas, resource endpoints, stdio and SSE transports, registration in Claude Code and Cursor configs, testing with InMemoryTransport. Principles: atomic tools, typed inputs, safe (read-only default), paginated responses.

---

## Skill 22: i18n & Localization
**Trigger:** Multi-language support, locale routing, translation management, date/currency formatting.

Covers: `next-intl` setup with App Router, middleware locale routing, translation files with ICU MessageFormat (plurals, interpolation), `useFormatter` for dates/currency, locale-prefixed routing. Best practice: never hardcode user-facing strings, use `namespace.context.element` key pattern.

---

## Skill 23: GDPR / LGPD Data Handling
**Trigger:** Consent management, data subject rights, privacy policies, data retention, audit logging, LGPD compliance.

Covers: LGPD vs GDPR mapping, consent management schema (purpose-based), data export (right to access), account deletion (right to erasure), audit logging middleware, data retention cron jobs. Requirements: DPO/Encarregado designation, breach notification process, cookie consent banner.

---

## Skill 24: Insecure Defaults Detection
**Trigger:** Security hardening, env variable audit, config review, pre-deployment security scan.

Covers: fail-open detection patterns — permissive env fallbacks (`|| '*'`), open CORS, missing rate limiting, tables without RLS, Server Actions without auth, missing security headers. Scan pattern: search for `|| '*'`, `|| true`, `cors()` without args, tables without RLS. Source: Trail of Bits methodology.

---

## Skill 25: Differential Review
**Trigger:** PR security review, git diff analysis for auth/payments/permissions changes.

Covers: 4-step process (scope → analyze high-risk → git history context → structured output), file risk categorization (auth=🔴, api=🟡), security-focused diff checks, CI integration for missing security tests. Red flags: `@ts-ignore` near auth, `as any` in permissions, removed security tests.

---

## Skill 26: Dispatching Parallel Agents
**Trigger:** 2+ independent tasks without shared state, large multi-file refactoring, parallelizable work units.

Covers: decision matrix (when to parallelize vs sequence), task specification format (self-contained with goal/files/context/acceptance), execution pattern with context embedding, merge strategy (integration test → import resolution → type check), anti-patterns (shared migrations, implicit ordering, >5 parallel tasks).

---

## Skill 27: Claude API & Agent SDK (TypeScript)
**Trigger:** Code importing `@anthropic-ai/sdk` or `@anthropic-ai/claude-agent-sdk`, building AI-powered features, tool use, streaming, structured outputs, programmatic agents.

Covers: Claude API (Messages, streaming, tool runner with `betaZodTool` + Zod, structured outputs via `output_config`, batches at 50% cost, files API), Agent SDK (subagents programáticos, hooks PostToolUse, MCP integration, permission modes, session forking), current models (Opus 4.6, Sonnet 4.6, Haiku 4.5) with IDs e pricing, adaptive thinking config, effort parameter. 11 reference files on-demand (80KB). Source: `anthropics/skills/claude-api`.

---

## Skill 28: Claude CI/CD Actions
**Trigger:** Setting up @claude in PRs/issues, automated PR review, CI/CD integration with Claude, GitHub Actions workflow, flaky test detection.

Covers: `anthropics/claude-code-action@v1` setup, interactive mode (@claude mentions), automated PR review workflow, structured output for CI analysis (flaky test detection), MCP integration in Actions, plugin installation in workflows, CI log access tools (`mcp__github_ci__*`). Rules: never hardcode API key, use `--max-turns` to cap costs, Sonnet 4.6 for reviews.

---

## Skill 29: Smart Model Dispatch
**Trigger:** Feature implementation with multiple subtasks, spawning subagents, parallel task dispatch, cost optimization, or when task complexity varies across work units.

Covers: 3-tier routing (Opus for planning/security/architecture, Sonnet for implementation/debugging/review, Haiku for boilerplate/i18n/tests/docs), per-agent model mapping (planner→opus, debugger→sonnet, docs→haiku), dispatch patterns for feature/bugfix/audit workflows, parallel dispatch with mixed models, cost estimation reference (~65% savings vs all-opus), escalation rules (haiku→sonnet→opus on failure).

---

## Skill 30: Context7 Docs-First
**Trigger:** Questions about Next.js, Supabase, Prisma, Stripe, Playwright, Bun, shadcn/ui, Vercel, or any version-sensitive library. Also trigger on "docs", "latest", "current version", or API integration tasks.

Covers: Workflow resolve-library-id → query-docs → respond from source of truth. Quick reference table with Context7 IDs for all stack libraries (/vercel/next.js, /supabase/supabase, /prisma/prisma, /stripe/stripe-node, /microsoft/playwright, /shadcn-ui/ui, /oven-sh/bun, /colinhacks/zod). Rules: max 3 calls per question, prefer official sources, report gaps honestly. Requires Context7 MCP server.

---

## Skill 31: Smart Hooks (Python)
**Trigger:** Setting up quality gates, safety rails, or developer experience hooks for Claude Code. Also trigger when configuring pre-commit checks, blocking dangerous commands, or adding audit logging to a project.

Covers: 4 production-grade Python hooks — pre_tool_use.py (blocks dangerous bash commands + protected file writes + audit log), post_tool_use.py (TypeScript quality gates: console.log, any type, @ts-ignore, export default), pre_compact.py (conversation backup before context compaction), session_end.py (session logging + macOS notification). Design: command hooks (not prompt — zero token cost), fail-open, <100ms each, configurable via JSON.

---

## TypeScript Strict Mode (Global Rule)
**Always active for all TypeScript files.**

Every project MUST have `"strict": true` in tsconfig.json plus: `noUncheckedIndexedAccess`, `noImplicitReturns`, `noFallthroughCasesInSwitch`, `forceConsistentCasingInFileNames`.

Prohibitions: No `any` (use `unknown` + narrowing), no `@ts-ignore` without justification, no disabling strict mode, no `enum` (use `as const`), no `export default` (use named exports).

## Code Style (Global Rule)
**Always active.**

### Product Thinking (PDD)
Before implementing any feature, ask: Does this solve the USER's problem or a TECHNICAL problem? Is there a simpler solution delivering 80% of the value? How will the user perceive this change? What metric proves this worked? Product trade-offs > technical elegance.

### Conventions
Naming: Components PascalCase, hooks camelCase with `use` prefix, types PascalCase (no `I` prefix), constants UPPER_SNAKE_CASE.
Imports: React/Next → external libs → @/ aliases → relative → types. Always use path aliases.
Next.js: Server Components by default, `"use client"` only when needed, Server Actions for mutations.
No `console.log` in production, no `var`, no `enum`, no `export default`.


---

## Skill 32: llmfit Advisor (Local LLM Hardware Fit)
**Trigger:** Detecta hardware e recomenda LLMs locais. TRIGGER quando: usuário pergunta quais modelos rodam localmente, quer configurar Ollama/LM Studio, menciona rodar modelos offline, precisa de alternativa local por custo ou privacidade LGPD, dados sensíveis que não podem ir para API externa (Tressen, Red Caveat), ou quando smart-model-dispatch identifica tarefa Haiku-eligible com alto volume.
Requires: `llmfit` binary (`brew install llmfit` ou `cargo install llmfit`). Commands: `llmfit --json system` (hardware), `llmfit recommend --json --use-case coding --limit 3` (recomendações). Output JSON com score, fit_level (Perfect/Good/Marginal/TooTight), best_quant, estimated_tps, run_mode (GPU/CPU+GPU/CPU). Integra com smart-model-dispatch: tarefas Haiku-eligible + dados sensíveis → modelo local preferível. Mapping HF→Ollama incluso. Casos OSForge: Tressen/Red Caveat (privacidade obrigatória), OSystems clientes PME (hardware limitado), tasks repetitivas de desenvolvimento (economia de API).

---

## Skill 33: The Agency — Biblioteca de Especialistas de IA
**Trigger:** Precisar de um especialista em qualquer área não coberta pelas skills técnicas acima. Inclui: engenharia (segurança, SRE, DevOps, mobile, blockchain), design (UI/UX, sistemas de design, identidade, prompts de imagem), marketing (SEO, conteúdo, redes sociais, growth, ASO), mídia paga (Google/Meta Ads, PPC, analytics), produto (roadmap, priorização, pesquisa de mercado), gestão de projetos (planejamento, Jira, scrum), vendas (outbound, discovery, MEDDPICC, pipeline), suporte (atendimento, compliance, operações), qualidade (QA, testes de API, WCAG, performance), e especialistas avançados (orquestração de agentes, SOC2/ISO, supply chain, MCP builder).

**Load:** `Leia skills/agency/SKILL.md`

121 especialistas em 10 divisões. Carregamento hierárquico: router → índice da divisão → agente. Zero custo de contexto até ser ativado.


---

## Skill 34: Spec Builder (Collaborative)
**Trigger:** "spec", "especificar", "definir feature", "tech spec", ou quando o Orchestrator assigna fase Spec.

Facilitação colaborativa de especificação técnica. Produz tech-spec com acceptance criteria testáveis, tasks ordenadas por dependência, e riscos. Stack-aware — respeita project-context.md. Checkpoint [A] Approve / [E] Edit / [S] Simplify antes de avançar. Output: `docs/specs/{feature}.md` com frontmatter de rastreamento. Não gera — FACILITA com o usuário.

---

## Skill 35: PRD Builder (Collaborative)
**Trigger:** "prd", "requisitos", "requirements", "product requirements", ou quando Orchestrator assigna fase PRD (triage COMPLEX).

Facilitação colaborativa de Product Requirements Document. Guia definição de problema, usuários, requisitos funcionais/não-funcionais, métricas de sucesso e escopo MVP. Checkpoint por seção. Output: `docs/prd/{feature}.md` com frontmatter. Nível COMPLEX — para projetos com ambiguidade significativa.

---

## Skill 36: Architecture Builder (ADR)
**Trigger:** "arquitetura", "architecture", "decisões técnicas", "ADR", schema changes, ou quando Orchestrator assigna fase Architecture.

Facilitação de decisões arquiteturais com ADRs (Architecture Decision Records). Stack-aware — otimiza para Next.js/Prisma/Supabase. Avalia opções com trade-offs explícitos, gera migration paths para Prisma, valida RLS policies para Supabase. Output: `docs/specs/arch-decisions-{feature}.md`. FACILITA decisão — não decide sozinho.

---

## Skill 37: Epic Decomposer
**Trigger:** "épicos", "stories", "decompor", "breakdown", ou quando Orchestrator assigna fase Stories/Épicos.

Decompõe specs, PRDs ou requisitos em épicos e stories implementáveis. Cada story com ACs testáveis, tasks com file paths, dependências mapeadas e estimativa qualitativa. Output: `docs/specs/stories/{feature}/` com index + story files. Referencia artefatos anteriores (spec, arch-decisions).

---

## Skill 38: Story Executor
**Trigger:** "executar story", "implementar story", "dev story", ou quando Orchestrator assigna fase de implementação dentro do sprint loop.

Coordena implementação de uma story seguindo suas tasks e ACs. Invoca skills de execução corretos do OSForge (prisma-expert, nextjs-supabase-auth, tdd-workflow, etc.) na ordem das tasks. Verifica ACs ao completar. Atualiza status.yaml. Fluxo: load story → execute tasks in order → verify ACs → report.

---

## Skill 39: Adversarial Review
**Trigger:** "adversarial", "revisão cínica", "critica isso", "o que está errado?", ou automaticamente na fase Final Review do Orchestrator.

Revisão cínica e adversarial de qualquer artefato: código, specs, PRDs, schemas, configs. Persona: Senior Paranóico. Encontra o que está errado E o que está faltando. Metodologia: assumptions → dependencies → failure modes → security → perf → edge cases → missing requirements. Severity P0-P3. Recomendações concretas.

---

## Skill 40: Code Review (OSForge)
**Trigger:** "code review", "revisar código", "review PR", ou automaticamente na fase Review do sprint loop.

Review estruturado de código adaptado ao stack OSForge (Next.js/Prisma/Supabase/shadcn). Checklist: TypeScript strict, Server Components, RLS, error handling, ACs coverage, performance. Integra adversarial-review + edge-case-hunter automaticamente. Output: lista de findings com severity + suggestions.

---

## Skill 41: Edge Case Hunter
**Trigger:** "edge cases", "boundary conditions", "o que pode dar errado?", ou invocado automaticamente por code-review e adversarial-review.

Caça exaustiva de edge cases por enumeração sistemática de caminhos: null/undefined, empty, boundary, concurrent, timing, encoding, overflow, auth bypass, state transitions. Method-driven, não attitude-driven (ortogonal ao adversarial-review). Reporta APENAS paths sem handling adequado.

---

## Skill 42: Elicitation Engine
**Trigger:** "elicitar", "refinar output", "melhorar spec", ou invocável dentro de outros skills para melhorar qualquer artefato.

Refinamento iterativo de outputs usando técnicas de elicitação estruturadas: 5 Whys, Assumption Surfacing, Scenario Planning, Pre-Mortem, Socratic Questioning. Carrega methods.csv com catálogo de técnicas. Pode ser standalone ou composable dentro de spec-builder, prd-builder, arch-builder.

---

## Skill 43: Readiness Gate
**Trigger:** "readiness check", "pronto para implementar?", "quality gate", ou automaticamente antes do sprint loop em triage COMPLEX.

Quality gate pré-implementação. Valida alinhamento e completude entre PRD ↔ Architecture ↔ Épicos antes de iniciar coding. Checklist: cobertura de requisitos, consistência de decisões, stories com ACs testáveis, dependências resolvidas, riscos mitigados. GO / NO-GO com justificativa.

---

## Skill 44: Context Distillator
**Trigger:** "distill", "comprimir contexto", "compress", ou quando documento excede tamanho ideal para LLM.

Compressão lossless de documentos para consumo otimizado por LLMs. Preserva 100% da informação factual eliminando overhead textual (hedging, repetição, filler). Não é sumarização (lossy) — é compressão lossless. Carrega compression-rules.md com padrões de compressão. Target: 40-60% do original.

---

## Skill 45: Project Context Generator
**Trigger:** "project context", "gerar contexto", "constituição do projeto", ou no início de qualquer projeto novo.

Analisa codebase existente e gera project-context.md — a "constituição" do projeto que alimenta todos os outros skills e agents. Escaneia: package.json, tsconfig, prisma/schema, .env, estrutura de diretórios. Output: stack confirmado, convenções, padrões, constraints. Fonte de verdade para o Orchestrator.

---

## Skill 46: Doc Shard
**Trigger:** "shard doc", "dividir documento", "split markdown", ou quando documento excede context window.

Divide documentos markdown grandes em arquivos menores organizados com index. Preserva referências cruzadas, gera table of contents no index, e mantém frontmatter consistente. Útil para specs longas, PRDs extensos, ou documentação que precisa ser carregada parcialmente.

---

## Skill 47: Editorial Review
**Trigger:** "editorial review", "review prose", "review structure", "revisar documento", ou na fase final de qualquer documento.

Revisão editorial de documentos técnicos em 2 modos: **prose** (copy-editing clínico — clareza, concisão, gramática, tom) e **structure** (reorganização — flow lógico, headings, redundância, gaps). Pode rodar ambos em sequência. Output: documento revisado com tracked changes.

---

## Skill 48: App Builder
**Trigger:** Scaffolding, new project, project template, boilerplate, "create new app", application orchestration.

Application building orchestrator. Analyzes user requests, determines project type, selects tech stack, and coordinates agents for full-stack application creation from natural language.

---

## Skill 49: API Patterns
**Trigger:** REST, GraphQL, tRPC, API design, endpoint design, rate limiting, API versioning.

API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination, authentication patterns, rate limiting, and documentation.

---

## Skill 50: Game Development
**Trigger:** Game, game loop, sprites, 2D/3D, multiplayer, game engine.

Game development orchestrator providing core principles and routing to platform-specific sub-skills (web, mobile, PC, VR/AR) and dimensional specialties (2D, 3D).

---

## Skill 51: Red Team Tactics
**Trigger:** Red team, offensive security, attack simulation, MITRE ATT&CK.

Red team tactics based on MITRE ATT&CK framework. Attack phases, reconnaissance, initial access, privilege escalation, defense evasion, lateral movement, and reporting principles.

---

## Skill 52: Tailwind Patterns
**Trigger:** Tailwind, utility classes, responsive design, Tailwind v4.

Tailwind CSS v4 principles. CSS-first configuration, container queries, modern responsive patterns, color systems, typography, animations, and component extraction.

---

## Skill 53: Systematic Debugging
**Trigger:** Debug methodology, root cause analysis, systematic troubleshooting.

4-phase systematic debugging methodology: reproduce → isolate → understand → fix. Evidence-based verification and root cause analysis to prevent random guessing.

---

## Skill 54: Mobile Design
**Trigger:** Mobile app design, touch targets, responsive mobile, iOS/Android design.

Mobile-first design thinking for iOS and Android. Touch interaction patterns, performance optimization, platform conventions, navigation, typography, and offline capabilities.

---

## Skill 55: Rust Pro
**Trigger:** Rust, cargo, ownership, borrowing, lifetimes, async Rust.

Master Rust 1.75+ with modern async patterns, advanced type system features, and production-ready systems programming. Ownership, lifetimes, async design, and ecosystem expertise.

---

## Skill 56: Python Patterns
**Trigger:** Python, FastAPI, Django, Flask, pip, poetry, Python architecture.

Python development principles and decision-making. Framework selection (FastAPI, Django, Flask), async patterns, type hints, project structure, and thinking-based approaches.

---

## Skill 57: Brainstorming
**Trigger:** Brainstorm, explorar ideia, antes de começar, o que construir, alternativas, ideia vaga, ideação, problem exploration, Socratic questioning, "não sei como fazer", "quero construir X".

Refinamento socrático de ideia ANTES de qualquer código ou spec técnica. Fase 1: entender o problema real (não a solução). Fase 2: explorar 2-3 abordagens distintas com tradeoffs. Fase 3: detalhar a abordagem escolhida em chunks aprovados um por vez. Salva design document em `.osforge/designs/` para alimentar spec-builder. Fonte: obra/superpowers (MIT).

---

## Skill 58: Web Design Guidelines
**Trigger:** Web design review, UI accessibility audit, design compliance.

Web Interface Guidelines review and compliance checking. Audit UI code for accessibility, design principles, and best practices against established web standards.

---

## Skill 59: Clean Code
**Trigger:** Clean code, code standards, naming conventions, readability.

Pragmatic coding standards emphasizing conciseness, directness, and solution-focus. SRP, DRY, KISS, YAGNI principles, naming conventions, and avoiding over-engineering.

---

## Skill 60: Bash Linux
**Trigger:** Bash, shell script, Linux commands, terminal, CLI scripting.

Bash/Linux terminal patterns for macOS and Linux. Critical commands, piping, error handling, scripting best practices, and file operations.

---

## Skill 61: PowerShell Windows
**Trigger:** PowerShell, Windows scripting, Windows administration.

PowerShell Windows patterns. Operator syntax, error handling, safe scripting, cmdlet usage, and Windows-specific gotchas.

---

## Skill 62: Frontend Design
**Trigger:** Design system, color theory, typography, animation, UX psychology, visual design.

Design thinking and decision-making for web UI. Color systems, typography, visual effects, animation, motion graphics, and component design patterns.

---

## Skill 63: Performance Profiling
**Trigger:** Performance profiling, Lighthouse, Web Vitals profiling, bundle analysis.

Performance profiling principles. Measurement, Core Web Vitals analysis, bottleneck identification, and optimization strategies.

---

## Skill 64: Node.js Best Practices
**Trigger:** Node.js, Express patterns, async Node, Node architecture.

Node.js development principles and decision-making. Framework selection, async patterns, security, architecture patterns, and thinking-based approaches.

---

## Skill 65: Architecture
**Trigger:** System architecture, design patterns, architectural decisions, scalability patterns.

Architectural decision-making framework. Requirements analysis, trade-off evaluation, pattern selection, ADR documentation, and design principles.

---

## Skill 66: GEO Fundamentals
**Trigger:** GEO, AI search optimization, LLM visibility, ChatGPT/Perplexity ranking.

Generative Engine Optimization for AI-powered search engines (ChatGPT, Claude, Perplexity). Citation strategies, content structure, and visibility optimization.

---

## Skill 67: Database Design
**Trigger:** Database design, schema design, database selection, ORM choice, indexing strategy, migrations.

Database design principles and decision-making. Schema design, database selection (PostgreSQL, Neon, Turso, SQLite), ORM selection, indexing, optimization, and safe migrations.

---

## Skill 68: Deployment Procedures
**Trigger:** Deployment, release process, rollback, blue-green, canary deployment.

Deployment principles for safe production releases. Platform selection, deployment strategies, rollback procedures, verification steps, and operational safety.

---

## Skill 69: Server Management
**Trigger:** Server management, process management, monitoring, health checks, scaling.

Server management principles. Process management tools, monitoring strategy, scaling decisions, observability, and operational thinking.

---

## Skill 70: Documentation Templates
**Trigger:** Documentation template, README template, API docs template, changelog, ADR.

Documentation templates and structure guidelines. README, API documentation, code comments, changelog, ADR format, and AI-friendly documentation.

---

## Skill 71: Vulnerability Scanner
**Trigger:** Vulnerability scan, security scan, OWASP checklist, dependency audit.

Vulnerability analysis principles. OWASP 2025 framework, supply chain security, attack surface mapping, risk prioritization, and security expert mindset.

---

## Skill 72: Next.js React Expert
**Trigger:** Next.js performance, React optimization, waterfall elimination, bundle optimization, SSR/SSG.

React and Next.js performance optimization from Vercel Engineering. 57 optimization rules prioritized by impact. Eliminate waterfalls, optimize bundles, reduce JavaScript, and server-side strategies.

---

## Skill 73: Lint and Validate
**Trigger:** Linting, code validation, ESLint, Prettier, quality checks.

Automatic quality control and static analysis. Linting, formatting, type checking, and security audits for Node.js, Python, and other ecosystems.

---

## Skill 74: Code Review Checklist
**Trigger:** Code review checklist, review guidelines, PR review.

Code review guidelines covering correctness, security, performance, testing, style, and maintainability. Structured checklist for quality assurance.

---

## Skill 75: Behavioral Modes
**Trigger:** Agent mode, brainstorm mode, implement mode, debug mode, review mode, teach mode.

AI behavioral modes for adaptive problem-solving. Brainstorm, implement, debug, review, teach, ship, and orchestrate modes with specific behaviors and outputs.

---

## Skill 76: Plan Writing
**Trigger:** Task planning, plan breakdown, structured planning, implementation plan.

Structured task planning framework. Small focused tasks, clear verification criteria, dependency identification, and logical ordering for multi-step work.

---

## Skill 77: SEO Fundamentals
**Trigger:** SEO basics, E-E-A-T, search ranking, meta tags, structured data.

SEO fundamentals covering E-E-A-T framework, Core Web Vitals, on-page optimization, meta tags, structured data, and search ranking principles.

---

## Skill 78: Testing Patterns
**Trigger:** Testing pyramid, test patterns, AAA pattern, unit testing, integration testing.

Testing patterns and principles. Testing pyramid, unit testing, integration testing, E2E testing, mocking strategies, and test organization.

---

## Skill 79: Web App Testing
**Trigger:** Web app testing, E2E testing, Playwright testing, visual regression.

Web application testing principles. Deep audit approaches, Playwright-based testing, accessibility testing, visual regression, and discovery-driven testing.

---

## Skill 80: Finishing a Development Branch
**Trigger:** Finalizar branch, merge, pull request, PR, ship, branch completa, done, concluído, terminar feature, fechar branch, "pronto para mergear", "abrir PR".

Workflow de finalização de branch: (1) verificação pré-merge — testes, TypeScript, lint, status; (2) resumo do trabalho na branch; (3) menu de opções [M]erge / [P]ull Request / [K]eep / [D]iscard com execução segura. Discard requer confirmação explícita. Arquiva specs em `.osforge/archive/`. Fonte: obra/superpowers (MIT).

---

## Skill 81: Receiving Code Review
**Trigger:** Responder review, feedback de review, changes requested, responder PR, tratar comments, resolver feedback, revisor pediu mudanças, CHANGES_REQUESTED.

Resposta estruturada a feedback de code review: cataloga itens em bloqueante/importante/opcional, classifica cada um (concordo/concordo parcialmente/discordo), implementa correções com verificação por item, gera resposta formal ao reviewer e solicita re-review. Commits atômicos por item. Fonte: obra/superpowers (MIT).

---

## Skill 82: Using Git Worktrees
**Trigger:** Git worktree, worktrees, parallel development, multiple branches, isolated workspace, branch paralela, desenvolvimento paralelo, agents paralelos em branches separadas.

Setup e uso de git worktrees para desenvolvimento paralelo: layout recomendado de diretórios por agent, integração com dispatching-parallel-agents (um worktree por task paralela), comandos essenciais (add/remove/list/prune), setup de node_modules e .env por worktree, portas diferentes para dev servers. Fonte: obra/superpowers (MIT).

---

## Skill 83: Requirements Clarify
**Trigger:** Clarificar requisitos, requirements clarification, underspecified, ambiguous requirements, clarify, antes do plano, esclarecer requisitos, spec tem áreas vagas, "pode ser qualquer coisa", requirements vagas.

Clarificação estruturada por dimensões de cobertura ANTES do plano técnico: funcional, dados, UX, integração, segurança. Máximo 8-10 perguntas priorizadas por impacto. Produz Clarifications Record em `.osforge/designs/{feature}-clarifications.md` que alimenta spec-builder. Fonte: github/spec-kit (MIT).

---

## Skill 84: DB State Sync
**Trigger:** Salvar estado, registrar decisão, add-decision, set-phase, resumir sessão, buscar decisão, osforge-db, estado do projeto, blocker, retomar sessão, where did I leave off.

Gerencia o estado de projetos no banco SQLite local do OSForge (`~/.osforge/osforge.db`). Usa `osforge-db` CLI para salvar progresso de fases, registrar decisões arquiteturais, adicionar/resolver blockers e retomar sessões com contexto preciso (~50 tokens via `osforge-db resume`). Banco global cross-project; banco local por projeto via `--scope=local`. FTS5 para busca semântica cross-project em decisões passadas.

---

## Skill 85: Visual Planner (Plan → Interactive HTML)
**Trigger:** Visualizar plano, breakdown visual, transformar spec em HTML, apresentar PRD visualmente, gerar HTML interativo, tornar spec mais fácil de seguir, visual breakdown, plan breakdown, turn spec into HTML, make plan visual, visualize this spec, break down this plan.

Camada de apresentação do pipeline de planejamento. Transforma qualquer documento de planejamento (PRD, spec, épico, ADR, ou markdown genérico) em um breakdown HTML single-page interativo com scroll-based navigation, animações reveal, flow diagrams, expandable cards, stat badges, e review system embutido. Reconhece automaticamente os formatos OSForge (`osforge-prd`, `osforge-spec`, `osforge-architecture`, `osforge-epic`, `osforge-phase-context`). Design system warm com Bricolage Grotesque + DM Sans, 13 componentes visuais reutilizáveis, e sistema de review com clipboard output para iteration loop. Zero dependências além de Google Fonts. Source: `ethanplusai/visualplanner` (adapted).
