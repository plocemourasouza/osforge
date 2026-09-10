# Análise — OSForge × `tt-a1i/archify`

> **Fonte externa:** https://github.com/tt-a1i/archify (MIT, ~56k ★) · site https://tt-a1i.github.io/archify/ · leitura de 2026-09-10
> **Versão lida:** `2.17.0-dev.1` na `main`; última tag estável `v2.16.0`.
> **Idioma:** análise em pt-BR (convenção de `docs/DECISIONS.md`); conteúdo deployado em inglês por ADR-011.
> **Método:** repositório clonado e o pacote executado de ponta a ponta (`doctor` → autoria → `validate` → `deliver`) antes de escrever qualquer linha abaixo. Números são medidos, não estimados.

---

## 0. Escopo

O Archify **não é uma biblioteca de skills** — é **uma skill com um motor embutido**: um pacote Node (`archify/`) que compila JSON tipado em HTML interativo autocontido, com validador determinístico e recibo de entrega. Comparar com o OSForge nos eixos de agentes, hooks, banco de estado ou roteamento seria inútil.

**Comparado:** o que o pacote faz · a disciplina de autoria que a `SKILL.md` impõe · onde isso encaixa no pipeline `spec-*` e nas skills de arquitetura/planejamento · custo de contexto · mecanismo de distribuição · o que **não** trazer.

---

## 1. O que é o Archify

**Tese:** "descreva o sistema no chat; o agente entrega um mapa interativo, verificado, num único HTML". Cinco tipos de diagrama, cada um com schema JSON, renderer e validador próprios:

| Tipo | Serve para |
|---|---|
| `architecture` | componentes, serviços, fronteiras cloud/segurança, infraestrutura |
| `workflow` | processos, gates de aprovação, runbooks, CI/CD (swim-lanes) |
| `sequence` | cadeias de chamadas de API, ciclo de vida de request, traces assíncronos |
| `dataflow` | pipelines, ETL/ELT, linhagem, governança |
| `lifecycle` | máquinas de estado, retries, estados terminais |

**O motor** (`bin/archify.mjs`): `guide` (roteador de tipo por cenário) · `validate` (schema + composição, com diagnósticos legíveis por máquina: `subject`, `evidence`, `supportedFixes`) · `deliver` (renderiza, checa 9 verificações, grava atomicamente e devolve SHA-256 + bytes da spec e do artefato) · `preview` (loop local) · `compare` (delta before/after de arquitetura) · `visual-check` (evidência em browser real) · `brands` (107 marcas embutidas, digest-pinned; `next-js`, `supabase`, `prisma`, `postgresql`, `stripe`, `vercel`, `cloudflare`, `claude`, `anthropic`, `github`, `docker`, `redis`, `node-js` — a stack padrão do OSForge está coberta) · `doctor` · `demo`.

**Números medidos (sandbox Linux, Node 22):**
- Pacote: 8,1 MB no clone; **~2,2 MB sem `test/` (1,7 MB) e `examples/` (4,0 MB)**. Zero dependências de runtime (`devDependencies` só para regenerar validadores/marcas). `doctor`: 15/15 ok sem `npm install`.
- `SKILL.md`: 16,4 KB (~4k tokens) — **carregada só quando dispara**; a `description` (o custo permanente) tem ~120 tokens.
- Artefato HTML: ~810 KB (o viewer completo vai embutido — pan/zoom, busca, foco, rastreio de alcance, rotas, temas, export PNG/SVG/WebM).
- Ciclo real, diagrama de 8 componentes da stack OSForge: **3 rodadas** de `validate` (marca inexistente → 2 arestas cruzando nós + 3 labels colidindo → 1 label) até `deliver` com `checksPassed: 9/9, errors: 0, warnings: 0`. Cada diagnóstico veio com coordenadas e correção sugerida ("labelAt [392, 182] or labelDy +7").

---

## 2. O que o Archify traz que o OSForge não tem

