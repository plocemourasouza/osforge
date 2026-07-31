# Análise comparativa — OSForge × `mattpocock/skills`

> **Fonte externa:** https://github.com/mattpocock/skills (MIT, ~193k ★) · leitura de 2026-07-30
> **Revisão 2** — a v1 foi escrita antes de auditar o repositório; vários números estavam errados
> e três recomendações já estavam parcialmente implementadas. Correções em §7.
> **Idioma:** análise em pt-BR (mesma convenção do `docs/DECISIONS.md`); conteúdo deployado
> continua em inglês por ADR-011.

---

## 0. Escopo da comparação

O repositório do Matt Pocock é **só uma biblioteca de skills** — não tem agentes, MCPs, hooks
(salvo um guardrail de git), banco de estado, memória vetorial, rules `.mdc` ou UI generativa.
Comparar OSForge com ele nesses eixos seria inútil.

**Comparado:** filosofia de autoria de skill · eixo de invocação · curadoria e ciclo de vida ·
tamanho e progressive disclosure · descoberta e roteamento · modelo de domínio por projeto ·
bootstrap por repositório · fluxo spec→ticket→implementação · debugging · TDD · grilling ·
design de código · distribuição e governança · validação de triggering.

**Fora de escopo:** 27 agentes, orquestrador, MCPs, hooks, `osforge-db`, Qdrant, Canvas,
rules `.mdc`, operação hub/satélite, `deploy.sh` como mecanismo de sync.

---

## 1. O que é o repositório do Matt

**Tese:** GSD, BMAD e Spec-Kit "tomam o processo de você e escondem os bugs do processo". A resposta
dele é o oposto — **poucas skills, pequenas, adaptáveis, componíveis, agnósticas de modelo**.

**Números:** 14 skills publicadas, 6 buckets (`engineering/`, `productivity/`, `misc/`, `personal/`,
`in-progress/`, `deprecated/`) e um `.out-of-scope/` que registra **decisões de não fazer**.

**As 4 falhas que ele ataca** — é o esqueleto do README:

1. *O agente não fez o que eu queria* → **grilling** (entrevista implacável antes de codar).
2. *O agente é verboso demais* → **linguagem ubíqua** (`CONTEXT.md`), que também dá nomes
   consistentes a variáveis e arquivos e reduz tokens de raciocínio.
3. *O código não funciona* → **feedback loops** (`tdd`, `diagnose`).
4. *Viramos uma bola de lama* → **design de código** (`improve-codebase-architecture`, deep modules).

**A peça mais valiosa:** `writing-great-skills` + seu `GLOSSARY.md` — uma teoria completa de autoria,
com vocabulário fechado: *predictability, context load × cognitive load, information hierarchy,
progressive disclosure, completion criterion, legwork, leading word* e os modos de falha
*premature completion, duplication, sediment, sprawl, no-op*.

**Invariante de repositório** (o `CLAUDE.md` dele, 12 linhas): toda skill em `engineering/`,
`productivity/` ou `misc/` **precisa** de entrada no README raiz, no README do bucket e no
`.claude-plugin/plugin.json`; skills em `personal/`, `in-progress/`, `deprecated/` **não podem**
aparecer em nenhum dos três. Regra checável, não conselho.

---

## 2. Comparativo eixo a eixo

