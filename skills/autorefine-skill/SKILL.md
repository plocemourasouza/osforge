---
name: autorefine-skill
description: "Refinamento autônomo iterativo com loop autoresearch + meta-otimização + transferência cross-domínio. ACIONE quando: usuário pede 'melhorar uma skill', 'otimizar a skill X', 'a skill Y não está funcionando bem', 'iterar sobre skill', 'autorefine', 'refinar código', 'otimizar performance', 'melhorar métrica X', 'meta-otimizar', 'transferir aprendizado', 'aplicar padrão de outro projeto'. Generalizado para qualquer artefato com métrica mensurável — skills, código, prompts, configs, docs. Keywords: melhorar skill, refinar skill, otimizar, autorefine, iteração autônoma, autoresearch, loop de melhoria, self-improving, guard, verify, meta-otimização, transferência, cross-domain."
model: sonnet
allowed-tools: Read, Write, Bash, Glob, Grep
metadata:
  author: osforge
  version: '3.0'
  inspired_by: 'karpathy/autoresearch, uditgoenka/autoresearch, alfonsograziano/auto-agent, facebookresearch/HyperAgents'
  changelog: 'v3.0 — meta-otimização de skills (self-improvement loop) + transferência multi-domínio via osforge-db. v2.0 — verify+guard separation, osforge-db memory, domain generalization, eval packages'
---

## Estado do projeto
!`osforge-db list-projects --status=active 2>/dev/null | head -3 || echo "nenhum projeto ativo"`
!`osforge-db search "autorefine" 2>/dev/null | head -5 || echo "sem histórico de autorefine"`
!`osforge-db search "meta-review" 2>/dev/null | head -3 || echo "sem meta-reviews anteriores"`
!`osforge-db search "transfer-candidate" 2>/dev/null | head -3 || echo "sem candidatos a transferência"`

# AutoRefine v3

## Princípio

Aplicar o loop de pesquisa autônoma do Karpathy a **qualquer artefato com métrica mensurável**: skills, código, prompts, configs, documentação. O agente formula uma hipótese → aplica uma mudança atômica → verifica com métrica mecânica → protege com guard contra regressões → mantém ou reverte → registra no banco → repete.

**constraint + mechanical metric + autonomous iteration = compounding gains**

v3 adiciona duas camadas inspiradas no HyperAgents (Meta Research):
- **Meta-otimização**: o loop analisa seus próprios padrões de sucesso/falha e ajusta o SKILL.md do autorefine
- **Transferência cross-domínio**: hipóteses validadas num projeto propagam para projetos similares via osforge-db
---

## Dois modos de operação

### Modo Skill (refinar SKILL.md do OSForge)
O modo original: iterar sobre o conteúdo de uma skill para melhorar seus outputs.
Artefato: `skills/<nome>/SKILL.md`. Métrica: aprovação em prompts de teste.

### Modo Genérico (qualquer artefato com métrica)
Modo expandido inspirado no autoresearch generalizado: iterar sobre qualquer arquivo/conjunto de arquivos onde existe uma métrica mecânica.

Exemplos:
- **Código**: `npm test -- --coverage` → melhorar cobertura de testes
- **Performance**: `lighthouse --output=json` → melhorar Core Web Vitals
- **Bundle**: `bun build && du -sh dist/` → reduzir tamanho
- **Prompt**: `python eval.py` → melhorar accuracy em dataset
- **Config**: `bun run bench` → melhorar throughput

---

## Setup inicial

Antes de iniciar o loop, colete do usuário:

### 1. Escopo

| Pergunta | Exemplo |
|---|---|
| Qual artefato refinar? | `skills/frontend-design/SKILL.md` ou `src/lib/auth.ts` |
| Qual o problema/objetivo? | "a skill gera código sem TypeScript" ou "latência p95 acima de 200ms" |
| Quais arquivos podem ser modificados? | Lista explícita (scope constraint) |
| Quais arquivos são read-only? | Guard files — nunca modificados |
### 2. Verify + Guard (separação obrigatória)

```
Verify: <comando que mede a métrica principal>
Guard:  <comando que garante que nada mais quebrou>
```

**Verify** = "A métrica melhorou?" — é o objetivo da otimização.
**Guard** = "Alguma outra coisa quebrou?" — é a rede de segurança.

