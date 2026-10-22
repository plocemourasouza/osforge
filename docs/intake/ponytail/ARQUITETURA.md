# Arquitetura proposta: comportamento, guardas e monitor de andamento

Este documento responde a três perguntas:

- como trazer do Ponytail o que melhora o **comportamento** do agente;
- como dar ao OSForge um **monitor visual** do andamento de cada projeto;
- como fazer as duas coisas sem criar um segundo sistema ao lado do primeiro.

A cobertura item a item está em [`COBERTURA.md`](COBERTURA.md); as evidências, em
[`EVIDENCIAS.md`](EVIDENCIAS.md).

## Princípios

1. **Uma fonte de verdade.** O estado do projeto e da sessão mora no `osforge-db`, como já
   moram tarefas, fases, decisões, bloqueios e chamadas (EV-O-P15, EV-M-P02). Nada de um
   segundo livro-razão em CSV, como o do Ponytail (EV-P14).
2. **O modelo recebe o sinal na hora em que pode agir.** O Ponytail mostra "chamadores
   abertos" e "duplicata?" só para o humano, na faixa (EV-P33). Aqui o mesmo sinal vai para
   o modelo no próprio Edit (EV-C-P06) e, depois, para o monitor.
3. **O visual nunca é o único canal.** Sem a faixa, nada se perde: o modelo já foi avisado e
   o painel mostra o resto.
4. **API instável fora do caminho crítico.** A API de módulos de UI é *early access* e muda
   entre versões (EV-C-P01). A faixa é opcional, desligável e só lê. Guardas e regras usam
   hooks clássicos, que o OSForge já testa por contrato.
5. **Determinístico e testável offline.** Toda peça nova tem suíte que fica vermelha sem ela.
6. **Medir antes de adotar** (ADR-015). Regras passam pela r3; guardas passam por um período
   em modo sombra; o monitor passa por testes de correção dos números.
7. **Local.** Só `127.0.0.1`, nenhum dado sai da máquina, nenhum texto de prompt é gravado.

## Visão geral

```
                ┌──────────────── Claude Code: sessão principal e subagentes ────────────────┐
 Camada 1       │ CLAUDE.md → SKILLS.md (resumo sempre carregado; chega a 270/277 subagentes  │
 regras         │ que codam — EV-M-P01) + skills sob demanda: coding-guidelines, code-review, │
                │ repo-audit                                                                  │
                └───────┬───────────────────────────────────────────────┬─────────────────────┘
                        │ Edit / Write / MultiEdit                       │ Bash (comando de teste)
 Camada 2               ▼                                                ▼
 guardas        hooks/quality-guard.py (PostToolUse) ─────────────────────────────────┐
                 ├─ G-1 chamadores abertos ─┐                                         │
                 ├─ G-2 duplicata provável ─┼─→ additionalContext ao modelo (no ato)  │
                 └─ G-3 estado dos testes ──┘                                         │
                                            └─→ osforge-db: tabela signals ◄──────────┘
 Camada 3       osforge-db (SQLite) ◄── session-save (calls, usage) · tasks · phases · decisions · blockers
 monitor               │  contrato único: `osforge-db monitor [<slug>] --json`
                       ├──→ Painel: servidor do Canvas, 127.0.0.1:4242/monitor (SSE ao vivo)
                       └──→ Faixa: mod `osforge-monitor` (AbovePrompt) + $.session.usage()
                                  (custo, contexto, janela de 5 h — EV-C-P03)
```

## Camada 1 — regras

As regras novas do Ponytail entram onde já chegam ao modelo. O canal do OSForge funciona: o
resumo de `SKILLS.md` estava em **270 dos 277** subagentes que escreveram código. A skill
`coding-guidelines` inteira, em só **10** (EV-M-P01). Por isso a injeção em `SubagentStart`
do Ponytail (EV-P11) não traz nada novo: o que falta é **conteúdo**.

- P-01 escada da solução + nunca cortar + atalho declarado → corpo de `coding-guidelines`, e
  uma oração (~40 tokens) no resumo de `SKILLS.md` ([SPEC-P01](SPEC-P01-escada-da-solucao.md)).
