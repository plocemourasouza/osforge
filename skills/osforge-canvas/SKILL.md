---
name: osforge-canvas
description: >
  UI generativa local para revisão interativa de planos, specs e breakdowns no
  browser, com feedback estruturado nativo. ACIONE quando: usuário pede "abre no
  canvas", "mostra no browser", "quero revisar interativamente", "preciso aprovar
  antes de implementar", "canvas", ou ao atingir checkpoints de aprovação em
  triage STANDARD/COMPLEX (planos, specs, breakdowns que precisam de aprovação
  por seção, edição iterativa, input de formulário, ou revisão item a item).
  Keywords: canvas, revisão interativa, aprovar plano, feedback estruturado,
  checkpoint, approve, review interativo, open canvas. Não acione para: respostas
  rápidas em texto que não requerem round-trip; documento apresentável one-shot
  sem coleta de feedback → usar visual-planner.
version: 1.0.0
metadata:
  category: "planning"
  position: "interactive-review-layer"
allowed-tools: Read, Write, Bash
---

# OSForge Canvas

Generative UI local estilo Thesys C1. Claude emite um artefato JSON estruturado,
o servidor Bun renderiza a UI interativa no browser, e o feedback retorna por arquivo
para o próximo turno do Claude.

## Decision table

| Situação | Ferramenta |
|---|---|
| Resposta rápida / status / pergunta | texto no terminal |
| Plano / spec que precisa aprovação, edição por seção, formulário ou revisão item a item | **CANVAS** |
| Documento apresentável standalone sem round-trip de feedback | `visual-planner` HTML |

## Workflow operacional

### 1. Health-check do servidor

```bash
curl -sf http://localhost:4242/api/health
```

Se retornar erro (conexão recusada ou status não-2xx): iniciar o servidor em background
**a partir do diretório do projeto atual** — o `DATA_DIR` padrão é `<cwd>/outputs/canvas/`.

```bash
# Substitua <osforge-repo> pelo caminho absoluto do repositório OSForge
bun <osforge-repo>/scripts/canvas/server.ts &
```

Porta padrão: `4242`. Override via `CANVAS_PORT=<porta>` antes do comando.
Re-checar health após iniciar.

### 2. Escrever o artefato

Gravar `outputs/canvas/artifacts/<slug>.json` seguindo o schema em
`skills/osforge-canvas/references/schema.md`.

Regras rápidas:
- `$schema`: `"osforge-canvas/v1"` (literal)
- `id`: kebab-case único — mesmo valor que o nome do arquivo sem `.json`
- `revision`: começa em `1`, incrementa a cada sobrescrita
- `createdAt`: ISO 8601, não alterar em revisões
- `blocks`: array de até 8 tipos (`heading`, `markdown`, `cards`, `table`,
  `checklist`, `form`, `decision`, `mermaid`) — todos com `id` único em kebab-case
- `accent`: escolher conforme domínio (ver tabela na seção "Accent color")

**Pseudo-streaming:** para artefatos longos, escrever o arquivo cedo com blocks
iniciais e sobrescrever conforme completa. O viewer detecta mudanças via SSE e
recarrega sem refresh manual.

### 3. Apresentar ao usuário

Imprimir a URL e pedir revisão:

```
Artefato pronto. Abra para revisar:
http://localhost:4242/?a=<slug>

Quando terminar, submeta o feedback no browser — lerei na sequência.
```

### 4. Próximo turno — ler feedback antes de continuar

**Toda vez que o usuário enviar qualquer mensagem após um artefato ativo**, ler
`outputs/canvas/feedback/<slug>.json` antes de qualquer outra ação.

Verificações obrigatórias:
- Arquivo existe? Se não: feedback ainda não submetido — avisar o usuário.
- `feedback.revision === artifact.revision`? Se menor: feedback é stale (usuário
  revisou versão anterior) — avisar e reconciliar antes de agir.
- Agir sobre `responses` por block: `checklist` → itens marcados; `form` → valores
  preenchidos; `decision` → ação (`approve` / `edit` / `reject`) + comentário.

**Revisões solicitadas:** sobrescrever o mesmo arquivo `artifacts/<slug>.json`
incrementando `revision`. O viewer recarrega via SSE automaticamente.

## Accent color

| Domínio | Accent | Hex |
|---|---|---|
| Engenharia geral, produto | `vermillion` (default) | `#D94F30` |
| Dados, infra, backend | `teal` | `#2A7B9B` |
| Consumer, UX, front-end | `coral` | `#E06B56` |
| DevTools, CLI, OSS | `forest` | `#2D8B55` |
| Fintech, analytics, BI | `amber` | `#D4A843` |

## Referência do schema

`skills/osforge-canvas/references/schema.md` — fonte da verdade para todos os
tipos de block, campos obrigatórios, formato do feedback, e regras de IDs.

## Backlog v2 (deferido)

- Charts interativos (block tipo `chart`)
- Streaming block-level via SSE (enviar blocks à medida que são gerados)
- Hook `UserPromptSubmit` para injetar feedback automaticamente no contexto
- Binário compilado standalone para deploy sem Bun instalado
