# Apêndice de auditoria e evidências — OSForge × ECC

> **Este documento é um retrato**, congelado no SHA auditado (`d87a9bf`) de 2026-09-18. Os
> defeitos E-A* descritos aqui **não** são o estado atual do repositório: a maioria foi
> corrigida depois, cada um com teste que fica vermelho sem a correção. O estado corrente
> está em [`BACKLOG-EVOLUCAO.md`](BACKLOG-EVOLUCAO.md) (painel no topo) e no `CHANGELOG.md`.
> Alterar as linhas abaixo apagaria a evidência que justificou cada mudança — elas ficam.

## 1. Snapshots

| | Projeto A — OSForge | Projeto B — ECC |
|---|---|---|
| URL canônica | https://github.com/plocemourasouza/osforge | https://github.com/affaan-m/ECC (a URL `…/affaan-m/ecc` redireciona para cá) |
| Branch | `main` | `main` |
| SHA | `d87a9bfc2058df233d30a2637fe252efb3256894` | `dd6ee538aee0f548d4a6b520118f875431fd749e` |
| Data do commit | 2026-09-10T04:06:09Z | 2026-09-17T14:04:06-04:00 |
| Versão | 5.0.0 (`VERSION`) | 2.2.1 (`VERSION`) |
| Arquivos versionados | 721 | 3.718 |
| Data da auditoria | 2026-09-17/18 (UTC) | idem |

Os dois SHAs são exatamente os da referência de preparação. O clone do ECC é raso (`--depth 1`), então histórico e autoria por `git log` não foram verificados. `sources/` do OSForge é gitignored (ADR-009) e não existe no checkout: nada do que está lá foi lido.

## 2. Método e isolamento

- Checkouts limpos em diretório de trabalho temporário, fora de qualquer ambiente pessoal. `git status --porcelain` vazio nos dois ao final.
- Toda execução usou cópias dos repositórios e `HOME`, `TMPDIR` e diretórios de estado apontados para um sandbox. Nada foi instalado globalmente; nenhum deploy tocou `~/.claude`, `~/.cursor` ou `~/.claude.json` reais.
- Seis frentes paralelas de leitura e execução (hooks e segurança; estado e memória; instalação, CI e portabilidade; skills e contexto; orquestração, planejamento e evals; cenários e licenças). As evidências das propostas prioritárias foram relidas e reexecutadas por mim (coluna **Quem** = P).
- O conteúdo dos repositórios foi tratado como objeto de análise. Nenhuma instrução encontrada nos arquivos foi seguida.

### Desvios do escopo que você definiu

1. **Uma chamada paga a modelo aconteceu.** Um subagente executou `scripts/hooks/session-end.js` do ECC depois de apenas fazer grep nele. O script chamou `claude --model haiku -p` (`scripts/lib/llm-summary.js:153`) sobre um transcript falso de 5 linhas. Foi uma chamada ao Haiku, em HOME isolado. Depois disso, todas as execuções do ECC usaram `ECC_SKIP_LLM_SUMMARY=1` e um `claude` falso no início do PATH; o log do falso ficou vazio. O achado que isso produziu é relevante para você: **o ECC chama modelo de dentro de hooks de Stop e PreCompact sem pedir.**
2. **Escritas fora do sandbox, no `/tmp` do contêiner da auditoria** (não na sua máquina): `/tmp/agent-hooks.log` (caminho fixo em `hooks/protect-tests.sh:34` e `hooks/notify-done.sh:27`) e `/tmp/osforge-skill-tests/` (caminho fixo do harness).
3. **`rsync` não existe no sandbox.** O primeiro deploy real abortou em `deploy.sh:279`. As execuções seguintes usaram um substituto em Python que emula `rsync -a --delete --exclude`. Os resultados que dependem de `--delete` (E-A29) valem para a semântica documentada do rsync, não para o binário real.
4. **Da rodada anterior:** a revisão 2 desta análise ocupou `docs/ANALISE-COMPARATIVA-ECC.md` por um dia; foi substituída pela revisão 3, que é o relatório ao lado.

## 3. Tabela de evidências

Cada linha abaixo é citada no relatório e no backlog pelo ID. **Escada:** DOC = documentado · IMPL = implementado · WIRED = conectado ao fluxo de execução · TEST = coberto por testes inspecionados · EXEC = validado por execução nesta auditoria. **Quem:** P = reli/reexecutei pessoalmente nesta rodada · S = subagente leu/executou com referência de linha · P+S = ambos.

