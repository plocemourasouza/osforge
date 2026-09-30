# Laya — o que serve ao OSForge

| | |
|---|---|
| Fonte | https://github.com/aayushch/laya (branch padrão) |
| SHA analisado | `5970a114241ee09cec09d571acf9ba52d27ae612` (commit de 2026-09-19) |
| Licença | Apache-2.0 (`LICENSE`, `NOTICE`: © 2026 Aayush Chawla) |
| Tamanho | 379 commits · 674 arquivos · ~51 mil linhas de Python no `engine/` |
| OSForge de referência | `v5.1.0` (`3f0446c`) |
| Claude Code de referência | 2.1.278 (instalado na máquina de trabalho) |
| Evidências | [`EVIDENCIAS.md`](EVIDENCIAS.md) — todo `EV-…` citado aqui está lá |
| Data | 2026-09-22 (leitura) → 2026-09-24 (verificações e specs) |

## Resumo

O Laya não é um framework de configuração como o OSForge: é um aplicativo de desktop (Tauri +
Svelte, engine em Python/FastAPI, n8n, ChromaDB) que agrega notificações e usa LLMs para
triagem. Não há o que instalar nem copiar. O que ele tem de valioso para nós são **três
mecanismos** que resolvem problemas que já temos, e **um alerta** sustentado por código real:

| # | Candidato | Problema que resolve no OSForge | Spec | Esforço |
|---|---|---|---|---|
| L-01 | Guarda de janela de cota | A janela de 5h acaba no meio do trabalho sem aviso ao modelo; e o harness de evals conta uma rejeição por cota como *miss*, contaminando o E1 | [SPEC-L01](SPEC-L01-guarda-de-cota.md) | M |
| L-02 | Juiz isolado | Não existe caminho para avaliar **qualidade** (só disparo); uma chamada de juiz hoje carregaria o próprio OSForge do usuário | [SPEC-L02](SPEC-L02-juiz-isolado.md) | P–M |
| L-03 | Auditoria por chamada | Só há totais por sessão/modelo; sem série temporal, sem custo, sem retenção | [SPEC-L03](SPEC-L03-auditoria-por-chamada.md) | M |
| L-04 | Decisão do R-09 | O laço de *instincts* está adiado; o Laya fechou um laço equivalente e o código mostra onde ele degrada | [DECISAO-L04](DECISAO-L04-laco-de-aprendizado.md) | — |

## O que o Laya faz bem, e onde o OSForge encaixa

**Claude Code como motor de inferência.** O Laya roda o próprio pipeline sobre a cota da
assinatura do CLI, sem chave de API (EV-L01, EV-L05). A chamada é one-shot, sem ferramentas,
com schema forçado por `--json-schema` e saída lida de `structured_output` (EV-L06, EV-L08),
e ele lê do mesmo stream o evento `rate_limit_event` (EV-L07). Para o OSForge isso vira duas
coisas diferentes: a **convenção de chamada** para um juiz (L-02) e o **sinal de cota** (L-01).

**Orçamento por janela com pausa e retomada automática.** Sinal nativo primeiro; na falta
dele, soma de tokens do `audit_log` contra um teto configurado, pausando a 85% de uma janela
de 5h e religando no reset (EV-L11 a EV-L14). A ideia de "sinal nativo manda; estimativa só
na falta" é o núcleo de L-01. A estimativa por soma de tokens **não** foi aceita — ver
"Recusados".

**Auditoria sem conteúdo, custo derivado.** Uma linha por chamada, sem prompt nem resposta
gravados; custo calculado na consulta a partir de uma tabela de preços, com modelo
desconhecido valendo $0 para não inventar gasto (EV-L15 a EV-L19). É o desenho de L-03, com
três correções: o Laya zera modelo sem preço em silêncio, grava o texto de erro do provedor
sem limpeza, e lê as linhas por posição de coluna.

## Achado lateral que torna L-01 urgente

Os dois harnesses de eval não têm nenhum ramo para erro de API ou limite de cota
(EV-O02, EV-O04). Um caso rejeitado por cota não tem evidência de disparo, então cai em
`miss` e o veredito vira **FLAKY** (se alguma execução anterior acertou) ou **FAIL**
(EV-O03). O E1 — a rodada que o B-013 espera — existe justamente para medir instabilidade;
rodado perto do limite, ele mediria a cota e chamaria de instabilidade. Na máquina de trabalho
a janela de 5h foi rejeitada em **duas janelas distintas nas últimas três semanas**, sem
*overage* disponível (EV-M01, EV-M03). A parte B de L-01 deve entrar **antes** do B-013.

## Recusados

| Mecanismo do Laya | Por que não | Evidência |
|---|---|---|
| Busca híbrida (vetor + BM25/FTS5 com RRF) | Já temos, e melhor: `cmd_search_hybrid` funde FTS5 e vetor com RRF k=60, rank 1-based, e filtra por projeto **antes** da fusão; o do Laya tem fallback de id `str(rank)` que colide entre listas | EV-O09, EV-L20 |
| Estimar a janela somando tokens | As duas rejeições observadas têm composições incompatíveis (numa, 2,3 mil chamadas de Sonnet; na outra, Opus dominante) e a soma bruta é dominada por *cache read*. O limite pondera modelo e categoria de um jeito que não conhecemos. E o Claude Code já entrega o percentual pronto no statusline (EV-C01) | EV-M02, EV-L13 |
| Retry com schema-como-texto para outros CLIs | O OSForge só roda sobre Claude Code; o caminho *native* basta | EV-L01 |
| Personas, n8n, egress, ChromaDB, UI | Outro produto | — |

## Ordem proposta dentro do pacote

```
L-01 parte B (harness)  ──→  B-013 / E1        (antes de gastar cota medindo)
L-03 (auditoria)        ──→  L-01 parte C      (calibração, só se um dia for necessária)
E-J0 (1–3 chamadas)     ──→  L-02 (juiz)  ──→  E4 (leniência do revisor)
L-04                    ──→  pré-requisito do E5: registro de injeção
```

Custo: tudo verificável offline, exceto o experimento E-J0 de L-02 (1 a 3 chamadas curtas,
pede autorização) e a validação ao vivo de L-01 (nenhuma chamada extra: aproveita a primeira
rodada real do B-013).

## Licença e proveniência

Apache-2.0 é compatível com o MIT do OSForge para ideias e para código com atribuição. As
specs descrevem mecanismos com palavras próprias e **não copiam código**; se na implementação
algum trecho for reaproveitado literalmente (por exemplo o texto da diretiva não interativa,
EV-L03), ele entra com o aviso da Apache-2.0 e o `NOTICE` do Laya em `THIRD_PARTY_NOTICES`,
como foi feito com o ECC.

## Método e limites

Leitura do código no SHA fixado (clone local), com dois leitores independentes para os
módulos de aprendizado e de recuperação; toda afirmação usada nas specs foi reconferida
contra o arquivo e está em `EVIDENCIAS.md`. O Laya **não foi executado**. Nenhuma chamada de
modelo foi feita: o comportamento do Claude Code vem da documentação pública e, onde ela é
omissa, dos textos de ajuda e esquemas embutidos no binário 2.1.278 — marcado como
*observado, não documentado*, com o risco correspondente em cada spec. As medições da máquina
de trabalho são agregadas e não citam projeto, conteúdo nem prompt.
