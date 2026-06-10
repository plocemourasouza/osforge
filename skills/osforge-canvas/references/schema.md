---
name: osforge-canvas-schema
description: Schema v1 do OSForge Canvas — formato de artefatos JSON que Claude escreve em outputs/canvas/artifacts/.
---

# OSForge Canvas — Schema v1

## Visão Geral do Fluxo

```
Claude
  │  escreve (ou sobrescreve) artefato JSON
  ▼
outputs/canvas/artifacts/<id>.json
  │  SSE notifica mudança
  ▼
scripts/canvas/server.ts (Bun)
  │  serve o viewer via HTTP
  ▼
Browser (viewer)
  │  usuário interage com blocks interativos
  │  (checklist, form, decision)
  ▼
outputs/canvas/feedback/<artifact-id>.json
  │  Claude lê feedback
  ▼
Claude (próxima iteração)
```

**Pseudo-streaming via revision:** Claude escreve o arquivo cedo com blocks parciais e vai sobrescrevendo (`revision` incrementado a cada write). O viewer detecta mudanças via SSE e recarrega sem refresh manual.

---

## Envelope

```json
{
  "$schema": "osforge-canvas/v1",
  "id": "kebab-case-slug",
  "title": "Título legível do artefato",
  "accent": "vermillion",
  "createdAt": "2026-06-10T14:30:00Z",
  "revision": 1,
  "blocks": []
}
```

| Campo | Tipo | Regra |
|-------|------|-------|
| `$schema` | `"osforge-canvas/v1"` | Literal fixo, identifica versão |
| `id` | string (kebab-case) | Slug único, também parte do nome do arquivo |
| `title` | string | Exibido no header do viewer |
| `accent` | enum | Cor temática; ver paleta abaixo |
| `createdAt` | ISO 8601 | Timestamp do primeiro write; não altera em revisões |
| `revision` | integer ≥ 1 | Claude incrementa a cada sobrescrita; viewer usa para detectar mudança |
| `blocks` | array | Sequência de blocks; pode estar incompleta em revisões intermediárias |

### Paleta de Accent (herdada do visual-planner)

| Valor | Hex | Uso típico |
|-------|-----|------------|
| `vermillion` | `#D94F30` | Default — engenharia geral, produto |
| `teal` | `#2A7B9B` | Dados, infra, backend |
| `coral` | `#E06B56` | Consumer, UX, front-end |
| `forest` | `#2D8B55` | DevTools, CLI, OSS |
| `amber` | `#D4A843` | Fintech, analytics, BI |

---

## Blocks

Todo block **deve** ter `id` único (kebab-case) dentro do artefato. O `id` é a chave de endereçamento no arquivo de feedback.

### 1. `heading`

Seção ou sub-seção dentro do artefato.

```json
{
  "type": "heading",
  "id": "fase-1",
  "level": 2,
  "text": "Fase 1 — Preparação"
}
```

| Campo | Tipo | Valores |
|-------|------|---------|
| `level` | integer | `2` (seção principal) ou `3` (sub-seção) |
| `text` | string | Texto do heading |

---

### 2. `markdown`

Bloco de texto livre em Markdown. Suporta listas, negrito, itálico, código inline, links.

```json
{
  "type": "markdown",
  "id": "contexto-geral",
  "md": "O objetivo é **migrar sessões legadas** para JWT + refresh token, mantendo compatibilidade com clientes v1."
}
```

| Campo | Tipo | Valores |
|-------|------|---------|
| `md` | string | Fonte Markdown (GFM) |

---

### 3. `cards`

Grade de cards com título, badge opcional e corpo Markdown.

```json
{
  "type": "cards",
  "id": "beneficios",
  "columns": 3,
  "items": [
    { "title": "Stateless", "badge": "JWT", "md": "Elimina lookups de sessão no DB a cada request." },
    { "title": "Refresh Token", "badge": "Segurança", "md": "Rotação automática; revogação granular por usuário." },
    { "title": "Multi-device", "md": "Cada device recebe seu próprio refresh token." }
  ]
}
```

