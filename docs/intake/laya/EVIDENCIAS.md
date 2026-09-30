# Laya — evidências

Toda afirmação das specs aponta para uma linha daqui. **FATO** = lido no código ou medido;
**OBS** = observado no binário do Claude Code, sem documentação pública; **INF** = inferência,
dita como tal.

- Laya: `aayushch/laya` @ `5970a114241ee09cec09d571acf9ba52d27ae612` — links abaixo usam
  `L = https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya`
- OSForge: `v5.1.0` @ `3f0446cafe57158ad7b9823c565ae4f973bdf014` (caminho:linha)
- Claude Code: 2.1.278 (macOS arm64); documentação consultada em 2026-09-24:
  `code.claude.com/docs/en/headless.md`, `cli-reference.md`, `hooks.md`, `permission-modes.md`

## Laya (EV-L)

| ID | Onde | Fato | Tipo |
|---|---|---|---|
| EV-L01 | [`llm/agent_backend.py#L49`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L49) | Claude Code é o único backend `native` (schema forçado); Codex, Gemini e Pi são `best_effort` (schema como texto + validação + retry) | FATO |
| EV-L02 | [`agent_backend.py#L59`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L59) | Lista de ferramentas embutidas negadas para a chamada ser "completion pura" | FATO |
| EV-L03 | [`agent_backend.py#L78`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L78) | Diretiva prefixada ao system prompt para o CLI não perguntar nem oferecer ações | FATO |
| EV-L04 | [`agent_backend.py#L145`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L145) | Semáforo de concorrência (padrão 3; cada processo leva 5–12 s segundo o comentário) | FATO |
| EV-L05 | [`agent_backend.py#L282`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L282) | `claude -p … --output-format stream-json --verbose --permission-mode default --disallowedTools …`; cwd vazio e efêmero | FATO |
| EV-L06 | [`agent_backend.py#L290`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L290) | `--json-schema` com o schema do estágio | FATO |
| EV-L07 | [`agent_backend.py#L358`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L358) | Lê o evento `rate_limit_event` e guarda `rate_limit_info` | FATO |
| EV-L08 | [`agent_backend.py#L364`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L364) | Resultado estruturado lido de `result.structured_output` | FATO |
| EV-L09 | [`agent_backend.py#L372`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L372) | Tokens de entrada = `input + cache_creation + cache_read` — mesma fórmula do nosso `context-threshold.py` (EV-O06) | FATO |
| EV-L10 | [`agent_backend.py#L222`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/agent_backend.py#L222) | Validação local: `jsonschema` se importável, senão só chaves obrigatórias | FATO |
| EV-L11 | [`pipeline/agent_budget.py#L33-L34`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/agent_budget.py#L33-L34) | Padrões: pausa a 85% de uma janela de 5 h | FATO |
| EV-L12 | [`agent_budget.py#L37`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/agent_budget.py#L37) | Status considerados "ok": `allowed`, vazio, nulo | FATO |
| EV-L13 | [`agent_budget.py#L135`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/agent_budget.py#L135) | Consumo da janela = `SUM(input_tokens + output_tokens)` do `audit_log` nas últimas N horas (a entrada inclui *cache read*, EV-L09) | FATO |
| EV-L14 | [`agent_budget.py#L217`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/agent_budget.py#L217) | Sinal nativo primeiro; senão teto de tokens; pausa até o reset mais tardio | FATO |
| EV-L15 | [`pipeline/budget.py#L20-L27`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/budget.py#L20-L27) | Modelo sem preço custa $0 — o padrão antigo gerava gasto fantasma e pausava tudo | FATO |
| EV-L16 | [`budget.py#L30`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/budget.py#L30) | "Feature" derivada do passo por mapa, não gravada | FATO |
| EV-L17 | [`db/migrations/003_audit.sql#L3`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/db/migrations/003_audit.sql#L3) | `audit_log`: passo, modelo, tokens, latência, sucesso, erro, metadados; sem conteúdo de mensagem | FATO |
| EV-L18 | [`llm/client.py#L522`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/client.py#L522) | Gravação síncrona no caminho de cada chamada | FATO |
| EV-L19 | [`config.py#L73`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/config.py#L73) · [`scheduler.py#L166`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/scheduler.py#L166) | Retenção de 90 dias, podada pelo agendador | FATO |
| EV-L20 | [`retrieval.py#L56`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/retrieval.py#L56) · [`#L79`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/retrieval.py#L79) | RRF com k=60; id cai para `str(rank)` quando o item não tem id — itens diferentes no mesmo rank de listas diferentes colidem | FATO |
| EV-L21 | [`pipeline/learn_common.py#L42`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/learn_common.py#L42) · [`config.py#L154-L165`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/config.py#L154-L165) | Aprende quando um escopo junta ≥ 15 correções (contexto: 10); lote 50 (40); injeta até 20; consolida acima de 40 | FATO |
| EV-L22 | [`scheduler.py#L549`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/scheduler.py#L549) | Verificação a cada 6 h pelo agendador | FATO |
| EV-L23 | [`pipeline/learn.py#L121-L126`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/learn.py#L121-L126) · [`db/migrations/028_classification_feedback.sql#L23`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/db/migrations/028_classification_feedback.sql#L23) | Regra aprendida = frase com `source='learned'`; a tabela não tem contagem nem data de disparo | FATO |
| EV-L24 | [`learn.py#L149-L155`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/learn.py#L149-L155) · [`#L235`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/learn.py#L235) | Consolidação só roda logo após uma extração; se o resultado não for menor, nada é trocado | FATO |
| EV-L25 | [`pipeline/feedback.py#L86-L98`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/feedback.py#L86-L98) | Injeção seleciona só `field, rule_text` (sem `source`), mais recentes primeiro; sem espaço, ramo sem filtro de escopo | FATO |
| EV-L26 | [`feedback.py#L157`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/feedback.py#L157) | Regras entram como texto "(always follow these)" no prompt; nada as executa | FATO |
| EV-L27 | [`llm/prompts/learner.py#L46`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/llm/prompts/learner.py#L46) · [`learn.py#L128-L134`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/pipeline/learn.py#L128-L134) | Anti-duplicata é só instrução no prompt; a justificativa do modelo vai truncada para o log e é descartada | FATO |
| EV-L28 | [`db/migrations/060_processing_rules_constraints.sql#L39-L40`](https://github.com/aayushch/laya/blob/5970a114241ee09cec09d571acf9ba52d27ae612/engine/laya/db/migrations/060_processing_rules_constraints.sql#L39-L40) | Regras **determinísticas** têm `last_fired_at` e `fire_count` (e tabela de disparos); as aprendidas não | FATO |

## OSForge (EV-O) — `v5.1.0`

| ID | Onde | Fato | Tipo |
|---|---|---|---|
| EV-O01 | `scripts/test-skill-triggering.sh:221-229` | `claude -p --model --dangerously-skip-permissions --max-turns --output-format stream-json --verbose` | FATO |
| EV-O02 | `scripts/test-skill-triggering.sh:240-246` | Sem evidência de disparo → `miss` (ou timeout se exit 124); nenhum ramo para erro de API | FATO |
| EV-O03 | `scripts/test-skill-triggering.sh:268-275` | `k = N` PASS · `0 < k < N` FLAKY (3) · só timeouts TIMEOUT (2) · resto FAIL (1) | FATO |
| EV-O04 | `grep -rn "is_error\|rate_limit\|429\|session limit"` em `scripts/test-*.sh`, `scripts/run-trigger-eval.sh`, `scripts/lib/`, `skills/skill-creator/scripts/run_eval.py` | Zero ocorrências | FATO |
| EV-O05 | `scripts/test-orchestrator-routing.sh:163` | Mesma invocação e mesma ausência de tratamento | FATO |
| EV-O06 | `hooks/context-threshold.py:57-87` (fórmula na 82) | Contexto = `input + cache_read + cache_creation` da última resposta | FATO |
| EV-O07 | `hooks/session-save.py:195-238` | Uso por modelo desduplicado por `message.id`; teto de 64 MB; hora, subagente e erro descartados | FATO |
| EV-O08 | `scripts/osforge-db.py:862-874` | Tabela `usage`: único por projeto+sessão+modelo; sem série temporal | FATO |
| EV-O09 | `scripts/osforge-db.py:555-566`, `568-625`, `810-812` | RRF k=60 com rank 1-based; filtro de projeto antes da fusão; FTS5 de conteúdo externo com triggers | FATO |
| EV-O10 | `scripts/osforge-db.py:847-860` e `grep -rln instinct hooks/` | `instincts` com confiança 0–1, escopo, `seen_count`; nenhum hook lê a tabela | FATO |
| EV-O11 | `hooks/hooks-claude-code.json` | `UserPromptSubmit`: `context-threshold.py`, `gateguard.py`; `Stop`: `notify-done`, `session-save`, `canvas-feedback`, `route-guard` | FATO |
| EV-O12 | `scripts/check-counts.py:24-26`, `34` | Conta os scripts de hook conectados e confere "N hooks" no README | FATO |
| EV-O13 | `docs/ANALISE-COMPARATIVA-ECC.md:246`, `docs/BACKLOG-EVOLUCAO.md:232` | R-09 adiado até o E5; caminho barato de injeção já desenhado | FATO |

## Claude Code (EV-C) — 2.1.278

| ID | Fato | Fonte | Tipo |
|---|---|---|---|
| EV-C01 | O JSON de entrada do statusline traz `rate_limits.five_hour` e `.seven_day` com `used_percentage` e `resets_at`; `rate_limits_available: false` (API key, Bedrock, Vertex) → `rate_limits: null`. O statusline do usuário já lê esses campos (`~/.claude/statusline-command.sh:10-11`, fora do repositório) | esquema e montagem no binário | OBS |
| EV-C02 | Evento `{type: "rate_limit_event", rate_limit_info, uuid, session_id}`, com `rate_limit_info = {status, resetsAt, rateLimitType, isUsingOverage}` | construtor no binário; ausente de `headless.md` | OBS |
| EV-C03 | O valor `allowed_warning` existe no binário ao lado de `allowed` e `rejected` | binário | OBS |
| EV-C04 | Na rejeição, o transcript grava uma linha de assistente com `isApiErrorMessage: true`, `error: "rate_limit"`, modelo `<synthetic>`, tokens zero e `quotaLimits = {status: "rejected", rateLimitType: "five_hour", resetsAt, overageStatus, …}`. `quotaLimits` **só** aparece nessas linhas (7 de 7) | transcripts locais | FATO |
| EV-C05 | Ajuda do `--bare`: "Anthropic auth is strictly ANTHROPIC_API_KEY or apiKeyHelper via --settings (OAuth and keychain are never read)" | texto de ajuda no binário | OBS |
| EV-C06 | `--setting-sources <sources>`: "Comma-separated list of setting sources to load (user, project, local)"; não consta de `headless.md` nem `cli-reference.md` | texto de ajuda no binário | OBS |
| EV-C07 | `--tools <tools...>`: 'Use "" to disable all tools' | texto de ajuda no binário | OBS |
| EV-C08 | `--strict-mcp-config`: só usa MCPs de `--mcp-config` | documentação + binário | FATO |
| EV-C09 | Variáveis `CLAUDE_CODE_DISABLE_CLAUDE_MDS` e `CLAUDE_CODE_DISABLE_AUTO_MEMORY` existem | tabela de variáveis no binário | OBS |
| EV-C10 | `--json-schema`; resultado em `structured_output` do evento final | `headless.md` | FATO |
| EV-C11 | O evento `system/init` traz `tools` e `mcp_servers` | montagem do evento no binário | OBS |
| EV-C12 | Payloads de hook não trazem dado de cota ou janela | `hooks.md` | FATO |

## Medições na máquina de trabalho (EV-M) — 2026-09-22 a 24, agregadas

| ID | Fato |
|---|---|
| EV-M01 | `~/.claude/projects`: 487 transcripts (recursivo), **32.869 chamadas únicas** de assistente (por `message.id`, sem as sintéticas), de 2026-07-14 a 2026-09-21. 7 linhas de rejeição em 3 transcripts, **2 janelas distintas**, ambas `five_hour`: reset em 2026-09-04 17:00 UTC e em 2026-09-15 03:30 UTC |
| EV-M02 | Composição das duas janelas até a rejeição (tabela abaixo): Sonnet domina a primeira em chamadas, Opus domina a segunda em *cache write*; em todos os modelos o *cache read* é de 6 a 15 vezes o *cache write*. Somas brutas não são comparáveis entre as duas |
| EV-M03 | Nas duas rejeições: `overageStatus: "rejected"`, `overageDisabledReason: "org_level_disabled"` — não há excedente; o trabalho para |
| EV-M04 | 24.757 das 32.869 chamadas (**75%**) têm `isSidechain: true` (subagentes); todas trazem `stop_reason` e `usage.cache_creation` detalhado em 5 min / 1 h |

Janela 1 (12:00–17:00 UTC de 2026-09-04, até a rejeição às 15:38):

| Modelo | Chamadas | Cache write | Cache read | Saída |
|---|---:|---:|---:|---:|
| Sonnet 5 | 2.325 | 21,5 M | 243,8 M | 228 k |
| Fable 5.1 | 185 | 8,2 M | 74,0 M | 209 k |
| Haiku 4.5 | 140 | 0,6 M | 9,3 M | 3 k |

Janela 2 (22:30–03:30 UTC, até a rejeição às 02:58 de 2026-09-15):

| Modelo | Chamadas | Cache write | Cache read | Saída |
|---|---:|---:|---:|---:|
| Sonnet 5 | 686 | 8,0 M | 66,7 M | 79 k |
| Opus 5 | 326 | 21,9 M | 147,6 M | 177 k |
| Haiku 4.5 | 78 | 0,4 M | 5,3 M | 1 k |
| Fable 5.1 | 54 | 6,9 M | 40,1 M | 116 k |

## Método

- Laya: clone no SHA fixado; leitura direta; os módulos de aprendizado e de recuperação lidos
  também por dois leitores independentes, e cada afirmação reconferida no arquivo antes de
  entrar aqui. O Laya não foi executado.
- Claude Code: documentação pública; onde omissa, busca de cadeias no executável instalado
  (`grep -a` / leitura de bytes), **sem executar nenhuma chamada de modelo**. `claude --version`
  foi o único comando executado.
- Máquina de trabalho: leitura dos `.jsonl` em `~/.claude/projects`, contando por
  `message.id`, sem gravar, sem copiar conteúdo e sem registrar nome de projeto.
