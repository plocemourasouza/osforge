---
name: context-distillator
description: >
  Compressão lossless de documentos para consumo otimizado por LLMs.
  Preserva 100% da informação factual eliminando overhead textual.
  Não é sumarização (lossy) — é compressão lossless.
  Use com "distill", "comprimir docs", "compress context".
trigger: distill|comprimir|compress context|distilat
model-tier: sonnet
---

# Context Distillator

## Objetivo
Produzir documentos hiper-comprimidos (distillates) a partir de fontes,
preservando cada fato, decisão, constraint e relacionamento, eliminando
overhead que humanos precisam e LLMs não.

## Inputs
- **source_paths** (obrigatório) — Caminhos de arquivos/diretórios para distillar
- **downstream_consumer** (opcional) — Skill que vai consumir ("implementação", "arquitetura", "review")
- **output_path** (opcional) — Onde salvar. Default: `{source}-distillate.md`

## Processo

### 1. Análise de Fontes
- Ler todos os arquivos fonte completamente
- Classificar tipo: PRD, architecture, spec, code, config, docs
- Estimar tamanho total em tokens

### 2. Extração de Entidades
Extrair TODA informação discreta:
- Fatos e dados (números, datas, versões, percentuais)
- Decisões tomadas + rationale
- Alternativas rejeitadas + motivo
- Requisitos e constraints (explícitos e implícitos)
- Dependências e relacionamentos entre entidades
- Named entities (produtos, tecnologias, pessoas)
- Questões em aberto e itens não resolvidos
- Limites de escopo (in/out/deferred)
- Critérios de sucesso e validação
- Riscos com severidade

### 3. Deduplicação
Aplicar regras de `./compression-rules.md`:
- Mesmo fato em múltiplos docs → manter versão com mais contexto
- Mesmo conceito em diferentes níveis de detalhe → manter o detalhado
- Listas sobrepostas → merge sem duplicatas
- Docs discordantes → notar conflito: "Doc A diz X; Doc B diz Y — não resolvido"

### 4. Filtragem (se downstream_consumer informado)
Para cada item: "O skill downstream precisa disso?"
- Eliminar itens claramente irrelevantes
- Na dúvida, MANTER — errar para preservação
- NUNCA eliminar: decisões, alternativas rejeitadas, questões abertas, constraints

### 5. Agrupamento Temático
Organizar em temas derivados do conteúdo (não template fixo).
Temas comuns: core/problema, solução/approach, stack/decisões técnicas,
escopo, critérios de sucesso, riscos, questões abertas.

### 6. Compressão de Linguagem
Aplicar `./compression-rules.md` item por item:
- Eliminar transições, hedging, retórica, auto-referência
- Preservar números, nomes, versões, decisões
- Cada bullet autocontido e compreensível isoladamente
- Relacionamentos explícitos: "X porque Y", "X bloqueia Y"

### 7. Formato de Saída

```yaml
---
type: osforge-distillate
sources:
  - "{caminho relativo fonte 1}"
  - "{caminho relativo fonte 2}"
downstream_consumer: "{consumer ou 'general'}"
created: "{data}"
token_estimate: {contagem aprox}
compression_ratio: "{X:1}"
---
```

Corpo: bullets densos agrupados por `##` temáticos.
Sem prosa, sem parágrafos — apenas bullets.
Sem formatação decorativa. Semicolons para itens curtos relacionados.

### 8. Splitting (se distillate > ~5000 tokens)
Criar diretório `{base}-distillate/`:
- `_index.md` — Orientação + manifest + itens cross-cutting
- `01-{topic}.md` — Seção autocontida com header "Parte N de M"
- `02-{topic}.md`

### 9. Report
Informar: "Comprimido {N} fontes ({X} tokens) → distillate ({Y} tokens).
Ratio: {X/Y}:1. Salvo em {path}."
