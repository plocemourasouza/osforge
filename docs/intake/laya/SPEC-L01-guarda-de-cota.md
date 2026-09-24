# L-01 · Guarda de janela de cota

**Origem:** Laya `agent_budget.py` + leitura de `rate_limit_event` (EV-L07, EV-L11 a EV-L14).
**Evidência local:** EV-M01 a EV-M03, EV-O02 a EV-O05, EV-C01 a EV-C04, EV-C12.
**Esforço:** M (A: P · B: P · C: adiada). **Custo de verificação:** zero chamadas.

## Problema

1. A janela de 5h da assinatura acaba no meio do trabalho. Na máquina de trabalho isso
   aconteceu em duas janelas distintas nas últimas três semanas, com *overage* desligado pela
   organização — ao bater no limite, o trabalho simplesmente para (EV-M01, EV-M03). O
   percentual consumido chega ao statusline do usuário (EV-C01) mas **não chega ao modelo**:
   nenhum payload de hook carrega esse dado (EV-C12). O modelo não tem como gravar o handoff
   antes de ser cortado, que é exatamente o que o `context-threshold` já faz para contexto.
2. Os harnesses de eval tratam uma rejeição por cota como *miss* (EV-O02 a EV-O05), o que
   transforma esgotamento de cota em FLAKY/FAIL e corrompe o E1.

## Os três sinais que existem (Claude Code 2.1.278)

| Sinal | Onde aparece | Quando | Conteúdo | Status |
|---|---|---|---|---|
| S1 `rate_limits` | stdin do comando de statusline | a cada atualização da sessão interativa | `five_hour` e `seven_day` → `used_percentage`, `resets_at`; `null` quando o plano não tem limite (API key, Bedrock, Vertex) | observado no binário; já lido pelo statusline do usuário (EV-C01) |
| S2 `quotaLimits` | linha do transcript | **só na rejeição** | `status: "rejected"`, `rateLimitType`, `resetsAt`, `overageStatus`; a linha tem `isApiErrorMessage: true`, `error: "rate_limit"`, modelo `<synthetic>` | observado nos transcripts (EV-C04) |
| S3 `rate_limit_event` | `claude -p --output-format stream-json --verbose` | em execução headless | `rate_limit_info`: `status` (`allowed`, `allowed_warning`, `rejected`), `resetsAt`, `rateLimitType`, `isUsingOverage` | não documentado; observado no binário e consumido pelo Laya (EV-C02, EV-C03, EV-L07) |

S1 é o único sinal **antecipado**. S2 é o único que um hook consegue ler sozinho. S3 é o
único disponível no harness.

## Desenho

### Parte A — sessão interativa (S1 + S2)

**A1. Gravador.** `hooks/quota-record.py` **(NOVO)** lê o JSON do statusline no stdin e grava
`~/.osforge/quota.json` de forma atômica (temporário + `os.replace`):

```json
{"schema": "osforge.quota.v1", "at": 1790000000, "source": "statusline",
 "five_hour": {"pct": 83.0, "resets_at": 1790012345},
 "seven_day": {"pct": 41.0, "resets_at": 1790500000},
 "rejected": null}
```

Regras: nunca imprime nada; sai 0 em qualquer erro; `rate_limits` ausente ou `null` → não
grava (e não apaga o arquivo existente); termina em < 20 ms; mesmo tamanho máximo de stdin do
`context-threshold.py` (1 MB). Variável de caminho `OSFORGE_QUOTA_FILE` para os testes.

**A2. Rejeição pelo transcript.** No Stop, `hooks/session-save.py` já lê o fim do transcript
(EV-O07). Na mesma passada: se a última linha de assistente tiver `quotaLimits.status ==
"rejected"`, gravar `rejected: {"type": rateLimitType, "resets_at": resetsAt, "at": agora}`
em `quota.json` com `source: "transcript"`. Não depende do statusline.

