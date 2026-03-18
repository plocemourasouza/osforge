# Regras de Triage

## Classificação de Complexidade

### QUICK — Execução direta

**TODOS os critérios devem se aplicar:**
- Escopo claro e limitado (1-3 arquivos)
- Zero ambiguidade no que fazer
- Sem decisões arquiteturais novas
- Sem novos models/schemas no Prisma
- Sem integrações externas novas
- Zero blast radius (sem consequências não-intencionais)

**Sinais típicos do usuário:**
- "corrigir", "fix", "ajustar", "bug"
- "adicionar campo", "mudar cor", "renomear"
- "refatorar função", "extrair componente"
- "adicionar validação em X"

**Pipeline:** spec → implement → review
**Artefatos:** tech-spec.md apenas

---

### STANDARD — Feature com planejamento

**ALGUM dos critérios se aplica:**
- Feature com escopo definido mas multi-arquivo (4-10 arquivos)
- Precisa de novos models ou schema changes no Prisma
- Impacta API routes ou Server Actions existentes
- Cria novo fluxo de UI (mas domínio conhecido)
- Integração com serviço já configurado (ex: Stripe já existe, adicionar novo webhook)

**MAS domínio é conhecido e stack é o padrão do projeto.**

**Sinais típicos do usuário:**
- "criar feature de", "adicionar módulo de"
- "implementar fluxo de", "integrar com"
- "novo CRUD de", "adicionar autenticação em"

**Pipeline:** spec → arch-check (se schema) → stories → implement loop → review
**Artefatos:** spec.md, stories/

---

### COMPLEX — Sistema com planejamento completo

**ALGUM dos critérios se aplica:**
- Sistema ou módulo inteiro novo
- Requisitos ambíguos que precisam ser destilados
- Múltiplas integrações externas novas
- Decisões arquiteturais significativas (nova infra, novo padrão)
- Impacto cross-cutting em vários módulos existentes
- Requisitos de compliance (LGPD, TSE, ICP-Brasil)
- Multi-tenant ou multi-role com regras complexas

**Sinais típicos do usuário:**
- "construir sistema de", "novo produto", "nova plataforma"
- "migrar de X para Y", "redesenhar módulo"
- "sistema completo com", "quero que tenha"
- Descrições longas com múltiplas features interconectadas

**Pipeline:** prd → architecture → epics → readiness-gate → sprint loop
**Artefatos:** prd.md, architecture.md, epics/, sprint-status.yaml

---

## Decisão em Caso de Dúvida

Quando a classificação não é clara:

1. **Na dúvida entre QUICK e STANDARD** → STANDARD
   (é melhor planejar um pouco mais do que descobrir no meio que faltou)

2. **Na dúvida entre STANDARD e COMPLEX** → Perguntar ao usuário:
   "Isso me parece entre STANDARD e COMPLEX. Se você já tem clareza do
   que construir e é um módulo isolado, STANDARD basta. Se os requisitos
   ainda estão se formando ou há muitas peças interconectadas, COMPLEX
   garante que nada se perca. O que você acha?"

3. **Override do usuário** sempre prevalece:
   "Quero tratar como QUICK" → respeitar, mesmo que tecnicamente seja STANDARD
   "Faz o planejamento completo" → COMPLEX independente da classificação
