#!/usr/bin/env python3
"""
osforge-db — SQLite state manager para o OSForge
Uso: osforge-db <comando> [args] [--scope=local|global] [--json]

Escopo global:  ~/.osforge/osforge.db  (padrão — cross-project; OSFORGE_DB=<path> sobrepõe)
Escopo local:   .osforge/osforge.db    (por projeto — via --scope=local)

Comandos:
  init                              Cria banco e schema
  status <slug>                     Estado atual do projeto (para INTAKE)
  resume <slug>                     Resume point compacto (para shell injection)
  upsert-project <slug> <desc> <triage> <status> [--root=DIR|.] [--remote=URL|auto]
  bind-project <slug> [--root=DIR|.] [--remote=URL|auto]
                                    Amarra o projeto à raiz git e/ou ao remote; é assim que
                                    os hooks reconhecem subdiretórios, worktrees e pastas
                                    homônimas (hooks/lib/project_id.py)
  set-phase <slug> <phase> <status> [skill] [artifact]
  set-resume <slug> <resume_point>
  add-decision <slug> <content> [--category=arch|product|ux|data|security]
  add-blocker <slug> <description> [--waiting=<what>]
  resolve-blocker <slug> <blocker_id>
  list-blockers <slug>
  list-decisions <slug> [--category=<cat>] [--limit=5] [--since=YYYY-MM-DD] [--until=YYYY-MM-DD]
  add-task <slug> <title> [--phase=<name>] [--wave=N] [--depends=1,2] [--priority=p0|p1|p2]
  set-task <slug> <task_id> <status>   status: pending|in-progress|done|blocked|cancelled
  list-tasks <slug> [--status=<status>]
  board [--status=active|all]          Visão cross-project de tasks
  search <query> [--project=<slug>] [--limit=5] [--since=YYYY-MM-DD] [--until=YYYY-MM-DD]
                                    FTS5: content words OR-ed (stopwords pt/en dropped),
                                    accent-insensitive, bm25 order. since/until inclusive.
  list-projects [--status=active|all]
  set-project-status <slug> <active|backlog|paused|done|archived>
                                    Ciclo de vida do projeto (ADR-019); o monitor agrupa por ele
  monitor [<slug>] [--days=30] [--discover] [--all] [--compact]
                                    Contrato do monitor (osforge.monitor.v1, sempre JSON, só leitura):
                                    sem slug = portfólio; com slug = detalhe (B-036)
  live                              O que roda agora (Claude Code, IDE, servidor de dev) por projeto (B-040)
  inbox-add <slug> <texto>          Orientação para os agentes do projeto (entregue pelo hook inbox-deliver)
  inbox-take <slug> --session=ID    Entrega atômica das pendentes (JSON); usado pelo hook
  inbox <slug> | inbox-cancel <id>
  run-add <slug> --kind=terminal|background|ide [--tool=] [--prompt=] [--pid=] [--log=]
  run-update <id> [--status=] [--result=] [--cost=] | runs <slug>
  add-signal <slug> <callers_open|duplicate|tests> <subject> [--detail=JSON] [--session=ID]
  resolve-signal <id> [<id>...]
  signals [<slug>] [--open] [--report] [--since=YYYY-MM-DD]
                                    Sinais do quality-guard (B-035); --report = resumo da sombra
  import-yaml <yaml_path> <slug>    Migra status.yaml existente
  stats                             Resumo geral do banco
  add-usage <slug> --session=ID --model=M --input=N --output=N [--cache-read=N] [--cache-create=N] [--turns=N]
                                    Tokens de uma sessão (upsert por projeto+sessão+modelo; B-022)
  usage <slug>                      Tokens por sessão e modelo do projeto; totais no `board` e no `stats`

  add-observation <project> <trigger_text> [--context=<ctx>] [--tool=<tool>]
                                    Grava uma observação de sessão no banco
  evolve [--project=<slug>] [--min-count=2]
                                    Clusteriza observations e propõe candidates
                                    (SKILL/COMMAND/AGENT); não escreve arquivos
  list-instincts [--project=<slug>] [--scope=project|global]
                                    Lista instincts promovidos
  promote-instinct <instinct_id> [--scope=global]
                                    Promove instinct project→global (conf ≥ 0.8)

  Memória vetorial híbrida (3 tiers: qdrant > sqlite > off):
  vec-init                          Cria/valida coleção Qdrant (descobre dim via probe).
                                    No-op se backend=sqlite ou OSFORGE_EMBED=off.
  embed <source_table> <source_id> <text>
                                    Computa e faz upsert via vstore (qdrant ou sqlite).
                                    No-op com aviso se OSFORGE_EMBED=off.
  embed-backfill [--source=decisions]
                                    Embeda linhas existentes sem embedding.
                                    No-op se OSFORGE_EMBED=off.
  search-semantic <query> [--top=5]
                                    Busca vetorial (Qdrant ou SQLite conforme backend).
                                    OSFORGE_EMBED=off → mensagem clara; exit 0.
  search-hybrid <query> [--project=<slug>] [--top=5] [--since=YYYY-MM-DD] [--until=YYYY-MM-DD]
                                    RRF(FTS5 + vector), both legs filtered before the merge.
                                    Embedder off = plain FTS5 search, no note.
                                    Embedder unreachable → FTS5 only, with a stdout
                                    note and `degraded` in each --json row.
  vec-status                        Backend ativo, provider, modelo, contagem, coverage
                                    (embedded/total decisions), embedder reachable.
                                    Se qdrant: mostra saúde + total de pontos.
  memory-health [--timeout=0.3]     One-line hint when the embedder is down or coverage
                                    is under 80%; silent otherwise (session-resume hook).

  Brain — long-term memory (Qdrant + journal ~/.osforge/brain.jsonl; scripts/osforge_brain.py):
  remember "<text>" --kind=decision|knowledge|technique|methodology [--project=slug|--global] [--tags=a,b]
                                    Journal first (scrubbed), then index (dense gemma + sparse BM25).
  recall "<query>" [--kind=] [--project=slug|--global] [--since=YYYY-MM-DD] [--until=YYYY-MM-DD]
                   [--top=5] [--mode=dense|keyword|hybrid] [--json]
                                    Dense first; nothing above the floor → BM25. Store/embedder
                                    down → lexical scan of the journal + `note: brain degraded`.
  forget <id|prefix>                Tombstone in the journal + delete the point
  brain status|rebuild|migrate|health
                                    rebuild = collection from the journal; migrate = SQLite
                                    decisions → brain (idempotent); health = one line or nothing
    OSFORGE_BRAIN=off  OSFORGE_BRAIN_STORE=server|local  OSFORGE_BRAIN_PATH  OSFORGE_QDRANT_URL
    OSFORGE_BRAIN_EMBED=gemma|e5-large|fake  OSFORGE_BRAIN_PYTHON  OSFORGE_BRAIN_MODELS  OSFORGE_BRAIN_MIN_SCORE

  Variáveis de ambiente:
    OSFORGE_EMBED       ollama (padrão) | off | mock | voyage | openai
    OSFORGE_EMBED_MODEL Modelo para o provider (default ollama: bge-m3 multilíngue; ex: nomic-embed-text, voyage-3-lite)
    OSFORGE_VECTOR      sqlite (padrão) | qdrant
    OSFORGE_QDRANT_URL  URL do Qdrant (padrão: http://localhost:6333)
    OSFORGE_OLLAMA_URL  Ollama endpoint (default: http://localhost:11434; config: ollama_url)
    OSFORGE_COLLECTION  Nome da coleção Qdrant (padrão: osforge_memory)
    OSFORGE_CONFIG      Caminho alternativo para config.json (para testes isolados)
    VOYAGE_API_KEY      Chave para voyage
    OPENAI_API_KEY      Chave para openai
"""

import sqlite3, sys, os, json, textwrap, math, hashlib, struct, re, unicodedata, time, shlex
from array import array
from datetime import datetime, timezone, timedelta
from pathlib import Path


class _LazyModule:
    """Imports on first attribute access. urllib.request costs ~60 ms to import and only the
    vector/HTTP paths use it; every other command (and every hook calling osforge-db) skips it."""

    def __init__(self, name):
        self._name, self._mod = name, None

    def __getattr__(self, attr):
        if self._mod is None:
            import importlib
            self._mod = importlib.import_module(self._name)
        return getattr(self._mod, attr)


_urllib_request = _LazyModule("urllib.request")
_urllib_error = _LazyModule("urllib.error")

# The brain (long-term memory) ships next to this file; stdlib-only at import time.
# No bytecode: the deployed copy lives in ~/.local/bin, which must not grow a __pycache__.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import osforge_brain as _brain  # noqa: E402

# numpy é OPCIONAL — acelerador; resultado idêntico ao pure-Python. Imported lazily, on the
# first vector operation: importing it costs ~100 ms, paid by every hook that calls osforge-db
# and by the monitor's 200 ms budget even though they never touch a vector (B-036).
_np = None
_HAS_NUMPY = None


def _numpy():
    global _np, _HAS_NUMPY
    if _HAS_NUMPY is None:
        try:
            import numpy as _mod
            _np, _HAS_NUMPY = _mod, True
        except ImportError:
            _np, _HAS_NUMPY = None, False
    return _np

# ── Localização do banco ──────────────────────────────────────────────────

def db_path(scope="global"):
    if scope == "local":
        return Path(".osforge/osforge.db")
    override = os.environ.get("OSFORGE_DB", "").strip()      # documentado desde sempre, lido só agora (E-A26)
    if override:
        return Path(override).expanduser()
    return Path.home() / ".osforge" / "osforge.db"

def get_conn(scope="global"):
    path = db_path(scope)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

# ── Memória vetorial: provider de embedding ───────────────────────────────
#
# OSFORGE_EMBED  = ollama (padrão) | off | mock | voyage | openai
# OSFORGE_EMBED_MODEL = nome do modelo para o provider
#
# mock: embedding DETERMINÍSTICO offline usando hashlib.
#   NÃO é semântico — existe apenas para testar o pipeline completo sem rede.
#   Dois textos idênticos → vetor idêntico; textos diferentes → vetores distintos
#   por hash de tokens. Dimensão fixa: 64. Normalizado L2.
#
# Política de falha de rede: retorna None + warning em stderr. NUNCA crash.

_EMBED_MODEL_ENV  = os.environ.get("OSFORGE_EMBED_MODEL", "").strip()

# ── Config loader (lê ~/.osforge/config.json ou OSFORGE_CONFIG) ────────────
# Precedência: env vars > config.json > defaults

def _load_osforge_config():
    """Carrega config JSON. Retorna dict. Nunca lança exceção."""
    cfg_path_env = os.environ.get("OSFORGE_CONFIG", "")
    if cfg_path_env:
        cfg_path = Path(cfg_path_env)
    else:
        cfg_path = Path.home() / ".osforge" / "config.json"
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

_OSFORGE_CFG = _load_osforge_config()

def _cfg(key, default=""):
    """Lê valor do config.json (usado apenas para chaves sem env var direta)."""
    return _OSFORGE_CFG.get(key, default)

# Provider de embedding: env > config > default "ollama"
_EMBED_PROVIDER = (
    os.environ.get("OSFORGE_EMBED", "").lower().strip()
    or _cfg("embed_provider", "ollama").lower().strip()
)

# Backend vetorial: env > config > default "sqlite"
_VECTOR_BACKEND = (
    os.environ.get("OSFORGE_VECTOR", "").lower().strip()
    or _cfg("vector_backend", "sqlite").lower().strip()
)

# URL e coleção Qdrant
_QDRANT_URL = (
    os.environ.get("OSFORGE_QDRANT_URL", "").strip()
    or _cfg("qdrant_url", "http://localhost:6333")
)
_QDRANT_COLLECTION = (
    os.environ.get("OSFORGE_COLLECTION", "").strip()
    or _cfg("collection", "osforge_memory")
)

# Ollama endpoint: env > config > default (the override lets tests point at a dead port)
_OLLAMA_URL = (
    os.environ.get("OSFORGE_OLLAMA_URL", "").strip()
    or _cfg("ollama_url", "http://localhost:11434")
).rstrip("/")

_DEFAULT_MODELS = {
    "ollama":  "bge-m3",
    "voyage":  "voyage-3-lite",
    "openai":  "text-embedding-3-small",
    "mock":    "mock-hash-64",
}

def _embed_model():
    return _EMBED_MODEL_ENV or _DEFAULT_MODELS.get(_EMBED_PROVIDER, "unknown")

def _vec_normalize(vec):
    """Normaliza vetor L2 → retorna list[float]. Usa numpy se disponível."""
    if _numpy() is not None:
        a = _np.array(vec, dtype=_np.float32)
        n = float(_np.linalg.norm(a))
        if n == 0.0:
            return a.tolist()
        return (a / n).tolist()
    # pure-Python fallback
    n = math.sqrt(sum(x * x for x in vec))
    if n == 0.0:
        return list(vec)
    return [x / n for x in vec]

def _vec_to_blob(vec):
    """Serializa list[float] como bytes float32 (array stdlib)."""
    a = array('f', [float(x) for x in vec])
    return a.tobytes()

def _blob_to_vec(blob):
    """Desserializa bytes → list[float]."""
    a = array('f')
    a.frombytes(blob)
    return list(a)

def _cosine(a, b):
    """Cosseno entre dois vetores já normalizados L2 → valor em [-1, 1]."""
    if _numpy() is not None:
        return float(_np.dot(_np.array(a, dtype=_np.float32),
                             _np.array(b, dtype=_np.float32)))
    return sum(x * y for x, y in zip(a, b))

def _embed_mock(text, dim=64):
    """Embedding determinístico offline para testes de pipeline.
    NÃO é semântico. Usa SHA-256 de tokens para preencher o vetor.
    """
    tokens = text.lower().split()
    vec = [0.0] * dim
    for i, tok in enumerate(tokens or [text]):
        digest = hashlib.sha256(tok.encode()).digest()
        for j in range(dim):
            byte_val = digest[j % len(digest)]
            vec[j] += float(byte_val) * math.cos(float(i + j))
    return _vec_normalize(vec)

def _embed_ollama(text, model):
    """Chama Ollama local (http://localhost:11434/api/embeddings)."""
    url = _OLLAMA_URL + "/api/embeddings"
    payload = json.dumps({"model": model, "prompt": text}).encode()
    req = _urllib_request.Request(url, data=payload,
                                  headers={"Content-Type": "application/json"})
    try:
        with _urllib_request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        return data["embedding"]
    except Exception as exc:
        print(f"[osforge-db] aviso: ollama embed falhou ({exc})", file=sys.stderr)
        return None

def _embed_voyage(text, model):
    """Chama Voyage AI embeddings API."""
    api_key = os.environ.get("VOYAGE_API_KEY", "")
    if not api_key:
        print("[osforge-db] aviso: VOYAGE_API_KEY não definida", file=sys.stderr)
        return None
    url = "https://api.voyageai.com/v1/embeddings"
    payload = json.dumps({"input": [text], "model": model}).encode()
    req = _urllib_request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    })
    try:
        with _urllib_request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        return data["data"][0]["embedding"]
    except Exception as exc:
        print(f"[osforge-db] aviso: voyage embed falhou ({exc})", file=sys.stderr)
        return None

