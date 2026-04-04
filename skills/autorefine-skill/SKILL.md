---
name: autorefine-skill
description: "Refinamento autônomo iterativo com loop autoresearch. ACIONE quando: usuário pede 'melhorar uma skill', 'otimizar a skill X', 'a skill Y não está funcionando bem', 'iterar sobre skill', 'autorefine', 'refinar código', 'otimizar performance', 'melhorar métrica X'. Generalizado para qualquer artefato com métrica mensurável — skills, código, prompts, configs, docs. Keywords: melhorar skill, refinar skill, otimizar, autorefine, iteração autônoma, autoresearch, loop de melhoria, self-improving, guard, verify."
model: sonnet
allowed-tools: Read, Write, Bash, Glob, Grep
metadata:
  author: osforge
  version: '2.0'
  inspired_by: 'karpathy/autoresearch, uditgoenka/autoresearch, alfonsograziano/auto-agent'
  changelog: 'v2.0 — verify+guard separation, osforge-db memory, domain generalization, eval packages'
---

## Estado do projeto
!`osforge-db list-projects --status=active 2>/dev/null | head -3 || echo "nenhum projeto ativo"`
!`osforge-db search "autorefine" 2>/dev/null | head -5 || echo "sem histórico de autorefine"`

# AutoRefine v2

## Princípio

Aplicar o loop de pesquisa autônoma do Karpathy a **qualquer artefato com métrica mensurável**: skills, código, prompts, configs, documentação. O agente formula uma hipótese → aplica uma mudança atômica → verifica com métrica mecânica → protege com guard contra regressões → mantém ou reverte → registra no banco → repete.

**constraint + mechanical metric + autonomous iteration = compounding gains**

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
```

Se existem hipóteses anteriores que falharam, **nunca repeti-las**. Listar as hipóteses falhas conhecidas antes de formular novas.

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
  2. [haiku]  Formula hipótese: "se eu modificar X, a métrica Y vai melhorar porque Z"
  3. [haiku]  Aplica UMA modificação atômica
  4. [haiku]  git commit -m "experiment: <hipótese resumida>"
  5. [haiku]  Executa Verify → coleta métrica
  6. [haiku]  Executa Guard → verifica que nada quebrou
  7. [sonnet] Decide: KEEP / REWORK / DISCARD (ver tabela acima)
  8. [sonnet] Se DISCARD → git revert HEAD
     [sonnet] Se REWORK → tenta ajustar (max 2x), depois DISCARD
  9. Registra no log + osforge-db
```

### Modelo por etapa (smart-model-dispatch)

| Etapa | Modelo | Razão |
|---|---|---|
| Leitura + hipótese + modificação | Haiku | Mecânico, baixo custo |
| Execução verify + guard | Haiku | Rodar comandos |
| Avaliação + decisão | Sonnet | Requer julgamento |
| Síntese final (relatório) | Sonnet | Análise de padrões |

Usar Opus apenas se o critério for ambíguo e exigir raciocínio sobre tradeoffs arquiteturais.

---

## Log de iterações (TSV + markdown)

### TSV (machine-readable)

Manter `autorefine-results.tsv` no diretório do artefato:

```tsv
iteration	commit	metric	delta	guard	status	hypothesis
0	a1b2c3d	85.2	0.0	pass	baseline	initial state
1	b2c3d4e	87.1	+1.9	pass	keep	add explicit TypeScript types to output rules
2	-	86.5	-0.6	pass	discard	refactor section ordering (no improvement)
3	c4d5e6f	89.3	+2.2	pass	keep	add code block examples for each pattern
4	d5e6f7g	91.0	+1.7	fail	rework	aggressive minification broke guard tests
4b	e6f7g8h	90.8	+1.5	pass	keep	conservative minification (guard-safe)
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

## Resultado final
- Melhor versão: iteração N
- Métrica inicial: X
- Métrica final: Y (delta: +Z, melhoria de W%)
- Hipóteses que funcionaram: ...
- Hipóteses que falharam: ...
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

## Relatório final

Ao encerrar o loop:

```
## AutoRefine v2 — Resultado Final

Artefato: <nome>
Modo: Skill | Genérico
Iterações: N/budget
Métrica: <inicial> → <final> (delta: +X, melhoria: Y%)
Guard: <N> passes, <M> fails, <K> reworks

### Hipóteses que funcionaram (KEEP)
| # | Hipótese | Delta | Guard |
|---|----------|-------|-------|
| 1 | <descrição> | +1.9 | pass |
| 3 | <descrição> | +2.2 | pass |

### Hipóteses que falharam (DISCARD)
| # | Hipótese | Razão |
|---|----------|-------|
| 2 | <descrição> | sem melhoria mensurável |
| 4 | <descrição> | guard failure (testes quebraram) |

### Memória persistida
- <N> decisões registradas em osforge-db
- Próxima sessão consultará hipóteses falhas automaticamente

### Próximos passos sugeridos
- <sugestão baseada nos padrões observados>

Snapshot original: <path>
```

Ofereça fazer commit com mensagem convencional:
```
refine(<escopo>): autorefine <artefato> — N iterações, metric +X%
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
