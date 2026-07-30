# Análise comparativa — OSForge × `mattpocock/skills`

> **Data:** 2026-07-30 · **Fonte externa:** https://github.com/mattpocock/skills (MIT, ~193k ★)
> **Nota de idioma:** documento de análise escrito em pt-BR (mesma convenção do `docs/DECISIONS.md`).
> Conteúdo *deployado* continua em inglês por ADR-011.

---

## 0. Escopo da comparação

O repositório do Matt Pocock é **só uma biblioteca de skills** — não tem agentes, MCPs, hooks
(salvo um único guardrail de git), banco de estado, memória vetorial, rules `.mdc` ou UI generativa.
Comparar OSForge com ele nesses eixos seria injusto e inútil.

**Eixos comparados (o que o repo dele efetivamente trata):**

| # | Eixo |
|---|------|
| A | Filosofia do que é uma skill (teoria de predictability) |
| B | Eixo de invocação: model-invoked × user-invoked |
| C | Curadoria: quantas skills existem e como se aposenta uma |
| D | Tamanho de skill / progressive disclosure |
| E | Descoberta e roteamento (índice × description × router) |
| F | Modelo de domínio por projeto (`CONTEXT.md` + ADRs) |
| G | Bootstrap por repositório-alvo |
| H | Fluxo spec → tickets → triagem → implementação |
| I | Disciplina de debugging |
| J | Disciplina de TDD |
| K | Alinhamento prévio (grilling) |
| L | Design de código / arquitetura (deep modules) |
| M | Distribuição, versionamento e governança do próprio repo |
| N | Validação de que a skill dispara |

**Fora de escopo (não comparado):** 27 agentes, orquestrador, 8 MCPs, 8 hooks, `osforge-db`,
memória vetorial/Qdrant, OSForge Canvas, rules `.mdc`, operação hub/satélite, `deploy.sh` como
mecanismo de sync. Nada disso existe no repo dele.

---

## 1. O que é o repositório do Matt (leitura de fundo)

**Tese central.** GSD, BMAD e Spec-Kit "tomam o processo de você e escondem os bugs do processo".
A resposta dele é o oposto: **poucas skills, pequenas, adaptáveis, componíveis, agnósticas de modelo**.

**Números:** 14 skills publicadas no plugin, distribuídas em 6 buckets — `engineering/`,
`productivity/`, `misc/`, `personal/` (não promovido), `in-progress/` (rascunhos), `deprecated/`.
Mais um diretório `.out-of-scope/` que registra **decisões de não fazer**.

**As 4 falhas que ele ataca** (é o esqueleto do README):

1. *O agente não fez o que eu queria* → **grilling** (entrevista implacável antes de codar).
2. *O agente é verboso demais* → **linguagem ubíqua** (`CONTEXT.md`), que também dá nomes consistentes
   a variáveis/arquivos e reduz tokens de raciocínio.
3. *O código não funciona* → **feedback loops** (`tdd`, `diagnose`).
4. *Viramos uma bola de lama* → **design de código** (`improve-codebase-architecture`, deep modules).

**A peça mais valiosa do repo:** `writing-great-skills` + seu `GLOSSARY.md`. É uma teoria completa de
autoria de skills, com vocabulário próprio: *predictability, context load × cognitive load, information
hierarchy, progressive disclosure, completion criterion, legwork, leading word, single source of truth* e
os modos de falha *premature completion, duplication, sediment, sprawl, no-op*.

**Invariantes de repositório** (o `CLAUDE.md` dele, 12 linhas): toda skill em `engineering/`,
`productivity/` ou `misc/` **precisa** de entrada no README raiz, no README do bucket e no
`.claude-plugin/plugin.json`; skills em `personal/`, `in-progress/`, `deprecated/` **não podem** aparecer
em nenhum dos três. Regra checável, não conselho.

**Distribuição:** plugin oficial do Claude Code (`claude plugins install mattpocock-skills`) para quem
quer assinar as atualizações, ou `npx skills add` para quem quer forkar e editar. Changesets + CHANGELOG
+ GitHub Actions.

---

## 2. Comparativo eixo a eixo

