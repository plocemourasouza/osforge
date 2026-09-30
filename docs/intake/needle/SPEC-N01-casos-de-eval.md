# N-01 · Casos de eval com categoria, casos críticos e validação sem modelo

**Origem:** método das suítes de aceite do Needle (EV-N01 a EV-N06).
**Evidência local:** EV-O-N01 a EV-O-N07; rótulos propostos em [`rotulos-trigger.tsv`](rotulos-trigger.tsv).
**Esforço:** M (código ~1 dia; rótulos e casos novos já estão propostos aqui). **Custo de
verificação:** zero chamadas. **Efeito no E1:** +39 chamadas (ver "Custo").

## Problema

1. **Um FLAKY não diz onde a skill quebra.** Os casos de trigger só dizem "deve disparar:
   sim/não" (EV-O-N01). Rotulados à mão, os 75 negativos atuais são **27 vizinhos** (pedidos
   do mesmo domínio que pertencem a outra skill), **46 irrelevantes** e **2 negações**
   ("não quero X"). 13 das 15 skills não têm nenhuma negação e 6 têm menos de dois vizinhos.
   Depois de pagar o E1, o relatório diria "FLAKY 2/3" sem dizer se a skill falha no caso
   difícil (vizinho), no fácil (irrelevante) ou no que desobedece o usuário (negação).
2. **Nenhum erro pesa mais que outro.** Disparar uma skill que o usuário acabou de recusar conta
   o mesmo que não disparar num pedido vago — e `--allow-flaky` deixa os dois passarem
   (EV-O-N04).
3. **Caso quebrado passa no CI.** Na suíte em TSV, um caso cuja skill não existe aparece como
   "ÓRFÃO" no `--dry`, que sai com 0 (EV-O-N02, reproduzido); só a execução paga descobre,
   gastando chamadas num FAIL garantido. O `--dry` de roteamento não confere nada (EV-O-N03).

## Desenho

### 1. Esquema `osforge/trigger-eval/v2`

Cada caso ganha `category` e, quando aplicável, `critical` e `expect_route`:

```json
{"id": "n6", "should_trigger": false, "category": "negacao", "critical": true,
 "query": "Não precisa revisar, só faz o commit do que está staged."}
{"id": "n7", "should_trigger": false, "category": "vizinho", "expect_route": "receiving-code-review",
 "query": "O revisor pediu mudanças no meu PR; como eu respondo aos comentários?"}
```

| Categoria | `should_trigger` | Significado |
|---|---|---|
| `positivo` | `true` | A skill deve disparar |
| `vizinho` | `false` | Mesmo domínio ou mesmo objeto, mas outra skill é a certa — o caso difícil |
| `irrelevante` | `false` | Nada liga o pedido a esta skill (pode pertencer a outra, ou a nenhuma) |
| `negacao` | `false` | O pedido exclui explicitamente o que a skill faz |

`expect_route` (opcional) diz qual skill deveria atender o pedido; nesta fase é **informativo**
— serve à leitura do relatório e a um futuro eval de roteamento de negativos —, mas é validado.

### 2. Regras de validação (no `validate()` de `run-trigger-eval.sh`, que já roda no `--dry` e no CI — EV-O-N06)

- `category` obrigatória e coerente com `should_trigger`;
- por skill: ≥ 5 `positivo`, ≥ 2 `vizinho`, ≥ 1 `negacao`, ≥ 1 `irrelevante`;
- **toda `negacao` é `critical: true`** (desobedecer uma exclusão explícita nunca é um erro menor);
- `critical` só booleano; `expect_route`, quando presente, aponta para uma skill existente;
- as regras atuais continuam (rel existente, ids únicos, 5+5, split, consulta repetida).

### 3. Migração dos 150 casos

Script de uso único que lê [`rotulos-trigger.tsv`](rotulos-trigger.tsv) e grava `category`,
`critical` e `expect_route` em cada arquivo, e acrescenta os **20 casos novos** propostos ali
(ids `n6`–`n8`: 13 negações e 7 vizinhos), passando o `$schema` para v2. Split: negações novas
entram em `eval` (é o que queremos medir), vizinhos novos em `tune`. Resultado: 170 casos, 20
críticos (15 negações + 5 positivos em que agir errado custa caro: pedido vago em
`requirements-clarify`, "posso considerar resolvido?" em `verification-before-completion`,
"já mexi em três lugares e piorou" em `systematic-debugging`).

