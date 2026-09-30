# Backlog de evolução do OSForge

Derivado de [`ANALISE-COMPARATIVA-ECC.md`](ANALISE-COMPARATIVA-ECC.md); evidências em [`ANALISE-COMPARATIVA-ECC-EVIDENCIAS.md`](ANALISE-COMPARATIVA-ECC-EVIDENCIAS.md).
Base: OSForge `d87a9bfc2058df233d30a2637fe252efb3256894`. Caminhos relativos à raiz do repositório. **(NOVO)** marca arquivo proposto que ainda não existe.
Esforço: **P** até meio dia · **M** 1–3 dias · **G** 3–7 dias, para quem conhece o repositório.
Todos os comandos de verificação rodam com `HOME` temporário; nenhum toca `~/.claude`.

## Estado (2026-09-18)

**23 de 24 itens fechados.** O que sobrou não é trabalho parado: é trabalho que depende de
uma decisão de gasto ou do resultado de um experimento.

| Etapa | Itens | Estado |
|---|---|---|
| 0 — Correções imediatas | B-001 … B-005 | ✅ |
| 1 — Rede de segurança | B-006 … B-009 | ✅ |
| 2 — Evals confiáveis | B-010, B-011, B-012 | ✅ · B-013 ◐ E1 rodado; E2 liberado, E3/E4 aguardam correção do instrumento |
| 3 — Consolidação | B-014 … B-020 | ✅ |
| 4 — Conforme os experimentos | B-021, B-022, B-024 | ✅ · B-023 ◐ (arquivos feitos; plano proporcional depende do E3) |

Aberto, e por quê:

- **B-013 (E1, estabilidade)** — rodado em 2026-09-29: roteamento 1/16 PASS (skill
  declarada e não carregada é comportamento real), trigger 1/30 positivos. E2 liberado;
  E3/E4 esperam `max-turns`, `r11`/`r15` e visibilidade do `route-guard`. Detalhe no próprio B-013.
- **B-023 (plano proporcional)** — os arquivos do orquestrador já são deployados; mudar o
  "todo plano precisa de Roster/User stories/Task manifest" depende do E3, que depende do E1.
- **R-11 condicionada** (`~/.claude/rules/`) — precisa confirmar em sessão real, com
  `scripts/measure-context.py`, que o Claude Code honra `paths:`.
- **E-A08** (ligar o gate de Edit/Write do GateGuard) e **R-09** (laço de instincts) — presos
  a E6 e E5, pela mesma razão: ninguém mediu o ganho ainda.

Tudo que foi fechado tem teste que falha sem a correção. As dez suítes offline somam
**441 verificações** (assertions 60 · contratos de hook 59 · gateguard-grant 84 · deploy
lifecycle 64 · continuidade 35 · canvas 34 · scan-secrets 33 · contexto/tokens 27 ·
gateguard-sql 23 · installers 22) e nenhuma toca o `~/.claude` de ninguém. O Pacote 01
(B-025–B-029) somou mais cinco — judge 77 · eval-cases 42 · quota 30 · calls 26 · harness-quota
15 — e os contratos de hook foram a 62: **634 verificações** em quinze suítes.

Fora do backlog, uma coisa que a auditoria não tinha visto: `scripts/install-skill.sh` —
deployado em `~/.local/bin` e metade do Model A — usava `mapfile`, que **não existe no
/bin/bash 3.2 do macOS**. `bash -n` só faz o parse e nunca ia pegar. Corrigido, com
`tests/test-installers.sh` (22 verificações, incluindo um shell sem os builtins do bash 4)
e `scripts/check-portability.py` no preflight e no CI para impedir a classe inteira.

## Etapa 0 — Correções imediatas

### B-001 · Grant do GateGuard exige negação pendente — ✅ feito
- **Recomendação / evidência:** C-01 · E-A05, E-A06, E-A07
- **Objetivo:** um "ok" ou "proceed" só libera um comando destrutivo que acabou de ser negado, e só aquele.
- **Arquivos:** `hooks/gateguard.py` (`apply_prompt_to_state`, `_active_grant`, ramo `Bash` de `main`, `_AUTH_PHRASES` L325-329); `tests/test-gateguard-grant.sh`.
- **Mudança:** ao negar, gravar `state["last_denial"] = {"key": destructive_key, "at": now}`. `apply_prompt_to_state` só concede `grant` de turno se `last_denial` existir e tiver menos de `PENDING_TTL` (sugestão: 600 s); o grant guarda `scope_key`. No ramo Bash, grant de turno vale só se `scope_key == destructive_key`. A frase explícita de sessão continua valendo sem negação pendente.
- **Dependências:** nenhuma.
- **Aceite:** (1) sessão nova + "ok" + `git reset --hard HEAD~10` → negado; (2) negação + "ok" + mesmo comando → permitido e logado `GRANT-ALLOW`; (3) negação de A + "ok" + comando B → B negado; (4) "please proceed with the refactor" sem negação → `none`; (5) os 67 casos atuais continuam passando ou são atualizados com justificativa.
- **Verificação:** `./tests/test-gateguard-grant.sh`
- **Esforço:** P. **Risco:** um passo extra quando o usuário autoriza de antemão. **Reversão:** `OSFORGE_GATEGUARD_LEGACY_GRANT=1` por uma versão.

