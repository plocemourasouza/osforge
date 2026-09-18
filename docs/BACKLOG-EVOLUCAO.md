# Backlog de evolução do OSForge

Derivado de [`ANALISE-COMPARATIVA-ECC.md`](ANALISE-COMPARATIVA-ECC.md); evidências em [`ANALISE-COMPARATIVA-ECC-EVIDENCIAS.md`](ANALISE-COMPARATIVA-ECC-EVIDENCIAS.md).
Base: OSForge `d87a9bfc2058df233d30a2637fe252efb3256894`. Caminhos relativos à raiz do repositório. **(NOVO)** marca arquivo proposto que ainda não existe.
Esforço: **P** até meio dia · **M** 1–3 dias · **G** 3–7 dias, para quem conhece o repositório.
Todos os comandos de verificação rodam com `HOME` temporário; nenhum toca `~/.claude`.

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

### B-004 · Revisor: tirar a cota de achados, pôr o gate pré-relatório
- **Recomendação / evidência:** R-12 · E-A42; origem `agents/code-reviewer.md:39-74` do ECC (MIT)
- **Arquivos:** `skills/quality/adversarial-review/SKILL.md` L85-88; `agents/code-reviewer.md`; `THIRD_PARTY_NOTICES` **(NOVO)**.
- **Mudança:** remover "HALT if zero findings" e "findings < 10"; acrescentar o gate de quatro perguntas, exigência de prova para HIGH/CRITICAL, a cláusula "zero achados é um resultado válido" e a lista de falsos positivos, reescritos no `SKILL-STANDARD`, com `inspired_by` e aviso MIT.
- **Aceite:** harness de acionamento continua disparando a skill; experimento E4 agendado.
- **Esforço:** P. **Risco:** revisor ficar leniente — é o que E4 mede.

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

### B-008 · CI mínimo + checagem de contagens — ✅ feito (CI ainda não executado no GitHub)
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

### B-010 · Fixar modelo e repetições nos dois harnesses
- **Recomendação / evidência:** R-08 · E-A45
- **Arquivos:** `scripts/test-skill-triggering.sh`, `scripts/test-orchestrator-routing.sh`, `scripts/lib/harness-assertions.sh`, `tests/test-assertions.sh`.
- **Mudança:** flags `--model` (obrigatória fora de `--dry`) e `--runs N` (padrão 3); relatório por caso = k de N; asserção de skill exige nome da ferramenta e caminho **no mesmo evento**; dimensão agente exige despacho (`Agent/Task`) quando o caso esperar delegação; opção `--home DIR` para rodar contra um deploy limpo.
- **Aceite:** `tests/test-assertions.sh` cobre os dois modos novos com streams sintéticos; nenhuma chamada de API no teste offline.
- **Esforço:** M.

### B-011 · Ativar o eval de trigger que já existe
- **Recomendação / evidência:** R-08 · E-A46
- **Arquivos:** `skills/skill-creator/scripts/run_eval.py`, `run_loop.py`; **(NOVO)** `scripts/evals/trigger/<skill>.json` com consultas positivas e negativas; **(NOVO)** `scripts/run-trigger-eval.sh`.
- **Mudança:** 5 positivas + 5 negativas escritas à mão para as 47 core, começando por 15; divisão 60/40 ajuste/avaliação registrada no arquivo.
- **Aceite:** `--dry` lista os casos sem chamar modelo; uma rodada real gera `docs/evals/<data>-<modelo>-trigger.md`.
- **Esforço:** M (a maior parte é escrever casos).

### B-012 · Versionar resultados de eval
- **Arquivos (NOVOS):** `docs/evals/README.md`, `docs/evals/<data>-<modelo>-<suite>.md`.
- **Conteúdo mínimo:** SHA do OSForge, id do modelo, comando, casos, k de N por caso, tokens e tempo totais. Substitui os números soltos em `claude-code/CLAUDE.md:49-50`, `hooks/route-guard.py:7-8` e na análise do Matt.
- **Esforço:** P.