| Eixo | `mattpocock/skills` | OSForge (estado real hoje) | Veredito |
|---|---|---|---|
| **A. Filosofia** | `writing-great-skills` + `GLOSSARY.md`: teoria explícita, vocabulário fechado | `docs/SKILL-STANDARD.md` **já importa a teoria dele** (cita nominalmente) + acrescenta *Iron Law* e o tripé `Use when / Keywords / Do NOT use for` | **Empate na teoria** — o padrão OSForge é mais completo. Perde na **aplicação** (§3) |
| **B. Invocação** | Decisão consciente e documentada; `disable-model-invocation: true` nos orquestradores | Previsto no padrão, **usado em 1 de 147 skills** | **Matt ganha** |
| **C. Curadoria** | 14 skills; buckets `in-progress/` e `deprecated/`; `.out-of-scope/` | 147 dirs de skill + ~80 `.md` avulsos; **nenhum** bucket de aposentadoria; `design-taste-frontend-v1` legado convivendo com a v2; 16 skills na órbita "design" | **Matt ganha com folga** |
| **D. Tamanho** | `SKILL.md` enxuto + disclosure (`GLOSSARY.md`, `LANGUAGE.md`, `DEEPENING.md`) | 42.291 linhas em `SKILL.md`; **média 311 linhas**; 42 skills >300; maior = 1.501 linhas. Usa disclosure (363 arquivos de referência, 25 dirs `references/`) mas ainda há *sprawl* | **Matt ganha** |
| **E. Roteamento** | Sem índice always-on; description faz o trabalho; router skill (`ask-matt`) para as user-invoked | `SKILLS.md` (~15,7 KB ≈ 4k tokens) sempre no contexto **+** descriptions nativas = dois canais para a mesma função; índice **desatualizado**: 96 das 147 skills não aparecem nele, e o header anuncia "174 skills" | **Matt ganha** na economia; OSForge ganha em previsibilidade *se* o índice for fiel |
| **F. Domínio** | Pilar do repo: `CONTEXT.md` (glossário ubíquo) + `docs/adr/`, consumidos por `tdd`, `diagnose`, `improve-codebase-architecture`, `to-issues` | **Não existe equivalente.** Há `.specs/` e `osforge-db add-decision`, mas nenhum glossário de projeto que as skills leiam | **Matt ganha — maior lacuna do OSForge** |
| **G. Bootstrap por repo** | `/setup-matt-pocock-skills` escreve bloco `## Agent skills` no CLAUDE.md do projeto + `docs/agents/{issue-tracker,triage-labels,domain}.md` | Convenções globais assumidas; sem passo de configuração por projeto-alvo | **Matt ganha** |
| **H. Spec→ticket** | `to-prd` → `to-issues` (tracer bullets, `blocked by`, rótulo **HITL/AFK**) → `triage` (máquina de estados de labels) → `implement` → `code-review`. Integra com GitHub/GitLab/`.scratch/` | 9 comandos `spec-*` + `osforge-db` com `wave`/`depends_on` e dispatch paralelo | **OSForge ganha** em paralelismo e estado. Falta dele: fatia vertical explícita, eixo **HITL/AFK** (autonomia por tarefa) e integração com issue tracker real |
| **I. Debugging** | `diagnose`: **"construa o feedback loop primeiro"** (10 táticas ranqueadas), 3–5 hipóteses **falsificáveis**, logs com tag `[DEBUG-a4f2]`, post-mortem que faz handoff para arquitetura | `systematic-debugging`: 4 fases, sem "loop primeiro", sem hipóteses falsificáveis, sem tag de limpeza, sem post-mortem | **Matt ganha** |
| **J. TDD** | Anti-pattern "horizontal slices" muito bem escrito; usa glossário de domínio nos nomes de teste; aponta para deep modules | `tdd-workflow` com **Iron Law** ("NO PRODUCTION CODE WITHOUT A FAILING TEST") + proteção de testes — coisas que o dele não tem. Mas a description tem a mesma branch escrita 6× (*duplication*) e nenhum `Do NOT use for` | **Empate** — cada um tem metade do que o outro precisa |
| **K. Grilling** | Skill dedicada (`grilling`) + variante que atualiza docs (`grill-with-docs`) + `grill-me` | 3 linhas de regra no `CLAUDE.md` + passo "Grill first" no Plan Mode | **Matt ganha** |
| **L. Arquitetura** | `improve-codebase-architecture` + `codebase-design`: glossário-contrato (*module, interface, depth, seam, adapter, leverage, locality*), **deletion test**, "a interface é a superfície de teste", relatório HTML, loop de grilling, ADR quando o usuário recusa | `clean-code`, `architecture`, `technical-design-doc-creator`. O `SKILL-STANDARD.md` **prevê** `codebase-design` — e ele não existe | **Matt ganha** |
| **M. Distribuição** | Plugin no marketplace oficial + `npx skills`; changesets, CHANGELOG, CI; invariantes de índice checáveis | `deploy.sh` (rsync local, backup, merge reconciliador de hooks) — excelente para uso pessoal; sem versionamento, changelog, CI ou empacotamento como plugin | **Matt ganha** em distribuição; **OSForge ganha** em fidelidade do deploy |
| **N. Validação** | Nenhuma | `scripts/test-skill-triggering.sh` + `skill-triggering-cases.tsv` (**~25 casos** para 147 skills; arquivo ainda em pt-BR citando o legado "ACIONE quando") | **OSForge ganha** — mas o ativo está subutilizado |