### B-002 · `scan-secrets` funciona no Claude Code — ✅ feito
- **Recomendação / evidência:** C-02 · E-A01, E-A03, E-A04
- **Objetivo:** bloquear commit com segredo e `rm -rf` de raiz nos dois harnesses.
- **Arquivos:** `hooks/scan-secrets.sh` (ou reescrever como `hooks/scan-secrets.py` **(NOVO)**, mantendo o nome antigo como wrapper); `hooks/hooks-claude-code.json` e `hooks/hooks.json` se o nome mudar.
- **Mudança:** comando = `tool_input.command` com fallback para `command`; `workspace` = `cwd` com fallback para `workspace_roots[0]`; saída `hookSpecificOutput.permissionDecision="deny"` quando `hook_event_name` indicar Claude Code, JSON atual no Cursor; padrões: `sk-[A-Za-z0-9_-]{20,}`, `ghp_[A-Za-z0-9]{36}`, `AKIA[0-9A-Z]{16}`, `xox[bp]-…`, `://[^/\s:]+:[^@\s]+@`, `-----BEGIN [A-Z ]*PRIVATE KEY-----`; varrer o **diff staged**, não só nomes de arquivo.
- **Dependências:** nenhuma (os casos entram em B-005).
- **Aceite:** payload do Claude Code com `rm -rf ~` → `deny`; `git commit` com `ghp_…` staged → `deny` nos dois formatos; comando inofensivo → permite; JSON inválido → permite com exit 0.
- **Verificação:** `echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rm -rf ~"}}' | bash hooks/scan-secrets.sh` deve conter `"deny"`.
- **Esforço:** P. **Risco:** falso positivo em fixtures com chaves falsas → permitir `# osforge:allow-secret` na linha.

### B-003 · Deploy funciona em HOME novo; dry-run é inerte — ✅ feito
- **Recomendação / evidência:** C-03 · E-A31, E-A33
- **Arquivos:** `deploy.sh` (`sync_mcps_claude` L196-233, bloco L357-373, `copy_dir` L87-94, L308, L322, L346, `merge_settings_claude` L158-167, topo do script).
- **Mudança:** tratar `~/.claude.json` ausente como `{}`; pôr a checagem de drift de MCP atrás de `$DRY_RUN`; `command -v rsync` no início com mensagem clara; nenhum `mkdir`/`rm` em dry-run; remover toda chave iniciada por `_` de `settings-base.json` antes do merge.
- **Aceite:** `H=$(mktemp -d); HOME=$H ./deploy.sh --dry-run` sai 0 e `find $H -type f | wc -l` = 0; deploy real em HOME vazio chega a instalar `osforge-db` e `install-skill`; `settings.json` resultante não tem chave `_…`.
- **Esforço:** P. **Risco:** baixo.

### B-004 · Revisor: tirar a cota de achados, pôr o gate pré-relatório — ✅ feito (E4 pendente)
- **Recomendação / evidência:** R-12 · E-A42; origem `agents/code-reviewer.md:39-74` do ECC (MIT)
- **Arquivos:** `skills/quality/adversarial-review/SKILL.md` L85-88; `agents/code-reviewer.md`; `THIRD_PARTY_NOTICES` **(NOVO)**.
- **Mudança:** remover "HALT if zero findings" e "findings < 10"; acrescentar o gate de quatro perguntas, exigência de prova para HIGH/CRITICAL, a cláusula "zero achados é um resultado válido" e a lista de falsos positivos, reescritos no `SKILL-STANDARD`, com `inspired_by` e aviso MIT.
- **Aceite:** harness de acionamento continua disparando a skill; experimento E4 agendado.
- **Esforço:** P. **Risco:** revisor ficar leniente — é o que E4 mede.
- **Resultado:** `adversarial-review` v1.2 sem cota, com gate de quatro perguntas, prova para Critical/Important, "zero achados é válido" (com a lista de áreas trabalhadas), lista de falsos positivos; `agents/code-reviewer.md` aponta para o gate. `THIRD_PARTY_NOTICES` criado (ECC MIT, zunoworks/gateguard via ECC, mattpocock). Harness de acionamento: descrição/keywords intactos.

