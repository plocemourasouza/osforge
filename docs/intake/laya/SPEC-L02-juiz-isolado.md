# L-02 · Juiz isolado (chamada de inferência pura sobre a cota da assinatura)

**Origem:** Laya `llm/agent_backend.py` (EV-L01 a EV-L10).
**Evidência local:** EV-O01, EV-C05 a EV-C11.
**Esforço:** P–M. **Custo de verificação:** offline para o contrato; **1 a 3 chamadas** no
experimento E-J0 (pede autorização).

## Problema

O programa de evals do OSForge mede **disparo** — se a skill ou o agente certo foi acionado —
com veredito determinístico sobre o stream (`stream_assert.py`). Não há como medir
**qualidade**: se a revisão do `adversarial-review` achou o problema certo, se um plano está
proporcional (E3), se o revisor ficou leniente depois do B-004 (E4). Isso pede um juiz: uma
chamada de modelo que recebe um artefato e uma rubrica e devolve uma nota estruturada.

Chamar o `claude` para isso do jeito que o harness chama hoje (EV-O01) seria errado por três
motivos: carregaria o `~/.claude` do usuário — `CLAUDE.md` do orquestrador com a linha de rota
obrigatória, hooks como `route-guard` e `gateguard`, MCPs —, teria ferramentas disponíveis, e
devolveria texto livre para ser interpretado.

## O que o Laya ensina, e o que precisa ser diferente aqui

O Laya chama `claude -p` one-shot, com `--output-format stream-json --verbose`,
`--permission-mode default`, todas as ferramentas embutidas negadas, cwd vazio e efêmero,
`--append-system-prompt` e `--json-schema`, lendo `structured_output` do evento `result`
(EV-L05, EV-L06, EV-L08), e prefixa uma diretiva que impede o modelo de fazer perguntas ou
oferecer ações (EV-L03). Concorrência limitada por semáforo (EV-L04).

O que o Laya **não** resolve e o OSForge precisa: isolar a chamada da configuração global do
usuário. O caminho óbvio, `--bare`, é **proibido** aqui: no Claude Code 2.1.278 ele faz a
autenticação usar exclusivamente `ANTHROPIC_API_KEY` ou `apiKeyHelper`, nunca OAuth nem
keychain (EV-C05) — ou seja, transformaria a chamada em cobrança de API.

## Receita

```
cwd  = mktemp -d            (vazio; apagado ao final)
env  += CLAUDE_CODE_DISABLE_CLAUDE_MDS=1  CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
claude -p "<artefato + instrução>" \
  --model <id>                       # obrigatório, como no B-010
  --output-format stream-json --verbose
  --tools ""                         # nenhuma ferramenta embutida (EV-C07)
  --setting-sources ""               # nem user, nem project, nem local: sem hooks (EV-C06)
  --strict-mcp-config                # nenhum MCP (EV-C08)
  --permission-mode default
  --json-schema '<schema>'           # (EV-C10)
  --append-system-prompt "<diretiva não interativa + rubrica>"
  < /dev/null
```

Nunca: `--bare`, `--dangerously-skip-permissions`, `--mcp-config`, `--max-turns` alto.

## Contrato — `scripts/lib/judge.py` **(NOVO)**

```
judge.py --model ID --schema FILE --rubric FILE --input FILE [--timeout 120] [--dry]
```

Saída: **uma** linha JSON no stdout:

```json
{"ok": true, "verdict": {...}, "usage": {"input": 0, "output": 0, "cache_read": 0, "cache_create": 0},
 "rate_limit": {"status": "allowed", "resets_at": 0}, "isolation": {"tools": [], "mcp_servers": []},
 "model": "…", "argv_sha256": "…"}
```

| Exit | Significado |
|---|---|
| 0 | veredito válido |
| 2 | `structured_output` ausente ou fora do schema |
| 3 | erro do CLI (`is_error`), timeout ou isolamento violado |
| 75 | cota (mesma regra de `run-status == quota` de L-01) |