**A3. Aviso ao modelo.** Em `UserPromptSubmit`, ler `quota.json` e injetar
`additionalContext` por faixa, **uma vez por faixa por janela** (a chave é `resets_at`, não a
sessão — a janela atravessa sessões):

| Faixa (`five_hour.pct`) | Mensagem (resumo) |
|---|---|
| ≥ 80 | "Janela de 5h em N% (reseta HH:MM local): termine o passo atual; não abra ondas paralelas nem subagentes novos." |
| ≥ 95 | "Janela de 5h em N%: PARE e grave o handoff agora (`osforge-db set-resume <slug> "…"` ou plano). Você pode ser cortado no próximo turno." |
| `rejected` com reset no futuro | Na primeira mensagem após o reset: "A janela anterior foi rejeitada às HH:MM; confira o handoff antes de retomar." |

Ignorar o arquivo quando `at` tiver mais de 15 min (sessão sem statusline ativo) ou quando
`resets_at` já passou. Faixas sobrepostas por `OSFORGE_QUOTA_BANDS="80,95"`; desligar com
`OSFORGE_QUOTA_THRESHOLD=off`. A faixa de 7 dias entra só como texto informativo quando
`seven_day.pct ≥ 90`.

### Parte B — harness de evals (S3)

**B1.** `scripts/lib/stream_assert.py` ganha o subcomando `quota <stream>`: imprime o último
`rate_limit_info` (JSON numa linha) ou nada; e `run-status <stream>`: `ok`, `error` ou
`quota`, onde `quota` = evento `result` com `is_error` **e** (`rate_limit_info.status ==
"rejected"` **ou** texto de erro de limite). Nenhuma heurística além dessas duas.

**B2.** Nos três harnesses (`test-skill-triggering.sh`, `test-orchestrator-routing.sh`,
`run-trigger-eval.sh`), depois de cada execução: `run-status == quota` → a execução **não
conta** (nem hit, nem miss), o lote para, os casos restantes saem como `NOT RUN` no relatório,
e o script sai com **75** (`EX_TEMPFAIL`), distinto de FAIL (1), TIMEOUT (2) e FLAKY (3).
`run-status == error` → conta como `ERROR`, também fora do k de N.

**B3.** Antes de cada caso: se `quota.json` existir, for recente e `five_hour.pct ≥
OSFORGE_EVAL_QUOTA_STOP` (padrão 85) ou houver `rejected` com reset no futuro, não iniciar o
caso (mesmo `NOT RUN` / 75). `--ignore-quota` desliga, para quem sabe o que está fazendo.
O relatório de `eval_report.py` registra `quota_at_start` e `quota_at_end`.

### Parte C — calibração (adiada, não implementar agora)

Estimar a janela a partir de tokens só faz sentido se S1 deixar de existir. Com duas
rejeições observadas e composições incompatíveis (EV-M02), não há como ajustar pesos. Se um
dia for preciso: usar as linhas de L-03 e exigir ≥ 5 rejeições antes de propor qualquer teto.

## Decisões em aberto

- **D-1 — como o gravador recebe o stdin do statusline.** O statusline é do usuário
  (`~/.claude/statusline-command.sh`, fora do repositório) e o OSForge não o gerencia.
  (a) **recomendado para começar:** uma linha opcional, documentada, no script do usuário —
  `printf '%s' "$input" | python3 "$HOME/.claude/hooks/quota-record.py" >/dev/null 2>&1 &` —
  sem conflito de propriedade; (b) depois, se provar valor: o deploy passa a gerenciar a
  chave `statusLine` com um wrapper que grava e depois executa o comando original, guardado no
  estado de instalação e restaurado pelo `--uninstall`.
- **D-2 — hook novo ou dentro do `context-threshold.py`.** Recomendado: módulo
  `hooks/lib/quota.py` chamado de dentro do `context-threshold.py` (mesmo evento, EV-O11; mesmo padrão
  de estado, um processo a menos por prompt, contagem de hooks inalterada). Os dois avisos
  continuam com chaves de desligamento independentes. Se virar hook próprio, o `check-counts`
  exige atualizar "11 hooks" no README (EV-O12).