### B-005 · Correções de documentação divergente — ✅ feito
- **Recomendação / evidência:** §4.4 · E-A32, E-A35 a E-A39
- **Arquivos:** `README.md` L36, L282; `CLAUDE.md` L10, L39, L55; `claude-code/CLAUDE.md` L11, L75, L206-207, L221; `USAGE.md` L33, L87, L93, L106-107; `rules/agent-skills-reference.mdc` L2, L9; `scripts/_generate_index_md.py` L98; `docs/DECISIONS.md` (marcar ADR-002 como superado pelo Model A); docstring de `hooks/gateguard.py` L53.
- **Aceite:** passa na checagem de contagens de B-008.
- **Esforço:** P. **Observação:** mexer em `claude-code/CLAUDE.md` invalida o cache de prompt de todas as sessões; agrupar com outras mudanças nesse arquivo (B-020).

## Etapa 1 — Rede de proteção

### B-006 · Runner de testes de contrato de hook — ✅ feito
- **Recomendação / evidência:** R-01 · E-A01, E-A12, E-A13; estilo de E-B25
- **Arquivos (NOVOS):** `tests/hooks/run-contracts.sh`, `tests/hooks/cases.tsv`, `tests/hooks/fixtures/{claude-code,cursor,transcripts}/*`, `docs/HOOKS.md`.
- **Mudança:** conforme §5.3 do relatório: extrai o comando real de `hooks/hooks-claude-code.json` e `hooks/hooks.json`, roda com fixture no stdin, HOME e TMPDIR temporários, confere exit 0, stdout vazio ou JSON válido, veredito por harness e nenhuma escrita fora do sandbox.
- **Dependências:** nenhuma; B-001 e B-002 deixam os casos verdes.
- **Aceite:** no commit atual falha em pelo menos: scan-secrets/Claude Code, grant sem negação, `notify-done` com `stop_hook_active=false`, payload não-objeto no gateguard e no route-guard, escrita em `/tmp`. Verde após as correções. Roda em < 30 s.
- **Verificação:** `./tests/hooks/run-contracts.sh`
- **Esforço:** M. **Risco:** contrato do Claude Code mudar → contrato fica numa tabela só dentro do runner.

### B-007 · Correções pequenas que o runner revela — ✅ feito
- **Evidência:** E-A11, E-A12, E-A13, E-A14
- **Arquivos:** `hooks/notify-done.sh` L25 (condição invertida); `hooks/gateguard.py` e `hooks/route-guard.py` (payload que não é dict → permitir, exit 0); `hooks/protect-tests.sh` e `hooks/notify-done.sh` (log em `~/.osforge/logs/`, não `/tmp`); `hooks/route-guard.py` L115-118 (evidência de carga só vale em `Skill`, `Read` de `SKILL.md` e prompt de `Task/Agent` que cite o **caminho**, não o nome solto).
- **Decisão embutida:** `protect-tests.sh` passa a emitir `additionalContext` ("arquivo de teste alterado: …") ou sai do JSON de hooks. Não fica como está.
- **Esforço:** P.

### B-008 · CI mínimo + checagem de contagens — ✅ feito (CI executa no primeiro push da branch)
- **Recomendação / evidência:** R-13 · §4.4
- **Arquivos (NOVOS):** `.github/workflows/ci.yml`, `scripts/check-counts.py`.
- **Conteúdo do job** (ubuntu + macos): `bash -n` em `*.sh`; `python3 -m py_compile` em `*.py`; parse dos JSON; `_generate_manifest.py --check`; regenerar índices + `git diff --exit-code`; `tests/*.sh`; `tests/hooks/run-contracts.sh`; `HOME=$(mktemp -d) ./deploy.sh --dry-run`; `scripts/check-counts.py`.
- **`check-counts.py`:** conta `SKILL.md` vivos, entradas do core, agentes, rules, comandos, hooks conectados e servidores MCP; procura os números correspondentes nos arquivos de B-005 e falha em divergência.
- **Dependências:** B-003, B-006.
- **Aceite:** verde no `main`; introduzir "~64 core" em qualquer doc deixa vermelho.
- **Esforço:** P. **Rejeitado de propósito:** matriz de versões, gate de cobertura.

### B-009 · Frontmatter e ferramentas dos agentes — ✅ feito
- **Recomendação / evidência:** R-07 · E-A41, E-A40; origem E-B20
- **Arquivos:** `scripts/_generate_manifest.py` (nova checagem em `--check`); `agents/*.md`; apagar `claude-code/agents/`.
- **Mudança:** `tools: Read, Grep, Glob, Bash` em `code-reviewer`, `security-auditor`, `validator`, `explorer-agent`, `planner`; corrigir `validator.md` L9-18 para o esquema do Claude Code; `project-planner` ganha `Write` (o corpo exige criar arquivo); `model:` alinhado a `smart-model-dispatch`; remover `always-active`/`model-tier` de `orchestrator/AGENT.md` ou documentar que são só anotação.
- **Aceite:** `--check` falha com agente sem `name`/`description`, com `tools` em lista YAML ou com `model` fora do enum; preflight do deploy passa.
- **Esforço:** P. **Risco:** agente que precisava de escrita perder a ferramenta → rodar os 16 casos de rota depois.