---

## 3. Diagnóstico

### 3.1 O achado principal: o padrão existe, a aplicação não

`docs/SKILL-STANDARD.md` já é um trabalho de altíssima qualidade — importa a teoria do Matt e a melhora.
Ele mesmo se declara: *"specification + examples. Nothing applied to the repo yet."* O plano de adoção
em 5 commits (§7) parou no commit 2. Medindo o acervo contra o próprio padrão:

| Regra do `SKILL-STANDARD.md` | Cobertura real |
|---|---|
| `Use when:` na description | 101 / 147 (69%) |
| `Do NOT use for:` (desambiguação) | **48 / 147 (33%)** |
| `Done when:` em cada passo (completion criterion) | **4 / 147 (3%)** |
| Eixo de invocação decidido (`disable-model-invocation`) | **1 / 147 (0,7%)** |
| Legado pt-BR (`ACIONE`) removido | 2 skills restantes |

Sem `Done when:` o modo de falha que o Matt chama de **premature completion** fica sem defesa —
justamente o modo de falha mais caro em execução autônoma por ondas, que é o diferencial do OSForge.

### 3.2 Onde o OSForge é genuinamente superior

- **Iron Law** — uma regra inviolável em maiúsculas no topo. É um *leading word* estrutural que o repo
  do Matt não tem. Manter e propagar.
- **Tripé de ativação** `Use when / Keywords / Do NOT use for` — mais rigoroso que a description dele,
  porque o "Do NOT use for" resolve colisão entre skills irmãs, e o OSForge tem 147 irmãs.
- **Harness de triggering** — o Matt não tem nada disso. É o mecanismo que torna a padronização em lote
  segura.
- **Frontmatter de execução** (`model`, `context: fork`, `agent`, `allowed-tools`) — roteamento que o
  repo dele nem tenta.
- **Dispatch por ondas com `wave`/`depends_on`** — mais avançado que os `blocked by` textuais dele.

### 3.3 Onde o OSForge perde

1. **Sem glossário ubíquo por projeto.** É a lacuna com maior retorno por token investido.
2. **Context load não gerido.** 147 descriptions + índice de 4k tokens + descriptions nativas.
3. **Sem ciclo de vida de skill.** Nada nasce "in-progress" nem morre "deprecated" — só acumula
   (*sediment*, no vocabulário dele).
4. **Índice manual e à deriva.** 96 skills fora do `SKILLS.md`; contagem anunciada (174) ≠ real (147+80).
5. **Skills grandes demais** — média 311 linhas contra o ideal de "SKILL.md legível de uma passada".

---

## 4. Recomendações

### P0 — fechar o gap entre o padrão e o acervo

**R1. Retomar o plano de adoção do `SKILL-STANDARD.md` §7, a partir do commit 3.**
Lotes por categoria, cada lote validado pelo harness.
*Aceite:* `Do NOT use for:` em 100% das skills que têm irmã de domínio próximo; `Done when:` em 100%
das skills com seção `## Process`; zero ocorrências de `ACIONE`.

**R2. Decidir o eixo de invocação de cada uma das 147 skills.**
Classificar em **ORQUESTRADOR** (só o humano invoca → `disable-model-invocation: true`, description
vira humana) e **DISCIPLINA** (o modelo alcança sozinho → description rica em gatilhos). Regra prática:
se nos últimos 3 meses a skill só foi acionada por digitação, é orquestrador.
*Aceite:* toda `SKILL.md` tem a decisão explícita; queda mensurável no total de descriptions carregadas.

**R3. Criar ciclo de vida de skill: `skills/_in-progress/` e `skills/_deprecated/`, excluídos do `deploy.sh`.**
Mover `design-taste-frontend-v1` para lá. Auditar a órbita "design" (16 skills) e consolidar por
sobreposição de gatilho.
*Aceite:* `./deploy.sh --dry-run` não copia nada dos dois buckets; ADR-014 registra a política.

**R4. Gerar `claude-code/SKILLS.md` a partir do frontmatter e travar com teste.**
`scripts/_extract_index.py` já lê todo `SKILL.md`; falta o gerador do índice de gatilhos e um check no
deploy que falhe se índice ≠ acervo (o invariante checável que o Matt tem em 3 linhas de `CLAUDE.md`).
*Aceite:* zero skills fora do índice; contagem anunciada = contagem real; `deploy.sh` aborta em drift.

### P1 — trazer o que o Matt tem de melhor

