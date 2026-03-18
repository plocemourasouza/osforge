---
name: doc-shard
description: >
  Divide documentos markdown grandes em arquivos menores organizados
  com index. Use quando documento exceder context window ou para
  organizar docs extensos. Use com "shard doc", "dividir documento".
trigger: shard|split doc|dividir doc|quebrar documento
model-tier: haiku
---

# Document Sharder

## Objetivo
Dividir documentos markdown grandes em arquivos menores, organizados
e com index, para consumo eficiente por LLMs e outros skills.

## Inputs
- **source_path** — Caminho do documento markdown a dividir
- **split_level** (default: 2) — Nível de heading para split (## = level 2)
- **output_dir** (opcional) — Diretório de saída. Default: `{source_name}-sharded/`

## Processo

### 1. Analisar Documento
- Ler documento fonte completamente
- Identificar todos os headings do nível especificado
- Mapear seções e tamanhos aproximados em tokens
- Preservar frontmatter original

### 2. Gerar Shards
Para cada seção no nível especificado:
- Criar arquivo: `{NN}-{slug-do-heading}.md`
- Incluir header de contexto: `<!-- Parte N de M — {heading original} -->`
- Incluir conteúdo da seção com sub-headings preservados
- Se seção individual > ~3000 tokens, subdividir no próximo nível de heading

### 3. Gerar Index
Criar `_index.md`:

```markdown
---
type: osforge-shard-index
source: "{path do documento original}"
shards: {N}
created: "{data}"
total_tokens_estimate: {N}
---

# Index: {título do documento original}

## Sobre
- {1-2 bullets descrevendo o documento original}

## Seções
| # | Arquivo | Tópico | ~Tokens |
|---|---------|--------|---------|
| 1 | `01-{slug}.md` | {descrição 1 linha} | ~{N} |
| 2 | `02-{slug}.md` | {descrição 1 linha} | ~{N} |
...

## Cross-Cutting
- {itens que apareceram em múltiplas seções}
```

### 4. Report
"Documento dividido em {N} shards + index.
Carregar _index.md (~{X} tokens) vs documento completo (~{Y} tokens)
= {ratio}x mais eficiente para discovery inicial."

## Regras
- Nunca perder conteúdo no split — todo texto do original deve aparecer em algum shard
- Manter referências internas entre seções quando existirem
- Frontmatter do original vai para o _index.md, não para os shards
- Shards devem ser autocontidos — compreensíveis sem ler os outros
