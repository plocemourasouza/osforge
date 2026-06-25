---
name: llmfit-advisor
description: "Detects the machine's hardware (RAM, CPU, GPU/VRAM) and recommends the best local LLMs with optimal quantization, speed estimate, and fit scoring. Use when: the user asks which models run locally, wants to set up Ollama/LM Studio, mentions running models offline, needs a local alternative for cost or privacy (LGPD), or when smart-model-dispatch identifies a task suitable for a local model."
metadata:
  author: osforge
  version: '1.0'
  source: github.com/AlexsJones/llmfit
  requires_binary: llmfit
---

# llmfit Advisor

Hardware-aware local LLM advisor. Detects real system specs and recommends models that actually run well, with optimal quantization and a tokens/s estimate.

## Prerequisite

```bash
# macOS
brew tap AlexsJones/llmfit && brew install llmfit

# Any platform (requires Rust)
cargo install llmfit

# Verify installation
llmfit --version
```

## When to use

The activation triggers are in the frontmatter description. Beyond those, use when
`smart-model-dispatch` identifies a task eligible for a local model
(boilerplate, translation, test stubs, simple CRUD) and cost/privacy are relevant.

---

## Essential commands

### Detect hardware
```bash
llmfit --json system
```
Returns CPU, total/available RAM, GPU, VRAM, backend (Metal/CUDA/ROCm/CPU), and whether it is unified memory (Apple Silicon).

### Top general recommendations
```bash
llmfit recommend --json --limit 5
```

### Filter by use case
```bash
llmfit recommend --json --use-case coding    --limit 3
llmfit recommend --json --use-case reasoning --limit 3
llmfit recommend --json --use-case chat      --limit 3
llmfit recommend --json --use-case general   --limit 5
```
Valid cases: `general` · `coding` · `reasoning` · `chat` · `multimodal` · `embedding`

### Filter by minimum fit level
```bash
llmfit recommend --json --min-fit perfect --limit 5
llmfit recommend --json --min-fit good    --limit 10
```
Levels: `perfect` › `good` › `marginal` (never recommend `TooTight`)

### VRAM override (when autodetect fails)
```bash
llmfit --memory=24G recommend --json --limit 5
```

---

## Interpreting the JSON output

### System
```json
{
  "system": {
    "cpu_name": "Apple M2 Max",
    "total_ram_gb": 32.0,
    "has_gpu": true,
    "gpu_vram_gb": 32.0,
    "backend": "Metal",
    "unified_memory": true
  }
}
```

### Recommendation fields — the most important ones

| Field | Meaning |
|---|---|
| `name` | HuggingFace ID (e.g. `Qwen/Qwen2.5-Coder-7B-Instruct`) |
| `score` | Composite score 0–100 (quality + speed + fit + context) |
| `fit_level` | `Perfect` / `Good` / `Marginal` / `TooTight` |
| `run_mode` | `GPU` / `CPU+GPU Offload` / `CPU` |
| `best_quant` | Best quantization for the hardware (e.g. `Q5_K_M`) |
| `estimated_tps` | Estimated tokens/s |
| `memory_required_gb` | VRAM/RAM required at that quantization |
| `category` | `Coding` / `Reasoning` / `Chat` / `Embedding` etc. |
| `is_moe` | Whether it uses Mixture-of-Experts (lower real VRAM than parameters suggest) |

**Golden rule:** `fit_level: "TooTight"` → never recommend. `Perfect` with `run_mode: GPU` → ideal choice.

---

## Integration with smart-model-dispatch

llmfit complements `smart-model-dispatch` by adding the **local track** to the model decision:

```
API Track (smart-model-dispatch)     Local Track (llmfit-advisor)
──────────────────────────────       ───────────────────────────
🔴 Opus    — deep reasoning           🟢 Qwen2.5-Coder — boilerplate, CRUD
🟡 Sonnet  — solid implementation     🟢 CodeLlama     — translation, stubs
🟢 Haiku   — mechanical/repetitive    🟢 Phi-4-mini    — docs, comments
```

**When to prefer local:**
- Task is Haiku-eligible AND data is sensitive (LGPD, accounting, legal)
- High volume of repetitive tasks where cost accumulates
- Offline environment or client with no API budget
- OSystems client data that cannot leave the local environment

**When to keep the API:**
- Task requires Opus (architecture, complex reasoning) — no viable local equivalent
- Quality is critical and latency matters
- Very long context (>32K tokens)

---

## Standard workflow

**"Which models can I run locally?"**
1. `llmfit --json system` → show hardware summary
2. `llmfit recommend --json --limit 5` → top 5 recommendations
3. Present with scores and fit levels in clear language
4. If the user wants to install: map the HuggingFace name → Ollama tag and offer `ollama pull`

**"Recommend a model for coding without API cost"**
1. `llmfit recommend --json --use-case coding --limit 3`
2. Present the code-specific options
3. Offer pull via Ollama and configuration

**Sensitive data (LGPD/accounting/legal)**
1. Confirm Ollama is running (`ollama list`)
2. `llmfit recommend --json --use-case general --min-fit good --limit 5`
3. Explain: local model = zero exposure of external data
4. Configure the chosen model

---

## HuggingFace → Ollama mapping (quick reference)

| llmfit name | Ollama tag |
|---|---|
| `Qwen/Qwen2.5-Coder-7B-Instruct` | `qwen2.5-coder:7b` |
| `Qwen/Qwen2.5-Coder-14B-Instruct` | `qwen2.5-coder:14b` |
| `Qwen/Qwen2.5-72B-Instruct` | `qwen2.5:72b` |
| `meta-llama/Llama-3.1-8B-Instruct` | `llama3.1:8b` |
| `meta-llama/Llama-3.3-70B-Instruct` | `llama3.3:70b` |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` | `deepseek-r1:32b` |
| `google/gemma-2-9b-it` | `gemma2:9b` |
| `mistralai/Mistral-7B-Instruct-v0.3` | `mistral:7b` |
| `microsoft/Phi-4-mini-instruct` | `phi4-mini` |

---

## OSForge / OSystems use cases

| Context | Recommended use |
|---|---|
| **Tressen (accounting)** | Local fiscal/OFX data — local model mandatory for privacy |
| **Red Caveat (legal)** | Contract documents — never to external API |
| **OSystems (SMB clients)** | Limited client hardware — llmfit identifies the best viable model |
| **Daily development** | Haiku-eligible tasks → local Qwen2.5-Coder = zero cost |
| **LinkMeTur / Mira** | High volume of CRUD/boilerplate → significant savings |

---

## Technical notes

- MoE models (Mixtral, DeepSeek-V3) have much lower real VRAM than the total parameter count — llmfit computes the real cost of expert offloading
- `best_quant` balances quality vs memory: Q8_0 is best quality, Q2_K is most compressed
- `estimated_tps` is an estimate based on per-backend benchmarks — actual result varies
- Apple Silicon: `unified_memory: true` means VRAM = system RAM