| Eixo | OSForge hoje | Archify | Veredito |
|---|---|---|---|
| **Diagrama em `design.md` / ADR / TDD** | "Text or Mermaid diagram" (`spec-design`), "Context Diagram: textual description" (`arch-builder`), Mermaid/PlantUML (`technical-design-doc-creator`) | JSON tipado → HTML verificado, com receipt | **Archify.** Mermaid não é validado nem verificado; o Archify é um **gate determinístico** — exatamente a filosofia dos hooks de custo zero |
| **Visualização de planos** | `visual-planner` (HTML narrativo de spec/PRD, desenha diagramas "à mão" em CSS) | 5 tipos com layout semântico e validação de composição | **Complementares:** `visual-planner` conta a história do plano; o Archify é o mapa técnico verificado dentro dela |
| **Revisão interativa** | `osforge-canvas` (artefato JSON + feedback estruturado) | HTML standalone, sem round-trip de feedback | **Complementares:** o Canvas é o canal de aprovação; o Archify é o artefato durável em `.specs/` |
| **Verdade antes de espetáculo** | `verification-before-completion`, "evidência antes de afirmar" | `deliver` separa três alegações: checks determinísticos · evidência de browser · revisão perceptual humana; "non-zero exit can never be described as success" | **Empate de filosofia** — o Archify já fala a língua do OSForge |
| **Roteamento de tipo** | não existe (o agente escolhe Mermaid `flowchart` para tudo) | `guide "<cenário>" --json` com `useWhen`/`avoidWhen` | **Archify** |
| **Delta de arquitetura** | nada | `compare base.json head.json` → Before/Delta/After | **Archify** (útil em `/spec-measure` e em revisões de PR) |
| **Evidência de código** | nada | nós podem apontar `evidence` para paths/commits reais, verificáveis por git | **Archify** — encaixa no `spec-implement` (diagrama que aponta o código que o cumpre) |

**O achado principal:** o valor **não é o desenho** — é o **loop `validate → repair → deliver`** com diagnóstico estruturado. É a mesma tese do GateGuard e do `route-guard`: prosa bate no teto, determinismo assume. Um diagrama Mermaid num `design.md` é uma opinião; um `deliver` com 9/9 checks e SHA-256 é um fato.

---

## 3. Onde encaixa no OSForge (definição de estrutura, projeto ou "algo")

O uso pedido — "quando estivermos criando uma nova estrutura, projeto ou definição de algo" — passa por quatro pontos do pipeline, e cada um já tem um lugar para um diagrama que hoje é texto:

| Momento | Skill/comando | Tipo Archify | Artefato |
|---|---|---|---|
| Fase 2 do spec | `/spec-design` | `architecture` (componentes) + `dataflow` ou `sequence` (fluxo da feature) | `.specs/features/<f>/diagrams/*.html` linkados em `design.md` |
| Decisão arquitetural | `architecture`, `planning/arch-builder` | `architecture` (ADR: contexto antes/depois via `compare`) | `.specs/architecture/*.html` ou junto do ADR |
| TDD (design doc) | `technical-design-doc-creator` | `architecture` + `sequence` | seção "Technical Solution" aponta para o HTML |
| Apresentação de plano | `visual-planner`, `osforge-canvas` | embute/linka o HTML já entregue | não desenha de novo |
| Runbook / CI | `deployment-procedures`, `operations` | `workflow`, `lifecycle` | junto do runbook |

**Regra de encaixe:** o diagrama é **derivado** do artefato de texto (spec, ADR, TDD), nunca a fonte. A fonte de verdade continua sendo o Markdown + o JSON da spec do diagrama (versionável, diffável); o HTML é o artefato entregue.

---

## 4. Decisão: como trazer

### 4.1 Distribuição — instalar no `deploy.sh`, pinado, fora do repo

- `./deploy.sh` ganha `--with-archify` (padrão **ligado**) / `--no-archify`. Baixa o **tarball da tag pinada** (`ARCHIFY_VERSION` no topo do `deploy.sh`) e extrai só `archify/` (o pacote da skill) para `~/.claude/skills/archify/` e `~/.cursor/skills/archify/`, sem `test/` nem `examples/` pesados além dos 5 exemplos canônicos que a `SKILL.md` manda ler. Idempotente: se a versão instalada (`skill-release.json`) já é a pinada, não faz nada. Termina com `node bin/archify.mjs doctor`.
- **Por que não vendorizar:** 2–8 MB de código de terceiro no repo, upgrade manual, e o Archify tem checker de atualização próprio (`scripts/check-update.mjs`, opt-in, nunca instala sozinho) que perderia sentido. A regra de `sources/` ("raw, disk-only, never deployed") é para **padrões que curamos**; o Archify é uma **ferramenta que executamos** — o precedente é o `llmfit` (`requires_binary`), não o `taste-skill`.
- **Por que não `npx skills add`:** adiciona dependência num CLI de terceiro no deploy, sem pin de versão, e ignora o `~/.cursor`. O tarball do GitHub é um `curl` + `tar`.

### 4.2 Conhecimento nativo — skill de disciplina no core + pipeline

