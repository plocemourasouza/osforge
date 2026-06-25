---
name: project-context-generator
description: "Analyzes a codebase and generates project-context.md + constitution.md — the project's governing documents. Use when: starting on a new project, the project has no project-context.md, you need to update context after stack changes, or you want to create project principles. Keywords: project context, generate context, project constitution, generate context, constitution, project principles, project rules."
model: sonnet
allowed-tools: Read, Write, Bash, Glob, Grep
metadata:
  version: '1.1'
  source_concept: github/spec-kit (constitution pattern)
---

## Project state
!`[ -f project-context.md ] && echo "project-context.md exists ($(wc -l < project-context.md) lines)" || echo "project-context.md not found — generating from scratch"`
!`[ -f .osforge/memory/constitution.md ] && echo "constitution.md exists" || echo "constitution.md not found"`
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Stack: {list(d.get(\"dependencies\",{}).keys())[:8]}')" 2>/dev/null || echo "package.json not found"`

# Project Context Generator

## Objective
Discover the project's stack, patterns, conventions and rules and generate a
lean `project-context.md` optimized for consumption by LLMs. This file
is the source of truth that all skills and agents must respect.

## Process

### 1. Discovery — Project Analysis

**Configuration files (read all that exist):**
- `package.json` / `bun.lockb` — dependencies and exact versions
- `tsconfig.json` — strictness, paths, target, module resolution
- `next.config.js` or `next.config.ts` — features, rewrites, middleware
- `prisma/schema.prisma` — models, relations, enums, datasource
- `.env.example` — expected environment variables (NEVER the real .env)
- `tailwind.config.ts` — customizations, plugins, design tokens
- `.eslintrc` / `biome.json` / `eslint.config.mjs` — lint rules
- `vercel.json` — deploy configuration
- `supabase/config.toml` — local Supabase configuration

**Code patterns (sample ~5 files of each type):**
- `app/` — route structure, layouts, loading/error states, metadata
- `components/` — organization, naming, style co-location
- `lib/` or `utils/` — helpers, clients, configurations
- `server/` or `actions/` — Server Actions vs API Routes pattern
- `prisma/` — migrations, seeds, Prisma middleware
- `supabase/` — SQL migrations, RLS policies, edge functions

**Security patterns:**
- RLS policies (SQL files in supabase/migrations/)
- Auth middleware (middleware.ts, auth patterns)
- Validation (Zod schemas — where defined, how organized)
- CORS config, rate limiting patterns
- LGPD compliance patterns (consent, anonymization)

**Test patterns:**
- Framework (vitest, jest, playwright, cypress)
- Organization (`__tests__/`, co-located, `*.test.ts`, `*.spec.ts`)
- Mocking patterns, fixtures, factories

### 2. Present Discovery
Show a summary of what was found:
- Stack with versions
- Number of patterns identified
- Rule areas found

Ask: "Is this correct? Anything to add or fix?"

### 3. Generate project-context.md

```markdown
---
project: "{name}"
stack: "{short summary}"
generated: "{date}"
generator: "osforge/project-context-generator"
---

# Project Context for AI Agents

_Critical rules and patterns. Focus on non-obvious details that agents
could get wrong without explicit guidance._

## Stack & Versions
- {technology}: {exact version}
- {technology}: {exact version}
- Runtime: {node/bun} {version}
- Deploy: {Vercel/other}

## Project Structure
- {folder organization pattern}
- {file naming conventions}
- {co-location rules}

## Next.js / React
- Server vs Client Components: {when to use each}
- Data fetching: {pattern — RSC, Server Actions, SWR, etc.}
- Server Actions vs API Routes: {project pattern}
- State management: {approach}
- Form handling: {pattern}

## Prisma / Database
- Schema conventions: {naming, relations}
- Query patterns: {includes, selects, transactions}
- Migration workflow: {how to run, naming}

## Supabase
- Auth: {provider, flow}
- RLS: {policy pattern}
- Storage: {patterns if used}
- Edge Functions: {if used}

## Security
- Input validation: {Zod — where and how}
- Auth middleware: {pattern}
- LGPD: {rules if applicable}
- Rate limiting: {if configured}

## Tests
- Framework: {name} with {runner}
- Organization: {pattern}
- Coverage: {expectation}
- E2E: {if used, framework}

## Code Style
- Lint: {ESLint/Biome config}
- Format: {Prettier config}
- Import ordering: {pattern}
- Commits: {Conventional Commits if used}

## Anti-Patterns (DO NOT DO)
- {important negative rule}
- {important negative rule}
- Never use `any` in TypeScript
- Never commit without explicit user approval

## Open Questions
- {pending decision that affects implementation}
```

### 4. Save and Confirm
- Save to `docs/project-context.md` or the path indicated by the user
- Confirm with the user that the content is correct
- If using Cursor: suggest adding the path to the rules for auto-load

## Gotchas

- **Generating a project-context.md that is too long**: ideal is 100-150 lines. Beyond that, use `@path` imports to split sections by domain (e.g., `@prisma-patterns.md`, `@nextjs-patterns.md`).
- **Not updating after stack changes**: an outdated project-context.md is worse than none — it makes agents implement with obsolete patterns. Update whenever there is a major dependency change or a new established pattern.
- **Constitution.md with vague principles**: "write clean code" is not an actionable principle. Each principle must be verifiable: it either passes or fails in a code review.
- **Exposing the real .env in the analysis**: when analyzing environment variables, use ONLY `.env.example` or `.env.local.example`. NEVER read the real `.env` with credentials.

---

## Constitution.md — Governing Principles (spec-kit pattern)

In addition to `project-context.md` (which describes HOW the project is built),
also generate a `constitution.md` that defines THE PRINCIPLES guiding decisions:

```markdown
---
type: osforge-constitution
project: "{project name}"
created_at: {date}
governs: [spec-builder, arch-builder, story-executor, code-review]
---

# Project Constitution: {name}

## Code Principles
- {principle 1} — Ex: "Prefer Server Components over Client Components whenever possible"
- {principle 2} — Ex: "Every Prisma query must include an index on frequently filtered fields"
- {principle 3} — Ex: "Never expose the service role key on the client"

## Quality Principles
- {principle} — Ex: "Every PR must have tests for the happy path + at least 1 edge case"
- {principle} — Ex: "Zero TypeScript errors before merge — no unjustified @ts-ignore"

## Product Principles
- {principle} — Ex: "Product decision before technical decision — always"
- {principle} — Ex: "LGPD features have priority zero — never postponed"

## Architecture Principles
- {principle} — Ex: "Multi-tenant: always filter by organizationId in queries"
- {principle} — Ex: "Server Actions for mutations, API Routes for external webhooks"

## Absolute Constraints (NEVER do)
- {constraint} — Ex: "Never use `any` without a comment explaining why"
- {constraint} — Ex: "Never commit .env or real credentials"
- {constraint} — Ex: "Never disable RLS on a table holding user data"

## Conflicting Priorities
When there is a conflict between principles:
1. Security and LGPD compliance
2. Correctness (correct behavior)
3. Maintainability
4. Performance
5. DX (developer experience)
```

Save to `.osforge/memory/constitution.md`.

**The constitution.md is read automatically** by the orchestrator, spec-builder and arch-builder as a reference for decisions. Update whenever the team makes a significant architectural decision.