## Etapa 2 — Evals confiáveis

### B-010 · Fixar modelo e repetições nos dois harnesses — ✅ feito
- **Recomendação / evidência:** R-08 · E-A45
- **Arquivos:** `scripts/test-skill-triggering.sh`, `scripts/test-orchestrator-routing.sh`, `scripts/lib/harness-assertions.sh`, `tests/test-assertions.sh`.
- **Mudança:** flags `--model` (obrigatória fora de `--dry`) e `--runs N` (padrão 3); relatório por caso = k de N; asserção de skill exige nome da ferramenta e caminho **no mesmo evento**; dimensão agente exige despacho (`Agent/Task`) quando o caso esperar delegação; opção `--home DIR` para rodar contra um deploy limpo.
- **Aceite:** `tests/test-assertions.sh` cobre os dois modos novos com streams sintéticos; nenhuma chamada de API no teste offline.
- **Esforço:** M.
- **Resultado:** `--model` obrigatório fora de `--dry`, `--runs` (padrão 3) com veredito k de N (PASS só em `k = N`; `0 < k < N` = FLAKY, reprova), `--home DIR`, `--dry` (lista e valida sem chamar modelo) e `--report` nos dois harnesses. O veredito saiu do `grep` por linha para **lib/stream_assert.py**, que confere por BLOCO: texto citando o caminho + `tool_use` de outro arquivo na mesma mensagem passava como skill lida. Casos que exigem delegação levam `!` no campo de agente (`r12`) e só aceitam despacho real. `tests/test-assertions.sh`: 26 → 60 casos, todos offline.

### B-011 · Ativar o eval de trigger que já existe — ✅ feito (rodada paga pendente de autorização)
- **Recomendação / evidência:** R-08 · E-A46
- **Arquivos:** `skills/skill-creator/scripts/run_eval.py`, `run_loop.py`; **(NOVO)** `scripts/evals/trigger/<skill>.json` com consultas positivas e negativas; **(NOVO)** `scripts/run-trigger-eval.sh`.
- **Mudança:** 5 positivas + 5 negativas escritas à mão para as 47 core, começando por 15; divisão 60/40 ajuste/avaliação registrada no arquivo.
- **Aceite:** `--dry` lista os casos sem chamar modelo; uma rodada real gera `docs/evals/<data>-<modelo>-trigger.md`.
- **Esforço:** M (a maior parte é escrever casos).
- **Resultado:** `scripts/run-trigger-eval.sh` liga o `run_eval.py` que já existia e ninguém chamava (E-A46). 15 skills core × (5 positivas + 5 negativas) = 150 casos escritos à mão em `scripts/evals/trigger/`, com o split 60/40 gravado em cada arquivo (`tune` ajusta a description, `eval` mede). `--dry` valida (5+5 mínimos, ids únicos, consultas não repetidas entre skills, split cobrindo todos os casos) e imprime o custo: 450 chamadas a suíte inteira, 180 o split `eval`, 30 uma skill. **Falta só a rodada paga** — aguarda autorização de custo.

### B-012 · Versionar resultados de eval — ✅ feito
- **Arquivos (NOVOS):** `docs/evals/README.md`, `docs/evals/<data>-<modelo>-<suite>.md`.
- **Conteúdo mínimo:** SHA do OSForge, id do modelo, comando, casos, k de N por caso, tokens e tempo totais. Substitui os números soltos em `claude-code/CLAUDE.md:49-50`, `hooks/route-guard.py:7-8` e na análise do Matt.
- **Esforço:** P.
- **Resultado:** `docs/evals/README.md` (formato, como nasce um arquivo, como ler, custo) + `scripts/lib/eval_report.py`, chamado pelo `--report` das três suítes: carimba SHA, versão, árvore suja, modelo, HOME, comando exato, tokens somados dos streams (uma vez por `message.id`), duração e a tabela de k de N, com a lista de instáveis separada para o E1. Os quatro números soltos (CLAUDE.md ×3, route-guard.py ×1) passaram a dizer que são de 2026-08 e não versionados, e estão tabelados em **Pendentes de versionamento** com o comando que os refaz.

### B-013 · Rodar E1 (estabilidade) e decidir E2–E4 — ◐ E1 rodado (2026-09-29); E2 liberado, E3/E4 aguardam correção do instrumento
- **Recomendação:** §8.2 do relatório. **Dependências:** B-003, B-010, B-012 — **todas fechadas**. **Custo:** API — fazer piloto de 2 casos antes. **Saída:** lista de casos instáveis e ruído por suíte, que vira o limiar de decisão dos demais experimentos.
- **Pronto para rodar** (o FLAKY do relatório já é a saída que o E1 pede). Piloto e rodada, em ordem de custo:

```bash
# piloto: 2 casos × 3 execuções = 6 chamadas
# (sem --home: um HOME vazio não tem login -- "Not logged in", 6/6 ERROR, 2026-09-29)
./scripts/test-orchestrator-routing.sh --model <id> --id r01,r12 --runs 3 \
    --report docs/evals/$(date +%F)-<id>-routing-piloto.md

# E1 roteamento: 16 × 3 = 48 chamadas
./scripts/test-orchestrator-routing.sh --model <id> --runs 3 --report docs/evals/$(date +%F)-<id>-routing.md

# E1 trigger (split de avaliação): 60 × 3 = 180 chamadas
./scripts/run-trigger-eval.sh --model <id> --runs 3 --split eval --report docs/evals/$(date +%F)-<id>-trigger.md
```

**Resultado E1 (2026-09-29, `claude-sonnet-5`, 3 execuções por caso).** Relatórios:
[`routing`](evals/2026-09-29-claude-sonnet-5-routing.md) e [`trigger`](evals/2026-09-29-claude-sonnet-5-trigger.md).
Antes da rodada, três defeitos do próprio harness foram achados e corrigidos com teste
(`3979cc0`, `c8d8b84`): ERROR passava a suíte; o trigger eval só contava o clone da skill e
rodava dentro do repo hub (as regras do hub sequestravam a resposta); ERROR de um caso
escondia misses medidos nas outras execuções (`case_verdict`, assertions 60 → 67).

- **Roteamento, 16 × 3:** PASS 1 · FLAKY 6 · FAIL 8 · ERROR 1. A dimensão *agente* acerta em
  14/16; o que reprova é a *skill*.
- **O miss de skill é comportamento real, não asserção errada.** Conferido nos streams: em
  `r03` e `r06` a linha de rota declara a skill esperada do manifest nas 3 execuções
  (`security-threat-model`, `aws-deploy`/`deployment-procedures`) e o `SKILL.md` nunca é
  lido; `r14` declara `spec-builder` 3/3 e não carrega; `r12` declara `offensive-*` e nunca
  despacha o `penetration-tester` (crítico, 0/3). É exatamente o padrão que o
  `claude-code/CLAUDE.md` descreve ("declarada e nunca aberta") — agora medido.
- **Instabilidade (entrada do E1):** `r01 r02 r04 r05 r08 r10` variam na dimensão skill ou
  por ERROR. Os 6 ERRORs da rodada são todos `error_max_turns` com `--max-turns 8`: o limite
  pune justamente quem carrega a skill (ler `SKILL.md` + referências gasta turnos).
- **Casos com defeito de desenho:** `r15` é pergunta ("como estruturo…?") e o contrato isenta
  pergunta pura da linha de rota — o modelo respondeu direto 3/3, coerente com a regra.
  `r11` pede "monta o plano" e 2/3 execuções foram para o `osforge-canvas` (a regra da casa
  para planos) sem linha de rota; o miss de linha é real, mas o conjunto de skills aceitas
  não inclui a skill que a própria regra manda usar.
- **Trigger, split `eval`, 73 casos × 3:** positivos **1/30**, negativos 43/43. Sondagem
  manual confirma: pedidos implícitos em pt-BR são respondidos direto, sem ferramenta — as
  descriptions não disparam. Os negativos passarem não diz nada enquanto quase nenhum
  positivo dispara (um detector que nunca dispara tira 100% em negativo).
- **Lacuna do instrumento:** o `stream-json` só registra hooks de `SessionStart`; se o
  `route-guard` (Stop) bloqueou e forçou a carga, isso não aparece no log. A rodada mede o
  modelo **com** o guard ligado, mas não mostra quanto o guard contribuiu.

**Decisão E2–E4:**

| Exp. | Decisão | Por quê |
|---|---|---|
| E2 (guarda do resume) | **Liberado** — piloto de 2 × 2 antes dos 10 × 2 | Não usa o harness de roteamento nem de trigger; a guarda é adotada de qualquer forma (custo ≈ 0) |
| E3 (plano proporcional) | **Adiado** até a correção abaixo + piloto de 2 tarefas | Não há fixtures com teste oculto ainda; com 6/16 casos instáveis no E1, n = 10 × 3 só detecta diferença grande — o limiar precisa vir de uma rodada sem os ERRORs de `max-turns` |
| E4 (gate do revisor) | **Adiado**, mesma condição do E3 | Rubrica existe (`scripts/evals/judge/e4/rubric-v1.md`), os 20 diffs não |

