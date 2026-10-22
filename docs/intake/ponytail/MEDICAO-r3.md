# Rodada r3 do eval de resultado — medir P-01, P-02 e P-03 antes de adotar

**Instrumento:** `scripts/evals/outcome/driver.py` + `scripts/lib/judge.py` (ADR-016), o mesmo
das rodadas r1 e r2. Três braços que diferem **só** no `--append-system-prompt`, executor isolado
(sem CLAUDE.md, sem settings, sem MCP, sem ferramentas). Cada resposta é avaliada às cegas pelo
juiz, contra a rubrica e a verdade da tarefa (EV-O-P10).

## O que precisa mudar no instrumento (offline, sem chamada)

- `driver.py` e `build_variants.py` passam a aceitar `--round r3` (hoje só `r1|r2`, EV-O-P10).
- `scripts/evals/outcome/tasks_r3.py` define a tabela de tarefas.
- Em `r3/` ficam `tasks/<alvo>/<tarefa>.md` e `.truth.md`, `rubrics/`, `schemas/` e `variants/`,
  no mesmo formato da r2.
- Os textos dos braços C de P-01 e P-02 **são o entregável**: escrever primeiro como variante.
  A skill só é tocada se a variante ganhar.

## Alvos e braços

| Alvo | A | B | C | Pergunta |
|---|---|---|---|---|
| `coding-guidelines` | nota neutra | SKILL.md atual | atual + P-01 | A escada melhora? (e, de quebra, a **primeira medição** da skill atual: B − A) |
| `code-review` | nota neutra | SKILL.md atual | atual + P-02 | Ler o código conectado melhora? (também a primeira medição da skill) |
| `repo-audit` | nota neutra | skill nova (P-03) | instrução de uma linha | A skill vale mais que uma linha? |
| `ponytail-ref` *(opcional, D-P1)* | nota neutra | SKILL.md do Ponytail, literal | o mesmo C de `coding-guidelines` | A adaptação perdeu o que fazia o original funcionar? |
| `mapa-repo` *(item 18 da cobertura)* | nota neutra | `coding-guidelines` + P-01 | B + mapa de exports do repositório, no formato do `ponytail-map.js` (EV-P30) | O mapa no contexto faz reusar o que **não** está no prompt? |

O `mapa-repo` usa variantes cg1m, cg3m e cg5m das tarefas cg1, cg3 e cg5, em que o arquivo do helper existente (`components/ui/input.tsx`, `lib/format.ts`, `lib/money.ts`) **não** vem no prompt. Sem o mapa, o modelo não tem como saber que ele existe; com o mapa, só sabe o nome e o caminho. Se C não superar B além do ruído, o mapa não vira injeção de sessão.

O `ponytail-ref` reusa as tarefas cg1–cg6. O texto literal do Ponytail entra só como variante
de eval, com o aviso MIT no cabeçalho do arquivo.

## Tarefas

Todas no stack do OSForge (Next.js App Router, TypeScript, Prisma, Supabase), com o código
necessário inline no prompt e a verdade em `.truth.md` para o juiz.

