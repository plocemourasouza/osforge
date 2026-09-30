# Resultados de eval

Todo número de eval citado no OSForge aponta para um arquivo daqui. Um resultado sem
**modelo**, **data**, **SHA do repo** e **k de N** não é um resultado: é uma lembrança.
Foi assim que "30/30" e "15/16" acabaram em arquivos sempre carregados sem que ninguém
soubesse de quando eram, com que modelo, nem quanto custaram (auditoria B-012).

## Nome do arquivo

```
docs/evals/<AAAA-MM-DD>-<modelo>-<suite>.md
docs/evals/2026-09-18-claude-sonnet-4-6-trigger.md
```

Suítes: `trigger` (a skill dispara quando deve e **só** quando deve), `routing`
(o orquestrador alcança agente/skill/tier), `skills` (triggering das skills core
pelo harness antigo).

## Como um arquivo nasce

Sempre pela flag `--report` do harness — nunca escrito à mão. O gerador
(`scripts/lib/eval_report.py`) carimba SHA, versão, modelo, HOME, comando exato,
tokens somados dos streams e a tabela de k de N.

```bash
# Roteamento do orquestrador (16 casos × 3 execuções)
./scripts/test-orchestrator-routing.sh --model claude-sonnet-4-6 --runs 3 \
    --home /tmp/osforge-home-limpo \
    --report docs/evals/$(date +%F)-claude-sonnet-4-6-routing.md

# Trigger com positivas e negativas (15 skills; comece pelo split 'eval')
./scripts/run-trigger-eval.sh --model claude-sonnet-4-6 --runs 3 --split eval \
    --report docs/evals/$(date +%F)-claude-sonnet-4-6-trigger.md

# Triggering das skills core (suíte antiga, à mão)
./scripts/test-skill-triggering.sh --model claude-sonnet-4-6 --runs 3 \
    --report docs/evals/$(date +%F)-claude-sonnet-4-6-skills.md
```

Todas as suítes aceitam `--dry`: lista os casos, valida os arquivos e **não chama
modelo nenhum**. É o que roda no CI; a rodada paga é sempre uma decisão humana.

## Como ler

- **PASS** é `k = N`: acertou em todas as execuções. Uma execução não distingue
  "a skill dispara" de "disparou uma vez".
- **FLAKY** é `0 < k < N`. Não é aprovado — é a lista que o experimento E1
  (estabilidade) consome para decidir o que vale medir.
- **NOT RUN** é um caso que a suíte parou antes de rodar (cota esgotada, L-01).
  Sozinho não reprova; um caso **crítico** em NOT RUN deixa a suíte
  **INCOMPLETE** — nem aprovada nem reprovada, porque não dá pra saber.
- Numa suíte de trigger, cada caso é uma consulta e traz o sinal: `+` deve disparar,
  `-` **não** deve. Uma description que dispara em tudo é pior que uma que não dispara:
  o custo aparece em toda sessão.

## Formato v2 dos casos de trigger (N-01/B-025)

Cada caso em `scripts/evals/trigger/*.json` (schema `osforge/trigger-eval/v2`) tem uma
`category`, e — quando aplicável — `critical` e `expect_route`:

```json
{"id": "n6", "should_trigger": false, "category": "negacao", "critical": true,
 "query": "Não precisa revisar, só faz o commit do que está staged."}
{"id": "n7", "should_trigger": false, "category": "vizinho", "expect_route": "receiving-code-review",
 "query": "O revisor pediu mudanças no meu PR; como eu respondo aos comentários?"}
```

| Categoria | `should_trigger` | Significado |
|---|---|---|
| `positivo` | `true` | A skill deve disparar |
| `vizinho` | `false` | Mesmo domínio ou objeto, mas outra skill é a certa — o caso difícil |
| `irrelevante` | `false` | Nada liga o pedido a esta skill |
| `negacao` | `false` | O pedido exclui explicitamente o que a skill faz — **sempre `critical: true`** |

`expect_route` é **informativo** (não é asserção nesta fase — D-N2), mas é validado: tem
de apontar para uma skill que existe em `skills/` (não precisa ser uma das 15 medidas
aqui). Um caso **crítico** que não seja PASS reprova a suíte mesmo com `--allow-flaky`
(ver "Como ler" acima). `./scripts/run-trigger-eval.sh --dry` valida tudo isso sempre —
inclusive as contagens mínimas por categoria (≥ 5 positivo, ≥ 2 vizinho, ≥ 1 negacao,
≥ 1 irrelevante por skill) — e é o que o CI roda.

O mesmo formato de "críticos primeiro" vale para `scripts/routing-cases.tsv`: a 6ª
coluna (`critico`) marca os casos de despacho obrigatório (`!agente`, D-N1) como
críticos — um deles falhando reprova mesmo com `--allow-flaky`.

## Antes de citar um número

Cite o arquivo, não o número solto: "12 de 16 demandas sem rota identificável
(`docs/evals/2026-08-30-…-routing.md`)". Quando o arquivo não existir ainda, escreva
que a medição está pendente. Prosa que afirma "medido" sem apontar para cá é exatamente
o que esta pasta existe para acabar.

## Custo

Cada caso custa `--runs` chamadas. A suíte de trigger inteira (170 casos × 3) são 510
chamadas; o split `eval` (73 × 3) são 219; uma skill só, ~30. O formato v2 (categoria e
casos críticos, N-01/B-025) acrescentou 20 casos negativos ao conjunto — 13 negações e
7 vizinhos novos — e moveu o split `eval` de 60 para 73 casos (as negações novas entram
nele: é o que queremos medir). `--dry` diz o custo antes.

## Pendentes de versionamento

Números que circulam em arquivo sempre carregado e ainda **não** têm um arquivo aqui.
Até terem, são narrativa, não medição (ADR-015 §4). Cada um está marcado como tal na
origem; sai desta lista quem for refeito com `--report`.

| Afirmação | Onde aparece | Como refazer |
|---|---|---|
| "12 de 16 demandas sem roteamento identificável" | `claude-code/CLAUDE.md` §route line | `test-orchestrator-routing.sh --model X --runs 3 --report …-routing.md` |
| "5 de 7 falhas eram skill declarada e nunca aberta" | `claude-code/CLAUDE.md` §route line | idem |
| "linha de rota em 14/16; skill carregada em ~metade" | `hooks/route-guard.py` (cabeçalho) | idem, com e sem o hook (`OSFORGE_ROUTEGUARD=off`) |
| "customer service flow / SQL injection respondidos sem a skill" | `claude-code/CLAUDE.md` §manifest | `run-trigger-eval.sh --model X --split eval --report …-trigger.md` |
