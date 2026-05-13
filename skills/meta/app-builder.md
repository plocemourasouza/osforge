# App Builder

**Trigger:** Scaffolding, new project, project template, boilerplate, "create new app", application orchestration.

---

## Purpose

Application building orchestrator. Analyzes user requests, determines project type, selects tech stack, and coordinates agents for full-stack application creation from natural language.

---

## Project Types

| Type | Stack | Use Case |
|------|-------|----------|
| **Web App** | Next.js + Supabase + Prisma | SaaS, dashboards |
| **API** | Next.js API Routes or Hono | Backend services |
| **Mobile** | React Native + Expo | iOS/Android apps |
| **CLI** | Bun + Commander | Command-line tools |

---

## Workflow

```
1. Analyze request → Extract requirements
2. Determine type → Web, API, Mobile, CLI
3. Select stack → Based on requirements
4. Generate scaffold → Project structure
5. Coordinate agents → Parallel implementation
```

---

## OSForge Stack (Default)

```bash
# Create Next.js app with OSForge defaults
bunx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Add core dependencies
cd my-app
bun add @supabase/supabase-js @prisma/client zod
bun add -d prisma @types/node
```

---

## Project Structure

```
my-app/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   ├── (dashboard)/
│   │   ├── api/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/          # shadcn components
│   │   └── features/    # Feature components
│   ├── lib/
│   │   ├── supabase/
│   │   ├── prisma/
│   │   └── utils/
│   └── types/
├── prisma/
│   └── schema.prisma
├── public/
└── tests/
```

---

## Agent Coordination

```
1. system-architect → Define structure
2. database-architect → Design schema
3. backend-engineer → API routes
4. frontend-engineer → UI components
5. test-engineer → Write tests
```

---

## Quick Start Templates

### SaaS with Auth
```bash
bun create osforge/saas my-saas
```

### API Only
```bash
bun create osforge/api my-api
```

### Mobile App
```bash
bunx create-expo-app my-mobile --template with-supabase
```
