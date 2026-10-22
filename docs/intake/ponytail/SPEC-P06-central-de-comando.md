# P-06 · Central de comando: grupos por atividade, conversa com os agentes e disparo de ferramentas

**Pedido (2026-10-22, depois de usar a prévia do monitor):** destacar em tempo real os projetos
em que o Claude Code está atuando; separar os parados há mais de 24 h; mandar para um histórico
(a biblioteca de projetos) os parados há muito tempo ou os que foram segurados/arquivados; e ter
no painel uma conversa para orientar os agentes e disparar o Claude Code ou uma IDE.
**Decisões do Paulo:** histórico depois de **30 dias**; Claude Code **no Terminal e em segundo
plano**, e qualquer **IDE instalada** (Cursor, VS Code…); orientação entregue **na próxima
resposta** do agente; "rodando" = **sessão do Claude Code, Cursor/IDE aberto no projeto e servidor
de desenvolvimento**.
**Base:** P-05 rev. 3 (contrato `osforge.monitor.v1`, painel `/monitor`). **Chamadas pagas:** 0
para construir; a execução em segundo plano usa a assinatura só quando o Paulo dispara.

## 1. Grupos

| Grupo | Regra (a primeira que casa) |
|---|---|
| **Ativo agora** | Há sessão do Claude Code, janela de IDE ou servidor de desenvolvimento rodando na pasta do projeto (detecção ao vivo, §2). Vence qualquer outra regra |
| **Backlog** | `status = backlog` |
| **Histórico** | `status` em `paused`, `done`, `archived` (segurar, concluir, arquivar), ou nenhuma atividade há mais de 30 dias |
| **Em andamento** | Última atividade há menos de 24 h |
| **Aguardando** | Última atividade entre 24 h e 30 dias |

O contrato devolve `grupo_base` (tudo menos "Ativo agora", que depende do momento) e
`grupo_regra` (por que caiu ali). O painel sobrepõe a detecção ao vivo: ao vivo → "Ativo agora".
As pastas sem cadastro também recebem o selo ao vivo.

## 2. Detecção ao vivo — `osforge-db live --json`

Somente leitura, sem rede, ~100–300 ms. Três fontes, todas locais:

- **Claude Code:** processos `claude` e o diretório atual de cada um (`lsof -d cwd`). "Trabalhando
  agora" quando o transcript mais recente daquela pasta mudou nos últimos 2 minutos.
- **IDE:** o processo de extensões de cada janela do Cursor, do VS Code e derivados se chama
  `… Helper (Plugin): extension-host (user) <pasta>`. Uma janela aberta = uma pasta. Medido no
  Mac em 2026-10-22: duas janelas do Cursor, duas pastas, nomes exatos.
- **Servidor de desenvolvimento:** processos `next dev`, `vite`, `expo start`, `bun --hot`/`bun dev`,
  `npm|pnpm|yarn run dev|start`, `nodemon`, `uvicorn`, `manage.py runserver`, com o diretório atual
  dentro da pasta do projeto.

Pasta → projeto pela mesma regra dos hooks (raiz cadastrada → remote → nome da pasta). O painel
consulta a cada 10 s; o servidor guarda 5 s.

## 3. Conversa com os agentes (caixa de entrada)

- O Paulo escreve uma orientação no painel (pode ditar com o ditado do macOS; nada sai da máquina).
- `osforge-db inbox-add <slug> "<texto>"` grava na tabela `inbox` e cria a marca
  `~/.osforge/inbox/<slug>`.
- **Hook `inbox-deliver`** em `PostToolUse` (qualquer ferramenta), `UserPromptSubmit` e
  `SessionStart`: sem marca nenhuma, sai em ~30 ms sem chamar nada. Com marca do projeto da sessão,
  pega as pendentes (`inbox-take`, atômico), entrega como `additionalContext` e grava qual sessão
  recebeu. Subagentes não recebem (`agent_id` no payload): a orientação é para quem conduz.
- Texto entregue: `[Orientação do Paulo pelo painel do OSForge, 14:32] <texto>` — o modelo trata
  como instrução do usuário, porque é.
- O painel mostra pendente → entregue (sessão, hora). Sem sessão ativa, fica pendente até a
  próxima; o painel oferece abrir uma com a mesma orientação.

