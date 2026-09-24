# L-03 · Auditoria por chamada, com custo derivado e retenção

**Origem:** Laya `audit_log` + `pipeline/budget.py` (EV-L15 a EV-L19).
**Evidência local:** EV-O07, EV-O08, EV-M01, EV-M02.
**Esforço:** M. **Custo de verificação:** zero chamadas.

## Problema

O B-022 grava tokens por **projeto + sessão + modelo** (tabela `usage`, EV-O08). O
`session-save.py` já percorre cada chamada do transcript e desduplica por `message.id`
(EV-O07), mas joga fora tudo o que distingue uma chamada da outra: hora, se foi de subagente,
se foi erro. Resultado: não dá para responder "quanto gastei nas últimas 5 horas", "quanto
disso foi subagente", "qual modelo pesa mais nesta semana", nem montar a base que L-01
(parte C) e o E5 precisariam. Também não há preço nem política de retenção.

Na máquina de trabalho há **32.869 chamadas únicas** em 487 transcripts, e **75% delas são de
subagentes** (EV-M01, EV-M04) — dado que existe, está local, e hoje não é consultável: a tabela
`usage` não separa o que o orquestrador gastou do que os subagentes gastaram.

## O que o Laya ensina

Uma linha por chamada, **sem conteúdo** (nem prompt, nem resposta), com passo, modelo, tokens,
latência, sucesso e erro (EV-L17), gravada no caminho da chamada (EV-L18); custo **não é
gravado**: é calculado na consulta a partir de uma tabela de preços, e modelo sem preço vale
$0 para não gerar gasto fantasma (EV-L15); "feature" é derivada do passo por um mapa
(EV-L16); retenção de 90 dias podada por agendador (EV-L19).

O que **não** repetir: zerar modelo sem preço em silêncio; gravar a mensagem de erro do
provedor sem limpeza; mapear linhas do banco por posição de coluna.

## Desenho

**Tabela `calls`** em `osforge-db.py` (migração idempotente, como as do B-018):

```sql
CREATE TABLE IF NOT EXISTS calls (
    message_id    TEXT PRIMARY KEY,            -- id da mensagem do assistente (desduplica)
    project_id    INTEGER REFERENCES projects(id),
    session_id    TEXT    NOT NULL,
    ts            TEXT    NOT NULL,            -- timestamp da linha do transcript, UTC ISO-8601
    model         TEXT    NOT NULL,
    input         INTEGER NOT NULL DEFAULT 0,
    output        INTEGER NOT NULL DEFAULT 0,
    cache_read    INTEGER NOT NULL DEFAULT 0,
    cache_write_5m INTEGER NOT NULL DEFAULT 0, -- usage.cache_creation.ephemeral_5m_input_tokens
    cache_write_1h INTEGER NOT NULL DEFAULT 0, -- usage.cache_creation.ephemeral_1h_input_tokens
    sidechain     INTEGER NOT NULL DEFAULT 0,  -- isSidechain (subagente)
    stop_reason   TEXT,
    error         TEXT                         -- só o tipo ("rate_limit", …), já limpo
);
CREATE INDEX IF NOT EXISTS calls_ts ON calls(ts);
CREATE INDEX IF NOT EXISTS calls_project_ts ON calls(project_id, ts);
```

Quando `cache_creation` não vier detalhado, `cache_write_5m` recebe
`cache_creation_input_tokens` (o preço de escrita de 5 min é o padrão).

**Escrita.** Na mesma passada de `_extract_usage` (EV-O07), acumular as linhas por chamada e
enviar **um** `osforge-db add-calls --stdin` com JSONL (um processo, não um por chamada).
`INSERT … ON CONFLICT(message_id) DO NOTHING` — Stop repetido não duplica. Linhas de erro
sintético (`isApiErrorMessage`) entram com tokens zero e `error` preenchido: é assim que a
rejeição de L-01 fica na série temporal. O teto atual de 64 MB por transcript continua valendo.
A tabela `usage` continua sendo gravada como hoje (compatibilidade com `board`/`stats`).

**Preços.** `claude-code/pricing.json` **(NOVO)**:

```json
{"schema": "osforge.pricing.v1", "source": "<URL oficial de preços>", "retrieved": "AAAA-MM-DD",
 "unit": "USD por milhão de tokens",
 "models": {"<prefixo do id>": {"input": 0, "output": 0, "cache_read": 0,
                                "cache_write_5m": 0, "cache_write_1h": 0}}}
```

Os valores são preenchidos **na implementação**, a partir da página oficial, com a data. Casar
por prefixo mais longo. Modelo sem preço custa 0 **e é listado** ("sem preço: N chamadas de
X") — a correção sobre o Laya. Sob assinatura, o número é **custo equivalente de API**, e é
assim que aparece na saída.

**Consulta.** `osforge-db calls [--project SLUG] [--since 5h|24h|7d|AAAA-MM-DD]
[--by model|session|day|sidechain] [--json]`: tokens por categoria, número de chamadas, custo
equivalente, e a linha de "sem preço". `--since 5h` é a visão de janela.

**Retenção.** `osforge-db prune-calls --older-than 90d`; o `session-save.py` chama no máximo
uma vez por dia (marca em `~/.osforge/calls-pruned-at`). `OSFORGE_CALLS_RETENTION_DAYS`
sobrepõe; `0` desliga a poda.

**Histórico.** `osforge-db backfill-calls [DIR]` (padrão `~/.claude/projects`, recursivo)
importa o que já existe, só leitura na origem, idempotente. Projeto resolvido pelo `cwd` da
linha com `hooks/lib/project_id.py`; sem projeto registrado → `project_id` nulo.

**Privacidade.** Nenhum texto de mensagem é gravado. O campo `error` guarda só o tipo
(`rate_limit`, `overloaded`, …) e passa por `hooks/lib/scrub.py`.

## Arquivos

`scripts/osforge-db.py` (tabela, `add-calls`, `calls`, `prune-calls`, `backfill-calls`) ·
`hooks/session-save.py` · `claude-code/pricing.json` **(NOVO)** · `deploy.sh` (levar o
`pricing.json`) · `tests/test-calls.sh` **(NOVO)** · `USAGE.md`.

## Testes (offline)

`tests/test-calls.sh`, com banco temporário (`OSFORGE_DB`) e transcripts sintéticos:

1. mesma `message.id` em três linhas → uma linha em `calls`; tokens idênticos à tabela `usage`
   para a mesma sessão (as duas visões batem).
2. `isSidechain: true` → `sidechain = 1`; `--by sidechain` separa.
3. linha de rejeição (formato de EV-C04) → linha com `error = "rate_limit"` e tokens zero.
4. Stop repetido → contagem de linhas inalterada.
5. `cache_creation` com 5m e 1h → colunas separadas; sem detalhe → tudo em 5m.
6. preço: modelo conhecido → custo calculado igual à conta à mão; modelo desconhecido →
   custo 0 **e** a linha "sem preço" com a contagem.
7. `--since 5h` exclui chamada de 6h atrás.
8. `prune-calls --older-than 90d` remove só o que passou; roda no máximo uma vez por dia.
9. `backfill-calls` em árvore com subpastas → mesma contagem que a passada direta; rodar duas
   vezes → idempotente.
10. nenhuma linha contém texto de mensagem (varredura do banco por um marcador plantado no
    conteúdo do transcript sintético).

## Aceite

Testes verdes; `session-save` continua abaixo do tempo atual no transcript de 30 MB do
`test-context-usage.sh` (medir antes e depois); `backfill-calls` na máquina de trabalho
reproduz a contagem de EV-M01 (32.869 chamadas, mais as 7 linhas sintéticas de rejeição).

## Riscos

| Risco | Mitigação |
|---|---|
| Crescimento do banco | ~33 mil linhas pequenas em dez semanas (EV-M01); retenção de 90 dias |
| Preço desatualizado | `retrieved` visível na saída; custo nunca gravado, então corrigir o arquivo corrige o histórico |
| Formato do transcript mudar | Leitura tolerante; campo ausente vira 0; fixture presa à versão |
