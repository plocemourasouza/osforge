# OSForge — Usage Examples

10 cenários reais de uso, do mais simples ao mais complexo.

---

## Exemplo 1 — Quick fix: corrigir bug de autenticação

**Cenário:** Login retorna 500 após deploy. Precisa de diagnóstico rápido.

**O que o OSForge faz:**
O `intelligent-routing` detecta domínio DEBUG + SECURITY automaticamente e
ativa o `debugger` sem que você precise mencionar nada.

```
Você: "O endpoint /api/auth/login está retornando 500 após o deploy de hoje"

🤖 Detectado: Debug + Backend — aplicando @debugger...

→ debugger executa os 10 steps:
   1. Reproduz o erro localmente
   2. Lê os logs da Vercel
   3. Isola o stack trace
   4. Identifica root cause (env var NEXTAUTH_SECRET ausente no ambiente)
   5. Propõe fix + verifica via verification-before-completion
```

**Skills ativadas:** `debugger` (auto) → `verification-before-completion`

---

## Exemplo 2 — Nova feature STANDARD: módulo de convites de equipe

**Cenário:** Adicionar convites por email ao SaaS. Multi-arquivo, domínio conhecido.

```
Você: "Quero adicionar um sistema de convites de equipe. O usuário admin
envia email, o convidado clica e entra direto com a organização já configurada."

🤖 Detectado: Feature multi-domínio — sugestão: ativar Orchestrator.

→ orchestrator:
   TRIAGE: STANDARD (schema change + nova API + UI + email)

→ phase-discussion:
   "Convite expira em quantos dias? Reenvio automático? Limite de convites?"
   → CONTEXT.md gerado com suas respostas

→ spec-builder (lê CONTEXT.md):
   → spec.md com ACs testáveis

→ epic-decomposer:
   Epic 1: Schema (Invitation model + relações)
   Epic 2: API (criar, aceitar, revogar convite)
   Epic 3: UI (tela de convites + email template)

→ story-executor (wave execution):
   Wave 1 || Schema Prisma + Resend email setup
   Wave 2 || POST /api/invitations + GET /api/invitations/[token]
   Wave 3 →  InvitationsPage + InviteForm

→ code-reviewer + edge-case-hunter
```

**Skills ativadas:** `orchestrator` → `phase-discussion` → `spec-builder` →
`epic-decomposer` → `story-executor` → `dispatching-parallel-agents` →
`code-reviewer` → `edge-case-hunter`

---

## Exemplo 3 — UI com identidade visual: dashboard financeiro

**Cenário:** Criar dashboard de receitas para a Essent. Precisa ter visual
profissional de contabilidade, não o shadcn padrão.

```
Você: "Cria um dashboard de receitas mensais para a Essent.
Quero algo sério, estilo fintech, dark mode."

🤖 Detectado: Frontend + Design — aplicando @frontend-engineer...

→ ui-design-intelligence:
   Produto: Dashboard contábil / Indústria: Fintech / Keywords: dark, sério

   Design System Spec gerado:
   ─ Estilo: Enterprise Dark + Fintech Modern
   ─ Paleta: #060b18 fundo | #0d1b2a surface | #0ea5e9 primary
             #00c896 positivo (crédito) | #ff4757 negativo (débito)
   ─ Tipografia: Space Grotesk 600 (heading) + Inter 400 (body) + IBM Plex Mono (valores)
   ─ Charts: Line Chart (evolução mensal) + Stacked Bar (breakdown categoria)
   ─ UX: valores numéricos sempre à direita, mono font em tabelas,
         verde/vermelho com ícone (não só cor)

→ openui-genui-layout (usa o design system como input):
   Padrão: dashboard
   ```openui
   root = Stack([header, kpi_row, charts_row, transactions_table])
   kpi_row = Grid([revenue_card, expenses_card, profit_card, margin_card])
   revenue_card = StatCard("Receita", "R$ 142.800", "up")
   charts_row = Grid([monthly_chart, breakdown_chart])
   monthly_chart = LineChart(months, [revenue_series, expenses_series])
   ```

→ frontend-engineer implementa com os tokens do design system

→ ui-audit verifica os 6 pilares (incluindo Pilar 6: alinhamento com o spec)
```

**Skills ativadas:** `ui-design-intelligence` → `openui-genui-layout` →
`frontend-engineer` → `ui-audit`

---

## Exemplo 4 — Auditoria de segurança: módulo de pagamentos Stripe

**Cenário:** Antes de ir para produção, auditar o módulo de billing recém-implementado.

