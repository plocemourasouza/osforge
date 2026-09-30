# Pacote 01 — Qualidade e controle

**Estado:** proposta, aguardando aprovação. **Fontes:** [Laya](laya/ANALISE.md) e [Needle](needle/ANALISE.md).
**Base:** OSForge `v5.1.0`. **Ids propostos no backlog:** B-025 a B-030.
**Evidências:** `EV-L…`, `EV-O…`, `EV-C…`, `EV-M…` em [`laya/EVIDENCIAS.md`](laya/EVIDENCIAS.md); `EV-N…`, `EV-N-M…`, `EV-O-N…` em [`needle/EVIDENCIAS.md`](needle/EVIDENCIAS.md).

## Em uma frase

Hoje o OSForge mede se a skill certa dispara. Mas essa medição pode ser corrompida pela cota e
por casos quebrados, e não diz em que tipo de pedido a skill falha. Além disso, o OSForge não
mede qualidade, e o consumo é visível para o usuário mas não para o modelo nem para o
harness. Este pacote fecha essas três lacunas, começando pelo que precisa estar pronto
**antes** do primeiro gasto com o E1.

## O pacote

| Id | Item | Origem | Problema que resolve | Esforço | Chamadas pagas | Spec |
|---|---|---|---|---|---|---|
| B-025 | Casos de eval com categoria, casos críticos e validação sem modelo | Needle | FLAKY sem diagnóstico; negação quase não medida; caso quebrado passa no CI | M | 0 | [N-01](needle/SPEC-N01-casos-de-eval.md) |
| B-026 | Harness respeita a cota | Laya | Rejeição por cota vira FLAKY/FAIL e corrompe o E1 | P | 0 | [L-01 parte B](laya/SPEC-L01-guarda-de-cota.md) |
| B-027 | Aviso de janela de cota ao modelo | Laya | Sessão cortada sem handoff; o percentual só aparece no statusline | P | 0 | [L-01 parte A](laya/SPEC-L01-guarda-de-cota.md) |
| B-028 | Auditoria por chamada, custo derivado, retenção | Laya | Só totais por sessão; sem série temporal, sem custo, sem ver subagentes | M | 0 | [L-03](laya/SPEC-L03-auditoria-por-chamada.md) |
| B-029 | Juiz isolado sobre a assinatura | Laya | Não existe como medir qualidade (E3, E4) | P–M | 1–3 (E-J0) | [L-02](laya/SPEC-L02-juiz-isolado.md) |
| B-030 | Registro de injeção de instincts | Laya | O E5 não é mensurável sem saber o que cada sessão recebeu | P | 0 | [L-04](laya/DECISAO-L04-laco-de-aprendizado.md) — **só se o E5 for rodar** |

Esforço na escala do backlog (P ≤ meio dia · M 1–3 dias): **3 a 7 dias** para o pacote
inteiro, sem contar B-030.

## Ordem

```
Onda 1 — antes do E1 (offline)      B-025 casos de eval ──┐
                                    B-026 harness × cota ─┴──→ B-013 / E1 (autorização de custo)
Onda 2 — visibilidade               B-027 aviso de cota      B-028 auditoria   (independentes)
Onda 3 — qualidade                  E-J0 (1–3 chamadas) ─→ B-029 juiz ─→ E4, E3
Condicional                         B-030 ──→ E5 ──→ decisão do R-09
```

A Onda 1 é a razão de o pacote existir agora. O E1 custa **273 chamadas**: 234 hoje, mais 39
porque B-025 passa a medir negação (EV-O-N07). Se ele rodar antes da Onda 1, o resultado pode
vir com FLAKY falsos por cota, sem leitura por categoria e sem os casos críticos. Seria pagar
por uma medição que depois teria de ser refeita.

## O que ganhamos

### 1. Medições em que dá para confiar e que dizem onde está o problema

| Hoje | Com o pacote |
|---|---|
| Uma rejeição por cota no meio do E1 transforma os casos seguintes em FLAKY/FAIL (EV-O02 a EV-O05) | A execução para, os casos restantes saem como `NOT RUN`, sai com 75 e o relatório registra a cota no início e no fim (B-026) |
| Caso com skill inexistente passa no CI e só falha na rodada paga (EV-O-N02, reproduzido) | O `--dry` reprova, e o CI (que já roda o `--dry` das três suítes) fica vermelho (B-025) |
| Resultado por caso: "FLAKY 2/3" | Resultado por categoria: positivo, vizinho (o caso difícil), irrelevante, negação (B-025) |
| 2 casos de negação em 150; 13 de 15 skills sem nenhuma | 15 negações, pelo menos uma por skill, todas críticas |
| `--allow-flaky` deixa passar qualquer caso instável | Caso crítico instável reprova a suíte sempre (20 críticos) |

### 2. Controle do consumo

