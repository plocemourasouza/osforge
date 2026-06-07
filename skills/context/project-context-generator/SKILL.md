---
name: project-context-generator
description: "Analisa codebase e gera project-context.md + constitution.md — os documentos governantes do projeto. ACIONE quando: iniciar em projeto novo, projeto não tem project-context.md, precisar atualizar contexto após mudanças de stack, criar princípios do projeto. Keywords: project context, gerar contexto, constituição do projeto, generate context, constitution, project principles, regras do projeto."
model: sonnet
allowed-tools: Read, Write, Bash, Glob, Grep
metadata:
  version: '1.1'
  source_concept: github/spec-kit (constitution pattern)
---

## Estado do projeto
!`[ -f project-context.md ] && echo "project-context.md existente ($(wc -l < project-context.md) linhas)" || echo "project-context.md não encontrado — gerando do zero"`
!`[ -f .osforge/memory/constitution.md ] && echo "constitution.md existente" || echo "constitution.md não encontrado"`
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Stack: {list(d.get(\"dependencies\",{}).keys())[:8]}')" 2>/dev/null || echo "package.json não encontrado"`

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

## Gotchas

- **Gerar project-context.md muito longo**: ideal é 100-150 linhas. Acima disso, usar `@path` imports para separar seções por domínio (ex: `@prisma-patterns.md`, `@nextjs-patterns.md`).
- **Não atualizar após mudanças de stack**: project-context.md desatualizado é pior que não ter — faz agents implementarem com padrões obsoletos. Atualizar sempre que houver mudança de dependência major ou novo padrão estabelecido.
- **Constitution.md com princípios vagos**: "escrever código limpo" não é um princípio acionável. Cada princípio deve ser verificável: ou passa ou não passa em um code review.
- **Expor .env real na análise**: ao analisar variáveis de ambiente, usar APENAS `.env.example` ou `.env.local.example`. NUNCA ler `.env` real com credenciais.

---

## Constitution.md — Princípios Governantes (padrão spec-kit)

Além do `project-context.md` (que descreve COMO o projeto está construído),
gerar também um `constitution.md` que define OS PRINCÍPIOS que guiam decisões:

```markdown
---
type: osforge-constitution
project: "{nome do projeto}"
created_at: {data}
governs: [spec-builder, arch-builder, story-executor, code-review]
---

# Project Constitution: {nome}

## Princípios de Código
- {princípio 1} — Ex: "Preferir Server Components ao Client Components sempre que possível"
- {princípio 2} — Ex: "Toda query Prisma deve incluir index nos campos de filtro frequente"
- {princípio 3} — Ex: "Nunca expor service role key no cliente"

## Princípios de Qualidade
- {princípio} — Ex: "Todo PR deve ter testes para happy path + pelo menos 1 edge case"
- {princípio} — Ex: "Zero TypeScript errors antes de merge — sem @ts-ignore não justificado"

## Princípios de Produto
- {princípio} — Ex: "Decisão de produto antes de decisão técnica — sempre"
- {princípio} — Ex: "Features de LGPD têm prioridade zero — nunca adiadas"

## Princípios de Arquitetura
- {princípio} — Ex: "Multi-tenant: sempre filtrar por organizationId nas queries"
- {princípio} — Ex: "Server Actions para mutations, API Routes para webhooks externos"

## Restrições Absolutas (NUNCA fazer)
- {restrição} — Ex: "Nunca usar `any` sem comentário explicando por quê"
- {restrição} — Ex: "Nunca commitar .env ou credenciais reais"
- {restrição} — Ex: "Nunca desabilitar RLS em tabela de dados de usuário"

## Prioridades em Conflito
Quando houver conflito entre princípios:
1. Segurança e LGPD compliance
2. Correctness (comportamento correto)
3. Manutenibilidade
4. Performance
5. DX (developer experience)
```

Salvar em `.osforge/memory/constitution.md`.

**A constitution.md é lida automaticamente** pelo orchestrator, spec-builder e arch-builder como referência para decisões. Atualizar sempre que o time tomar uma decisão arquitetural significativa.