```
Você: "Faz um audit de segurança no módulo de pagamentos antes do deploy"

🤖 Detectado: Security + Backend — aplicando @security-auditor...

→ security-auditor (Trail of Bits methodology):
   1. Threat modeling: superfície de ataque (webhook, checkout, portal)
   2. Verifica: idempotency keys nos webhooks? ✅
   3. Verifica: validação de assinatura Stripe? ✅
   4. Verifica: preços hardcoded no frontend? ❌ CRÍTICO
   5. Verifica: RLS no Supabase para subscription data? ⚠️ revisar
   6. Verifica: logging de dados de cartão? ✅ (ausente — correto)

→ insecure-defaults varre fail-open patterns:
   ❌ Encontrou: plano não verificado no middleware → assume free tier
   → Gera task de correção

→ differential-review nos PRs recentes do módulo

→ Relatório final com issues priorizados (Alto/Médio/Baixo)
```

**Skills ativadas:** `security-auditor` → `insecure-defaults` → `differential-review`

---

## Exemplo 5 — Migração de schema com wave execution

**Cenário:** Adicionar multi-tenancy ao sistema. Envolve 8 tabelas,
migrations interdependentes, e seeds.

```
Você: "Precisamos adicionar suporte multi-tenant. Cada empresa tem seus
próprios usuários, projetos e configurações. Hoje tudo é flat."

→ orchestrator: COMPLEX (novo sistema, impacta todo o codebase)

→ arch-builder:
   ADR-001: Row-Level Security via organizationId em todas as tabelas
   ADR-002: Middleware de tenant detection via subdomínio
   ADR-003: Soft migration (sem perda de dados existentes)

→ epic-decomposer → 3 épicos, 14 stories

→ story-executor com wave execution:

   Wave 1 (paralelo) — fundação:
   ║ Organization model + migration
   ║ OrganizationMember model + migration

   Wave 2 (paralelo, após Wave 1) — entidades dependentes:
   ║ Adicionar organizationId em User
   ║ Adicionar organizationId em Project
   ║ Adicionar organizationId em Settings

   Wave 3 (após Wave 2) — RLS e middleware:
   → RLS policies no Supabase
   → Middleware de tenant resolution

   Wave 4 (após Wave 3) — seed e migration dos dados existentes:
   → Script de migration de dados (organização padrão)
   → Seed com dados de teste multi-tenant

→ verification-before-completion:
   bun prisma validate && bun tsc --noEmit && bun run test
```

**Skills ativadas:** `orchestrator` → `arch-builder` → `epic-decomposer` →
`story-executor` → `dispatching-parallel-agents` → `prisma-expert` →
`verification-before-completion`

---

## Exemplo 6 — Dados sensíveis com modelo local (LGPD)

**Cenário:** Gerar relatórios contábeis da Essent com dados de clientes.
Não pode sair do ambiente local por compliance LGPD.

```
Você: "Precisa gerar um script que processa os lançamentos contábeis
do mês e gera um relatório de DRE. Os dados não podem ir para API externa."

→ smart-model-dispatch detecta: tarefa Haiku-eligible + dados sensíveis
   → recomenda track local

→ llmfit-advisor:
   llmfit recommend --json --use-case coding --limit 3
   ✅ qwen2.5-coder:14b → fit: Perfect | 28 tok/s | LGPD-safe

→ Executa localmente via Ollama:
   - Sem tokens de API consumidos
   - Dados de clientes nunca saem do Mac
   - qwen2.5-coder:14b para geração do script de DRE

→ prisma-expert valida as queries geradas (rodando em API para revisão)
→ postgres-optimization verifica se há N+1 no relatório
```

**Skills ativadas:** `smart-model-dispatch` → `llmfit-advisor` →
`prisma-expert` → `postgres-optimization`

---

## Exemplo 7 — Onboarding de projeto existente (brownfield)

**Cenário:** Novo projeto herdado de cliente da OSystems. Precisa entender
o que existe antes de começar a trabalhar.

```
Você: "Tenho um projeto Next.js de cliente que vou assumir.
Precisa entender o que tem antes de mexer em qualquer coisa."

→ context/project-context-generator:
   Analisa o codebase e gera project-context.md com:
   ─ Stack identificado: Next.js 14, Prisma, MySQL, JWT próprio (sem Supabase)
   ─ Padrões de código: Pages Router (não App Router)
   ─ Modelos principais: User, Order, Product, Category
   ─ Dívidas técnicas identificadas: console.log em produção (12 ocorrências),
     any em 8 arquivos, sem testes
   ─ Pontos de atenção: auth sem refresh token, sem RLS

→ orchestrator carrega o project-context.md em todas as sessões seguintes

→ security-threat-model mapeia os riscos do auth caseiro

→ adversarial-review no módulo mais crítico (pagamentos):
   "Faça uma revisão cínica assumindo que o código foi escrito por
   um dev júnior sem experiência em segurança"
```

**Skills ativadas:** `context/project-context-generator` → `orchestrator` →
`security-threat-model` → `adversarial-review`

---

## Exemplo 8 — Especialista de negócio: estratégia de vendas (The Agency)

**Cenário:** LinkMeTur precisa estruturar um processo de prospecção
outbound para agências de turismo B2B.