| Campo | Tipo | Valores |
|-------|------|---------|
| `columns` | integer | `2`, `3` ou `4` |
| `items[].title` | string | Título do card |
| `items[].badge` | string? | Label colorido no canto superior direito (opcional) |
| `items[].md` | string | Corpo em Markdown |

---

### 4. `table`

Tabela estruturada com cabeçalho e linhas.

```json
{
  "type": "table",
  "id": "endpoints-auth",
  "columns": ["Endpoint", "Método", "Mudança", "Breaking?"],
  "rows": [
    ["/auth/login", "POST", "Retorna access + refresh token", "Não"],
    ["/auth/refresh", "POST", "Novo endpoint", "Não"],
    ["/auth/logout", "POST", "Revoga refresh token", "Não"],
    ["/auth/session", "GET", "Removido", "**Sim**"]
  ]
}
```

| Campo | Tipo | Valores |
|-------|------|---------|
| `columns` | string[] | Nomes das colunas |
| `rows` | string[][] | Cada linha é um array de células; suporta Markdown inline |

---

### 5. `checklist`

Lista de verificação interativa. O usuário pode marcar/desmarcar itens; o estado é salvo no feedback.

```json
{
  "type": "checklist",
  "id": "criterios-aceite",
  "title": "Critérios de Aceite",
  "items": [
    { "id": "testes-unitarios", "text": "Cobertura ≥ 80% nos módulos de auth", "checked": false },
    { "id": "zero-downtime", "text": "Deploy sem interrupção (blue-green)", "checked": false },
    { "id": "docs-atualizados", "text": "OpenAPI atualizado com novos endpoints", "checked": false }
  ]
}
```

| Campo | Tipo | Valores |
|-------|------|---------|
| `title` | string? | Título opcional acima da lista |
| `items[].id` | string | kebab-case; chave no feedback |
| `items[].text` | string | Texto do item |
| `items[].checked` | boolean | Estado inicial |

---

### 6. `form`

Formulário interativo com campos de texto, textarea, select e checkbox. Permite coletar input estruturado do usuário.

```json
{
  "type": "form",
  "id": "parametros-rollout",
  "submitLabel": "Confirmar estratégia",
  "fields": [
    {
      "id": "estrategia",
      "label": "Estratégia de rollout",
      "kind": "select",
      "options": ["big-bang", "canary", "shadow"],
      "value": "canary"
    },
    {
      "id": "observacoes",
      "label": "Observações adicionais",
      "kind": "textarea",
      "value": ""
    }
  ]
}
```

| Campo | Tipo | Valores |
|-------|------|---------|
| `submitLabel` | string? | Texto do botão de submit (default: "Enviar") |
| `fields[].id` | string | kebab-case; chave no feedback |
| `fields[].label` | string | Label exibido acima do campo |
| `fields[].kind` | enum | `"text"`, `"textarea"`, `"select"`, `"checkbox"` |
| `fields[].options` | string[]? | Obrigatório quando `kind = "select"` |
| `fields[].value` | any? | Valor inicial |

---

### 7. `decision`

Block de decisão explícita. Exige que o usuário aprove, edite ou rejeite antes de continuar.

```json
{
  "type": "decision",
  "id": "aprovacao-arquitetura",
  "prompt": "A arquitetura JWT + refresh token está alinhada com os requisitos de segurança?",
  "options": ["approve", "edit", "reject"],
  "commentRequiredFor": ["edit", "reject"]
}
```

| Campo | Tipo | Valores |
|-------|------|---------|
| `prompt` | string | Pergunta ou afirmação para o usuário decidir |
| `options` | enum[] | Subconjunto de `["approve", "edit", "reject"]` — pelo menos um |
| `commentRequiredFor` | enum[] | Opções que exigem comentário obrigatório no feedback |

---

### 8. `mermaid`

Diagrama renderizado como Mermaid.js.

```json
{
  "type": "mermaid",
  "id": "fluxo-dependencias",
  "kind": "graph",
  "code": "graph LR\n  Schema-->Endpoints\n  Endpoints-->Cutover"
}
```

