# Needle — o que serve ao OSForge

| | |
|---|---|
| Fonte | https://github.com/cactus-compute/needle |
| SHA analisado | `42bf1f2d0a7784b0d4d1ec94bb5ade425cf9a67c` (commit de 2026-09-22) |
| Licença | Apache-2.0 (código e pesos) |
| O que é | Modelo de 35 MB para chamar ferramentas em dispositivos pequenos, com nota de confiança e embeddings; motor nativo de 0,8 MB |
| OSForge de referência | `v5.1.0` (`3f0446c`) |
| Evidências | [`EVIDENCIAS.md`](EVIDENCIAS.md) · medição: [`medicao/`](medicao/README.md) |
| Data | 2026-09-24 (leitura e medição) → 2026-09-25 (registro) |

## Veredito

**O modelo: recusado, com medição.** O único uso plausível no OSForge seria um roteador local
de skills (um hook que sugere a skill antes do Claude responder) ou um provider local de
embeddings para a memória. Medido nos 150 casos de trigger do próprio OSForge, ele não serve
para nenhum dos dois (EV-N-M01 a EV-N-M08).

**O método de avaliação: aproveitado.** As suítes de aceite do Needle impõem categorias de
caso, marcam casos críticos e validam os próprios casos sem chamar o modelo. Isso resolve uma
fraqueza real dos nossos evals, antes da primeira rodada paga (E1). Vira o candidato
[N-01](SPEC-N01-casos-de-eval.md).

## O que foi medido

Execução isolada no Mac de trabalho, com autorização explícita: venv e `HOME` temporários,
telemetria desligada, nenhuma chamada paga, tudo apagado ao final. As 47 skills core entraram
como ferramentas (nome + `description` do `SKILL.md`), sem parâmetros.

| Cenário | Acerto nos 75 positivos | Negativos com lista vazia |
|---|---|---|
| 47 core, pedido em português | 0 | 0 de 75 |
| 47 core, 1ª frase da descrição | 4 | 0 de 75 |
| 15 skills avaliadas, português | 10 | 0 de 75 |
| 47 core, pedido traduzido para inglês | 3 | — |
| 15 avaliadas, inglês | 13 | — |
| Linha de base léxica (~20 linhas), inglês | 16 top-1 · 33 top-5 | — |

Além disso:

- **A confiança não informa.** AUC acerto × erro de 0,41 e 0,47 em português (abaixo do
  acaso) e de 0,57 e 0,64 em inglês. Das 111 decisões em português com confiança ≥ 0,7 — o
  limiar de "agir" do guia deles —, 60 estavam certas (EV-N-M03).
- **Ele sempre escolhe alguma skill.** Nenhum negativo recebeu lista vazia; no cenário com 47
  ferramentas, 93 das 150 consultas foram para a mesma skill (EV-N-M02).
- **Os embeddings dele perdem da conta de palavras.** 4 top-1 / 18 top-5 em inglês, contra
  16 / 33 da linha de base léxica (EV-N-M04).
- **Partida a frio de 8,7 a 10,5 s** por processo com 47 ferramentas; o cache de índice
  documentado não gerou arquivo (EV-N-M05, EV-N09). Num hook que roda a cada prompt, isso é
  inviável sem um servidor residente.

Não é um modelo ruim; é outro problema. O Needle foi feito para até cinco ações concretas, com
parâmetros fechados e em inglês — o próprio teste deles exige no máximo cinco ferramentas por
ambiente (EV-N04) e a documentação admite que o modelo base não passa em cinco das seis
suítes de aceite (EV-N11). As skills do OSForge são intenções de trabalho abstratas, e o
usuário escreve em português.

## Problemas de operação encontrados no caminho

| Problema | Evidência |
|---|---|
| O pacote atual do PyPI (3.0.5) pede o motor 3.0.2, que **não foi publicado** no Hugging Face (só 3.0.0 e 3.0.1): o exemplo do README falha com 404 | EV-N07, EV-N-M06 |
| A biblioteca nativa é baixada em tempo de execução, da `main` do repositório de pesos, sem revisão fixa nem conferência de hash — é por isso que quebrou | EV-N07, EV-N08 |
| Telemetria ligada por padrão; a parte em Python é auditável (evento, versões, SO, id aleatório), a do binário não | EV-N12, EV-N13 |
| O código no GitHub (`pyproject` 3.0.1) não é o que está no PyPI (3.0.5) | EV-N14 |
| 1 de 150 chamadas: envelope do motor com UTF-8 truncado num caractere acentuado | EV-N-M07 |
| Pedido fora do escopo **em português** gera chamada inventada com confiança 1,0; o mesmo pedido em inglês devolve lista vazia | EV-N-M08 |
| Os dois ambientes isolados desta análise (nuvem e VM do Cowork) bloqueiam o Hugging Face | EV-N-M09 |

## O que o Needle faz melhor que o OSForge

A disciplina das suítes de aceite (EV-N01 a EV-N06):

1. Categorias de caso obrigatórias — positivo, informação faltando, irrelevante, negação,
   inválido, paralelo — e um teste **sem modelo** que reprova a suíte se faltar alguma.
2. Casos `critical`: reprovam a suíte mesmo quando o placar passa de 90%.
3. Os próprios casos são validados contra as ferramentas declaradas, sem chamar o modelo.
4. A regra de placar da suíte é fixada por testes contra um motor falso.

No OSForge, a regra de placar já é testada sem modelo (B-010, `tests/test-assertions.sh`) e
a suíte de trigger em JSON já valida seus casos. O que falta é o resto:

- os casos só dizem "deve disparar: sim/não" (EV-O-N01);
- os 75 negativos misturam 27 vizinhos, 46 irrelevantes e 2 negações sem rótulo nenhum (ver
  [`rotulos-trigger.tsv`](rotulos-trigger.tsv));
- não existe caso crítico;
- a suíte de trigger em TSV lista um caso órfão no `--dry` e sai com 0 (EV-O-N02, reproduzido);
- o `--dry` de roteamento não confere se o agente ou a skill esperados existem (EV-O-N03).

## Recusados

| O quê | Por quê |
|---|---|
| Needle como roteador local de skills | 0–13% de acerto, confiança sem sinal, sempre escolhe algo, 8–10 s de partida a frio |
| Needle como provider de embeddings | Perde para a linha de base léxica no nosso domínio; 3072 dimensões, ~80 ms por texto |
| Portão de "argumento não ancorado" (valor que não aparece no pedido) | Útil para chamadas com argumentos; as skills do OSForge não têm argumentos |
| `triggers` por regex que forçam a ferramenta | O equivalente no OSForge é a própria `description`; regex por fora duplicaria a fonte da verdade |

## Licença e método

Apache-2.0. O candidato N-01 importa uma **ideia** (categorias, casos críticos, validação sem
modelo), escrita com palavras e taxonomia próprias; nenhuma linha de código do Needle entra no
OSForge. O script de medição em [`medicao/`](medicao/README.md) é do OSForge e só roda o
Needle como programa externo.
