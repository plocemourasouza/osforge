---
name: requirements-clarify
description: "Clarificação estruturada de requisitos ANTES do plano técnico. ACIONE quando: spec tem áreas vagas ou underspecificadas, usuário disse 'pode ser qualquer coisa', os requisitos deixam margem para múltiplas interpretações, ANTES de spec-builder em demandas novas. Keywords: clarificar requisitos, requirements clarification, underspecified, ambiguous requirements, clarify, antes do plano, esclarecer requisitos."
model: sonnet
allowed-tools: Read, Write, Glob
metadata:
  author: osforge
  version: '1.0'
  source: github/spec-kit (MIT)
  adapted_by: osforge
---

## Contexto
!`[ -f project-context.md ] && head -15 project-context.md || echo "project-context.md não encontrado"`
!`ls .osforge/designs/ 2>/dev/null | head -5 && echo "Designs encontrados" || echo "Nenhum design document encontrado"`

# Requirements Clarify

## Papel

Facilitador de clarificação baseado em cobertura. Identifica sistematicamente
as áreas underspecificadas de uma demanda e as resolve antes que o plano
técnico seja gerado — prevenindo retrabalho de spec e implementação.

Adaptado do padrão `/speckit.clarify` do github/spec-kit.

---

## Quando usar

- Antes de `spec-builder` para demandas com termos vagos
- Quando brainstorming gerou design aprovado mas com gaps
- Sempre que o usuário usar palavras como "funcionar bem", "ser rápido", "integrar com X", "de alguma forma", sem detalhar
- Para features complexas com múltiplos stakeholders ou fluxos alternativos

**Não usar** para: tasks mecânicas claras, bugs com causa conhecida, extensões triviais com padrão estabelecido.

---

## Processo

### 1. Analisar a demanda por dimensões de cobertura

Verificar cobertura em cada dimensão:

**Funcional**
- O happy path está completo e sem gaps?
- Os fluxos alternativos (error states, edge cases) estão definidos?
- As regras de negócio estão explícitas ou implícitas?

**Dados**
- Quais dados são necessários para cada ação?
- Qual é o formato esperado das entradas e saídas?
- Há limites de volume, tamanho, ou frequência?

**Usuário / UX**
- Quem são os usuários e qual é o contexto de uso?
- Que nível de feedback visual é necessário (loading, error, success)?
- Há considerações de acessibilidade ou internacionalização?

**Integração**
- Com que sistemas externos isso precisa se integrar?
- Quais são os contratos de API esperados?
- Há dependências de timing (sync vs async)?

**Segurança / Privacidade**
- Quais dados são sensíveis?
- Quem pode ver/editar o quê?
- Há requisitos de LGPD ou auditoria?

### 2. Gerar perguntas de clarificação

Para cada gap identificado, formular uma pergunta específica e acionável:

```markdown
## Perguntas de Clarificação — {feature}

**Funcional (3 perguntas)**
1. {pergunta específica com contexto}
   *Por que importa: sem isso, spec pode gerar ACs incorretos para {caso X}*

2. {pergunta sobre fluxo alternativo}
   *Por que importa: {impacto na implementação}*

**Dados (2 perguntas)**
3. {pergunta sobre formato/limite de dados}

**UX (1 pergunta)**
4. {pergunta sobre feedback visual necessário}

**Segurança (1 pergunta)**
5. {pergunta sobre acesso/permissões}
```

Apresentar as perguntas em grupos por dimensão. Máximo 8-10 perguntas no total — priorizar as mais impactantes.

### 3. Processar respostas

Para cada resposta recebida:
- Registrar a decisão
- Identificar se a resposta gera novas perguntas (máximo 2 rounds de follow-up)
- Marcar a área como "clarificada" ✅

### 4. Gerar Clarifications Record

Após todas as respostas, consolidar em:

```markdown
---
type: osforge-clarifications
feature: "{nome}"
clarified_at: {data}
feeds: [spec-builder]
---

# Clarifications: {nome da feature}

## Decisões Tomadas

### Funcional
- **{área}:** {decisão} — registrada em {data}
- **{área}:** {decisão}

### Dados
- **{área}:** {decisão}

### UX
- **{área}:** {decisão}

### Segurança
- **{área}:** {decisão}

## Áreas Explicitamente Fora do Escopo
- {item que o usuário confirmou que NÃO está no escopo}

## Premissas Assumidas (sem confirmação explícita)
- {premissa assumida porque o usuário disse "qualquer coisa serve"}
```

Salvar em `.osforge/designs/{feature-slug}-clarifications.md`.

Handoff: "Clarificações completas. Pronto para chamar `spec-builder` com este documento como input adicional."

---

## Gotchas

- **Fazer perguntas óbvias**: perguntas que qualquer desenvolvedor responderia da mesma forma não precisam ser feitas. Focar nas ambiguidades que levariam a decisões diferentes de implementador para implementador.
- **Mais de 10 perguntas de uma vez**: sobrecarrega o usuário e sinaliza que a demanda está mal compreendida. Se precisar de mais de 10, dividir em rounds.
- **Não registrar premissas assumidas**: se o usuário disse "qualquer coisa serve" para algo importante, registrar a premissa assumida explicitamente. Premissas implícitas são a fonte mais comum de retrabalho.
- **Segunda rodada de clarificação indefinida**: máximo 2 rounds de follow-up. Após isso, o que ainda não está claro deve ser registrado como premissa assumida e revisitado na fase de spec.
- **Clarificar o óbvio**: se a resposta é universalmente "sim" para o stack OSForge (ex: "vai usar TypeScript?"), não perguntar — registrar como premissa assumida diretamente.
