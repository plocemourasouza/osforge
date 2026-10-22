# P-01 · Escada da solução em `coding-guidelines`

**Origem:** `skills/ponytail/SKILL.md` (EV-P01 a EV-P04), reescrito no padrão do OSForge.
**Evidência local:** EV-O-P01, EV-O-P02, EV-O-P06.
**Esforço:** P (texto) + a parte que lhe cabe na rodada r3 ([`MEDICAO-r3.md`](MEDICAO-r3.md)).
**Entra só se:** na r3, o braço C (atual + escada) superar o B (atual) além do ruído, sem
piorar nenhum critério crítico.

## Problema

`coding-guidelines` diz *quanto* código escrever ("minimum code", "no speculative features"),
mas não diz *de onde tirar* a solução. Nem ela nem `clean-code` falam de biblioteca padrão,
recurso nativo da plataforma ou dependência nova (EV-O-P01). Num stack Next.js + TypeScript +
Prisma + Supabase, os excessos mais comuns são exatamente esses:

- instalar uma biblioteca de data quando `<input type="date">` e `Intl` resolvem;
- puxar `uuid` com `crypto.randomUUID()` disponível;
- escrever um formatador de moeda ao lado do que já existe em `lib/`;
- validar à mão com Zod já instalado.

E a regra "no error handling for impossible scenarios" (EV-O-P02) não tem contrapeso escrito.
Nada diz o que **nunca** se corta quando se simplifica.

## Mudança

Em `skills/coding-guidelines/SKILL.md`, §2 "Simplicity First" ganha duas subseções.
§5 "Read Before You Write" ganha uma linha.

**Escada (antes de escrever, pare no primeiro degrau que resolve por inteiro):**

1. Precisa existir? O que ninguém pediu fica fora, e é nomeado numa linha.
2. Já existe neste repositório (helper, componente, serviço, padrão)? Use como o código vizinho usa.
3. A biblioteca padrão ou a plataforma resolve (`Intl`, `crypto.randomUUID()`, `URLSearchParams`,
   `structuredClone`, `<input type="date">`, `<dialog>`)? Use — salvo se o projeto tiver o seu.
   O componente da casa ganha do nativo.
4. Uma dependência **já instalada** resolve (Zod, o cliente do Supabase, `upsert`/`$transaction`
   do Prisma)? Use. **Nunca** adicione dependência por poucas linhas.
5. Só então: o mínimo que funciona.

**Nunca cortar ao simplificar:** validação na fronteira de confiança (entrada de usuário,
webhook, Server Action), tratamento de erro que evita perda de dados, checagens de segurança
e autorização, acessibilidade, e qualquer coisa que o usuário pediu.

**Atalho declarado:** um atalho com limite conhecido leva um comentário de uma linha:
`shortcut: <o limite>, <quando trocar>`. O `code-review` (P-02) trata esse comentário como
decisão, não como achado.

**§5 + uma linha:** em correção de bug, procure **todos os chamadores** da função tocada e
corrija a causa uma vez, no código compartilhado.

Em `claude-code/SKILLS.md:19-22`, o resumo da lei sempre carregada ganha uma oração
(~40 tokens):

> … · escada: repositório → stdlib/plataforma → dependência instalada, antes de escrever;
> nunca dependência nova por poucas linhas; nunca cortar validação de fronteira, perda de
> dados, segurança ou acessibilidade.

Frontmatter: `version: "1.2.0"`, `inspired_by` apontando o Ponytail (MIT) e
`THIRD_PARTY_NOTICES` atualizado.

## O que **não** entra, e por quê

| Do Ponytail | Motivo |
|---|---|
| Piso de "um teste pequeno para lógica não trivial" | O OSForge já é mais exigente: a lei do TDD (`SKILLS.md`) |
| "Termine toda resposta com o que pulou e o risco" | Já existe onde importa (`verification-before-completion`) e entra no `code-review` por P-02; não vira regra de toda resposta |
| Persona ("você é um dev sênior preguiçoso") e níveis lite/full/ultra | Tom não é mecanismo; os níveis já existem em `behavioral-modes` |

## Medição

O alvo `coding-guidelines` da r3 tem seis tarefas no stack do OSForge. Cada uma testa um degrau
ou o contrapeso, com critérios críticos (detalhe em [`MEDICAO-r3.md`](MEDICAO-r3.md)):

| Tarefa | Testa | Crítico |
|---|---|---|
| cg1 seletor de data | degrau 3, com componente da casa | reusa o `Input` da casa; nenhuma dependência nova |
| cg2 id público do pedido | degrau 3 | `crypto.randomUUID()` ou equivalente; nenhuma dependência nova |
| cg3 preço em BRL | degrau 2 vence o 3 | usa o `formatCurrency` que já existe |
| cg4 validar webhook | degrau 4 + nunca cortar | Zod já instalado; assinatura e validação mantidas |
| cg5 arredondamento errado | chamadores | corrige no helper compartilhado; trata o contorno local de um chamador |
| cg6 simplificar botão | nunca cortar | acessibilidade preservada; nenhum comportamento perdido |

## Aceite

1. r3: C − B maior que o ruído (maior spread entre execuções dos dois braços) no alvo
   `coding-guidelines`, e nenhum critério crítico pior em C.
2. Testes atuais verdes; `check-counts` e `_generate_manifest.py --check` verdes.
3. Se a r3 der C ≈ B: **não entra** e fica registrado como recusado, com o relatório.