def _embed_openai(text, model):
    """Chama OpenAI embeddings API."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[osforge-db] aviso: OPENAI_API_KEY não definida", file=sys.stderr)
        return None
    url = "https://api.openai.com/v1/embeddings"
    payload = json.dumps({"input": text, "model": model}).encode()
    req = _urllib_request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    })
    try:
        with _urllib_request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        return data["data"][0]["embedding"]
    except Exception as exc:
        print(f"[osforge-db] aviso: openai embed falhou ({exc})", file=sys.stderr)
        return None

def compute_embedding(text):
    """Computa embedding para `text` usando o provider configurado.
    Retorna list[float] normalizado ou None (se provider=off ou falha de rede).
    """
    provider = _EMBED_PROVIDER
    model    = _embed_model()
    if provider == "off":
        return None
    if provider == "mock":
        return _embed_mock(text)
    if provider == "ollama":
        vec = _embed_ollama(text, model)
    elif provider == "voyage":
        vec = _embed_voyage(text, model)
    elif provider == "openai":
        vec = _embed_openai(text, model)
    else:
        print(f"[osforge-db] aviso: provider desconhecido '{provider}'; "
              "use off|mock|ollama|voyage|openai", file=sys.stderr)
        return None
    if vec is None:
        return None
    return _vec_normalize(vec)

# ── Qdrant REST backend (urllib stdlib — zero deps) ───────────────────────

import uuid as _uuid

_QDRANT_NS = _uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # NAMESPACE_URL


def _qdrant_req(method, path, body=None, timeout=10):
    """Faz requisição REST ao Qdrant. Retorna (status_code, dict|None).
    Em falha de rede retorna (0, None) — NUNCA lança exceção.
    """
    url = _QDRANT_URL.rstrip("/") + path
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"}
    req = _urllib_request.Request(url, data=data, headers=headers, method=method)
    try:
        with _urllib_request.urlopen(req, timeout=timeout) as resp:
            try:
                return resp.status, json.loads(resp.read().decode())
            except Exception:
                return resp.status, None
    except _urllib_error.HTTPError as exc:
        # Status HTTP real (ex.: 404 = coleção inexistente no ensure_collection).
        # Não é falha de rede — devolve o código para o caller decidir, sem ruído.
        try:
            payload = json.loads(exc.read().decode())
        except Exception:
            payload = None
        return exc.code, payload
    except Exception as exc:
        print(f"[osforge-db] aviso: Qdrant {method} {path} falhou ({exc})",
              file=sys.stderr)
        return 0, None


def _qdrant_ensure_collection(dim):
    """Cria coleção se não existir. No-op se já existe. Retorna True em sucesso."""
    status, _ = _qdrant_req("GET", f"/collections/{_QDRANT_COLLECTION}")
    if status == 200:
        return True
    if status == 404 or status == 0:
        body = {
            "vectors": {
                "size": dim,
                "distance": "Cosine",
            }
        }
        st2, _ = _qdrant_req("PUT", f"/collections/{_QDRANT_COLLECTION}", body)
        if st2 in (200, 201):
            return True
        print(f"[osforge-db] aviso: Qdrant create collection status={st2}",
              file=sys.stderr)
        return False
    print(f"[osforge-db] aviso: Qdrant collection check status={status}",
          file=sys.stderr)
    return False


def _qdrant_point_id(source_table, source_id):
    """UUID v5 determinístico para idempotência de upsert."""
    key = f"{source_table}:{source_id}"
    return str(_uuid.uuid5(_QDRANT_NS, key))


def _qdrant_upsert(source_table, source_id, content, vec):
    """Upsert de ponto no Qdrant. Retorna True em sucesso."""
    if not _qdrant_ensure_collection(len(vec)):
        return False
    point_id = _qdrant_point_id(source_table, source_id)
    body = {
        "points": [
            {
                "id": point_id,
                "vector": list(vec),
                "payload": {
                    "source_table": source_table,
                    "source_id": str(source_id),
                    "content": content,
                },
            }
        ]
    }
    st, _ = _qdrant_req("PUT",
                        f"/collections/{_QDRANT_COLLECTION}/points?wait=true",
                        body)
    if st in (200, 201):
        return True
    print(f"[osforge-db] aviso: Qdrant upsert status={st}", file=sys.stderr)
    return False


def _qdrant_search(query_vec, top, project=None):
    """Busca vetorial no Qdrant. Retorna list[(source_table, source_id, content, score)].
    Em falha retorna lista vazia — NUNCA lança exceção.
    """
    body = {
        "vector": list(query_vec),
        "limit": int(top),
        "with_payload": True,
    }
    st, resp = _qdrant_req("POST",
                           f"/collections/{_QDRANT_COLLECTION}/points/search",
                           body)
    if st == 0 or resp is None:
        return []
    results = []
    for hit in resp.get("result", []):
        payload = hit.get("payload", {})
        src_table = payload.get("source_table", "")
        src_id    = payload.get("source_id", "")
        content   = payload.get("content", "")
        score     = float(hit.get("score", 0.0))
        results.append((src_table, src_id, content, score))
    return results


# ── vstore abstraction ────────────────────────────────────────────────────

def vstore_upsert(conn, source_table, source_id, content, vec):
    """Grava embedding no backend ativo (qdrant ou sqlite)."""
    if _VECTOR_BACKEND == "qdrant":
        _qdrant_upsert(source_table, str(source_id), content, vec)
        # Sempre grava também em SQLite como cache/fallback
        _sqlite_upsert(conn, source_table, source_id, content, vec)
    else:
        _sqlite_upsert(conn, source_table, source_id, content, vec)


def vstore_search(conn, query_vec, top, project=None):
    """Busca vetorial no backend ativo.
    Retorna list[(source_table, source_id, content, score)].
    """
    if _VECTOR_BACKEND == "qdrant":
        results = _qdrant_search(query_vec, top, project)
        if results:
            return results
        # Fallback silencioso para SQLite se Qdrant retornar vazio
        print("[osforge-db] aviso: Qdrant vazio ou inacessível — fallback SQLite.",
              file=sys.stderr)
    return _sqlite_search(conn, query_vec, top)


def _sqlite_upsert(conn, source_table, source_id, content, vec):
    """SQLite upsert (implementação original preservada)."""
    model = _embed_model()
    dim   = len(vec)
    blob  = _vec_to_blob(vec)
    conn.execute("""
        INSERT INTO vec_memory (source_table, source_id, content, dim, model, embedding)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_table, source_id, model) DO UPDATE SET
            content    = excluded.content,
            dim        = excluded.dim,
            embedding  = excluded.embedding,
            created_at = datetime('now','utc')
    """, (source_table, str(source_id), content, dim, model, blob))
    conn.commit()


def _sqlite_search(conn, query_vec, top):
    """Cosine brute-force em vec_memory (implementação original preservada)."""
    rows = conn.execute(
        "SELECT source_table, source_id, content, embedding FROM vec_memory"
    ).fetchall()
    if not rows:
        return []
    scored = []
    for row in rows:
        doc_vec = _blob_to_vec(row["embedding"])
        score   = _cosine(query_vec, doc_vec)
        scored.append((row["source_table"], row["source_id"], row["content"], score))
    scored.sort(key=lambda x: x[3], reverse=True)
    return scored[:int(top)]


def upsert_vec_memory(conn, source_table, source_id, content, vec):
    """Compatibilidade: delega para vstore_upsert."""
    vstore_upsert(conn, source_table, str(source_id), content, vec)

# ── Comandos vetoriais ────────────────────────────────────────────────────

def cmd_embed(conn, source_table, source_id, text):
    """Computa e faz upsert via vstore_upsert. No-op com aviso se provider=off."""
    if _EMBED_PROVIDER == "off":
        print("[osforge-db] embed: provider=off. "
              "Defina OSFORGE_EMBED=mock|ollama|voyage|openai para habilitar.",
              file=sys.stderr)
        return
    vec = compute_embedding(text)
    if vec is None:
        print("[osforge-db] embed: falha ao computar embedding (veja avisos acima).",
              file=sys.stderr)
        return
    vstore_upsert(conn, source_table, str(source_id), text, vec)
    _ok(f"vstore[{_VECTOR_BACKEND}]: {source_table}/{source_id} embedado "
        f"(dim={len(vec)}, model={_embed_model()})")

def cmd_embed_backfill(conn, source="decisions"):
    """Embeda linhas existentes de `source` sem embedding em vec_memory."""
    if _EMBED_PROVIDER == "off":
        print("[osforge-db] embed-backfill: provider=off — no-op. "
              "Defina OSFORGE_EMBED para habilitar.", file=sys.stderr)
        return
    model = _embed_model()
    if source == "decisions":
        rows = conn.execute("""
            SELECT d.id, d.content FROM decisions d
            WHERE NOT EXISTS (
                SELECT 1 FROM vec_memory v
                WHERE v.source_table='decisions'
                  AND v.source_id=CAST(d.id AS TEXT)
                  AND v.model=?
            )
        """, (model,)).fetchall()
    else:
        _err(f"Fonte '{source}' não suportada para backfill. Use: decisions")
        return
    count = 0
    for row in rows:
        vec = compute_embedding(row["content"])
        if vec is None:
            print(f"[osforge-db] backfill: falha no id={row['id']} — pulando",
                  file=sys.stderr)
            continue
        vstore_upsert(conn, source, str(row["id"]), row["content"], vec)
        count += 1
    _ok(f"embed-backfill [{_VECTOR_BACKEND}]: {count}/{len(rows)} itens de '{source}'")

def cmd_search_semantic(conn, query, top=5):
    """Busca vetorial via vstore_search (Qdrant ou SQLite conforme backend ativo).
    Se provider=off → mensagem clara e exit 0.
    """
    if _EMBED_PROVIDER == "off":
        print("Busca semântica desativada: OSFORGE_EMBED=off.\n"
              "Use `search <query>` para busca FTS5 textual, ou defina\n"
              "OSFORGE_EMBED=mock|ollama|voyage|openai para habilitar vetores.")
        return
    q_vec = compute_embedding(query)
    if q_vec is None:
        _err("Falha ao computar embedding da query. Veja avisos acima.")
    results = vstore_search(conn, q_vec, int(top))
    if not results:
        _out("Nenhum resultado encontrado. Use `embed-backfill` para popular.")
        return
    if _json_mode:
        out = [{"score": round(score, 4), "source_table": st, "source_id": sid,
                "content": c} for st, sid, c, score in results]
        print(json.dumps(out, ensure_ascii=False))
        return
    _out(f"── Busca semantica [{_VECTOR_BACKEND}]: '{query}' (top={top}) ──────────────────")
    for rank, (src_table, src_id, content, score) in enumerate(results, 1):
        short = textwrap.shorten(content, width=100, placeholder="...")
        _out(f"  #{rank} [{src_table}/{src_id}] score={score:.4f}  {short}")

def _rrf_merge(ranked_a, ranked_b, k=60):
    """Reciprocal Rank Fusion de duas listas rankeadas.
    Cada lista e uma seq de id_str onde posicao = rank.
    Retorna lista de ids ordenada por RRF score desc.
    k=60 segue o valor classico do paper Cormack et al. 2009.
    """
    scores = {}
    for rank, item_id in enumerate(ranked_a, 1):
        scores[item_id] = scores.get(item_id, 0.0) + 1.0 / (k + rank)
    for rank, item_id in enumerate(ranked_b, 1):
        scores[item_id] = scores.get(item_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda x: scores[x], reverse=True)

def cmd_search_hybrid(conn, query, top=5, project_slug=None, since=None, until=None):
    """RRF(FTS5 + vector). Degrades to FTS5 only, and SAYS so, when no query vector exists.

    Both legs are filtered by project/date before the merge. The vector store knows
    neither (E-A24), so its candidates are filtered through the decisions table.
    Provider off is plain FTS5: not degraded, no note. `degraded` (JSON field,
    stdout note) is None | embedder-unreachable | no-embeddings.
    """
    top = int(top)
    filtered = bool(project_slug or since or until)
    fts_ranked = [str(i) for i in _fts_ids(conn, query, project_slug, since, until, top * 3)]

    degraded = None
    q_vec = None
    if _EMBED_PROVIDER != "off":
        q_vec = compute_embedding(query)
        if q_vec is None:
            degraded = "embedder-unreachable"

    vec_ranked = []
    if q_vec is not None:
        vec_results = [r for r in vstore_search(conn, q_vec, top * (10 if filtered else 3))
                       if r[0] == "decisions"]
        if not vec_results:
            degraded = "no-embeddings"
        ranked = [str(sid) for _, sid, _c, _s in
                  sorted(vec_results, key=lambda x: x[3], reverse=True)]
        allowed = _filter_decision_ids(conn, ranked, project_slug, since, until)
        vec_ranked = [sid for sid in ranked if sid in allowed][:top * 3]

    merged = _rrf_merge(fts_ranked, vec_ranked, k=60)[:top] if vec_ranked else fts_ranked[:top]
    rows = _decision_rows(conn, merged)

    if _json_mode:
        print(json.dumps([_decision_json(rows[sid], degraded=degraded)
                          for sid in merged if sid in rows], ensure_ascii=False))
        return
    if degraded:
        _out(f"note: degraded to FTS-only ({_DEGRADED_WHY[degraded]}) — "
             "vector leg skipped; see `osforge-db memory-health`.")
    if not merged:
        _out("Nenhum resultado encontrado.")
        return
    leg = "FTS5" if (degraded or _EMBED_PROVIDER == "off") else "RRF FTS5+vetor"
    _out(f"── Busca hibrida ({leg}): '{query}' (top={top}) ──────────")
    for rank, sid in enumerate(merged, 1):
        r = rows.get(sid)
        if not r:
            continue
        short = textwrap.shorten(r["content"], width=100, placeholder="...")
        _out(f"  #{rank} #{r['id']} [{r['proj']}] [{r['category']}] ({r['created_at'][:10]})  {short}")

_DEGRADED_WHY = {
    "embedder-unreachable": "embedder unreachable",
    "no-embeddings": "no decision embedded yet — run `osforge-db embed-backfill`",
}


def _coverage(conn):
    """(embedded, total) decisions for the ACTIVE model — what embed-backfill would fill."""
    total = conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]
    embedded = conn.execute("""
        SELECT COUNT(*) FROM decisions d WHERE EXISTS (
            SELECT 1 FROM vec_memory v WHERE v.source_table='decisions'
              AND v.source_id=CAST(d.id AS TEXT) AND v.model=?)
    """, (_embed_model(),)).fetchone()[0]
    return embedded, total


def _probe_embedder(timeout=2.0):
    """(reachable: bool|None, reason: str). Cheap: never computes an embedding.
    None = provider off (nothing to reach). ollama → GET /api/tags + model listed;
    voyage/openai → API key present (no network call); mock → always reachable."""
    provider = _EMBED_PROVIDER
    if provider == "off":
        return None, "off"
    if provider == "mock":
        return True, "mock"
    if provider in ("voyage", "openai"):
        key = "VOYAGE_API_KEY" if provider == "voyage" else "OPENAI_API_KEY"
        return (True, provider) if os.environ.get(key) else (False, f"{key} not set")
    if provider != "ollama":
        return False, f"unknown provider '{provider}'"
    try:
        with _urllib_request.urlopen(_OLLAMA_URL + "/api/tags", timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return False, f"ollama not answering at {_OLLAMA_URL}"
    model = _embed_model()
    names = {m.get("name", "") for m in data.get("models", []) if isinstance(m, dict)}
    if not any(n == model or n.startswith(model + ":") for n in names):
        return False, f"model {model} not pulled in ollama (ollama pull {model})"
    return True, f"ollama {model}"


# Below this share of embedded decisions, recall falls back mostly to FTS.
_LOW_COVERAGE = 0.8


def cmd_memory_health(conn, timeout=0.3):
    """One-line hint for the agent when the memory is degraded, else silence.
    Fast by design (session-resume hook): SQLite counts + one short embedder probe."""
    embedded, total = _coverage(conn)
    reachable, reason = _probe_embedder(timeout)
    hint = ""
    if total and reachable is not None:
        if not reachable:
            hint = (f"memory: embedder unreachable ({reason}) — search-hybrid is FTS-only "
                    "until it is back; new decisions are saved without embedding.")
        elif embedded < total * _LOW_COVERAGE:
            hint = (f"memory: {embedded}/{total} decisions embedded — semantic recall is "
                    "partial; run `osforge-db embed-backfill`.")
    if _json_mode:
        print(json.dumps({"provider": _EMBED_PROVIDER, "model": _embed_model(),
                          "embedder_reachable": reachable, "reason": reason,
                          "coverage": {"embedded": embedded, "total": total},
                          "hint": hint or None}, ensure_ascii=False))
        return
    if hint:
        print(hint)


def cmd_vec_status(conn):
    """Imprime provider ativo, backend vetorial, modelo, contagem por source_table.
    Se backend=qdrant, também mostra saúde e total de pontos na coleção.
    """
    _numpy()   # resolve the lazy import before printing: output must not pause mid-report
    provider = _EMBED_PROVIDER
    model    = _embed_model()
    rows = conn.execute("""
        SELECT source_table, model, dim, COUNT(*) as cnt
        FROM vec_memory GROUP BY source_table, model, dim
    """).fetchall()

    # Qdrant health + point count
    qdrant_healthy = None
    qdrant_points  = None
    if _VECTOR_BACKEND == "qdrant":
        st_h, _ = _qdrant_req("GET", "/healthz")
        qdrant_healthy = (st_h == 200)
        st_c, resp_c = _qdrant_req("GET", f"/collections/{_QDRANT_COLLECTION}")
        if st_c == 200 and resp_c:
            try:
                qdrant_points = resp_c["result"]["points_count"]
            except (KeyError, TypeError):
                qdrant_points = None

    embedded, total = _coverage(conn)
    reachable, reason = _probe_embedder()

    if _json_mode:
        out = {
            "provider": provider,
            "model": model,
            "coverage": {"embedded": embedded, "total": total},
            "embedder_reachable": reachable,
            "embedder_reason": reason,
            "vector_backend": _VECTOR_BACKEND,
            "qdrant_url": _QDRANT_URL if _VECTOR_BACKEND == "qdrant" else None,
            "qdrant_collection": _QDRANT_COLLECTION if _VECTOR_BACKEND == "qdrant" else None,
            "qdrant_healthy": qdrant_healthy,
            "qdrant_points": qdrant_points,
            "numpy_available": _numpy() is not None,
            "sqlite_tables": [dict(r) for r in rows],
        }
        print(json.dumps(out, ensure_ascii=False))
        return

    _out("── vec-status ──────────────────────────────────────────────────────")
    _out(f"  provider       : {provider}")
    _out(f"  model          : {model}")
    _out(f"  vector_backend : {_VECTOR_BACKEND}")
    if reachable is None:
        _out("  embedder       : off")
    else:
        reach = {True: "ok", False: "UNREACHABLE"}[reachable]
        _out(f"  embedder       : {reach} ({reason})")
    pct = f" ({100 * embedded // total}%)" if total else ""
    _out(f"  coverage       : {embedded}/{total} decisions embedded{pct}"
         + ("  → run `osforge-db embed-backfill`"
            if reachable is not None and total and embedded < total else ""))
    _out(f"  numpy          : {'sim (acelerador ativo)' if _numpy() is not None else 'nao (pure-Python)'}")
    if _VECTOR_BACKEND == "qdrant":
        _out(f"  qdrant_url     : {_QDRANT_URL}")
        _out(f"  collection     : {_QDRANT_COLLECTION}")
        health_str = "ok" if qdrant_healthy else ("INDISPONÍVEL" if qdrant_healthy is False else "?")
        _out(f"  qdrant_health  : {health_str}")
        pts = str(qdrant_points) if qdrant_points is not None else "?"
        _out(f"  qdrant_points  : {pts}")
    _out("  SQLite vec_memory (cache/fallback):")
    if not rows:
        _out("    (nenhum embedding gravado ainda)")
    else:
        for r in rows:
            _out(f"    {r['source_table']:20s}  model={r['model']}  "
                 f"dim={r['dim']}  count={r['cnt']}")

def cmd_vec_init(conn):
    """Cria/valida coleção Qdrant descobrindo dim via embedding de probe.
    No-op silencioso se backend=sqlite ou provider=off.
    """
    if _VECTOR_BACKEND != "qdrant":
        _out(f"vec-init: backend='{_VECTOR_BACKEND}' — no-op (só relevante para qdrant).")
        return
    if _EMBED_PROVIDER == "off":
        print("[osforge-db] vec-init: OSFORGE_EMBED=off — não é possível descobrir dim.",
              file=sys.stderr)
        return
    _out(f"vec-init: testando conexão com Qdrant em {_QDRANT_URL} ...")
    st_h, _ = _qdrant_req("GET", "/healthz")
    if st_h != 200:
        print(f"[osforge-db] vec-init: Qdrant indisponível (status={st_h}). "
              "Verifique se o container está rodando.", file=sys.stderr)
        return
    _out("  Qdrant: ok")
    _out(f"  Embedando probe para descobrir dim (provider={_EMBED_PROVIDER}, "
         f"model={_embed_model()}) ...")
    probe_vec = compute_embedding("osforge vector store initialization probe")
    if probe_vec is None:
        print("[osforge-db] vec-init: falha ao computar embedding da probe. "
              "Verifique o provider.", file=sys.stderr)
        return
    dim = len(probe_vec)
    _out(f"  dim={dim}")
    # Verificar se coleção já existe
    st_c, resp_c = _qdrant_req("GET", f"/collections/{_QDRANT_COLLECTION}")
    if st_c == 200 and resp_c:
        try:
            existing_dim = resp_c["result"]["config"]["params"]["vectors"]["size"]
            if existing_dim != dim:
                print(f"[osforge-db] vec-init: AVISO — coleção '{_QDRANT_COLLECTION}' "
                      f"já existe com dim={existing_dim}, mas embedder produz dim={dim}. "
                      "Inconsistência — recrie a coleção manualmente se necessário.",
                      file=sys.stderr)
            else:
                _ok(f"vec-init: coleção '{_QDRANT_COLLECTION}' já existe e compatível "
                    f"(dim={dim}).")
        except (KeyError, TypeError):
            _ok(f"vec-init: coleção '{_QDRANT_COLLECTION}' já existe.")
        return
    ok = _qdrant_ensure_collection(dim)
    if ok:
        _ok(f"vec-init: coleção '{_QDRANT_COLLECTION}' criada (dim={dim}, "
            f"distance=Cosine).")
    else:
        print("[osforge-db] vec-init: falha ao criar coleção. Veja avisos acima.",
              file=sys.stderr)


# ── Schema ────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    slug        TEXT    NOT NULL UNIQUE,
    description TEXT    NOT NULL DEFAULT '',
    triage      TEXT    NOT NULL DEFAULT 'standard',
    status      TEXT    NOT NULL DEFAULT 'active',
    stack_json  TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now','utc')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now','utc'))
);

CREATE TABLE IF NOT EXISTS phases (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   INTEGER NOT NULL REFERENCES projects(id),
    name         TEXT    NOT NULL,
    status       TEXT    NOT NULL DEFAULT 'pending',
    skill_path   TEXT,
    artifact_path TEXT,
    started_at   TEXT,
    completed_at TEXT,
    UNIQUE(project_id, name)
);

CREATE TABLE IF NOT EXISTS state (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id    INTEGER NOT NULL UNIQUE REFERENCES projects(id),
    current_phase TEXT,
    resume_point  TEXT,
    plan_approved INTEGER DEFAULT 0,
    plan_approved_at TEXT,
    updated_at    TEXT    NOT NULL DEFAULT (datetime('now','utc'))
);

CREATE TABLE IF NOT EXISTS decisions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    content    TEXT    NOT NULL,
    category   TEXT    NOT NULL DEFAULT 'arch',
    created_at TEXT    NOT NULL DEFAULT (datetime('now','utc'))
);

CREATE VIRTUAL TABLE IF NOT EXISTS decisions_fts
    USING fts5(content, project_slug, category,
               content='decisions', content_rowid='id',
               tokenize='unicode61 remove_diacritics 2');

CREATE TABLE IF NOT EXISTS blockers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  INTEGER NOT NULL REFERENCES projects(id),
    description TEXT    NOT NULL,
    waiting_for TEXT,
    resolved_at TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now','utc'))
);

CREATE TABLE IF NOT EXISTS tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id),
    phase_id   INTEGER REFERENCES phases(id),
    title      TEXT    NOT NULL,
    status     TEXT    NOT NULL DEFAULT 'pending'
               CHECK(status IN ('pending','in-progress','done','blocked','cancelled')),
    wave       INTEGER,
    depends_on TEXT,
    priority   TEXT    NOT NULL DEFAULT 'p1'
               CHECK(priority IN ('p0','p1','p2')),
    created_at TEXT    NOT NULL DEFAULT (datetime('now','utc')),
    updated_at TEXT    NOT NULL DEFAULT (datetime('now','utc'))
);

CREATE TABLE IF NOT EXISTS observations (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project      TEXT    NOT NULL DEFAULT '',
    trigger_text TEXT    NOT NULL,
    context      TEXT    NOT NULL DEFAULT '',
    tool         TEXT    NOT NULL DEFAULT '',
    created_at   TEXT    NOT NULL DEFAULT (datetime('now','utc'))
);

CREATE TABLE IF NOT EXISTS instincts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger     TEXT    NOT NULL,
    guidance    TEXT    NOT NULL DEFAULT '',
    confidence  REAL    NOT NULL DEFAULT 0.5
                CHECK(confidence >= 0.0 AND confidence <= 1.0),
    domain      TEXT    NOT NULL DEFAULT '',
    scope       TEXT    NOT NULL DEFAULT 'project'
                CHECK(scope IN ('project','global')),
    project     TEXT    NOT NULL DEFAULT '',
    seen_count  INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now','utc')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now','utc'))
);

CREATE TABLE IF NOT EXISTS usage (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id    INTEGER NOT NULL REFERENCES projects(id),
    session_id    TEXT    NOT NULL,
    model         TEXT    NOT NULL,
    input_tokens  INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    cache_read    INTEGER NOT NULL DEFAULT 0,
    cache_create  INTEGER NOT NULL DEFAULT 0,
    turns         INTEGER NOT NULL DEFAULT 0,
    updated_at    TEXT    NOT NULL DEFAULT (datetime('now','utc')),
    UNIQUE(project_id, session_id, model)
);

CREATE TABLE IF NOT EXISTS calls (
    message_id    TEXT PRIMARY KEY,            -- assistant message id (dedupes)
    project_id    INTEGER REFERENCES projects(id),
    session_id    TEXT    NOT NULL,
    ts            TEXT    NOT NULL,            -- transcript line timestamp, UTC ISO-8601
    model         TEXT    NOT NULL,
    input         INTEGER NOT NULL DEFAULT 0,
    output        INTEGER NOT NULL DEFAULT 0,
    cache_read    INTEGER NOT NULL DEFAULT 0,
    cache_write_5m INTEGER NOT NULL DEFAULT 0, -- usage.cache_creation.ephemeral_5m_input_tokens
    cache_write_1h INTEGER NOT NULL DEFAULT 0, -- usage.cache_creation.ephemeral_1h_input_tokens
    sidechain     INTEGER NOT NULL DEFAULT 0,  -- isSidechain (subagent)
    stop_reason   TEXT,
    error         TEXT                         -- error TYPE only ("rate_limit", ...), already scrubbed
);
CREATE INDEX IF NOT EXISTS calls_ts ON calls(ts);
CREATE INDEX IF NOT EXISTS calls_project_ts ON calls(project_id, ts);

-- Edit-time quality signals written by hooks/quality-guard.py (B-035, ADR-019).
-- kind: callers_open | duplicate | tests. detail = JSON with paths and names only.
CREATE TABLE IF NOT EXISTS signals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ts          TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    project_id  INTEGER NOT NULL REFERENCES projects(id),
    session_id  TEXT,
    kind        TEXT    NOT NULL CHECK(kind IN ('callers_open','duplicate','tests')),
    subject     TEXT    NOT NULL,
    detail      TEXT    NOT NULL DEFAULT '{}',
    resolved_at TEXT
);
CREATE INDEX IF NOT EXISTS signals_project_open ON signals(project_id, resolved_at);

-- Command centre (B-041/B-042, SPEC-P06): messages to the agents of a project, delivered by the
-- inbox-deliver hook, and what the panel launched (Terminal, background run, IDE).
CREATE TABLE IF NOT EXISTS inbox (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    ts                TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    project_id        INTEGER NOT NULL REFERENCES projects(id),
    text              TEXT    NOT NULL,
    status            TEXT    NOT NULL DEFAULT 'pendente' CHECK(status IN ('pendente','entregue','cancelada')),
    delivered_at      TEXT,
    delivered_session TEXT,
    via               TEXT    NOT NULL DEFAULT 'painel'
);
CREATE INDEX IF NOT EXISTS inbox_project_status ON inbox(project_id, status);
CREATE TABLE IF NOT EXISTS runs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    project_id INTEGER NOT NULL REFERENCES projects(id),
    kind       TEXT    NOT NULL CHECK(kind IN ('terminal','background','ide')),
    tool       TEXT    NOT NULL DEFAULT '',
    prompt     TEXT    NOT NULL DEFAULT '',
    status     TEXT    NOT NULL DEFAULT 'iniciada' CHECK(status IN ('iniciada','rodando','concluida','falhou','interrompida')),
    pid        INTEGER,
    ended_at   TEXT,
    log_path   TEXT,
    result     TEXT,
    cost_usd   REAL
);
CREATE INDEX IF NOT EXISTS runs_project ON runs(project_id, id);

CREATE TABLE IF NOT EXISTS vec_memory (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    source_table TEXT    NOT NULL,
    source_id    TEXT    NOT NULL,
    content      TEXT    NOT NULL,
    dim          INTEGER NOT NULL,
    model        TEXT    NOT NULL,
    embedding    BLOB    NOT NULL,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now','utc')),
    UNIQUE(source_table, source_id, model)
);
"""