**R5. `CONTEXT.md` — linguagem ubíqua por projeto.** *(maior ganho)*
Adaptar `CONTEXT-FORMAT.md` e `ADR-FORMAT.md`; criar a skill `domain-modeling`; fazer
`tdd-workflow`, `systematic-debugging`, `code-review-checklist` e os comandos `spec-*` **lerem o
glossário do projeto** antes de nomear qualquer coisa. Encaixa direto no `osforge-db` (o glossário
pode virar um tipo de `decision` versionada) e no `.specs/project/`.
*Aceite:* um projeto satélite com `CONTEXT.md` gerado; nomes de teste e títulos de task usando os
termos canônicos.

**R6. Skill `grilling` + variante `grill-with-docs`.**
Hoje são 3 linhas de regra global — regra global é *no-op* fácil de ignorar. Como skill, ganha
gatilho, corpo e critério de conclusão ("toda branch da árvore de decisão resolvida").

**R7. Upgrade do `systematic-debugging` com o miolo do `diagnose`.**
Fase 1 = **construir o feedback loop** (as 10 táticas ranqueadas, incluindo o script HITL), hipóteses
falsificáveis ranqueadas antes de testar qualquer uma, tag `[DEBUG-xxxx]` para limpeza por grep,
post-mortem que dispara handoff para arquitetura.
*Aceite:* `Done when:` em cada fase; checklist de limpeza obrigatório antes de declarar concluído.

**R8. Criar `codebase-design` (já especificado no §6.4 do `SKILL-STANDARD.md`, nunca implementado)
e uma skill de auditoria arquitetural** com o **deletion test** e o glossário-contrato
(*module / interface / depth / seam / adapter / leverage / locality*). O relatório HTML dele mapeia
direto no OSForge Canvas.

**R9. Fatias verticais + eixo HITL/AFK no `spec-tasks`.**
Duas importações baratas e de alto valor: (a) cada task é um **tracer bullet** que atravessa todas as
camadas, nunca uma fatia horizontal; (b) cada task declara **HITL** ou **AFK**, e o dispatch por ondas
só roda sozinho as AFK — é o controle de autonomia que hoje só existe como "checkpoint por onda".

### P2 — governança e distribuição

**R10. Empacotar o OSForge como plugin do Claude Code** (`.claude-plugin/plugin.json` + marketplace
próprio), mantendo o `deploy.sh` para o uso pessoal. Permite instalar **subconjuntos** (`engineering`,
`security`, `agency`) em vez de 147 skills sempre — que é a cura estrutural do context load.

**R11. Adotar `.out-of-scope/`** — um arquivo por decisão de *não* fazer. Custo quase zero, evita
re-litigar. Complementa o `docs/DECISIONS.md` (que registra o que foi feito).

**R12. Expandir o harness** de ~25 para cobrir as 50 skills mais usadas, com prompts pt-BR e inglês, e
rodá-lo no `deploy.sh --dry-run`. Traduzir o cabeçalho do `.tsv`.

**R13. Router user-invoked (`/osforge`)** listando os comandos e skills-orquestrador — o análogo de
`ask-matt`, para pagar cognitive load em vez de context load nas skills que só o humano dispara.

---

## 5. Ordem de execução sugerida

| Onda | Itens | Por quê primeiro |
|---|---|---|
| 1 | R4, R3 | Índice fiel e ciclo de vida são pré-requisito para medir qualquer outra coisa |
| 2 | R1, R2 | Padronização em lote, protegida pelo harness já existente |
| 3 | R5, R6 | Maior ganho de qualidade por token; independentes entre si |
| 4 | R7, R8, R9 | Upgrades de disciplina, cada um isolado numa skill |
| 5 | R10, R11, R12, R13 | Governança — depende do acervo já estar limpo |

---

## 6. Uma frase

O OSForge tem **mais motor** (roteamento de modelo, agentes, ondas, estado, harness) e o repo do Matt
tem **mais disciplina** (curadoria implacável, ciclo de vida, linguagem ubíqua, critérios de conclusão).
O padrão que reconcilia os dois já está escrito em `docs/SKILL-STANDARD.md` — falta executá-lo, e
importar as três peças que ele não cobre: **`CONTEXT.md`, o `diagnose` com feedback-loop-primeiro, e
o vocabulário de deep modules**.

---

### Referências

- [mattpocock/skills — README](https://github.com/mattpocock/skills)
- [`writing-great-skills/SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md) · [`GLOSSARY.md`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/GLOSSARY.md)
- [`grill-with-docs`](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) · [`CONTEXT-FORMAT.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/CONTEXT-FORMAT.md)
- [`diagnose`](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnose/SKILL.md) · [`tdd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) · [`improve-codebase-architecture`](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md)
- [`to-issues`](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md) · [`setup-matt-pocock-skills`](https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md)
- Licença MIT — atribuição via `metadata.inspired_by`, conforme §5.C do `SKILL-STANDARD.md`
