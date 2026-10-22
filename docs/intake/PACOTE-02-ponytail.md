# Pacote 02 — Ponytail, incorporação incremental e medida

**Estado:** proposta, aguardando aprovação. **Fonte:** [Ponytail](ponytail/ANALISE.md) (MIT, `09c434a`).
**Base:** OSForge `v5.3.1`. **Ids propostos no backlog:** B-031 a B-034.
**Evidências:** `EV-P…` e `EV-O-P…` em [`ponytail/EVIDENCIAS.md`](ponytail/EVIDENCIAS.md).

## Em uma frase

Do Ponytail entram três mecanismos que o OSForge não tem, e cada um só fica depois de ganhar
no eval de resultado que o OSForge já usa:

- a escada que decide **de onde** sai a solução;
- um review que lê também quem chama o código alterado;
- uma auditoria do repositório inteiro.

O plugin em si não entra, porque competiria com o OSForge pelas mesmas regras, hooks e roteamento.

## O pacote

| Id | Item | Spec | Esforço | Chamadas pagas |
|---|---|---|---|---|
| B-031 | Rodada r3 do eval de resultado: instrumento aceita `r3`, 13 tarefas no stack, rubricas e variantes | [MEDICAO-r3](ponytail/MEDICAO-r3.md) | M | 0 para preparar |
| B-032 | Escada da solução + "nunca cortar" + atalho declarado em `coding-guidelines` | [P-01](ponytail/SPEC-P01-escada-da-solucao.md) | P | — |
| B-033 | `code-review` lê os chamadores, declara a carga, exige caso concreto e diz "se não corrigir" | [P-02](ponytail/SPEC-P02-review-codigo-conectado.md) | P | — |
| B-034 | `repo-audit`, skill sob demanda (fora do core) | [P-03](ponytail/SPEC-P03-repo-audit.md) | P–M | — |

```
B-031 preparar r3 (offline) ──→ piloto (2 chamadas) ──→ r3 (234 ou 342 chamadas, autorização)
                                                             │
                     ┌───────────────────────────────────────┼─────────────────────┐
                     ▼                                       ▼                     ▼
            B-032 se C > B                          B-033 se C > B        B-034 se B > A e B > C
                     └──────────────→ release 5.4.0 com o que ganhou ←─────────────┘
```

## O que ganhamos

| Hoje | Com o pacote |
|---|---|
| As regras de código dizem "escreva pouco", mas não dizem de onde tirar a solução; nada sobre stdlib, plataforma ou dependência nova (EV-O-P01) | Uma ordem explícita, com exemplos do nosso stack: `Intl`, `crypto.randomUUID()`, `<input type="date">`, Zod e Prisma já instalados, antes de instalar ou escrever |
| "Simplifique" sem contrapeso escrito (EV-O-P02) | Uma lista do que nunca se corta: validação de fronteira, perda de dados, segurança, acessibilidade |
| O review cobre o diff (EV-O-P03); o chamador quebrado fora dele passa | O review segue a mudança até quem a chama, e cada achado diz a consequência de não corrigir |
| Não há auditoria de código do repositório inteiro (EV-O-P05) | `repo-audit` sob demanda, com mapa primeiro, achados ranqueados, máximo de 20 e checklist do stack (service role no cliente, tabela sem RLS, dinheiro em `float`) |
| `coding-guidelines` e `code-review`, duas das skills mais usadas, nunca foram medidas (EV-O-P12) | A r3 mede as duas pela primeira vez (B − A), mesmo que as mudanças sejam recusadas |
| Alegações do Ponytail que o repositório dele não sustenta (EV-P20 a EV-P26) | Uma medição própria, no nosso stack, com juiz cego e critérios críticos |

E o que evitamos: dois prompts globais brigando, ~1,2–1,5 mil tokens por sessão, mais ~3 KB em
cada subagente (EV-P10, EV-P11), um hook pedindo ao modelo para editar o seu `settings.json`
(EV-P12) e uma faixa com "✓ testes" que pode mentir (EV-P15, EV-P16).

## Custo

- **Preparar:** zero chamadas.
- **Medir:** 234 chamadas (~25 em dólar-equivalente da assinatura), ou 342 (~36) com o
  braço de referência do Ponytail original. Piloto de 2 chamadas antes.
- **Adotar:** zero chamadas. A única mudança sempre carregada é ~40 tokens no resumo de
  `SKILLS.md`, e só se P-01 ganhar.

## Pronto quando

1. r3 rodada e relatório versionado em `docs/evals/`.
2. Só o que ganhou foi aplicado. O que não ganhou está registrado como recusado, com o número.
3. Suítes, manifesto e contagens verdes; `THIRD_PARTY_NOTICES` com o Ponytail; ADR-019;
   CHANGELOG; release pelo fluxo da ADR-018.

## Decisões pendentes

| Id | Decisão | Recomendação |
|---|---|---|
| D-P1 | Incluir o braço `ponytail-ref` (Ponytail original contra a nossa adaptação) | Sim: +108 chamadas, e responde se a adaptação perdeu o que funcionava |
| D-P2 | Autorizar a r3 (piloto + rodada) | Depois de B-031 pronto e do `--dry` limpo |
| D-P3 | Modelo executor | `claude-opus-5-5`, o mesmo da r2, para comparar com a série |