TRIGGERS = """
CREATE TRIGGER IF NOT EXISTS decisions_ai AFTER INSERT ON decisions BEGIN
    INSERT INTO decisions_fts(rowid, content, project_slug, category)
    VALUES (new.id, new.content,
            (SELECT slug FROM projects WHERE id = new.project_id),
            new.category);
END;

CREATE TRIGGER IF NOT EXISTS decisions_ad AFTER DELETE ON decisions BEGIN
    INSERT INTO decisions_fts(decisions_fts, rowid, content, project_slug, category)
    VALUES ('delete', old.id, old.content,
            (SELECT slug FROM projects WHERE id = old.project_id),
            old.category);
END;
"""

# Colunas acrescentadas depois do schema inicial: ALTER idempotente (B-018).
_MIGRATIONS = [
    ("projects", "root_path",   "TEXT"),
    ("projects", "remote_hash", "TEXT"),
]

_FTS_DDL = SCHEMA[SCHEMA.index("CREATE VIRTUAL TABLE IF NOT EXISTS decisions_fts"):]
_FTS_DDL = _FTS_DDL[:_FTS_DDL.index(";") + 1]


def _migrate_fts_tokenizer(conn):
    """Rebuild decisions_fts with the accent-insensitive tokenizer when it predates it.

    Idempotent (keyed on the stored DDL) and atomic (one transaction: a failure leaves the
    old index untouched). The index is external-content but `project_slug` is not a column
    of `decisions`, so FTS5 'rebuild' cannot be used: rows are re-inserted from a join."""
    row = conn.execute("SELECT sql FROM sqlite_master WHERE name='decisions_fts'").fetchone()
    if row is None or "remove_diacritics" in (row[0] or ""):
        return
    conn.commit()
    try:
        conn.execute("BEGIN IMMEDIATE")
        # Re-check under the write lock: a concurrent process may have migrated meanwhile.
        cur = conn.execute("SELECT sql FROM sqlite_master WHERE name='decisions_fts'").fetchone()
        if cur is None or "remove_diacritics" in (cur[0] or ""):
            conn.execute("COMMIT")
            return
        conn.execute("DROP TABLE decisions_fts")
        conn.execute(_FTS_DDL)
        conn.execute("""
            INSERT INTO decisions_fts(rowid, content, project_slug, category)
            SELECT d.id, d.content, p.slug, d.category
            FROM decisions d LEFT JOIN projects p ON p.id = d.project_id
        """)
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def migrate(conn):
    for table, col, typ in _MIGRATIONS:
        cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if col not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
    conn.commit()
    _migrate_fts_tokenizer(conn)


def cmd_init(conn, args):
    conn.executescript(SCHEMA)
    conn.executescript(TRIGGERS)
    migrate(conn)
    conn.commit()
    _ok("Schema criado/verificado com sucesso")
    _ok(f"Banco: {db_path(_scope(args))}")

# ── Helpers de output ─────────────────────────────────────────────────────

_json_mode = False

def _ok(msg):
    if not _json_mode:
        print(f"✅ {msg}")

def _out(msg):
    if not _json_mode:
        print(msg)

def _err(msg):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)

def _scope(args):
    for a in args:
        if a.startswith("--scope="):
            return a.split("=", 1)[1]
    return "global"

def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _get_project(conn, slug):
    row = conn.execute("SELECT * FROM projects WHERE slug=?", (slug,)).fetchone()
    if not row:
        _err(f"Projeto '{slug}' não encontrado. Use 'upsert-project' para criar.")
    return row

# ── Comandos ──────────────────────────────────────────────────────────────

def cmd_upsert_project(conn, slug, desc, triage="standard", status="active"):
    conn.execute("""
        INSERT INTO projects (slug, description, triage, status)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            description = excluded.description,
            triage      = excluded.triage,
            status      = excluded.status,
            updated_at  = datetime('now','utc')
    """, (slug, desc, triage, status))
    pid = conn.execute("SELECT id FROM projects WHERE slug=?", (slug,)).fetchone()[0]
    conn.execute("""
        INSERT OR IGNORE INTO state (project_id) VALUES (?)
    """, (pid,))
    conn.commit()
    _ok(f"Projeto '{slug}' ({triage}/{status}) salvo")

def _git_out(args, cwd):
    import subprocess
    try:
        r = subprocess.run(["git", "-C", cwd] + args, capture_output=True, text=True, timeout=3, check=False)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""

def _normalize_remote(url):
    """Mesmo algoritmo de hooks/lib/project_id.py (mantido em sincronia; testado)."""
    import re
    u = (url or "").strip()
    if not u:
        return ""
    u = re.sub(r"^[a-z+]+://", "", u)
    u = re.sub(r"^[^@/]+@", "", u)
    u = u.replace(":", "/", 1) if re.match(r"^[^/]+:[^/]", u) else u
    return re.sub(r"\.git/?$", "", u).rstrip("/").lower()

def _remote_hash(url):
    n = _normalize_remote(url)
    return hashlib.sha256(n.encode("utf-8")).hexdigest()[:16] if n else ""

def _slugify(name):
    """Mesmo algoritmo de hooks/lib/project_id.py:slugify (mantido em sincronia; testado)."""
    return re.sub(r"[^a-z0-9-]+", "-", (name or "").lower().replace("_", "-")).strip("-")

def _resolve_root(root_arg):
    """--root=. → raiz git do cwd (repo principal no caso de worktree); caminho → realpath."""
    if not root_arg:
        return None
    cwd = os.getcwd() if root_arg == "." else os.path.expanduser(root_arg)
    top = _git_out(["rev-parse", "--show-toplevel"], cwd)
    if top:
        common = _git_out(["rev-parse", "--path-format=absolute", "--git-common-dir"], cwd)
        if common and os.path.basename(common) == ".git":
            return os.path.realpath(os.path.dirname(common))
        return os.path.realpath(top)
    return os.path.realpath(cwd)

def cmd_bind_project(conn, slug, root_arg=None, remote_arg=None):
    p = _get_project(conn, slug)
    root = _resolve_root(root_arg)
    rh = None
    if remote_arg:
        url = _git_out(["config", "--get", "remote.origin.url"], root or os.getcwd()) if remote_arg == "auto" else remote_arg
        rh = _remote_hash(url) or None
    if root is None and rh is None:
        _err("Uso: bind-project <slug> [--root=DIR|.] [--remote=URL|auto]")
    if root is not None:
        conn.execute("UPDATE projects SET root_path=?, updated_at=datetime('now','utc') WHERE id=?", (root, p["id"]))
    if rh is not None:
        conn.execute("UPDATE projects SET remote_hash=?, updated_at=datetime('now','utc') WHERE id=?", (rh, p["id"]))
    conn.commit()
    _ok(f"Projeto '{slug}' amarrado: root={root or '(mantido)'} remote_hash={rh or '(mantido)'}")

def cmd_set_phase(conn, slug, phase_name, status,
                  skill_path=None, artifact_path=None):
    p = _get_project(conn, slug)
    now = _now()
    started  = now if status == "in-progress" else None
    completed = now if status in ("complete", "skipped", "cancelled") else None
    conn.execute("""
        INSERT INTO phases (project_id, name, status, skill_path,
                            artifact_path, started_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(project_id, name) DO UPDATE SET
            status        = excluded.status,
            skill_path    = COALESCE(excluded.skill_path, skill_path),
            artifact_path = COALESCE(excluded.artifact_path, artifact_path),
            started_at    = COALESCE(excluded.started_at, started_at),
            completed_at  = excluded.completed_at
    """, (p["id"], phase_name, status, skill_path, artifact_path,
          started, completed))
    if status == "in-progress":
        conn.execute("""
            UPDATE state SET current_phase=?, updated_at=?
            WHERE project_id=?
        """, (phase_name, now, p["id"]))
    conn.commit()
    _ok(f"Fase '{phase_name}' → {status}")

def cmd_set_resume(conn, slug, resume_point):
    p = _get_project(conn, slug)
    conn.execute("""
        UPDATE state SET resume_point=?, updated_at=?
        WHERE project_id=?
    """, (resume_point, _now(), p["id"]))
    conn.commit()
    _ok(f"Resume point salvo para '{slug}'")

def cmd_add_decision(conn, slug, content, category="arch", scope="global"):
    p = _get_project(conn, slug)
    cur = conn.execute("""
        INSERT INTO decisions (project_id, content, category)
        VALUES (?, ?, ?) RETURNING id
    """, (p["id"], content, category)).fetchone()
    conn.execute("UPDATE projects SET updated_at=? WHERE id=?",
                 (_now(), p["id"]))
    conn.commit()
    _ok(f"Decisão ({category}) adicionada a '{slug}'")
    if cur is None:
        return
    _auto_embed_decision(conn, cur[0], content)
    if scope == "global":           # local-scope ids would collide in the one global brain
        _brain_remember_decision(cur[0], slug, content, category)


def _auto_embed_decision(conn, decision_id, content):
    """Legacy vector memory (vec_memory / osforge_memory): best-effort, never fails the write."""
    if _EMBED_PROVIDER == "off":
        return
    try:
        vec = compute_embedding(content)
        if vec is not None:
            upsert_vec_memory(conn, "decisions", str(decision_id), content, vec)
            return
        why = "embedder unavailable"
    except Exception as _auto_embed_exc:
        why = f"auto-embed failed ({_auto_embed_exc})"
    print(f"[osforge-db] warning: decision #{decision_id} saved WITHOUT embedding ({why}); "
          "run `osforge-db embed-backfill` when the embedder is back.", file=sys.stderr)


def _brain_remember_decision(decision_id, slug, content, category):
    """Brain copy of a decision (kind=decision): best-effort. The SQLite row is already
    committed; any brain failure prints ONE line and never changes the exit code."""
    if not _brain.enabled():
        return
    try:
        _rec, indexed, why = _brain.remember(content, "decision", slug, [category],
                                             f"add-decision:{decision_id}")
    except Exception as e:      # journal unwritable, scrub missing: nothing journaled
        _out(f"note: brain skipped decision #{decision_id} ({e}) — run `osforge-db brain migrate` later")
        return
    if not indexed:
        _out(f"note: brain degraded ({why}) — decision #{decision_id} journaled, "
             "not indexed; run `osforge-db brain rebuild` later")


def cmd_add_blocker(conn, slug, description, waiting_for=None):
    p = _get_project(conn, slug)
    cur = conn.execute("""
        INSERT INTO blockers (project_id, description, waiting_for)
        VALUES (?, ?, ?) RETURNING id
    """, (p["id"], description, waiting_for)).fetchone()
    conn.commit()
    _ok(f"Blocker #{cur[0]} adicionado a '{slug}'")
    return cur[0]

def cmd_resolve_blocker(conn, slug, blocker_id):
    p = _get_project(conn, slug)
    conn.execute("""
        UPDATE blockers SET resolved_at=?
        WHERE id=? AND project_id=?
    """, (_now(), blocker_id, p["id"]))
    conn.commit()
    _ok(f"Blocker #{blocker_id} resolvido")

def cmd_status(conn, slug):
    """Retorna estado completo do projeto — para INTAKE do orchestrator."""
    p = _get_project(conn, slug)
    st = conn.execute("SELECT * FROM state WHERE project_id=?",
                      (p["id"],)).fetchone()
    phases = conn.execute("""
        SELECT name, status, skill_path, artifact_path,
               started_at, completed_at
        FROM phases WHERE project_id=? ORDER BY id
    """, (p["id"],)).fetchall()
    blockers = conn.execute("""
        SELECT id, description, waiting_for FROM blockers
        WHERE project_id=? AND resolved_at IS NULL
    """, (p["id"],)).fetchall()
    decisions_recent = conn.execute("""
        SELECT category, content, created_at FROM decisions
        WHERE project_id=? ORDER BY created_at DESC LIMIT 5
    """, (p["id"],)).fetchall()

    if _json_mode:
        data = {
            "project": dict(p),
            "state": dict(st) if st else {},
            "phases": [dict(r) for r in phases],
            "blockers": [dict(r) for r in blockers],
            "recent_decisions": [dict(r) for r in decisions_recent],
        }
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    _out(f"── Projeto: {p['slug']} ({p['triage']}) ──────────────────────")
    _out(f"Status:  {p['status']}")
    _out(f"Desc:    {p['description']}")
    if st:
        _out(f"Fase atual:    {st['current_phase'] or '–'}")
        _out(f"Resume point:  {st['resume_point'] or '–'}")
        _out(f"Plano aprovado: {'sim' if st['plan_approved'] else 'não'}")
    _out("")
    if phases:
        _out("Fases:")
        for ph in phases:
            icon = {"complete":"✅","in-progress":"🔄","pending":"○",
                    "blocked":"🔴","skipped":"–","cancelled":"✗"}.get(ph["status"],"?")
            _out(f"  {icon} {ph['name']}"
                 + (f" [{ph['artifact_path']}]" if ph["artifact_path"] else ""))
    if blockers:
        _out(f"\nBlockers ativos ({len(blockers)}):")
        for b in blockers:
            _out(f"  #{b['id']} {b['description']}"
                 + (f" — esperando: {b['waiting_for']}" if b["waiting_for"] else ""))
    if decisions_recent:
        _out(f"\nDecisões recentes:")
        for d in decisions_recent:
            short = textwrap.shorten(d["content"], width=80, placeholder="…")
            _out(f"  [{d['category']}] {short}")

def cmd_resume(conn, slug):
    """Output mínimo para shell injection — só o resume point."""
    p = _get_project(conn, slug)
    st = conn.execute("SELECT current_phase, resume_point FROM state WHERE project_id=?",
                      (p["id"],)).fetchone()
    if not st:
        _out("sem estado registrado")
        return
    phase = st["current_phase"] or "–"
    resume = st["resume_point"] or "–"
    _out(f"fase={phase} | resume={resume}")

def cmd_list_blockers(conn, slug):
    p = _get_project(conn, slug)
    rows = conn.execute("""
        SELECT id, description, waiting_for, created_at FROM blockers
        WHERE project_id=? AND resolved_at IS NULL ORDER BY id
    """, (p["id"],)).fetchall()
    if _json_mode:
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False))
        return
    if not rows:
        _out("Sem blockers ativos")
        return
    for r in rows:
        _out(f"#{r['id']} [{r['created_at'][:10]}] {r['description']}"
             + (f"\n   → esperando: {r['waiting_for']}" if r["waiting_for"] else ""))

def cmd_list_decisions(conn, slug, category=None, limit=10, since=None, until=None):
    p = _get_project(conn, slug)
    flt, params = _decision_filters(None, since, until)
    q = ("SELECT d.id, p.slug AS proj, d.category, d.content, d.created_at "
         "FROM decisions d JOIN projects p ON p.id = d.project_id WHERE d.project_id=?" + flt)
    params = [p["id"]] + params
    if category:
        q += " AND d.category=?"
        params.append(category)
    q += " ORDER BY d.created_at DESC LIMIT ?"
    params.append(int(limit))
    rows = conn.execute(q, params).fetchall()
    if _json_mode:
        print(json.dumps([_decision_json(r) for r in rows], ensure_ascii=False))
        return
    for r in rows:
        _out(f"#{r['id']} [{r['category']}] ({r['created_at'][:10]}) {r['content']}")

TASK_STATUSES = ("pending", "in-progress", "done", "blocked", "cancelled")
TASK_PRIORITIES = ("p0", "p1", "p2")

def _resolve_phase_id(conn, project_id, phase_name):
    """Resolve um phase_id por nome dentro do projeto. Erro claro se não existir."""
    row = conn.execute(
        "SELECT id FROM phases WHERE project_id=? AND name=?",
        (project_id, phase_name)).fetchone()
    if not row:
        _err(f"Fase '{phase_name}' não encontrada no projeto. "
             "Crie-a com 'set-phase' antes de vincular a task.")
    return row["id"]

def cmd_add_task(conn, slug, title, phase_name=None, wave=None,
                 depends=None, priority="p1"):
    p = _get_project(conn, slug)
    if priority not in TASK_PRIORITIES:
        _err(f"Prioridade inválida: '{priority}'. Use: {', '.join(TASK_PRIORITIES)}")
    phase_id = _resolve_phase_id(conn, p["id"], phase_name) if phase_name else None
    wave_val = None
    if wave is not None:
        try:
            wave_val = int(wave)
        except ValueError:
            _err(f"Wave inválida: '{wave}'. Use um inteiro.")
    now = _now()
    cur = conn.execute("""
        INSERT INTO tasks (project_id, phase_id, title, status, wave,
                           depends_on, priority, created_at, updated_at)
        VALUES (?, ?, ?, 'pending', ?, ?, ?, ?, ?) RETURNING id
    """, (p["id"], phase_id, title, wave_val, depends, priority, now, now)).fetchone()
    conn.commit()
    _ok(f"Task #{cur[0]} criada em '{slug}' ({priority})")
    if _json_mode:
        print(json.dumps({"id": cur[0]}, ensure_ascii=False))
    return cur[0]

def cmd_set_task(conn, slug, task_id, status):
    p = _get_project(conn, slug)
    if status not in TASK_STATUSES:
        _err(f"Status inválido: '{status}'. Use: {', '.join(TASK_STATUSES)}")
    try:
        tid = int(task_id)
    except ValueError:
        _err(f"task_id inválido: '{task_id}'. Use um inteiro.")
    cur = conn.execute("""
        UPDATE tasks SET status=?, updated_at=?
        WHERE id=? AND project_id=?
    """, (status, _now(), tid, p["id"]))
    conn.commit()
    if cur.rowcount == 0:
        _err(f"Task #{tid} não encontrada no projeto '{slug}'.")
    _ok(f"Task #{tid} → {status}")

