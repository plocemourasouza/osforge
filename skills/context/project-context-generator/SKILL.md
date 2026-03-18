---
name: project-context-generator
description: >
  Analisa codebase existente e gera project-context.md — a "constituição"
  do projeto que alimenta todos os outros skills e agents.
  Use com "project context", "gerar contexto", "constituição do projeto".
trigger: project context|gerar contexto|generate context|constituição
model-tier: sonnet
---

# Project Context Generator

## Objetivo
Descobrir stack, padrões, convenções e regras do projeto e gerar um
`project-context.md` lean e otimizado para consumo por LLMs. Este arquivo
é a fonte de verdade que todos os skills e agents devem respeitar.

## Processo

### 1. Discovery — Análise do Projeto

**Arquivos de configuração (ler todos que existirem):**
- `package.json` / `bun.lockb` — dependências e versões exatas
- `tsconfig.json` — strictness, paths, target, module resolution
- `next.config.js` ou `next.config.ts` — features, rewrites, middleware
- `prisma/schema.prisma` — models, relations, enums, datasource
- `.env.example` — variáveis de ambiente esperadas (NUNCA .env real)
- `tailwind.config.ts` — customizações, plugins, design tokens
- `.eslintrc` / `biome.json` / `eslint.config.mjs` — regras de lint
- `vercel.json` — configuração de deploy
- `supabase/config.toml` — configuração Supabase local

**Padrões de código (amostrar ~5 arquivos de cada tipo):**
- `app/` — estrutura de rotas, layouts, loading/error states, metadata
- `components/` — organização, naming, co-location de styles
- `lib/` ou `utils/` — helpers, clients, configurações
- `server/` ou `actions/` — Server Actions vs API Routes pattern
- `prisma/` — migrations, seeds, middleware de Prisma
- `supabase/` — migrations SQL, RLS policies, edge functions

**Padrões de segurança:**
- RLS policies (arquivos SQL em supabase/migrations/)
- Middleware de auth (middleware.ts, auth patterns)
- Validação (Zod schemas — onde definidos, como organizados)
- CORS config, rate limiting patterns
- LGPD compliance patterns (consentimento, anonimização)

**Padrões de teste:**
- Framework (vitest, jest, playwright, cypress)
- Organização (`__tests__/`, co-located, `*.test.ts`, `*.spec.ts`)
- Mocking patterns, fixtures, factories

### 2. Apresentar Discovery
Mostrar resumo do que foi encontrado:
- Stack com versões
- Número de patterns identificados
- Áreas de regras encontradas

Perguntar: "Isso está correto? Algo a adicionar ou corrigir?"

### 3. Gerar project-context.md

```markdown
---
project: "{nome}"
stack: "{resumo curto}"
generated: "{data}"
generator: "osforge/project-context-generator"
---

# Project Context para AI Agents

_Regras e padrões críticos. Foco em detalhes não-óbvios que agentes
poderiam errar sem orientação explícita._

## Stack & Versões
- {tecnologia}: {versão exata}
- {tecnologia}: {versão exata}
- Runtime: {node/bun} {versão}
- Deploy: {Vercel/outro}

## Estrutura de Projeto
- {padrão de organização de pastas}
- {convenções de naming de arquivos}
- {co-location rules}

## Next.js / React
- Server vs Client Components: {quando usar cada}
- Data fetching: {padrão — RSC, Server Actions, SWR, etc.}
- Server Actions vs API Routes: {padrão do projeto}
- State management: {approach}
- Form handling: {pattern}

## Prisma / Database
- Schema conventions: {naming, relations}
- Query patterns: {includes, selects, transactions}
- Migration workflow: {como rodar, naming}

## Supabase
- Auth: {provider, flow}
- RLS: {padrão de policies}
- Storage: {patterns se usado}
- Edge Functions: {se usado}

## Segurança
- Input validation: {Zod — onde e como}
- Auth middleware: {pattern}
- LGPD: {rules se aplicável}
- Rate limiting: {se configurado}

## Testes
- Framework: {nome} com {runner}
- Organização: {pattern}
- Coverage: {expectativa}
- E2E: {se usado, framework}

## Estilo de Código
- Lint: {ESLint/Biome config}
- Format: {Prettier config}
- Import ordering: {padrão}
- Commits: {Conventional Commits se usado}

## Anti-Patterns (NÃO FAZER)
- {regra negativa importante}
- {regra negativa importante}
- Nunca usar `any` em TypeScript
- Nunca commitar sem aprovação explícita do usuário

## Questões em Aberto
- {decisão pendente que afeta implementação}
```

### 4. Salvar e Confirmar
- Salvar em `docs/project-context.md` ou path indicado pelo usuário
- Confirmar com usuário que o conteúdo está correto
- Se usar Cursor: sugerir adicionar path nas rules para auto-load