- P-02 `code-review` com código conectado ([SPEC-P02](SPEC-P02-review-codigo-conectado.md)).
- P-03 `repo-audit` sob demanda, com o livro de atalhos ([SPEC-P03](SPEC-P03-repo-audit.md)).
- Mapa do repositório (item 18 da cobertura): braço extra na r3; só vira injeção de sessão se
  ganhar.

Medição: rodada r3 do eval de resultado ([MEDICAO-r3](MEDICAO-r3.md)).

## Camada 2 — guardas durante a edição

Um hook novo, `hooks/quality-guard.py`, registrado em `PostToolUse` para `Edit|Write|MultiEdit`
e para `Bash`. Spec: [SPEC-P04](SPEC-P04-guardas-de-edicao.md).

| Guarda | Gatilho | O que faz | Para quem |
|---|---|---|---|
| G-1 chamadores abertos | Uma definição exportada sumiu ou mudou de nome no arquivo editado | `git grep -nw` do nome antigo; se ainda há chamadas, lista até 5 `arquivo:linha` | Modelo (`additionalContext`) + `signals` |
| G-2 duplicata provável | Uma definição nova tem o mesmo nome normalizado de uma existente em outro arquivo | Aponta a existente | Modelo + `signals` |
| G-3 estado dos testes | Bash roda o script de teste do `package.json`; ou um Edit toca código depois disso | Grava passou / falhou / desatualizado | `signals` (e o monitor) |

O que muda em relação ao Ponytail:

- o aviso chega ao **modelo**, não só ao humano;
- o teste é reconhecido pelo script do `package.json`, não por uma regex de comando;
- o estado desatualiza para qualquer arquivo de código do projeto, não só em seis linguagens;
- G-2 ignora nomes genéricos (`get`, `handle`, `render`…), numa lista como a `GENERIC` que o Ponytail mantém.

**Adoção em dois passos:**

1. **Modo sombra** por duas semanas: grava os sinais e não injeta nada.
2. Liga a injeção se a taxa de alarme falso medida nos próprios sinais ficar abaixo do limite
   da spec.

## Camada 3 — monitor de andamento

Um contrato de dados e duas vistas. Spec: [SPEC-P05](SPEC-P05-monitor.md).

**Contrato:** `osforge-db monitor [<slug>] [--days 30] --json` — sem slug, o portfólio de todos os projetos; com slug, o detalhe (rev. 3 da P-05). Devolve:

| Bloco | Conteúdo | Fonte |
|---|---|---|
| `projeto` | nome, raiz, fase atual | `projects`, `phases`, `state` |
| `andamento` | tarefas por status e prioridade, por fase e onda; dependências bloqueando; % concluído por fase | `tasks`, `phases` |
| `bloqueios` | abertos, há quanto tempo, esperando o quê | `blockers` |
| `decisoes` | as últimas N, por categoria | `decisions` |
| `consumo` | custo equivalente, tokens, chamadas por dia e modelo; orquestrador × subagente | `calls` (B-028) |
| `janela` | % da janela de 5 h e de 7 dias, horário de reset | `quota.json` (B-027) |
| `qualidade` | estado dos testes, chamadores abertos, duplicatas, atalhos sem gatilho | `signals` (Camada 2) |
| `saude` | chamadas sem projeto identificado (hoje 25% — EV-M-P02), cobertura de embeddings | `calls`, `vec-status` |

**Painel (fase 1):** a página `/monitor` no servidor do Canvas, que já existe, já sobe sozinho
no `SessionStart`, já escuta só em `127.0.0.1` e já tem SSE em `/api/events` (EV-O-P14). Mostra:

- seletor de projeto;
- as fases com barra de progresso;
- quadro de tarefas (pendente, em andamento, bloqueada, feita), com dependências;
- bloqueios e decisões recentes;
- consumo por dia e por modelo, com a janela de 5 h;
- sinais de qualidade;
- mapa de atividade de 12 semanas, a parte boa do painel do Ponytail (EV-P37).

Funciona em qualquer superfície que abra um navegador e não depende da API de UI.

