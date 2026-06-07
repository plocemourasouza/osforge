---
name: llmfit-advisor
description: "Detecta o hardware da máquina (RAM, CPU, GPU/VRAM) e recomenda os melhores LLMs locais com quantização ideal, estimativa de velocidade e scoring de fit. TRIGGER quando: usuário pergunta quais modelos rodam localmente, quer configurar Ollama/LM Studio, menciona rodar modelos offline, precisa de alternativa local por custo ou privacidade (LGPD), ou quando smart-model-dispatch identifica tarefa adequada para modelo local."
metadata:
  author: osforge
  version: '1.0'
  source: github.com/AlexsJones/llmfit
  requires_binary: llmfit
---

# llmfit Advisor

Hardware-aware local LLM advisor. Detecta specs reais do sistema e recomenda modelos que de fato rodam bem, com quantização ótima e estimativa de tokens/s.

## Pré-requisito

```bash
# macOS
brew tap AlexsJones/llmfit && brew install llmfit

# Qualquer plataforma (requer Rust)
cargo install llmfit

# Verificar instalação
llmfit --version
```

## Quando usar

Os gatilhos de ativação estão na description do frontmatter. Além deles, usar quando
`smart-model-dispatch` identificar tarefa elegível para modelo local
(boilerplate, tradução, test stubs, CRUD simples) e custo/privacidade forem relevantes.

---

## Comandos essenciais

### Detectar hardware
```bash
llmfit --json system
```
Retorna CPU, RAM total/disponível, GPU, VRAM, backend (Metal/CUDA/ROCm/CPU) e se é memória unificada (Apple Silicon).

### Top recomendações gerais
```bash
llmfit recommend --json --limit 5
```

### Filtrar por caso de uso
```bash
llmfit recommend --json --use-case coding    --limit 3
llmfit recommend --json --use-case reasoning --limit 3
llmfit recommend --json --use-case chat      --limit 3
llmfit recommend --json --use-case general   --limit 5
```
Casos válidos: `general` · `coding` · `reasoning` · `chat` · `multimodal` · `embedding`

### Filtrar por nível mínimo de fit
```bash
llmfit recommend --json --min-fit perfect --limit 5
llmfit recommend --json --min-fit good    --limit 10
```
Níveis: `perfect` › `good` › `marginal` (nunca recomendar `TooTight`)

### Override de VRAM (quando autodetect falhar)
```bash
llmfit --memory=24G recommend --json --limit 5
```

---

## Interpretando o output JSON

### Sistema
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

### Campos de recomendação — os mais importantes

| Campo | Significado |
|---|---|
| `name` | ID HuggingFace (ex: `Qwen/Qwen2.5-Coder-7B-Instruct`) |
| `score` | Score composto 0–100 (qualidade + velocidade + fit + contexto) |
| `fit_level` | `Perfect` / `Good` / `Marginal` / `TooTight` |
| `run_mode` | `GPU` / `CPU+GPU Offload` / `CPU` |
| `best_quant` | Melhor quantização para o hardware (ex: `Q5_K_M`) |
| `estimated_tps` | Tokens/s estimados |
| `memory_required_gb` | VRAM/RAM necessária nessa quantização |
| `category` | `Coding` / `Reasoning` / `Chat` / `Embedding` etc. |
| `is_moe` | Se usa Mixture-of-Experts (menor VRAM real que parâmetros sugerem) |

**Regra de ouro:** `fit_level: "TooTight"` → nunca recomendar. `Perfect` com `run_mode: GPU` → escolha ideal.

---

## Integração com smart-model-dispatch

O llmfit complementa o `smart-model-dispatch` adicionando o **track local** à decisão de modelo:

```
API Track (smart-model-dispatch)     Local Track (llmfit-advisor)
──────────────────────────────       ───────────────────────────
🔴 Opus    — raciocínio profundo     🟢 Qwen2.5-Coder — boilerplate, CRUD
🟡 Sonnet  — implementação sólida    🟢 CodeLlama     — tradução, stubs
🟢 Haiku   — mecânico/repetitivo     🟢 Phi-4-mini    — docs, comentários
```

**Quando preferir local:**
- Tarefa é Haiku-eligible E dados são sensíveis (LGPD, contábil, jurídico)
- Volume alto de tarefas repetitivas onde custo acumula
- Ambiente offline ou cliente sem budget para API
- Dados de clientes OSystems que não podem sair do ambiente local

**Quando manter API:**
- Tarefa requer Opus (arquitetura, raciocínio complexo) — sem equivalente local viável
- Qualidade é crítica e latência importa
- Contexto muito longo (>32K tokens)

---

## Workflow padrão

**"Quais modelos posso rodar localmente?"**
1. `llmfit --json system` → mostrar resumo do hardware
2. `llmfit recommend --json --limit 5` → top 5 recomendações
3. Apresentar com scores e fit levels em linguagem clara
4. Se usuário quiser instalar: mapear nome HuggingFace → tag Ollama e oferecer `ollama pull`

**"Recomenda modelo para coding sem custo de API"**
1. `llmfit recommend --json --use-case coding --limit 3`
2. Apresentar as opções específicas para código
3. Oferecer pull via Ollama e configuração

**Dados sensíveis (LGPD/contábil/jurídico)**
1. Confirmar que Ollama está rodando (`ollama list`)
2. `llmfit recommend --json --use-case general --min-fit good --limit 5`
3. Explicar: modelo local = zero exposição de dados externos
4. Configurar modelo escolhido

---

## Mapeamento HuggingFace → Ollama (referência rápida)

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

## Casos de uso OSForge / OSystems

| Contexto | Uso recomendado |
|---|---|
| **Tressen (contábil)** | Dados fiscais/OFX locais — modelo local obrigatório por privacidade |
| **Red Caveat (jurídico)** | Documentos contratuais — nunca para API externa |
| **OSystems (clientes PME)** | Hardware limitado do cliente — llmfit identifica o melhor modelo viável |
| **Desenvolvimento diário** | Haiku-eligible tasks → Qwen2.5-Coder local = zero custo |
| **LinkMeTur / Mira** | Volume alto de CRUD/boilerplate → economia significativa |

---

## Notas técnicas

- Modelos MoE (Mixtral, DeepSeek-V3) têm VRAM real muito menor que o total de parâmetros — llmfit calcula o custo real de expert offloading
- `best_quant` balanceia qualidade vs memória: Q8_0 é melhor qualidade, Q2_K é mais comprimido
- `estimated_tps` é estimativa baseada em benchmarks por backend — resultado real varia
- Apple Silicon: `unified_memory: true` significa que VRAM = RAM do sistema