**Antes de E3/E4 (barato, sem API):** (1) subir `OSFORGE_TEST_MAX_TURNS` do roteamento de 8
para 12 e remedir só os casos que deram ERROR; (2) reescrever `r15` como demanda de ação e
aceitar `osforge-canvas` em `r11`; (3) expor no relatório se o `route-guard` bloqueou
(ex.: o hook grava um marcador que o harness lê). **Achados de produto, fora do E1** — viram
itens próprios, cada um com eval antes/depois: (a) reescrever descriptions das skills core
para pedido implícito em pt-BR (1/30 positivos); (b) garantir carga da skill de manifest
declarada (`r03`, `r06`, `r14`: declarada 3/3, lida 0/3); (c) despacho obrigatório do
`penetration-tester` (`r12`).

## Etapa 3 — Consolidação

### B-014 · `scripts/osforge-state.py` + install-state — ✅ feito
- **Recomendação / evidência:** R-03 · E-A27 a E-A30; origem E-B01, E-B02, E-B04
- **Arquivos:** **(NOVO)** `scripts/osforge-state.py`; `deploy.sh` (`copy_file`, `copy_dir`, `backup_file`, laço de hooks L323-329, cópia do canvas, `deploy_skills`).
- **Mudança:** esquema `osforge.install.v1` do relatório §5.3; registro de `{dst, src, sha256}`; backup em `~/.claude_backups/<run_id>/<relativo>`; regra de propriedade (não registrado e diferente → pula e avisa; registrado e alterado → backup + aviso, sobrescreve com `--force`); modo adoção na primeira execução.
- **Dependências:** B-003.
- **Aceite:** ver B-017.
- **Esforço:** M–G. **Risco:** estado corrompido → escrita atômica; ausência de estado = modo adoção.

### B-015 · Merge de hooks por id com recusa de drift — ✅ feito
- **Recomendação / evidência:** R-03 · E-A27; origem E-B01
- **Arquivos:** `deploy.sh` `merge_hooks_claude` L96-143 e `merge_settings_claude` L146-194.
- **Mudança:** id = `evento|matcher|basename(comando)`; remove só entrada idêntica à gravada no estado; id gravado com conteúdo diferente → aborta mostrando diff (`--force-hooks`); itera eventos do estado **e** do repositório; escrita em temporário + `mv`; um único backup por execução.
- **Aceite:** hook do usuário em `~/.claude/hooks/meu.sh` sobrevive; hook do OSForge editado à mão faz o deploy parar; evento removido do repositório some do `settings.json`.
- **Esforço:** M.

### B-016 · `--doctor`, `--uninstall`, `--restore <run_id>`; poda por estado — ✅ feito
- **Recomendação / evidência:** R-03 · E-A29; origem E-B04
- **Arquivos:** `deploy.sh`, `scripts/osforge-state.py`.
- **Mudança:** `deploy_skills` troca `rsync --delete` por cópia + poda do que estava no estado anterior e saiu da allowlist; mesma poda para agentes, comandos e scripts de hook; excluir `hooks/validate.py` do glob L323 (mover para `docs/templates/`).
- **Aceite:** skill instalada por `install-skill.sh --global` sobrevive ao deploy; agente removido do repositório some do destino; `--uninstall` deixa só o que era do usuário e restaura valores anteriores das settings.
- **Esforço:** M.

### B-017 · Teste de ciclo de vida do deploy — ✅ feito
- **Arquivos (NOVO):** `tests/test-deploy-lifecycle.sh` (roteiro do relatório §5.3, HOME temporário; usa `rsync` real se existir).
- **Aceite:** verde; entra no CI de B-008.
- **Esforço:** P–M.
- **Resultado:** 61 checagens, ~50 s, offline; roda o `deploy.sh` real 15× num HOME semeado (hook seu, skill sua, skill `--global`, `CLAUDE.md` seu, `settings.json` com `theme`/`env`/hooks seus, `~/.claude.json` com MCP seu, hook do OSForge de uma revisão antiga = instalação legada). Adicionado ao CI; não entra no preflight do deploy por custo (~1 min).

### B-018 · Identidade de projeto única — ✅ feito
- **Recomendação / evidência:** R-04 · E-A19, E-A20, E-A26; origem E-B08
- **Arquivos:** **(NOVO)** `hooks/lib/project_id.py`; `hooks/observe-capture.py` L117-121; `hooks/session-save.py` L60-82; `hooks/session-resume.sh` L36-56; `scripts/osforge-db.py` (esquema `projects`, `cmd_upsert_project`, migração).
- **Mudança:** ordem de resolução `OSFORGE_PROJECT` → raiz do git casada com `projects.root_path` → `projects.remote_hash` (sha256 do remote normalizado, sem credenciais) → basename normalizado; `ALTER TABLE projects ADD COLUMN root_path/remote_hash`; honrar de fato a variável `OSFORGE_DB`.
- **Aceite:** pastas homônimas com remotes diferentes → slugs diferentes; subdiretório e worktree → mesmo projeto; projetos já registrados continuam resolvendo.
- **Esforço:** M.

