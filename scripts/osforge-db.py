#!/usr/bin/env python3
"""
osforge-db — SQLite state manager para o OSForge
Uso: osforge-db <comando> [args] [--scope=local|global] [--json]

Escopo global:  ~/.osforge/osforge.db  (padrão — cross-project)
Escopo local:   .osforge/osforge.db    (por projeto — via --scope=local)

Comandos:
  init                              Cria banco e schema
  status <slug>                     Estado atual do projeto (para INTAKE)
  resume <slug>                     Resume point compacto (para shell injection)
  upsert-project <slug> <desc> <triage> <status>
  set-phase <slug> <phase> <status> [skill] [artifact]
  set-resume <slug> <resume_point>
  add-decision <slug> <content> [--category=arch|product|ux|data|security]
  add-blocker <slug> <description> [--waiting=<what>]
  resolve-blocker <slug> <blocker_id>
  list-blockers <slug>
  list-decisions <slug> [--category=<cat>] [--limit=10]
  add-task <slug> <title> [--phase=<name>] [--wave=N] [--depends=1,2] [--priority=p0|p1|p2]
  set-task <slug> <task_id> <status>   status: pending|in-progress|done|blocked|cancelled
  list-tasks <slug> [--status=<status>]
  board [--status=active|all]          Visão cross-project de tasks
  search <query> [--project=<slug>] [--limit=5]
  list-projects [--status=active|all]
  import-yaml <yaml_path> <slug>    Migra status.yaml existente
  stats                             Resumo geral do banco

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
  search-hybrid <query> [--top=5]
                                    RRF(FTS5 + vetor). Degrada para FTS5 se off.
  vec-status                        Backend ativo, provider, modelo, contagem.
                                    Se qdrant: mostra saúde + total de pontos.

  Variáveis de ambiente:
    OSFORGE_EMBED       ollama (padrão) | off | mock | voyage | openai
    OSFORGE_EMBED_MODEL Modelo para o provider (default ollama: bge-m3 multilíngue; ex: nomic-embed-text, voyage-3-lite)
    OSFORGE_VECTOR      sqlite (padrão) | qdrant
    OSFORGE_QDRANT_URL  URL do Qdrant (padrão: http://localhost:6333)
    OSFORGE_COLLECTION  Nome da coleção Qdrant (padrão: osforge_memory)
    OSFORGE_CONFIG      Caminho alternativo para config.json (para testes isolados)
    VOYAGE_API_KEY      Chave para voyage
    OPENAI_API_KEY      Chave para openai
"""

import sqlite3, sys, os, json, textwrap, math, hashlib, struct
from array import array
from datetime import datetime, timezone
from pathlib import Path
from urllib import request as _urllib_request

# numpy é OPCIONAL — acelerador; resultado idêntico ao pure-Python
try:
    import numpy as _np
    _HAS_NUMPY = True
except ImportError:
    _np = None
    _HAS_NUMPY = False

# ── Localização do banco ──────────────────────────────────────────────────

def db_path(scope="global"):
    if scope == "local":
        return Path(".osforge/osforge.db")
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
# OSFORGE_EMBED  = off (padrão) | mock | ollama | voyage | openai
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
    if _HAS_NUMPY:
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
    if _HAS_NUMPY:
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
    url = "http://localhost:11434/api/embeddings"
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

