# OSForge Qdrant — Memória Vetorial

## 3 tiers de fallback

| Tier | Backend | Quando ativo |
|------|---------|--------------|
| 1 | **Qdrant** (Docker, HNSW) | `vector_backend=qdrant` em config.json ou `OSFORGE_VECTOR=qdrant` |
| 2 | **SQLite** (cosine brute-force) | `vector_backend=sqlite` (padrão se Qdrant ausente) |
| 3 | **off** (FTS5 lexical apenas) | `OSFORGE_EMBED=off` |

Qdrant é o STORE vetorial. O EMBEDDER (quem converte texto em vetor) é configurado separadamente via `embed_provider`.

## Contrato config.json (`~/.osforge/config.json`)

```json
{
  "vector_backend":  "qdrant",
  "embed_provider":  "ollama",
  "embed_model":     "bge-m3",
  "qdrant_url":      "http://localhost:6333",
  "collection":      "osforge_memory"
}
```

Variáveis de ambiente têm precedência sobre config.json:

| Env var | Config.json key | Default |
|---------|-----------------|---------|
| `OSFORGE_VECTOR` | `vector_backend` | `sqlite` |
| `OSFORGE_EMBED` | `embed_provider` | `ollama` |
| `OSFORGE_EMBED_MODEL` | `embed_model` | (depende do provider) |
| `OSFORGE_QDRANT_URL` | `qdrant_url` | `http://localhost:6333` |
| `OSFORGE_COLLECTION` | `collection` | `osforge_memory` |
| `OSFORGE_CONFIG` | (caminho do arquivo config) | `~/.osforge/config.json` |

`OSFORGE_CONFIG` aceita caminho para um arquivo de config alternativo — útil para testes isolados sem tocar o config global.

## Inicialização

```bash
# Subir Qdrant
docker compose -f scripts/qdrant/docker-compose.yml up -d

# Verificar saúde
curl http://localhost:6333/healthz

# Criar/validar coleção (descobre dim embedando uma probe string)
OSFORGE_VECTOR=qdrant OSFORGE_EMBED=ollama osforge-db vec-init

# Status completo
OSFORGE_VECTOR=qdrant osforge-db vec-status

# Backfill das decisões existentes para Qdrant
OSFORGE_VECTOR=qdrant OSFORGE_EMBED=ollama osforge-db embed-backfill
```

## Parar / reiniciar

```bash
docker compose -f scripts/qdrant/docker-compose.yml stop
docker compose -f scripts/qdrant/docker-compose.yml down   # remove container, mantém volume
docker compose -f scripts/qdrant/docker-compose.yml down -v # apaga também o volume
```

## Dependência Ollama

Qdrant é o store; Ollama provê os embeddings. Para usar `embed_provider=ollama`:

```bash
# Verificar se está instalado
command -v ollama

# Verificar modelo
ollama list | grep bge-m3

# Instalar modelo se ausente
ollama pull bge-m3
```

Sem Ollama, use `OSFORGE_EMBED=mock` para testes de pipeline (não semântico) ou `OSFORGE_EMBED=off` (degrada para FTS5).

### Escolha do modelo: `bge-m3` (default) vs `nomic-embed-text`

Default é **`bge-m3`** (multilíngue, 1024d, ~1.2GB). Avaliação empírica em texto técnico curto em PT-BR (3 decisões, 3 queries sem overlap léxico):

| Modelo | Acertos top-1 | Observação |
|--------|---------------|------------|
| `bge-m3` | **3/3** | separação saudável (gaps 0.05–0.18), multilíngue |
| `nomic-embed-text` | 1/3 | um doc domina todas as queries; gaps minúsculos (0.03–0.06); inglês-cêntrico |

Para corpus majoritariamente em inglês ou se 1.2GB for inviável, `OSFORGE_EMBED_MODEL=nomic-embed-text` (274MB) é a alternativa leve — ao trocar o modelo, **a dim muda** (768 vs 1024): rode `vec-init` (recria a coleção) + `embed-backfill` para re-popular.

## Dados persistentes

O volume está em `~/.osforge/qdrant/storage`. O deploy não apaga este diretório. Para limpar manualmente:

```bash
rm -rf ~/.osforge/qdrant/storage
```