| Eixo | `mattpocock/skills` | OSForge (estado em 2026-07-30, pós-auditoria) | Veredito |
|---|---|---|---|
| **Filosofia** | `writing-great-skills` + `GLOSSARY.md` | `docs/SKILL-STANDARD.md` já importa a teoria dele e acrescenta *Iron Law* + o tripé `Use when / Keywords / Do NOT use for` | **Empate na teoria**, OSForge perde na aplicação (§3) |
| **Invocação** | Decisão consciente, `disable-model-invocation` | Prevista no padrão, usada em **1 de 174** skills | **Matt** |
| **Curadoria** | 14 skills; buckets `in-progress/` e `deprecated/`; `.out-of-scope/` | 174 skills + 76 notas flat; **nenhum** bucket de aposentadoria; `design-taste-frontend-v1` legado; 16 skills na órbita "design" | **Matt, com folga** |
| **Tamanho** | `SKILL.md` enxuto + disclosure | 42.291 linhas em `SKILL.md`; média **311**; 42 acima de 300; maior 1.501. Usa disclosure (363 arquivos de referência) mas ainda há *sprawl* | **Matt** |
| **Descoberta** | Sem índice always-on; description faz o trabalho; router (`ask-matt`) | Dois canais: 44 skills nativas + **manifesto gerado** com 130 skills e 76 notas, com protocolo de resolução e gate no deploy | **OSForge** (era Matt antes de hoje) |
| **Domínio por projeto** | Pilar: `CONTEXT.md` + `docs/adr/`, lidos por `tdd`, `diagnose`, `improve-codebase-architecture`, `to-issues` | **Não existe equivalente** — há `.specs/` e `osforge-db add-decision`, mas nenhum glossário que as skills leiam | **Matt — maior lacuna** |
| **Bootstrap por repo** | `/setup-matt-pocock-skills` escreve bloco `## Agent skills` + `docs/agents/*.md` | Convenções globais assumidas; sem passo por projeto | **Matt** |
| **Spec→ticket** | `to-prd` → `to-issues` (tracer bullets, `blocked by`, **HITL/AFK**) → `triage` → `implement` → `code-review`; integra GitHub/GitLab/`.scratch/` | 9 comandos `spec-*` + `osforge-db` com `wave`/`depends_on` e dispatch paralelo | **OSForge** em paralelismo e estado; falta fatia vertical explícita, eixo HITL/AFK e issue tracker real |
| **Debugging** | `diagnose`: **feedback loop primeiro** (10 táticas), 3–5 hipóteses **falsificáveis**, tag `[DEBUG-a4f2]`, post-mortem → handoff pra arquitetura | `systematic-debugging`: 4 fases, sem loop-primeiro, sem hipóteses falsificáveis, sem limpeza por tag | **Matt** |
| **TDD** | Anti-pattern "horizontal slices"; usa glossário nos nomes de teste | **Iron Law** + proteção de testes (que ele não tem). Mas a description repete a mesma branch 6× e não tem `Do NOT use for` | **Empate** |
| **Grilling** | Skill dedicada + `grill-with-docs` + `grill-me` | 3 linhas de regra no `CLAUDE.md` + passo no Plan Mode | **Matt** |
| **Arquitetura** | `improve-codebase-architecture` + `codebase-design`: glossário-contrato, **deletion test**, relatório HTML, ADR na recusa | `clean-code`, `architecture`, `technical-design-doc-creator`. `codebase-design` está **previsto** no SKILL-STANDARD §6.4 e não existe | **Matt** |
| **Distribuição** | Plugin no marketplace + `npx skills`; changesets, CHANGELOG, CI | `deploy.sh` + allowlist core + `install-skill.sh` por projeto — cobre o caso de uso sem plugin; sem versionamento nem CI | **Empate** |
| **Validação** | Nenhuma | `test-skill-triggering.sh` + `.tsv` (~25 casos para 174 skills; cabeçalho ainda em pt-BR) | **OSForge**, subutilizado |

---

## 3. O achado principal: o padrão existe, a aplicação não

`docs/SKILL-STANDARD.md` já importa a teoria do Matt e a melhora. Ele mesmo se declara:
*"specification + examples. Nothing applied to the repo yet."* O plano de adoção em 5 commits (§7)
parou no commit 2. Medindo o acervo contra o próprio padrão:

| Regra do `SKILL-STANDARD.md` | Cobertura real |
|---|---|
| `Use when:` na description | 133 / 174 |
| `Do NOT use for:` (desambiguação) | **71 / 174** |
| `Done when:` em cada passo | **4 / 174** |
| Eixo de invocação decidido | **1 / 174** |
| Legado pt-BR (`ACIONE`) removido | 2 skills restantes |

Sem `Done when:` o modo de falha que o Matt chama de **premature completion** fica sem defesa —
justamente o mais caro em execução autônoma por ondas, que é o diferencial do OSForge.

---

## 4. O que o OSForge tem de melhor e deve manter

- **Iron Law** — regra inviolável em maiúsculas no topo. Um *leading word* estrutural que o repo dele não tem.
- **Tripé de ativação** `Use when / Keywords / Do NOT use for` — mais rigoroso que a description dele,
  porque o "Do NOT use for" resolve colisão entre irmãs, e aqui há 174 irmãs.
- **Harness de triggering** — ele não tem nada disso; é o que torna padronização em lote segura.
- **Frontmatter de execução** (`model`, `context: fork`, `agent`, `allowed-tools`).
- **Dispatch por ondas** com `wave`/`depends_on` — mais avançado que os `blocked by` textuais dele.
- **Model A + manifesto** (feito hoje) — cobertura total com ponteiro barato, algo que o modelo
  "poucas skills" dele nunca precisou resolver.

---