### B-013 · Rodar E1 (estabilidade) e decidir E2–E4
- **Recomendação:** §8.2 do relatório. **Dependências:** B-003, B-010, B-012. **Custo:** API — fazer piloto de 2 casos antes. **Saída:** lista de casos instáveis e ruído por suíte, que vira o limiar de decisão dos demais experimentos.

## Etapa 3 — Consolidação

### B-014 · `scripts/osforge-state.py` + install-state
- **Recomendação / evidência:** R-03 · E-A27 a E-A30; origem E-B01, E-B02, E-B04
- **Arquivos:** **(NOVO)** `scripts/osforge-state.py`; `deploy.sh` (`copy_file`, `copy_dir`, `backup_file`, laço de hooks L323-329, cópia do canvas, `deploy_skills`).
- **Mudança:** esquema `osforge.install.v1` do relatório §5.3; registro de `{dst, src, sha256}`; backup em `~/.claude_backups/<run_id>/<relativo>`; regra de propriedade (não registrado e diferente → pula e avisa; registrado e alterado → backup + aviso, sobrescreve com `--force`); modo adoção na primeira execução.
- **Dependências:** B-003.
- **Aceite:** ver B-017.
- **Esforço:** M–G. **Risco:** estado corrompido → escrita atômica; ausência de estado = modo adoção.

### B-015 · Merge de hooks por id com recusa de drift
- **Recomendação / evidência:** R-03 · E-A27; origem E-B01
- **Arquivos:** `deploy.sh` `merge_hooks_claude` L96-143 e `merge_settings_claude` L146-194.
- **Mudança:** id = `evento|matcher|basename(comando)`; remove só entrada idêntica à gravada no estado; id gravado com conteúdo diferente → aborta mostrando diff (`--force-hooks`); itera eventos do estado **e** do repositório; escrita em temporário + `mv`; um único backup por execução.
- **Aceite:** hook do usuário em `~/.claude/hooks/meu.sh` sobrevive; hook do OSForge editado à mão faz o deploy parar; evento removido do repositório some do `settings.json`.
- **Esforço:** M.

### B-016 · `--doctor`, `--uninstall`, `--restore <run_id>`; poda por estado
- **Recomendação / evidência:** R-03 · E-A29; origem E-B04
- **Arquivos:** `deploy.sh`, `scripts/osforge-state.py`.
- **Mudança:** `deploy_skills` troca `rsync --delete` por cópia + poda do que estava no estado anterior e saiu da allowlist; mesma poda para agentes, comandos e scripts de hook; excluir `hooks/validate.py` do glob L323 (mover para `docs/templates/`).
- **Aceite:** skill instalada por `install-skill.sh --global` sobrevive ao deploy; agente removido do repositório some do destino; `--uninstall` deixa só o que era do usuário e restaura valores anteriores das settings.
- **Esforço:** M.

### B-017 · Teste de ciclo de vida do deploy
- **Arquivos (NOVO):** `tests/test-deploy-lifecycle.sh` (roteiro do relatório §5.3, HOME temporário; usa `rsync` real se existir).
- **Aceite:** verde; entra no CI de B-008.
- **Esforço:** P–M.

### B-018 · Identidade de projeto única
- **Recomendação / evidência:** R-04 · E-A19, E-A20, E-A26; origem E-B08
- **Arquivos:** **(NOVO)** `hooks/lib/project_id.py`; `hooks/observe-capture.py` L117-121; `hooks/session-save.py` L60-82; `hooks/session-resume.sh` L36-56; `scripts/osforge-db.py` (esquema `projects`, `cmd_upsert_project`, migração).
- **Mudança:** ordem de resolução `OSFORGE_PROJECT` → raiz do git casada com `projects.root_path` → `projects.remote_hash` (sha256 do remote normalizado, sem credenciais) → basename normalizado; `ALTER TABLE projects ADD COLUMN root_path/remote_hash`; honrar de fato a variável `OSFORGE_DB`.
- **Aceite:** pastas homônimas com remotes diferentes → slugs diferentes; subdiretório e worktree → mesmo projeto; projetos já registrados continuam resolvendo.
- **Esforço:** M.