| Cenário | Verify | Guard | Decisão |
|---|---|---|---|
| ✅ melhora | ✅ passa | ✅ passa | **KEEP** |
| ✅ melhora | ✅ passa | ❌ falha | **REWORK** (max 2 tentativas, depois DISCARD) |
| ❌ piora | ❌ falha | ✅ passa | **DISCARD** |
| ❌ piora | ❌ falha | ❌ falha | **DISCARD + rollback imediato** |

Exemplos de pares verify/guard:

| Domínio | Verify | Guard |
|---|---|---|
| Skill OSForge | `python eval_skill.py --prompts=3` | `grep -c "allowed-tools" SKILL.md` (frontmatter intacto) |
| Cobertura de testes | `bun test --coverage \| grep Stmts` | `bun tsc --noEmit` (tipos não quebraram) |
| Performance API | `bun run bench:api \| grep p95` | `bun test` (funcionalidade intacta) |
| Bundle size | `bun build && du -sh dist/` | `bun test && bun tsc --noEmit` |
| Prompt engineering | `python eval.py --metric=accuracy` | `python eval.py --metric=safety` (safety ≥ baseline) |

Se o guard não for definido pelo usuário, o default é: `exit 0` (sem guard). Mas **sempre sugerir** um guard relevante.
### 3. Budget e prompts de teste

| Configuração | Default |
|---|---|
| Iterações | 5 (max 10) |
| Prompts de teste (modo skill) | 2-3 exemplos reais |
| Direção da métrica | higher-is-better ou lower-is-better |

### 4. Snapshot obrigatório

```bash
cp -r <artefato-dir> <artefato-dir>-snapshot-$(date +%Y%m%d%H%M)
```

### 5. Carregar memória de hipóteses

```bash
# Buscar iterações anteriores de autorefine neste artefato
osforge-db search "autorefine <nome-do-artefato>" 2>/dev/null

# v3: Buscar também candidatos de transferência de outros projetos
osforge-db search "transfer-candidate <domínio>" 2>/dev/null
```

Se existem hipóteses anteriores que falharam, **nunca repeti-las**. Listar as hipóteses falhas conhecidas antes de formular novas.

Se existem **candidatos de transferência** de outros projetos no mesmo domínio, listá-los como hipóteses prioritárias (já validadas em contexto similar).

---

## O Loop (modify → verify → guard → keep/discard → log → repeat)
### Regras de ferro

| # | Regra | Implementação |
|---|---|---|
| 1 | Loop até acabar o budget | Bounded: N iterações, depois para |
| 2 | Ler antes de escrever | Entender contexto completo antes de modificar |
| 3 | Uma mudança por iteração | Atômico e rastreável — se quebra, sabe o porquê |
| 4 | Verificação mecânica apenas | Números, não julgamento subjetivo |
| 5 | Rollback automático | Falha → revert via git ou snapshot |
| 6 | Simplicidade vence | Resultado igual + menos código = KEEP |
| 7 | Git é memória | Commits prefixados `experiment:` preservam histórico |
| 8 | Quando travado, pensar mais | Re-ler, combinar near-misses, tentar abordagem radical |

### Estrutura de cada iteração

```
Iteração N:
  1. [haiku]  Lê o artefato atual + git log + memória (hipóteses que já falharam)
  1b.[haiku]  Consulta transfer-candidates do mesmo domínio (v3)
  2. [haiku]  Formula hipótese: "se eu modificar X, a métrica Y vai melhorar porque Z"
  3. [haiku]  Aplica UMA modificação atômica
  4. [haiku]  git commit -m "experiment: <hipótese resumida>"
  5. [haiku]  Executa Verify → coleta métrica
  6. [haiku]  Executa Guard → verifica que nada quebrou
  7. [sonnet] Decide: KEEP / REWORK / DISCARD (ver tabela acima)
  8. [sonnet] Se DISCARD → git revert HEAD
     [sonnet] Se REWORK → tenta ajustar (max 2x), depois DISCARD
  9. Registra no log + osforge-db
  9b.Se KEEP → avalia elegibilidade para transferência (v3)
```
### Modelo por etapa (smart-model-dispatch)

