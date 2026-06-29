# Stack Coverage Map

The verifiable contract behind **ADR-012**: every supported technology maps to either a
**skill** (durable discipline) or **Context7 docs-first** (volatile API facts). Skills never
duplicate API docs — for current syntax, the agent reads Context7.

Legend: ✅ dedicated skill · 🟦 covered by a broader skill · 📚 Context7 docs-first (no skill) · 🆕 created under ADR-012

## Frameworks

| Technology | Coverage | Where |
|---|---|---|
| Next.js (App Router) | ✅ | `nextjs-react-expert`, `stack/nextjs-react.md` |
| Node | 🟦 | `nodejs-best-practices` |
| Express | 🟦 | `nodejs-best-practices` |
| Vite | 📚 | Context7 |
| Astro | 📚 | Context7 (skill only if usage grows) |

## Languages

| Technology | Coverage | Where |
|---|---|---|
| TypeScript (strict) | ✅ | `typescript-strict.mdc`, `clean-code` |
| Python (FastAPI/Django/Flask, pytest) | ✅ | `python-patterns` |
| Ruby (Rails) | 📚 | Context7 (skill if Rails becomes a real target — highly opinionated) |
| PHP | 📚 | Context7 |
| Java | 📚 | Context7 |

## ORM & Database

| Technology | Coverage | Where |
|---|---|---|
| Prisma (default ORM) | ✅ | `prisma-expert`, `stack/prisma.md` |
| PostgreSQL | ✅ | `postgres-optimization`, `stack/postgres-supabase.md` |
| Qdrant (vector) | 🟦 | used by `osforge-db`; as a client → Context7 |
| SQLite | 🟦 | used by `osforge-db`; as a client → Context7 |

## Auth

| Technology | Coverage | Where |
|---|---|---|
| Supabase Auth (SSR) | ✅ | `nextjs-supabase-auth` |
| Better Auth | ✅ 🆕 | `better-auth` (current API → Context7) |

## UI & Validation

| Technology | Coverage | Where |
|---|---|---|
| shadcn/ui + Tailwind | ✅ | `frontend-ui-system`, `tailwind-patterns` |
| Zod | 📚 | Context7 + enforced by `security-best-practices` (validate all external input) |
| Accessory libs (TanStack Query, SWR, React Hook Form, Recharts, next-themes, lucide-react, Framer Motion, GSAP) | 📚 / 🟦 | Context7; motion/taste via `taste-design-dials` |

## Runtime, Deploy, Payments

| Technology | Coverage | Where |
|---|---|---|
| Bun | ✅ | `bun-development`, `stack/bun.md` |
| Vercel | ✅ | `vercel-deploy` |
| AWS | ✅ 🆕 | `aws-deploy` (current CLI/service → Context7) |
| Stripe | ✅ | `stripe-integration` |
| ASAAS | ✅ 🆕 | `asaas-integration` (current API → Context7) |

## Testing

| Technology | Coverage | Where |
|---|---|---|
| Playwright (E2E) | ✅ | `e2e-testing-patterns` |
| Bun test | ✅ | `testing-patterns` |
| pytest | 🟦 | `python-patterns` |
| Jest | 📚 | Context7 + `testing-patterns` principles |

## AI tools

| Technology | Coverage | Where |
|---|---|---|
| Claude Code · Cursor | ✅ | this repo (deploy targets) |
| Context7 (docs MCP) | ✅ | `context7-docs-first` — the docs-first discipline itself |

## AI / LLM tooling (product features)

| Technology | Coverage | Where |
|---|---|---|
| Structured LLM output (decision: Instructor / PydanticAI / Zod) | ✅ | `llm-structured-output` (discipline) |
| Instructor (Python) · Instructor-JS | 📚 | Context7 (`instructor`) |
| PydanticAI (typed agent runtime) | 📚 | Context7 (`pydantic-ai`) |
| Zod (TS schema/validation) | 📚 / 🟦 | Context7 + `security-best-practices` (validate all external input) |

---

**Maintenance:** when adding a technology to the stack, add a row here and apply ADR-012 —
default to Context7; create a lean skill only for durable discipline or weak-coverage (new/regional) tech.
Validate any new skill's activation with `scripts/test-skill-triggering.sh` (include pt-BR prompts).
