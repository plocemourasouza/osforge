# P-03 · `repo-audit`, auditoria de código do repositório inteiro (sob demanda)

**Origem:** `skills/ponytail-audit/SKILL.md` (EV-P09), adaptado ao stack do OSForge.
**Evidência local:** EV-O-P05.
**Esforço:** P–M (skill nova + casos da r3).
**Entra só se:** na r3, B (a skill) superar A (sem skill) **e** C (uma linha de instrução) além do ruído.
Se uma linha bastar, entra a linha, não a skill.

## Problema

O OSForge revisa mudanças (`code-review`, `adversarial-review`, `edge-case-hunter`) e audita UI
(`ui-audit`, `redesign-audit`), mas não tem como auditar o código de um repositório inteiro
(EV-O-P05). É o pedido típico ao herdar um projeto, antes de uma release ou depois de meses
de *vibe coding*: "o que quebra primeiro aqui?".

## Mudança

Skill nova `skills/quality/repo-audit/SKILL.md`, **fora do core**: instalada por projeto com
`install-skill`, não entra no roteamento global. Isso evita piorar o trigger, que já é o ponto
fraco medido (EV-O-P09).

1. **Mapa primeiro.**
   - Ler README, `package.json`, `next.config.*` e deploy (`vercel.json`, Docker), `prisma/schema.prisma`,
     `supabase/migrations` e políticas RLS.
   - Ler os pontos de entrada: rotas do App Router, Route Handlers, Server Actions, middleware, jobs e cron.
   - Ler os testes.
   - Declarar a carga assumida.
2. **Seguir os fluxos que custam caro**, de ponta a ponta: autenticação e autorização, dinheiro,
   gravação de dados, segredos, jobs concorrentes. Num repositório grande, ir fundo onde o erro
   custa mais e dizer o que não foi lido.
3. **Procurar, nesta ordem:** bug, risco (segurança, perda de dado), escala sob a carga
   declarada, lógica arriscada sem teste, lentidão grande, código que não devia existir. Mais o
   checklist do stack:
   - service role do Supabase em código de cliente;
   - tabela sem RLS;
   - Server Action sem checagem de sessão;
   - dinheiro em `float`;
   - decremento de saldo ou estoque fora de `$transaction`;
   - `findMany` sem limite;
   - N+1 em Server Component.
4. **Prova:** todo achado tem caso concreto e arquivo:linha. Antes de chamar algo de não usado,
   procurar na árvore inteira (inclusive testes, config e referências por string).
5. **Saída:**
   - O que o repositório faz e a carga assumida.
   - Achados em Must fix / Should fix / Nice to have, numerados, **no máximo 20** (dizendo quantos
     ficaram de fora), cada um com o que é, problema, correção e "se não corrigir".
   - `Veredito:` o que corrigir primeiro.
   - `Não verificado:` o que não foi lido ou não pôde rodar.
   - Não altera código.

`inspired_by` (Ponytail, MIT) e `THIRD_PARTY_NOTICES`. Índices regenerados
(`INDICE-SKILLS`, manifesto); `check-counts` passa a contar 178 skills.

## Medição

O alvo `repo-audit` da r3 tem três mini-repositórios, de 5 a 7 arquivos, inline no prompt.
Os braços são: A sem skill · B a skill · C uma linha ("liste os problemas mais graves primeiro,
cada um com um caso concreto e arquivo:linha").

| Tarefa | Semeado | Crítico |
|---|---|---|
| ra1 Next.js + Supabase | service role no cliente; tabela sem RLS; um TODO inofensivo | achou os dois de segurança; nada bloqueante fabricado |
| ra2 Prisma + dinheiro | saldo decrementado fora de transação; `float` em valor; `findMany` sem limite | achou a corrida e o `float`; ranqueou certo |
| ra3 repositório saudável | nada grave | nenhum achado bloqueante fabricado |

## Aceite

1. r3: B − A **e** B − C além do ruído; `manufactured_high` de B não maior que o de A.
2. Se só B − A passar, mas B ≈ C: entra a instrução de uma linha, como nota no `code-review`, e
   não a skill.
3. `install-skill repo-audit` instala num projeto temporário (`tests/test-installers.sh` ganha o caso).