| Tarefa | Pedido | Semeado / esperado | Critérios críticos |
|---|---|---|---|
| cg1 | Seletor de data no agendamento | Repositório tem `components/ui/input.tsx`; nenhuma lib de data | `reuses_house_input`, `no_new_dependency` |
| cg2 | Id público curto para o pedido | Node 20; sem `uuid`/`nanoid` | `uses_platform_id`, `no_new_dependency` |
| cg3 | Preço em BRL na listagem | `lib/format.ts` já tem `formatCurrency` | `reuses_existing_helper` |
| cg4 | Validar o webhook de pagamento | Zod instalado e usado em outra rota; assinatura HMAC no código | `keeps_signature_check`, `validates_at_boundary` |
| cg5 | Total do carrinho arredonda errado | Bug em `lib/money.ts`, 3 chamadores, um com contorno local | `fix_in_shared_helper`, `handles_local_workaround` |
| cg6 | Simplificar o componente de botão | `div` clicável com `role`/teclado/aria e props sem uso | `keeps_accessibility`, `no_behavior_lost` |
| cr1 | Revisar: campo renomeado | Chamador **fora do diff** quebra | `found_outside_diff`, `no_manufactured_high` |
| cr2 | Revisar: reserva de estoque | Ler-depois-gravar sem `$transaction`; README: várias instâncias | `found_race_under_load` |
| cr3 | Revisar: atalho declarado + bug | `shortcut:` dentro da carga; bug real de fuso horário | `found_real_bug`, `shortcut_not_blocking` |
| cr4 | Revisar: mudança limpa | Nada | `no_manufactured_high`, `approves` |
| ra1 | Auditar mini-repo Next.js + Supabase | Service role no cliente; tabela sem RLS; TODO inofensivo | `found_service_role`, `found_rls`, `no_manufactured_high` |
| ra2 | Auditar mini-repo Prisma + dinheiro | Saldo fora de transação; `float`; `findMany` sem limite | `found_race`, `found_float_money`, `ranked_right` |
| ra3 | Auditar mini-repo saudável | Nada grave | `no_manufactured_high` |

As contagens que o juiz já devolve na r2 (`seeded_found`, `manufactured_findings`,
`manufactured_high`) valem para cr\* e ra\*.

## Custo e janela

| Escopo | Chamadas (executor + juiz) | Dólar-equivalente da assinatura* |
|---|---|---|
| Piloto (1 tarefa, 1 braço) | 2 | ~0,2 |
| r3 sem `ponytail-ref` (13 tarefas × 3 braços × 3 execuções) | 117 + 117 = 234 | ~25 |
| + `mapa-repo` (3 × 3 × 3) | +54 | ~6 |
| + `ponytail-ref` (6 × 3 × 3) | +108 | ~11 |
| **Tudo** | **396** | **~42** |

\* Pela taxa da r2: 38,33 por 360 chamadas (EV-O-P11). A r2 chegou a 24% de pico da janela de
5 h. Com até 396 chamadas e concorrência 4, espera-se um pico na mesma faixa (~25–30%), longe da
parada automática em 80% (B-026).

## Regra de decisão

| Alvo | Entra se | Senão |
|---|---|---|
| `coding-guidelines` | C − B > ruído e nenhum crítico pior em C | P-01 recusado, registrado |
| `code-review` | C − B > ruído e `manufactured_high`(C) ≤ `manufactured_high`(B) | P-02 recusado, registrado |
| `repo-audit` | B − A > ruído **e** B − C > ruído | Se só B − A: entra a linha (C), não a skill |
| `mapa-repo` | C − B > ruído nos critérios de reuso, sem crítico pior | O mapa não entra |
| `ponytail-ref` | — (informativo) | Se B(Ponytail) > C(nossa) além do ruído: refazer a adaptação antes de adotar |

"Ruído" = o maior spread entre execuções dos dois braços comparados, como na r2.

## Comandos (depois da autorização)

```bash
python3 scripts/evals/outcome/build_variants.py --round r3
python3 scripts/evals/outcome/driver.py --dry   --round r3                 # valida, sem chamada
python3 scripts/evals/outcome/driver.py --pilot --round r3 --model claude-opus-5-5
python3 scripts/evals/outcome/driver.py --run   --round r3 --model claude-opus-5-5 --runs 3 --concurrency 4 --budget 40
python3 scripts/evals/outcome/driver.py --report docs/evals/$(date +%F)-claude-opus-5-5-skill-outcome-r3.md \
        --round r3 --model claude-opus-5-5 --judge-model claude-fable-5-1
```

## Limite do instrumento

O eval é de **um turno, sem ferramentas**: o código vem no prompt. Ele mede se o texto da skill
muda a qualidade da resposta, não se o agente explora melhor um repositório real (procurar
chamadores com grep, abrir o arquivo certo). As alegações agênticas do Ponytail ficam fora
do alcance. O harness agêntico dele existe (`benchmarks/agentic/`), mas custaria ~585 sessões
(~$97 a preço de lista) e não tem nenhuma tarefa no stack do OSForge.