def cmd_list_tasks(conn, slug, status=None):
    p = _get_project(conn, slug)
    q = ("SELECT id, status, priority, wave, depends_on, title "
         "FROM tasks WHERE project_id=?")
    params = [p["id"]]
    if status:
        if status not in TASK_STATUSES:
            _err(f"Status inválido: '{status}'. Use: {', '.join(TASK_STATUSES)}")
        q += " AND status=?"
        params.append(status)
    q += " ORDER BY id"
    rows = conn.execute(q, params).fetchall()
    if _json_mode:
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False))
        return
    if not rows:
        _out("Sem tasks")
        return
    for r in rows:
        wave = f" wave:{r['wave']}" if r["wave"] is not None else ""
        deps = f" (deps: {r['depends_on']})" if r["depends_on"] else ""
        _out(f"  [{r['id']}] {r['status']:11} {r['priority']}{wave} {r['title']}{deps}")

# Ordem de exibição de status no board
_BOARD_ORDER = ("in-progress", "blocked", "pending", "done")

def cmd_board(conn, status="active"):
    """Visão cross-project de tasks, agrupadas por status por projeto."""
    if status == "all":
        projects = conn.execute(
            "SELECT id, slug FROM projects ORDER BY slug").fetchall()
    else:
        projects = conn.execute(
            "SELECT id, slug FROM projects WHERE status=? ORDER BY slug",
            (status,)).fetchall()

    if _json_mode:
        out = {}
        for proj in projects:
            tasks = conn.execute(
                "SELECT id, status, priority, wave, depends_on, title "
                "FROM tasks WHERE project_id=? ORDER BY id",
                (proj["id"],)).fetchall()
            out[proj["slug"]] = {"tasks": [dict(t) for t in tasks], "usage": _usage_totals(conn, proj["id"])}
        print(json.dumps(out, ensure_ascii=False))
        return

    if not projects:
        _out("Nenhum projeto")
        return

    for proj in projects:
        tasks = conn.execute(
            "SELECT id, status, priority, wave, title "
            "FROM tasks WHERE project_id=? ORDER BY id",
            (proj["id"],)).fetchall()
        tot = _usage_totals(conn, proj["id"])
        usage_note = f"  ({tot['total']:,} tokens em {tot['sessions']} sessão(ões))" if tot["sessions"] else ""
        if not tasks:
            _out(f"{proj['slug']}: sem tasks{usage_note}")
            continue
        by_status = {s: [] for s in _BOARD_ORDER}
        for t in tasks:
            by_status.setdefault(t["status"], []).append(t)
        _out(f"{proj['slug']}:{usage_note}")
        for s in _BOARD_ORDER:
            group = by_status.get(s) or []
            if s == "done":
                group = group[-3:]  # só as 3 últimas done
            for t in group:
                wave = f" wave:{t['wave']}" if t["wave"] is not None else ""
                _out(f"  [{s:11}] #{t['id']} {t['priority']}{wave} {t['title']}")

# ── Lexical query building + shared decision filters ───────────────────────

# pt-BR + English function words, plus words every decision shares ("decidimos", "decided").
# Compared accent-folded, so "não" and "nao" are the same entry.
# Stopwords, folding and the term list live in osforge_brain (one builder for the FTS
# query here and for the brain's lexical fallback).
_STOPWORDS = _brain.STOPWORDS
_fold = _brain.fold


def _fts_quote(query):
    """Natural-language query → FTS5 MATCH expression, or None when it has no word at all.

    Words only (unicode-aware), each one quoted (so `-`, `:`, `*`, NEAR, AND/OR/NOT are
    never operators) and OR-ed: a question matches on its content words, bm25 ranks.
    Stopwords and words under 3 characters are dropped; if that leaves nothing, the raw
    words are used (so "UI" alone still searches for "ui").
    """
    terms = _brain.query_terms(query)
    if not terms:
        return None
    return " OR ".join(f'"{t}"' for t in terms)


def _parse_day(value, flag):
    """'YYYY-MM-DD' → the same string; anything else is a usage error (never ignored)."""
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except (TypeError, ValueError):
        _err(f"{flag} expects YYYY-MM-DD, got {value!r}")
    return value


def _decision_filters(project_slug=None, since=None, until=None):
    """SQL fragment (starting with AND) + params over aliases d (decisions) and p (projects).
    since/until are inclusive days; created_at is 'YYYY-MM-DD HH:MM:SS' (UTC)."""
    sql, params = "", []
    if project_slug:
        sql += " AND p.slug = ?"
        params.append(project_slug)
    if since:
        sql += " AND d.created_at >= ?"
        params.append(since)
    if until:
        nxt = datetime.strptime(until, "%Y-%m-%d") + timedelta(days=1)
        sql += " AND d.created_at < ?"
        params.append(nxt.strftime("%Y-%m-%d"))
    return sql, params


def _fts_ids(conn, query, project_slug=None, since=None, until=None, limit=5):
    """Decision ids for `query`, best bm25 first, filters applied inside the query."""
    match = _fts_quote(query)
    if match is None:
        return []
    flt, params = _decision_filters(project_slug, since, until)
    try:
        rows = conn.execute(f"""
            SELECT d.id FROM decisions_fts f
            JOIN decisions d ON d.id = f.rowid
            JOIN projects  p ON p.id = d.project_id
            WHERE decisions_fts MATCH ? {flt}
            ORDER BY bm25(decisions_fts) LIMIT ?
        """, [match] + params + [int(limit)]).fetchall()
    except sqlite3.OperationalError as exc:      # defensive: the query is built to be valid
        print(f"[osforge-db] warning: FTS5 rejected the query ({exc})", file=sys.stderr)
        return []
    return [r[0] for r in rows]


def _filter_decision_ids(conn, ids, project_slug=None, since=None, until=None):
    """Subset of `ids` (str) that are existing decisions passing the filters."""
    nums = [int(i) for i in ids if str(i).isdigit()]
    if not nums:
        return set()
    flt, params = _decision_filters(project_slug, since, until)
    ph = ",".join("?" * len(nums))
    return {str(r[0]) for r in conn.execute(
        f"SELECT d.id FROM decisions d JOIN projects p ON p.id = d.project_id "
        f"WHERE d.id IN ({ph}) {flt}", nums + params).fetchall()}


def _decision_rows(conn, ids):
    """{id_str: row(id, proj, category, created_at, content)} for the given ids."""
    nums = [int(i) for i in ids if str(i).isdigit()]
    if not nums:
        return {}
    ph = ",".join("?" * len(nums))
    rows = conn.execute(
        f"SELECT d.id, p.slug AS proj, d.category, d.created_at, d.content "
        f"FROM decisions d JOIN projects p ON p.id = d.project_id WHERE d.id IN ({ph})",
        nums).fetchall()
    return {str(r["id"]): r for r in rows}


def _decision_json(r, **extra):
    """One decision as JSON — the same keys in search, search-hybrid and list-decisions."""
    out = {"id": r["id"], "project": r["proj"], "category": r["category"],
           "created_at": r["created_at"], "content": r["content"]}
    out.update(extra)
    return out


def cmd_search(conn, query, project_slug=None, limit=5, since=None, until=None):
    ids = [str(i) for i in _fts_ids(conn, query, project_slug, since, until, limit)]
    rows = _decision_rows(conn, ids)
    if _json_mode:
        # `slug` kept as an alias of `project` for callers of the old shape
        print(json.dumps([_decision_json(rows[i], slug=rows[i]["proj"]) for i in ids if i in rows],
                         ensure_ascii=False))
        return
    if not ids:
        _out("Nenhum resultado")
        return
    for i in ids:
        r = rows[i]
        short = textwrap.shorten(r["content"], width=100, placeholder="…")
        _out(f"#{r['id']} [{r['proj']}][{r['category']}] ({r['created_at'][:10]}) {short}")

def cmd_list_projects(conn, status="active"):
    q = "SELECT slug, triage, status, description, root_path, remote_hash FROM projects"
    if status != "all":
        q += " WHERE status=?"
        rows = conn.execute(q, (status,)).fetchall()
    else:
        rows = conn.execute(q).fetchall()
    if _json_mode:
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False))
        return
    for r in rows:
        desc = textwrap.shorten(r["description"], width=60, placeholder="…")
        _out(f"  [{r['status']:8}] {r['slug']:30} ({r['triage']})  {desc}")

def cmd_stats(conn):
    projects = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    active   = conn.execute("SELECT COUNT(*) FROM projects WHERE status='active'").fetchone()[0]
    phases   = conn.execute("SELECT COUNT(*) FROM phases").fetchone()[0]
    done     = conn.execute("SELECT COUNT(*) FROM phases WHERE status='complete'").fetchone()[0]
    decs     = conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]
    blk      = conn.execute("SELECT COUNT(*) FROM blockers WHERE resolved_at IS NULL").fetchone()[0]
    _out(f"Projetos: {projects} total / {active} ativos")
    _out(f"Fases:    {phases} total / {done} completas")
    _out(f"Decisões: {decs}")
    _out(f"Blockers: {blk} ativos")
    u = conn.execute("SELECT COALESCE(SUM(input_tokens+output_tokens+cache_read+cache_create),0), COUNT(DISTINCT session_id) FROM usage").fetchone()
    _out(f"Tokens: {u[0]:,} em {u[1]} sessão(ões) registradas")

def cmd_add_usage(conn, slug, session_id, model, inp, out, cread, ccreate, turns):
    """Upsert (não soma): o Stop hook recomputa a sessão inteira a cada chamada (B-022)."""
    p = _get_project(conn, slug)
    conn.execute("""
        INSERT INTO usage (project_id, session_id, model, input_tokens, output_tokens, cache_read, cache_create, turns)
        VALUES (?,?,?,?,?,?,?,?)
        ON CONFLICT(project_id, session_id, model) DO UPDATE SET
            input_tokens=excluded.input_tokens, output_tokens=excluded.output_tokens,
            cache_read=excluded.cache_read, cache_create=excluded.cache_create,
            turns=excluded.turns, updated_at=datetime('now','utc')
    """, (p["id"], session_id, model, int(inp), int(out), int(cread), int(ccreate), int(turns)))
    conn.commit()
    _ok(f"usage '{slug}' sessão {session_id[:12]} {model}: in={inp} out={out} cache_read={cread} cache_create={ccreate}")

def _usage_totals(conn, project_id):
    r = conn.execute("""SELECT COALESCE(SUM(input_tokens),0) i, COALESCE(SUM(output_tokens),0) o,
                        COALESCE(SUM(cache_read),0) cr, COALESCE(SUM(cache_create),0) cc,
                        COUNT(DISTINCT session_id) s FROM usage WHERE project_id=?""", (project_id,)).fetchone()
    return {"input": r["i"], "output": r["o"], "cache_read": r["cr"], "cache_create": r["cc"], "sessions": r["s"],
            "total": r["i"] + r["o"] + r["cr"] + r["cc"]}

def cmd_usage(conn, slug):
    p = _get_project(conn, slug)
    rows = conn.execute("""SELECT session_id, model, input_tokens, output_tokens, cache_read, cache_create, turns, updated_at
                           FROM usage WHERE project_id=? ORDER BY updated_at""", (p["id"],)).fetchall()
    tot = _usage_totals(conn, p["id"])
    if _json_mode:
        print(json.dumps({"sessions": [dict(r) for r in rows], "totals": tot}, ensure_ascii=False))
        return
    if not rows:
        _out("Sem uso registrado"); return
    for r in rows:
        _out(f"  {r['updated_at']}  {r['session_id'][:12]:12}  {r['model']:28} in={r['input_tokens']:>8} out={r['output_tokens']:>7} "
             f"cache_read={r['cache_read']:>9} cache_create={r['cache_create']:>8} turns={r['turns']}")
    _out(f"  total: {tot['total']:,} tokens em {tot['sessions']} sessão(ões) "
         f"(in {tot['input']:,} · out {tot['output']:,} · cache_read {tot['cache_read']:,} · cache_create {tot['cache_create']:,})")


# ── B-028: auditoria por chamada (calls) ──────────────────────────────────────
# Diferente de `usage` (upsert por sessão inteira): aqui é append-only, uma linha por
# message.id, nunca duplica (ON CONFLICT DO NOTHING). Custo nunca é armazenado — é
# recalculado na consulta a partir de claude-code/pricing.json (corrigir o arquivo
# corrige o histórico todo).

def _pricing_path():
    """Ordem: OSFORGE_PRICING → caminho de dev (sibling deste script) → deploy
    (~/.claude/pricing.json) → âncora ~/.osforge/repo-path. None se nada resolver
    (degrada para todo modelo sem preço, nunca falha)."""
    override = os.environ.get("OSFORGE_PRICING")
    if override:
        return override if os.path.isfile(override) else None
    here = os.path.dirname(os.path.abspath(__file__))
    dev_path = os.path.normpath(os.path.join(here, "..", "claude-code", "pricing.json"))
    if os.path.isfile(dev_path):
        return dev_path
    deployed = os.path.expanduser("~/.claude/pricing.json")
    if os.path.isfile(deployed):
        return deployed
    anchor = os.path.expanduser("~/.osforge/repo-path")
    try:
        with open(anchor, encoding="utf-8") as f:
            cand = os.path.join(f.read().strip(), "claude-code", "pricing.json")
        if os.path.isfile(cand):
            return cand
    except OSError:
        pass
    return None

def _load_pricing():
    path = _pricing_path()
    if not path:
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        models = data.get("models")
        return models if isinstance(models, dict) else {}
    except (OSError, ValueError):
        return {}

def _price_for_model(models, model):
    """Longest-prefix match; None quando nenhum prefixo casa (modelo sem preço)."""
    best = None
    for prefix, price in models.items():
        if model.startswith(prefix) and (best is None or len(prefix) > len(best[0])):
            best = (prefix, price)
    return best[1] if best else None

def _cost_usd(price, row):
    if not price:
        return 0.0
    total = 0.0
    for field in ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h"):
        total += (row[field] or 0) * float(price.get(field, 0) or 0) / 1_000_000
    return total

def _row_from_entry(e, msg, u, session_id):
    """Constrói uma linha de `calls` a partir de uma entrada de transcript já sabida ter
    message.usage (mesmo formato que hooks/session-save.py:_build_call_row — duplicado por
    design, ver _normalize_remote acima). None quando falta timestamp ou message.id (ambos
    NOT NULL no schema)."""
    ts = e.get("timestamp")
    if not isinstance(ts, str) or not ts:
        return None
    mid = msg.get("id") or e.get("uuid")
    if not mid:
        return None
    cache_creation = u.get("cache_creation")
    if isinstance(cache_creation, dict):
        cw5 = cache_creation.get("ephemeral_5m_input_tokens") or 0
        cw1h = cache_creation.get("ephemeral_1h_input_tokens") or 0
    else:
        cw5 = u.get("cache_creation_input_tokens") or 0
        cw1h = 0
    error = None
    if e.get("isApiErrorMessage"):
        error = e.get("error") or "unknown"
    return {
        "message_id": str(mid), "session_id": session_id or "", "ts": ts,
        "model": str(msg.get("model") or "unknown"),
        "input": int(u.get("input_tokens") or 0), "output": int(u.get("output_tokens") or 0),
        "cache_read": int(u.get("cache_read_input_tokens") or 0),
        "cache_write_5m": int(cw5), "cache_write_1h": int(cw1h),
        "sidechain": 1 if e.get("isSidechain") else 0,
        "stop_reason": msg.get("stop_reason"), "error": error,
    }

def _insert_calls_rows(conn, project_id, rows):
    for r in rows:
        conn.execute("""
            INSERT INTO calls (message_id, project_id, session_id, ts, model, input, output,
                                cache_read, cache_write_5m, cache_write_1h, sidechain, stop_reason, error)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(message_id) DO NOTHING
        """, (str(r.get("message_id")), project_id, str(r.get("session_id") or ""), str(r.get("ts")),
              str(r.get("model") or "unknown"), int(r.get("input") or 0), int(r.get("output") or 0),
              int(r.get("cache_read") or 0), int(r.get("cache_write_5m") or 0), int(r.get("cache_write_1h") or 0),
              1 if r.get("sidechain") else 0, r.get("stop_reason"), r.get("error")))
    conn.commit()

def cmd_add_calls(conn, slug):
    """Lê JSONL do stdin (uma linha por chamada) e insere em `calls`; resolve project_id
    UMA vez para o lote inteiro. Chamado pelo session-save.py com --stdin (B-028)."""
    p = _get_project(conn, slug)
    rows = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(r, dict) and r.get("message_id") and r.get("ts"):
            rows.append(r)
    _insert_calls_rows(conn, p["id"], rows)
    _ok(f"calls '{slug}': {len(rows)} linha(s) processada(s)")

def _parse_since(s):
    """'5h'|'24h'|'7d' → cutoff relativo a agora; 'AAAA-MM-DD' → aquela data 00:00 UTC.
    None (formato desconhecido) → sem filtro de data."""
    if not s:
        return None
    m = re.match(r"^(\d+)([hd])$", s)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        delta = timedelta(hours=n) if unit == "h" else timedelta(days=n)
        return (datetime.now(timezone.utc) - delta).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        d = datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return d.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None

def cmd_calls(conn, proj_flt=None, since_flt=None, by_flt=None):
    """Tokens/custo por model|session|day|sidechain (--by, padrão model), com filtro opcional
    de projeto e janela (--since). Custo = 'custo equivalente de API', calculado agora a
    partir de pricing.json — nunca armazenado (B-028)."""
    where, params = [], []
    if proj_flt:
        p = _get_project(conn, proj_flt)
        where.append("project_id=?"); params.append(p["id"])
    cutoff = _parse_since(since_flt)
    if cutoff:
        where.append("ts>=?"); params.append(cutoff)
    clause = ("WHERE " + " AND ".join(where)) if where else ""
    rows = conn.execute(f"SELECT * FROM calls {clause} ORDER BY ts", params).fetchall()

    models = _load_pricing()
    key_fn = {
        "model":     lambda r: r["model"],
        "session":   lambda r: r["session_id"],
        "day":       lambda r: (r["ts"] or "")[:10],
        "sidechain": lambda r: "sidechain" if r["sidechain"] else "main",
    }.get(by_flt or "model", lambda r: r["model"])

    groups = {}
    priceless = {}
    for r in rows:
        key = key_fn(r)
        g = groups.setdefault(key, {"calls": 0, "input": 0, "output": 0, "cache_read": 0,
                                     "cache_write_5m": 0, "cache_write_1h": 0, "cost_usd": 0.0})
        g["calls"] += 1
        for f in ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h"):
            g[f] += r[f]
        price = _price_for_model(models, r["model"])
        if price is None:
            priceless[r["model"]] = priceless.get(r["model"], 0) + 1
        else:
            g["cost_usd"] += _cost_usd(price, r)

    if _json_mode:
        print(json.dumps({"groups": [{"key": k, **v} for k, v in groups.items()],
                           "priceless": priceless}, ensure_ascii=False))
        return
    if not rows:
        _out("Sem chamadas registradas"); return
    for k, v in groups.items():
        _out(f"  {str(k):28} calls={v['calls']:>6} in={v['input']:>9,} out={v['output']:>8,} "
             f"cache_read={v['cache_read']:>10,} custo equivalente de API=US$ {v['cost_usd']:.4f}")
    for model, n in priceless.items():
        _out(f"  sem preço: {n} chamadas de {model}")

def cmd_prune_calls(conn, older_than):
    """DELETE FROM calls WHERE ts < cutoff — janela de retenção (padrão chamado pelo
    session-save.py no máximo uma vez por dia; B-028)."""
    m = re.match(r"^(\d+)d$", older_than or "")
    if not m:
        _err("Uso: prune-calls --older-than=90d")
    days = int(m.group(1))
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = conn.execute("DELETE FROM calls WHERE ts<?", (cutoff,))
    # Signals share the retention window; open ones are kept whatever their age (B-035).
    sig = conn.execute("DELETE FROM signals WHERE ts<? AND resolved_at IS NOT NULL", (cutoff,))
    conn.commit()
    _ok(f"prune-calls: {cur.rowcount} linha(s) removida(s) (mais antigas que {days}d); "
        f"{sig.rowcount} sinal(is) resolvido(s) removido(s)")

# ── Project lifecycle (ADR-019) ─────────────────────────────────────────────

PROJECT_STATUSES = ("active", "backlog", "paused", "done", "archived")


def _err2(msg):
    """Usage/lookup error with exit 2 (the monitor contract distinguishes it from failures)."""
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(2)


def cmd_set_project_status(conn, slug, status):
    if status not in PROJECT_STATUSES:
        _err2(f"status inválido '{status}'. Use: {'|'.join(PROJECT_STATUSES)}")
    row = conn.execute("SELECT id FROM projects WHERE slug=?", (slug,)).fetchone()
    if not row:
        _err2(f"Projeto '{slug}' não encontrado.")
    conn.execute("UPDATE projects SET status=?, updated_at=datetime('now','utc') WHERE id=?",
                 (status, row["id"]))
    conn.commit()
    _ok(f"Projeto '{slug}' → {status}")


# ── Quality signals (B-035, ADR-019) ────────────────────────────────────────

SIGNAL_KINDS = ("callers_open", "duplicate", "tests")


