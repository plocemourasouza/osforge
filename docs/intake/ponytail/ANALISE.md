# Ponytail — o que entra no OSForge, e como

| | |
|---|---|
| Fonte | https://github.com/DietrichGebert/ponytail |
| SHA analisado | `09c434ab73ca43761c5d8b0c5d341926c2fba710` (commit de 2026-10-18) |
| Licença | MIT (© 2026 DietrichGebert) |
| O que é | Um prompt de "dev sênior preguiçoso" (`skills/ponytail/SKILL.md`, 52 linhas) mais review, audit, uma faixa de métricas no Claude Code e manifestos para ~20 agentes |
| OSForge de referência | `v5.3.1` (`fd2e1ff`) |
| Evidências | [`EVIDENCIAS.md`](EVIDENCIAS.md) |
| Data | 2026-10-22 |

## Veredito

**Não instalar o plugin. Importar três mecanismos, e só depois de medi-los com o eval de
resultado que o OSForge já tem.**

O plugin, instalado ao lado do OSForge, competiria com ele em quatro pontos:

- injeta persona e regras de resposta em toda sessão e em todo subagente (EV-P10, EV-P11);
- pede ao modelo que edite o seu `settings.json` (EV-P12);
- grava arquivos a cada turno (EV-P14);
- disputa o roteamento com uma skill que se declara "para qualquer tarefa de código" (EV-P05).

O roteamento é justamente o ponto fraco medido no E1: 1 de 30 positivos (EV-O-P09). Os números
de benefício do README medem menos do que dizem (seção abaixo). O que sobra, e não temos, é
pouco e é bom:

| Id | Candidato | O que o OSForge ganha | Spec |
|---|---|---|---|
| P-01 | **Escada da solução** em `coding-guidelines` | Uma ordem de preferência antes de escrever código: precisa existir? → já existe no repo? → stdlib ou plataforma → dependência já instalada → mínimo que funciona. Mais uma lista do que **nunca** se corta e um piso de teste para lógica não trivial. Hoje nenhuma das duas skills de código fala de stdlib, plataforma ou dependência nova (EV-O-P01) | [SPEC-P01](SPEC-P01-escada-da-solucao.md) |
| P-02 | **Review que lê o código conectado** em `code-review` | Hoje o escopo é "o diff inteiro" (EV-O-P03). Passa a incluir quem chama o que mudou, a carga esperada como premissa declarada, caso concreto obrigatório por achado e o "se não corrigir" de cada um | [SPEC-P02](SPEC-P02-review-codigo-conectado.md) |
| P-03 | **`repo-audit`**, skill sob demanda | Não existe auditoria de código do repositório inteiro, só de UI (EV-O-P05). Mapa primeiro, achados ranqueados, no máximo 20, e "não verificado" no fim | [SPEC-P03](SPEC-P03-repo-audit.md) |

As três passam pelo mesmo crivo, uma rodada do eval de resultado (r3) descrita em
[`MEDICAO-r3.md`](MEDICAO-r3.md). Esse crivo é necessário porque o OSForge já sabe que texto
de skill frequentemente não muda nada: na rodada 2, cinco de seis alvos ficaram neutros
(EV-O-P07), e nem `coding-guidelines` nem `code-review` foram medidos até hoje (EV-O-P12). Entra o que bater o próprio ruído; o resto fica registrado como recusado.

## O que o Ponytail mede de verdade

O benchmark (39 tarefas, Opus 5.5, 5 execuções) é melhor que a média dos projetos do gênero.
Usa a CLI pura como linha de base, conta linhas com script e tem verificações escondidas
em 18 tarefas. Mas o README conta mais do que os dados sustentam:

| O README diz | O que os dados do próprio repositório mostram |
|---|---|
| −53% de código, −26% de custo | Consistente com a tabela por tarefa. Mas o ganho de custo vem quase todo das tarefas **sem** verificação de correção. Nas 18 com verificação escondida o custo cai ~1% (EV-P20, EV-P22) |
| "98% da lógica arriscada sai com teste", "66% dos bugs injetados pegos" | A classificação de "precisa de teste" é manual e as ferramentas de teste e mutação **não estão no repositório**. A seção de limitações que dizia isso foi apagada depois da publicação (EV-P21) |
| Review: "100% dos problemas plantados, 87% sem a skill" | Não existe tarefa, harness nem dado; o número está só no texto alternativo de uma imagem (EV-P23) |
| "Passou nas 30 execuções de segurança" | As três condições passaram 30/30, inclusive sem a skill. O próprio relatório diz que "os três braços empatam" (EV-P24) |
| Respostas melhores, 110 a 67 | Contra o Ponytail anterior. Contra **nenhuma skill**, o juiz preferiu a resposta sem skill: 106 a 82, número que o README não mostra (EV-P25) |
| Tarefas | As do grupo de "apps pequenos", onde está o maior efeito, foram triadas para "manter os vencedores claros" (EV-P26). Nas 12 tarefas de repositório real, conta como "correto" qualquer execução que tenha adicionado alguma linha (EV-P22). Nenhuma tarefa usa Next.js, Prisma ou Supabase |

Leitura honesta: o prompt deixa o código mais curto e mais barato **sem piorar** o que o
benchmark verifica. Que ele **melhore** qualidade, testes ou review não está demonstrado. É
exatamente o tipo de alegação que a ADR-015 manda medir antes de adotar.

## Recusados

| O quê | Por quê |
|---|---|
| Instalar o plugin | Os quatro conflitos acima; cerca de 1,2–1,5 mil tokens por sessão, mais ~3 KB por subagente. No OSForge, 75% das chamadas são de subagentes (EV-M04 do Laya), então esse custo pesa |
| A faixa ("band") e o painel ("board") | Exigem a API de módulos de UI de plugin, que o deploy do OSForge não usa. Os números são frágeis: "testes passaram" vem de regex no comando e no código de saída, e só fica desatualizado em seis linguagens; "reuso %" é regex sobre nomes. O teste da faixa não roda no CI (EV-P15 a EV-P18). O OSForge já tem os dados de custo, tokens e tempo na tabela `calls` (B-028, EV-O-P08) |
| Formato fixo de fim de resposta ("o que pulei, que risco existe") | O OSForge já tem regra equivalente onde importa (`verification-before-completion`), e P-02 a leva ao `code-review`; impor em toda resposta seria mais um bloco sempre carregado |
| Modos lite/full/ultra, `/ponytail-gain`, `/ponytail-debt` | Já há `behavioral-modes`; os outros dois são variações do audit |

## Licença e proveniência

MIT, compatível. As specs reescrevem os mecanismos no padrão do `SKILL-STANDARD`; se alguma
frase for mantida literalmente (o exemplo de achado em quatro partes é o candidato óbvio), o
aviso entra em `THIRD_PARTY_NOTICES` e o frontmatter leva `inspired_by`, como foi feito com
o ECC.

## Método

Leitura do código no SHA fixado; o runtime (hooks, faixa, rede, instalação) e o benchmark
(método, dados, números recalculados a partir da tabela publicada) foram lidos também por dois
leitores independentes. Cada afirmação usada aqui foi reconferida no arquivo e está em
`EVIDENCIAS.md`. Nada do Ponytail foi executado. Nenhuma chamada de modelo foi feita.
