# Eval · trigger · claude-sonnet-5

- **Data (UTC):** 2026-09-29T22:12:21Z · duração 735 s
- **Modelo:** `claude-sonnet-5`
- **OSForge:** v5.1.0 · `c8d8b84` · **árvore suja**
- **HOME usado:** `/Users/paulosouza`
- **Execuções por caso:** 3
- **Comando:** `./scripts/run-trigger-eval.sh`
- **Tokens:** in 0 · out 0 · cache_read 0 · cache_create 0

## Críticos reprovados

- `requirements-clarify/p5+` — FAIL (0/3): deve disparar · Faz o sistema ficar seguro.

**Resultado:** 44/73 PASS (60 %) · FAIL 28 · FLAKY 1

**Por categoria:** `vizinho` 6/6 PASS · `negacao` 13/13 PASS · `irrelevante` 24/24 PASS · `positivo` 1/30 PASS

Um caso só é PASS quando acerta nas N execuções. `0 < k < N` é **FLAKY**: instável,
não aprovado — é esta lista que o experimento E1 consome.

| Caso | Categoria | k de N | Veredito | Detalhe |
|---|---|---|---|---|
| `adversarial-review/p4+` | positivo | 0/3 | FAIL | deve disparar · O que um revisor implicante acharia de errado aqui? |
| `adversarial-review/p5+` | positivo | 0/3 | FAIL | deve disparar · Procura o que está FALTANDO nesse desenho, não o que está es |
| `brainstorming/p4+` | positivo | 0/3 | FAIL | deve disparar · Quero explorar formas de monetizar a base que já tenho, sem  |
| `brainstorming/p5+` | positivo | 0/3 | FAIL | deve disparar · Pensei numa feature de comunidade dentro do produto. Vale a  |
| `clean-code/p4+` | positivo | 0/3 | FAIL | deve disparar · Esse componente faz coisa demais. Como quebro sem quebrar o  |
| `clean-code/p5+` | positivo | 0/3 | FAIL | deve disparar · Herdei esse código e quero deixá-lo apresentável antes de me |
| `code-review/p4+` | positivo | 0/3 | FAIL | deve disparar · O PR do estagiário está aberto há dois dias. Consegue revisa |
| `code-review/p5+` | positivo | 0/3 | FAIL | deve disparar · Olha esse commit e me diz o que você mudaria. |
| `domain-modeling/p4+` | positivo | 0/3 | FAIL | deve disparar · Quero deixar explícito no código quais estados de contrato s |
| `domain-modeling/p5+` | positivo | 0/3 | FAIL | deve disparar · As regras de negócio estão espalhadas pelos controllers. Ond |
| `edge-case-hunter/p4+` | positivo | 0/3 | FAIL | deve disparar · Quero mapear todos os caminhos infelizes antes de escrever o |
| `edge-case-hunter/p5+` | positivo | 0/3 | FAIL | deve disparar · Essa API assume que o array nunca vem vazio. O que mais ela  |
| `frontend-design/p5+` | positivo | 0/3 | FAIL | deve disparar · A hierarquia visual dessa página está confusa para o usuário |
| `grilling/p4+` | positivo | 0/3 | FAIL | deve disparar · Me faz as perguntas que o meu tech lead faria nesse desenho. |
| `grilling/p5+` | positivo | 0/3 | FAIL | deve disparar · Quero fechar todas as decisões em aberto desse plano antes d |
| `osforge-canvas/p4+` | positivo | 0/3 | FAIL | deve disparar · Monta uma visão do escopo para eu comentar em cima, item por |
| `osforge-canvas/p5+` | positivo | 0/3 | FAIL | deve disparar · Quero dar feedback estruturado nesse desenho, não responder  |
| `prd-builder/p4+` | positivo | 0/3 | FAIL | deve disparar · Já decidimos a ideia; agora quero requisitos e critérios de  |
| `prd-builder/p5+` | positivo | 0/3 | FAIL | deve disparar · Preciso alinhar produto e engenharia sobre o que é a versão  |
| `requirements-clarify/p4+` | positivo | 0/3 | FAIL | deve disparar · Quero integrar com o ERP deles. |
| `requirements-clarify/p5+` | positivo | 0/3 | FAIL | deve disparar · Faz o sistema ficar seguro. |
| `system-diagrams/p5+` | positivo | 0/3 | FAIL | deve disparar · Consigo ver o relacionamento entre as tabelas principais num |
| `systematic-debugging/p4+` | positivo | 0/3 | FAIL | deve disparar · Tem um vazamento de memória no worker e eu não consigo repro |
| `systematic-debugging/p5+` | positivo | 0/3 | FAIL | deve disparar · Depois do deploy de ontem os webhooks pararam. Preciso achar |
| `tdd-workflow/p4+` | positivo | 0/3 | FAIL | deve disparar · Quero escrever a função de parcelamento hoje e não quebrar o |
| `tdd-workflow/p5+` | positivo | 0/3 | FAIL | deve disparar · Vamos fazer o endpoint de refund. Prefiro ir devagar e com s |
| `verification-before-completion/p4+` | positivo | 0/3 | FAIL | deve disparar · Já testei na minha máquina e funcionou. É suficiente? |
| `verification-before-completion/p5+` | positivo | 0/3 | FAIL | deve disparar · Vou marcar como concluído. Tem algum passo que eu costumo es |
| `system-diagrams/p4+` | positivo | 1/3 | FLAKY | deve disparar · Mostra visualmente o caminho de um pedido desde o checkout a |
| `adversarial-review/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Traduz o documento para inglês. |
| `adversarial-review/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Resume esse spec em cinco bullets. |
| `adversarial-review/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não precisa criticar nada, só confere se o spec tem todas as |
| `brainstorming/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Quais são os planos e preços do Supabase hoje? |
| `brainstorming/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Faz o deploy da branch de staging. |
| `brainstorming/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não quero discutir a ideia, já está decidida; só me diz por  |
| `clean-code/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Faz o build de produção e me diz o tamanho do bundle. |
| `clean-code/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Escreve a documentação da API pública. |
| `clean-code/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não mexe na estrutura nem nos nomes; só corrige o erro de di |
| `code-review/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Gera o changelog da versão 2.1. |
| `code-review/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Roda o prettier em tudo. |
| `code-review/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não precisa revisar, só faz o commit do que está staged. |
| `domain-modeling/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Qual ORM tem melhor suporte a Postgres? |
| `domain-modeling/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Arruma o import quebrado no arquivo de tipos. |
| `domain-modeling/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não quero repensar o modelo; só adiciona a coluna status na  |
| `edge-case-hunter/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Aumenta o timeout do teste e2e. |
| `edge-case-hunter/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Configura o coverage no CI. |
| `edge-case-hunter/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não precisa caçar caso de borda, é só um protótipo para a de |
| `frontend-design/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Otimiza as imagens do diretório public. |
| `frontend-design/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Corrige o erro de hidratação no Next. |
| `frontend-design/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não quero opinião de design; só troca a cor do botão para o  |
| `frontend-design/p4+` | positivo | 2/3 | PASS | deve disparar · Preciso definir a cara do produto antes de sair montando com |
| `grilling/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Gera os testes e2e do fluxo de login. |
| `grilling/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Resume essa thread de e-mail em três linhas. |
| `grilling/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não me interroga, o plano já foi aprovado; só executa o prim |
| `osforge-canvas/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Quais componentes do shadcn eu já uso no projeto? |
| `osforge-canvas/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Corrige o CSS do header que quebrou no mobile. |
| `prd-builder/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Faz um diagrama de sequência do login. |
| `prd-builder/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Qual o preço do plano enterprise do Linear? |
| `prd-builder/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não precisa de documento formal; é uma mudança de uma linha  |
| `requirements-clarify/n4-` | vizinho | 3/3 | PASS | NÃO deve disparar · Adiciona o campo created_at na tabela orders, tipo timestamp |
| `requirements-clarify/n5-` | vizinho | 3/3 | PASS | NÃO deve disparar · Faz commit do que está staged com a mensagem 'fix: corrige m |
| `requirements-clarify/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não me pergunta nada: troca o timeout do fetch de 5 para 10  |
| `system-diagrams/n4-` | vizinho | 3/3 | PASS | NÃO deve disparar · Exporta esse gráfico de vendas em PNG. |
| `system-diagrams/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Qual biblioteca de gráficos combina com shadcn? |
| `systematic-debugging/n4-` | vizinho | 3/3 | PASS | NÃO deve disparar · Qual a diferença entre erro 502 e 504? |
| `systematic-debugging/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Adiciona um log de auditoria quando o usuário troca a senha. |
| `systematic-debugging/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não precisa investigar a causa, só reverte o último commit q |
| `tdd-workflow/n4-` | vizinho | 3/3 | PASS | NÃO deve disparar · Qual a diferença entre Vitest e Jest em performance? |
| `tdd-workflow/n5-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Preciso de um resumo do que mudou no último release do Prism |
| `tdd-workflow/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Sem testes agora, é um script descartável para migrar uns da |
| `verification-before-completion/n4-` | irrelevante | 3/3 | PASS | NÃO deve disparar · Explica o que é integração contínua. |
| `verification-before-completion/n5-` | vizinho | 3/3 | PASS | NÃO deve disparar · Abre um PR com as mudanças atuais. |
| `verification-before-completion/n6-` | negacao | 3/3 | PASS | NÃO deve disparar · Não precisa verificar nada, isso é só um rascunho que eu vou |

## Casos instáveis (entrada do E1)

`system-diagrams/p4+`
