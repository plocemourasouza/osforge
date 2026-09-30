# L-04 · O que o Laya diz sobre o R-09 (laço de *instincts*)

**Tipo:** insumo de decisão, não implementação.
**Evidência:** EV-L21 a EV-L28 (Laya) · EV-O10, EV-O13 (OSForge).

## Onde estamos

O R-09 está **adiado até o E5**: completar o laço de *instincts* ou removê-lo
(`BACKLOG-EVOLUCAO.md`, "Adiados"). No OSForge o laço termina no `evolve`: a tabela
`instincts` tem confiança com limite, escopo projeto/global, contagem de ocorrências e
promoção só com confiança ≥ 0,8, mas **nada injeta um instinct de volta numa sessão**
(EV-O10). A análise do ECC já desenhou o caminho barato caso o E5 justifique: injeção no
`session-resume.sh` (top N ≥ 0,7, projeto antes de global, teto rígido), alimentada por sinais
**rotulados** — bloqueios do `route-guard`, negações do GateGuard, erro→correção — e não por
frequência de ferramenta (EV-O13).

## O que o Laya mostra

O Laya fechou um laço equivalente e o mantém em produção: correções explícitas do usuário
viram regras em linguagem natural, que voltam ao prompt do classificador.

| Como funciona | Evidência |
|---|---|
| Um agendador verifica a cada 6 h; aprende quando um escopo junta ≥ 15 correções não processadas (10 no laço de contexto), em lotes de até 50 | EV-L21, EV-L22 |
| A regra é uma frase gravada com `source = 'learned'`; manual e aprendida convivem na mesma tabela | EV-L23 |
| Consolidação por LLM acima de 40 regras aprendidas, com uma guarda boa: se o resultado não for **menor**, nada é trocado | EV-L24 |
| Injeção: as 20 mais recentes, como texto "(always follow these)" no prompt do roteador | EV-L25, EV-L26 |

E é aí que ele degrada — cada ponto abaixo está no código, não é hipótese:

1. **A regra é só texto sugerido.** Nada executa ou verifica uma regra aprendida; ela vai para
   o prompt de um modelo de triagem e o resto é esperança (EV-L26).
2. **O aprendido expulsa o manual.** A injeção pega as 20 mais recentes **sem selecionar
   `source`**; regras aprendidas novas empurram para fora as que o usuário escreveu à mão, e o
   modelo não tem como distinguir uma da outra (EV-L25).
3. **Escopo que falha aberto.** Quando o item não tem espaço, a consulta cai no ramo sem
   filtro e devolve as regras ativas de **todos** os espaços (EV-L25).
4. **Consolidação presa à extração.** Só roda logo depois de aprender algo novo; um escopo que
   para de receber correções nunca é consolidado (EV-L24).
5. **Sem confiança, sem decaimento, sem contradição.** A única defesa contra duplicata é uma
   instrução no prompt do extrator (EV-L27); a justificativa que o modelo dá é truncada num log
   e descartada.
6. **Sem registro de uso.** As tabelas de regras aprendidas não têm contagem nem data de
   disparo; o próprio Laya tem esse registro — para as regras **determinísticas**, não para as
   aprendidas (EV-L23, EV-L28).

## Consequência para o OSForge

**Recomendação: manter o R-09 adiado, e mudar o que o E5 exige antes de rodar.**

O ponto 6 é o decisivo: sem saber **quais** instincts foram injetados em **qual** sessão, o E5
não tem como medir ganho — compararia sessões sem saber o que cada uma recebeu. Então, se o E5
for rodar, o primeiro passo não é completar o laço, é o **registro de injeção**:

- tabela `instinct_injections(session_id, instinct_id, injected_at)`, gravada pelo
  `session-resume.sh` no momento em que injeta;
- ligação com L-03 pela `session_id`, para cruzar injeção com custo e com os sinais rotulados
  que vierem depois (negação, bloqueio, correção).

E, se o E5 justificar completar, o caminho barato do ECC ganha estas exigências, uma para cada
defeito acima:

| Defeito no Laya | Exigência no OSForge |
|---|---|
| 1 texto sugerido | Instinct injetado declara o sinal que o originou e é **medido** pelo registro de injeção; sem efeito mensurável em N sessões → rebaixa |
| 2 aprendido expulsa manual | Precedência fixa: manual/promovido global → promovido de projeto → candidato; teto por camada, nunca um teto único |
| 3 escopo aberto | Projeto não resolvido → **nenhuma** injeção de projeto (falha fechada) |
| 4 consolidação presa | Consolidação independente (comando próprio), com a guarda do Laya: só troca se o resultado for menor |
| 5 sem contradição | Antes de gravar, procurar instinct do mesmo gatilho com orientação oposta → não grava, marca conflito para o usuário |
| 6 sem uso | `seen_count` já existe; somar `last_injected_at` e decaimento de confiança sem uso |

**Se o E5 não justificar:** o Laya reforça o ramo "remover `instincts`, `evolve` e
`promote-instinct` e manter só a telemetria de skill" — um laço de regras sugeridas, mesmo bem
feito e em uso, não traz prova de que melhora o resultado.

## O que o OSForge já tem que o Laya não tem

Confiança com `CHECK` entre 0 e 1, escopo explícito, contagem de ocorrências e promoção com
limiar (EV-O10). O desenho de dados do OSForge é mais cuidadoso; o que falta é o laço e,
principalmente, a medição.
