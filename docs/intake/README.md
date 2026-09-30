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
| `L-01`…, `N-01`… | candidato de uma fonte (L = Laya, N = Needle) |
| `EV-L…`, `EV-N…` | evidência no código da fonte, com permalink no SHA fixado |
| `EV-O…`, `EV-O-N…` | evidência no OSForge (caminho:linha em `v5.1.0`, `3f0446c`), por fonte |
| `EV-C…` | comportamento do Claude Code observado (versão registrada) |
| `EV-M…`, `EV-N-M…` | medição feita na máquina de trabalho (agregada, sem conteúdo), por fonte |
| `D-…` | decisão em aberto que a implementação precisa tomar |

## Estado

| Fonte | Analisada em | SHA | Candidatos | Estado |
|---|---|---|---|---|
| [Laya](laya/ANALISE.md) (`aayushch/laya`, Apache-2.0) | 2026-09-22 → 24 | `5970a11` | L-01 guarda de cota · L-02 juiz isolado · L-03 auditoria por chamada · L-04 decisão do R-09 | no [Pacote 01](PACOTE-01-qualidade-e-controle.md) |
| [Needle](needle/ANALISE.md) (`cactus-compute/needle`, Apache-2.0) | 2026-09-24 → 25 | `42bf1f2` | N-01 casos de eval com categoria e críticos · o modelo foi **recusado com medição** | no [Pacote 01](PACOTE-01-qualidade-e-controle.md) |

**Pacotes:** [Pacote 01 — Qualidade e controle](PACOTE-01-qualidade-e-controle.md) (B-025 a B-030), proposta aguardando aprovação.

Quando um pacote é aprovado: cada candidato vira um `B-0xx` no backlog com a mesma spec como corpo,
a análise passa a ser citada pela ADR que aprovar o pacote, e esta tabela marca a fonte como
**incorporada**.
