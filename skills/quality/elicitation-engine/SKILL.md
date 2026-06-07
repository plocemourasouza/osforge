---
name: elicitation-engine
description: "Refinamento iterativo de outputs (specs, PRDs, decisões arquiteturais, qualquer artefato) via menu interativo de técnicas de elicitação estruturadas. ACIONE quando: pedirem refine isso, melhorar ou aprofundar uma spec/PRD, dig deeper numa decisão de design, que perguntas estou ignorando, fortalecer seção fraca de um documento antes de finalizar. Keywords: elicitar, refine, refinamento, aprofundar, melhorar output, spec, PRD, elicitation, dig deeper, iterar. Não acione para: caça de edge cases em código (use edge-case-hunter) nem review de código (use code-review-checklist)."
trigger: elicit|refine output|dig deeper|melhorar spec|aprofundar
model-tier: sonnet
---

# Elicitation Engine

## Objetivo
Forçar reconsideração, refinamento e melhoria de output recente
usando técnicas estruturadas de elicitação. Cada técnica ataca o
conteúdo de um ângulo diferente para revelar gaps, melhorar decisões,
e fortalecer a qualidade do artefato.

## Inputs
- **content** — Conteúdo/seção a ser refinado (do contexto da conversa)
- **focus_area** (opcional) — Área específica para focar a elicitação

## Processo

### 1. Carregar Métodos
Ler `./methods.csv` (campos: num, category, method_name, description, output_pattern)

### 2. Análise de Contexto
- Analisar conteúdo atual: tipo, complexidade, riscos, potencial criativo
- Identificar áreas mais fracas do conteúdo que se beneficiariam de elicitação

### 3. Seleção Inteligente
1. Selecionar 3 métodos que melhor se aplicam ao contexto e tipo de conteúdo
2. Balancear entre foundational e especializados
3. Priorizar métodos que atacam as áreas mais fracas identificadas

### 4. Apresentar e Executar

```
**Elicitation Engine**
Escolha (1-3), [r] Reshuffle, [x] Prosseguir:

1. {Método} — {descrição curta}
2. {Método} — {descrição curta}
3. {Método} — {descrição curta}
r. Novos 3 métodos
a. Listar todos os métodos disponíveis
x. Finalizar com conteúdo atual
```

**Se 1-3:** Executar método selecionado sobre o conteúdo.
  - Aplicar criativamente ao conteúdo/seção sendo refinado
  - Mostrar versão melhorada com o que o método revelou
  - Perguntar: "Aplicar mudanças? [S] Sim / [N] Não / {instrução livre}"
  - Se sim → aplicar ao artefato. Se não → descartar.
  - Re-apresentar menu para mais elicitações

**Se r:** Selecionar 3 novos métodos diversos, apresentar.

**Se a:** Listar todos os métodos com descrições em tabela compacta.
  Permitir seleção por número ou nome.

**Se x:** Retornar conteúdo refinado final ao skill chamador.

### 5. Acumulação
Cada método se acumula sobre melhorias anteriores.
Manter tracking do que foi aplicado para não repetir.

## Integração
Quando invocado de dentro de outro skill (spec-builder, prd-builder, etc.):
1. Receber conteúdo da seção sendo trabalhada
2. Executar loop de elicitação
3. Retornar conteúdo refinado quando usuário selecionar 'x'
4. Skill chamador continua com o conteúdo melhorado