**Faixa (fase 2):** o mod `osforge-monitor`, um módulo de hooks de função (`AbovePrompt`,
EV-C-P04), entregue pelo deploy do OSForge numa pasta própria e ligado por
`CLAUDE_CODE_PLUGIN_DIRS` no bloco `env` do `settings.json`, que o deploy já gerencia
(EV-C-P02, EV-O-P16). Uma linha mostra:

- projeto e fase;
- tarefa em andamento;
- tarefas feitas sobre o total;
- bloqueios abertos;
- custo e tempo da sessão;
- janela de 5 h e contexto, lidos de `$.session.usage()`. Isso substitui o desvio pelo
  statusline previsto em L-01 (D-1).

Alertas aparecem quando existem: chamadores abertos, testes desatualizados. Os botões são
Painel (abre `/monitor`), Review, Audit e Copiar status.

Lê um JSON em cache, renovado a cada `turn.complete`; nada roda dentro do desenho.

**Painel lateral (fase 3, opcional):** a mesma informação num `Pane`, ao lado do chat, para
quem prefere acompanhar sem sair do Claude Code.

## Alternativas consideradas

| Opção | O que é | A favor | Contra | Veredito |
|---|---|---|---|---|
| A | Instalar o Ponytail inteiro | Pronto hoje | Duas fontes de regras; ~1,2–1,5 mil tokens por sessão + ~3 KB por subagente; pede para editar o seu `settings.json`; segundo livro-razão; atualiza do marketplace sem versão fixa (EV-P10–P12, EV-P14) | Recusada |
| B | Ponytail só com a faixa (`PONYTAIL_DEFAULT_MODE=off` desliga as regras) | Faixa e painel prontos | Mostra **sessão**, não **projeto** (sem tarefas, fases, bloqueios); sinais só para o humano; "✓ testes" por regex; CSV paralelo ao `calls`; teste da faixa fora do CI (EV-P15, EV-P16, EV-P18) | Recusada como solução; ótima **referência de UX** (MIT) |
| C | OSForge nativo: Camadas 1–3 sobre o `osforge-db` | Uma fonte de verdade; o modelo recebe os sinais; andamento do projeto; testável; desligável peça por peça | Mais trabalho (5–9 dias) | **Recomendada** |
| D | Só o painel no Canvas | Nenhuma dependência da API de UI | Não aparece dentro do Claude Code | É a **fase 1** de C |

## Desempenho, falhas e segurança

| Peça | Orçamento | Se falhar |
|---|---|---|
| `quality-guard.py` | < 150 ms p95 por Edit; `git grep` só quando uma definição sumiu ou nasceu | Sai 0 em silêncio (contrato de hooks do OSForge) |
| `osforge-db monitor --json` | faixa (`--compact`) < 200 ms; detalhe < 400 ms e portfólio < 600 ms, em 50 mil chamadas | Painel mostra o erro; a faixa some |
| Faixa | Zero trabalho no desenho; 1 processo por turno | Hook pulado sozinho pelo motor; `OSFORGE_MONITOR_BAND=off` |
| Painel | Só `127.0.0.1`; mesmas regras de Origin do Canvas (B-020) | Sessão segue normal |

Nenhum texto de prompt ou de resposta é gravado. O nome da tarefa vem do que você mesmo
registrou em `tasks`.

## Esforço e ordem

| Ordem | Peça | Esforço | Chamadas pagas |
|---|---|---|---|
| 1 | B-031 preparar r3 (inclui o braço do mapa) | M | 0 |
| 2 | B-035 Camada 2 em modo sombra + tabela `signals` | M | 0 |
| 3 | B-036 contrato `monitor --json` + painel no Canvas | M | 0 |
| 4 | r3 (autorização) → B-032, B-033, B-034 conforme o resultado | P cada | 288–396 |
| 5 | Guardas ligadas ao modelo, se a sombra aprovar | P | 0 |
| 6 | B-037 faixa `osforge-monitor` | M | 0 |
| 7 | Painel lateral | P–M | 0 |

Total: 5 a 9 dias de trabalho, sem contar a espera da sombra.
