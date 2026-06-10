# Template de Brief de Delegação

> Workers (sub-agentes, Task tools) **não têm acesso à conversa com o usuário**.
> O brief é o único contexto que o worker recebe. Um brief incompleto gera output
> incompleto — lixo entra, lixo sai. Preencha todos os campos antes de despachar.

---

## Template Canônico

```markdown
## Objetivo
<!-- 1-3 frases: o que fazer e por que isso importa agora. -->

## Skills a Carregar
<!-- Paths exatos que o worker deve ler ANTES de implementar.
     Exemplo: `skills/stack/prisma.md`, `skills/security-best-practices.md` -->
- 

## Escopo de Arquivos
**Pode ler/editar:**
- 

**Fora de escopo (não tocar):**
- 

## Contexto Essencial
<!-- Decisões já tomadas, constraints, padrões do projeto que o worker precisa
     respeitar. Inclua: stack relevante, convenções, decisões arquiteturais,
     por que abordagens alternativas foram descartadas. -->

## Critério de Pronto
<!-- Verificável: comando a executar + resultado esperado.
     O worker NÃO pode reportar done sem rodar este comando e ver este resultado. -->
**Comando:** `<comando>`
**Resultado esperado:** <o que deve aparecer>

## Formato de Output
<!-- O que reportar de volta: commit hash? diff resumido? lista de achados?
     Seja explícito — o worker não vai adivinhar. -->

## Paralelo-com / Depende-de
<!-- IDs de tasks irmãs rodando em paralelo (alerta de arquivos compartilhados)
     ou tasks que devem completar antes deste worker iniciar. -->
- Paralelo-com: (nenhum | task-X)
- Depende-de: (nenhum | task-Y completa)
```

---

## Exemplo Completo

```markdown
## Objetivo
Criar endpoint `POST /api/products` com validação Zod e persistência via Prisma.
A validação deve rodar antes de qualquer escrita no banco para garantir que
dados inválidos nunca cheguem ao storage.

## Skills a Carregar
- `skills/stack/prisma.md` — padrões de schema e transaction handling
- `skills/api-patterns.md` — estrutura de Route Handler e tratamento de erro
- `skills/security-best-practices.md` — seção "Zod validation on ALL external input"

## Escopo de Arquivos
**Pode ler/editar:**
- `app/api/products/route.ts` (criar se não existir)
- `lib/validations/product.ts` (criar se não existir)
- `prisma/schema.prisma` (apenas leitura — não alterar)
- `types/product.ts` (apenas leitura — usar os tipos existentes)

**Fora de escopo (não tocar):**
- Qualquer outro arquivo em `app/api/`
- Migrations Prisma — schema já está aprovado
- Testes E2E existentes

## Contexto Essencial
- Stack: Next.js App Router, TypeScript strict, Prisma 5, Bun
- Convenção de erro: `{ error: string, code: string }` com HTTP status correto
- Autenticação: já existe `lib/auth/session.ts` — importar `getSession()` e
  retornar 401 se sessão nula (não implementar auth do zero)
- O model `Product` no schema tem campos obrigatórios: `name`, `price`, `tenantId`
- `tenantId` deve vir da sessão, NUNCA do body da requisição

## Critério de Pronto
**Comando:** `bun test app/api/products/route.test.ts`
**Resultado esperado:** todos os testes passando, 0 failures

(Se o arquivo de teste não existir, criar antes de implementar — TDD obrigatório.)

## Formato de Output
Reportar:
1. Hash do commit com a implementação
2. Sumário dos testes: `N passed, 0 failed`
3. Se houver decisão de design não óbvia, listar em 1-2 bullets

## Paralelo-com / Depende-de
- Paralelo-com: task-frontend-product-form (arquivos distintos — sem conflito)
- Depende-de: task-schema-product completa (migration já deve estar aplicada)
```

---

## Seleção de Modelo

| Modelo | Usar quando |
|--------|-------------|
| `haiku` | Tarefas mecânicas: formatar output, gerar boilerplate simples, buscar em docs |
| `sonnet` | Implementação padrão: CRUD, componentes, refactoring, testes unitários |
| `opus` / `fable` | Alta complexidade: schema migrations com impacto cross-tenant, design de sistema distribuído, concorrência, decisões arquiteturais com trade-offs não-óbvios |

**Regra rápida:** quando o erro de julgamento do modelo pode custar horas de
rollback (migrations, design de contratos de API públicos, mudanças de RLS),
use opus/fable. Para todo o resto, sonnet é suficiente.
