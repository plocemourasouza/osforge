---
name: prisma-expert
description: "Padrões avançados de Prisma ORM. ACIONE quando: mudanças de schema com >3 models, estratégias de migration, queries lentas ou N+1, relações many-to-many ou polimórficas, isolamento multi-tenant, debugging de Prisma. Keywords: prisma, schema, migration, query, relation, database, orm, model, seed, index, RLS."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: prompt
          prompt: "Se o comando contiver 'prisma migrate deploy' em ambiente que não seja dev local, confirme com o usuário antes de executar."
metadata:
  author: osforge
  version: '1.1'
---

## Contexto do projeto
!`[ -f prisma/schema.prisma ] && echo "Schema encontrado: $(wc -l < prisma/schema.prisma) linhas, $(grep -c '^model' prisma/schema.prisma) models" || echo "prisma/schema.prisma não encontrado"`
!`[ -f .env ] && grep -c 'DATABASE_URL' .env > /dev/null 2>&1 && echo "DATABASE_URL configurada" || echo "DATABASE_URL não encontrada no .env"`

# Prisma Expert

## Schema Design Patterns

### Multi-Tenant Isolation
```prisma
model Organization {
  id        String   @id @default(cuid())
  slug      String   @unique
  members   Member[]
  // ALL tenant-scoped models reference org
}

model Project {
  id             String       @id @default(cuid())
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id])
  // Always filter by organizationId in queries
  @@index([organizationId])
}
```

### Polymorphic Relations (Union Pattern)
```prisma
model Notification {
  id          String   @id @default(cuid())
  type        NotificationType
  // Use JSON for polymorphic payload
  payload     Json
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  @@index([userId, type])
}

enum NotificationType {
  COMMENT
  MENTION
  SYSTEM
}
```

### Soft Delete
```prisma
model Record {
  id        String    @id @default(cuid())
  deletedAt DateTime?
  // Middleware filters deletedAt globally
  @@index([deletedAt])
}
```

## Migration Strategies

### Safe Production Migrations
1. **Additive only** — add columns/tables, never remove in same deploy
2. **Two-phase drops** — mark deprecated → deploy without usage → drop in next release
3. **Default values** — always provide defaults for new required columns
4. **Index concurrently** — for large tables, use raw SQL with `CREATE INDEX CONCURRENTLY`

```bash
# Generate migration without applying
bunx prisma migrate dev --create-only --name add_tenant_field

# Review generated SQL before applying
cat prisma/migrations/*_add_tenant_field/migration.sql

# Apply after review
bunx prisma migrate dev
```

### Migration Checklist
- [ ] New columns have defaults or are optional
- [ ] No column renames (add new → migrate data → drop old)
- [ ] Indexes added for new foreign keys
- [ ] RLS policies updated if Supabase
- [ ] Seed data updated

## Query Optimization

### N+1 Prevention
```typescript
// ❌ N+1 problem
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } })
}

// ✅ Eager loading
const users = await prisma.user.findMany({
  include: { posts: { where: { published: true }, take: 10 } }
})

// ✅ For complex cases, use raw query
const result = await prisma.$queryRaw`
  SELECT u.*, COUNT(p.id) as post_count
  FROM "User" u
  LEFT JOIN "Post" p ON p."authorId" = u.id
  GROUP BY u.id
  HAVING COUNT(p.id) > 5
`
```

### Pagination (Cursor-based)
```typescript
// ✅ Cursor pagination (performant for large datasets)
const posts = await prisma.post.findMany({
  take: 20,
  skip: 1, // Skip cursor itself
  cursor: { id: lastPostId },
  orderBy: { createdAt: 'desc' },
})

// ❌ Offset pagination (slow on large tables)
const posts = await prisma.post.findMany({
  skip: page * 20,
  take: 20,
})
```

### Transaction Patterns
```typescript
// Interactive transaction with timeout
const result = await prisma.$transaction(async (tx) => {
  const account = await tx.account.update({
    where: { id: fromId },
    data: { balance: { decrement: amount } },
  })
  if (account.balance < 0) throw new Error('INSUFFICIENT_FUNDS')
  
  await tx.account.update({
    where: { id: toId },
    data: { balance: { increment: amount } },
  })
  return account
}, { timeout: 5000, isolationLevel: 'Serializable' })
```

## Prisma + Supabase Integration
- Use `directUrl` for migrations, `url` (pooled) for queries
- RLS policies apply at DB level, Prisma bypasses via service role
- Always validate tenant context in Server Actions before Prisma calls
- Use `@db.Uuid` for Supabase auth user references

## References
- [postgres-optimization](../postgres-optimization/SKILL.md) — DB-level optimization
- [security-best-practices](../security-best-practices/SKILL.md) — RLS + auth patterns

## Gotchas

- **`migrate dev` vs `migrate deploy`**: `migrate dev` gera migration + aplica. `migrate deploy` só aplica (para CI/prod). Nunca rodar `migrate dev` em produção — ele pode resetar dados.
- **Renomear coluna causa DROP + ADD**: Prisma não detecta rename — gera `DROP COLUMN` + `ADD COLUMN`, zerando os dados. Para renomear: (1) adicionar nova coluna, (2) migrar dados via script, (3) remover antiga em release separada.
- **`include` vs `select` na mesma query**: não misturar `include` e `select` no mesmo nível — Prisma não permite. Escolha um: `select` para controle granular, `include` para relations completas.
- **RLS não aplica via service role**: quando usando Supabase com `service_role`, o Prisma bypassa RLS completamente. Sempre validar `organizationId` no nível da Server Action antes de qualquer query Prisma.
- **Offset pagination em tabelas grandes**: `skip: page * 20` vai ficando progressivamente mais lento conforme a tabela cresce. Para tabelas >10K registros, sempre usar cursor-based pagination com `cursor: { id: lastId }`.
- **`$queryRaw` precisa de template literal**: `prisma.$queryRaw(sql)` é vulnerável a SQL injection. Sempre usar template literal tagged: `` prisma.$queryRaw`SELECT * FROM "User" WHERE id = ${id}` ``.
- **Migrations sem `--create-only` em prod**: sempre gerar a migration com `--create-only`, revisar o SQL gerado, e só então aplicar. Nunca deixar o Prisma aplicar migration automaticamente em produção.
