# llmfit Advisor (Local LLM Hardware Fit)

**Trigger:** Detecta hardware e recomenda LLMs locais. TRIGGER quando: usuário pergunta quais modelos rodam localmente, quer configurar Ollama/LM Studio, menciona rodar modelos offline, precisa de alternativa local por custo ou privacidade LGPD, dados sensíveis que não podem ir para API externa.

---

## Installation

```bash
# macOS
brew install llmfit

# Or via cargo
cargo install llmfit
```

---

## Commands

### Detect Hardware
```bash
llmfit --json system
```

Output:
```json
{
  "ram_gb": 32,
  "cpu_cores": 10,
  "gpu": "Apple M2 Pro",
  "vram_gb": 16,
  "unified_memory": true
}
```

### Get Recommendations
```bash
llmfit recommend --json --use-case coding --limit 3
```

Output:
```json
{
  "recommendations": [
    {
      "model": "codellama:13b-instruct-q4_K_M",
      "score": 0.92,
      "fit_level": "Perfect",
      "best_quant": "Q4_K_M",
      "estimated_tps": 45,
      "run_mode": "GPU"
    }
  ]
}
```

---

## Fit Levels

| Level | Score | Meaning |
|-------|-------|---------|
| **Perfect** | >0.9 | Runs smoothly, room to spare |
| **Good** | 0.7-0.9 | Runs well, may swap occasionally |
| **Marginal** | 0.5-0.7 | Runs but slow, swap likely |
| **TooTight** | <0.5 | Won't fit in memory |

---

## Run Modes

| Mode | Description |
|------|-------------|
| **GPU** | Full GPU acceleration |
| **CPU+GPU** | Hybrid, some layers on CPU |
| **CPU** | CPU only, GGML optimized |

---

## Smart Model Dispatch Integration

```typescript
// If task is Haiku-eligible AND data is sensitive
if (taskComplexity === 'haiku' && dataSensitivity === 'high') {
  // Prefer local model
  const recommendation = await llmfit.recommend({
    useCase: 'coding',
    limit: 1
  })

  if (recommendation.fit_level !== 'TooTight') {
    return useLocalModel(recommendation.model)
  }
}
```

---

## HF to Ollama Mapping

| Hugging Face | Ollama |
|--------------|--------|
| `meta-llama/Llama-2-7b-chat-hf` | `llama2:7b` |
| `codellama/CodeLlama-13b-Instruct-hf` | `codellama:13b-instruct` |
| `deepseek-ai/deepseek-coder-6.7b-instruct` | `deepseek-coder:6.7b` |
| `Qwen/Qwen2.5-Coder-7B-Instruct` | `qwen2.5-coder:7b` |

---

## OSForge Use Cases

1. **Privacidade obrigatória** — Dados de cliente que não podem sair do sistema
2. **Hardware limitado** — Clientes PME sem GPU potente
3. **Tasks repetitivas** — Economia de API em tarefas de alto volume
4. **Desenvolvimento offline** — Sem dependência de internet

---

## Example Workflow

```bash
# 1. Check system capabilities
llmfit --json system

# 2. Get coding recommendations
llmfit recommend --use-case coding --limit 3

# 3. Install recommended model
ollama pull codellama:13b-instruct-q4_K_M

# 4. Test inference speed
ollama run codellama:13b-instruct-q4_K_M "Write a TypeScript function"
```
