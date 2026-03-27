---
name: code-review
description: "Review estruturado de código com checklist adaptado ao stack OSForge. ACIONE quando: code review, revisar código, review PR, CR. Integra adversarial-review e edge-case-hunter automaticamente. Keywords: code review, revisar código, review PR, CR, pull request, diff, changes, revisar mudanças."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Bash, Glob, Grep
metadata:
  version: '1.1'
---

## Contexto do review
!`git log --oneline -10 2>/dev/null || echo "Git não disponível ou não inicializado"`
!`git diff --stat HEAD 2>/dev/null | tail -5 || echo "Diff não disponível"`

# Code Review

## Papel
Reviewer técnico rigoroso mas construtivo. Foco em correção, segurança,
performance e manutenibilidade. Respeita project-context.md.

## Inputs
- **diff ou changes** — Código a revisar (identificar automaticamente)
- **story file** (opcional) — Se existe, verificar ACs contra implementação
- **project-context.md** — Regras do codebase (carregar se existir)

## Execução

### 1. Identificar Escopo
- Identificar arquivos modificados e tipo de mudança
- Carregar story file se referenciado
- Carregar project-context.md

### 2. Checklist Estruturado

**Funcionalidade:**
- [ ] Todos ACs da story satisfeitos? (se story existe)
- [ ] Lógica de negócio correta para happy path?
- [ ] Error states tratados adequadamente?
- [ ] Loading states implementados? (para UI changes)

**TypeScript:**
- [ ] Tipos corretos e específicos (sem `any`)?
- [ ] Strict mode respeitado?
- [ ] Interfaces/types exportados quando necessário?
- [ ] Zod schemas para inputs externos?

**Next.js Patterns:**
- [ ] Server vs Client Components corretos?
- [ ] Server Actions vs API Routes conforme padrão do projeto?
- [ ] Metadata/SEO configurado (para páginas)?
- [ ] Error boundaries e loading states?

**Database/Supabase:**
- [ ] Prisma queries eficientes (sem N+1)?
- [ ] RLS policies cobrindo novos dados?
- [ ] Migrations reversíveis?
- [ ] Indexes para queries frequentes?

**Segurança:**
- [ ] Inputs validados com Zod?
- [ ] Auth verificado nos endpoints?
- [ ] Sem dados sensíveis expostos em client?
- [ ] CORS e rate limiting se aplicável?
- [ ] LGPD compliance (dados pessoais)?

**Qualidade:**
- [ ] Sem console.log ou código de debug?
- [ ] Imports organizados?
- [ ] Naming conventions seguidas?
- [ ] Sem código duplicado?
- [ ] Testes para happy path + edge cases?

### 3. Análise Profunda
- Invocar `edge-case-hunter` no diff (se mudanças > 20 linhas)
- Identificar patterns que divergem do project-context

### 4. Verdict

```markdown
## Code Review: {identificação}

**Verdict:** APPROVED | CHANGES_REQUESTED
**Files reviewed:** {N}
**Findings:** {N}

### Issues (devem ser resolvidos)
1. {issue com localização e sugestão}

### Sugestões (recomendado)
1. {sugestão}

### Positivos
1. {algo que ficou bom}
```

Se CHANGES_REQUESTED: listar cada issue com correção sugerida.
Se APPROVED: pode incluir sugestões opcionais para melhorar.


## Gotchas

- **Aprovar sem verificar ACs da story**: se existe uma story associada, SEMPRE verificar cada AC contra o código. Muitos PRs passam no review técnico mas falham silenciosamente nos critérios de aceitação de negócio.
- **Focar só em style issues**: review de code style (imports, naming) é Baixa prioridade. Issues de segurança, lógica de negócio incorreta e N+1 queries são Alta prioridade. Não investir 80% do review em problemas de formatação.
- **Não invocar edge-case-hunter**: para diffs >20 linhas, edge-case-hunter é mandatório — ele encontra casos que o review manual rotineiramente perde (valores null, strings vazias, concorrência, limites de paginação).
- **APPROVED com "sugestões opcionais" que são críticas**: se um issue é crítico para segurança ou correção, deve ser CHANGES_REQUESTED, não APPROVED com nota. A distinção importa para o PR workflow.
- **Não checar impacto de mudanças de schema**: toda mudança em `prisma/schema.prisma` exige verificação de: (1) migration gerada, (2) RLS policies impactadas, (3) queries que podem quebrar com o novo schema.
- **Ignorar `bun tsc --noEmit`**: sempre mencionar se o type-check passa. TypeScript errors silenciados com `@ts-ignore` ou `any` são red flags que devem aparecer no relatório de review.
