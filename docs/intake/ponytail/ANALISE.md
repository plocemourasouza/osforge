# Ponytail — o que entra no OSForge, e como (revisão 2)

| | |
|---|---|
| Fonte | https://github.com/DietrichGebert/ponytail |
| SHA analisado | `09c434ab73ca43761c5d8b0c5d341926c2fba710` (commit de 2026-10-18) |
| Licença | MIT (© 2026 DietrichGebert) |
| OSForge de referência | `v5.3.1` (`fd2e1ff`) |
| Documentos | [`COBERTURA.md`](COBERTURA.md) (31 comportamentos, um a um) · [`ARQUITETURA.md`](ARQUITETURA.md) · specs P-01 a P-05 · [`MEDICAO-r3.md`](MEDICAO-r3.md) · [`EVIDENCIAS.md`](EVIDENCIAS.md) |
| Data | 2026-10-22 |

**O que mudou da revisão 1:**

- o inventário passou a cobrir **todas** as estruturas do Ponytail, inclusive mapa do
  repositório, guardas da faixa, livro de dívida e painel;
- medimos, nos transcripts reais, o que chega aos subagentes do OSForge;
- estudamos a API de UI do Claude Code que a faixa usa;
- o resultado é uma proposta em três camadas, com monitor de andamento do projeto.

## O que é o Ponytail, estrutura por estrutura

| Estrutura | O que é de fato | Decisão | Por quê |
|---|---|---|---|
| **"Funciona com 20 agentes"** | São **20 ferramentas hospedeiras** (Cursor, Codex, Gemini, Copilot…), cada uma com um adaptador que carrega o mesmo prompt. O repositório **não define nenhum agente** no sentido do OSForge, isto é, nenhum subagente com papel próprio (EV-P36) | Nada a incorporar | Não existe esse artefato. O OSForge tem 25 agentes próprios e já atende Claude Code e Cursor |
| Injeção em subagentes (`SubagentStart`) | Põe ~3 KB de regras em todo subagente (EV-P11) | Não importar o canal; **importar o conteúdo** | Medimos: o resumo do OSForge já chega a **270 de 277** subagentes que escreveram código, e a skill `coding-guidelines` inteira a só 10 (EV-M-P01). O que falta é o que o resumo diz, não um canal novo |
| Regras do prompt (escada, nunca cortar, chamadores, atalho declarado…) | 52 linhas (EV-P01–P04) | **Camada 1**: P-01, medido na r3 | 9 das 12 regras faltam ou estão incompletas no OSForge (COBERTURA §1) |
| Ativação na sessão, níveis, desligar | `SessionStart` + arquivos de modo (EV-P10, EV-P13, EV-P35) | Não importar | O OSForge já tem o equivalente: resumo sempre carregado, `behavioral-modes` e `OSFORGE_*=off` |
| Mapa do repositório | Exports por pasta, 2000 caracteres, no início da sessão (EV-P30) | **Camada 1, condicionado**: braço próprio na r3 | Pode aumentar o reuso, mas custa ~500 tokens por sessão; só entra se ganhar |
| Review, audit, livro de dívida | Skills (EV-P06–P09, EV-P34) | **Camada 1**: P-02, P-03 (com o livro de atalhos) | O review do OSForge para no diff; não existe auditoria do repositório inteiro |
| Guardas da faixa (chamadores abertos, duplicata, testes) | Calculados no turno e mostrados **só ao humano** (EV-P31–P33) | **Camada 2**: P-04, como hooks que avisam o **modelo** no ato | É a parte mais valiosa do Ponytail, e o OSForge não tem nada parecido |
| Faixa e painel | Módulo de UI de plugin + HTML estático sobre CSV (EV-P14, EV-P37) | **Camada 3**: P-05, monitor próprio sobre o `osforge-db` | Mostram a **sessão**; você quer o **andamento do projeto**, e esses dados o OSForge já tem (EV-M-P02) |
| Import de sessões, webhook, "gain" | Utilitários (EV-P17, EV-P38) | Não importar | A tabela `calls` já tem 33.840 chamadas; o "gain" é placar de benchmark, não medida do repositório |

## Proposta em três camadas

Detalhe e alternativas em [`ARQUITETURA.md`](ARQUITETURA.md).

1. **Regras (Camada 1):** P-01 escada, P-02 review conectado, P-03 `repo-audit`, e o mapa como
   candidato. Entram só se ganharem na r3 do eval de resultado.
2. **Guardas (Camada 2):** P-04, um hook `PostToolUse` que avisa o modelo, no próprio Edit,
   quando ele quebrou um chamador ou recriou algo que já existe, e registra o estado dos testes.
   Entra primeiro em modo sombra, e a injeção só liga com alarme falso medido baixo.
3. **Monitor (Camada 3):** P-05. Um contrato de dados (`osforge-db monitor --json`) e duas vistas:
   - **Painel** no servidor do Canvas: fases, tarefas, bloqueios, decisões, consumo, janela e
     qualidade.
   - **Faixa** no Claude Code: fase, tarefa em andamento, progresso, bloqueios, custo, janela e
     alertas.

## O que o benchmark do Ponytail mede de verdade

O harness é sério: CLI pura como linha de base (EV-P27), linhas contadas por script e
verificação escondida em 18 tarefas. Mas o README conta mais do que os dados sustentam:

| O README diz | O que os dados do próprio repositório mostram |
|---|---|
| −53% de código, −26% de custo | Bate com a tabela por tarefa. Mas o custo cai só **1%** nas 18 tarefas com verificação de correção, e sobe em 8 delas (recalculado, EV-P20). As 12 tarefas de repositório real contam como corretas se adicionaram qualquer linha (EV-P22) |
| "98% da lógica arriscada sai com teste", "66% dos bugs injetados pegos" | Classificação manual; as ferramentas de teste e mutação não estão no repositório. A seção que admitia isso foi apagada depois da publicação (EV-P21) |
| Review: "100% dos problemas plantados, 87% sem a skill" | Não existe tarefa nem dado; só o texto alternativo de uma imagem (EV-P23) |
| "Passou nas 30 execuções de segurança" | As três condições passaram 30/30, inclusive sem a skill (EV-P24) |
| Respostas melhores, 110 a 67 | Contra a versão anterior. Contra **nenhuma skill**, o juiz preferiu sem skill: 106 a 82 (EV-P25) |
| Tarefas | O grupo de maior efeito foi triado para "manter os vencedores claros" (EV-P26); nenhuma tarefa em Next.js, Prisma ou Supabase |

Leitura: o prompt encurta o código sem piorar o que o benchmark verifica. Que ele melhore
qualidade não está demonstrado. Por isso cada peça passa pela nossa medição antes de entrar.

## Licença e proveniência

MIT, compatível. O texto das regras é reescrito; o layout do painel pode partir do `board.ts`
(MIT). Tudo com `inspired_by` e aviso em `THIRD_PARTY_NOTICES`, como foi feito com o ECC.

## Método

Leitura do código no SHA fixado; runtime e benchmark lidos também por dois leitores
independentes, com cada afirmação reconferida no arquivo. Números do benchmark recalculados da
tabela publicada. A API de UI do Claude Code foi lida na referência e nos tipos da versão
2.1.308; o comportamento de subagentes, na documentação e em 321 transcripts reais. Nada do
Ponytail foi executado e nenhuma chamada de modelo foi feita.
