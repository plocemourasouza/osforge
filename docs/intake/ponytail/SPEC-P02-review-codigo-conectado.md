# P-02 · `code-review` que lê o código conectado

**Origem:** `skills/ponytail-review/SKILL.md` (EV-P06 a EV-P08).
**Evidência local:** EV-O-P03, EV-O-P04.
**Esforço:** P (texto) + a parte que lhe cabe na rodada r3.
**Entra só se:** na r3, C (atual + P-02) superar B (atual) além do ruído, sem mais achados fabricados.

## Problema

O escopo do `code-review` é "o diff inteiro" (EV-O-P03): todo arquivo modificado, nenhum
pulado. Isso deixa de fora a classe de bug que mais escapa de review: a mudança de assinatura,
retorno ou comportamento que quebra um chamador **que não está no diff**. O veredito também não
traz duas coisas (EV-O-P04):

- a premissa de carga sob a qual a escalabilidade foi julgada;
- a consequência de não corrigir, que é o que ajuda a priorizar.

## Mudança

Em `skills/quality/code-review/SKILL.md`:

**§1 Identify Scope** ganha um item: quando uma função muda assinatura, retorno ou
comportamento, procurar **todos os chamadores no repositório**, inclusive em arquivos
fora do diff, e revisá-los. O "Done when" passa a ser: "cobre o diff e o código que ele
alcança".

**§1 também:** declarar a carga esperada, tirada do README, da config de deploy ou do
`project-context.md` (um usuário, um time, muitos processos). Achados de escala são julgados
contra essa carga, e ela é dita no relatório.

**§3 Deep Analysis** ganha a regra de prova: todo achado precisa de um caso concreto ("esta
entrada ou situação leva a este resultado errado"). Sem caso, não é achado. Um comentário
`shortcut: <limite>, <quando trocar>` (P-01) é decisão, não achado, salvo se a carga declarada
já ultrapassa o limite.

**§4 Verdict:** cada item de *Issues* ganha uma linha `Se não corrigir:` (uma frase, a
consequência para o usuário ou para o dado). O cabeçalho ganha `**Carga assumida:**`, e o fim
ganha `Não verificado:` (uma linha: o que importava e não pôde ser conferido), que hoje não existe.

Frontmatter com `inspired_by` (Ponytail, MIT). `agents/code-reviewer.md` já aponta para o
gate da `adversarial-review` e não muda.

## O que **não** entra

| Do Ponytail | Motivo |
|---|---|
| A ordem fixa correto → seguro → carga → testado → rápido → enxuto | O checklist estruturado do OSForge já cobre essas classes; reordenar não tem evidência |
| "Inglês muito simples, explique cada termo" | O OSForge responde em pt-BR e no tom do usuário; não é mecanismo |
| Grupo "Lean" com linhas a cortar | Coberto por `clean-code` ("Reviewing against this skill") |

## Medição

O alvo `code-review` da r3 tem quatro tarefas: Next.js route handler, Server Action, Prisma e
Supabase, com diff e arquivos conectados no próprio prompt.

| Tarefa | Semeado | Crítico |
|---|---|---|
| cr1 campo renomeado | um chamador **fora do diff** passa a quebrar | achou o chamador fora do diff |
| cr2 reserva de estoque | ler-depois-gravar sem transação; o README diz que roda em várias instâncias | achou a corrida, sob a carga declarada |
| cr3 atalho declarado | um `shortcut:` dentro da carga + um bug real | achou o bug; não tratou o atalho como bloqueante |
| cr4 mudança limpa | nada | nenhum achado bloqueante fabricado; aprova |

## Aceite

1. r3: C − B além do ruído no alvo `code-review`, `manufactured_high` de C não maior que o de B.
2. Testes atuais verdes; manifesto e contagens verdes.
3. Neutro → não entra, registrado.
