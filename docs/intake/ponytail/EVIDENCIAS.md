# Ponytail — evidências

**FATO** = lido no código ou recalculado · **EST** = estimativa, com a conta.

- Ponytail: `DietrichGebert/ponytail` @ `09c434ab73ca43761c5d8b0c5d341926c2fba710`; links abaixo usam
  `https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/…`
- OSForge: `v5.3.1` @ `fd2e1ffbf0349ce0337ea3ec508866faea62815f` (caminho:linha)

## O prompt e as skills (EV-P01 a EV-P09)

| ID | Onde | Fato | Tipo |
|---|---|---|---|
| EV-P01 | [`skills/ponytail/SKILL.md#L25-L30`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md#L25-L30) | A escada: precisa existir? → já existe no código → stdlib/plataforma → dependência instalada ("nunca adicione uma dependência por poucas linhas") → uma linha → o mínimo | FATO |
| EV-P02 | [`SKILL.md#L44`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md#L44) | Nunca cortar: validação na fronteira de confiança, tratamento de erro que evita perda de dados, segurança, acessibilidade, o que o usuário pediu | FATO |
| EV-P03 | [`SKILL.md#L21`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md#L21) · [`#L38`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md#L38) | Antes de escrever, listar todo lugar que a mudança precisa alcançar; em bug, procurar todos os chamadores e corrigir a causa uma vez no código compartilhado | FATO |
| EV-P04 | [`SKILL.md#L41-L42`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md#L41-L42) | Piso de teste para lógica não trivial; atalho com limite conhecido leva comentário `shortcut: <limite>, <quando trocar>` | FATO |
| EV-P05 | [`SKILL.md#L5`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md#L5) | A descrição diz "use em qualquer tarefa de código" | FATO |
| EV-P06 | [`skills/ponytail-review/SKILL.md#L21`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-review/SKILL.md#L21) · [`#L26`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-review/SKILL.md#L26) | Review lê o diff **e** o código que ele toca (chamadores, chamados, testes); declara a carga esperada que assumiu | FATO |
| EV-P07 | [`ponytail-review/SKILL.md#L59`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-review/SKILL.md#L59) · [`#L64`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-review/SKILL.md#L64) | Sem caso concreto, não há achado; um `shortcut:` declarado é decisão, não achado, salvo se a carga já o ultrapassa | FATO |
| EV-P08 | [`ponytail-review/SKILL.md#L91`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-review/SKILL.md#L91) | Achado em quatro partes: o que é, problema, correção, "se não corrigir" | FATO |
| EV-P09 | [`skills/ponytail-audit/SKILL.md#L16`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-audit/SKILL.md#L16) · [`#L84`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-audit/SKILL.md#L84) | Audit: mapa primeiro (entradas, fluxos, carga); no máximo 20 achados, dizendo quantos ficaram de fora | FATO |

## O que roda (EV-P10 a EV-P19)

| ID | Onde | Fato | Tipo |
|---|---|---|---|
| EV-P10 | [`hooks/claude-codex-hooks.json#L3`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/claude-codex-hooks.json#L3) | `SessionStart` (início, retomada, clear, compact) imprime o corpo do SKILL.md e um mapa do repo de até 2000 caracteres. O SKILL.md tem 3.496 bytes; ~1,2–1,5 mil tokens por sessão | FATO · EST |
| EV-P11 | [`hooks/claude-codex-hooks.json#L16`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/claude-codex-hooks.json#L16) · [`hooks/ponytail-subagent.js#L26`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/ponytail-subagent.js#L26) | `SubagentStart` injeta as regras em todo subagente | FATO |
| EV-P12 | [`hooks/ponytail-activate.js#L149`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/ponytail-activate.js#L149) | Sem `statusLine` configurado, o hook diz ao modelo para "oferecer proativamente" editar o `settings.json` | FATO |
| EV-P13 | [`hooks/ponytail-config.js#L42`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/ponytail-config.js#L42) | A mensagem inteira "stop ponytail" ou "normal mode" desliga o modo | FATO |
| EV-P14 | [`hooks/band/register.tsx#L339`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/band/register.tsx#L339) | A faixa é um módulo de UI de plugin (`AbovePrompt`), não um hook nem statusline; grava CSV e reconstrói um HTML local a cada turno | FATO |
| EV-P15 | [`hooks/band/metrics.ts#L92`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/band/metrics.ts#L92) · [`register.tsx#L246`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/band/register.tsx#L246) | "Teste rodou" = regex no comando; "passou" = o comando não terminou em erro | FATO |
| EV-P16 | [`register.tsx#L276`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/band/register.tsx#L276) · [`metrics.ts#L14-L23`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/band/metrics.ts#L14-L23) | O "✓ testes" só fica desatualizado quando Edit/Write toca py, js/ts, go, rs ou rb; reuso é regex sobre nomes | FATO |
| EV-P17 | [`.claude-plugin/plugin.json#L33-L36`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/.claude-plugin/plugin.json#L33-L36) | Webhook opcional (desligado por padrão); se ligado, manda nomes de tarefa por padrão (`sendNames: true`) | FATO |
| EV-P18 | [`package.json#L38`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/package.json#L38) | `node --test tests/*.test.js`: `tests/band.test.tsx` não roda no CI | FATO |
| EV-P19 | [`hooks/ponytail-band-import.js#L17`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/ponytail-band-import.js#L17) | Tabela de preços embutida, "conferida em 2026-10-17" | FATO |

## O benchmark (EV-P20 a EV-P29)

| ID | Onde | Fato | Tipo |
|---|---|---|---|
| EV-P20 | [`benchmarks/results/2026-10-07-agentic.md`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/results/2026-10-07-agentic.md) (tabela por tarefa) | Recalculado (média geométrica do custo, Ponytail 5 ÷ sem skill): todas −25,9% (bate com o README); **verificação escondida (18) −1,0%, mais caro em 8**; repo (12) −41,9%; apps pequenos (5) −52,3%; exemplos (3) −28,0% | FATO |
| EV-P21 | commit `88cedeb` (2026-10-10), mesmo arquivo | Removeu a seção "Limitations": "21 de 39 tarefas não têm verificação de correção", "a classificação de teste é decisão minha", "as ferramentas de teste e mutação não estão no repositório" | FATO |
| EV-P22 | [`benchmarks/agentic/run.py#L313-L314`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/agentic/run.py#L313-L314) | As 12 tarefas de repositório real contam como corretas se a execução adicionou qualquer linha | FATO |
| EV-P23 | [`README.md#L99`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/README.md#L99) | "100% dos problemas plantados, 87% sem a skill" só existe no texto alternativo da imagem; não há tarefa de review no benchmark | FATO |
| EV-P24 | [`2026-10-07-agentic.md#L68-L71`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/results/2026-10-07-agentic.md#L68-L71) | Segurança: os três braços passaram 30/30; "less code did not cost correctness or safety. It did not add any either" | FATO |
| EV-P25 | [`2026-10-07-agentic.md#L121`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/results/2026-10-07-agentic.md#L121) | Comparação cega das respostas, Ponytail 5 × sem skill: 82 a 106 (p = 0,09), favorável a **sem skill** | FATO |
| EV-P26 | [`benchmarks/agentic/tasks.py#L1493`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/agentic/tasks.py#L1493) | "candidate pool … screened baseline-vs-ponytail, keep the clear winners" | FATO |
| EV-P27 | [`benchmarks/agentic/run.py#L332`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/agentic/run.py#L332) | Linha de base isolada (CLAUDE.md desligado) — boa prática, a mesma do `judge.py` do OSForge | FATO |
| EV-P28 | [`.gitignore#L24`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/.gitignore#L24) | Os resultados por execução não são versionados; só medianas por tarefa | FATO |
| EV-P29 | [`2026-10-07-agentic.md#L42`](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/results/2026-10-07-agentic.md#L42) | O "−45% de tokens" é só de tokens de **saída** | FATO |
| — | `benchmarks/agentic/tasks.py` | Zero ocorrências de Next.js, Prisma ou Supabase | FATO |

## OSForge (EV-O-P) — `v5.3.1`

| ID | Onde | Fato | Tipo |
|---|---|---|---|
| EV-O-P01 | `skills/coding-guidelines/SKILL.md`, `skills/clean-code/SKILL.md` | Nenhuma ocorrência de dependência, stdlib ou plataforma nativa | FATO |
| EV-O-P02 | `skills/coding-guidelines/SKILL.md:27-35`, `:77` | "Simplicity First" inclui "no error handling for impossible scenarios", sem lista do que nunca se corta; "Read Before You Write" pede ler o arquivo e vizinhos, não os chamadores | FATO |
| EV-O-P03 | `skills/quality/code-review/SKILL.md:29-37` | Escopo do review = arquivos modificados, "o diff inteiro" | FATO |
| EV-O-P04 | `skills/quality/code-review/SKILL.md:96-115` | Veredito: Issues / Suggestions / Positives, sem consequência por achado nem premissa de carga | FATO |
| EV-O-P05 | `skills/**/SKILL.md` com `name: *audit` | Só `ui-audit` e `redesign-audit`; não há auditoria de código do repositório | FATO |
| EV-O-P06 | `claude-code/SKILLS.md:19-22` | Resumo sempre carregado de `coding-guidelines` (simplicidade, cirúrgico, orientado a meta) | FATO |
| EV-O-P07 | `docs/evals/2026-10-17-claude-opus-5-5-skill-outcome-r2-fable-judge.md:36, 103, 162, 221, 278, 330` | Rodada 2: `clean-code` ajuda; os outros cinco alvos neutros | FATO |
| EV-O-P08 | `CHANGELOG.md:137` | Auditoria por chamada (B-028): custo, tokens e tempo já registrados | FATO |
| EV-O-P09 | `docs/BACKLOG-EVOLUCAO.md:186` | E1: positivos de trigger 1/30 | FATO |
| EV-O-P10 | `scripts/evals/outcome/driver.py:4`, `:547` | Eval de resultado com três braços que diferem só no `--append-system-prompt`; rodadas aceitas: r1, r2 | FATO |
| EV-O-P11 | `docs/evals/…-r2-fable-judge.md:14`, `:16` | Rodada 2: 360 chamadas, 38,33 em dólar-equivalente da assinatura, pico de 24% da janela de 5 h | FATO |
| EV-O-P12 | `scripts/evals/outcome/driver.py` (`TASKS`), `scripts/evals/outcome/tasks_r2.py` | Alvos medidos até hoje: r1 `clean-code`, `frontend-design`, `adversarial-review`; r2 `clean-code`, `verification-before-completion`, `behavioral-modes`, `output-enforcement`, agentes `planner` e `code-reviewer`. `coding-guidelines` e `code-review` nunca | FATO |