### B-019 · Retomada com guarda, teto, escopo e limpeza
- **Recomendação / evidência:** R-04 · E-A21 a E-A24, E-A14; origem E-B07
- **Arquivos:** `hooks/session-resume.sh` L59-94; `hooks/session-save.py` L106-109, L138-195; `hooks/observe-capture.py` L102-108; `scripts/osforge-db.py` L382-404, L596-601, L1555/L1569; **(NOVO)** `hooks/lib/scrub.py`.
- **Aceite:** os seis casos de R-04 no relatório §5.3, como casos de `tests/hooks/` e de banco temporário.
- **Esforço:** M. **Dependências:** B-018, B-006.

### B-020 · Dreno do feedback do Canvas + validação no servidor
- **Recomendação / evidência:** R-05 · E-A43, E-A44; origem E-B06
- **Arquivos:** **(NOVO)** `hooks/canvas-feedback.py`; `hooks/hooks-claude-code.json` (Stop); `scripts/canvas/server.ts` L176-196, L291-314; `skills/osforge-canvas/SKILL.md` L99-137; **(NOVO)** `tests/canvas/` com o roteiro `curl` desta auditoria.
- **Aceite:** feedback pendente do projeto atual → Stop bloqueia uma vez com o conteúdo; outro cwd, `stop_hook_active`, já entregue e servidor fora do ar → passa; POST para artefato inexistente, `revision` divergente, `action` fora do enum ou Origin não-loopback → 4xx.
- **Esforço:** M. **Dependências:** B-018 (slug), B-006.

## Etapa 4 — Conforme os experimentos

### B-021 · Aviso de contexto pelo uso real
- **Recomendação / evidência:** R-06 · E-B19. **Arquivos:** **(NOVO)** `hooks/context-threshold.py`; `hooks/hooks-claude-code.json`; espinha de `claude-code/SKILLS.md` L117-146. **Aceite:** transcripts sintéticos de 100k/125k/155k → 0/1/2 avisos, um por faixa por sessão; < 40 ms por chamada. **Esforço:** P.

### B-022 · Tokens por sessão e por projeto
- **Recomendação / evidência:** R-10 · E-B27. **Arquivos:** `hooks/session-save.py`; `scripts/osforge-db.py` (tabela `usage`, `cmd_board`). **Aceite:** transcript com a mesma `message.id` em duas linhas conta uma vez; tokens separados por modelo; `board` mostra o total do projeto. **Esforço:** P. **Dependências:** B-018.

### B-023 · Plano proporcional e arquivos do orquestrador
- **Recomendação / evidência:** R-14 · E-A38, E-A40, E-A28. **Arquivos:** `claude-code/CLAUDE.md` L126, L140; `agents/orchestrator/AGENT.md` L126-137, L432-437; `deploy.sh` `copy_dir` (ou embutir `triage-rules.md`); `scripts/routing-cases.tsv` (casos de piso). **Aceite:** depois do experimento E3; `~/.claude/agents/orchestrator/` contém os arquivos citados ou o `AGENT.md` não os cita mais. **Esforço:** P.

### B-024 · Rules com escopo; unicode; atenuação de negações
- **R-11 (parte imediata):** `alwaysApply: false` nas rules de stack em `rules/*.mdc`. **R-11 (condicionada):** gerar `~/.claude/rules/osforge/` em `deploy_claude` só depois de confirmar o carregamento com `measure-context.py` numa sessão real.
- **R-16:** **(NOVO)** `scripts/check-unicode.py` no preflight e sobre `sources/`.
- **R-02:** `_deny` em `hooks/gateguard.py` encurta a mensagem a partir da 4ª negação da sessão.
- **Esforço:** P cada.

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