def cmd_add_signal(conn, slug, kind, subject, detail=None, session=None):
    """Record one signal. An open signal with the same (project, kind, subject) is refreshed
    instead of duplicated. `tests` is a state, not an alarm: a new one closes the previous."""
    if kind not in SIGNAL_KINDS:
        _err2(f"kind inválido '{kind}'. Use: {'|'.join(SIGNAL_KINDS)}")
    p = _get_project(conn, slug)
    try:
        det = json.loads(detail) if detail else {}
    except ValueError:
        _err2("--detail precisa ser JSON")
    det_txt = json.dumps(det, ensure_ascii=False, sort_keys=True)
    now = _now()
    if kind == "tests":
        conn.execute("UPDATE signals SET resolved_at=? WHERE project_id=? AND kind='tests' "
                     "AND resolved_at IS NULL", (now, p["id"]))
        row = None
    else:
        row = conn.execute("SELECT id FROM signals WHERE project_id=? AND kind=? AND subject=? "
                           "AND resolved_at IS NULL", (p["id"], kind, subject)).fetchone()
    if row:
        sid = row["id"]
        conn.execute("UPDATE signals SET ts=?, detail=?, session_id=COALESCE(?, session_id) "
                     "WHERE id=?", (now, det_txt, session, sid))
    else:
        sid = conn.execute("INSERT INTO signals (ts, project_id, session_id, kind, subject, detail) "
                           "VALUES (?,?,?,?,?,?)",
                           (now, p["id"], session, kind, subject, det_txt)).lastrowid
    conn.commit()
    if _json_mode:
        print(json.dumps({"id": sid}))
    else:
        _ok(f"signal {sid} ({kind}) {subject}")


def cmd_resolve_signal(conn, ids):
    now = _now()
    n = 0
    for i in ids:
        try:
            n += conn.execute("UPDATE signals SET resolved_at=? WHERE id=? AND resolved_at IS NULL",
                              (now, int(i))).rowcount
        except ValueError:
            _err2(f"id inválido '{i}'")
    conn.commit()
    _ok(f"resolve-signal: {n} sinal(is) resolvido(s)")


def _signal_rows(conn, slug=None, open_only=False, since=None):
    q = ("SELECT s.*, p.slug FROM signals s JOIN projects p ON p.id=s.project_id WHERE 1=1")
    args = []
    if slug:
        q += " AND p.slug=?"
        args.append(slug)
    if open_only:
        q += " AND s.resolved_at IS NULL"
    if since:
        q += " AND s.ts>=?"
        args.append(since)
    return conn.execute(q + " ORDER BY s.id DESC", args).fetchall()