| Hoje | Com o pacote |
|---|---|
| Janela de 5 h rejeitada em 2 janelas distintas em três semanas, sem excedente disponível: o trabalho simplesmente para (EV-M01, EV-M03) | O modelo recebe aviso a 80% e a 95%, uma vez por faixa, e grava o handoff antes de ser cortado (B-027) |
| Depois do corte, a sessão seguinte não sabe o que aconteceu | A primeira mensagem depois do reset avisa que a janela anterior foi rejeitada e aponta o handoff |
| 32.869 chamadas locais sem consulta possível; tokens só como total por sessão | Uma linha por chamada: "últimas 5 h", por modelo, por dia, orquestrador × subagente (B-028) |
| 75% das chamadas são de subagentes, e nada mostra isso (EV-M04) | `--by sidechain` separa; custo equivalente de API por modelo, com preço datado |

### 3. Qualidade medida, não só disparo

| Hoje | Com o pacote |
|---|---|
| Nenhum jeito de avaliar se uma revisão, um plano ou um diagnóstico está bom | Um juiz de uma chamada, sobre a assinatura (sem chave de API), com schema forçado e isolamento **conferido em cada chamada** pelo evento `init` (B-029) |
| Isolar pelo caminho óbvio (`--bare`) transformaria a chamada em cobrança de API (EV-C05) | A receita evita o `--bare` e é provada antes pelo E-J0 |
| E3 (plano proporcional) e E4 (leniência do revisor) sem instrumento | Os dois ganham o consumidor que faltava |

### 4. Decisões com base, não por impressão

- O R-09 deixa de ser "completar ou remover por palpite": o E5 só roda com o registro de
  injeção (B-030), e se o laço for completado já há a lista de seis guardas, tirada de um
  laço real que degrada sem elas (L-04).
- O que **não** fazer fica registrado com número, para ninguém reabrir sem dado novo:

| Recusado | Motivo medido |
|---|---|
| Needle como roteador local de skills | 0 a 13 acertos em 75; confiança sem sinal; sempre escolhe alguma skill; 8–10 s por processo |
| Needle como provider de embeddings | Perde para uma linha de base léxica de ~20 linhas |
| Estimar a janela somando tokens (Laya) | Duas rejeições com composições incompatíveis; o percentual real já vem pronto do Claude Code |
| Busca híbrida do Laya | O OSForge já tem, e com filtro de projeto antes da fusão |

## Custo

- **Implementar:** zero chamadas de modelo. Todos os testes são offline (quatro suítes novas:
  `test-eval-cases`, `test-quota`, `test-calls`, `test-judge`).
- **E-J0:** 1 a 3 chamadas curtas, com autorização própria, antes de adotar o juiz.
- **E1:** +39 chamadas (234 → 273), o preço de passar a medir negação.

## Pronto quando

1. As dez suítes atuais e as quatro novas verdes; CI verde em ubuntu e macOS.
2. `./scripts/run-trigger-eval.sh --dry`: 170 casos, 20 críticos, nenhum problema; os `--dry`
   de trigger em TSV e de roteamento reprovam caso órfão.
3. `check-counts` coerente. Se o aviso de cota ficar dentro do `context-threshold` (D-2,
   recomendado), a contagem de hooks continua 11.
4. E-J0 registrado em `docs/evals/`, com o juiz adotado ou recusado.
5. ADR-016 aprovando o pacote, `CHANGELOG` e os itens B-025 a B-030 no backlog.

## Como saber se valeu (depois de adotado)

- O E1 sai sem nenhum FLAKY causado por cota (`quota_at_start` e `quota_at_end` no relatório).
- Nenhum caso inválido chega a uma rodada paga.
- Nas próximas rejeições de janela registradas na tabela de chamadas, houve aviso de 80% antes.
- O relatório do E1 separa o resultado por categoria e mostra os críticos no topo.

## Riscos

| Risco | Mitigação |
|---|---|
| O Claude Code não documenta vários sinais usados (percentual no statusline, `rate_limit_event`, `--setting-sources`, variáveis de ambiente) | Leitura tolerante (campo ausente = silêncio), fixtures presas à versão 2.1.278, testes de contrato no CI, E-J0 para o juiz |
| Os rótulos de categoria são julgamento | Revisão humana antes da migração (D-N3) |
| O pacote crescer além do combinado | Ondas independentes; cada item tem chave de desligamento ou reversão própria |

## Decisões pendentes

| Id | Decisão | Recomendação |
|---|---|---|
| D-1 | Como o gravador de cota recebe o stdin do statusline, que é seu | Uma linha opcional no seu script agora; wrapper gerenciado pelo deploy depois |
| D-2 | Aviso de cota como hook novo ou dentro do `context-threshold` | Dentro do `context-threshold` |
| D-3 | O que o harness faz com `allowed_warning` | Registrar e seguir |
| D-N1 | Quais casos de roteamento são críticos | Os de despacho obrigatório (`!`) |
| D-N2 | `expect_route` vira asserção | Não agora |
| D-N3 | Revisão dos rótulos e dos 20 casos novos | Antes da migração |
| — | Autorizar o E-J0 (1–3 chamadas) | Na Onda 3 |
