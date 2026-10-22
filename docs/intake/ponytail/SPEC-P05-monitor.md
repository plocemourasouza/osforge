# P-05 · Monitor de projetos e atividades (painel + faixa)

**Revisão 3 (2026-10-22, aprovada):** o painel passa a ser um **portfólio**: lista todos os
projetos (em andamento, backlog, pausados, concluídos e os que têm sessão mas ainda não foram
cadastrados) e mostra o detalhe do projeto selecionado. O visual parte do quadro do Ponytail
(`hooks/band/board.ts`, MIT), adaptado; os dados e a lógica são do OSForge.
**Origem:** a faixa e o quadro do Ponytail (EV-P14, EV-P37).
**Evidência local:** EV-O-P14, EV-O-P15, EV-O-P16, EV-M-P02, EV-C-P01 a EV-C-P04.
**Esforço:** M (contrato) + M (painel) + M (faixa). **Chamadas pagas:** 0.

## Problema

O OSForge já guarda o andamento de cada projeto e o consumo de cada sessão: 9 projetos,
43 fases, 292 tarefas, 129 decisões, 7 bloqueios e 33.840 chamadas desde 23/08 (EV-M-P02). Mas
só se vê isso pelo `osforge-db board` em texto ou perguntando ao modelo, e sempre um projeto por
vez. Não há uma visão de **tudo o que está em curso**: o que anda, o que está parado em
bloqueio, o que está no backlog, quanto cada um consome.

Três lacunas nos dados aparecem ao montar essa visão (medidas em 2026-10-22, agregadas):

- `projects.status` só tem um valor em uso (`active`): não existe "backlog", "pausado" nem
  "concluído", então não há como separar o portfólio;
- só 1 de 9 projetos tem `root_path`: sem a raiz, o monitor não sabe onde contar atalhos nem
  rodar `git`;
- 25% das chamadas não têm projeto (EV-M-P02): sessões em pastas que não casam com nenhum
  projeto cadastrado.

## Desenho

### 0. Ciclo de vida do projeto

`projects.status` passa a ter cinco valores: `active` (em andamento), `backlog` (planejado,
não começou), `paused`, `done` e `archived`. Comando novo:
`osforge-db set-project-status <slug> <status>`; `upsert-project --status` valida o valor.
Valores antigos fora da lista continuam legíveis e aparecem como `outro` (nada é reescrito).
`archived` sai do portfólio por padrão (`--all` o inclui).

### 1. Contrato — `osforge-db monitor [<slug>] [--days 30] [--discover] --json`

Um único comando, usado pelas duas vistas e testável com banco temporário. Esquema versionado
`osforge.monitor.v1`. Somente leitura: o monitor nunca grava no banco.

**Sem slug → portfólio.**

- `gerado_em`, `dias`, `janela` (de `quota.json`, B-027; `null` se ausente);
- `totais`: projetos por status, tarefas abertas, bloqueios abertos, sinais abertos, chamadas,
  sessões, tokens e custo equivalente no período;
- `projetos[]`, um por projeto: `slug`, `descricao`, `status`, `triage`, `fase_atual`,
  `fases {total, feitas}`, `tarefas {pending, in_progress, blocked, done, cancelled}`, `pct`,
  `bloqueios_abertos`, `sinais_abertos`, `ultima_atividade`, `periodo {chamadas, sessoes,
  tokens, custo, minutos}`, `serie` (por dia do período: chamadas, tokens, custo, minutos),
  `acesso {raiz, raiz_existe, remoto}`;
- `sem_cadastro[]` (só com `--discover`): pastas com sessão do Claude Code nos últimos 30 dias
  que não casam com nenhum projeto, lidas do campo `cwd` das primeiras linhas dos transcripts
  em `~/.claude/projects/` (um arquivo por pasta, o mais recente). Para um projeto cadastrado
  sem `root_path`, a mesma leitura sugere a raiz (`acesso.raiz_sugerida`). Nada é gravado: o
  painel mostra o comando (`osforge-db upsert-project …`, `bind-project … --root=…`);
- `saude`: % de chamadas sem projeto, projetos sem raiz.

**Com slug → projeto.** Tudo do item do portfólio, mais:

- `fases[]` com total, feitas, em andamento, bloqueadas e %;
- `tarefas[]` abertas, com prioridade, onda e dependências não resolvidas;
- `bloqueios[]` com idade em dias;
- `decisoes[]` (as últimas 10);
- `consumo`: por dia e por modelo; orquestrador × subagente; custo com o preço datado (B-028);
- `sessoes[]` (as últimas 20): início, duração, chamadas, tokens, custo, modelo principal;
- `qualidade`: `signals` abertos (P-04), estado dos testes, atalhos (`shortcut:`) e quantos
  não dizem quando trocar, contados com `git grep` na raiz (como o livro de dívida do
  Ponytail, EV-P34), com timeout de 2 s; sem raiz, `null`;
- `atividade`: 84 dias (12 semanas) de minutos de agente por dia.

"Minutos de agente" = soma, por sessão, do intervalo entre chamadas consecutivas, com cada
intervalo limitado a 5 min (pausa longa não conta como trabalho). É a mesma ideia do "agent
time" do Ponytail, calculada a partir de `calls` em vez de medida na faixa.

Slug desconhecido → exit 2. Projeto sem tarefas → blocos vazios, sem erro.

### 2. Painel — `/monitor` no servidor do Canvas (fase 1)

- **Rotas:** `GET /monitor` (página) e `GET /api/monitor[?project=<slug>&days=30]` (o JSON
  acima, via `osforge-db`). Atualiza pelo SSE que já existe (`/api/events`) e, sem evento, a
  cada 60 s.
