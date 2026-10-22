# Ponytail × OSForge — cobertura de comportamento

Cada coisa que o Ponytail faz, como ele faz, onde o OSForge (`v5.3.1`) já cobre e o que fazemos
com ela. "Camada" remete a [`ARQUITETURA.md`](ARQUITETURA.md). Evidências em
[`EVIDENCIAS.md`](EVIDENCIAS.md).

**Situação:** ✅ coberto · ◐ parcial · ✗ ausente · ▲ o OSForge já faz melhor.

## 1. Regras de comportamento (o prompt)

| # | O Ponytail faz | Como | OSForge hoje | Situação | Decisão |
|---|---|---|---|---|---|
| 1 | Escada: precisa existir? → já existe no repositório → stdlib/plataforma → dependência instalada → uma linha → o mínimo | Lista ordenada no prompt (EV-P01) | "Minimum code", sem ordem de origem; nada sobre stdlib, plataforma ou dependência nova (EV-O-P01) | ✗ | **Camada 1** — P-01 |
| 2 | "Nunca adicione dependência por poucas linhas" | Uma frase (EV-P01) | Ausente | ✗ | Camada 1 — P-01 |
| 3 | Nunca cortar: validação de fronteira, perda de dados, segurança, acessibilidade, o que foi pedido | Lista fechada (EV-P02) | "No error handling for impossible scenarios", sem contrapeso (EV-O-P02) | ✗ | Camada 1 — P-01 |
| 4 | Antes de escrever, listar tudo que a mudança alcança: chamadores, testes, fixtures, config, exports | Instrução (EV-P03) | "Read Before You Write": arquivo e vizinhos, não chamadores (EV-O-P02) | ◐ | Camada 1 — P-01 + **Camada 2** (G-1 confere de fato) |
| 5 | Bug: procurar todos os chamadores e corrigir a causa uma vez no código compartilhado | Instrução (EV-P03) | Ausente em `coding-guidelines`; `systematic-debugging` trata causa raiz, não chamadores | ◐ | Camada 1 — P-01 |
| 6 | Código movido ou fundido mantém validação e tratamento de erro | Instrução | Ausente | ✗ | Camada 1 — P-01 (uma linha) |
| 7 | Entre opções do mesmo tamanho, a correta nas bordas | Instrução | `edge-case-hunter` (sob demanda) | ◐ | Camada 1 — P-01 (uma linha) |
| 8 | Piso de teste para lógica não trivial | Instrução (EV-P04) | Lei do TDD sempre carregada, mais exigente (`SKILLS.md`) | ▲ | Não importar |
| 9 | Atalho com limite conhecido leva `shortcut: <limite>, <quando trocar>` | Convenção (EV-P04) | Ausente | ✗ | Camada 1 — P-01 |
| 10 | Comentar só o porquê, em uma linha | Instrução | `clean-code` § Comments | ✅ | — |
| 11 | Pedido vago → menor versão que faz o essencial | Instrução (EV-P01) | `requirements-clarify` pergunta antes; `coding-guidelines` §1 "ask when unclear" | ▲ | Não importar (perguntar é o comportamento do OSForge) |
| 12 | Terminar toda resposta com "o que pulei / que risco" | Instrução (EV-P39) | `verification-before-completion` (evidência antes de "pronto") | ◐ | Só no `code-review` (P-02) |

## 2. Como as regras chegam ao modelo

| # | O Ponytail faz | Como | OSForge hoje | Situação | Decisão |
|---|---|---|---|---|---|
| 13 | Regras sempre ativas na sessão | `SessionStart` imprime o SKILL.md inteiro (~1,2–1,5 mil tokens) a cada início, retomada, clear e compact (EV-P10) | Resumo da lei em `SKILLS.md`, importado pelo CLAUDE.md global | ▲ | Manter o modelo do OSForge; P-01 acrescenta ~40 tokens ao resumo |
| 14 | Regras em todo subagente | `SubagentStart` injeta ~3 KB (EV-P11) | Subagentes já recebem o CLAUDE.md global: **270 de 277** subagentes que escreveram código tinham o resumo; só **10** carregaram a skill `coding-guidelines` inteira (EV-M-P01, EV-C-P05) | ◐ | O que falta é **conteúdo** no resumo, não um canal novo. Se P-01 ganhar, vai para o resumo, que já chega a 97% dos subagentes que codam |
| 15 | Nível por projeto (lite/full/ultra) persistido | Arquivo por hash do diretório (EV-P35) | `behavioral-modes` + alavanca de esforço (v5.3.0) | ✅ | — |
| 16 | Desligar com "stop ponytail" / "normal mode" | Frase exata (EV-P13) | Variáveis `OSFORGE_*=off` por mecanismo | ✅ | — |
| 17 | Badge no statusline | Script próprio + sugestão ao modelo de editar `settings.json` (EV-P12) | O statusline é seu; o OSForge não o toca | — | Não importar; a faixa da Camada 3 substitui |

