---
name: osforge-canvas
description: >
  UI generativa local para revisão interativa de planos, specs e breakdowns no
  browser, com feedback estruturado nativo. CANAL DEFAULT para apresentação de
  qualquer spec ou plano: o servidor é iniciado automaticamente por SessionStart
  hook — não espere o usuário pedir. ACIONE quando: for apresentar um plano, spec
  ou breakdown (default), checkpoints de aprovação em triage STANDARD/COMPLEX,
  ou usuário pede "abre no canvas", "mostra no browser", "quero revisar
  interativamente", "preciso aprovar antes de implementar", "canvas".
  Keywords: canvas, revisão interativa, aprovar plano, spec, feedback estruturado,
  checkpoint, approve, review interativo, open canvas. Não acione para: respostas
  rápidas em texto que não requerem round-trip; documento apresentável one-shot
  sem coleta de feedback → usar visual-planner; usuário pediu explicitamente
  "só texto" / "no terminal".
version: 1.1.0
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
| **Qualquer apresentação de plano, spec ou breakdown** (default — não precisa de pedido) | **CANVAS** |
| Documento apresentável standalone sem round-trip de feedback (pedido explícito) | `visual-planner` HTML |
| Usuário pediu "só texto" / "no terminal" | texto no terminal |

Ao emitir no canvas, incluir também um resumo curto (5-10 linhas) no terminal —
o canvas é o documento completo, o terminal é o TL;DR.

## Workflow operacional

### 1. Health-check do servidor (normalmente já está rodando)

O servidor é iniciado automaticamente pelo SessionStart hook
(`hooks/canvas-autostart.sh`) com data dir **global** `~/.osforge/canvas/`.
Confirme e capture o data dir real:

```bash
curl -sf http://localhost:4242/api/health
# → {"ok":true,...,"dir":"<DATA_DIR>"}  ← use SEMPRE este dir para artifacts/feedback
```

Se retornar erro (hook não rodou / bun ausente): iniciar manualmente em background:

```bash
bun ~/.claude/canvas/server.ts --dir="$HOME/.osforge/canvas" &
# fallback se não deployado: bun <osforge-repo>/scripts/canvas/server.ts --dir="$HOME/.osforge/canvas" &
```

Porta padrão: `4242`. Override via `CANVAS_PORT=<porta>` antes do comando.
Re-checar health após iniciar.

### 2. Escrever o artefato

Gravar `<DATA_DIR>/artifacts/<slug>.json` (DATA_DIR vem do health — global por
default) seguindo o schema em `skills/osforge-canvas/references/schema.md`.

Regras rápidas:
- `$schema`: `"osforge-canvas/v1"` (literal)
- `id`: kebab-case único — mesmo valor que o nome do arquivo sem `.json`.
  **Prefixar com o slug do projeto** (ex.: `meuapp-auth-refactor-plan`) — o
  data dir é compartilhado entre todos os projetos da máquina
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
`<DATA_DIR>/feedback/<slug>.json` antes de qualquer outra ação.

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