def cmd_search_hybrid(conn, query, top=5, project_slug=None):
    """RRF(FTS5 + vetor). Degrada para FTS5 puro se OSFORGE_EMBED=off."""
    top = int(top)
    if _EMBED_PROVIDER == "off":
        print("[osforge-db] aviso: OSFORGE_EMBED=off — busca hibrida degradou para FTS5.",
              file=sys.stderr)
        cmd_search(conn, query, project_slug, top)
        return

    # Lista A: FTS5
    fts_query = _fts_quote(query)
    if project_slug:
        fts_rows = conn.execute("""
            SELECT decisions.id
            FROM decisions_fts
            JOIN decisions ON decisions.id = decisions_fts.rowid
            JOIN projects  ON projects.id  = decisions.project_id
            WHERE decisions_fts MATCH ? AND projects.slug=?
            ORDER BY rank LIMIT ?
        """, (fts_query, project_slug, top * 3)).fetchall()
    else:
        fts_rows = conn.execute("""
            SELECT decisions.id
            FROM decisions_fts
            JOIN decisions ON decisions.id = decisions_fts.rowid
            WHERE decisions_fts MATCH ?
            ORDER BY rank LIMIT ?
        """, (fts_query, top * 3)).fetchall()
    fts_ranked = [str(r["id"]) for r in fts_rows]

    # Lista B: vetor
    q_vec = compute_embedding(query)
    if q_vec is None:
        print("[osforge-db] aviso: falha no embed da query — usando so FTS5.",
              file=sys.stderr)
        cmd_search(conn, query, project_slug, top)
        return

    vec_results = vstore_search(conn, q_vec, top * 3)
    vec_ranked = [sid for _, sid, _c, _s in
                  sorted(vec_results, key=lambda x: x[3], reverse=True)[:top * 3]]

    # RRF
    merged = _rrf_merge(fts_ranked, vec_ranked, k=60)[:top]

    if not merged:
        _out("Nenhum resultado encontrado.")
        return

    placeholders = ",".join("?" * len(merged))
    rows = conn.execute(
        f"SELECT d.id, d.category, d.content, p.slug as proj "
        f"FROM decisions d JOIN projects p ON p.id=d.project_id "
        f"WHERE d.id IN ({placeholders})",
        [int(m) for m in merged]
    ).fetchall()
    row_by_id = {str(r["id"]): r for r in rows}

    if _json_mode:
        out = []
        for sid in merged:
            r = row_by_id.get(sid)
            if r:
                out.append({"id": r["id"], "project": r["proj"],
                            "category": r["category"], "content": r["content"]})
        print(json.dumps(out, ensure_ascii=False))
        return

    _out(f"── Busca hibrida (RRF FTS5+vetor): '{query}' (top={top}) ──────────")
    for rank, sid in enumerate(merged, 1):
        r = row_by_id.get(sid)
        if not r:
            continue
        short = textwrap.shorten(r["content"], width=100, placeholder="...")
        _out(f"  #{rank} [{r['proj']}] [{r['category']}]  {short}")

def cmd_vec_status(conn):
    """Imprime provider ativo, backend vetorial, modelo, contagem por source_table.
    Se backend=qdrant, também mostra saúde e total de pontos na coleção.
    """
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

    if _json_mode:
        out = {
            "provider": provider,
            "model": model,
            "vector_backend": _VECTOR_BACKEND,
            "qdrant_url": _QDRANT_URL if _VECTOR_BACKEND == "qdrant" else None,
            "qdrant_collection": _QDRANT_COLLECTION if _VECTOR_BACKEND == "qdrant" else None,
            "qdrant_healthy": qdrant_healthy,
            "qdrant_points": qdrant_points,
            "numpy_available": _HAS_NUMPY,
            "sqlite_tables": [dict(r) for r in rows],
        }
        print(json.dumps(out, ensure_ascii=False))
        return

    _out("── vec-status ──────────────────────────────────────────────────────")
    _out(f"  provider       : {provider}")
    _out(f"  model          : {model}")
    _out(f"  vector_backend : {_VECTOR_BACKEND}")
    _out(f"  numpy          : {'sim (acelerador ativo)' if _HAS_NUMPY else 'nao (pure-Python)'}")
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
               content='decisions', content_rowid='id');

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

def cmd_init(conn, args):
    conn.executescript(SCHEMA)
    conn.executescript(TRIGGERS)
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

def cmd_add_decision(conn, slug, content, category="arch"):
    p = _get_project(conn, slug)
    cur = conn.execute("""
        INSERT INTO decisions (project_id, content, category)
        VALUES (?, ?, ?) RETURNING id
    """, (p["id"], content, category)).fetchone()
    conn.execute("UPDATE projects SET updated_at=? WHERE id=?",
                 (_now(), p["id"]))
    conn.commit()
    _ok(f"Decisão ({category}) adicionada a '{slug}'")
    # Auto-embed: best-effort, nunca falha a operação principal
    try:
        if _EMBED_PROVIDER != "off" and cur is not None:
            vec = compute_embedding(content)
            if vec is not None:
                upsert_vec_memory(conn, "decisions", str(cur[0]), content, vec)
    except Exception as _auto_embed_exc:
        print(f"[osforge-db] aviso: auto-embed falhou ({_auto_embed_exc})",
              file=sys.stderr)

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

