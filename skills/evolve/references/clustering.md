# Trigger Clustering Heuristic

This module explains the normalization and grouping algorithm used by
`osforge-db evolve`. No NLP, no embeddings — just Python stdlib.

---

## Problem

Observations about the same topic arrive with different phrasings:

```
"when writing tests prefer TDD"
"when writing tests use red-green cycle"
"when tests fail check production code first"
```

Goal: recognize that they all revolve around "tests" and group them.

---

## 3-Step Algorithm

### Step 1 — Normalization

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

Removes high-frequency verbal connectors, keeping the subject noun.

Examples:
```
"when writing tests prefer TDD"     → "tests prefer tdd"
"when adding components run shadcn" → "components run shadcn"
"when deploying check lint passes"  → "deploying check lint passes"
```

### Step 2 — Cluster Key Extraction

```python
normalized = _normalize_trigger(row["trigger_text"])
words = normalized.split()
key = words[0] if words else normalized  # subject noun = 1st remaining word
```

Only the **first word** of the normalized result becomes the cluster key.

This ensures phrases about the same subject group together despite different predicates:

```
"tests prefer tdd"      → key: "tests"
"tests use red-green"   → key: "tests"   ✓ same cluster
"components run shadcn" → key: "components"
"components check registry" → key: "components"  ✓ same cluster
```

### Step 3 — Filtering and Classification

```python
candidates = {k: v for k, v in clusters.items() if len(v) >= min_count}
```

Only clusters with `len ≥ min_count` (default 2) become candidates.

Confidence estimated from the number of observations:
```python
confidence = 0.5 + min(0.3, len(obs) * 0.05)
```

| Observations | Confidence |
|-------------|-----------|
| 1 | 0.55 |
| 2 | 0.60 |
| 4 | 0.70 |
| 6 | 0.80 |
| 8+ | 0.80 (cap) |

Candidate classification:
```python
def _classify_candidate(cluster_size, avg_conf):
    if cluster_size >= 3 and avg_conf >= 0.75:
        return "AGENT"
    if avg_conf >= 0.70:
        return "COMMAND"
    return "SKILL"
```

---

## Known Limitations

**False positives from generic nouns:**
- "tests", "files", "data" are very common → may aggregate unrelated patterns
- Mitigation: filter by `--project=<slug>` to keep context cohesive

**Short triggers collide:**
- "run tests" and "run lint" → key "run" (ambiguous)
- Mitigation: write triggers with a specific subject ("when tests fail..." not "run tests")

**No semantics:**
- "when writing tests" and "when running benchmarks" end up in different clusters
- This is intentional: the heuristic prioritizes precision over recall

---

## Trigger-Writing Strategies

To maximize cluster quality:

| ✅ Good | ❌ Avoid |
|--------|----------|
| "when writing tests prefer TDD" | "TDD" |
| "when adding components use shadcn" | "shadcn install" |
| "when schema changes run migration" | "migrate" |
| "when auth fails check RLS policies" | "RLS bug" |

Recommended pattern: **"when [context] [specific-action]"**

---

## Complete Example

```bash
# Capture observations throughout the session
osforge-db add-observation my-proj "when writing tests prefer TDD"
osforge-db add-observation my-proj "when writing tests check edge cases first"
osforge-db add-observation my-proj "when adding shadcn components run npx shadcn add"
osforge-db add-observation my-proj "when adding shadcn components check registry"
osforge-db add-observation my-proj "when auth fails verify RLS policies in Supabase"

# Analyze
osforge-db evolve --project=my-proj
```

Expected output:
```
EVOLVE ANALYSIS — 5 observation(s), project=my-proj
Clusters ≥ 2: 2

## SKILL CANDIDATES (2)
1. Cluster: "tests"      | 2 obs | conf 60%
2. Cluster: "shadcn"     | 2 obs | conf 60%
```

"auth" is left out (cluster_size = 1 < min_count).