- **D-3 — `allowed_warning` para o harness.** Recomendado: registrar e seguir; parar só em
  `rejected` ou pelo limiar de B3.

## Arquivos

`hooks/quota-record.py` **(NOVO)** · `hooks/lib/quota.py` **(NOVO)** · `hooks/context-threshold.py`
· `hooks/session-save.py` · `scripts/lib/stream_assert.py` · `scripts/test-skill-triggering.sh`
· `scripts/test-orchestrator-routing.sh` · `scripts/run-trigger-eval.sh` ·
`scripts/lib/harness-assertions.sh` · `scripts/lib/eval_report.py` · `tests/test-quota.sh`
**(NOVO)** · `tests/hooks/` (casos de contrato) · `USAGE.md` (seção de variáveis) ·
`docs/HOOKS.md`.

## Testes (offline, todos vermelhos sem a mudança)

`tests/test-quota.sh`:

1. statusline com `five_hour.used_percentage=83` → `quota.json` com `pct: 83` e `resets_at`;
   stdout vazio; exit 0.
2. statusline sem `rate_limits`, com `null` e com JSON inválido → arquivo anterior intacto,
   exit 0.
3. faixas: 79 / 80 / 95 → 0 / 1 / 2 avisos; repetir 95 na mesma janela → nenhum; nova
   `resets_at` → avisa de novo; sessão diferente na mesma janela → **não** avisa de novo.
4. `quota.json` com `at` de 20 min atrás → silêncio; `resets_at` no passado → silêncio;
   `OSFORGE_QUOTA_THRESHOLD=off` → silêncio.
5. transcript com a linha de rejeição (fixture no formato de EV-C04, sem conteúdo real) →
   Stop grava `rejected`; o próximo `UserPromptSubmit` depois do reset avisa uma vez.
6. `stream_assert.py run-status`: stream com `result.is_error` + `rate_limit_event` rejeitado
   → `quota`; com `allowed` → `ok`; `is_error` sem limite → `error`.
7. harness com `claude` falso no `PATH` que devolve o stream rejeitado no 2º caso → caso 1
   PASS, caso 2 e seguintes `NOT RUN`, exit 75; **nenhum** FLAKY/FAIL no relatório.
8. harness com `quota.json` em 90% → nenhum caso inicia, exit 75; com `--ignore-quota` roda.
9. `quota-record.py` com stdin de 1 MB → < 20 ms, exit 0.

Mais: casos no `tests/hooks/run-contracts.sh` para o `context-threshold` com e sem
`quota.json`; `check-portability.py` verde (a linha de D-1 usa só `printf` e `&`).

## Aceite

- Os nove casos acima verdes; as dez suítes atuais continuam verdes.
- Numa sessão real acima de 80%, a próxima mensagem do usuário recebe o aviso **uma** vez.
- A primeira rodada paga do B-013 grava `quota_at_start`/`quota_at_end` no relatório; se S3
  aparecer no stream, o formato real é conferido contra a fixture do caso 6 (sem custo extra).

## Riscos

| Risco | Mitigação |
|---|---|
| S1 e S3 não são documentados e podem mudar | Leitura tolerante (campo ausente = silêncio); fixtures presas à versão 2.1.278; contrato testado no CI |
| O aviso vira ruído | Uma vez por faixa por janela, e só com dado recente |
| Harness parar à toa | Limiar configurável e `--ignore-quota` |
| Uso fora do Claude Code (claude.ai, outro dispositivo) consome a mesma janela e não aparece nos transcripts locais | S1 vem do servidor (a `utilization` da resposta da API), não de contagem local — INF: por isso tende a refletir o consumo da conta inteira. É mais um motivo para não estimar por tokens locais |