def cmd_list_decisions(conn, slug, category=None, limit=10):
    p = _get_project(conn, slug)
    q = "SELECT id, category, content, created_at FROM decisions WHERE project_id=?"
    params = [p["id"]]
    if category:
        q += " AND category=?"
        params.append(category)
    q += " ORDER BY created_at DESC LIMIT ?"
    params.append(int(limit))
    rows = conn.execute(q, params).fetchall()
    if _json_mode:
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False))
        return
    for r in rows:
        _out(f"[{r['category']}] ({r['created_at'][:10]}) {r['content']}")

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
            out[proj["slug"]] = [dict(t) for t in tasks]
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
        if not tasks:
            _out(f"{proj['slug']}: sem tasks")
            continue
        by_status = {s: [] for s in _BOARD_ORDER}
        for t in tasks:
            by_status.setdefault(t["status"], []).append(t)
        _out(f"{proj['slug']}:")
        for s in _BOARD_ORDER:
            group = by_status.get(s) or []
            if s == "done":
                group = group[-3:]  # só as 3 últimas done
            for t in group:
                wave = f" wave:{t['wave']}" if t["wave"] is not None else ""
                _out(f"  [{s:11}] #{t['id']} {t['priority']}{wave} {t['title']}")

def _fts_quote(query):
    """Envolve cada termo em aspas para FTS5 — evita interpretação de - como operador."""
    terms = query.strip().split()
    return " ".join(f'"{t}"' for t in terms)

def cmd_search(conn, query, project_slug=None, limit=5):
    query = _fts_quote(query)
    if project_slug:
        rows = conn.execute("""
            SELECT d.category, d.content, d.created_at, p.slug
            FROM decisions_fts f
            JOIN decisions d ON d.id = f.rowid
            JOIN projects p ON p.id = d.project_id
            WHERE decisions_fts MATCH ? AND p.slug = ?
            ORDER BY rank LIMIT ?
        """, (query, project_slug, int(limit))).fetchall()
    else:
        rows = conn.execute("""
            SELECT d.category, d.content, d.created_at, p.slug
            FROM decisions_fts f
            JOIN decisions d ON d.id = f.rowid
            JOIN projects p ON p.id = d.project_id
            WHERE decisions_fts MATCH ?
            ORDER BY rank LIMIT ?
        """, (query, int(limit))).fetchall()
    if _json_mode:
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False))
        return
    if not rows:
        _out("Nenhum resultado")
        return
    for r in rows:
        short = textwrap.shorten(r["content"], width=100, placeholder="…")
        _out(f"[{r['slug']}][{r['category']}] {short}")

def cmd_list_projects(conn, status="active"):
    q = "SELECT slug, triage, status, description FROM projects"
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
    args = [a for a in args if not a.startswith("--")]

    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    rest = args[1:]

    conn = get_conn(scope)
    # Auto-init sempre
    conn.executescript(SCHEMA)
    conn.executescript(TRIGGERS)

    if cmd == "init":
        cmd_init(conn, sys.argv[1:])
    elif cmd == "upsert-project":
        if len(rest) < 2:
            _err("Uso: upsert-project <slug> <desc> [triage] [status]")
        cmd_upsert_project(conn, rest[0], rest[1],
                           rest[2] if len(rest)>2 else "standard",
                           rest[3] if len(rest)>3 else "active")
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
                         category or "arch")
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
            _err("Uso: list-decisions <slug> [--category=] [--limit=10]")
        cmd_list_decisions(conn, rest[0], category, limit)
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
            _err("Uso: search <query> [--project=slug] [--limit=5]")
        cmd_search(conn, " ".join(rest), proj_flt, limit)
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
            _err("Uso: search-hybrid <query> [--project=slug] [--top=5]")
        cmd_search_hybrid(conn, " ".join(rest), top_flt, proj_flt)
    elif cmd == "vec-status":
        cmd_vec_status(conn)
    elif cmd == "vec-init":
        cmd_vec_init(conn)
    else:
        _err(f"Comando desconhecido: '{cmd}'. Use 'osforge-db' sem args para ajuda.")

    conn.close()

if __name__ == "__main__":
    main()