def cmd_signals(conn, slug=None, open_only=False, report=False, since=None):
    """List signals, or (--report) the shadow-mode summary used to decide on injection:
    per kind, how many fired, how many resolved by themselves and how fast, plus a sample of
    20 alarms to check by hand (ADR-019: G-1 false alarms <= 10%, G-2 <= 25%)."""
    if slug:
        _get_project(conn, slug)
    rows = _signal_rows(conn, slug, open_only and not report, since)
    if not report:
        items = [{"id": r["id"], "ts": r["ts"], "project": r["slug"], "kind": r["kind"],
                  "subject": r["subject"], "detail": json.loads(r["detail"] or "{}"),
                  "resolved_at": r["resolved_at"]} for r in rows]
        if _json_mode:
            print(json.dumps(items, ensure_ascii=False))
            return
        if not items:
            _out("  (nenhum sinal)")
        for it in items:
            mark = "✓" if it["resolved_at"] else "●"
            _out(f"  {mark} #{it['id']:<5} {it['ts'][:16]} {it['project']:<20} {it['kind']:<13} {it['subject']}")
        return
    by = {}
    for r in rows:
        if r["kind"] == "tests":
            continue
        b = by.setdefault(r["kind"], {"total": 0, "resolved": 0, "minutes": []})
        b["total"] += 1
        if r["resolved_at"]:
            b["resolved"] += 1
            try:
                t0 = datetime.strptime(r["ts"], "%Y-%m-%dT%H:%M:%SZ")
                t1 = datetime.strptime(r["resolved_at"], "%Y-%m-%dT%H:%M:%SZ")
                b["minutes"].append((t1 - t0).total_seconds() / 60)
            except ValueError:
                pass
    out = {"kinds": {}, "sample": []}
    for k, b in sorted(by.items()):
        mins = sorted(b["minutes"])
        out["kinds"][k] = {"total": b["total"], "resolved": b["resolved"],
                           "median_minutes_to_resolve": round(mins[len(mins) // 2], 1) if mins else None}
    alarms = [r for r in rows if r["kind"] != "tests"]
    # Deterministic sample: every n-th alarm, newest first, so a re-run shows the same 20.
    step = max(1, len(alarms) // 20)
    for r in alarms[::step][:20]:
        out["sample"].append({"id": r["id"], "project": r["slug"], "kind": r["kind"],
                              "subject": r["subject"], "detail": json.loads(r["detail"] or "{}"),
                              "resolved": bool(r["resolved_at"])})
    if _json_mode:
        print(json.dumps(out, ensure_ascii=False))
        return
    _out("Sinais (relatório da sombra)")
    for k, v in out["kinds"].items():
        _out(f"  {k:<13} {v['total']:>4} disparos · {v['resolved']:>4} resolvidos sozinhos · "
             f"mediana {v['median_minutes_to_resolve']} min")
    _out("Amostra para conferir à mão (marque cada um como acerto ou alarme falso):")
    for it in out["sample"]:
        _out(f"  #{it['id']:<5} {it['project']:<20} {it['kind']:<13} {it['subject']} "
             f"{'(resolvido)' if it['resolved'] else ''}")


# ── Monitor (B-036, SPEC-P05 rev. 3, ADR-019) ───────────────────────────────
# One read-only contract for the Canvas panel (/monitor) and the Claude Code band:
#   osforge-db monitor [<slug>] [--days=30] [--discover] [--all] [--compact] --json
# Without a slug: the portfolio (every project, grouped by lifecycle status). With a slug: the
# project's detail. Never writes to the database. Schema `osforge.monitor.v1`.

MONITOR_SCHEMA = "osforge.monitor.v1"


def _tz_modifier():
    """SQLite date modifier for the local UTC offset, computed once. `'localtime'` would call
    localtime_r per row (the slowest part of the query on 50k calls). The offset of *now* is used
    for the whole horizon: around a DST change a call within an hour of midnight may land on the
    neighbouring day, which a progress view tolerates."""
    off = datetime.now().astimezone().utcoffset() or timedelta(0)
    return f"{int(off.total_seconds() // 60):+d} minutes"
_AGENT_GAP_CAP_S = 300          # a pause longer than 5 min between calls is not agent work
_MONITOR_HEATMAP_DAYS = 84      # 12 weeks
_OPEN_TASK = ("pending", "in-progress", "blocked")


def _iso_utc(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(ts):
    """UTC timestamp from 'YYYY-MM-DDTHH:MM:SS[.fff][Z]' or SQLite's 'YYYY-MM-DD HH:MM:SS'."""
    try:
        return datetime.fromisoformat((ts or "")[:19].replace(" ", "T")).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _day_keys(n):
    today = datetime.now().astimezone().date()
    return [(today - timedelta(days=i)).isoformat() for i in range(n - 1, -1, -1)]


def _quota_snapshot():
    path = os.environ.get("OSFORGE_QUOTA_FILE") or os.path.expanduser("~/.osforge/quota.json")
    try:
        with open(path, encoding="utf-8") as f:
            q = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(q, dict) or q.get("schema") not in (None, "osforge.quota.v1"):
        return None
    out = {"at": q.get("at")}
    for k in ("five_hour", "seven_day"):
        sub = q.get(k)
        if isinstance(sub, dict):
            out[k] = {"pct": sub.get("pct"), "resets_at": sub.get("resets_at")}
    if isinstance(q.get("rejected"), dict):
        out["rejected"] = {"resets_at": q["rejected"].get("resets_at")}
    return out


def _usage_by_day(conn, cutoff, project_id=None, with_sessions=False):
    """Usage since `cutoff`, aggregated in SQLite (50k calls must stay well under 200 ms):
    per project and local day, per (day, model), per session (detail only) and
    orchestrator/subagent. Cost is priced per aggregated group from pricing.json, never per row.
    Agent minutes: gap to the previous call of the same session (LAG), capped at 5 minutes."""
    where, params = "ts>=?", [cutoff]
    if project_id is not None:
        where += " AND project_id=?"
        params.append(project_id)
    models = _load_pricing()
    price_cache = {}
    tzm = _tz_modifier()

    def price(model):
        if model not in price_cache:
            price_cache[model] = _price_for_model(models, model)
        return price_cache[model]

    per, per_model, split, priceless = {}, {}, {}, {}
    for r in conn.execute(
            f"SELECT project_id, date(ts,'{tzm}') day, model, sidechain, COUNT(*) n, "
            f"SUM(input) input, SUM(output) output, SUM(cache_read) cache_read, "
            f"SUM(cache_write_5m) cache_write_5m, SUM(cache_write_1h) cache_write_1h "
            f"FROM calls WHERE {where} GROUP BY project_id, day, model, sidechain", params):
        pid, day = r["project_id"], r["day"]
        pr = price(r["model"])
        cost = _cost_usd(pr, r) if pr else 0.0
        if pr is None:
            priceless[r["model"]] = priceless.get(r["model"], 0) + r["n"]
        tokens = (r["input"] or 0) + (r["output"] or 0) + (r["cache_write_5m"] or 0) + (r["cache_write_1h"] or 0)
        d = per.setdefault(pid, {}).setdefault(day, {"chamadas": 0, "tokens": 0, "cache_read": 0,
                                                     "custo": 0.0, "minutos": 0.0, "_s": set()})
        d["chamadas"] += r["n"]
        d["tokens"] += tokens
        d["cache_read"] += r["cache_read"] or 0
        d["custo"] += cost
        m = per_model.setdefault(pid, {}).setdefault((day, r["model"]), {"chamadas": 0, "tokens": 0, "custo": 0.0})
        m["chamadas"] += r["n"]
        m["tokens"] += tokens
        m["custo"] += cost
        sp = split.setdefault(pid, {}).setdefault("subagente" if r["sidechain"] else "orquestrador",
                                                 {"chamadas": 0, "tokens": 0, "custo": 0.0})
        sp["chamadas"] += r["n"]
        sp["tokens"] += tokens
        sp["custo"] += cost
    # Sessions and agent minutes per (project, day, session).
    for r in conn.execute(
            f"SELECT project_id, day, session_id, SUM(MIN(COALESCE(gap, 0), {_AGENT_GAP_CAP_S})) / 60.0 minutes "
            f"FROM (SELECT project_id, session_id, date(ts,'{tzm}') day, "
            f"      MAX((julianday(ts) - julianday(LAG(ts) OVER (PARTITION BY session_id ORDER BY ts))) * 86400, 0) gap "
            f"      FROM calls WHERE {where}) GROUP BY project_id, day, session_id", params):
        d = per.get(r["project_id"], {}).get(r["day"])
        if d is not None:
            d["minutos"] += r["minutes"] or 0.0
            d["_s"].add(r["session_id"])
    sessions = {}
    if with_sessions and project_id is not None:
        rows = conn.execute(
            f"SELECT session_id, model, MIN(ts) inicio, MAX(ts) fim, COUNT(*) n, SUM(input) input, "
            f"SUM(output) output, SUM(cache_read) cache_read, SUM(cache_write_5m) cache_write_5m, "
            f"SUM(cache_write_1h) cache_write_1h FROM calls WHERE {where} GROUP BY session_id, model", params)
        mins = {r["session_id"]: r["m"] or 0.0 for r in conn.execute(
            f"SELECT session_id, SUM(MIN(COALESCE(gap, 0), {_AGENT_GAP_CAP_S})) / 60.0 m FROM "
            f"(SELECT session_id, MAX((julianday(ts) - julianday(LAG(ts) OVER (PARTITION BY session_id ORDER BY ts))) * 86400, 0) gap "
            f" FROM calls WHERE {where}) GROUP BY session_id", params)}
        for r in rows:
            pr = price(r["model"])
            tokens = (r["input"] or 0) + (r["output"] or 0) + (r["cache_write_5m"] or 0) + (r["cache_write_1h"] or 0)
            s = sessions.setdefault(r["session_id"], {"inicio": r["inicio"], "fim": r["fim"], "chamadas": 0,
                                                      "tokens": 0, "custo": 0.0,
                                                      "minutos": mins.get(r["session_id"], 0.0), "_m": {}})
            s["inicio"] = min(s["inicio"], r["inicio"])
            s["fim"] = max(s["fim"], r["fim"])
            s["chamadas"] += r["n"]
            s["tokens"] += tokens
            s["custo"] += _cost_usd(pr, r) if pr else 0.0
            s["_m"][r["model"]] = s["_m"].get(r["model"], 0) + r["n"]
        sessions = {project_id: sessions}
    return per, per_model, sessions, split, priceless


def _series(per_day, keys):
    out = []
    for k in keys:
        d = per_day.get(k) or {}
        out.append({"dia": k, "chamadas": d.get("chamadas", 0), "tokens": d.get("tokens", 0),
                    "custo": round(d.get("custo", 0.0), 4), "minutos": round(d.get("minutos", 0.0), 1),
                    "sessoes": len(d.get("_s", ()))})
    return out


def _period(per_day, keys):
    tot = {"chamadas": 0, "tokens": 0, "custo": 0.0, "minutos": 0.0}
    sess = set()
    for k in keys:
        d = per_day.get(k)
        if not d:
            continue
        for f in ("chamadas", "tokens", "custo", "minutos"):
            tot[f] += d[f]
        sess |= d["_s"]
    tot["custo"] = round(tot["custo"], 4)
    tot["minutos"] = round(tot["minutos"], 1)
    tot["sessoes"] = len(sess)
    return tot


def _project_summary(conn, p, per_day, keys_period, keys_series):
    pid = p["id"]
    counts = {s: 0 for s in ("pending", "in_progress", "blocked", "done", "cancelled")}
    for r in conn.execute("SELECT status, COUNT(*) n FROM tasks WHERE project_id=? GROUP BY status", (pid,)):
        counts[r["status"].replace("-", "_")] = r["n"]
    ph = conn.execute("SELECT COUNT(*) total, SUM(CASE WHEN status IN ('complete','done') THEN 1 ELSE 0 END) feitas "
                      "FROM phases WHERE project_id=?", (pid,)).fetchone()
    st = conn.execute("SELECT current_phase, resume_point, updated_at FROM state WHERE project_id=?", (pid,)).fetchone()
    blockers = conn.execute("SELECT COUNT(*) FROM blockers WHERE project_id=? AND resolved_at IS NULL", (pid,)).fetchone()[0]
    signals = conn.execute("SELECT COUNT(*) FROM signals WHERE project_id=? AND resolved_at IS NULL AND kind!='tests'",
                           (pid,)).fetchone()[0]
    live = sum(v for k, v in counts.items() if k != "cancelled")
    if live:
        pct = round(100.0 * counts["done"] / live, 1)
    elif ph["total"]:
        pct = round(100.0 * (ph["feitas"] or 0) / ph["total"], 1)
    else:
        pct = None
    last = [conn.execute(q, (pid,)).fetchone()[0] for q in (
        "SELECT MAX(ts) FROM calls WHERE project_id=?",
        "SELECT MAX(updated_at) FROM tasks WHERE project_id=?",
        "SELECT MAX(created_at) FROM decisions WHERE project_id=?",
        "SELECT MAX(updated_at) FROM state WHERE project_id=?")]
    last = [x for x in last if x]
    # Several older columns are written with datetime('now','utc'), which SQLite shifts by the
    # local offset (UTC-3 → now + 3 h). Clamp: activity is never in the future.
    now_utc = datetime.now(timezone.utc)
    stamps = [min(d, now_utc) for d in (_parse_iso(x) for x in last) if d]
    last_iso = _iso_utc(max(stamps)) if stamps else None
    status = p["status"] if p["status"] in PROJECT_STATUSES else "outro"
    grupo, regra = _grupo_base(status, last_iso)
    root = p["root_path"] if "root_path" in p.keys() else None
    return {
        "slug": p["slug"], "descricao": p["description"], "status": status,
        "status_bruto": p["status"], "triage": p["triage"],
        "fase_atual": (st["current_phase"] if st else None),
        "fases": {"total": ph["total"] or 0, "feitas": ph["feitas"] or 0},
        "tarefas": counts, "tarefas_abertas": counts["pending"] + counts["in_progress"] + counts["blocked"],
        "pct": pct, "bloqueios_abertos": blockers, "sinais_abertos": signals,
        "ultima_atividade": last_iso,
        "periodo": _period(per_day, keys_period),
        "serie": _series(per_day, keys_series),
        "acesso": {"raiz": root, "raiz_existe": bool(root and os.path.isdir(root)),
                   "remoto": bool(p["remote_hash"] if "remote_hash" in p.keys() else None)},
        "grupo_base": grupo, "grupo_regra": regra,
        "inbox_pendentes": conn.execute("SELECT COUNT(*) FROM inbox WHERE project_id=? AND status='pendente'",
                                        (pid,)).fetchone()[0],
    }


def _discover(conn, max_age_days=30):
    """Folders with a Claude Code session in the last `max_age_days` days, from the `cwd` field
    of the newest transcript per folder in ~/.claude/projects. Read-only: nothing is written;
    the caller shows commands. Returns (unregistered[], suggested_roots{project_id: dir})."""
    base = os.environ.get("OSFORGE_TRANSCRIPTS_DIR") or os.path.expanduser("~/.claude/projects")
    if not os.path.isdir(base):
        return [], {}
    horizon = time.time() - max_age_days * 86400
    cwds = {}
    for entry in os.listdir(base):
        d = os.path.join(base, entry)
        if not os.path.isdir(d):
            continue
        try:
            files = [os.path.join(d, f) for f in os.listdir(d) if f.endswith(".jsonl")]
            files = [(os.path.getmtime(f), f) for f in files]
        except OSError:
            continue
        files = [x for x in files if x[0] >= horizon]
        if not files:
            continue
        mtime, newest = max(files)
        cwd = None
        try:
            with open(newest, encoding="utf-8", errors="replace") as fh:
                for _ in range(60):
                    line = fh.readline()
                    if not line:
                        break
                    try:
                        e = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(e, dict) and isinstance(e.get("cwd"), str) and e["cwd"]:
                        cwd = e["cwd"]
                        break
        except OSError:
            continue
        if not cwd or not os.path.isdir(cwd):
            continue
        if cwd not in cwds or cwds[cwd][0] < mtime:
            cwds[cwd] = (mtime, len(files))
    cache, unregistered, suggested, seen = {}, [], {}, set()
    home = os.path.realpath(os.path.expanduser("~"))
    for cwd, (mtime, nfiles) in sorted(cwds.items(), key=lambda kv: -kv[1][0]):
        top = _git_out(["rev-parse", "--show-toplevel"], cwd)
        root = os.path.realpath(top) if top else os.path.realpath(cwd)
        if root == home or root in seen:
            continue
        seen.add(root)
        pid = _resolve_project_id_for_cwd(conn, os.path.realpath(cwd), cache)
        if pid is not None:
            row = conn.execute("SELECT root_path FROM projects WHERE id=?", (pid,)).fetchone()
            if not (row and row["root_path"]) and top:
                suggested.setdefault(pid, root)
            continue
        slug = _slugify(os.path.basename(root)) or "projeto"
        unregistered.append({
            "pasta": root, "nome": os.path.basename(root), "slug_sugerido": slug, "git": bool(top),
            "ultima_sessao": _iso_utc(datetime.fromtimestamp(mtime, timezone.utc)),
            "sessoes_30d": nfiles,
            "comando": (f"osforge-db upsert-project {shlex.quote(slug)} {shlex.quote(os.path.basename(root))} "
                        f"standard backlog --root={shlex.quote(root)}"),
        })
    return unregistered, suggested


def _shortcuts(root):
    """`shortcut:` comments in the project (Ponytail's debt ledger, EV-P34): how many, and how
    many do not say when to replace them (no comma after the limit)."""
    if not root or not os.path.isdir(root):
        return None
    import subprocess
    try:
        r = subprocess.run(["git", "-C", root, "grep", "-n", "-I", "--no-color", "-E", r"shortcut:"],
                           capture_output=True, text=True, timeout=2, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode not in (0, 1):
        return None
    items, no_trigger = [], 0
    for line in r.stdout.splitlines():
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        note = parts[2].split("shortcut:", 1)[-1].strip()
        has_trigger = "," in note
        no_trigger += 0 if has_trigger else 1
        if len(items) < 50:
            items.append({"local": f"{parts[0]}:{parts[1]}", "nota": note[:160], "gatilho": has_trigger})
    return {"total": len(r.stdout.splitlines()), "sem_gatilho": no_trigger, "itens": items}


def _project_detail(conn, p, summary, per_model, sessions, split, priceless, keys_period):
    pid = p["id"]
    phases = []
    for ph in conn.execute("SELECT id, name, status, started_at, completed_at FROM phases WHERE project_id=? ORDER BY id", (pid,)):
        c = {s: 0 for s in ("pending", "in-progress", "blocked", "done", "cancelled")}
        for r in conn.execute("SELECT status, COUNT(*) n FROM tasks WHERE phase_id=? GROUP BY status", (ph["id"],)):
            c[r["status"]] = r["n"]
        live = sum(v for k, v in c.items() if k != "cancelled")
        phases.append({"nome": ph["name"], "status": ph["status"], "total": live, "feitas": c["done"],
                       "em_andamento": c["in-progress"], "bloqueadas": c["blocked"],
                       "pct": round(100.0 * c["done"] / live, 1) if live else
                              (100.0 if ph["status"] in ("complete", "done") else 0.0)})
    done_ids = {r["id"] for r in conn.execute("SELECT id FROM tasks WHERE project_id=? AND status='done'", (pid,))}
    open_tasks = []
    for t in conn.execute(
            "SELECT t.id, t.title, t.status, t.priority, t.wave, t.depends_on, t.updated_at, ph.name phase "
            "FROM tasks t LEFT JOIN phases ph ON ph.id=t.phase_id WHERE t.project_id=? AND t.status IN "
            "('pending','in-progress','blocked') ORDER BY t.priority, t.wave, t.id", (pid,)):
        deps = [d.strip() for d in (t["depends_on"] or "").split(",") if d.strip()]
        pend = [d for d in deps if not (d.isdigit() and int(d) in done_ids)]
        open_tasks.append({"id": t["id"], "titulo": t["title"], "status": t["status"], "prioridade": t["priority"],
                           "onda": t["wave"], "fase": t["phase"], "dependencias_abertas": pend,
                           "atualizada": t["updated_at"]})
    recent_done = [{"id": t["id"], "titulo": t["title"], "atualizada": t["updated_at"]} for t in conn.execute(
        "SELECT id, title, updated_at FROM tasks WHERE project_id=? AND status='done' "
        "ORDER BY updated_at DESC, id DESC LIMIT 10", (pid,))]
    now = datetime.now(timezone.utc)
    blockers = []
    for b in conn.execute("SELECT id, description, waiting_for, created_at FROM blockers "
                          "WHERE project_id=? AND resolved_at IS NULL ORDER BY created_at", (pid,)):
        c = _parse_iso(b["created_at"])
        blockers.append({"id": b["id"], "descricao": b["description"], "aguardando": b["waiting_for"],
                         "desde": b["created_at"], "idade_dias": (now - c).days if c else None})
    decisions = [{"id": d["id"], "texto": textwrap.shorten(d["content"], width=280, placeholder="…"),
                  "categoria": d["category"], "em": d["created_at"]} for d in conn.execute(
        "SELECT id, content, category, created_at FROM decisions WHERE project_id=? "
        "ORDER BY created_at DESC, id DESC LIMIT 10", (pid,))]
    sigs = [{"id": s["id"], "tipo": s["kind"], "assunto": s["subject"], "em": s["ts"],
             "detalhe": json.loads(s["detail"] or "{}")} for s in conn.execute(
        "SELECT * FROM signals WHERE project_id=? AND resolved_at IS NULL AND kind!='tests' ORDER BY id DESC LIMIT 50", (pid,))]
    t = conn.execute("SELECT detail, ts FROM signals WHERE project_id=? AND kind='tests' ORDER BY id DESC LIMIT 1",
                     (pid,)).fetchone()
    tests = dict(json.loads(t["detail"] or "{}"), em=t["ts"]) if t else None
    pm = per_model.get(pid, {})
    by_day_model = [{"dia": k[0], "modelo": k[1], "chamadas": v["chamadas"], "tokens": v["tokens"],
                     "custo": round(v["custo"], 4)} for k, v in sorted(pm.items())]
    sess = []
    for sid, s in sorted((sessions.get(pid) or {}).items(), key=lambda kv: kv[1]["inicio"], reverse=True)[:20]:
        main_model = max(s["_m"].items(), key=lambda kv: kv[1])[0] if s["_m"] else None
        sess.append({"sessao": sid[:8], "inicio": s["inicio"], "fim": s["fim"], "minutos": round(s["minutos"], 1),
                     "chamadas": s["chamadas"], "tokens": s["tokens"], "custo": round(s["custo"], 4),
                     "modelo": main_model})
    root = summary["acesso"]["raiz"] if summary["acesso"]["raiz_existe"] else None
    detail = dict(summary)
    detail.update({
        "fases_detalhe": phases,
        "tarefas_abertas_lista": open_tasks,
        "feitas_recentes": recent_done,
        "bloqueios": blockers,
        "decisoes": decisions,
        "consumo": {"por_dia_modelo": by_day_model,
                    "orquestrador_subagente": {k: dict(v, custo=round(v["custo"], 4))
                                               for k, v in (split.get(pid) or {}).items()},
                    "sem_preco": priceless},
        "sessoes": sess,
        "qualidade": {"sinais": sigs, "testes": tests, "atalhos": _shortcuts(root)},
        "conversa": _conversation(conn, pid),
        "atividade": [{"dia": x["dia"], "minutos": x["minutos"]} for x in summary["serie"][-_MONITOR_HEATMAP_DAYS:]],
    })
    return detail


def cmd_monitor(conn, slug=None, days=30, discover=False, include_archived=False, compact=False, live=False):
    if days < 1 or days > 365:
        _err2("--days entre 1 e 365")
    horizon = max(2 * days, _MONITOR_HEATMAP_DAYS)
    keys_series = _day_keys(horizon)
    keys_period = keys_series[-days:]
    cutoff = _iso_utc(datetime.strptime(keys_series[0], "%Y-%m-%d").replace(tzinfo=timezone.utc)
                      - timedelta(days=1))
    out = {"schema": MONITOR_SCHEMA, "gerado_em": _iso_utc(datetime.now(timezone.utc)), "dias": days,
           "horizonte_dias": horizon, "janela": _quota_snapshot()}
    if slug:
        p = conn.execute("SELECT * FROM projects WHERE slug=?", (slug,)).fetchone()
        if not p:
            _err2(f"Projeto '{slug}' não encontrado.")
        if compact:   # the band gets cost and window from the engine; skip the usage scan
            per, per_model, sessions, split, priceless = {}, {}, {}, {}, {}
        else:
            per, per_model, sessions, split, priceless = _usage_by_day(conn, cutoff, p["id"], True)
        summary = _project_summary(conn, p, per.get(p["id"], {}), keys_period, keys_series)
        if compact:
            in_prog = conn.execute("SELECT title FROM tasks WHERE project_id=? AND status='in-progress' "
                                   "ORDER BY priority, id LIMIT 1", (p["id"],)).fetchone()
            t = conn.execute("SELECT detail FROM signals WHERE project_id=? AND kind='tests' ORDER BY id DESC LIMIT 1",
                             (p["id"],)).fetchone()
            kinds = {r["kind"]: r["n"] for r in conn.execute(
                "SELECT kind, COUNT(*) n FROM signals WHERE project_id=? AND resolved_at IS NULL AND kind!='tests' "
                "GROUP BY kind", (p["id"],))}
            out["projeto"] = {k: summary[k] for k in ("slug", "status", "fase_atual", "fases", "tarefas", "pct",
                                                       "bloqueios_abertos")}
            out["projeto"]["em_andamento"] = in_prog["title"] if in_prog else None
            out["projeto"]["sinais"] = kinds
            out["projeto"]["testes"] = (json.loads(t["detail"] or "{}").get("state") if t else None)
        else:
            out["projeto"] = _project_detail(conn, p, summary, per_model, sessions, split, priceless, keys_period)
        print(json.dumps(out, ensure_ascii=False, separators=(",", ":") if compact else None))
        return
    per, _pm, _s, _sp, priceless = _usage_by_day(conn, cutoff)
    q = "SELECT * FROM projects"   # archived projects are the history library: always listed (P-06)
    projects = [_project_summary(conn, p, per.get(p["id"], {}), keys_period, keys_series)
                for p in conn.execute(q + " ORDER BY slug").fetchall()]
    suggested, unregistered = {}, []
    if discover:
        unregistered, suggested = _discover(conn)
        by_id = {r["slug"]: r["id"] for r in conn.execute("SELECT id, slug FROM projects")}
        for pr in projects:
            sug = suggested.get(by_id.get(pr["slug"]))
            if sug:
                pr["acesso"]["raiz_sugerida"] = sug
                pr["acesso"]["comando"] = f"osforge-db bind-project {pr['slug']} --root={shlex.quote(sug)}"
    order = {g: i for i, g in enumerate(("andamento", "aguardando", "backlog", "historico"))}
    projects.sort(key=lambda x: (order.get(x["grupo_base"], 9), -(_parse_iso(x["ultima_atividade"]) or
                                 datetime(1970, 1, 1, tzinfo=timezone.utc)).timestamp(), x["slug"]))
    by_status, by_group = {}, {}
    for pr in projects:
        by_status[pr["status"]] = by_status.get(pr["status"], 0) + 1
        by_group[pr["grupo_base"]] = by_group.get(pr["grupo_base"], 0) + 1
    tot = {"chamadas": 0, "tokens": 0, "custo": 0.0, "minutos": 0.0}
    sess = set()
    for pid, days_map in per.items():
        for k in keys_period:
            d = days_map.get(k)
            if d:
                for f in tot:
                    tot[f] += d[f]
                sess |= d["_s"]
    unassigned = sum(d["chamadas"] for k, d in (per.get(None) or {}).items() if k in keys_period)
    out["totais"] = {
        "projetos": len(projects), "por_status": by_status, "por_grupo": by_group,
        "inbox_pendentes": sum(p["inbox_pendentes"] for p in projects),
        "tarefas_abertas": sum(p["tarefas_abertas"] for p in projects),
        "bloqueios_abertos": sum(p["bloqueios_abertos"] for p in projects),
        "sinais_abertos": sum(p["sinais_abertos"] for p in projects),
        "chamadas": tot["chamadas"], "sessoes": len(sess), "tokens": tot["tokens"],
        "custo": round(tot["custo"], 4), "minutos": round(tot["minutos"], 1),
    }
    out["projetos"] = projects
    out["regras_grupo"] = {"aguardando_apos_h": GROUP_WAITING_AFTER_H, "historico_apos_dias": GROUP_HISTORY_AFTER_D}
    if live:
        out["ao_vivo"] = live_state(conn)
    now = datetime.now(timezone.utc)
    shown = {p["slug"] for p in projects}
    blk = []
    for b in conn.execute("SELECT b.id, b.description, b.waiting_for, b.created_at, p.slug FROM blockers b "
                          "JOIN projects p ON p.id=b.project_id WHERE b.resolved_at IS NULL ORDER BY b.created_at"):
        if b["slug"] not in shown:
            continue
        c = _parse_iso(b["created_at"])
        blk.append({"projeto": b["slug"], "id": b["id"], "descricao": b["description"], "aguardando": b["waiting_for"],
                    "desde": b["created_at"], "idade_dias": (now - c).days if c else None})
    out["bloqueios"] = blk
    out["sem_projeto"] = {"serie": _series(per.get(None) or {}, keys_series)}
    if discover:
        out["sem_cadastro"] = unregistered
    out["saude"] = {
        "chamadas_sem_projeto_pct": round(100.0 * unassigned / tot["chamadas"], 1) if tot["chamadas"] else 0.0,
        "projetos_sem_raiz": [p["slug"] for p in projects if not p["acesso"]["raiz_existe"]],
        "modelos_sem_preco": priceless,
    }
    print(json.dumps(out, ensure_ascii=False))


# ── Command centre (B-040..B-042, SPEC-P06) ─────────────────────────────────
# Sidebar groups by live activity and age; a per-project inbox the `inbox-deliver` hook hands to
# the running agent; and the record of what the panel launched (`runs`).

GROUP_WAITING_AFTER_H = 24
GROUP_HISTORY_AFTER_D = 30
INBOX_MAX_CHARS = 4000
RUN_KINDS = ("terminal", "background", "ide")
RUN_STATUSES = ("iniciada", "rodando", "concluida", "falhou", "interrompida")
_HELD = {"paused": "segurado", "done": "concluído", "archived": "arquivado"}


def _grupo_base(status, last_iso, now=None):
    """(group, reason) without live activity — the panel puts a live project in "ativo"."""
    now = now or datetime.now(timezone.utc)
    if status == "backlog":
        return "backlog", "no backlog"
    if status in _HELD:
        return "historico", _HELD[status]
    last = _parse_iso(last_iso) if last_iso else None
    if not last:
        return "historico", "sem atividade registrada"
    age_h = (now - last).total_seconds() / 3600
    if age_h > GROUP_HISTORY_AFTER_D * 24:
        return "historico", f"parado há {int(age_h // 24)} dias"
    if age_h > GROUP_WAITING_AFTER_H:
        return "aguardando", (f"parado há {int(age_h // 24)} dias" if age_h >= 48 else f"parado há {int(age_h)} h")
    return "andamento", "atividade nas últimas 24 h"


def _inbox_dir():
    return os.environ.get("OSFORGE_INBOX_DIR") or os.path.expanduser("~/.osforge/inbox")


def _inbox_flag(slug):
    safe = slug if re.match(r"^[a-z0-9][a-z0-9._-]{0,99}$", slug or "") else \
        "h-" + hashlib.sha1((slug or "").encode("utf-8")).hexdigest()[:16]
    return os.path.join(_inbox_dir(), safe)


def _inbox_sync_flag(conn, pid, slug):
    """The flag file mirrors "this project has pending messages": the hook's fast path."""
    n = conn.execute("SELECT COUNT(*) FROM inbox WHERE project_id=? AND status='pendente'", (pid,)).fetchone()[0]
    flag = _inbox_flag(slug)
    try:
        if n:
            os.makedirs(_inbox_dir(), mode=0o700, exist_ok=True)
            with open(flag, "w", encoding="utf-8") as f:
                f.write(str(n))
        elif os.path.exists(flag):
            os.remove(flag)
    except OSError:
        pass
    return n


def cmd_inbox_add(conn, slug, text, via="painel"):
    text = (text or "").strip()
    if not text:
        _err2("orientação vazia")
    if len(text) > INBOX_MAX_CHARS:
        _err2(f"orientação com mais de {INBOX_MAX_CHARS} caracteres")
    p = conn.execute("SELECT id FROM projects WHERE slug=?", (slug,)).fetchone()
    if not p:
        _err2(f"Projeto '{slug}' não encontrado.")
    mid = conn.execute("INSERT INTO inbox (ts, project_id, text, via) VALUES (?,?,?,?)",
                       (_now(), p["id"], text, via or "painel")).lastrowid
    conn.commit()
    _inbox_sync_flag(conn, p["id"], slug)
    if _json_mode:
        print(json.dumps({"id": mid}))
    else:
        _ok(f"orientação {mid} na caixa de entrada de '{slug}'")


def cmd_inbox_take(conn, slug, session):
    """Atomically hand every pending message of `slug` to `session`. Prints a JSON list (empty
    when there is nothing, or the project is unknown — the hook calls this blind)."""
    p = conn.execute("SELECT id FROM projects WHERE slug=?", (slug,)).fetchone()
    if not p:
        print("[]")
        return
    conn.commit()
    conn.execute("BEGIN IMMEDIATE")
    rows = conn.execute("SELECT id, ts, text FROM inbox WHERE project_id=? AND status='pendente' ORDER BY id",
                        (p["id"],)).fetchall()
    now = _now()
    for r in rows:
        conn.execute("UPDATE inbox SET status='entregue', delivered_at=?, delivered_session=? WHERE id=?",
                     (now, session or "", r["id"]))
    conn.execute("COMMIT")
    _inbox_sync_flag(conn, p["id"], slug)
    print(json.dumps([{"id": r["id"], "ts": r["ts"], "text": r["text"]} for r in rows], ensure_ascii=False))


def cmd_inbox_list(conn, slug, limit=50):
    p = _get_project(conn, slug)
    rows = conn.execute("SELECT * FROM inbox WHERE project_id=? ORDER BY id DESC LIMIT ?", (p["id"], limit)).fetchall()
    items = [{"id": r["id"], "ts": r["ts"], "texto": r["text"], "status": r["status"], "via": r["via"],
              "entregue_em": r["delivered_at"], "sessao": (r["delivered_session"] or "")[:8] or None} for r in rows]
    if _json_mode:
        print(json.dumps(items, ensure_ascii=False))
        return
    for it in items:
        _out(f"  #{it['id']:<5} {it['ts'][:16]} {it['status']:<9} {textwrap.shorten(it['texto'], 70, placeholder='…')}")


def cmd_inbox_cancel(conn, mid):
    try:
        mid = int(mid)
    except ValueError:
        _err2(f"id inválido '{mid}'")
    r = conn.execute("SELECT i.project_id, p.slug FROM inbox i JOIN projects p ON p.id=i.project_id "
                     "WHERE i.id=? AND i.status='pendente'", (mid,)).fetchone()
    if not r:
        _err2(f"orientação {mid} não está pendente")
    conn.execute("UPDATE inbox SET status='cancelada' WHERE id=?", (mid,))
    conn.commit()
    _inbox_sync_flag(conn, r["project_id"], r["slug"])
    _ok(f"orientação {mid} cancelada")


def cmd_run_add(conn, slug, kind, tool="", prompt="", pid=None, log_path=None, status="iniciada"):
    if kind not in RUN_KINDS:
        _err2(f"kind inválido '{kind}'. Use: {'|'.join(RUN_KINDS)}")
    if status not in RUN_STATUSES:
        _err2(f"status inválido '{status}'")
    p = conn.execute("SELECT id FROM projects WHERE slug=?", (slug,)).fetchone()
    if not p:
        _err2(f"Projeto '{slug}' não encontrado.")
    rid = conn.execute("INSERT INTO runs (ts, project_id, kind, tool, prompt, status, pid, log_path) "
                       "VALUES (?,?,?,?,?,?,?,?)",
                       (_now(), p["id"], kind, tool or "", (prompt or "")[:INBOX_MAX_CHARS * 2], status,
                        pid, log_path)).lastrowid
    conn.commit()
    print(json.dumps({"id": rid}) if _json_mode else f"run {rid}")


def cmd_run_update(conn, rid, status=None, pid=None, result=None, cost=None, log_path=None):
    try:
        rid = int(rid)
    except ValueError:
        _err2(f"id inválido '{rid}'")
    if status and status not in RUN_STATUSES:
        _err2(f"status inválido '{status}'")
    if not conn.execute("SELECT 1 FROM runs WHERE id=?", (rid,)).fetchone():
        _err2(f"execução {rid} não encontrada")
    sets, args = [], []
    for col, val in (("status", status), ("pid", pid), ("result", (result or "")[:4000] if result is not None else None),
                     ("cost_usd", cost), ("log_path", log_path)):
        if val is not None:
            sets.append(f"{col}=?")
            args.append(val)
    if status in ("concluida", "falhou", "interrompida"):
        sets.append("ended_at=?")
        args.append(_now())
    if sets:
        conn.execute(f"UPDATE runs SET {', '.join(sets)} WHERE id=?", args + [rid])
        conn.commit()
    _ok(f"execução {rid} atualizada")


def _runs_rows(conn, pid, limit=30):
    return [{"id": r["id"], "ts": r["ts"], "tipo": r["kind"], "ferramenta": r["tool"], "texto": r["prompt"],
             "status": r["status"], "pid": r["pid"], "fim": r["ended_at"], "resultado": r["result"],
             "custo": r["cost_usd"]}
            for r in conn.execute("SELECT * FROM runs WHERE project_id=? ORDER BY id DESC LIMIT ?", (pid, limit))]


def cmd_runs(conn, slug, limit=30):
    p = _get_project(conn, slug)
    items = _runs_rows(conn, p["id"], limit)
    if _json_mode:
        print(json.dumps(items, ensure_ascii=False))
        return
    for it in items:
        _out(f"  #{it['id']:<5} {it['ts'][:16]} {it['tipo']:<10} {it['status']:<12} {it['ferramenta']}")


# ── Live detection (B-040) ───────────────────────────────────────────────────

_IDE_HELPER = re.compile(r"^(?:.*/)?(.+?) Helper \(Plugin\): extension-host \(user\) (.+?)(?: \[[\d-]+\])?\s*$")
_IDE_NAMES = {"Code": "VS Code", "Code - Insiders": "VS Code Insiders"}
_DEV_SERVER = re.compile(
    r"(?:^|[\s/])(?:next(?:-server)?\s+dev|next-server|vite(?:\s|$)|expo\s+start|nodemon|uvicorn|"
    r"manage\.py\s+runserver|astro\s+dev|nuxt\s+dev|remix\s+dev|wrangler\s+dev|"
    r"(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?(?:dev|start)(?:\s|$)|bun\s+(?:--hot|--watch))")


def _ps_lines():
    fx = os.environ.get("OSFORGE_LIVE_PS_FILE")          # tests: a captured `ps` output
    if fx:
        try:
            return open(fx, encoding="utf-8").read().splitlines()
        except OSError:
            return []
    import subprocess
    try:
        r = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True, timeout=3, check=False)
        return r.stdout.splitlines()
    except (OSError, subprocess.SubprocessError):
        return []


def _cwds(pids):
    """pid -> working directory. Tests: OSFORGE_LIVE_CWD_FILE (JSON). Linux: /proc. macOS: lsof."""
    fx = os.environ.get("OSFORGE_LIVE_CWD_FILE")
    if fx:
        try:
            d = json.load(open(fx, encoding="utf-8"))
            return {int(k): v for k, v in d.items() if int(k) in pids}
        except (OSError, ValueError):
            return {}
    out = {}
    if not pids:
        return out
    if os.path.isdir("/proc/self"):
        for pid in pids:
            try:
                out[pid] = os.readlink(f"/proc/{pid}/cwd")
            except OSError:
                pass
        return out
    import subprocess
    try:
        r = subprocess.run(["lsof", "-a", "-d", "cwd", "-Fpn", "-p", ",".join(str(p) for p in sorted(pids))],
                           capture_output=True, text=True, timeout=3, check=False)
    except (OSError, subprocess.SubprocessError):
        return out
    cur = None
    for line in r.stdout.splitlines():
        if line.startswith("p"):
            try:
                cur = int(line[1:])
            except ValueError:
                cur = None
        elif line.startswith("n") and cur is not None:
            out[cur] = line[1:]
    return out


def _transcript_recent(cwd, seconds=120):
    """Claude Code keeps a session's transcript in ~/.claude/projects/<cwd with every
    non-alphanumeric character as '-'>; a write in the last `seconds` = working right now."""
    base = os.environ.get("OSFORGE_TRANSCRIPTS_DIR") or os.path.expanduser("~/.claude/projects")
    d = os.path.join(base, re.sub(r"[^A-Za-z0-9]", "-", cwd))
    try:
        newest = max((os.path.getmtime(os.path.join(d, f)) for f in os.listdir(d) if f.endswith(".jsonl")), default=0)
    except OSError:
        return False
    return time.time() - newest < seconds


def live_state(conn):
    """{"projetos": {slug: {...}}, "sem_cadastro": [...]} — what is running right now."""
    claude, servers, ides = {}, {}, []
    for line in _ps_lines():
        line = line.strip()
        m = re.match(r"^(\d+)\s+(.*)$", line)
        if not m:
            continue
        pid, cmd = int(m.group(1)), m.group(2)
        if pid == os.getpid():
            continue
        ide = _IDE_HELPER.match(cmd)
        if ide:
            app = os.path.basename(ide.group(1))
            ides.append((_IDE_NAMES.get(app, app), re.sub(r"\s*\(Workspace\)$", "", ide.group(2)).strip()))
            continue
        exe = cmd.split()[0] if cmd.split() else ""
        if os.path.basename(exe) == "claude":
            claude[pid] = cmd
        elif _DEV_SERVER.search(cmd) and "osforge" not in cmd:
            servers[pid] = cmd
    cwds = _cwds(set(claude) | set(servers))
    projects = {r["id"]: r for r in conn.execute("SELECT id, slug, root_path FROM projects")}
    cache, out, loose = {}, {}, {}

    def slot(pid_, key, label):
        if pid_ is not None:
            return out.setdefault(projects[pid_]["slug"], {"claude": 0, "trabalhando": False, "ides": [], "servidores": [], "pastas": []})
        return loose.setdefault(key, {"pasta": key, "nome": label, "claude": 0, "trabalhando": False, "ides": [], "servidores": []})

    for pid, cwd in cwds.items():
        real = os.path.realpath(cwd)
        top = _git_out(["rev-parse", "--show-toplevel"], real) if os.path.isdir(real) else ""
        root = os.path.realpath(top) if top else real
        if root == os.path.realpath(os.path.expanduser("~")) or root == "/":
            continue
        proj = _resolve_project_id_for_cwd(conn, real, cache)
        s = slot(proj, root, os.path.basename(root))
        if proj is not None and root not in s["pastas"]:
            s["pastas"].append(root)
        if pid in claude:
            s["claude"] += 1
            s["trabalhando"] = s["trabalhando"] or _transcript_recent(cwd)
        else:
            s["servidores"].append({"pid": pid, "cmd": servers[pid][:160]})
    by_name = {}
    for p in projects.values():
        by_name.setdefault(p["slug"], p["id"])
        if p["root_path"]:
            by_name.setdefault(os.path.basename(p["root_path"].rstrip("/")), p["id"])
    for app, name in ides:
        proj = by_name.get(name) or by_name.get(_slugify(name))
        s = slot(proj, name, name)
        if app not in s["ides"]:
            s["ides"].append(app)
    return {"projetos": out, "sem_cadastro": list(loose.values())}


def cmd_live(conn):
    res = {"schema": "osforge.live.v1", "gerado_em": _iso_utc(datetime.now(timezone.utc))}
    res.update(live_state(conn))
    print(json.dumps(res, ensure_ascii=False))


def _conversation(conn, pid, limit=50):
    msgs = [{"tipo": "orientacao", "id": r["id"], "ts": r["ts"], "texto": r["text"], "status": r["status"],
             "entregue_em": r["delivered_at"], "sessao": (r["delivered_session"] or "")[:8] or None}
            for r in conn.execute("SELECT * FROM inbox WHERE project_id=? ORDER BY id DESC LIMIT ?", (pid, limit))]
    runs = [dict(r, tipo_execucao=r["tipo"], tipo="execucao") for r in _runs_rows(conn, pid, limit)]
    return sorted(msgs + runs, key=lambda x: x["ts"])[-limit:]


def _resolve_project_id_for_cwd(conn, cwd, cache):
    """Mesma ordem de hooks/lib/project_id.py:resolve (sem o passo OSFORGE_PROJECT — o
    backfill varre históricos de MUITOS projetos, não 'esta sessão'): root_path (exato ou
    subdiretório) → remote_hash → slugify(basename). None quando nada casa. Reusa os
    helpers locais _git_out/_resolve_root/_remote_hash já usados por cmd_bind_project."""
    if not cwd:
        return None
    if cwd in cache:
        return cache[cwd]
    pid = None
    root = None
    if os.path.isdir(cwd):
        top = _git_out(["rev-parse", "--show-toplevel"], cwd)
        if top:
            common = _git_out(["rev-parse", "--path-format=absolute", "--git-common-dir"], cwd)
            root = (os.path.realpath(os.path.dirname(common))
                    if common and os.path.basename(common) == ".git" else os.path.realpath(top))
    if root:
        for r in conn.execute("SELECT id, root_path FROM projects").fetchall():
            rp = (r["root_path"] or "").rstrip("/")
            if rp and (cwd == rp or cwd.startswith(rp + os.sep) or root == rp):
                pid = r["id"]; break
    if pid is None and root:
        remote_url = _git_out(["config", "--get", "remote.origin.url"], root)
        rh = _remote_hash(remote_url) if remote_url else ""
        if rh:
            row = conn.execute("SELECT id FROM projects WHERE remote_hash=?", (rh,)).fetchone()
            if row:
                pid = row["id"]
    if pid is None:
        base = _slugify(os.path.basename(root or cwd))
        row = conn.execute("SELECT id FROM projects WHERE slug=?", (base,)).fetchone()
        if row:
            pid = row["id"]
    cache[cwd] = pid
    return pid

def cmd_backfill_calls(conn, root_dir=None):
    """Varre recursivamente transcripts JSONL (padrão ~/.claude/projects) e importa chamadas
    históricas — leitura apenas na fonte, idempotente (ON CONFLICT DO NOTHING; correr duas
    vezes não duplica). Projeto resolvido pelo `cwd` de cada transcript (B-028)."""
    base = os.path.expanduser(root_dir) if root_dir else os.path.expanduser("~/.claude/projects")
    if not os.path.isdir(base):
        _err(f"Diretório não encontrado: {base}")
    cache = {}
    total_rows = 0
    total_files = 0
    for path in Path(base).rglob("*.jsonl"):
        total_files += 1
        rows = []
        cwd = None
        sid = None
        seen = set()
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or '"usage"' not in line:
                        continue
                    try:
                        e = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(e, dict):
                        continue
                    if cwd is None and e.get("cwd"):
                        cwd = e.get("cwd")
                    if sid is None and (e.get("sessionId") or e.get("session_id")):
                        sid = e.get("sessionId") or e.get("session_id")
                    msg = e.get("message")
                    if not isinstance(msg, dict) or msg.get("role") != "assistant":
                        continue
                    u = msg.get("usage")
                    if not isinstance(u, dict):
                        continue
                    mid = msg.get("id") or e.get("uuid")
                    if not mid or mid in seen:
                        continue
                    seen.add(mid)
                    row = _row_from_entry(e, msg, u, sid or "")
                    if row:
                        rows.append(row)
        except OSError:
            continue
        if not rows:
            continue
        pid = _resolve_project_id_for_cwd(conn, cwd, cache) if cwd else None
        _insert_calls_rows(conn, pid, rows)
        total_rows += len(rows)
    _ok(f"backfill-calls: {total_files} arquivo(s) escaneado(s), {total_rows} chamada(s) processada(s)")


def cmd_add_observation(conn, project, trigger_text, context="", tool=""):
    """Grava uma observação de sessão para posterior clusterização via evolve."""
    conn.execute(
        "INSERT INTO observations (project, trigger_text, context, tool) VALUES (?,?,?,?)",
        (project, trigger_text, context, tool),
    )
    conn.commit()
    _ok(f"Observação gravada: [{project}] {trigger_text[:60]}")


# ── Helpers de clustering ────────────────────────────────────────────────────

_STRIP_VERBS = frozenset([
    "when", "creating", "writing", "adding", "implementing", "testing",
    "building", "running", "using", "making", "working", "editing",
    "reading", "fixing", "updating", "setting", "getting",
])

def _normalize_trigger(text):
    """Normaliza trigger para clustering: lower, strip stop-verbs, collapse spaces."""
    words = text.lower().split()
    filtered = [w for w in words if w not in _STRIP_VERBS]
    return " ".join(filtered).strip() or text.lower().strip()

def _classify_candidate(cluster_size, avg_conf):
    """Classifica candidato: AGENT (≥3, conf≥0.75) | COMMAND (conf≥0.70) | SKILL."""
    if cluster_size >= 3 and avg_conf >= 0.75:
        return "AGENT"
    if avg_conf >= 0.70:
        return "COMMAND"
    return "SKILL"

def _suggest_skill_diff(cluster_key, observations):
    """Gera diff textual sugerido para um SKILL candidate."""
    triggers = list({o["trigger_text"] for o in observations})
    lines = [
        f"--- /dev/null",
        f"+++ skills/{cluster_key.replace(' ', '-')}/SKILL.md",
        f"@@ -0,0 +1,18 @@",
        f"+---",
        f"+name: {cluster_key.replace(' ', '-')}",
        f'+description: |',
        f'+  ACIONE quando: {triggers[0]}',
    ]
    for t in triggers[1:]:
        lines.append(f'+  ACIONE quando: {t}')
    lines += [
        f"+---",
        f"+",
        f"# {cluster_key.title()}",
        f"+",
        f"# TODO: preencher guidance a partir das {len(observations)} observações",
    ]
    return "\n".join(lines)


def cmd_evolve(conn, project_slug=None, min_count=2):
    """Clusteriza observations por normalização de trigger e propõe candidates.

    Não escreve nenhum arquivo — apenas lista candidatos com diffs sugeridos.
    """
    q = "SELECT project, trigger_text, context, tool, created_at FROM observations"
    params = []
    if project_slug:
        q += " WHERE project=?"
        params.append(project_slug)
    q += " ORDER BY created_at"
    rows = conn.execute(q, params).fetchall()

    if not rows:
        _out("Nenhuma observation registrada. Use 'add-observation' para capturar padrões.")
        return

    # Agrupar por trigger normalizado — usa apenas a 1ª palavra de conteúdo (substantivo-sujeito)
    # Ex: "when writing tests prefer TDD" e "when writing tests use red-green"
    # → norm = "tests prefer tdd" / "tests use red-green" → key = "tests" em ambos
    clusters = {}  # norm_key → list[Row]
    for row in rows:
        normalized = _normalize_trigger(row["trigger_text"])
        words = normalized.split()
        key = words[0] if words else normalized  # 1ª palavra = substantivo-sujeito
        clusters.setdefault(key, []).append(row)

    # Filtrar clusters com tamanho ≥ min_count
    candidates = {k: v for k, v in clusters.items() if len(v) >= min_count}

    if not candidates:
        total = len(rows)
        _out(f"{total} observation(s) registrada(s), nenhum cluster ≥ {min_count}. "
             "Continue capturando padrões.")
        return

    # Ordenar por tamanho desc
    sorted_cands = sorted(candidates.items(), key=lambda kv: len(kv[1]), reverse=True)

    label = f"projeto={project_slug}" if project_slug else "global"
    _out(f"{'='*60}")
    _out(f"  EVOLVE ANALYSIS — {len(rows)} observation(s), {label}")
    _out(f"  Clusters ≥ {min_count}: {len(sorted_cands)}")
    _out(f"{'='*60}")
    _out("")

    skill_cands, cmd_cands, agent_cands = [], [], []
    for key, obs in sorted_cands:
        avg_conf = 0.5 + min(0.3, len(obs) * 0.05)  # heurística: mais obs → mais conf
        kind = _classify_candidate(len(obs), avg_conf)
        entry = (key, obs, avg_conf)
        if kind == "AGENT":
            agent_cands.append(entry)
        elif kind == "COMMAND":
            cmd_cands.append(entry)
        else:
            skill_cands.append(entry)

    if skill_cands:
        _out(f"## SKILL CANDIDATES ({len(skill_cands)})")
        for i, (key, obs, conf) in enumerate(skill_cands, 1):
            _out(f"\n{i}. Cluster: \"{key}\"")
            _out(f"   Observações: {len(obs)} | conf estimada: {conf:.0%}")
            projects = list({o['project'] for o in obs if o['project']})
            if projects:
                _out(f"   Projetos: {', '.join(projects)}")
            _out(f"\n   Diff sugerido:")
            for line in _suggest_skill_diff(key, obs).splitlines():
                _out(f"   {line}")

    if cmd_cands:
        _out(f"\n## COMMAND CANDIDATES ({len(cmd_cands)})")
        for i, (key, obs, conf) in enumerate(cmd_cands, 1):
            slug = key.replace(" ", "-")
            _out(f"\n{i}. /{slug}")
            _out(f"   Observações: {len(obs)} | conf estimada: {conf:.0%}")
            _out(f"   Criar: commands/{slug}.md")

    if agent_cands:
        _out(f"\n## AGENT CANDIDATES ({len(agent_cands)})")
        for i, (key, obs, conf) in enumerate(agent_cands, 1):
            slug = key.replace(" ", "-")
            _out(f"\n{i}. {slug}-agent")
            _out(f"   Cobre {len(obs)} observações | conf estimada: {conf:.0%}")
            _out(f"   Criar: agents/{slug}.md")

    _out(f"\n{'='*60}")
    _out("Para promover um candidato como instinct:")
    _out("  osforge-db add-observation <project> '<trigger>' --context='...'")
    _out("  # revise e edite skills/ ou rules/ manualmente após aprovação humana")

    if _json_mode:
        out = []
        for key, obs, conf in (skill_cands + cmd_cands + agent_cands):
            kind = _classify_candidate(len(obs), conf)
            out.append({
                "cluster": key,
                "kind": kind,
                "count": len(obs),
                "confidence": round(conf, 2),
                "projects": list({o["project"] for o in obs if o["project"]}),
            })
        print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_list_instincts(conn, project=None, scope=None):
    """Lista instincts promovidos, opcionalmente filtrados por projeto ou scope."""
    q = "SELECT id, trigger, guidance, confidence, domain, scope, project, seen_count, created_at FROM instincts WHERE 1=1"
    params = []
    if project:
        q += " AND project=?"
        params.append(project)
    if scope:
        if scope not in ("project", "global"):
            _err("scope deve ser 'project' ou 'global'")
        q += " AND scope=?"
        params.append(scope)
    q += " ORDER BY confidence DESC, seen_count DESC"
    rows = conn.execute(q, params).fetchall()
    if _json_mode:
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False, indent=2))
        return
    if not rows:
        _out("Nenhum instinct registrado.")
        return
    for r in rows:
        conf_pct = f"{r['confidence']:.0%}"
        proj_tag = f" [{r['project']}]" if r["project"] else ""
        _out(f"#{r['id']} [{r['scope']:7}]{proj_tag} conf={conf_pct} seen={r['seen_count']}")
        _out(f"   trigger:  {r['trigger']}")
        if r["guidance"]:
            short = textwrap.shorten(r["guidance"], width=80, placeholder="…")
            _out(f"   guidance: {short}")
        if r["domain"]:
            _out(f"   domain:   {r['domain']}")


def cmd_promote_instinct(conn, instinct_id, scope="global"):
    """Promove instinct para scope global (exige confidence ≥ 0.8)."""
    try:
        iid = int(instinct_id)
    except ValueError:
        _err(f"instinct_id inválido: '{instinct_id}'")
    row = conn.execute(
        "SELECT id, trigger, confidence, scope FROM instincts WHERE id=?", (iid,)
    ).fetchone()
    if not row:
        _err(f"Instinct #{iid} não encontrado. Use 'list-instincts' para ver os ids.")
    if row["scope"] == scope:
        _err(f"Instinct #{iid} já está em scope '{scope}'.")
    if row["confidence"] < 0.8:
        _err(
            f"Instinct #{iid} tem confidence {row['confidence']:.0%} < 80%. "
            "Aumente seen_count registrando mais observações antes de promover."
        )
    now = _now()
    conn.execute(
        "UPDATE instincts SET scope=?, project='', updated_at=? WHERE id=?",
        (scope, now, iid),
    )
    conn.commit()
    _ok(f"Instinct #{iid} promovido para scope='{scope}': {row['trigger'][:60]}")


def cmd_import_yaml(conn, yaml_path, slug):
    """Migra um status.yaml existente para o banco."""
    try:
        import yaml
    except ImportError:
        _err("PyYAML não instalado. Use: pip install pyyaml --break-system-packages")
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    if not data:
        _err(f"Arquivo vazio ou inválido: {yaml_path}")

    desc = data.get("description", slug)
    triage = data.get("triage", "standard")
    status = data.get("status", "active")
    cmd_upsert_project(conn, slug, desc, triage, status)

    p = _get_project(conn, slug)
    for ph in data.get("phases", []):
        conn.execute("""
            INSERT INTO phases (project_id, name, status, skill_path,
                                artifact_path, started_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(project_id, name) DO NOTHING
        """, (p["id"], ph.get("name","?"), ph.get("status","pending"),
              ph.get("skill"), ph.get("artifact"),
              ph.get("started"), ph.get("completed")))

    # Detectar fase atual (in-progress)
    current = next((ph["name"] for ph in data.get("phases", [])
                    if ph.get("status") == "in-progress"), None)
    if current:
        conn.execute("""
            UPDATE state SET current_phase=?, updated_at=?
            WHERE project_id=?
        """, (current, _now(), p["id"]))
    conn.commit()
    _ok(f"Import concluído: '{slug}' com {len(data.get('phases',[]))} fases")

# ── Main ──────────────────────────────────────────────────────────────────

# ── Brain (long-term memory, ADR-017) ────────────────────────────────────────
# Commands that never need the SQLite workbench (except migrate, which reads it).

_BRAIN_MODES = ("dense", "keyword", "hybrid")


def _brain_short(rec):
    proj = rec.get("project") or "global"
    day = (rec.get("created_at") or "")[:10]
    return f"#{(rec.get('id') or '')[:8]} [{rec.get('kind')}] {proj} ({day})"


def cmd_remember(text, kind, project, is_global, tags):
    if not kind:
        _err(f"remember needs --kind={'|'.join(_brain.KINDS)}")
    try:
        rec, indexed, why = _brain.remember(text, kind, None if is_global else project, tags)
    except _brain.BrainError as e:
        _err(f"remember: {e}")
    if _json_mode:
        print(json.dumps({"id": rec["id"], "kind": rec["kind"], "project": rec["project"],
                          "tags": rec["tags"], "created_at": rec["created_at"],
                          "indexed": indexed, "degraded": why}, ensure_ascii=False))
        return
    _ok(f"remembered {_brain_short(rec)}")
    if not indexed:
        print(f"note: brain degraded ({why}) — journaled only; "
              "`osforge-db brain rebuild` indexes it later")


def cmd_recall(query, kind, project, is_global, since, until, top, mode):
    if mode not in _BRAIN_MODES:
        _err(f"--mode must be one of {', '.join(_BRAIN_MODES)}")
    if kind and kind not in _brain.KINDS:
        _err(f"--kind must be one of {', '.join(_brain.KINDS)}")
    since_ts, until_ts = _brain.day_range(since, until)
    flt = {"kind": kind, "project": None if is_global else project, "global": is_global,
           "since_ts": since_ts, "until_ts": until_ts}
    rows, degraded = _brain.recall(query, flt, top, mode)
    if _json_mode:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if degraded:
        print(f"note: brain degraded ({degraded}) — lexical fallback")
    if not rows:
        _out(f"Nothing found for '{query}'")
        return
    for r in rows:
        tags = f" {{{','.join(r['tags'])}}}" if r.get("tags") else ""
        content = (r.get("content") or "").replace("\n", " ")
        short = content if len(content) <= 160 else content[:157] + "..."
        print(f"  {_brain_short(r)} score={r['score']}{tags} {short}")


def cmd_forget(id_or_prefix):
    try:
        rec, deleted, why = _brain.forget(id_or_prefix)
    except _brain.BrainError as e:
        _err(f"forget: {e}")
    if _json_mode:
        print(json.dumps({"id": rec["id"], "deleted": deleted, "degraded": why}))
        return
    _ok(f"forgot {_brain_short(rec)}")
    if not deleted:
        print(f"note: brain degraded ({why}) — tombstone journaled; "
              "`osforge-db brain rebuild` drops it from the index")


def cmd_brain_status():
    st = _brain.status()
    if _json_mode:
        print(json.dumps(st, indent=2))
        return
    where = st["url"] if st["store"] == "server" else st["path"]
    print(f"brain store:  {st['store']} {where} (collection {st['collection']})")
    print(f"embedder:     {st['embed']} ({st['model']})")
    print(f"venv:         {st['venv']}")
    print(f"journal:      {st['journal']} — {st['journal_live']} live, "
          f"{st['journal_forgotten']} forgotten")
    pts = st["points"] if st["points"] is not None else "?"
    print(f"indexed:      {pts} points" + ("  (pending: run `osforge-db brain rebuild`)"
                                           if st["pending"] else ""))
    if st["degraded"]:
        print(f"note: brain degraded ({st['degraded']}) — recall uses a lexical scan of the journal")


def cmd_brain_rebuild():
    ok, res = _brain.rebuild()
    if not ok:
        _err(f"brain rebuild failed: {res} (the journal is intact)")
    if _json_mode:
        print(json.dumps({"ok": True, "points": res.get("n")}))
        return
    _ok(f"brain rebuilt from the journal: {res.get('n')} points")


def cmd_brain_migrate(conn):
    rows = conn.execute("""
        SELECT d.id, d.content, d.category, d.created_at, p.slug
        FROM decisions d JOIN projects p ON p.id = d.project_id ORDER BY d.id
    """).fetchall()
    try:
        added, indexed, why = _brain.migrate_decisions(
            {"id": r["id"], "content": r["content"], "category": r["category"],
             "created_at": r["created_at"], "slug": r["slug"]} for r in rows)
    except _brain.BrainError as e:
        _err(f"brain migrate: {e}")
    if _json_mode:
        print(json.dumps({"added": added, "indexed": indexed, "degraded": why}))
        return
    _ok(f"brain migrate: {added} new decision(s) of {len(rows)} journaled, {indexed} indexed")
    if why:
        print(f"note: brain degraded ({why}) — journaled only; `osforge-db brain rebuild` indexes them later")


def cmd_brain_health(timeout):
    ok, why = _brain.health(timeout)
    if _json_mode:
        print(json.dumps({"ok": ok, "reason": why}))
    elif not ok:
        print(f"brain: degraded ({why}) — `osforge-db recall` falls back to a lexical scan")


def main():
    global _json_mode
    args = sys.argv[1:]
    if "--json" in args:
        _json_mode = True
        args = [a for a in args if a != "--json"]

    scope = _scope(args)
    args  = [a for a in args if not a.startswith("--scope=")]

    cat_arg      = next((a for a in args if a.startswith("--category=")), None)
    wait_arg     = next((a for a in args if a.startswith("--waiting=")), None)
    proj_arg     = next((a for a in args if a.startswith("--project=")), None)
    limit_arg    = next((a for a in args if a.startswith("--limit=")), None)
    status_arg   = next((a for a in args if a.startswith("--status=")), None)
    phase_arg    = next((a for a in args if a.startswith("--phase=")), None)
    wave_arg     = next((a for a in args if a.startswith("--wave=")), None)
    deps_arg     = next((a for a in args if a.startswith("--depends=")), None)
    prio_arg     = next((a for a in args if a.startswith("--priority=")), None)
    ctx_arg      = next((a for a in args if a.startswith("--context=")), None)
    tool_arg     = next((a for a in args if a.startswith("--tool=")), None)
    mincount_arg = next((a for a in args if a.startswith("--min-count=")), None)
    scope_arg    = next((a for a in args if a.startswith("--scope=")), None)
    top_arg      = next((a for a in args if a.startswith("--top=")), None)
    source_arg   = next((a for a in args if a.startswith("--source=")), None)
    root_arg     = next((a for a in args if a.startswith("--root=")), None)
    since_arg    = next((a for a in args if a.startswith("--since=")), None)
    by_arg       = next((a for a in args if a.startswith("--by=")), None)
    older_arg    = next((a for a in args if a.startswith("--older-than=")), None)
    until_arg    = next((a for a in args if a.startswith("--until=")), None)
    timeout_arg  = next((a for a in args if a.startswith("--timeout=")), None)
    kind_arg     = next((a for a in args if a.startswith("--kind=")), None)
    tags_arg     = next((a for a in args if a.startswith("--tags=")), None)
    mode_arg     = next((a for a in args if a.startswith("--mode=")), None)
    is_global    = "--global" in args
    _flags = [x for x in args if x.startswith("--")]      # capturado agora: `args` é filtrado adiante
    def _intflag(name, default=0):
        a = next((x for x in _flags if x.startswith(f"--{name}=")), None)
        try:
            return int(a.split("=", 1)[1]) if a else default
        except ValueError:
            return default
    session_arg  = next((a for a in args if a.startswith("--session=")), None)
    model_arg    = next((a for a in args if a.startswith("--model=")), None)
    remote_arg   = next((a for a in args if a.startswith("--remote=")), None)
    detail_arg   = next((a for a in args if a.startswith("--detail=")), None)
    category   = cat_arg.split("=",1)[1]      if cat_arg      else None
    waiting    = wait_arg.split("=",1)[1]     if wait_arg      else None
    proj_flt   = proj_arg.split("=",1)[1]     if proj_arg      else None
    limit      = int(limit_arg.split("=",1)[1]) if limit_arg   else 5
    st_flag    = status_arg.split("=",1)[1]   if status_arg    else None
    st_filter  = st_flag if st_flag else "active"
    phase_flt  = phase_arg.split("=",1)[1]    if phase_arg     else None
    wave_flt   = wave_arg.split("=",1)[1]     if wave_arg      else None
    deps_flt   = deps_arg.split("=",1)[1]     if deps_arg      else None
    prio_flt   = prio_arg.split("=",1)[1]     if prio_arg      else None
    ctx_flt    = ctx_arg.split("=",1)[1]      if ctx_arg       else ""
    tool_flt   = tool_arg.split("=",1)[1]     if tool_arg      else ""
    min_count  = int(mincount_arg.split("=",1)[1]) if mincount_arg else 2
    scope_flt  = scope_arg.split("=",1)[1]    if scope_arg     else None
    top_flt    = int(top_arg.split("=",1)[1])  if top_arg       else 5
    source_flt = source_arg.split("=",1)[1]   if source_arg    else "decisions"
    root_flt   = root_arg.split("=",1)[1]     if root_arg      else None
    since_flt  = since_arg.split("=",1)[1]    if since_arg     else None
    by_flt     = by_arg.split("=",1)[1]       if by_arg        else None
    older_flt  = older_arg.split("=",1)[1]    if older_arg     else "90d"
    until_flt  = until_arg.split("=",1)[1]    if until_arg     else None
    try:
        timeout_flt = float(timeout_arg.split("=",1)[1]) if timeout_arg else 0.3
    except ValueError:
        timeout_flt = 0.3
    session_flt = session_arg.split("=",1)[1] if session_arg   else None
    model_flt  = model_arg.split("=",1)[1]    if model_arg     else None
    remote_flt = remote_arg.split("=",1)[1]   if remote_arg    else None
    detail_flt = detail_arg.split("=",1)[1]   if detail_arg    else None
    kind_flt   = kind_arg.split("=",1)[1]     if kind_arg      else None
    tags_flt   = [t for t in tags_arg.split("=",1)[1].split(",") if t.strip()] if tags_arg else []
    mode_flt   = mode_arg.split("=",1)[1]     if mode_arg      else "dense"
    args = [a for a in args if not a.startswith("--")]

    if not args:
        try:
            sys.stdout.write(__doc__ + "\n")
            sys.stdout.flush()
        except BrokenPipeError:
            # `osforge-db | grep -q x` / `| head`: the reader left early; that is not an error.
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(0)

    cmd = args[0]
    rest = args[1:]

    # Decision searches take whole days; `calls` keeps its own relative --since (5h/7d).
    day_since = day_until = None
    if cmd in ("search", "search-hybrid", "list-decisions", "recall"):
        day_since = _parse_day(since_flt, "--since") if since_flt else None
        day_until = _parse_day(until_flt, "--until") if until_flt else None

    # Brain commands that never touch the SQLite workbench
    if cmd == "remember":
        if not rest:
            _err("Usage: remember \"<text>\" --kind=decision|knowledge|technique|methodology "
                 "[--project=slug|--global] [--tags=a,b]")
        cmd_remember(" ".join(rest), kind_flt, proj_flt, is_global, tags_flt)
        return
    if cmd == "recall":
        if not rest:
            _err("Usage: recall \"<query>\" [--kind=] [--project=slug|--global] [--since=YYYY-MM-DD] "
                 "[--until=YYYY-MM-DD] [--top=5] [--mode=dense|keyword|hybrid] [--json]")
        cmd_recall(" ".join(rest), kind_flt, proj_flt, is_global, day_since, day_until,
                   top_flt, mode_flt)
        return
    if cmd == "forget":
        if not rest:
            _err("Usage: forget <id|id-prefix>")
        cmd_forget(rest[0])
        return
    if cmd == "brain" and (rest[:1] or [""])[0] in ("status", "rebuild", "health"):
        {"status": cmd_brain_status, "rebuild": cmd_brain_rebuild,
         "health": lambda: cmd_brain_health(timeout_flt)}[rest[0]]()
        return

    conn = get_conn(scope)
    # Auto-init sempre
    conn.executescript(SCHEMA)
    conn.executescript(TRIGGERS)
    migrate(conn)

    if cmd == "init":
        cmd_init(conn, sys.argv[1:])
    elif cmd == "upsert-project":
        if len(rest) < 2:
            _err("Uso: upsert-project <slug> <desc> [triage] [status]")
        if len(rest) > 3 and rest[3] not in PROJECT_STATUSES:
            _err2(f"status inválido '{rest[3]}'. Use: {'|'.join(PROJECT_STATUSES)}")
        cmd_upsert_project(conn, rest[0], rest[1],
                           rest[2] if len(rest)>2 else "standard",
                           rest[3] if len(rest)>3 else "active")
        if root_flt or remote_flt:
            cmd_bind_project(conn, rest[0], root_flt, remote_flt)
    elif cmd == "bind-project":
        if not rest:
            _err("Uso: bind-project <slug> [--root=DIR|.] [--remote=URL|auto]")
        cmd_bind_project(conn, rest[0], root_flt, remote_flt)
    elif cmd == "set-phase":
        if len(rest) < 3:
            _err("Uso: set-phase <slug> <phase> <status> [skill] [artifact]")
        cmd_set_phase(conn, rest[0], rest[1], rest[2],
                      rest[3] if len(rest)>3 else None,
                      rest[4] if len(rest)>4 else None)
    elif cmd == "set-resume":
        if len(rest) < 2:
            _err("Uso: set-resume <slug> <resume_point>")
        cmd_set_resume(conn, rest[0], " ".join(rest[1:]))
    elif cmd == "add-decision":
        if len(rest) < 2:
            _err("Uso: add-decision <slug> <content> [--category=arch]")
        cmd_add_decision(conn, rest[0], " ".join(rest[1:]),
                         category or "arch", scope)
    elif cmd == "add-blocker":
        if len(rest) < 2:
            _err("Uso: add-blocker <slug> <description> [--waiting=<what>]")
        cmd_add_blocker(conn, rest[0], " ".join(rest[1:]), waiting)
    elif cmd == "resolve-blocker":
        if len(rest) < 2:
            _err("Uso: resolve-blocker <slug> <blocker_id>")
        cmd_resolve_blocker(conn, rest[0], int(rest[1]))
    elif cmd == "list-blockers":
        if not rest:
            _err("Uso: list-blockers <slug>")
        cmd_list_blockers(conn, rest[0])
    elif cmd == "list-decisions":
        if not rest:
            _err("Uso: list-decisions <slug> [--category=] [--limit=10] "
                 "[--since=YYYY-MM-DD] [--until=YYYY-MM-DD]")
        cmd_list_decisions(conn, rest[0], category, limit, day_since, day_until)
    elif cmd == "status":
        if not rest:
            _err("Uso: status <slug>")
        cmd_status(conn, rest[0])
    elif cmd == "resume":
        if not rest:
            _err("Uso: resume <slug>")
        cmd_resume(conn, rest[0])
    elif cmd == "search":
        if not rest:
            _err("Uso: search <query> [--project=slug] [--limit=5] "
                 "[--since=YYYY-MM-DD] [--until=YYYY-MM-DD]")
        cmd_search(conn, " ".join(rest), proj_flt, limit, day_since, day_until)
    elif cmd == "add-task":
        if len(rest) < 2:
            _err("Uso: add-task <slug> <title> [--phase=] [--wave=N] "
                 "[--depends=1,2] [--priority=p0|p1|p2]")
        cmd_add_task(conn, rest[0], " ".join(rest[1:]),
                     phase_flt, wave_flt, deps_flt, prio_flt or "p1")
    elif cmd == "set-task":
        if len(rest) < 3:
            _err("Uso: set-task <slug> <task_id> <status>")
        cmd_set_task(conn, rest[0], rest[1], rest[2])
    elif cmd == "list-tasks":
        if not rest:
            _err("Uso: list-tasks <slug> [--status=<status>]")
        cmd_list_tasks(conn, rest[0], st_flag)
    elif cmd == "board":
        cmd_board(conn, st_filter)
    elif cmd == "list-projects":
        cmd_list_projects(conn, st_filter)
    elif cmd == "stats":
        cmd_stats(conn)
    elif cmd == "add-usage":
        if not rest or not session_flt or not model_flt:
            _err("Uso: add-usage <slug> --session=ID --model=M --input=N --output=N [--cache-read=N] [--cache-create=N] [--turns=N]")
        cmd_add_usage(conn, rest[0], session_flt, model_flt, _intflag("input"), _intflag("output"),
                      _intflag("cache-read"), _intflag("cache-create"), _intflag("turns"))
    elif cmd == "usage":
        if not rest:
            _err("Uso: usage <slug>")
        cmd_usage(conn, rest[0])
    elif cmd == "add-calls":
        if not rest:
            _err("Uso: add-calls <slug> --stdin")
        cmd_add_calls(conn, rest[0])
    elif cmd == "calls":
        cmd_calls(conn, proj_flt, since_flt, by_flt)
    elif cmd == "prune-calls":
        cmd_prune_calls(conn, older_flt)
    elif cmd == "backfill-calls":
        cmd_backfill_calls(conn, rest[0] if rest else None)
    elif cmd == "set-project-status":
        if len(rest) < 2:
            _err2(f"Uso: set-project-status <slug> {'|'.join(PROJECT_STATUSES)}")
        cmd_set_project_status(conn, rest[0], rest[1])
    elif cmd == "monitor":
        try:
            m_days = int(next((x.split("=", 1)[1] for x in _flags if x.startswith("--days=")), "30"))
        except ValueError:
            _err2("--days precisa ser um inteiro")
        cmd_monitor(conn, rest[0] if rest else None, m_days, "--discover" in _flags,
                    "--all" in _flags, "--compact" in _flags, "--live" in _flags)
    elif cmd == "live":
        cmd_live(conn)
    elif cmd == "inbox-add":
        if len(rest) < 2:
            _err2("Uso: inbox-add <slug> <texto> [--via=painel]")
        via = next((x.split("=", 1)[1] for x in _flags if x.startswith("--via=")), "painel")
        cmd_inbox_add(conn, rest[0], " ".join(rest[1:]), via)
    elif cmd == "inbox-take":
        if not rest:
            _err2("Uso: inbox-take <slug> --session=ID")
        cmd_inbox_take(conn, rest[0], session_flt)
    elif cmd == "inbox":
        if not rest:
            _err2("Uso: inbox <slug>")
        cmd_inbox_list(conn, rest[0])
    elif cmd == "inbox-cancel":
        if not rest:
            _err2("Uso: inbox-cancel <id>")
        cmd_inbox_cancel(conn, rest[0])
    elif cmd == "run-add":
        if not rest:
            _err2("Uso: run-add <slug> --kind=terminal|background|ide [--tool=] [--prompt=] [--pid=] [--log=] [--status=]")
        fl = {x.split("=", 1)[0][2:]: x.split("=", 1)[1] for x in _flags if "=" in x}
        cmd_run_add(conn, rest[0], fl.get("kind", ""), fl.get("tool", ""), fl.get("prompt", ""),
                    int(fl["pid"]) if fl.get("pid", "").isdigit() else None, fl.get("log"),
                    fl.get("status", "iniciada"))
    elif cmd == "run-update":
        if not rest:
            _err2("Uso: run-update <id> [--status=] [--pid=] [--result=] [--cost=] [--log=]")
        fl = {x.split("=", 1)[0][2:]: x.split("=", 1)[1] for x in _flags if "=" in x}
        try:
            cost = float(fl["cost"]) if "cost" in fl else None
        except ValueError:
            _err2("--cost precisa ser número")
        cmd_run_update(conn, rest[0], fl.get("status"), int(fl["pid"]) if fl.get("pid", "").isdigit() else None,
                       fl.get("result"), cost, fl.get("log"))
    elif cmd == "runs":
        if not rest:
            _err2("Uso: runs <slug>")
        cmd_runs(conn, rest[0])
    elif cmd == "add-signal":
        if len(rest) < 3:
            _err2("Uso: add-signal <slug> <callers_open|duplicate|tests> <subject> "
                  "[--detail=JSON] [--session=ID]")
        cmd_add_signal(conn, rest[0], rest[1], " ".join(rest[2:]), detail_flt, session_flt)
    elif cmd == "resolve-signal":
        if not rest:
            _err2("Uso: resolve-signal <id> [<id>...]")
        cmd_resolve_signal(conn, rest)
    elif cmd == "signals":
        cmd_signals(conn, rest[0] if rest else None, "--open" in _flags, "--report" in _flags,
                    since_flt)
    elif cmd == "import-yaml":
        if len(rest) < 2:
            _err("Uso: import-yaml <yaml_path> <slug>")
        cmd_import_yaml(conn, rest[0], rest[1])
    elif cmd == "add-observation":
        if len(rest) < 2:
            _err("Uso: add-observation <project> <trigger_text> [--context=<ctx>] [--tool=<tool>]")
        cmd_add_observation(conn, rest[0], " ".join(rest[1:]), ctx_flt, tool_flt)
    elif cmd == "evolve":
        cmd_evolve(conn, proj_flt, min_count)
    elif cmd == "list-instincts":
        cmd_list_instincts(conn, proj_flt, scope_flt)
    elif cmd == "promote-instinct":
        if not rest:
            _err("Uso: promote-instinct <instinct_id> [--scope=global]")
        cmd_promote_instinct(conn, rest[0], scope_flt or "global")
    elif cmd == "embed":
        if len(rest) < 3:
            _err("Uso: embed <source_table> <source_id> <text...>")
        cmd_embed(conn, rest[0], rest[1], " ".join(rest[2:]))
    elif cmd == "embed-backfill":
        cmd_embed_backfill(conn, source_flt)
    elif cmd == "search-semantic":
        if not rest:
            _err("Uso: search-semantic <query> [--top=5]")
        cmd_search_semantic(conn, " ".join(rest), top_flt)
    elif cmd == "search-hybrid":
        if not rest:
            _err("Uso: search-hybrid <query> [--project=slug] [--top=5] "
                 "[--since=YYYY-MM-DD] [--until=YYYY-MM-DD]")
        cmd_search_hybrid(conn, " ".join(rest), top_flt, proj_flt, day_since, day_until)
    elif cmd == "vec-status":
        cmd_vec_status(conn)
    elif cmd == "memory-health":
        cmd_memory_health(conn, timeout_flt)
    elif cmd == "vec-init":
        cmd_vec_init(conn)
    elif cmd == "brain":
        if rest[:1] != ["migrate"]:
            _err("Usage: brain status|rebuild|migrate|health [--timeout=0.3]")
        if scope != "global":
            _err("brain migrate reads the global workbench only (drop --scope=local)")
        cmd_brain_migrate(conn)
    else:
        _err(f"Comando desconhecido: '{cmd}'. Use 'osforge-db' sem args para ajuda.")

    conn.close()

if __name__ == "__main__":
    main()
