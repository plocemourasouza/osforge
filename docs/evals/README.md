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
- Numa suíte de trigger, cada caso é uma consulta e traz o sinal: `+` deve disparar,
  `-` **não** deve. Uma description que dispara em tudo é pior que uma que não dispara:
  o custo aparece em toda sessão.

## Antes de citar um número

Cite o arquivo, não o número solto: "12 de 16 demandas sem rota identificável
(`docs/evals/2026-08-30-…-routing.md`)". Quando o arquivo não existir ainda, escreva
que a medição está pendente. Prosa que afirma "medido" sem apontar para cá é exatamente
o que esta pasta existe para acabar.

## Custo

Cada caso custa `--runs` chamadas. A suíte de trigger inteira (150 casos × 3) são 450
chamadas; o split `eval` (60 × 3) são 180; uma skill só, 30. `--dry` diz o custo antes.

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
