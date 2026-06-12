# Heurística de Clusterização de Triggers

Este módulo explica o algoritmo de normalização e agrupamento usado pelo
`osforge-db evolve`. Sem NLP, sem embeddings — só Python stdlib.

---

## Problema

Observações sobre o mesmo tema chegam com fraseamentos diferentes:

```
"when writing tests prefer TDD"
"when writing tests use red-green cycle"
"when tests fail check production code first"
```

Objetivo: reconhecer que todas giram em torno de "tests" e agrupá-las.

---

## Algoritmo em 3 Passos

### Passo 1 — Normalização

```python
_STRIP_VERBS = frozenset([
    "when", "creating", "writing", "adding", "implementing", "testing",
    "building", "running", "using", "making", "working", "editing",
    "reading", "fixing", "updating", "setting", "getting",
])

def _normalize_trigger(text):
    words = text.lower().split()
    filtered = [w for w in words if w not in _STRIP_VERBS]
    return " ".join(filtered).strip() or text.lower().strip()
```

Remove articuladores verbais de alta frequência, mantendo o substantivo-sujeito.

Exemplos:
```
"when writing tests prefer TDD"     → "tests prefer tdd"
"when adding components run shadcn" → "components run shadcn"
"when deploying check lint passes"  → "deploying check lint passes"
```

### Passo 2 — Extração da Chave de Cluster

```python
normalized = _normalize_trigger(row["trigger_text"])
words = normalized.split()
key = words[0] if words else normalized  # substantivo-sujeito = 1ª palavra restante
```

Apenas a **primeira palavra** do resultado normalizado vira a chave de cluster.

Isso garante que frases sobre o mesmo sujeito se agrupem apesar de predicados diferentes:

```
"tests prefer tdd"      → key: "tests"
"tests use red-green"   → key: "tests"   ✓ mesmo cluster
"components run shadcn" → key: "components"
"components check registry" → key: "components"  ✓ mesmo cluster
```

### Passo 3 — Filtragem e Classificação

```python
candidates = {k: v for k, v in clusters.items() if len(v) >= min_count}
```

Só clusters com `len ≥ min_count` (default 2) viram candidatos.

Confiança estimada pela quantidade de observações:
```python
confidence = 0.5 + min(0.3, len(obs) * 0.05)
```

| Observações | Confiança |
|-------------|-----------|
| 1 | 0.55 |
| 2 | 0.60 |
| 4 | 0.70 |
| 6 | 0.80 |
| 8+ | 0.80 (teto) |

Classificação do candidato:
```python
def _classify_candidate(cluster_size, avg_conf):
    if cluster_size >= 3 and avg_conf >= 0.75:
        return "AGENT"
    if avg_conf >= 0.70:
        return "COMMAND"
    return "SKILL"
```

---

## Limitações Conhecidas

**Falsos positivos por substantivo genérico:**
- "tests", "files", "data" são muito comuns → podem agregar padrões não relacionados
- Mitigação: filtre por `--project=<slug>` para manter contexto coeso

**Triggers curtos colidem:**
- "run tests" e "run lint" → key "run" (ambíguo)
- Mitigação: escreva triggers com sujeito específico ("when tests fail..." não "run tests")

**Sem semântica:**
- "when writing tests" e "when running benchmarks" ficam em clusters diferentes
- Isso é intencional: a heurística prioriza precisão sobre recall

---

## Estratégias de Escrita de Triggers

Para maximizar qualidade dos clusters:

| ✅ Bom | ❌ Evitar |
|--------|----------|
| "when writing tests prefer TDD" | "TDD" |
| "when adding components use shadcn" | "shadcn install" |
| "when schema changes run migration" | "migrate" |
| "when auth fails check RLS policies" | "RLS bug" |

Padrão recomendado: **"when [contexto] [ação-específica]"**

---

## Exemplo Completo

```bash
# Capturar observações ao longo da sessão
osforge-db add-observation meu-proj "when writing tests prefer TDD"
osforge-db add-observation meu-proj "when writing tests check edge cases first"
osforge-db add-observation meu-proj "when adding shadcn components run npx shadcn add"
osforge-db add-observation meu-proj "when adding shadcn components check registry"
osforge-db add-observation meu-proj "when auth fails verify RLS policies in Supabase"

# Analisar
osforge-db evolve --project=meu-proj
```

Saída esperada:
```
EVOLVE ANALYSIS — 5 observation(s), projeto=meu-proj
Clusters ≥ 2: 2

## SKILL CANDIDATES (2)
1. Cluster: "tests"      | 2 obs | conf 60%
2. Cluster: "shadcn"     | 2 obs | conf 60%
```

"auth" fica fora (cluster_size = 1 < min_count).