| ID | Permalink | Escada | Quem | O que a evidência mostra |
|---|---|---|---|---|
| E-A01 | [`hooks/scan-secrets.sh`:6](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/scan-secrets.sh#L6) | WIRED · EXEC | P+S | Lê `command` na raiz do JSON (formato Cursor). Com payload do Claude Code (`tool_input.command`) devolve sempre `allow`. Executado: `rm -rf ~` → `{"continue": true, "permission": "allow"}`. |
| E-A02 | [`hooks/hooks-claude-code.json`:51-69](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/hooks-claude-code.json#L51-L69) | WIRED | P | PreToolUse tem só o matcher `Bash`, com `scan-secrets.sh` e `gateguard.py`. Não há matcher para Edit/Write. |
| E-A03 | [`deploy.sh`:323-327](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L323-L327) | IMPL | S | O mesmo `scan-secrets.sh` é copiado para `~/.claude/hooks`; `deploy.sh:680-684` copia para `~/.cursor/hooks`. |
| E-A04 | [`hooks/scan-secrets.sh`:19](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/scan-secrets.sh#L19) | IMPL · EXEC | P+S | Regex de secrets cobre 5 nomes de variável; `ghp_…`, `AKIA…`, `sk-…` passam mesmo no formato Cursor (executado pelo subagente). |
| E-A05 | [`hooks/gateguard.py`:385-399](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/gateguard.py#L385-L399) | WIRED · TEST · EXEC | P+S | `classify_prompt` concede `grant` sem checar negação pendente. Executado: sessão nova, prompt `ok`, depois `git reset --hard HEAD~10` → permitido; `denials.log` registra `GRANT-GRANT` / `GRANT-ALLOW`. |
| E-A06 | [`hooks/gateguard.py`:325-329](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/gateguard.py#L325-L329) | IMPL · EXEC | P+S | Frases de autorização incluem `go ahead`, `proceed`, `do it` em qualquer ponto da frase. Executado pelo subagente: "please proceed with the refactor of the header" → grant. |
| E-A07 | [`hooks/gateguard.py`:826-840](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/gateguard.py#L826-L840) | WIRED · EXEC | P+S | Marca o comando como checado e só então nega. Executado: mesma chamada repetida → permitida sem grant (retry cego). Falha fechada se o estado não grava (L831-839). |
| E-A08 | [`hooks/gateguard.py`:749-800](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/gateguard.py#L749-L800) | IMPL (não conectado) | S | Gates de Edit/Write/MultiEdit existem no código, mas nenhum matcher os aciona (ver E-A02). |
| E-A09 | [`claude-code/CLAUDE.md`:240-246](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/claude-code/CLAUDE.md#L240-L246) | DOC | S | A prosa diz que, negado um comando, o agente deve pedir confirmação ao usuário; o código permite o retry direto (E-A07). |
| E-A10 | [`hooks/route-guard.py`:126-158](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/route-guard.py#L126-L158) | WIRED · EXEC | P+S | Bloqueia 1x resposta acionável sem linha de rota e skill declarada sem evidência de carga. Executado pelo subagente com transcript sintético. |
| E-A11 | [`hooks/route-guard.py`:115-118](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/route-guard.py#L115-L118) | IMPL · EXEC | S | Evidência de carga é regex sobre qualquer input de ferramenta: `Bash: echo skills/x/SKILL.md` e um prompt de Task com o nome da skill contam como carga. `@agente-inexistente` e `model: gpt-99` passam. |
| E-A12 | [`hooks/protect-tests.sh`:34](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/protect-tests.sh#L34) | WIRED · EXEC | S | Só grava uma linha em `/tmp/agent-hooks.log`; nada chega ao modelo. |
| E-A13 | [`hooks/notify-done.sh`:25](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/notify-done.sh#L25) | WIRED · EXEC | S | Só dispara quando `stop_hook_active` é verdadeiro (lógica invertida no Claude Code). Executado: 0 linhas com false, 1 com true. |
| E-A14 | [`hooks/observe-capture.py`:105](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/observe-capture.py#L105) | WIRED · EXEC | P+S | Guarda os primeiros 120 caracteres do comando Bash sem limpar segredos. Executado: `curl -H "Authorization: Bearer sk-ant-…"` ficou na coluna `context`. |
| E-A15 | [`scripts/osforge-db.py`:1391](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/scripts/osforge-db.py#L1391) | IMPL · EXEC | P+S | `avg_conf = 0.5 + min(0.3, len(obs) * 0.05)`: confiança é função só da contagem. Chave do cluster = primeira palavra restante (L1365-1368). Executado: 6× `when running git` → `git-agent, 80%`. |
| E-A16 | [`scripts/osforge-db.py`:1500](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/scripts/osforge-db.py#L1500) | IMPL · EXEC | P+S | Único DML sobre `instincts` é um UPDATE. Nenhum INSERT no repositório: `evolve` não cria instinct; `list-instincts` fica vazio após `evolve` (executado). |
| E-A17 | [`scripts/osforge-db.py`:1555](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/scripts/osforge-db.py#L1555) | IMPL · EXEC | P+S | A linha 1555 remove `--scope=` dos args antes de a linha 1569 lê-los: `list-instincts --scope=global` é no-op (executado). |
| E-A18 | [`skills/evolve/SKILL.md`:19-36](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/skills/evolve/SKILL.md#L19-L36) | DOC | S | O consumidor do `evolve` é um humano que edita `skills/` e roda `./deploy.sh`. Nenhum hook lê `list-instincts` (grep: só `skills/evolve/SKILL.md` e `INDICE-SKILLS.json`). |
| E-A19 | [`hooks/session-resume.sh`:36-40](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/session-resume.sh#L36-L40) | WIRED · EXEC | P+S | Slug = `basename(pwd -P)` em minúsculas com `_`→`-`. Executado: dois diretórios `My_Proj` distintos recebem o mesmo resume; subdiretório fica sem resume. |
| E-A20 | [`hooks/observe-capture.py`:117-121](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/observe-capture.py#L117-L121) | WIRED · EXEC | P+S | Slug = basename cru (sem normalizar). Observações e resume podem cair em chaves diferentes para o mesmo projeto. |
| E-A21 | [`hooks/session-resume.sh`:72-80](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/session-resume.sh#L72-L80) | WIRED · EXEC | P+S | Injeta o resume literal + board cross-project (`head -40`), sem guarda e sem teto. Executado: `IGNORE PREVIOUS INSTRUCTIONS…` gravado no resume foi injetado literalmente; tarefa de outro projeto apareceu no contexto. |
| E-A22 | [`hooks/session-save.py`:106-109](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/session-save.py#L106-L109) | WIRED | P+S | Lê as PRIMEIRAS 2000 linhas do transcript e para; em sessão longa as "últimas 8 mensagens" vêm do início. |
| E-A23 | [`hooks/session-save.py`:138-140](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/hooks/session-save.py#L138-L140) | WIRED · EXEC | S | Persiste a 1ª linha (≤200 chars) das mensagens do usuário sem limpar segredos. Executado: `sk-ant-FAKESECRET…` gravado e reinjetável. |
| E-A24 | [`scripts/osforge-db.py`:596-601](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/scripts/osforge-db.py#L596-L601) | IMPL · EXEC | S | `search-hybrid --project=demo` devolve decisão de outro projeto: a lista vetorial não é filtrada por projeto; `_qdrant_search` ignora `project` (L382-404). |
| E-A25 | [`scripts/osforge-db.py`:802-815](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/scripts/osforge-db.py#L802-L815) | IMPL · EXEC | S | Tabela `tasks` sem colunas model/agent/skills/files/done-when/verify. Executado: `add-task --depends=99,banana` aceito; tarefa de wave 2 marcada `done` com dependência pendente. |
| E-A26 | [`scripts/osforge-db.py`:85-88](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/scripts/osforge-db.py#L85-L88) | IMPL · EXEC | P+S | `db_path` fixa em `$HOME/.osforge`; a variável `OSFORGE_DB` documentada em `observe-capture.py:28` nunca é lida. |
| E-A27 | [`deploy.sh`:125-137](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L125-L137) | WIRED · EXEC | P+S | `_is_managed` = substring `/.claude/hooks/`; o laço só itera eventos do repo. Executado em HOME isolado: hook do usuário em `~/.claude/hooks/my-own.sh` foi desregistrado; entrada obsoleta de evento ausente sobreviveu. |
| E-A28 | [`deploy.sh`:87-94](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L87-L94) | WIRED · EXEC | P+S | `copy_dir` copia só arquivos, sem backup. Executado: `agents/backend-engineer.md` do usuário sobrescrito sem backup; `triage-rules.md`, `plan-templates/` e `delegation-brief.md` não são deployados. |
| E-A29 | [`deploy.sh`:264-281](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L264-L281) | WIRED · EXEC (shim de rsync) | P+S | `rsync -a --delete` espelha o core. Executado: `~/.claude/skills/user-skill/` apagado; skill instalada com `install-skill.sh --global` apagada no deploy seguinte. |
| E-A30 | [`deploy.sh`:55-65](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L55-L65) | WIRED · EXEC | P+S | Backup por basename + timestamp de 1 s, chamado 2× para `settings.json` (L103, L155). Executado: o backup sobrevivente já continha hooks do OSForge; o original ficou irrecuperável. |
| E-A31 | [`deploy.sh`:359-366](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L359-L366) | WIRED · EXEC | P+S | Abre `~/.claude.json` sem guarda e fora do gate de dry-run. Executado: em HOME novo, `--dry-run` e deploy real saem com erro antes de `deploy_osforge_db`. |
| E-A32 | [`deploy.sh`:675](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L675) | WIRED · EXEC | P+S | Única cópia de `rules/` está em `deploy_cursor`. Após deploy isolado não existe `~/.claude/rules`. |
| E-A33 | [`deploy.sh`:160-166](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L160-L166) | WIRED · EXEC | P+S | Só três chaves `_…` são removidas; `_measured` e `_why_true_and_not_unset` vazam para o `settings.json` vivo (executado). |
| E-A34 | [`deploy.sh`:709-727](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/deploy.sh#L709-L727) | WIRED · EXEC | S | Preflight `_generate_manifest.py --check` aborta com manifesto defasado. Ponto cego: edição em description de skill core ou fora dos 78 primeiros caracteres não é detectada. |
| E-A35 | [`README.md`:36](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/README.md#L36) | DOC | P | "177 skills in a ~12K-token base". Soma de arquivos (bytes/4) dá ≈21,5k; o próprio `docs/ANALISE-COMPARATIVA-MATTPOCOCK.md:207-221` fala em ~18k. |
| E-A36 | [`claude-code/CLAUDE.md`:75](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/claude-code/CLAUDE.md#L75) | DOC | P+S | "~64 core skills" contra 47 entradas em `claude-code/skills-core.txt`. |
| E-A37 | [`claude-code/CLAUDE.md`:221](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/claude-code/CLAUDE.md#L221) | DOC | P+S | `ENABLE_TOOL_SEARCH=auto` contra `"true"` em `claude-code/settings-base.json:5`. |
| E-A38 | [`claude-code/CLAUDE.md`:140](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/claude-code/CLAUDE.md#L140) | DOC | P | Plano sem Roster/User stories/Task manifest é incompleto "even for a single-file change". A válvula de escape está em `rules/plan-mode.mdc:15`, que só vai para o Cursor. |
| E-A39 | [`CLAUDE.md`:10](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/CLAUDE.md#L10) | DOC | P+S | "There is no build, lint, or test suite", enquanto as linhas 29-30 do mesmo arquivo listam comandos de teste e `tests/` tem 3 scripts (todos passam: 26/26, 67/67, 23/23). |
| E-A40 | [`agents/orchestrator/AGENT.md`:126-137](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/agents/orchestrator/AGENT.md#L126-L137) | DOC | P+S | Manda carregar `./triage-rules.md` e `./plan-templates/{triage}.md`, que o deploy não copia (E-A28). `always-active: true` (L9) não é esquema de agente do Claude Code. |
| E-A41 | [`agents/validator.md`:9-18](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/agents/validator.md#L9-L18) | IMPL | S | `tools: allowed: - read_file` não é esquema do Claude Code. 9 de 26 agentes declaram `tools`; o validador do ECC aplicado aos agentes do OSForge acusa 41 erros (executado). |
| E-A42 | [`skills/quality/adversarial-review/SKILL.md`:85-88](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/skills/quality/adversarial-review/SKILL.md#L85-L88) | DOC | P+S | "HALT if zero findings → suspicious" e "findings < 10 → second pass": cota de achados, que induz falso positivo. |
| E-A43 | [`skills/osforge-canvas/SKILL.md`:99-113](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/skills/osforge-canvas/SKILL.md#L99-L113) | DOC | S | A volta do feedback ao agente é prosa ("leia o arquivo no próximo turno"); o hook automático está em "v2 backlog (deferred)" (L133-137). |
| E-A44 | [`scripts/canvas/server.ts`:176-196](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/scripts/canvas/server.ts#L176-L196) | IMPL · EXEC | P+S | Validação só do envelope (`artifactId`, `revision` numérico). Executado: feedback para artefato inexistente, `revision:-7`, `action:"launch-missiles"`, Origin estranho → `{"ok":true}`. |
| E-A45 | [`scripts/test-orchestrator-routing.sh`:97-102](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/scripts/test-orchestrator-routing.sh#L97-L102) | IMPL | P+S | Sem `--model`, 1 execução por caso, contra o `~/.claude` vivo. A dimensão agente passa com menção `@nome` no texto (`scripts/lib/harness-assertions.sh:119-134`). |
| E-A46 | [`skills/skill-creator/scripts/run_eval.py`:266-268](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/skills/skill-creator/scripts/run_eval.py#L266-L268) | IMPL (não conectado) | P+S | Já existe em A um eval de trigger com `should_trigger` verdadeiro/falso, `--runs-per-query` (padrão 3) e `--model`. Nada em `scripts/`, `tests/` ou `deploy.sh` o referencia. |
| E-A47 | [`claude-code/skills-core.txt`:8-19](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/claude-code/skills-core.txt#L8-L19) | DOC · EXEC | S | Critério de admissão no core. Integridade executada: 47 entradas, 0 sem `SKILL.md`, 0 colisões de basename; manifesto 130/130, 0 ponteiros pendentes. |
| E-A48 | [`.out-of-scope/claude-code-plugin-packaging.md`:5-12](https://github.com/plocemourasouza/osforge/blob/d87a9bfc2058df233d30a2637fe252efb3256894/.out-of-scope/claude-code-plugin-packaging.md#L5-L12) | DOC | P+S | Empacotamento como plugin rejeitado "while OSForge has a single user"; reabre se houver distribuição a terceiros. |
| E-B01 | [`scripts/lib/install/claude-settings.js`:528-545](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/install/claude-settings.js#L528-L545) | WIRED · TEST · EXEC | P+S | Merge de hooks por `id` em três vias; recusa sobrescrever entrada que o usuário alterou. Executado: "Refusing to overwrite Claude hook … has drifted", nada gravado. |
| E-B02 | [`scripts/lib/install/ownership-guard.js`:65-79](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/install/ownership-guard.js#L65-L79) | WIRED · TEST · EXEC | P+S | Arquivo existente e não registrado no install-state é pulado com aviso. Executado: `Skipped user-owned file ~/.claude/agents/architect.md`. |
| E-B03 | [`scripts/lib/install/ownership-guard.js`:50-51](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/install/ownership-guard.js#L50-L51) | WIRED · EXEC | P+S | "Recorded files remain updateable by reinstall/repair": reinstalar sobrescreve edição do usuário em arquivo gerenciado, sem aviso nem backup (executado). |
| E-B04 | [`scripts/lib/install-lifecycle.js`:882-915](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/install-lifecycle.js#L882-L915) | WIRED · TEST · EXEC | S | Uninstall só apaga arquivo cujo SHA-256 bate com o gravado. Executado: 701 removidos, 1 retido (o editado); arquivos e hooks do usuário sobreviveram. |
| E-B05 | [`.cursor/hooks/adapter.js`:24-26](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/.cursor/hooks/adapter.js#L24-L26) | WIRED · EXEC | P+S | `getPluginRoot()` = `__dirname/../..`; instalado num projeto, os scripts ficam em `.cursor/scripts/hooks`. Executado: hook delegado sai 0 sem fazer nada; `doctor` reporta OK. |
| E-B06 | [`scripts/hooks/plan-canvas-pending.js`:205-224](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/hooks/plan-canvas-pending.js#L205-L224) | WIRED · TEST · EXEC | P+S | Stop hook drena feedback pendente e devolve `{decision:'block'}`; respeita `stop_hook_active`; escopo por cwd; timeout de 1000 ms (L34). Executado ponta a ponta. |
| E-B07 | [`scripts/hooks/session-start.js`:683-688](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/hooks/session-start.js#L683-L688) | WIRED · EXEC | P+S | Resumo anterior embrulhado em "HISTORICAL REFERENCE ONLY — NOT LIVE INSTRUCTIONS"; teto de 8000 caracteres e top 6 instincts ≥0,7 (L35-39). |
| E-B08 | [`skills/continuous-learning-v2/scripts/detect-project.sh`:182-198](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/skills/continuous-learning-v2/scripts/detect-project.sh#L182-L198) | WIRED · EXEC | P+S | Id de projeto = sha256(remote normalizado)[:12], com fallback para o caminho. Executado: credenciais removidas da URL; subdiretório resolve para a raiz do repo. |
| E-B09 | [`skills/continuous-learning-v2/config.json`:4](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/skills/continuous-learning-v2/config.json#L4) | WIRED (desativado) | P+S | `observer.enabled: false` por padrão. O observer, quando ligado, roda `claude --model haiku --print` com `Read,Write` (`agents/observer-loop.sh:399`). |
| E-B10 | [`skills/continuous-learning-v2/agents/observer-loop.sh`:280](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/skills/continuous-learning-v2/agents/observer-loop.sh#L280) | IMPL | S | Confiança é um bucket atribuído pelo LLM uma vez; incrementos e decay existem só em `SKILL.md:334-342` e `agents/observer.md:137-139`. |
| E-B11 | [`skills/continuous-learning-v2/scripts/instinct-cli.py`:1955-2059](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/skills/continuous-learning-v2/scripts/instinct-cli.py#L1955-L2059) | IMPL · EXEC | S | `evolve --generate` grava em `…/ecc-homunculus/…/evolved/`; nenhum consumidor localizado. Executado: 5 arquivos criados, `~/.claude` intocado. |
| E-B12 | [`scripts/lib/eval-harness/gate.js`:175-177](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/eval-harness/gate.js#L175-L177) | IMPL (desativado) · EXEC | P+S | `requireSupportedIsolation()` sempre lança `gate.isolation_required`. Executado: `gate run` → rc=1. O doc `docs/architecture/eval-harness-frameworks.md:4` diz o mesmo. |
| E-B13 | [`scripts/harness-audit.js`:402-562](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/harness-audit.js#L402-L562) | WIRED · EXEC | S | Checagens por presença de arquivo. Executado: árvore oca com 3103 arquivos de zero byte → 76/80. |
| E-B14 | [`skills/gateguard/SKILL.md`:35-45](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/skills/gateguard/SKILL.md#L35-L45) | DOC | P+S | "+2.25" vem de duas tarefas, um par de notas cada; sem rubrica, avaliador, repetições ou dados brutos. |
| E-B15 | [`scripts/hooks/gateguard-fact-force.js`:1260-1274](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/hooks/gateguard-fact-force.js#L1260-L1274) | WIRED · TEST · EXEC | S | Nega a primeira edição e libera o retry sem conferir fatos. Falha aberta também para destrutivos quando o estado não grava (L1311-1312). |
| E-B16 | [`scripts/hooks/posttooluse-dispatcher.js`:240-244](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/hooks/posttooluse-dispatcher.js#L240-L244) | WIRED · EXEC | S | Com `ECC_POSTTOOLUSE_PASSTHROUGH='1'` o dispatcher ecoa o evento bruto no stdout, contrariando `bash-hook-dispatcher.js:125-129`. |
| E-B17 | [`scripts/hooks/stop-format-typecheck.js`:153-154](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/hooks/stop-format-typecheck.js#L153-L154) | WIRED | S | Erros de `tsc` vão para stderr com exit 0: não chegam ao modelo. O próprio `suggest-compact.js:251-257` reconhece que stderr+exit 0 não chega. |
| E-B18 | [`scripts/lib/llm-summary.js`:153](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/llm-summary.js#L153) | WIRED · EXEC (incidente) | S | `spawnSync('claude', ['--model','haiku','-p'])` dentro de hook (Stop/PreCompact). Um subagente desta auditoria disparou essa chamada por engano (ver §Incidente). |
| E-B19 | [`scripts/lib/transcript-context.js`:99-108](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/transcript-context.js#L99-L108) | WIRED · TEST · EXEC | P+S | Lê `message.usage` do transcript para estimar o contexto real. Testes 42/42 e 44/44; transcript sintético de 173k emitiu `additionalContext`. |
| E-B20 | [`scripts/ci/validate-agents.js`:97-109](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/ci/validate-agents.js#L97-L109) | WIRED · TEST · EXEC | S | Valida `model` (enum) e `tools` (escalar) em 68/68 agentes; roda no `npm test` e no CI. |
| E-B21 | [`scripts/ci/validate-skills.js`:15-18](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/ci/validate-skills.js#L15-L18) | WIRED · EXEC | S | Defeito de frontmatter é *warning* sem `--strict`; o CI não passa `--strict` (`.github/workflows/ci.yml:210-211`). |
| E-B22 | [`scripts/lib/hook-flags.js`:76-98](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/hook-flags.js#L76-L98) | WIRED · TEST · EXEC | S | Perfis `minimal|standard|strict`, `ECC_DISABLED_HOOKS`, dry-run. Executado: perfil minimal e id desabilitado deixam passar. |
| E-B23 | [`scripts/hooks/config-protection.js`:1-12](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/hooks/config-protection.js#L1-L12) | WIRED · TEST · EXEC | S | Bloqueia (exit 2) edição de config de lint/formatter existente; 9/9 testes. Não cobre `sed -i` via Bash. |
| E-B24 | [`scripts/hooks/block-no-verify.js`:542-553](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/hooks/block-no-verify.js#L542-L553) | WIRED · TEST · EXEC | S | Bloqueia `--no-verify` e `core.hooksPath`; 35/35 testes; roda em todos os perfis. |
| E-B25 | [`tests/integration/hooks.test.js`:104-160](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/tests/integration/hooks.test.js#L104-L160) | TEST · EXEC | S | Executa as strings de comando reais do `hooks.json` com JSON no stdin; 27/27. A maioria dos testes unitários chama `run()` direto. |
| E-B26 | [`workflows/orch-review.workflow.js`:259-273](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/workflows/orch-review.workflow.js#L259-L273) | IMPL (piloto, não distribuído) | S | Achados incertos continuam bloqueando; `workflows/` não está em `package.json` `files`; README L18 diz o contrário do código; sem testes. |
| E-B27 | [`scripts/hooks/cost-tracker.js`:128-149](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/hooks/cost-tracker.js#L128-L149) | WIRED · TEST · EXEC | S | Dedup por `message.id`; precifica a sessão inteira pela tarifa do último modelo (executado: tokens Opus cobrados como Haiku). |
| E-B28 | [`commands/plan.md`:10](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/commands/plan.md#L10) | DOC | S | "Do not call the Task tool or any subagent by default", contra `AGENTS.md:54-55` ("Complex feature requests → planner"). |
| E-B29 | [`scripts/lib/tmux-worktree-orchestrator.js`:210-232](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/scripts/lib/tmux-worktree-orchestrator.js#L210-L232) | IMPL · TEST · EXEC (dry-run) | S | Worktree por worker + arquivos task/handoff/status; `dependsOn` é ignorado e não há passo de merge. Previsão de conflito em `scripts/lib/worktree-lifecycle/git.js:123-140` (executada). |
| E-B30 | [`LICENSE`:1-3](https://github.com/affaan-m/ECC/blob/dd6ee538aee0f548d4a6b520118f875431fd749e/LICENSE#L1-L3) | DOC | S | MIT © 2026 Affaan Mustafa. Sem CLA/DCO em `CONTRIBUTING.md`. 8 skills marcadas Apache-2.0 sem NOTICE localizado. `gateguard` tem origem em `zunoworks/gateguard` (`scripts/hooks/gateguard-fact-force.js:19-20`). |

## 4. Comandos executados e resultados

### OSForge (A)

| Comando (em sandbox) | Resultado |
|---|---|
| `tests/test-assertions.sh` | 26/26 |
| `tests/test-gateguard-grant.sh` | 67/67 |
| `tests/test-gateguard-sql.sh` | 23/23 |
| `bash -n` em 16 `.sh`; `python3 -m py_compile` em 27 `.py` | 0 falhas |
| `_generate_manifest.py --check` / `--report` | em dia; 177 skills vivas, 47 core, 130 no manifesto, 76 módulos de conhecimento, 30 colisões de nome nota×skill |
| `_extract_index.py` + `_generate_index_md.py` + `git diff` | sem diferença |
| `./deploy.sh --dry-run` em HOME vazio | **exit 1** (`FileNotFoundError ~/.claude.json`, E-A31) |
| `./deploy.sh --claude-only --no-qdrant --no-archify` em HOME semeado | hook do usuário desregistrado, agente homônimo sobrescrito sem backup, skill do usuário apagada, backup de `settings.json` sobrescrito (E-A27 a E-A30); 2ª execução idempotente |
| Remoção de uma skill de `skills-core.txt` + redeploy | skill removida do destino; script de hook e agente aposentados **ficam** |
| Edição de `Keywords:` de skill não-core | preflight aborta (`manifest is STALE`) |
| Hooks com payloads sintéticos nos dois formatos | E-A01, E-A05, E-A07, E-A10 a E-A14 |
| Latência por hook, mediana de 20 execuções | scan-secrets 27 ms · gateguard 35 ms · observe 23 ms · route-guard 23 ms · session-save 161 ms · notify 44 ms |
| `strace -f -e execve` | `observe-capture` = 2 processos por chamada; `session-resume` = 12 |
| `osforge-db` em banco temporário: init, upsert-project, 16 observations, evolve, list-instincts, promote-instinct, resume, board, search, search-hybrid, search-semantic, vec-* | E-A15 a E-A17, E-A24 a E-A26; sem Ollama, `search-hybrid` cai para FTS5 (exit 0) e `search-semantic` sai com 1; linha de dimensão diferente derruba a busca com `ValueError` |
| Canvas: `bun server.ts` em porta aleatória + `curl` | confinamento de caminho OK; validação só de envelope (E-A44) |
| `validate-agents.js` do ECC sobre os agentes do OSForge | 41 erros (E-A41) |

**Não executado em A:** `test-skill-triggering.sh` e `test-orchestrator-routing.sh` (chamam `claude -p`, custo de API); Qdrant, Ollama, Archify; lado Cursor além do dry-run; bash 3.2 do macOS.

### ECC (B)

| Comando (cópia em sandbox, `npm ci --ignore-scripts`) | Resultado |
|---|---|
| 13 arquivos de teste de hooks | config-protection 9 · block-no-verify 35 · hook-flags 63 · gateguard-fact-force 196 · posttooluse-dispatcher 14 · bash-hook-dispatcher 6 · stop-hooks-stdout 29 · pre-compact 9 · hooks-metadata 16 · plugin-hook-bootstrap 15 · integration/hooks 27 · `hooks.test.js` 252 passam e 1 falha (provável artefato do sandbox) |
| 15 arquivos de teste de instalação | todos passam (ownership-guard 23, install-lifecycle 66, install-apply 42, uninstall 13 etc.) |
| Instalação alvo `claude`, perfil pequeno, HOME semeado | sem `--enable-hooks`/`--no-hooks` recusa e nada grava; com consentimento aplica 703 operações; arquivo homônimo do usuário pulado; hook alterado → recusa (E-B01, E-B02) |
| `doctor` → adulteração → `doctor` → `repair` → reinstalação → `uninstall` | detecta ausente/alterado; `repair` e reinstalação sobrescrevem a edição do usuário (E-B03); uninstall retém o alterado (E-B04); dry-run não altera nada, mas anuncia 704 remoções contra 701 reais |
| Instalação alvo `cursor` + hook delegado | não faz nada (E-B05) |
| Contagem de processos node por `Edit` (perfil standard) | 12 síncronos no PreToolUse + 1 no Post + 3 assíncronos; ~450–485 ms por Edit, ~280 ms por Bash |
| `validate-hooks` com um timeout alterado | sai com 1 (fingerprint divergente) |
| `catalog.js --text` | 68/94/292 conferem; `.codex-plugin/plugin.json:28` diz 281 e não é rastreado |
| `harness-audit` em si mesmo / diretório vazio / árvore oca | 80/80 · 0/39 · **76/80** (E-B13) |
| `eval-harness gate run` / `example` | recusa (`gate.isolation_required`, rc=1); recibos e replay de fixtures OK (E-B12) |
| Plan Canvas: `open`, `await` bloqueante, POST de origem estranha, Stop hook em três condições, 6 arquivos de teste | laço fechado confirmado (E-B06); origem estranha → `forbidden origin` |
| `orchestrate-worktrees --dry-run` com `dependsOn` | ignorado (E-B29); `worktree-lifecycle` num repo com conflito → `conflict` / `merge-ready` |
| `observe.sh`, `instinct-cli.py status` e `evolve --generate`, `session-start.js`, `cost-tracker.js` | E-B07, E-B11, E-B27 |
| `skill-comply` pytest com `claude` bloqueado | 39/39 (testa parser, grader com classificador simulado e sandbox; não roda modelo) |
| `suggest-compact.test.js`, `transcript-context.test.js` | 44/44, 42/42 (E-B19) |

**Não executado em B:** `tests/run-all.js` completo (286 arquivos) e cobertura; `auto-update`; jobs de release e de artefato empacotado; observer loop, `pre-compact`, `santa-loop`, `gan-harness`, `multi-*` (chamariam `claude` ou runtimes externos); state-store em runtime; `ecc2` (Rust); caminho Windows.

## 5. Cobertura por subsistema

| Subsistema | A | B |
|---|---|---|
| Hooks | 12 de 12 arquivos lidos por inteiro; todos executados | ~25 de ~50 scripts lidos (integral ou seções-chave); 13 suítes executadas |
| Estado, memória, aprendizado | `osforge-db.py` integral (1.713 linhas), 3 hooks, `skills/evolve`, `scripts/qdrant` | `observe.sh` integral; `instinct-cli.py` ~450 de 2.290 linhas; `session-start.js` ~200 de 798; state-store, tracker, vault por seções |
| Instalação | `deploy.sh` integral (763), 3 scripts auxiliares, geradores, ADRs 001/002/006/009 | `apply.js`, `ownership-guard.js`, `hook-consent.js`, 4 adaptadores integrais; `claude-settings.js` L399-702; `install-lifecycle.js` por seções; `install-plan.js`, `doctor.js`, `repair.js`, `uninstall.js` executados e **não lidos** |
| Skills e contexto | estatística sobre as 178; ~20 skills lidas (frontmatter + estrutura); geradores e harness integrais | estatística sobre as 292; `skill-comply` integral; ~15 skills por seções, ~9 só por descrição e títulos |
| Orquestração e planejamento | `AGENT.md`, 8 agentes, 2 de 9 comandos `spec-*` integrais (os outros 7 só por tamanho), skills de planejamento por títulos e gates | frontmatter dos 68 agentes; 3 agentes por seções; `plan.md` integral; PRP e `multi-*` por estrutura |
| Evals | 2 harnesses + lib de asserção + teste offline integrais | `eval-harness` (gate, CLI, doc), `harness-audit` (checagens) |
| Licenças | `LICENSE`, prática de `inspired_by`, README Origins | `LICENSE`, `CONTRIBUTING.md`, frontmatter `license:`/`origin:` das 292 skills, cabeçalhos dos candidatos |

## 6. O que não foi possível verificar

- **Comportamento real de modelo.** Nenhuma taxa de acionamento, os "30/30" e "15/16" citados em `docs/ANALISE-COMPARATIVA-MATTPOCOCK.md`, a linha de base de 61.324 tokens em `settings-base.json` e qualquer taxa de falso positivo. Não há logs dessas rodadas no repositório.
- **Como o Claude Code em uso trata:** o JSON em formato Cursor do `scan-secrets.sh`; frontmatter fora do esquema (`always-active`, `tools: allowed:`); `paths:` em `~/.claude/rules/**`; descoberta de skills aninhadas; o eco de evento bruto do ECC.
- **Sua instalação em uso.** Tudo aqui é sobre o código versionado. Não li `~/.claude`, `~/.osforge/osforge.db` nem `~/.claude/settings.json`; não sei quantas observations e instincts existem, nem se há hooks seus em `~/.claude/hooks/`.
- **Contagem de tokens por tokenizer.** Todo número de contexto é bytes ÷ 4 sobre arquivos e exclui prompt de sistema, esquemas de ferramentas e MCP.
- **Licenças de upstreams do ECC:** `zunoworks/gateguard`, `PRPs-agentic-eng` (Wirasm), `lavish-axi`, Homunculus; base das 8 skills Apache-2.0; situação das contribuições de terceiros sem CLA.

## 7. Dúvidas pendentes para você

1. Existem hooks seus em `~/.claude/hooks/` na máquina em uso? Se sim, o próximo `./deploy.sh` os desregistra (E-A27).
2. O uso do Cursor é real hoje? Várias correções só importam se for (rules `alwaysApply`, `scan-secrets` funciona só lá).
3. Os instincts já foram usados alguma vez? A tabela não tem escritor no código (E-A16); se estiver vazia, a decisão R-09 fica mais simples.
4. Quer manter o grant por afirmativa curta ("sim", "ok")? A correção proposta preserva isso, mas só quando há negação pendente.