Regras:

1. **Isolamento é verificado, não presumido.** Ler o evento `system/init` (EV-C11): `tools` e
   `mcp_servers` têm de estar vazios; senão exit 3 com o que vazou. É o equivalente, para o
   juiz, do veredito por bloco do B-010.
2. **Revalidar o schema localmente.** O Claude Code força o schema, mas o OSForge não confia:
   validador mínimo em Python puro (`type`, `required`, `enum`, `properties`, `items`,
   `minimum`/`maximum`) — sem dependência nova. O Laya usa `jsonschema` se existir e cai para
   "chaves obrigatórias" (EV-L10); aqui o subconjunto é sempre o mesmo, para o resultado não
   depender da máquina.
3. **Sem retry.** Schema nativo não precisa; erro não é repetido para não gastar cota.
4. **Sequencial por padrão.** `OSFORGE_JUDGE_CONCURRENCY` (padrão 1) para quem rodar em lote.
5. **Custo registrado.** `usage` somado como no `eval_report.py`; `total_cost_usd`, se vier,
   é gravado como "equivalente de API" — sob assinatura não é cobrança.
6. **A diretiva não interativa** é escrita com palavras próprias (ver licença na análise).
7. `--dry` imprime `argv` e `env` efetivos e sai 0 **sem** chamar o modelo.

## Experimento E-J0 (pede autorização: 1 a 3 chamadas curtas)

Com o modelo mais barato disponível; schema `{"answer": "yes"|"no"}` para os itens 1, 2 e 4 e
`{"answer": string}` para a sonda do item 3:

1. `ANTHROPIC_API_KEY` ausente do ambiente → a chamada completa (prova de que usou a
   assinatura, não API).
2. `system/init` com `tools: []` e `mcp_servers: []`.
3. Sonda de contaminação: pergunta cuja resposta só existe no `CLAUDE.md` do usuário (por
   exemplo, "qual linha você deve escrever antes de responder?") → o juiz **não** sabe.
4. `structured_output` presente e válido; registrar se veio `rate_limit_event` (alimenta L-01).

Se o item 2 ou 3 falhar, trocar `--setting-sources ""` por `--settings <arquivo vazio>` e
repetir; se ainda falhar, **não** adotar o juiz e registrar o motivo aqui.

## Testes (offline)

`tests/test-judge.sh` **(NOVO)**, com `claude` falso no `PATH` que grava o `argv`, o `env` e o
`cwd` recebidos e devolve um stream escolhido pelo teste:

1. `--dry` e execução normal: `argv` contém `--tools ""`, `--setting-sources ""`,
   `--strict-mcp-config`, `--json-schema`, `--model`; **não** contém `--bare` nem
   `--dangerously-skip-permissions`; `env` tem as duas variáveis; `cwd` é um diretório vazio
   que não existe mais depois.
2. stream com `init.tools` não vazio → exit 3, "isolamento violado: tools".
3. `structured_output` válido → exit 0; faltando campo obrigatório, `enum` inválido, tipo
   errado → exit 2.
4. `result.is_error` com `rate_limit_event` rejeitado → exit 75.
5. timeout do CLI → exit 3 e o diretório temporário removido.
6. validador: tabela de casos de schema (≥ 20) contra resultados esperados.

## Aceite

Testes verdes; E-J0 cumprido e o resultado registrado em `docs/evals/`; o primeiro consumidor
(E4, leniência do revisor) definido com rubrica e schema versionados em `scripts/evals/judge/`.

## Riscos

| Risco | Mitigação |
|---|---|
| `--setting-sources` e as duas variáveis não são documentados | E-J0 prova o efeito; o teste de isolamento roda em toda chamada real |
| O juiz também é um modelo e pode errar | Rubricas curtas, schema fechado, e nenhuma decisão por uma única nota: o consumidor usa k de N como no B-010 |
| Consumir a janela | Sequencial, sem retry, parada por cota de L-01 |