```
Você: "Preciso montar uma sequência de prospecção para agências de turismo.
Target: agências de médio porte no Sul do Brasil, 5-20 funcionários."

→ intelligent-routing: domínio Sales → sem código → aciona The Agency

→ skills/agency/sales/SKILL.md:
   "Ativar o Outbound Strategist"

→ Outbound Strategist (Agency specialist):
   ─ ICP refinado: agências 5-20 pessoas, com site próprio, Sul do Brasil
   ─ Sequência de 7 touchpoints (email + LinkedIn + WhatsApp)
   ─ Email #1: hook de dor específico do setor (sazonalidade, margens)
   ─ Email #3: case de resultado mensurável
   ─ Call to action: demo de 20 min, não "conversa"
   ─ Objeções mapeadas: "já uso outra plataforma", "margem pequena"
   ─ Script de discovery call adaptado ao contexto de turismo B2B
```

**Skills ativadas:** `skills/agency/sales/SKILL.md` →
`Outbound Strategist` specialist

---

## Exemplo 9 — Refinar uma skill que está produzindo outputs ruins

**Cenário:** A skill `docs-writer` está gerando documentação muito genérica,
sem respeitar o tom técnico dos projetos da OSystems.

```
Você: "A skill docs-writer não está produzindo o que quero.
Ela gera textos muito genéricos, sem o tom técnico que preciso."

→ autorefine-skill:

   Setup:
   ─ Skill alvo: skills/docs-writer/
   ─ Problema: tom genérico, sem especificidade técnica
   ─ Critério de sucesso: inclui stack específico, usa linguagem técnica
     precisa, não usa "solução robusta" ou "plataforma escalável"
   ─ Prompts de teste: 3 requests reais de documentação
   ─ Budget: 6 iterações

   Loop (Haiku executa, Sonnet avalia):
   ─ Iteração 1: adiciona instrução de especificidade → KEEP (melhora 1/3)
   ─ Iteração 2: proíbe termos genéricos explicitamente → KEEP (2/3)
   ─ Iteração 3: adiciona exemplos de tom → KEEP (3/3) ← convergência
   ─ Iteração 4: tenta adicionar template → DISCARD (piora)
   ─ Iteração 5: ajusta exemplos → KEEP (mantém 3/3)
   ─ Iteração 6: budget esgotado

   Resultado: val 0/3 → 3/3 (100%)
   Commit: "refine(skills): autorefine docs-writer — 6 iterações, val +100%"
```

**Skills ativadas:** `autorefine-skill` → `smart-model-dispatch`
(Haiku para iterações, Sonnet para avaliação)

---

## Exemplo 10 — Validação pré-deploy com checklist completo

**Cenário:** Feature de billing completa, pronta para ir para produção.
Verificar tudo antes do deploy na Vercel.

```
Você: "Feature de billing finalizada. Quero verificar tudo antes do deploy."

→ verification-before-completion:
   Gate 1: bun tsc --noEmit → 0 erros ✅
   Gate 2: bun run lint → 0 warnings ✅
   Gate 3: bun run test → 47 passed, 0 failed ✅
   Gate 4: bun run build → exit 0 ✅
   Gate 5: bun prisma validate → schema válido ✅

→ python3 .scripts/validate.py --pre-deploy:
   [types]   ✅ passou (2.1s)
   [lint]    ✅ passou (1.8s)
   [tests]   ✅ passou (12.4s)
   [build]   ✅ passou (34.2s)
   [prisma]  ✅ passou (0.9s)
   ✅ 5/5 checks passaram

→ security-auditor faz revisão final do módulo:
   ─ Webhook signature validation: ✅
   ─ Idempotency keys: ✅
   ─ Sem PII nos logs: ✅

→ quality/readiness-gate:
   [GO] — todos os ACs verificados, zero issues críticos abertos
   Pronto para: git tag v1.2.0 && vercel --prod

→ git-commit-helper:
   Gera CHANGELOG.md da v1.2.0 com todos os commits do billing
```

**Skills ativadas:** `verification-before-completion` → `validate.py` →
`security-auditor` → `quality/readiness-gate` → `git-commit-helper` →
`vercel-deploy`

---

## Mapa rápido de cenários × skills

| Cenário | Skills principais |
|---|---|
| Quick fix / bug | `debugger` (auto) → `verification-before-completion` |
| Feature STANDARD | `orchestrator` → `phase-discussion` → `spec-builder` → `story-executor` |
| UI com identidade | `ui-design-intelligence` → `openui-genui-layout` → `ui-audit` |
| Auditoria segurança | `security-auditor` → `insecure-defaults` → `differential-review` |
| Schema complexo | `arch-builder` → `story-executor` + waves → `prisma-expert` |
| Dados LGPD | `smart-model-dispatch` → `llmfit-advisor` → local model |
| Projeto herdado | `project-context-generator` → `security-threat-model` |
| Negócio / vendas | `agency/sales/` → especialista específico |
| Skill com problema | `autorefine-skill` → loop autônomo |
| Pré-deploy | `verification-before-completion` → `readiness-gate` → `git-commit-helper` |
