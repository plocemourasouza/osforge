---
name: marketing-context
description: "Criar ou atualizar o contexto de marketing do projeto. Usar antes de qualquer workflow de marketing. Gera `.osforge/marketing-context.md` que todos os workflows consultam como fonte de verdade sobre produto, audiência, posicionamento e voz."
metadata:
  version: 2.0.0
  origin: coreyhaines31/marketingskills (product-marketing-context v1.1.0)
  adapted-for: osforge
---

# Contexto de Marketing do Projeto

Você ajuda o usuário a criar e manter o documento de contexto de marketing.
Esse documento captura informações de posicionamento e messaging que TODOS os
workflows de marketing, mídia paga e vendas referenciam como fonte única de verdade.

**Arquivo de saída:** `.osforge/marketing-context.md`

---

## Integração com OSForge

### Fontes de contexto existentes

Antes de perguntar qualquer coisa ao usuário, verificar estas fontes nesta ordem:

1. **`.osforge/marketing-context.md`** — Se existe, ler e oferecer atualização
2. **`project-context.md`** (raiz ou `docs/`) — Extrair stack, produto e audiência
3. **`.osforge/STATE.md`** — Verificar decisões de produto anteriores
4. **`README.md`** do projeto — Nome, descrição, features

### Regra de não-duplicação

Se `project-context.md` já tem informações sobre o produto (nome, stack, features),
NÃO duplicar. Referenciar: "Stack e features cobertos em project-context.md."
O marketing-context foca no que project-context NÃO cobre: posicionamento,
audiência, voz, dores do cliente, diferenciação e prova social.

---

## Workflow

### Passo 1: Verificar contexto existente

Verificar se `.osforge/marketing-context.md` existe.
Também verificar `.agents/product-marketing-context.md` e
`.claude/product-marketing-context.md` como fallback de migração.

**Se encontrar em local antigo:** oferecer migração automática:
```
Encontrei contexto de marketing em .agents/product-marketing-context.md.
Vou migrar para .osforge/marketing-context.md para integrar com o OSForge.
```

**Se marketing-context.md existe:**
- Ler e resumir o que está capturado
- Perguntar quais seções quer atualizar
- Só coletar info das seções escolhidas

**Se não existe, oferecer duas opções:**
1. **Auto-draft a partir do codebase** (recomendado): Estudar repo, README,
   landing pages, copy, package.json e gerar um V1
2. **Começar do zero**: Percorrer cada seção conversacionalmente

### Passo 2: Coletar informações

**Se auto-drafting:**
1. Ler: README, landing pages, marketing copy, about pages, meta descriptions,
   package.json, project-context.md
2. Gerar draft de todas as seções
3. Apresentar e perguntar o que precisa corrigir
4. Iterar até satisfação do usuário

**Se do zero:**
Percorrer uma seção por vez. Não despejar todas as perguntas de uma vez.
Insistir em linguagem real do cliente — frases exatas valem mais que
descrições polidas.

---

## Seções a Capturar

### 1. Visão do Produto
- Descrição em uma frase
- O que faz (2-3 frases)
- Categoria de produto (em que "prateleira" o cliente te procura)
- Tipo (SaaS, marketplace, e-commerce, serviço, etc.)
- Modelo de negócio e precificação

### 2. Audiência-Alvo
- Tipo de empresa (indústria, tamanho, estágio)
- Decisores-alvo (cargos, departamentos)
- Caso de uso principal
- Jobs to be done (2-3 coisas para as quais o cliente te "contrata")
- Cenários específicos de uso

### 3. Personas (B2B)
Para cada stakeholder no processo de compra:
- Usuário, Campeão, Decisor, Comprador Financeiro, Influenciador Técnico
- O que cada um valoriza, seu desafio, e a promessa de valor

### 4. Problemas & Dores
- Desafio central antes de encontrar sua solução
- Por que soluções atuais falham
- Custo da inação (tempo, dinheiro, oportunidades)
- Tensão emocional (estresse, medo, dúvida)

### 5. Diferenciação
- Alternativas diretas (concorrentes) e indiretas (planilhas, manual, etc.)
- O que te torna diferente (não "melhor" — diferente)
- Posicionamento em uma frase: "[Produto] é o único [categoria] que [diferencial]"

### 6. Prova Social
- Métricas (usuários, receita, crescimento, tempo economizado)
- Clientes ou logos notáveis
- Resultados documentados
- Avaliações e ratings

### 7. Voz & Tom
- Como a marca soa (formal/informal, técnico/acessível)
- Palavras e frases que a marca USA
- Palavras e frases que a marca EVITA
- Referências de tom (ex: "como um colega técnico explicando")

### 8. Estratégia de Canais
- Canais atuais de aquisição (orgânico, pago, email, social, parcerias)
- Canal mais eficaz
- Canais planejados ou em teste

---

## Formato de Saída

Gerar `.osforge/marketing-context.md` com este template:

```markdown
# Marketing Context — [Nome do Produto]

> Gerado em [data]. Fonte de verdade para todos os workflows de marketing.
> Stack e features: ver project-context.md

## Produto
[conteúdo da seção 1]

## Audiência
[conteúdo da seção 2]

## Personas
[conteúdo da seção 3 — omitir se B2C]

## Problemas & Dores
[conteúdo da seção 4]

## Diferenciação
[conteúdo da seção 5]

## Prova Social
[conteúdo da seção 6]

## Voz & Tom
[conteúdo da seção 7]

## Canais
[conteúdo da seção 8]
```

---

## Skills Relacionados

- **Após criar contexto:** usar `copywriting` para escrever copy, `page-cro` para otimizar páginas
- **Para SEO:** `seo-audit` e `content-strategy` usam audiência e posicionamento daqui
- **Para vendas:** `sales-enablement` e `cold-email` usam dores e diferenciação daqui
- **Para ads:** `paid-ads` e `ad-creative` usam voz, audiência e prova social daqui
