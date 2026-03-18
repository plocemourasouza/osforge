---
name: code-review
description: >
  Review estruturado de código com checklist adaptado ao stack OSForge.
  Integra adversarial-review e edge-case-hunter automaticamente.
  Use com "code review", "revisar código", "review PR".
trigger: code review|revisar código|review PR|CR
model-tier: sonnet
---

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