### B-019 · Retomada com guarda, teto, escopo e limpeza — ✅ feito
- **Recomendação / evidência:** R-04 · E-A21 a E-A24, E-A14; origem E-B07
- **Arquivos:** `hooks/session-resume.sh` L59-94; `hooks/session-save.py` L106-109, L138-195; `hooks/observe-capture.py` L102-108; `scripts/osforge-db.py` L382-404, L596-601, L1555/L1569; **(NOVO)** `hooks/lib/scrub.py`.
- **Aceite:** os seis casos de R-04 no relatório §5.3, como casos de `tests/hooks/` e de banco temporário.
- **Esforço:** M. **Dependências:** B-018, B-006.
- **Resultado:** `tests/test-session-continuity.sh` (35 checagens, offline): hooks reais + `osforge-db` real em banco temporário (`OSFORGE_DB`) e repositórios git temporários. Cobre E-A14, E-A19 a E-A24 e E-A26 por execução; o filtro vetorial de E-A24 foi verificado ficando vermelho no código anterior (provider `mock`).

### B-020 · Dreno do feedback do Canvas + validação no servidor — ✅ feito
- **Recomendação / evidência:** R-05 · E-A43, E-A44; origem E-B06
- **Arquivos:** **(NOVO)** `hooks/canvas-feedback.py`; `hooks/hooks-claude-code.json` (Stop); `scripts/canvas/server.ts` L176-196, L291-314; `skills/osforge-canvas/SKILL.md` L99-137; **(NOVO)** `tests/canvas/` com o roteiro `curl` desta auditoria.
- **Aceite:** feedback pendente do projeto atual → Stop bloqueia uma vez com o conteúdo; outro cwd, `stop_hook_active`, já entregue e servidor fora do ar → passa; POST para artefato inexistente, `revision` divergente, `action` fora do enum ou Origin não-loopback → 4xx.
- **Esforço:** M. **Dependências:** B-018 (slug), B-006.
- **Resultado:** `tests/test-canvas-feedback.sh` (34 checagens): parte A roda o hook contra um data dir semeado e um health falso (sem Bun); parte B sobe o `server.ts` real em porta aleatória e verifica os 4xx do aceite mais o hook contra o servidor real. Servidor: 404/409/400/403 conforme o aceite; só os campos validados são persistidos. Contratos CC-49/CC-50 no runner.

## Etapa 4 — Conforme os experimentos

### B-021 · Aviso de contexto pelo uso real — ✅ feito
- **Recomendação / evidência:** R-06 · E-B19. **Arquivos:** **(NOVO)** `hooks/context-threshold.py`; `hooks/hooks-claude-code.json`; espinha de `claude-code/SKILLS.md` L117-146. **Aceite:** transcripts sintéticos de 100k/125k/155k → 0/1/2 avisos, um por faixa por sessão; < 40 ms por chamada. **Esforço:** P. **Resultado:** `tests/test-context-usage.sh`: 0/1/2 confirmados; transcript de 30 MB lido em ~1 ms (só o fim). Feito antes de E1 por ser P e não depender do experimento (a faixa é a do SKILLS.md; ajustável por `OSFORGE_CONTEXT_BANDS`).

### B-022 · Tokens por sessão e por projeto — ✅ feito
- **Recomendação / evidência:** R-10 · E-B27. **Arquivos:** `hooks/session-save.py`; `scripts/osforge-db.py` (tabela `usage`, `cmd_board`). **Aceite:** transcript com a mesma `message.id` em duas linhas conta uma vez; tokens separados por modelo; `board` mostra o total do projeto. **Esforço:** P. **Dependências:** B-018. **Resultado:** tabela `usage` (upsert por projeto+sessão+modelo), `add-usage`/`usage`, totais no `board` (texto e `--json`) e no `stats`; `session-save.py` computa por `message.id`. Coberto em `tests/test-context-usage.sh`.

### B-023 · Plano proporcional e arquivos do orquestrador — ◐ arquivos feitos; plano proporcional aguarda E3
- **Recomendação / evidência:** R-14 · E-A38, E-A40, E-A28. **Arquivos:** `claude-code/CLAUDE.md` L126, L140; `agents/orchestrator/AGENT.md` L126-137, L432-437; `deploy.sh` `copy_dir` (ou embutir `triage-rules.md`); `scripts/routing-cases.tsv` (casos de piso). **Aceite:** depois do experimento E3; `~/.claude/agents/orchestrator/` contém os arquivos citados ou o `AGENT.md` não os cita mais. **Esforço:** P. **Resultado (E-A40):** `deploy.sh` leva `triage-rules*.md`, `plan-templates/` e `delegation-brief.md` para `~/.claude/orchestrator/` (e `~/.cursor/orchestrator/`), e o `AGENT.md` cita esses caminhos; `always-active`/`model-tier` (não são esquema do Claude Code) viraram `model: sonnet`. **Pendente (E-A38):** plano proporcional — depois de E3.