- **Estrutura, a do quadro do Ponytail** (barra lateral + área principal), com o conteúdo do
  OSForge:
  - **barra lateral:** "Todos os projetos" no topo; depois os projetos agrupados por status
    (Em andamento, Backlog, Pausados, Concluídos, Sem cadastro), cada um com o ponto de cor,
    o nome e um contador (tarefas abertas); selo ⛔ quando há bloqueio aberto; alternância de
    tema no rodapé;
  - **"Todos os projetos":** quatro KPIs com sparkline e variação contra o período anterior
    (sessões, tempo de agente, custo, tokens); gráfico de área empilhado por projeto, com
    seletor de métrica e legenda clicável; tabela de projetos (status, fase, barra de
    progresso, tarefas abertas, bloqueios, sinais, última atividade, custo no período), com
    busca; mapa de atividade de 12 semanas; saúde (chamadas sem projeto, projetos sem raiz,
    pastas sem cadastro com o comando para cadastrar);
  - **projeto selecionado:** cabeçalho com status, fase atual e % geral; os mesmos quatro
    KPIs; fases como barras; quadro de tarefas em quatro colunas (A fazer, Em andamento,
    Bloqueadas, Feitas recentes) com selo de prioridade e dependência; bloqueios com idade;
    decisões recentes; qualidade (testes, chamadores abertos, duplicatas, atalhos sem gatilho);
    gráfico empilhado por modelo; tabela de sessões; mapa de atividade.
  - seletor de período 7d / 30d / 90d; a seleção fica no endereço (`#p=<slug>&d=30`), então
    dá para guardar o link de um projeto.
- **O que muda do Ponytail:** os dados vêm do contrato, não de CSV embutido; o cartão de
  compartilhamento e a marca do Ponytail saem; textos em português; o "✓ testes" vem do G-3
  (código de saída), não de regex.
- **Mantém o que o Canvas já garante:** só `127.0.0.1`, validação de Origin (B-020), nenhum
  recurso externo (fonte do sistema, SVG inline), tema claro e escuro, legível no celular.
  Nomes vindos do banco entram só como texto (`textContent`), nunca como HTML.
- **Licença:** CSS e funções de desenho derivados de `board.ts` levam o aviso MIT no cabeçalho
  do arquivo e em `THIRD_PARTY_NOTICES`.

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
- Botões: Painel (abre `http://127.0.0.1:4242/monitor#p=<slug>`), Review, Audit, Copiar status.
- Nada é calculado dentro do desenho. Sem dados do projeto, mostra só consumo e janela. Com
  `OSFORGE_MONITOR_BAND=off`, devolve `next(e)`.
- O deploy confere a versão do Claude Code. Abaixo da mínima testada, não liga a faixa e
  avisa; o painel continua.

### 4. Painel lateral (fase 3, opcional)

A mesma informação num `Pane` (`$.ui.open`), aberto por um comando `/osforge-monitor`.

## Arquivos

`scripts/osforge-db.py` (`monitor`, `set-project-status`) · `scripts/lib/monitor_discover.py`
**(NOVO)** · `scripts/canvas/server.ts` (duas rotas) · `scripts/canvas/monitor.html` **(NOVO)** ·
`mods/osforge-monitor/` **(NOVO)** · `deploy.sh` (copiar o mod, `env`, versão mínima) ·
`scripts/osforge-state.py` (estado do mod) · `tests/test-monitor.sh` **(NOVO)** ·
`tests/test-canvas-feedback.sh` · `THIRD_PARTY_NOTICES`.

## Testes (offline)

1. Portfólio contra banco semeado (projetos em cada status, um com status antigo fora da lista):
   agrupamento, contagens, % por projeto, bloqueios, série por dia e custo batem com a conta à
   mão; `archived` fora sem `--all`; esquema validado.
2. Projeto: % por fase, contagem por status, dependências abertas, bloqueio com idade, sessões
   e minutos de agente (com o teto de 5 min) batem com a conta à mão.
3. Projeto sem tarefas → blocos vazios, sem erro; slug desconhecido → exit 2.
4. `--discover` contra um `HOME` falso com transcripts sintéticos: pasta não cadastrada aparece
   em `sem_cadastro`; projeto sem raiz recebe `raiz_sugerida`; transcript malformado é ignorado;
   nada gravado no banco.
5. `set-project-status` aceita os cinco valores e recusa outro (exit 2).
6. 50 mil chamadas sintéticas → portfólio e projeto < 200 ms cada (sem `--discover`).
7. Canvas: `/api/monitor` só em `127.0.0.1`; Origin estranho → 403; projeto inexistente → 404;
   o HTML não carrega nada externo e não usa `innerHTML` com dado do banco.
8. Mod: `claude plugin validate` e `claude plugin test` verdes; o teste do módulo **roda no CI**
   (o do Ponytail não roda — EV-P18); desenho sem chamada de processo; `OSFORGE_MONITOR_BAND=off`
   → `next(e)`.
9. Deploy: mod copiado, `env` mesclado sem tocar nas suas chaves, `--uninstall` remove os dois,
   `--doctor` limpo; versão abaixo da mínima → faixa não ligada, aviso emitido.

## Aceite

Testes verdes; o painel mostra os 9 projetos atuais, agrupados, com números que conferem com
`osforge-db board`; o detalhe de cada projeto abre pela barra lateral e pelo link; a faixa
aparece no terminal e no app de desktop do Mac de trabalho (Claude Code 2.1.307, EV-M-P03);
nenhuma chamada nova de rede.
