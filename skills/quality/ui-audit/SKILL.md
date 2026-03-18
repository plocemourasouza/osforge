---
name: ui-audit
description: >
  Auditoria retroativa de 6 pilares de qualidade visual em código frontend
  já implementado. ACIONE após qualquer fase de UI/UX, quando o usuário
  disser "a tela ficou estranha", "não está como eu queria", "revisar o UI",
  "auditar o frontend", "verificar o visual", "checar acessibilidade visual".
  Complementa o openui-genui-layout (que planeja ANTES) auditando DEPOIS.
  Produz relatório estruturado com issues priorizados e planos de correção.
trigger: auditar ui|revisar ui|audit ui|ui review|verificar visual|checar frontend|não ficou como imaginei
model-tier: sonnet
---

# UI Audit

## Papel

Revisor de UI com olho clínico. Avalia código frontend já implementado
contra 6 pilares de qualidade visual, identifica gaps entre o que foi
construído e o que o usuário imaginou, e produz planos de correção acionáveis.

Inspirado no padrão `ui-review` do GSD (get-shit-done).

---

## Inputs

- **Arquivos de componentes** — `.tsx` relevantes da fase auditada
- **`CONTEXT.md` da fase** (`.osforge/phases/{N}-CONTEXT.md`) — decisões acordadas
- **Screenshot ou descrição** — como o usuário imaginava vs. como ficou (opcional mas valioso)

Sempre carregar o CONTEXT.md da fase auditada se existir — ele contém as
decisões que o usuário tomou e que devem ser verificadas.

---

## Os 6 Pilares

### Pilar 1 — Hierarquia Visual
O olho do usuário sabe o que é mais importante?

Verificar:
- Há uma âncora visual clara em cada tela (título, CTA primário, dado principal)?
- Peso tipográfico e tamanho guiam a leitura na ordem correta?
- Elementos secundários estão visualmente subordinados?
- Não há competição entre múltiplos elementos de igual destaque?

### Pilar 2 — Consistência
O sistema parece feito por uma só mente?

Verificar:
- Espaçamentos seguem escala consistente (não valores arbitrários)?
- Variantes de componentes shadcn/ui usadas corretamente (não misturando `outline` e `ghost` sem critério)?
- Tipografia usa tokens do design system, não valores hard-coded?
- Cores seguem semantic tokens (`primary`, `muted`, `destructive`) sem exceções injustificadas?
- Bordas, radii e sombras consistentes ao longo da feature?

### Pilar 3 — Feedback e Estados
O usuário sabe o que está acontecendo?

Verificar:
- Estados de loading têm skeleton ou spinner adequado?
- Estados de erro têm mensagem útil e ação de recuperação?
- Ações destrutivas têm confirmação?
- Estados vazios têm explicação e call-to-action?
- Formulários têm validação inline com mensagem clara?
- Ações assíncronas têm feedback imediato (botão desabilitado, loading state)?

### Pilar 4 — Responsividade
Funciona em todos os breakpoints relevantes?

Verificar:
- Layout não quebra em mobile (< 640px) e tablet (640–1024px)?
- Textos não transbordam containers em telas menores?
- Tabelas longas têm scroll horizontal ou adaptação mobile?
- Touch targets têm mínimo de 44px em mobile?
- Imagens e grids têm comportamento responsivo correto?

### Pilar 5 — Acessibilidade Visual
Usuários com baixa visão conseguem usar?

Verificar:
- Contraste de texto atende WCAG AA (4.5:1 para texto normal, 3:1 para texto grande)?
- Focus states visíveis em todos os elementos interativos?
- Ícones sem label têm `aria-label` ou tooltip?
- Formulários têm `<label>` associado a cada input?
- Cores não são o único indicador de estado (ex: erro vermelho SEM ícone)?

### Pilar 6 — Alinhamento com Decisões do Usuário
O que foi construído reflete o que foi acordado no `phase-discussion`?

Verificar cada decisão registrada no `CONTEXT.md`:
- Layout escolhido (card, lista, grid) foi implementado corretamente?
- Interações acordadas (modal, slide-over, inline) estão presentes?
- Tom visual (denso, espaçado, minimalista) foi respeitado?
- Decisões explicitamente postergadas (v2+) não foram acidentalmente implementadas?

---

## Processo de Auditoria

### 1. Carregar contexto
- Ler CONTEXT.md da fase se existir
- Identificar arquivos `.tsx` a auditar
- Se screenshot disponível: comparar visualmente

### 2. Auditar pilar por pilar
Para cada pilar, avaliar: ✅ OK | ⚠️ Atenção | ❌ Problema

Registrar issues com:
- **Localização:** arquivo + linha aproximada
- **Descrição:** o que está errado e por quê
- **Impacto:** Alto (bloqueia uso) / Médio (degrada experiência) / Baixo (cosmético)
- **Correção sugerida:** código ou orientação específica

### 3. Gerar relatório

```markdown
---
type: osforge-ui-audit
phase: "{N} — {título}"
audited_at: {data}
overall: OK | APROVADO COM RESSALVAS | REPROVADO
---

# UI Audit — Phase {N}: {título}

## Resumo Executivo
{2-3 frases: o que está bom, os principais problemas, ação recomendada}

## Resultado por Pilar

| Pilar | Status | Issues |
|---|---|---|
| 1. Hierarquia Visual | ✅/⚠️/❌ | {N} |
| 2. Consistência | ✅/⚠️/❌ | {N} |
| 3. Feedback e Estados | ✅/⚠️/❌ | {N} |
| 4. Responsividade | ✅/⚠️/❌ | {N} |
| 5. Acessibilidade Visual | ✅/⚠️/❌ | {N} |
| 6. Alinhamento com Decisões | ✅/⚠️/❌ | {N} |

## Issues por Prioridade

### 🔴 Alto (resolver antes de ship)
- [ ] **{arquivo}:{linha aprox}** — {descrição} → {correção}

### 🟡 Médio (resolver no próximo sprint)
- [ ] **{arquivo}:{linha aprox}** — {descrição} → {correção}

### 🟢 Baixo (backlog)
- [ ] **{arquivo}:{linha aprox}** — {descrição} → {correção}

## Plano de Correção

Se houver issues Alto ou Médio, oferecer:
- **Correção imediata:** lista de tasks prontas para `story-executor`
- **Estimativa:** S/M/L de esforço

## O que ficou bom
{reconhecer o que foi bem implementado — evitar relatório apenas negativo}
```

Salvar em `.osforge/phases/{N}-UI-AUDIT.md`.

---

## Integração com outros skills

- **`openui-genui-layout`** → planeja ANTES da implementação (contrato de design)
- **`ui-audit`** → audita DEPOIS da implementação (verificação de qualidade)
- **`phase-discussion`** → o `CONTEXT.md` é a referência para o Pilar 6
- **`story-executor`** → executa as correções identificadas pelo audit

O fluxo ideal é: `phase-discussion` → `openui-genui-layout` → implementação → `ui-audit`.