## 4. Disparo de ferramentas

| Ação | Como | Gasto |
|---|---|---|
| **Claude no Terminal** | Arquivo `~/.osforge/launch/<id>.command` (0700) com `cd <raiz> && exec claude '<orientação>'`, aberto com `open -a Terminal`. Sessão interativa normal | o que o Paulo usar |
| **Claude em segundo plano** | `claude -p '<orientação>' --output-format stream-json --verbose` na raiz, sem shell; saída em `~/.osforge/runs/<id>.jsonl`; o painel mostra rodando → concluída/falhou, o resultado e o custo. Permissões: as do projeto; edições só com "permitir edições" marcado (`--permission-mode acceptEdits`) | dispara cota sem o Paulo olhar — por isso é sempre uma ação explícita |
| **Abrir em IDE** | `open -a "<IDE>" <raiz>`, só IDEs encontradas em `/Applications` e `~/Applications` | — |
| **Status** | Segurar (`paused`), Concluir (`done`), Arquivar (`archived`), Backlog, Reativar (`active`) | — |
| **Cadastrar** | Pasta sem cadastro → `upsert-project` com a raiz; projeto sem raiz → `bind-project` com a raiz sugerida | — |

No compositor, texto simples = orientação. Comandos: `/claude [texto]`, `/bg [texto]`,
`/abrir <ide>`, `/segurar`, `/arquivar`, `/concluir`, `/backlog`, `/reativar`. As execuções ficam
na tabela `runs` e aparecem na conversa do projeto.

## 5. Segurança

O servidor continua só em `127.0.0.1`. Toda rota que age: método POST, `Content-Type:
application/json` (um site de fora não manda isso sem um preflight que o servidor não responde),
Origin igual ao próprio servidor ou ausente, Host da própria porta (contra DNS rebinding). A raiz
de um projeto **nunca vem do navegador**: vem do banco (`root_path`) ou da sugestão que o próprio
servidor recalcula. Nada passa por shell: `Bun.spawn` com argumentos; o `.command` do Terminal
leva a raiz e o texto com aspas simples escapadas. Orientação até 4.000 caracteres.

## 6. Dados

Tabelas novas (migração idempotente): `inbox` (`id, ts, project_id, text, status
pendente|entregue|cancelada, delivered_at, delivered_session, via`) e `runs` (`id, ts,
project_id, kind terminal|background|ide, tool, prompt, status, pid, ended_at, log_path, result,
cost_usd`). Comandos: `live`, `inbox-add`, `inbox-take`, `inbox`, `inbox-cancel`, `run-add`,
`run-update`, `runs`. `monitor` ganha `grupo_base`, `grupo_regra`, `inbox_pendentes` e, no
detalhe, `conversa` (orientações e execuções em ordem).

## 7. Testes (offline)

1. Grupos: cada regra da tabela, na ordem, contra banco semeado com datas controladas.
2. `live` com `ps`/`lsof` falsos (fixtures): claude, IDE e servidor mapeados ao projeto certo;
   pasta sem cadastro aparece; processo fora de projeto ignorado.
3. Caixa de entrada: add → marca criada; take atômico (duas sessões, uma recebe); cancel;
   marca removida quando não há pendentes.
4. Hook: sem marca → silêncio e sem subprocess; com marca → `additionalContext` no evento certo;
   subagente → silêncio; contrato de hooks.
5. Servidor: POST sem JSON → 415; Origin/Host estranhos → 403; projeto sem raiz → 409; o
   `.command` gerado tem aspas certas para textos com `'`, `$()`, crase; IDE fora da lista → 400;
   `claude` e `open` falsos registram os argumentos esperados; execução em segundo plano termina
   como concluída com o custo do evento `result`.
6. Painel: smoke no navegador quando houver Playwright.

## Limites conhecidos

- A orientação chega na próxima ferramenta ou mensagem: um agente parado esperando o Paulo só a
  vê quando houver nova mensagem ou nova sessão.
- A entrega depende do hook instalado (deploy). Na prévia, o painel grava e mostra, mas nenhuma
  sessão recebe até o hook estar no `settings.json`.
- Terminal: abre no Terminal do macOS. Warp e outros ficam para depois (o `.command` não roda
  neles do mesmo jeito).
