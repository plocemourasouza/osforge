---
name: osforge-evolve
description: |
  ACIONE quando: evolve, /evolve, osforge evolve, analisar observações, propor skills, clustering de padrões, instinct, promover instinct, aprendizado contínuo, fechar o loop de aprendizado, capturar padrões de sessão, add-observation, list-instincts, promote-instinct, evolução de configuração
---

# OSForge Evolve — Arquitetura Instinct

Fecha o loop de aprendizado no OSForge: captura eventos de sessão como `observations`
no banco SQLite, clusteriza por normalização de trigger, e propõe diffs concretos em
`skills/` ou `rules/` para aprovação humana.

**Princípios:** sem daemon, sem LLM no clustering, stdlib puro, human-in-loop.

---

## Fluxo Completo

```
sessão de trabalho
      │
      ▼
  add-observation            (manual ou via hook observe-capture.py)
      │
      ▼ (on-demand)
  osforge-db evolve          (clusteriza + propõe diffs)
      │
      ▼ (humano revisa)
  editar skills/ ou rules/   (curadoria manual)
      │
      ▼ (confiança ≥ 0.8)
  promote-instinct           (eleva scope project → global)
      │
      ▼
  ./deploy.sh                (propaga para ~/.claude/ e ~/.cursor/)
```

---

## Subcomandos

### `osforge-db add-observation <project> <trigger_text> [--context=<ctx>] [--tool=<tool>]`

Grava uma observação de sessão para posterior clusterização.

```bash
osforge-db add-observation meu-proj "when writing tests prefer TDD" \
  --context="ficou mais fácil com red-green" --tool=Bash
```

- `project` — slug do projeto (ex.: `osforge`, `api-prod`)
- `trigger_text` — frase descritiva do padrão observado (ex.: "when adding components run shadcn install")
- `--context` — contexto ou justificativa livre
- `--tool` — ferramenta que gerou a observação (ex.: `Bash`, `Edit`, `Write`)

### `osforge-db evolve [--project=<slug>] [--min-count=2]`

Clusteriza observations por normalização de trigger e propõe candidates.

```bash
osforge-db evolve --project=meu-proj
osforge-db evolve --min-count=3   # cluster mais apertado
```

**Saída:** diff unificado sugerido por cluster, classificado como SKILL / COMMAND / AGENT.

Regras de classificação:
| Critério | Tipo |
|----------|------|
| cluster ≥ 3 E conf ≥ 0.75 | AGENT |
| conf ≥ 0.70 | COMMAND |
| default | SKILL |

O humano revisa o diff, edita o arquivo real em `skills/` ou `rules/`, e só então commita.

### `osforge-db list-instincts [--project=<slug>] [--scope=project|global]`

Lista instincts registrados, com filtros opcionais.

```bash
osforge-db list-instincts
osforge-db list-instincts --scope=global
osforge-db list-instincts --project=osforge
```

### `osforge-db promote-instinct <instinct_id> [--scope=global]`

Eleva o scope de um instinct de `project` para `global` (requer confidence ≥ 0.8).

```bash
osforge-db promote-instinct 3
```

Instincts `global` são candidatos a entrar em `claude-code/SKILLS.md` ou `rules/` via
curadoria humana e `./deploy.sh`.

---

## Esquema de Dados

### Tabela `observations`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER PK | autoincrement |
| `project` | TEXT | slug do projeto (default `''` = global) |
| `trigger_text` | TEXT | frase do padrão (ex.: "when writing tests prefer TDD") |
| `context` | TEXT | contexto livre |
| `tool` | TEXT | ferramenta geradora |
| `created_at` | TEXT | UTC ISO8601 |

### Tabela `instincts`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER PK | autoincrement |
| `trigger` | TEXT | trigger canônico normalizado |
| `guidance` | TEXT | orientação concreta |
| `confidence` | REAL 0–1 | confiança estimada |
| `domain` | TEXT | domínio temático |
| `scope` | TEXT | `project` ou `global` |
| `project` | TEXT | slug do projeto de origem |
| `seen_count` | INTEGER | número de observações que geraram o instinct |
| `created_at` / `updated_at` | TEXT | UTC ISO8601 |

---

## Integração com Hook (observe-capture.py)

O arquivo `hooks/observe-capture.py` é um hook `PostToolUse` leve que grava observações
automaticamente. Para ativá-lo, adicione ao `hooks-claude-code.json`:

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write|Bash",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ~/.claude/hooks/observe-capture.py"
        }
      ]
    }
  ]
}
```

**Importante:** o hook é silencioso por design (exit 0 sempre) e não bloqueia o fluxo
principal mesmo em falha de gravação.

---

## Boas Práticas

- Capture observations no fim de sessões produtivas, não em tempo real
- Prefira triggers descritivos: "when X do Y" em vez de tags genéricas
- Use `--min-count=3` para projetos grandes com muitas observações
- Revise o diff sugerido pelo `evolve` — é um ponto de partida, não receita pronta
- Só promova instincts para `global` após validação em múltiplos projetos
- Não edite a tabela `instincts` diretamente; use os subcomandos

---

## Referências

- `skills/evolve/references/clustering.md` — heurística de normalização detalhada
- `scripts/osforge-db.py` — implementação completa (stdlib Python, zero deps)
- `docs/DECISIONS.md` ADR-001 — fluxo de deploy obrigatório via `./deploy.sh`