### B-024 · Rules com escopo; unicode; atenuação de negações — ✅ feito (R-11 condicionada continua aberta)
- **R-11 (parte imediata):** `alwaysApply: false` nas rules de stack em `rules/*.mdc`. **R-11 (condicionada):** gerar `~/.claude/rules/osforge/` em `deploy_claude` só depois de confirmar o carregamento com `measure-context.py` numa sessão real.
- **R-16:** **(NOVO)** `scripts/check-unicode.py` no preflight e sobre `sources/`.
- **R-02:** `_deny` em `hooks/gateguard.py` encurta a mensagem a partir da 4ª negação da sessão.
- **Esforço:** P cada.
- **Resultado:** R-11 imediata: `alwaysApply: false` em `nextjs-patterns`, `typescript-strict`, `code-style` (contagem 11 always-on + 3 por glob checada por `check-counts`). R-16: `scripts/check-unicode.py` (faixas do ECC + tolerância a `U+FE0F` após pictograma e em keycaps) no preflight e no CI; árvore limpa (709 arquivos). R-02: `gateguard.py` encurta a mensagem da 4ª negação consecutiva em diante e zera a contagem no grant (`tests/test-gateguard-grant.sh` 79 → 84 casos).

## Pacote 01 — Qualidade e controle (ADR-016)

Proposta e specs: [`intake/PACOTE-01-qualidade-e-controle.md`](intake/PACOTE-01-qualidade-e-controle.md). Decisões D-1, D-2, D-3, D-N1, D-N2 e D-N3 aprovadas em 2026-09-28 como recomendadas; rótulos duvidosos (`systematic-debugging n4`, `tdd-workflow n4`, `adversarial-review n2`) mantidos.

### B-025 · Casos de eval com categoria, casos críticos e validação sem modelo — ✅
- **Spec:** [N-01](intake/needle/SPEC-N01-casos-de-eval.md). **Chamadas pagas:** 0. `tests/test-eval-cases.sh`; `--dry`: 170 casos, 20 críticos, 0 problemas.

### B-026 · Harness respeita a cota — ✅
- **Spec:** [L-01 parte B](intake/laya/SPEC-L01-guarda-de-cota.md). **Dependências:** B-027. **Chamadas pagas:** 0. `tests/test-harness-quota.sh`; rejeição → `NOT RUN` + exit 75; parada preventiva em `OSFORGE_EVAL_QUOTA_STOP` (85%).

### B-027 · Aviso de janela de cota ao modelo — ✅
- **Spec:** [L-01 parte A](intake/laya/SPEC-L01-guarda-de-cota.md). **Chamadas pagas:** 0. `tests/test-quota.sh`; hooks continuam 11 (D-2).

### B-028 · Auditoria por chamada, custo derivado, retenção — ✅
- **Spec:** [L-03](intake/laya/SPEC-L03-auditoria-por-chamada.md). **Chamadas pagas:** 0. `tests/test-calls.sh`; `osforge-db calls|backfill-calls|prune-calls`; custo derivado de `claude-code/pricing.json`, nunca armazenado.

### B-029 · Juiz isolado sobre a assinatura — ✅ (E-J0 4/4, 2026-09-29)
- **Spec:** [L-02](intake/laya/SPEC-L02-juiz-isolado.md). **Chamadas pagas:** 1–3 (E-J0). `tests/test-judge.sh`.

### B-030 · Registro de injeção de instincts — ⏸ só se o E5 for rodar
- **Insumo:** [L-04](intake/laya/DECISAO-L04-laco-de-aprendizado.md).

## Adiados — só com evidência

| Item | Condição para reabrir |
|---|---|
| R-09 · completar ou remover o laço de instincts (`osforge-db.py` L826-839, L1343-1505; `skills/evolve/`) | Resultado de E5. Sem ganho claro: remover `instincts`, `evolve`, `promote-instinct` e manter só a telemetria `skill-invoked`/`skill-resolved` |
| Conectar o gate de Edit/Write do GateGuard (E-A08) | Resultado de E6 |
| R-15 · worktree por onda de escrita + `git merge-tree` | Uso recorrente de ondas paralelas de escrita |
| Reabrir `.out-of-scope/claude-code-plugin-packaging.md` | Decisão de distribuir a terceiros, ou necessidade de medir um componente isolado com `claude plugin eval` (não verificado nesta auditoria) |

## Ordem de dependências

```
B-001  B-002  B-003  B-004  B-005            (independentes)
   └──────┴──────┴──→ B-006 → B-007
B-003 + B-006 ─────→ B-008        B-009
B-003 ─────────────→ B-010 → B-012 → B-013 (E1) → E2…E7
B-003 ─────────────→ B-014 → B-015 → B-016 → B-017
B-006 ─────────────→ B-018 → B-019
                     B-018 → B-020, B-022
B-013 ─────────────→ B-021, B-023, B-024, adiados
```
