# Intake — candidatos de melhoria vindos de projetos externos

Esta pasta guarda o que foi **avaliado e aprovado como candidato**, mas ainda **não entrou no
backlog**. Cada projeto externo analisado ganha uma subpasta com análise, evidências e uma
especificação por mecanismo, pronta para implementação. Os candidatos só viram itens do
[`BACKLOG-EVOLUCAO.md`](../BACKLOG-EVOLUCAO.md) quando o pacote de melhorias for fechado —
depois de avaliadas as outras fontes previstas — para que a ordem de implementação saia do
conjunto, e não da ordem em que cada projeto foi lido.

## Regras (as mesmas da ADR-015)

1. **Importar mecanismo, não conteúdo.** Nenhuma linha de código de terceiro entra sem aviso
   de licença em `THIRD_PARTY_NOTICES`; o normal é reescrever a ideia no padrão do OSForge.
2. **Medir antes de adotar.** Todo candidato diz qual evidência o justifica e qual teste fica
   vermelho sem ele. Candidato sem medição possível vai para "adiado", não para "fazer".
3. **Nada pago sem autorização.** Cada spec separa o que é verificável offline do que exige
   chamada de modelo, e diz quantas chamadas.
4. **Não importar o que já temos.** Toda análise registra também o que foi recusado e por quê.

## Identificadores

| Prefixo | Significado |
|---|---|
| `L-01`…, `N-01`…, `P-01`… | candidato de uma fonte (L = Laya, N = Needle, P = Ponytail) |
| `EV-L…`, `EV-N…`, `EV-P…` | evidência no código da fonte, com permalink no SHA fixado |
| `EV-O…`, `EV-O-N…`, `EV-O-P…` | evidência no OSForge (caminho:linha em `v5.1.0`, `3f0446c`), por fonte |
| `EV-C…`, `EV-C-P…` | comportamento do Claude Code observado ou documentado (versão registrada) |
| `EV-M…`, `EV-N-M…`, `EV-M-P…` | medição feita na máquina de trabalho (agregada, sem conteúdo), por fonte |
| `D-…` | decisão em aberto que a implementação precisa tomar |

## Estado

| Fonte | Analisada em | SHA | Candidatos | Estado |
|---|---|---|---|---|
| [Laya](laya/ANALISE.md) (`aayushch/laya`, Apache-2.0) | 2026-09-22 → 24 | `5970a11` | L-01 guarda de cota · L-02 juiz isolado · L-03 auditoria por chamada · L-04 decisão do R-09 | **incorporada** — Pacote 01, ADR-016, v5.2.0 (L-04 segue condicional ao E5) |
| [Needle](needle/ANALISE.md) (`cactus-compute/needle`, Apache-2.0) | 2026-09-24 → 25 | `42bf1f2` | N-01 casos de eval com categoria e críticos · o modelo foi **recusado com medição** | **incorporada** — Pacote 01, ADR-016, v5.2.0 |
| [Ponytail](ponytail/ANALISE.md) (`DietrichGebert/ponytail`, MIT) | 2026-10-22 | `09c434a` | P-01 escada da solução · P-02 review do código conectado · P-03 `repo-audit` · P-04 guardas de edição · P-05 monitor de andamento · o plugin foi **recusado** | **incorporada** — [Pacote 02](PACOTE-02-ponytail.md), ADR-019 (aprovado em 2026-10-22; regras dependem da r3) |

**Pacotes:**

| Pacote | Itens | Estado |
|---|---|---|
| [Pacote 01 — Qualidade e controle](PACOTE-01-qualidade-e-controle.md) | B-025 a B-030 | entregue em v5.2.0 (ADR-016); B-030 condicional ao E5 |
| [Pacote 02 — Ponytail](PACOTE-02-ponytail.md) | B-031 a B-038 | aprovado (ADR-019), em implementação: regras medidas na r3, guardas em sombra, monitor de portfólio |

Quando um pacote é aprovado: cada candidato vira um `B-0xx` no backlog com a mesma spec como corpo,
a análise passa a ser citada pela ADR que aprovar o pacote, e esta tabela marca a fonte como
**incorporada**.
