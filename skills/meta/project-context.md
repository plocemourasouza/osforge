# Project Context Generator

**Trigger:** "project context", "gerar contexto", "constituição do projeto", ou no início de qualquer projeto novo.

---

## Purpose

Analisa codebase existente e gera `project-context.md` — a "constituição" do projeto que alimenta todos os outros skills e agents.

---

## Output Location

`.osforge/project-context.md`

---

## Scan Sources

| Source | Information |
|--------|-------------|
| `package.json` | Dependencies, scripts, name |
| `tsconfig.json` | TypeScript configuration |
| `prisma/schema.prisma` | Database schema, models |
| `.env.example` | Environment variables needed |
| `src/` structure | Architecture patterns |
| `README.md` | Project description |

---

## Generated Content

```markdown
# Project Context: [Project Name]

## Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript 5.3 (strict) |
| Database | PostgreSQL via Supabase |
| ORM | Prisma |
| Auth | Supabase Auth |
| UI | shadcn/ui + Tailwind |
| Testing | Vitest + Playwright |

## Architecture

```
src/
├── app/           # Next.js App Router
├── components/    # React components
│   ├── ui/        # shadcn components
│   └── features/  # Feature components
├── lib/           # Utilities
└── types/         # TypeScript types
```

## Conventions

- **Components**: PascalCase, named exports
- **Hooks**: camelCase with `use` prefix
- **API Routes**: `/api/[resource]/route.ts`
- **Server Actions**: `/app/actions/[domain].ts`

## Database Models

- User (id, email, name, role)
- Organization (id, name, slug)
- [Other models...]

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection | Yes |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase admin key | Yes |

## Constraints

- Multi-tenant: all queries must filter by `organizationId`
- RLS enabled on all tables
- No `any` types
- Server Components by default
```

---

## Usage

### Generate Context
```bash
# Run at project root
osforge context generate

# Or let Claude Code detect and generate
"Analyze this codebase and generate project context"
```

### Update Context
```bash
# After significant changes
osforge context update
```

---

## Integration

All other skills read `project-context.md` to:
- Know the tech stack
- Follow existing conventions
- Respect constraints
- Use correct patterns

---

## Source of Truth

Project context is the **single source of truth** for:
- Orchestrator routing decisions
- Spec Builder stack-awareness
- Code Review checklist customization
- Story Executor skill selection