## 5. Onde o OSForge perde

1. **Sem glossário ubíquo por projeto** — maior retorno por token investido.
2. **Sem ciclo de vida de skill** — nada nasce "in-progress" nem morre "deprecated" (*sediment*).
3. **Skills grandes demais** — média 311 linhas.
4. **Dívida de fusão** — 30 pares nome-colidente entre nota flat e skill, com 6–89% de sobreposição.

---

## 6. Recomendações

### Já implementado (2026-07-30)

- ~~**R2** Cortar context load~~ → Model A commitado: 44 skills nativas (era 174 deployadas),
  1 MCP global (era 8), stacks por projeto via `install-mcp.sh`.
- ~~**R4** Índice gerado e travado~~ → `_generate_manifest.py` + gate no `deploy.sh`.
- ~~**R10** Empacotar como plugin~~ → **rejeitada**: `install-skill.sh` + allowlist já entregam
  instalação por subconjunto; plugin só faria sentido para distribuir a terceiros.

### P0 — fechar o gap entre padrão e acervo

**R1. Retomar o plano de adoção do `SKILL-STANDARD.md` §7 a partir do commit 3**, em lotes por
categoria, cada lote validado pelo harness.
*Aceite:* `Do NOT use for:` em 100% das skills com irmã próxima; `Done when:` em 100% das que têm
`## Process`; zero ocorrências de `ACIONE`.

**R2′. Podar as 44 descriptions que continuam core** (~4.4k tokens). Regra do padrão: um gatilho por
branch, sem sinônimos.
*Bloqueado por:* o harness precisa rodar antes e depois — editar 44 descriptions sem validação é o
mega-diff que o §5.A proíbe.

**R3. Ciclo de vida: `skills/_in-progress/` e `skills/_deprecated/`, excluídos do deploy.**
Mover `design-taste-frontend-v1`. Auditar a órbita "design".
*Aceite:* `--dry-run` não copia nada dos dois buckets; ADR registra a política.

**R14 (nova). Estender o harness para validar resolução, não só disparo nativo.**
Hoje ele checa invocação da Skill tool. Com Model A, 130 skills nunca serão invocadas assim — serão
alcançadas por `Read` via manifesto. Sem esse modo de asserção, **o Model A não tem critério de
aceite**: não há como provar que uma skill rebaixada continua alcançável.
*Aceite:* prompt ingênuo → skill certa alcançada, nativa **ou** por manifesto/semântica.

### P1 — trazer o que o Matt tem de melhor

**R5. `CONTEXT.md` — linguagem ubíqua por projeto.** *(maior ganho)*
Adaptar `CONTEXT-FORMAT.md` e `ADR-FORMAT.md`; criar `domain-modeling`; fazer `tdd-workflow`,
`systematic-debugging`, `code-review` e os `spec-*` lerem o glossário antes de nomear qualquer coisa.
Encaixa no `osforge-db` (glossário como `decision` versionada) e no `.specs/project/`.

**R6. Skill `grilling` + `grill-with-docs`.** Hoje são 3 linhas de regra global — e regra global é
*no-op* fácil de ignorar. Como skill, ganha gatilho, corpo e critério de conclusão.

**R7. Upgrade do `systematic-debugging` com o miolo do `diagnose`:** fase 1 = construir o feedback
loop (10 táticas ranqueadas), hipóteses falsificáveis antes de testar, tag `[DEBUG-xxxx]` para limpeza
por grep, post-mortem que dispara handoff para arquitetura.

**R8. Criar `codebase-design`** (especificado no §6.4, nunca implementado) **e a auditoria
arquitetural** com o deletion test e o glossário-contrato. O relatório HTML dele mapeia no Canvas.

**R9. Fatias verticais + eixo HITL/AFK no `spec-tasks`.** Cada task é um tracer bullet que atravessa
todas as camadas; cada task declara HITL ou AFK, e o dispatch por ondas só roda sozinho as AFK.

**R15 (nova). Resolver a dívida de fusão** dos 30 pares nome-colidente — decisão por par: fundir a
nota na skill ou renomear. Enquanto durar, o manifesto marca `⇄` e impõe precedência da skill.

### P2 — governança

**R11. Adotar `.out-of-scope/`** — um arquivo por decisão de não fazer. Custo quase zero.
**R12. Expandir o harness** de ~25 para as 50 skills mais usadas, com prompts pt-BR e inglês.
**R13. Router user-invoked (`/osforge`)** sobre os comandos e skills-orquestrador.
**R16 (nova). Instrumentar uso** (`observe-capture` + `evolve`) para promover/rebaixar o allowlist
com dado em vez de gosto — hoje o critério de admissão é bom, mas nunca foi medido.