| Etapa | Modelo | Razão |
|---|---|---|
| Leitura + hipótese + modificação | Haiku | Mecânico, baixo custo |
| Execução verify + guard | Haiku | Rodar comandos |
| Avaliação + decisão | Sonnet | Requer julgamento |
| Síntese final (relatório) | Sonnet | Análise de padrões |
| Meta-review (v3) | Sonnet | Análise agregada cross-sessão |
| Decisão de transferência (v3) | Sonnet | Avaliar generalização |

Usar Opus apenas se o critério for ambíguo e exigir raciocínio sobre tradeoffs arquiteturais.

---

## Log de iterações (TSV + markdown)

### TSV (machine-readable)

Manter `autorefine-results.tsv` no diretório do artefato:

```tsv
iteration	commit	metric	delta	guard	status	hypothesis	transfer_eligible
0	a1b2c3d	85.2	0.0	pass	baseline	initial state	-
1	b2c3d4e	87.1	+1.9	pass	keep	add explicit TypeScript types to output rules	yes
2	-	86.5	-0.6	pass	discard	refactor section ordering (no improvement)	-
3	c4d5e6f	89.3	+2.2	pass	keep	add code block examples for each pattern	yes
4	d5e6f7g	91.0	+1.7	fail	rework	aggressive minification broke guard tests	-
4b	e6f7g8h	90.8	+1.5	pass	keep	conservative minification (guard-safe)	no
```
### Markdown (human-readable)

Manter `autorefine-log.md` durante o processo:

```markdown
# AutoRefine Log — <nome-do-artefato>
Data: <data>
Budget: <N> iterações
Verify: <comando>
Guard: <comando>
Direção: higher-is-better | lower-is-better

## Iteração 1
- Hipótese: ...
- Modificação: ...
- Métrica: X → Y (delta: +Z)
- Guard: pass | fail
- Resultado: KEEP | DISCARD | REWORK
- Razão: ...
- Transfer eligible: yes | no | - (razão)

## Resultado final
- Melhor versão: iteração N
- Métrica inicial: X
- Métrica final: Y (delta: +Z, melhoria de W%)
- Hipóteses que funcionaram: ...
- Hipóteses que falharam: ...
- Candidatas a transferência: N hipóteses marcadas
```

---
## Memória cross-sessão (osforge-db)

Ao final de cada sessão de autorefine, persista os aprendizados:

```bash
# Registrar cada hipótese KEEP como decisão
osforge-db add-decision <project-slug> \
  "autorefine(<artefato>): KEEP — <hipótese resumida> (metric +<delta>)" \
  --category=arch

# Registrar cada hipótese DISCARD como decisão
osforge-db add-decision <project-slug> \
  "autorefine(<artefato>): DISCARD — <hipótese resumida> (reason: <razão>)" \
  --category=arch

# Registrar resultado final
osforge-db add-decision <project-slug> \
  "autorefine(<artefato>): resultado — metric <inicial> → <final> (+<delta>%) em <N> iterações" \
  --category=arch

# v3: Registrar candidatos a transferência
osforge-db add-decision <project-slug> \
  "transfer-candidate(<domínio>): <hipótese resumida> — validada em <artefato> (metric +<delta>)" \
  --category=transfer

# v3: Registrar meta-review
osforge-db add-decision <project-slug> \
  "meta-review: <N> sessões analisadas — padrões: <lista de padrões encontrados>" \
  --category=meta
```

Na próxima sessão, o loop consulta `osforge-db search "autorefine <artefato>"` e evita repetir hipóteses que já falharam. Isso cria **aprendizado institucional** — o agente não comete os mesmos erros entre sessões.
---

## Crash recovery

| Falha | Resposta |
|---|---|
| Syntax error no artefato | Fix imediato, não contar iteração |
| Runtime error no verify/guard | Tentar fix (max 3x), depois skip |
| Timeout no comando | Revert, tentar variante menor |
| Guard quebra após verify passar | REWORK (max 2x), depois DISCARD |
| Processo interrompido | Snapshot preserva estado; `osforge-db resume` retoma |

---

## Condições de parada

Encerre o loop antes de esgotar o budget se:

1. **Convergência** — 3 iterações consecutivas KEEP sem melhoria adicional mensurável
2. **Saturação** — 100% dos critérios aprovados por 2 iterações consecutivas
3. **Regressão persistente** — 3 iterações consecutivas DISCARD (hipótese de melhoria está errada; pare e discuta com o usuário)
4. **Budget esgotado** — N iterações concluídas