O critério de admissão do `skills-core.txt` exclui geradores. O que entra no core **não é o gerador**: é uma skill de **disciplina** curta, `system-diagrams`, que (a) sabe **quando** um diagrama é devido dentro do fluxo OSForge, (b) roteia o tipo, (c) fixa **onde** o artefato vive e **como** é aceito (receipt), e (d) delega a autoria à `SKILL.md` do Archify — que só entra em contexto ao disparar. Custo permanente: uma `description` (~90 tokens). Clears o critério 1 (dispara sem o usuário pedir: "defina a estrutura do projeto" não contém a palavra "diagrama") e o 3 (bootstrap: é ela que aponta para o Archify).

Os pontos do pipeline (§3) recebem **um passo cada**, não uma cópia da skill.

### 4.3 O que NÃO incorporar (registrado aqui, não em `.out-of-scope/`, por ser decisão de terceiro)

- **Update-awareness** do Archify (notificação de versão nova a cada primeiro candidato): fica como está no upstream — é opt-in, nunca instala, e o deploy pinado é quem manda. Não replicar no OSForge.
- **`preview` por padrão:** o próprio upstream diz "never start preview by default". O canal de revisão do OSForge é o Canvas.
- **Motion / share cards / stories:** capacidades do viewer, já embutidas no HTML; não viram skill nem regra.
- **Integração DeepSeek Harness, gallery, benchmarks, experiments:** fora do pacote da skill; não deployar.
- **Substituir Mermaid inline em tudo:** um `sequence` de 3 participantes numa resposta de chat continua sendo Mermaid. O Archify entra quando o diagrama **vira artefato** (`.specs/`, ADR, TDD, runbook).

---

## 5. Orçamento de contexto

| Item | Custo | Quando |
|---|---|---|
| `system-diagrams` (core) — `description` | ~90 tokens | toda sessão |
| `archify` (global via deploy) — `description` | ~120 tokens | toda sessão (é uma skill em `~/.claude/skills`) |
| `system-diagrams` — corpo | ~600 tokens | ao disparar |
| `archify/SKILL.md` — corpo | ~4k tokens | ao disparar |
| schema + 1 exemplo do tipo (leitura obrigatória da SKILL.md) | ~3–6k tokens | por diagrama |

Total permanente: **~210 tokens/sessão**, dentro da margem que o `skills-core.txt` considera aceitável (o corte de 2026-07 removeu ~3,2k). Se `osforge-db evolve` mostrar zero disparos em 30 dias, o passo de reversão é uma linha em `skills-core.txt` e `--no-archify` no deploy.

---

## 6. Riscos e mitigação

- **Upstream em movimento rápido** (v2.9 → v2.16 em semanas; `main` já em 2.17-dev). Pin por tag no `deploy.sh`; upgrade é editar `ARCHIFY_VERSION`, rodar deploy e `doctor`. O checker do próprio Archify avisa quando há release nova.
- **Schema muda entre versões** (workflow v1 → v2 já aconteceu). Os JSONs em `.specs/` ficam versionados com `schema_version`; o Archify mantém migrações (`archify/migrations/`).
- **Artefatos de 800 KB em `.specs/`.** Aceitável (HTML autocontido é o produto); se pesar no repo do projeto, `.specs/**/diagrams/*.html` vai para `.gitignore` e só o `.json` (2–5 KB) é versionado — o HTML é reproduzível por `deliver`.
- **Sem Node ≥ 18 na máquina:** `deploy.sh` avisa e pula; a skill `system-diagrams` tem fallback explícito (Mermaid no Markdown, marcado como não verificado).

---

## 7. Uma frase

O OSForge já exige **fatos antes de ação** (GateGuard) e **evidência antes de "pronto"** (`verification-before-completion`); o Archify traz o mesmo princípio para o diagrama — **um mapa técnico só existe quando `deliver` devolve 9/9 e um hash** — e por isso entra como disciplina nativa do pipeline, não como mais um gerador.

---

### Referências

- [tt-a1i/archify — README](https://github.com/tt-a1i/archify) · [site](https://tt-a1i.github.io/archify/)
- [`archify/SKILL.md`](https://github.com/tt-a1i/archify/blob/main/archify/SKILL.md) · [`PRODUCT.md`](https://github.com/tt-a1i/archify/blob/main/PRODUCT.md) · [`DESIGN.md`](https://github.com/tt-a1i/archify/blob/main/DESIGN.md)
- Baseado em `Cocoon-AI/architecture-diagram-generator` (MIT) — atribuição transitiva mantida via `metadata.based_on` no upstream
- Licença MIT — atribuição via `metadata.inspired_by` / `source`, conforme §5.C do `SKILL-STANDARD.md`
- Decisão formal: ADR-014 em `docs/DECISIONS.md`
