# Pacote 02 — Ponytail: comportamento, guardas e monitor de andamento (revisão 2)

**Estado:** proposta, aguardando aprovação. **Fonte:** [Ponytail](ponytail/ANALISE.md) (MIT, `09c434a`).
**Base:** OSForge `v5.3.1`. **Ids propostos no backlog:** B-031 a B-038.
**Leitura recomendada:** [`ponytail/COBERTURA.md`](ponytail/COBERTURA.md) (o que ele trata e como,
item a item) e [`ponytail/ARQUITETURA.md`](ponytail/ARQUITETURA.md) (como encaixa e as alternativas).
**Evidências:** `EV-P…`, `EV-C-P…`, `EV-M-P…`, `EV-O-P…` em [`ponytail/EVIDENCIAS.md`](ponytail/EVIDENCIAS.md).

## Em uma frase

O Ponytail não traz agentes; os "20 agentes" do README são ferramentas hospedeiras. O que ele
tem de valioso é um conjunto de regras de escrita e três guardas que hoje só aparecem na tela
dele. O pacote traz isso para o OSForge em três camadas:

1. **regras**, onde o modelo de fato as lê;
2. **guardas**, que avisam o modelo no momento do erro;
3. **um monitor visual** do andamento de cada projeto, construído sobre os dados que o
   OSForge já tem.

## Como o fluxo de trabalho muda

| Momento | Hoje | Com o pacote |
|---|---|---|
| Antes de escrever | "Escreva pouco", sem dizer de onde tirar a solução | Escada: repositório → stdlib/plataforma → dependência instalada; nunca dependência por poucas linhas; nunca cortar validação, perda de dados, segurança e acessibilidade (P-01). Talvez também um mapa do repositório (se ganhar na r3) |
| Durante a edição | Nada observa o que foi quebrado | O modelo é avisado no ato: "você renomeou `formatPrice`; ainda é chamado em 2 lugares", "já existe `formatCurrency` em `lib/format.ts`" (P-04) |
| Antes de dizer "pronto" | Lei de verificação, sem dado de quando os testes rodaram | O estado dos testes (passou / falhou / desatualizado) é registrado e visível (P-04) |
| Revisão | O review cobre o diff | Também os chamadores fora do diff, a carga assumida e "se não corrigir"; mais auditoria do repositório inteiro e livro de atalhos (P-02, P-03) |
| Acompanhamento | `osforge-db board` em texto, ou perguntar ao modelo | Faixa no Claude Code e painel local com fase, tarefas, bloqueios, decisões, consumo, janela de 5 h e alertas de qualidade (P-05) |

## O pacote

| Id | Item | Camada | Spec | Esforço | Chamadas pagas |
|---|---|---|---|---|---|
| B-031 | Rodada r3 do eval de resultado (inclui o braço do mapa) | 1 | [MEDICAO-r3](ponytail/MEDICAO-r3.md) | M | 0 para preparar |
| B-032 | Escada da solução em `coding-guidelines` + resumo em `SKILLS.md` | 1 | [P-01](ponytail/SPEC-P01-escada-da-solucao.md) | P | — |
| B-033 | `code-review` com código conectado | 1 | [P-02](ponytail/SPEC-P02-review-codigo-conectado.md) | P | — |
| B-034 | `repo-audit` sob demanda, com livro de atalhos | 1 | [P-03](ponytail/SPEC-P03-repo-audit.md) | P–M | — |
| B-035 | Guardas de edição (`quality-guard`) + tabela `signals`, em modo sombra | 2 | [P-04](ponytail/SPEC-P04-guardas-de-edicao.md) | M | 0 |
| B-036 | Contrato `osforge-db monitor --json` + painel `/monitor` no Canvas | 3 | [P-05](ponytail/SPEC-P05-monitor.md) | M | 0 |
| B-037 | Faixa `osforge-monitor` no Claude Code | 3 | [P-05](ponytail/SPEC-P05-monitor.md) | M | 0 |
| B-038 | Painel lateral (`Pane`) — opcional | 3 | [P-05](ponytail/SPEC-P05-monitor.md) | P–M | 0 |

**Ordem:**

1. B-031, B-035 (sombra) e B-036, em paralelo, todos offline.
2. A r3, com autorização. Pelo resultado: B-032, B-033 e B-034 entram ou são recusados.
3. Guardas ligadas ao modelo, se a sombra aprovar.
4. B-037; depois, B-038.
5. Release 5.4.0 pelo fluxo da ADR-018.

Esforço total: 5 a 9 dias, mais as duas semanas de sombra correndo em paralelo.

## O que ganhamos

- **Comportamento.** As regras que faltam (9 de 12 estão ausentes ou incompletas, COBERTURA §1)
  entram no resumo que já chega a 270 de 277 subagentes que codam. Não precisa de canal novo nem
  de ~3 KB por subagente.
- **Erros pegos no ato.** Chamador quebrado e código duplicado viram aviso ao modelo no Edit,
  não um alerta numa tela que ele não vê, como no Ponytail.
- **Visão do projeto.** Fase, tarefas, bloqueios e decisões, com consumo e janela, a partir de
  dados que já existem: 9 projetos, 292 tarefas, 33.840 chamadas.
- **Um achado de brinde:** 25% das chamadas não têm projeto identificado. O monitor mostra isso,
  e passa a ser corrigível.
- **Nada adotado sem medição.** Regras pela r3; guardas por duas semanas de sombra; monitor por
  testes de correção dos números.

**O que evitamos:**

- dois prompts globais em conflito;
- um hook pedindo ao modelo para editar o seu `settings.json`;
- um segundo livro-razão em CSV;
- uma faixa com "✓ testes" que pode mentir;
- uma dependência da API de UI *early access* no caminho crítico.

## Custo

- **Implementar:** zero chamadas de modelo. Quatro suítes novas, todas offline.
- **Medir a Camada 1:** 288 chamadas (~31 em dólar-equivalente da assinatura); 396 (~42) com o
  braço do Ponytail original. Piloto de 2 chamadas antes.
- **Sempre carregado:** +~40 tokens no resumo (se P-01 ganhar); +~500 por sessão só se o mapa
  ganhar.

## Decisões pendentes

| Id | Decisão | Recomendação |
|---|---|---|
| D-P1 | Braço do Ponytail original na r3 | Sim (+108 chamadas): mostra se a adaptação perdeu algo |
| D-P2 | Autorizar a r3 | Depois do `--dry` limpo |
| D-G1 | Guardas para outras linguagens além de TS/JS/Python | Não agora |
| D-G2 | Lembrar o modelo no `Stop` quando os testes estão desatualizados | Depois da sombra |
| D-M1 | Como entregar a faixa | Pasta própria + `CLAUDE_CODE_PLUGIN_DIRS` gerenciado pelo deploy |
| D-M2 | Painel lateral | Depois de usar a faixa e o painel por algumas semanas |