Progresso impresso a cada 5 iterações (se budget > 5).
---

## 🧠 Meta-otimização (v3 — Ideia A: Self-Improvement Loop)

> Inspirado no HyperAgents (Meta Research): o sistema que melhora artefatos
> também deve melhorar a si mesmo. Metacognição pragmática sem Docker/GPU.

### Conceito

Após **N sessões acumuladas** no osforge-db (threshold: 10 sessões ou 50+ hipóteses registradas), o AutoRefine analisa seus próprios padrões de sucesso/falha e gera ajustes concretos para este SKILL.md. Isso é auto-melhoria de segunda ordem — não otimiza o artefato, otimiza **como** otimiza artefatos.

### Quando disparar

O meta-review é acionado automaticamente quando:

```bash
# Contar sessões acumuladas
SESSIONS=$(osforge-db search "autorefine" 2>/dev/null | grep -c "resultado")
HYPOTHESES=$(osforge-db search "autorefine" 2>/dev/null | grep -c "KEEP\|DISCARD")

# Threshold: 10+ sessões OU 50+ hipóteses
if [ "$SESSIONS" -ge 10 ] || [ "$HYPOTHESES" -ge 50 ]; then
  echo "META-REVIEW elegível"
fi
```

Também pode ser acionado manualmente: `"meta-otimizar autorefine"`, `"revisar padrões do autorefine"`, `"autorefine self-improve"`.
### Processo de meta-review (5 fases)

#### Fase 1: Coleta de dados agregados

```bash
# Extrair todos os registros de autorefine
osforge-db search "autorefine" --json 2>/dev/null > /tmp/autorefine-history.json

# Estrutura esperada por sessão:
# - artefato, domínio, modo (skill/genérico)
# - hipóteses KEEP: descrição, delta, domínio
# - hipóteses DISCARD: descrição, razão, domínio
# - resultado: métrica inicial → final, % melhoria
```

#### Fase 2: Análise de padrões [sonnet]

O agente analisa o corpus e responde:

| Pergunta | Exemplo de insight |
|---|---|
| Quais **tipos de hipótese** têm maior taxa KEEP? | "Hipóteses de tipagem forte: 78% KEEP vs 34% média" |
| Quais **tipos de hipótese** sempre falham? | "Reordenação de seções: 0/12 KEEP — nunca melhora métrica" |
| Qual **domínio** responde melhor ao autorefine? | "Skills: +18% médio vs Código: +7% médio" |
| Existe correlação entre **tamanho da mudança** e sucesso? | "Mudanças <20 linhas: 62% KEEP; >50 linhas: 11% KEEP" |
| Quais **combinações verify+guard** funcionam melhor? | "tsc+test: 89% guard-pass vs test-only: 64%" |
| Quantas iterações por sessão é ótimo? | "Ganho marginal cai após iteração 4 em 80% dos casos" |
| REWORK vale a pena? | "REWORK→KEEP: 38% das vezes — vale manter" |
#### Fase 3: Gerar propostas de ajuste

Com base nos padrões, o agente gera **propostas concretas** de modificação deste SKILL.md:

```markdown
## Meta-Review Proposta #1
Padrão: "Hipóteses de reordenação nunca funcionam (0/12)"
Ajuste: Adicionar às Regras de Ferro: "Regra 9: Não formular hipóteses de reordenação pura de seções"
Impacto estimado: Economiza ~2 iterações/sessão (evita dead ends)
Confiança: alta (12 amostras, 0% sucesso)

## Meta-Review Proposta #2
Padrão: "Ganho marginal cai após iteração 4"
Ajuste: Reduzir budget default de 5 para 4 iterações
Impacto estimado: Reduz custo em 20% sem perda significativa de ganho
Confiança: média (80% dos casos, mas 20% ainda ganham na 5ª)

## Meta-Review Proposta #3
Padrão: "Mudanças >50 linhas quase sempre falham"
Ajuste: Adicionar ao setup: "WARN se a diff da iteração exceder 50 linhas"
Impacto estimado: Sinaliza hipóteses over-scoped antes do verify
Confiança: alta (89% de correlação)
```

#### Fase 4: Aplicar ajustes (com aprovação)

**NUNCA aplicar meta-ajustes automaticamente.** Sempre apresentar as propostas ao usuário e pedir aprovação explícita antes de modificar o SKILL.md. Cada proposta aprovada gera:

```bash
# Backup antes de meta-ajuste
cp skills/autorefine-skill/SKILL.md skills/autorefine-skill/SKILL.md.pre-meta-$(date +%Y%m%d)

# Aplicar modificação aprovada
# ... (edição do SKILL.md)

# Commit com prefixo meta:
git commit -m "meta(autorefine): <descrição do ajuste> — baseado em <N> sessões"
```
#### Fase 5: Registrar meta-review no osforge-db

```bash
osforge-db add-decision global \
  "meta-review(autorefine): analisadas <N> sessões, <M> hipóteses. Padrões: <lista>. Ajustes aplicados: <lista de propostas aprovadas>" \
  --category=meta
```

### Guardrails da meta-otimização

| Regra | Razão |
|---|---|
| Max 1 meta-review por semana | Evita over-fitting em dados insuficientes |
| Min 10 sessões entre meta-reviews | Garante amostra estatisticamente relevante |
| Propostas precisam de ≥5 amostras de suporte | Evita generalizar de casos isolados |
| Backup obrigatório antes de cada meta-ajuste | Reversível se o ajuste piorar performance |
| Meta-ajustes são sempre apresentados, nunca auto-aplicados | O humano decide o que muda no processo |
| Manter histórico de meta-reviews no osforge-db | Rastrear a evolução do próprio skill ao longo do tempo |

### Métricas da meta-otimização

Após 3+ meta-reviews, comparar:

```
Taxa KEEP antes do meta-ajuste vs depois
Iterações médias por sessão antes vs depois
% de budget utilizado antes vs depois
Tempo médio por sessão antes vs depois (se disponível)
```

Se um meta-ajuste **piora** as métricas agregadas, revertê-lo e registrar como "meta-discard" no osforge-db.
---

## 🔄 Transferência Cross-Domínio (v3 — Ideia B: Knowledge Propagation)

> Inspirado no multi-domain evaluation do HyperAgents: validar que melhorias
> transferem entre contextos similares. Uma otimização que funciona num projeto
> não deve morrer ali — deve propagar para projetos do mesmo domínio.

### Conceito

Quando uma hipótese é KEEP com delta significativo, o AutoRefine avalia se ela é **generalizável** — se o insight subjacente se aplica a outros projetos do mesmo domínio. Se sim, marca como `transfer-candidate` no osforge-db. Na próxima sessão de autorefine num projeto similar, essas hipóteses aparecem como **sugestões prioritárias** (já validadas em outro contexto).

### Taxonomia de domínios

| Domínio | Identificadores | Exemplos de artefatos |
|---|---|---|
| `nextjs-frontend` | Next.js, React, Tailwind, componentes | `src/components/`, `src/app/` |
| `api-backend` | API routes, tRPC, Prisma, endpoints | `src/server/`, `src/api/` |
| `database` | Prisma schema, migrations, queries | `prisma/schema.prisma` |
| `devops` | Docker, CI/CD, deploy, infra | `Dockerfile`, `.github/workflows/` |
| `skill-osforge` | SKILL.md do OSForge | `skills/*/SKILL.md` |
| `prompt-eng` | Prompts, system messages, templates | `prompts/`, `*.prompt.md` |
| `config` | Configs, env, settings | `*.config.*`, `.env*` |
| `docs` | Documentação, READMEs, specs | `docs/`, `*.md` |

O domínio é inferido automaticamente pelo path e conteúdo do artefato. Se ambíguo, perguntar ao usuário.
### Critérios de elegibilidade para transferência

Uma hipótese KEEP é elegível para transferência se **todas** as condições forem verdadeiras:

| Critério | Razão |
|---|---|
| Delta ≥ 1.5% (higher-is-better) ou ≥ 1.5% redução (lower-is-better) | Melhoria deve ser significativa, não ruído |
| Guard passou sem REWORK | Se precisou de REWORK, a hipótese tem edge cases |
| A hipótese é **sobre o padrão**, não sobre o artefato específico | "Adicionar tipos explícitos" transfere; "Renomear variável X para Y" não |
| O domínio do artefato está na taxonomia | Precisa de classificação para matching |

### Avaliação de generalização [sonnet]

Para cada hipótese KEEP elegível, o agente responde:

```
Hipótese: "adicionar code blocks com exemplos para cada padrão"
Artefato original: skills/frontend-design/SKILL.md
Domínio: skill-osforge

Perguntas de generalização:
1. Esta hipótese depende de algo específico deste artefato? → Não
2. Outros artefatos do domínio "skill-osforge" poderiam se beneficiar? → Sim
3. A hipótese pode ser formulada genericamente? → "Skills com exemplos de código concretos
   têm +15-25% de aprovação em prompts de teste"

Decisão: TRANSFER ✅
Formulação genérica: "Adicionar ≥1 code block por seção de padrão em skills que definem padrões"
Domínio alvo: skill-osforge
```
### Registro de transfer-candidates

```bash
# Registrar candidato a transferência
osforge-db add-decision <project-slug> \
  "transfer-candidate(<domínio>): <hipótese genérica> — validada em <artefato> (metric +<delta>%, guard pass)" \
  --category=transfer

# Exemplo real:
osforge-db add-decision meu-saas \
  "transfer-candidate(skill-osforge): adicionar ≥1 code block por seção de padrão — validada em skills/frontend-design/SKILL.md (metric +22%, guard pass)" \
  --category=transfer
```

### Consumo de transfer-candidates (no setup do loop)

No passo 5 do setup ("Carregar memória"), além de buscar hipóteses falhas, buscar candidatos:

```bash
# Identificar domínio do artefato atual
DOMAIN=$(# inferir de path + conteúdo)

# Buscar candidatos de transferência para este domínio
osforge-db search "transfer-candidate($DOMAIN)" 2>/dev/null
```

Se existem candidatos, apresentar ao usuário:

```
📦 Hipóteses transferidas de outros projetos (domínio: skill-osforge):

1. [+22%] "Adicionar ≥1 code block por seção de padrão"
   Origem: meu-saas / skills/frontend-design/SKILL.md
   
2. [+18%] "Incluir seção de anti-patterns com exemplos do que NÃO fazer"
   Origem: outro-projeto / skills/api-design/SKILL.md

Deseja usar alguma como hipótese prioritária? (y/N)
```

Hipóteses transferidas entram como **primeiras iterações** do loop (antes das hipóteses novas), pois já têm validação prévia.
### Validação de transferência

Uma hipótese transferida ainda precisa passar pelo loop normal (verify + guard). Possíveis resultados:

| Resultado no novo projeto | Ação |
|---|---|
| KEEP com delta similar (±30% do original) | **TRANSFER CONFIRMED** — registrar como validação cross-project |
| KEEP com delta menor | **PARTIAL TRANSFER** — funciona mas com menos impacto |
| DISCARD | **TRANSFER FAILED** — o padrão não generaliza para este contexto |

```bash
# Registrar resultado da transferência
osforge-db add-decision <novo-project-slug> \
  "transfer-result(<domínio>): <CONFIRMED|PARTIAL|FAILED> — '<hipótese>' de <projeto-origem> → delta <original> vs <atual>" \
  --category=transfer
```

### Maturidade de transfer-candidates

Conforme um candidato é testado em mais projetos, sua confiança cresce:

| Validações | Status | Comportamento |
|---|---|---|
| 1 (origem) | 🟡 candidate | Sugerido com "experimental" |
| 2 (1 confirmação) | 🟢 validated | Sugerido como "recomendado" |
| 3+ (múltiplas confirmações) | 🔵 proven | Auto-aplicado se `--auto-transfer` estiver ativo |
| 1+ FAILED sem CONFIRMED | 🔴 revoked | Removido das sugestões |

```bash
# Consultar maturidade de um candidato
osforge-db search "transfer-result" 2>/dev/null | grep "<hipótese>" | \
  awk '{confirmed+=/CONFIRMED/; failed+=/FAILED/} END {print confirmed, failed}'
```

Candidatos `proven` (3+ validações) podem ser promovidos a **regras de ferro** ou **gotchas** neste SKILL.md pelo meta-review (Ideia A), fechando o ciclo A↔B.
---

## Relatório final

Ao encerrar o loop:

```
## AutoRefine v3 — Resultado Final

Artefato: <nome>
Modo: Skill | Genérico
Domínio: <domínio da taxonomia>
Iterações: N/budget
Métrica: <inicial> → <final> (delta: +X, melhoria: Y%)
Guard: <N> passes, <M> fails, <K> reworks

### Hipóteses que funcionaram (KEEP)
| # | Hipótese | Delta | Guard | Transfer |
|---|----------|-------|-------|----------|
| 1 | <descrição> | +1.9 | pass | ✅ eligible |
| 3 | <descrição> | +2.2 | pass | ✅ eligible |
| 4b | <descrição> | +1.5 | pass | ❌ specific |

### Hipóteses que falharam (DISCARD)
| # | Hipótese | Razão |
|---|----------|-------|
| 2 | <descrição> | sem melhoria mensurável |
| 4 | <descrição> | guard failure (testes quebraram) |

### Transferências aplicadas nesta sessão
| Hipótese | Origem | Delta original | Delta aqui | Status |
|---|---|---|---|---|
| <descrição> | <projeto> | +22% | +19% | CONFIRMED |

### Candidatos a transferência gerados
| Hipótese genérica | Domínio | Delta |
|---|---|---|
| <descrição> | skill-osforge | +2.2 |
### Memória persistida
- <N> decisões registradas em osforge-db
- <M> candidatos a transferência marcados
- Próxima sessão consultará hipóteses falhas + transfer-candidates automaticamente
- Meta-review elegível? <sim/não> (sessões: X/10, hipóteses: Y/50)

### Próximos passos sugeridos
- <sugestão baseada nos padrões observados>
- <sugestão de transfer-candidates a testar em outros projetos>
```

Ofereça fazer commit com mensagem convencional:
```
refine(<escopo>): autorefine <artefato> — N iterações, metric +X%, <M> transfers
```

Aguarde aprovação explícita antes de commitar.

---

## Gotchas

### Modificar muita coisa por iteração
O loop funciona com hipóteses atômicas. Reescrever o artefato inteiro em uma iteração torna impossível saber o que causou melhoria ou regressão.

### Verify sem Guard
Otimizar uma métrica sem guard é como correr sem freio — a métrica melhora mas o resto quebra. Sempre definir um guard, mesmo que simples (`bun test` ou `tsc --noEmit`).

### Repetir hipóteses falhas
Sem memória cross-sessão, o agente repete as mesmas hipóteses que já falharam. Sempre consultar `osforge-db search "autorefine <artefato>"` antes de formular hipóteses.

### Não fazer snapshot antes
O snapshot é obrigatório. Sem ele, não há como reverter à versão original.
### Critério de sucesso vago
"Ficar melhor" não é critério. O critério precisa ser mecânico e binário — um comando que retorna um número ou pass/fail.

### Avaliar com Haiku
A decisão KEEP/DISCARD deve usar Sonnet. Haiku gera modificações; Sonnet julga resultados.

### Guard files no scope de modificação
Arquivos usados pelo guard NUNCA podem estar no scope de modificação. Se o guard é `bun test`, os arquivos de teste são read-only.

### (v3) Transferir hipóteses sem verificar domínio
Uma hipótese de `nextjs-frontend` não transfere para `database`. Sempre verificar compatibilidade de domínio antes de sugerir transferência.

### (v3) Auto-aplicar meta-ajustes sem aprovação
Meta-otimização muda o próprio processo de melhoria. **Sempre** apresentar propostas ao usuário. Nunca modificar o SKILL.md automaticamente.

### (v3) Confiar em transfer-candidates com 1 validação
Um candidato com 1 validação é 🟡 experimental. Precisa de 2+ confirmações cross-project para ser 🟢 validated. Não tratar como regra até ter evidência suficiente.

---

## Ciclo completo A ↔ B

```
Sessão de autorefine
  → Hipóteses KEEP com delta significativo
    → Avaliação de generalização [Ideia B]
      → transfer-candidate no osforge-db
        → Próxima sessão em outro projeto do mesmo domínio
          → Hipótese transferida como prioritária
            → Validação: CONFIRMED / PARTIAL / FAILED
              → Candidato maduro (proven) após 3+ confirmações
                → Meta-review [Ideia A] promove a proven pattern
                  → Nova regra de ferro ou gotcha neste SKILL.md
                    → Todas as futuras sessões se beneficiam
```

As duas ideias se retroalimentam: **B gera dados** (transfer results), **A analisa esses dados** (meta-review) e **cristaliza os padrões** (ajusta o SKILL.md). O OSForge fica mais inteligente a cada sessão de autorefine, em qualquer projeto.