## 3. Contexto que ajuda a reusar

| # | O Ponytail faz | Como | OSForge hoje | Situação | Decisão |
|---|---|---|---|---|---|
| 18 | Mapa do repositório no início da sessão: exports por pasta, código compartilhado primeiro, 2000 caracteres | `git ls-files` + regex por linguagem (EV-P30) | `project-context-generator` (sob demanda), glossário `CONTEXT.md`, memória | ◐ | **Candidato condicionado**: testar na r3 como braço (o mapa no prompt muda o reuso?) antes de pôr ~500 tokens em toda sessão |

## 4. Guardas durante a edição

| # | O Ponytail faz | Como | OSForge hoje | Situação | Decisão |
|---|---|---|---|---|---|
| 19 | "Chamadores abertos": definição removida ou renomeada que ainda é chamada | No fim do turno, `git grep` de cada nome removido (EV-P31) — **só para o humano**, na faixa (EV-P33) | Nada | ✗ | **Camada 2** — G-1, e **para o modelo**, no momento do Edit |
| 20 | "Duplicata?": definição nova com o mesmo nome normalizado de uma existente em outro arquivo | Comparação de nomes (EV-P32), só na faixa | Nada | ✗ | Camada 2 — G-2, para o modelo |
| 21 | Estado dos testes: passou / falhou / desatualizado desde a última mudança | Regex no comando + código de saída; desatualiza só em 6 linguagens (EV-P15, EV-P16) | Lei de verificação (texto) | ◐ | Camada 2 — G-3, com detecção pelo `package.json` e sinal para o monitor |
| 22 | Reuso % | Regex sobre nomes usados × criados (EV-P16) | Nada | ✗ | Não importar como número (frágil); G-2 cobre a parte que importa |

## 5. Revisão, auditoria e dívida

| # | O Ponytail faz | Como | OSForge hoje | Situação | Decisão |
|---|---|---|---|---|---|
| 23 | Review lê o código conectado, declara a carga, exige caso concreto, achado em 4 partes | Skill (EV-P06–P08) | `code-review` cobre o diff (EV-O-P03) | ◐ | Camada 1 — P-02 |
| 24 | Auditoria do repositório inteiro, ranqueada | Skill (EV-P09) | Só auditorias de UI (EV-O-P05) | ✗ | Camada 1 — P-03 |
| 25 | Livro de dívida: todos os `shortcut:`; marca os que não dizem quando trocar | Skill com `git grep` (EV-P34) | Ausente | ✗ | Camada 1 (seção do `repo-audit`) + **Camada 3** (contador no monitor) |
| 26 | "Gain": placar do benchmark | Cartão fixo | — | — | Não importar (marketing, não medida do repositório) |

## 6. Visual

| # | O Ponytail faz | Como | OSForge hoje | Situação | Decisão |
|---|---|---|---|---|---|
| 27 | Faixa acima do prompt: nível, custo, último turno, média, tokens, tempo de agente, reuso, chamadores abertos, testes; botões Review/Audit/Board/Detalhes/Copiar | Módulo de UI de plugin, `AbovePrompt` (EV-P14) | Nada visual; os dados existem (`calls`, `usage`, `quota.json`) | ✗ | **Camada 3** — faixa própria do OSForge, com **andamento do projeto** |
| 28 | Painel: sessões, tempo, custo, tokens por período, tabela de sessões, mapa de atividade e sequência de dias | HTML estático reconstruído a cada turno a partir de CSV (EV-P14, EV-P37) | `osforge-db board` (texto): tarefas e tokens por projeto | ◐ | Camada 3 — painel no servidor do Canvas, sobre o `osforge-db` |
| 29 | Importar sessões antigas | Lê `~/.claude/projects`; custo = maior entre total próprio e estimativa (EV-P38) | `calls` já tem 33.840 chamadas desde 2026-08-23 (EV-M-P02) | ▲ | Não importar |
| 30 | Exportar a linha da tarefa por webhook | Opcional; manda nomes por padrão se ligado (EV-P17) | — | — | Não importar agora |

## 7. Distribuição

| # | O Ponytail faz | Como | OSForge hoje | Situação | Decisão |
|---|---|---|---|---|---|
| 31 | "Funciona com 20 agentes" | São **ferramentas hospedeiras** (Cursor, Codex, Gemini…), não subagentes: o repositório não define nenhum agente (EV-P36) | Claude Code + Cursor, 25 agentes próprios | — | Fora do escopo. Não há "agents" do Ponytail a incorporar |

## Resumo

| Situação | Itens |
|---|---|
| Ausente, entra (sujeito a medição) | 1, 2, 3, 6, 9, 19, 20, 24, 25, 27 |
| Parcial, complementa | 4, 5, 7, 12, 14, 18, 21, 23, 28 |
| Coberto ou melhor no OSForge | 8, 10, 11, 13, 15, 16, 29 |
| Não importar | 17, 22, 26, 30, 31 |