**Os rótulos e os casos novos são uma proposta** feita na análise; a fronteira entre vizinho
e irrelevante é julgamento. A implementação começa por uma revisão deles (D-N3).

### 4. As outras duas suítes

- `test-skill-triggering.sh` (TSV): caso órfão faz o `--dry` sair com **1** e a execução real
  se recusar a começar.
- `test-orchestrator-routing.sh`: o `--dry` confere que cada agente esperado existe em
  `agents/` (cada alternativa de `a|b`, com o `!` removido), que a skill esperada existe e que
  o tier está no conjunto aceito; qualquer falha → exit 1. Nova 6ª coluna opcional `critico`.

### 5. Veredito e relatório

- Caso **crítico** que não seja PASS (FLAKY, FAIL, TIMEOUT) reprova a suíte **mesmo com
  `--allow-flaky`**. Crítico em `NOT RUN` (parada por cota, L-01) → suíte "incompleta", nunca
  aprovada.
- `eval_report.py` ganha a coluna Categoria e uma linha de resumo por categoria
  ("vizinho 31/34 PASS · negação 15/15 · irrelevante 46/46 · positivo 70/75"), com os
  críticos reprovados listados antes de tudo (EV-O-N05).

## Arquivos

`scripts/run-trigger-eval.sh` (validação v2) · `scripts/evals/trigger/*.json` (migração) ·
`scripts/migrate-trigger-v2.py` **(NOVO, uso único)** · `scripts/test-skill-triggering.sh` ·
`scripts/test-orchestrator-routing.sh` · `scripts/routing-cases.tsv` (6ª coluna) ·
`scripts/lib/harness-assertions.sh` (veredito da suíte) · `scripts/lib/eval_report.py` ·
`tests/test-eval-cases.sh` **(NOVO)** · `docs/evals/README.md` (formato v2).

## Testes (offline, todos vermelhos sem a mudança)

`tests/test-eval-cases.sh`, contra cópias temporárias dos arquivos de caso:

1. caso sem `category` → validação reprova; `category: "negacao"` com `should_trigger: true`
   → reprova.
2. `negacao` sem `critical: true` → reprova.
3. skill com 1 vizinho, ou sem negação, ou sem irrelevante → reprova, dizendo qual falta.
4. `expect_route` para skill inexistente → reprova.
5. os casos do repositório, depois da migração → aprovam (e o CI continua verde).
6. TSV de trigger com skill inexistente → `--dry` sai 1.
7. roteamento com agente inexistente, com `!agente` inexistente e com uma alternativa ruim em
   `a|b` → `--dry` sai 1 nos três; caso válido → sai 0.
8. veredito da suíte com resultados sintéticos: crítico FLAKY + `--allow-flaky` → reprova;
   não crítico FLAKY + `--allow-flaky` → aprova; crítico `NOT RUN` → "incompleta".
9. `eval_report.py` com resultados sintéticos → linha por categoria com as contagens certas e
   críticos reprovados no topo.

## Aceite

Os nove casos verdes; as suítes atuais verdes; `./scripts/run-trigger-eval.sh --dry` mostra
170 casos, 20 críticos, nenhum problema; CI verde.

## Custo

Nenhuma chamada para implementar. O split `eval` passa de 60 para 73 casos: o trigger do E1
sobe de 180 para **219 chamadas** (3 execuções), e o E1 inteiro de 234 para 273 (EV-O-N07).
É o preço de medir negação, que hoje não é medida.

## Decisões em aberto

- **D-N1** — quais casos de roteamento são críticos. Sugestão: os de despacho obrigatório (`!`).
- **D-N2** — tornar `expect_route` uma asserção num eval futuro de "para onde foi o negativo".
  Recomendado: não agora.
- **D-N3** — revisão humana dos rótulos e dos 20 casos novos antes da migração.