---

## 7. Correções sobre a v1 desta análise

Registro do que a v1 errou, para não repetir:

| v1 dizia | Real |
|---|---|
| "147 skills" | **174** — a v1 contou diretórios de topo; 38 skills vivem aninhadas (`quality/`, `planning/`, `agency/`…) |
| "R2: criar cura de context load" | O "Model A" já estava escrito, só não commitado |
| "R10: empacotar como plugin (P2)" | Rejeitada — `install-skill.sh` cobre o caso |
| "30 duplicatas, seguro deletar" | **Não são duplicatas** — colisão de nome com 6–89% de sobreposição; deletar destruiria conteúdo |
| "manifesto vai cortar ~2k tokens" | Cortou o custo *por item* (77 → 28), mas o total subiu: cobertura foi de 51 para 206 itens indexados |
| "`Use when` em 101, `Do NOT use for` em 48" | **133** e **71** — contagem da v1 varreu só os diretórios de topo |

**Bugs encontrados durante a auditoria** (corrigidos):

- `_extract_index.py` truncava a description no primeiro apóstrofo — **59 de 174** afetadas.
  O `INDICE-SKILLS.json` alimenta `install-skill.sh` e `buscar-skill.py`, então o próprio caminho
  de resolução estava degradado.
- `deploy.sh` lia o MCP de um path fixo `~/Development/osforge` — qualquer clone em outro lugar
  mergeava o arquivo errado.
- `_extract_index.categorize_skill` classificava `accessibility` e `database-design` como Security
  (varredura de keyword com first-match-wins). Ponteiro mal categorizado é pior que ponteiro nenhum.

---

## 8. Orçamento de contexto — antes e depois

| | Antes de hoje | Agora |
|---|---|---|
| Skills nativas | 174 | **44** |
| MCPs globais | 8 | **1** |
| Descriptions sempre carregadas | ~7,6k tokens | **~4,4k** |
| `SKILLS.md` | ~3,9k (51 itens) | ~7,5k (**206 itens**) |
| **Baseline total** | ~17,6k | **~18,0k** |
| **Artefatos alcançáveis** | 115 | **220** |
| **Custo por artefato alcançável** | 153 tokens | **82 tokens** |

O baseline quase não mudou — a economia nas descriptions foi reinvestida em cobertura. A redução
absoluta depende de **R2′** (podar descriptions) e de **R3** (aposentar o que não se usa), ambas
bloqueadas pelo harness (**R14**). Essa é a ordem correta: medir antes de cortar.

---

## 8.1 Adendo — cobertura medida (2026-07-31)

Três rodadas reais da suíte gerada (`--generated --sample 30`), no ambiente do usuário:

| Rodada | Placar bruto | Após classificação |
|---|---|---|
| 1ª (interrompida por bug de `set -e` no harness) | 1 caso | expôs: 17 skills core aninhadas invisíveis em runtime (deploy achatado em resposta) |
| 2ª | 25 PASS · 4 FAIL · 1 TIMEOUT | 2 falhas reais; 3 artefatos do teste (workdir compartilhado, timeout-com-evidência, prompt pressupondo contexto) — todos corrigidos |
| 3ª (pós-correções + protocolo ampliado) | **30 PASS · 0 FAIL · 0 TIMEOUT** | auditada nos streams: 9 invocações nativas, 21 resoluções via manifesto, zero falso positivo |

As duas falhas reais da 2ª rodada tinham a mesma anatomia — o modelo respondeu competentemente de
conhecimento próprio sem consultar o manifesto — e motivaram o segundo gatilho do protocolo de
resolução ("prestes a produzir entregável multi-passo que se sente capaz de escrever sozinho →
varra o manifesto antes"). A 3ª rodada, com o protocolo deployado, não repetiu o padrão.

A métrica "skills com resolução provada por prompt ingênuo" saiu de **desconhecida** para
**100% na amostra corrente** (30/240 casos por rodada; rodadas sucessivas cobrem casos novos).

## 9. Uma frase

O OSForge tem **mais motor** (roteamento de modelo, agentes, ondas, estado, harness) e o repo do Matt
tem **mais disciplina** (curadoria implacável, ciclo de vida, linguagem ubíqua, critérios de conclusão).
O padrão que reconcilia os dois já está escrito em `docs/SKILL-STANDARD.md` — falta executá-lo e
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
