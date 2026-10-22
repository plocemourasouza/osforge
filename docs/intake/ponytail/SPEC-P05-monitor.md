# P-05 · Monitor de andamento do projeto (painel + faixa)

**Origem:** a faixa e o painel do Ponytail como referência de experiência (EV-P14, EV-P37),
reconstruídos sobre os dados do OSForge.
**Evidência local:** EV-O-P14, EV-O-P15, EV-O-P16, EV-M-P02, EV-C-P01 a EV-C-P04.
**Esforço:** M (painel) + M (faixa). **Chamadas pagas:** 0.

## Problema

O OSForge já guarda o andamento de cada projeto e o consumo de cada sessão. São 9 projetos,
43 fases, 292 tarefas, 129 decisões, 7 bloqueios e 33.840 chamadas desde 23/08 (EV-M-P02). Mas
só se vê isso pelo `osforge-db board` em texto ou perguntando ao modelo. A faixa do Ponytail
mostra o custo **da sessão**, não o andamento **do projeto**. Os números de qualidade dela
são frágeis (EV-P15, EV-P16) e vão para um CSV paralelo (EV-P14).

## Desenho

### 1. Contrato — `osforge-db monitor <slug> [--since 30d] --json`

Um único comando, usado pelas duas vistas e testável com banco temporário. Blocos:

- `projeto`;
- `andamento`: por fase, total, feitas, em andamento, bloqueadas, % concluído; tarefas abertas
  com prioridade, onda e dependências não resolvidas;
- `bloqueios`;
- `decisoes` (as últimas 10);
- `consumo`: por dia e por modelo; orquestrador × subagente; custo equivalente com preço datado
  (B-028);
- `janela` (`quota.json`, B-027);
- `qualidade`: `signals` abertos (P-04); estado dos testes; atalhos (`shortcut:`) e quantos
  não dizem quando trocar, contados com `git grep` na raiz do projeto, como no livro de dívida
  do Ponytail (EV-P34);
- `saude`: chamadas sem projeto, cobertura da memória.

Esquema versionado (`osforge.monitor.v1`).

### 2. Painel — `/monitor` no servidor do Canvas (fase 1)

- **Rotas:** `GET /monitor` (página) e `GET /api/monitor?project=<slug>&since=30d` (o JSON
  acima, via `osforge-db`). As atualizações chegam pelo SSE que já existe (`/api/events`),
  avisadas quando `session-save` ou `quality-guard` gravam.
- **Seções:**
  - cabeçalho com projeto, fase atual e % geral;
  - fases como barras;
  - quadro de tarefas em quatro colunas, com selo de prioridade e dependência;
  - bloqueios com idade;
  - decisões recentes;
  - consumo por dia, empilhado por modelo, com a linha da janela de 5 h;
  - qualidade (testes, chamadores abertos, duplicatas, atalhos sem gatilho);
  - atividade de 12 semanas.
- **Mantém o que o Canvas já garante:** só `127.0.0.1`, validação de Origin (B-020), nenhum
  recurso externo, tema claro e escuro, legível no celular.
- **Origem visual:** o layout de KPIs, gráfico por período e mapa de atividade pode partir do
  `board.ts` do Ponytail (MIT, com aviso). Os dados e a lógica são do OSForge.

### 3. Faixa — mod `osforge-monitor` (fase 2)

Módulo de hooks de função com `.claude-plugin/plugin.json` e `hooks/hooks.json`
(`{"modules": ["./register.tsx"]}`). O deploy o copia para `~/.osforge/mods/osforge-monitor/`
e acrescenta essa pasta a `CLAUDE_CODE_PLUGIN_DIRS` no `env` do `settings.json` (EV-C-P02).
O deploy já gerencia esse bloco e a remove no `--uninstall` (EV-O-P16).

- `session.start` e `turn.complete` rodam `osforge-db monitor <slug> --json --compact` por
  `$.process.run` e guardam o resultado em `$.state`.
- `$.session.usage()` traz custo, contexto e janela de 5 h direto do motor (EV-C-P03).
- `ui.render` em `AbovePrompt` (EV-C-P04) desenha uma linha:
  `● fase 2/4 · ▶ "Checkout com Pix" · 7/12 tarefas · ⛔ 1 bloqueio · $1,84 · 5h 63% · ctx 41%`.
  Quando há alertas, acrescenta `⚠ 2 chamadores abertos` e `testes desatualizados`.
- Botões: Painel (abre `http://127.0.0.1:4242/monitor`), Review, Audit, Copiar status.
- Nada é calculado dentro do desenho. Sem dados do projeto, mostra só consumo e janela. Com
  `OSFORGE_MONITOR_BAND=off`, devolve `next(e)`.
- O deploy confere a versão do Claude Code. Abaixo da mínima testada, não liga a faixa e
  avisa; o painel continua.

### 4. Painel lateral (fase 3, opcional)

A mesma informação num `Pane` (`$.ui.open`), aberto por um comando `/osforge-monitor`.

## Arquivos

`scripts/osforge-db.py` (`monitor`) · `scripts/canvas/server.ts` (duas rotas) ·
`scripts/canvas/monitor.html` **(NOVO)** · `mods/osforge-monitor/` **(NOVO)** · `deploy.sh`
(copiar o mod, `env`, versão mínima) · `scripts/osforge-state.py` (estado do mod) ·
`tests/test-monitor.sh` **(NOVO)** · `tests/canvas/` · `THIRD_PARTY_NOTICES`.

## Testes (offline)

1. `monitor --json` contra banco semeado: % por fase, contagem por status, dependências abertas,
   bloqueio com idade e consumo por dia batem com a conta à mão; esquema validado.
2. Projeto sem tarefas → blocos vazios, sem erro; slug desconhecido → exit 2.
3. 50 mil chamadas sintéticas → < 200 ms.
4. Canvas: `/api/monitor` só em `127.0.0.1`; Origin estranho → 403; projeto inexistente → 404;
   o HTML não carrega nada externo.
5. Mod: `claude plugin validate` e `claude plugin test` verdes; o teste do módulo **roda no CI**
   (o do Ponytail não roda — EV-P18); desenho sem chamada de processo; `OSFORGE_MONITOR_BAND=off`
   → `next(e)`.
6. Deploy: mod copiado, `env` mesclado sem tocar nas suas chaves, `--uninstall` remove os dois,
   `--doctor` limpo; versão abaixo da mínima → faixa não ligada, aviso emitido.

## Aceite

Testes verdes; o painel mostra os 9 projetos atuais com números que conferem com
`osforge-db board`; a faixa aparece no terminal e no app de desktop do Mac de trabalho
(Claude Code 2.1.307, EV-M-P03); nenhuma chamada nova de rede.