| Campo | Tipo | Valores |
|-------|------|---------|
| `kind` | enum | `"graph"` (flowchart/grafo) ou `"gantt"` |
| `code` | string | Fonte Mermaid válida; newlines como `\n` no JSON |

---

## Arquivo de Feedback

Gerado pelo viewer em `outputs/canvas/feedback/<artifact-id>.json` quando o usuário submete qualquer block interativo.

```json
{
  "artifactId": "auth-refactor-plan",
  "revision": 1,
  "submittedAt": "2026-06-10T15:00:00Z",
  "responses": {
    "criterios-aceite": {
      "type": "checklist",
      "checked": ["testes-unitarios", "zero-downtime"]
    },
    "parametros-rollout": {
      "type": "form",
      "values": {
        "estrategia": "canary",
        "observacoes": "Iniciar com 5% do tráfego, monitorar por 24h."
      }
    },
    "aprovacao-arquitetura": {
      "type": "decision",
      "action": "edit",
      "comment": "Adicionar rotação automática de refresh token após cada uso."
    }
  },
  "comment": "No geral aprovado; ajustar conforme comentários acima."
}
```

| Campo | Tipo | Regra |
|-------|------|-------|
| `artifactId` | string | Mesmo `id` do envelope do artefato |
| `revision` | integer | Revisão do artefato que o usuário visualizou; Claude usa para detectar feedback stale |
| `submittedAt` | ISO 8601 | Timestamp do submit |
| `responses` | object | Chaves = `blockId`; valor depende do tipo (ver abaixo) |
| `comment` | string? | Comentário geral opcional do usuário |

### Formatos por tipo em `responses`

| Tipo | Campos |
|------|--------|
| `checklist` | `{ type: "checklist", checked: string[] }` — array de `itemId` marcados |
| `form` | `{ type: "form", values: { [fieldId]: string } }` |
| `decision` | `{ type: "decision", action: "approve"\|"edit"\|"reject", comment?: string }` |

---

## Regras

1. **IDs únicos:** Todo `id` de block e `id` de item (em checklist e form) deve ser único dentro do artefato. Use kebab-case descritivo.
2. **Revision incremental:** Claude sempre sobrescreve o MESMO arquivo com `revision + 1`. Nunca cria arquivo novo para atualização.
3. **Pseudo-streaming:** É permitido escrever o arquivo com `blocks` incompletos nas revisões intermediárias. O viewer recarrega via SSE a cada write.
4. **createdAt imutável:** O campo `createdAt` reflete o primeiro write e não é alterado em revisões subsequentes.
5. **Feedback stale:** Se `feedback.revision < artifact.revision`, Claude deve indicar que o feedback é referente a uma revisão anterior.
6. **accent padrão:** Omitir `accent` equivale a `"vermillion"`. Sempre inclua explicitamente para artefatos temáticos.

---

## Exemplo Integral

Artefato mínimo válido com 3 tipos de block:

```json
{
  "$schema": "osforge-canvas/v1",
  "id": "sprint-planning",
  "title": "Sprint Planning — Semana 24",
  "accent": "forest",
  "createdAt": "2026-06-10T09:00:00Z",
  "revision": 1,
  "blocks": [
    {
      "type": "heading",
      "id": "objetivo",
      "level": 2,
      "text": "Objetivo da Sprint"
    },
    {
      "type": "markdown",
      "id": "contexto",
      "md": "Entregar a **feature de notificações** em produção com cobertura de testes ≥ 85%."
    },
    {
      "type": "checklist",
      "id": "entregaveis",
      "title": "Entregáveis",
      "items": [
        { "id": "api-notif", "text": "API de notificações (REST)", "checked": false },
        { "id": "ui-notif", "text": "UI — painel de notificações", "checked": false },
        { "id": "testes", "text": "Testes de integração E2E", "checked": false }
      ]
    },
    {
      "type": "decision",
      "id": "go-nogo",
      "prompt": "A sprint está pronta para iniciar?",
      "options": ["approve", "edit", "reject"],
      "commentRequiredFor": ["edit", "reject"]
    }
  ]
}
```
