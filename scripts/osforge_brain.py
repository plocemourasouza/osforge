#!/usr/bin/env python3
"""
osforge_brain.py — the BRAIN half of OSForge memory (ADR-017).

  WORKBENCH = SQLite (osforge-db): projects, phases, tasks, blockers, the per-project
              decision log that resume/board read. Stdlib only.
  BRAIN     = Qdrant: long-term knowledge — kind ∈ {decision, knowledge, technique,
              methodology}. Dense vector (embeddinggemma-300m, in-process via fastembed)
              is the primary signal; a sparse BM25 vector is the fallback / keyword mode.

Source of truth is the append-only journal ~/.osforge/brain.jsonl. Every write goes to
the journal FIRST (content scrubbed of secrets), then to Qdrant. The collection is a
derived index: `brain rebuild` recreates it from the journal at any time.

This file has two halves:
  * stdlib side — imported by osforge-db: config, journal, lexical fallback, health,
    and the bridge that runs the venv side as a subprocess. Never imports anything
    outside the standard library at module level.
  * venv side — `python osforge_brain.py <op>` run with the interpreter of
    ~/.osforge/venv (qdrant-client, fastembed, onnxruntime). JSON in on stdin, JSON out
    on stdout. Heavy imports happen inside the functions that need them.

Embedders (OSFORGE_BRAIN_EMBED or config `brain_model`):
  gemma     google/embeddinggemma-300m, 768d (Gemma Terms of Use) — default
  e5-large  intfloat/multilingual-e5-large, 1024d (MIT) — license-clean alternative
  fake      deterministic hash embedder (dense + sparse), no model, no numpy — tests/CI
"""
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

KINDS = ("decision", "knowledge", "technique", "methodology")
DEFAULT_COLLECTION = "osforge_brain"
DEFAULT_URL = "http://localhost:6333"

# Pinned runtime of ~/.osforge/venv (deploy.sh installs exactly these).
VENV_PINS = ("fastembed==0.9.0", "qdrant-client==1.19.1", "onnxruntime==1.31.0")

# name → (fastembed model, dim, query prefix, document prefix, cache dir marker, min score)
# Prompts are required for gemma and e5 and fastembed does not add them.
# min score = dense cosine floor under which recall falls back to the BM25 leg.
EMBEDDERS = {
    "gemma": ("google/embeddinggemma-300m", 768,
              "task: search result | query: ", "title: none | text: ",
              "embeddinggemma-300m", 0.30),
    "e5-large": ("intfloat/multilingual-e5-large", 1024, "query: ", "passage: ",
                 "multilingual-e5-large", 0.80),
    "fake": ("fake-hash", 4096, "", "", None, 0.20),
}
BM25_MODEL = "Qdrant/bm25"
BM25_MARKER = "Qdrant--bm25"
BM25_LANGUAGE = "portuguese"      # measured better than the English stemmer on pt-BR data

# ── Query terms (shared with osforge-db's FTS builder) ─────────────────────────

STOPWORDS = frozenset("""
a o as os um uma uns umas de da do das dos dum duma em no na nos nas num numa por pelo pela
pelos pelas para pra pro com sem sob sobre entre ate e ou mas nem que se nao sim ja so mais
menos muito muita muitos muitas pouco ao aos este esta estes estas esse essa esses essas isso
isto aquele aquela aquilo ele ela eles elas eu tu voce voces nos vos me te lhe meu minha seu
sua nosso nossa qual quais quanto quantos quanta quantas quando onde como porque quem cujo
foi foram era eram ser estar estao sao tem ter teve tinha havia fica ficou faz fez vai vamos
deve pode depois antes entao tambem ainda assim cada todo toda todos todas outro outra mesmo
mesma algum alguma
the an and or but nor not yes of to in on at by for from with without into onto over under
about as is are was were be been being am do does did done have has had having it its this
that these those there here what which who whom whose when where why how than then so too
very can could should would will shall may might must we us our you your they them their he
she his her me my all any each some such only own same just also again now
decisao decisoes decidimos decidiu decidir decidido decision decisions decide decided
""".split())


def fold(term):
    """Lowercase, accents stripped — the same folding unicode61 remove_diacritics applies."""
    return "".join(c for c in unicodedata.normalize("NFKD", term.lower())
                   if not unicodedata.combining(c))


def query_terms(text):
    """Content words of `text` in order, lowercased (accents kept). Stopwords and words
    under 3 characters are dropped; if that leaves nothing, the raw words are returned."""
    seen, raw, kept = set(), [], []
    for m in re.finditer(r"\w+", text or ""):
        low = m.group(0).lower()
        if low in seen:
            continue
        seen.add(low)
        raw.append(low)
        folded = fold(low)
        if folded not in STOPWORDS and len(folded) >= 3:
            kept.append(low)
    return kept or raw


# ── Configuration (env > ~/.osforge/config.json > default) ──────────────────────

def _home():
    return Path(os.path.expanduser("~"))


def osforge_dir():
    return _home() / ".osforge"


def load_config():
    p = os.environ.get("OSFORGE_CONFIG", "").strip()
    path = Path(p) if p else osforge_dir() / "config.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _setting(env, key, default, cfg=None):
    v = os.environ.get(env, "").strip()
    if v:
        return v
    cfg = load_config() if cfg is None else cfg
    v = cfg.get(key)
    return str(v).strip() if v not in (None, "") else default


def enabled():
    """OSFORGE_BRAIN=off (or config brain=off) turns the automatic paths off: add-decision
    no longer remembers and health stays silent. Explicit commands still work."""
    return _setting("OSFORGE_BRAIN", "brain", "on").lower() not in ("off", "0", "false", "no")


def journal_path():
    return osforge_dir() / "brain.jsonl"


def pending_path():
    return osforge_dir() / "brain.pending"


def venv_python():
    return Path(_setting("OSFORGE_BRAIN_PYTHON", "brain_python",
                         str(osforge_dir() / "venv" / "bin" / "python")))


def models_dir():
    return Path(_setting("OSFORGE_BRAIN_MODELS", "brain_models", str(osforge_dir() / "models")))


def embed_name():
    name = _setting("OSFORGE_BRAIN_EMBED", "brain_model", "gemma").lower()
    return name if name in EMBEDDERS else "gemma"


def min_score():
    raw = _setting("OSFORGE_BRAIN_MIN_SCORE", "brain_min_score", "")
    try:
        return float(raw) if raw else EMBEDDERS[embed_name()][5]
    except ValueError:
        return EMBEDDERS[embed_name()][5]


def _url_answers(url, timeout):
    from urllib import request
    try:
        request.urlopen(url.rstrip("/") + "/collections", timeout=timeout).read(64)
        return True
    except Exception:
        return False


def store_settings(probe_timeout=0.3):
    """{'store': 'server'|'local', 'url', 'path', 'collection'}.
    Precedence: OSFORGE_BRAIN_STORE > config brain_store > provisioned by
    `deploy.sh --with-qdrant` (vector_backend=qdrant) > the URL answers in 300 ms > local."""
    cfg = load_config()
    url = _setting("OSFORGE_QDRANT_URL", "qdrant_url", DEFAULT_URL, cfg)
    store = _setting("OSFORGE_BRAIN_STORE", "brain_store", "", cfg).lower()
    if store not in ("server", "local"):
        if str(cfg.get("vector_backend", "")).lower() == "qdrant":
            store = "server"
        else:
            store = "server" if _url_answers(url, probe_timeout) else "local"
    return {
        "store": store,
        "url": url,
        "path": _setting("OSFORGE_BRAIN_PATH", "brain_path",
                         str(osforge_dir() / "brain" / "qdrant"), cfg),
        "collection": _setting("OSFORGE_BRAIN_COLLECTION", "brain_collection",
                               DEFAULT_COLLECTION, cfg),
    }


# ── Scrub (hooks/lib/scrub.py, same filter as every other persisted text) ────────

def _load_scrub():
    here = Path(__file__).resolve().parent
    cands = [here.parent / "hooks" / "lib", _home() / ".claude" / "hooks" / "lib",
             _home() / ".cursor" / "hooks" / "lib"]
    try:
        cands.append(Path((osforge_dir() / "repo-path").read_text().strip()) / "hooks" / "lib")
    except OSError:
        pass
    for d in cands:
        if (d / "scrub.py").is_file():
            sys.path.insert(0, str(d))
            try:
                from scrub import scrub as fn
                return fn
            except Exception:
                continue
            finally:
                sys.path.remove(str(d))
    return None


class BrainError(Exception):
    """A write the brain must refuse (journal unwritable, scrub missing, bad input)."""


def scrub_text(text):
    fn = _load_scrub()
    if fn is None:      # fail-secure: never persist text that could not be scrubbed
        raise BrainError("hooks/lib/scrub.py not found — refusing to persist unscrubbed text")
    return fn(text)


# ── Journal (source of truth) ────────────────────────────────────────────────────

def _now():
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def journal_append(entries):
    """Append entries (dicts) to the journal, flushed and fsynced before returning."""
    path = journal_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            try:
                import fcntl
                fcntl.flock(f, fcntl.LOCK_EX)
            except (ImportError, OSError):
                pass
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
    except OSError as e:
        raise BrainError(f"journal not writable ({path}: {e.strerror or e})")


def journal_read(path=None):
    """(live records in journal order, forgotten records, every source key ever seen)."""
    live, gone, sources = {}, {}, set()
    try:
        f = open(path or journal_path(), encoding="utf-8")
    except OSError:
        return [], [], sources
    with f:
        for ln in f:
            try:
                e = json.loads(ln)
            except ValueError:
                continue                       # a torn last line never breaks reading
            if not isinstance(e, dict):
                continue
            if e.get("op") == "remember" and e.get("id"):
                live[e["id"]] = e
                if e.get("source"):
                    sources.add(e["source"])
            elif e.get("op") == "forget" and e.get("id"):
                rec = live.pop(e["id"], None)
                if rec is not None:
                    gone[e["id"]] = rec
                if e.get("source"):
                    sources.add(e["source"])
    return list(live.values()), list(gone.values()), sources


def make_record(content, kind, project=None, tags=None, source="manual", created=None):
    if kind not in KINDS:
        raise BrainError(f"--kind must be one of {', '.join(KINDS)} (got {kind!r})")
    content = (content or "").strip()
    if not content:
        raise BrainError("empty content")
    created = created or _now()
    return {
        "op": "remember",
        "id": str(uuid.uuid4()),
        "kind": kind,
        "project": project or None,
        "tags": [t.strip() for t in (tags or []) if t and t.strip()],
        "created_at": iso(created),
        "created_ts": int(created.timestamp()),
        "source": source,
        "content": scrub_text(content),
    }


def decision_source_id(source):
    """'add-decision:12' / 'migrate:sqlite#12' → '12' (one SQLite decision, one memory)."""
    m = re.match(r"^(?:add-decision:|migrate:sqlite#)(\d+)$", source or "")
    return m.group(1) if m else None


# ── Filters + lexical fallback ───────────────────────────────────────────────────

def day_range(since=None, until=None):
    """Inclusive YYYY-MM-DD days → (since_ts, until_ts_exclusive), each None when absent."""
    def ts(day, plus):
        d = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(days=plus)
        return int(d.timestamp())
    return (ts(since, 0) if since else None, ts(until, 1) if until else None)


def matches(rec, flt):
    if flt.get("kind") and rec.get("kind") != flt["kind"]:
        return False
    if flt.get("global") and rec.get("project") is not None:
        return False
    if flt.get("project") and rec.get("project") != flt["project"]:
        return False
    ts = rec.get("created_ts") or 0
    if flt.get("since_ts") is not None and ts < flt["since_ts"]:
        return False
    if flt.get("until_ts") is not None and ts >= flt["until_ts"]:
        return False
    return True


def lexical_search(records, query, flt, top):
    """OR of the query's content words over the journal, accent-insensitive, idf-weighted."""
    import math
    terms = {fold(t) for t in query_terms(query)}
    if not terms:
        return []
    docs = [(r, set(fold(w) for w in re.findall(r"\w+", r.get("content", "").lower())))
            for r in records if matches(r, flt)]
    n = len(docs) or 1
    df = {t: sum(1 for _, ws in docs if t in ws) for t in terms}
    scored = []
    for r, ws in docs:
        s = sum(math.log(1 + n / df[t]) for t in terms if t in ws)
        if s > 0:
            scored.append((s, r.get("created_ts") or 0, r))
    scored.sort(key=lambda x: (-x[0], -x[1]))
    return [row(r, round(s, 4)) for s, _, r in scored[:top]]


def row(rec, score, mode="lexical", degraded=None):
    return {"id": rec.get("id"), "kind": rec.get("kind"), "project": rec.get("project"),
            "tags": rec.get("tags") or [], "created_at": rec.get("created_at"),
            "score": score, "content": rec.get("content"), "source": rec.get("source"),
            "mode": mode, "degraded": degraded}


# ── Bridge to the venv side ──────────────────────────────────────────────────────

def _bridge_settings(probe_timeout=0.3):
    s = store_settings(probe_timeout)
    s.update(embed=embed_name(), models=str(models_dir()), journal=str(journal_path()))
    return s


def call_venv(op, payload=None, timeout=300):
    """Run `op` in the brain venv. Returns (True, result) or (False, short reason)."""
    py = venv_python()
    if not py.exists():
        return False, f"venv missing ({py}) — run ./deploy.sh"
    body = dict(payload or {}, settings=_bridge_settings())
    env = dict(os.environ, HF_HUB_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1",
               TOKENIZERS_PARALLELISM="false")
    try:
        r = subprocess.run([str(py), str(Path(__file__).resolve()), op],
                           input=json.dumps(body), capture_output=True, text=True,
                           timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return False, f"brain {op} timed out after {timeout}s"
    except OSError as e:
        return False, f"venv python not runnable ({e.strerror or e})"
    try:
        out = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else None
    except ValueError:
        out = None
    if isinstance(out, dict) and out.get("ok"):
        return True, out
    if isinstance(out, dict) and out.get("reason"):
        return False, out["reason"]
    tail = (r.stderr.strip().splitlines() or [""])[-1][:160]
    return False, f"brain process exited {r.returncode}" + (f": {tail}" if tail else "")


def mark_pending(reason):
    try:
        pending_path().parent.mkdir(parents=True, exist_ok=True)
        pending_path().write_text(f"{iso(_now())} {reason}\n", encoding="utf-8")
    except OSError:
        pass


def clear_pending():
    try:
        pending_path().unlink()
    except OSError:
        pass


# ── Public API used by osforge-db ────────────────────────────────────────────────

def remember(content, kind, project=None, tags=None, source="manual", created=None):
    """Journal first, then index. Returns (record, indexed, reason). Raises BrainError
    when the journal cannot be written (then nothing was indexed either)."""
    rec = make_record(content, kind, project, tags, source, created)
    journal_append([rec])
    ok, res = call_venv("index", {"records": [rec]})
    if not ok:
        mark_pending(res)
        return rec, False, res
    return rec, True, None


def forget(id_or_prefix):
    """Tombstone + delete. Returns (record, deleted_from_index, reason)."""
    live, _, _ = journal_read()
    hits = [r for r in live if r["id"] == id_or_prefix] or \
           [r for r in live if len(id_or_prefix) >= 4 and r["id"].startswith(id_or_prefix)]
    if not hits:
        raise BrainError(f"no memory with id {id_or_prefix!r}")
    if len(hits) > 1:
        raise BrainError(f"id prefix {id_or_prefix!r} is ambiguous ({len(hits)} memories)")
    rec = hits[0]
    journal_append([{"op": "forget", "id": rec["id"], "at": iso(_now()),
                     "source": rec.get("source")}])
    ok, res = call_venv("delete", {"ids": [rec["id"]]})
    if not ok:
        mark_pending(res)
        return rec, False, res
    return rec, True, None


def recall(query, flt, top=5, mode="dense"):
    """Rows best first. Store/embedder unavailable → lexical scan of the journal with
    every row's `degraded` set to the reason. Never silent, never raises for that."""
    live, _, _ = journal_read()
    if not live:                                # nothing remembered: nothing to index or scan
        return [], None
    ok, res = call_venv("query", {"query": query, "filter": flt, "top": top, "mode": mode,
                                  "min_score": min_score()})
    if ok:
        return res["rows"], None
    rows = lexical_search(live, query, flt, top)
    for r in rows:
        r["degraded"] = res
    return rows, res


def migrate_decisions(decisions):
    """decisions: iterable of dicts (id, slug, category, created_at 'YYYY-MM-DD HH:MM:SS',
    content). Journals every decision not yet in the brain (by source key, forgotten
    included), then indexes them in one venv call. Returns (added, indexed, reason)."""
    _, _, sources = journal_read()
    seen = {decision_source_id(s) for s in sources} - {None}
    recs = []
    for d in decisions:
        if str(d["id"]) in seen:
            continue
        try:
            created = datetime.strptime(d["created_at"][:19], "%Y-%m-%d %H:%M:%S") \
                .replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            created = None
        recs.append(make_record(d["content"], "decision", d.get("slug"),
                                [d["category"]] if d.get("category") else [],
                                f"migrate:sqlite#{d['id']}", created))
    if not recs:
        return 0, 0, None
    journal_append(recs)
    ok, res = call_venv("index", {"records": recs}, timeout=3600)
    if not ok:
        mark_pending(res)
        return len(recs), 0, res
    return len(recs), res.get("n", len(recs)), None


def rebuild():
    """Recreate the collection from the journal. Returns (ok, result|reason)."""
    ok, res = call_venv("rebuild", {}, timeout=3600)
    if ok:
        clear_pending()
    return ok, res


def status():
    live, gone, _ = journal_read()
    s = _bridge_settings()
    out = {"store": s["store"], "url": s["url"] if s["store"] == "server" else None,
           "path": s["path"] if s["store"] == "local" else None,
           "collection": s["collection"], "embed": s["embed"],
           "model": EMBEDDERS[s["embed"]][0], "venv": str(venv_python()),
           "journal": s["journal"], "journal_live": len(live), "journal_forgotten": len(gone),
           "points": None, "pending": pending_path().exists(), "degraded": None}
    ok, res = call_venv("count", {}, timeout=120)
    if ok:
        out["points"] = res["points"]
    else:
        out["degraded"] = res
    return out


def _model_present(marker):
    d = models_dir()
    try:
        return any(marker in p.name for p in d.iterdir())
    except OSError:
        return False


def health(timeout=0.3):
    """(ok, reason). Fast: file checks + at most one HTTP probe; never loads the model.
    An empty or disabled brain is healthy (nothing to recall, nothing to say)."""
    if not enabled():
        return True, None
    jp = journal_path()
    try:
        if jp.stat().st_size == 0:
            return True, None
    except OSError:
        return True, None
    py = venv_python()
    if not py.exists():
        return False, f"venv missing: {py}"
    name = embed_name()
    marker = EMBEDDERS[name][4]
    if marker and not (_model_present(marker) and _model_present(BM25_MARKER)):
        return False, f"{name} model not downloaded into {models_dir()}"
    s = store_settings(timeout)
    if s["store"] == "server":
        if not _url_answers(s["url"], timeout):
            return False, f"Qdrant not answering at {s['url']}"
    elif not Path(s["path"]).exists():
        return False, f"local store missing: {s['path']}"
    if pending_path().exists():
        why = pending_path().read_text(encoding="utf-8", errors="replace").strip()
        return False, f"memories journaled but not indexed ({why.split(' ', 1)[-1][:120]})"
    return True, None


# ═════════════════════════════════════════════════════════════════════════════════
# venv side — heavy imports live below, inside functions
# ═════════════════════════════════════════════════════════════════════════════════

class _FakeEmbedder:
    """Deterministic, offline. NOT semantic: shared words (and 5-char prefixes) → shared
    features. Dense = unsigned hashed bag, L2-normalised; sparse = hashed term counts."""
    dim = EMBEDDERS["fake"][1]

    @staticmethod
    def _feats(text):
        out = []
        for w in re.findall(r"\w+", (text or "").lower()):
            f = fold(w)
            if f in STOPWORDS or len(f) < 3:
                continue
            out.append(f)
            if len(f) > 5:
                out.append(f[:5] + "~")
        return out

    @staticmethod
    def _h(s, mod):
        import hashlib
        return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), "big") % mod

    def dense(self, text, is_query):
        v = [0.0] * self.dim
        for f in set(self._feats(text)):
            v[self._h(f, self.dim)] += 1.0
        n = sum(x * x for x in v) ** 0.5 or 1.0
        return [x / n for x in v]

    def sparse(self, text, is_query):
        counts = {}
        for f in self._feats(text):
            if f.endswith("~"):
                continue
            i = self._h(f, 2 ** 31)
            counts[i] = 1.0 if is_query else counts.get(i, 0.0) + 1.0
        return sorted(counts), [counts[i] for i in sorted(counts)]


class _FastEmbedder:
    def __init__(self, name, models):
        from fastembed import SparseTextEmbedding, TextEmbedding
        model, self.dim, self.qp, self.dp, _, _ = EMBEDDERS[name]
        self._dense = TextEmbedding(model, cache_dir=models, local_files_only=True)
        self._bm25 = SparseTextEmbedding(BM25_MODEL, cache_dir=models, language=BM25_LANGUAGE,
                                         local_files_only=True)

    def dense(self, text, is_query):
        prefix = self.qp if is_query else self.dp
        # batch_size=1: the default (256) pads every batch to its longest text → 6.8 GB RSS
        return next(iter(self._dense.embed([prefix + text], batch_size=1))).tolist()

    def sparse(self, text, is_query):
        gen = self._bm25.query_embed([text]) if is_query else self._bm25.embed([text], batch_size=1)
        sv = next(iter(gen))
        return sv.indices.tolist(), sv.values.tolist()


def _embedder(settings):
    name = settings.get("embed", "gemma")
    if name == "fake":
        return _FakeEmbedder()
    try:
        return _FastEmbedder(name, settings["models"])
    except Exception as e:
        raise RuntimeError(f"embedder unavailable ({name}: {str(e).splitlines()[0][:120]})")


def _client(settings):
    from qdrant_client import QdrantClient
    try:
        if settings["store"] == "server":
            cl = QdrantClient(url=settings["url"], timeout=5)
            cl.get_collections()
        else:
            Path(settings["path"]).mkdir(parents=True, exist_ok=True)
            cl = QdrantClient(path=settings["path"])
        return cl
    except Exception as e:
        where = settings["url"] if settings["store"] == "server" else settings["path"]
        raise RuntimeError(f"store unavailable ({settings['store']} {where}: "
                           f"{str(e).splitlines()[0][:120]})")


def _ensure_collection(cl, settings, dim, recreate=False):
    from qdrant_client import models as qm
    name = settings["collection"]
    if recreate and cl.collection_exists(name):
        cl.delete_collection(name)
    if cl.collection_exists(name):
        have = cl.get_collection(name).config.params.vectors["dense"].size
        if have != dim:
            raise RuntimeError(f"collection {name} has dense size {have}, embedder "
                               f"{settings['embed']} needs {dim} — run `osforge-db brain rebuild`")
        return
    cl.create_collection(
        name,
        vectors_config={"dense": qm.VectorParams(size=dim, distance=qm.Distance.COSINE)},
        sparse_vectors_config={"bm25": qm.SparseVectorParams(modifier=qm.Modifier.IDF)})
    if settings["store"] == "server":           # payload indexes are no-ops in local mode
        for key, schema in (("project", qm.PayloadSchemaType.KEYWORD),
                            ("kind", qm.PayloadSchemaType.KEYWORD),
                            ("tags", qm.PayloadSchemaType.KEYWORD),
                            ("created_ts", qm.PayloadSchemaType.INTEGER)):
            cl.create_payload_index(name, key, schema)


_PAYLOAD_KEYS = ("id", "kind", "project", "tags", "created_at", "created_ts", "source", "content")


def _index(cl, emb, settings, records):
    from qdrant_client import models as qm
    pts, n = [], 0
    for rec in records:                         # one text at a time (batch_size=1)
        idx, val = emb.sparse(rec["content"], False)
        pts.append(qm.PointStruct(
            id=rec["id"],
            vector={"dense": emb.dense(rec["content"], False),
                    "bm25": qm.SparseVector(indices=idx, values=val)},
            payload={k: rec.get(k) for k in _PAYLOAD_KEYS}))
        if len(pts) >= 64:
            cl.upsert(settings["collection"], points=pts, wait=True)
            n += len(pts)
            pts = []
    if pts:
        cl.upsert(settings["collection"], points=pts, wait=True)
        n += len(pts)
    return n


def _qfilter(flt):
    from qdrant_client import models as qm
    must = []
    if flt.get("kind"):
        must.append(qm.FieldCondition(key="kind", match=qm.MatchValue(value=flt["kind"])))
    if flt.get("global"):
        must.append(qm.IsNullCondition(is_null=qm.PayloadField(key="project")))
    elif flt.get("project"):
        must.append(qm.FieldCondition(key="project", match=qm.MatchValue(value=flt["project"])))
    if flt.get("since_ts") is not None or flt.get("until_ts") is not None:
        must.append(qm.FieldCondition(key="created_ts", range=qm.Range(
            gte=flt.get("since_ts"), lt=flt.get("until_ts"))))
    return qm.Filter(must=must) if must else None


def _query(cl, emb, settings, p):
    from qdrant_client import models as qm
    col, top, q = settings["collection"], int(p.get("top") or 5), p["query"]
    if not cl.collection_exists(col):           # journal has records (checked by the caller)
        raise RuntimeError(f"collection {col} missing — run `osforge-db brain rebuild`")
    f = _qfilter(p.get("filter") or {})
    floor = float(p.get("min_score", 0.0))
    mode = p.get("mode", "dense")

    def sparse_q():
        idx, val = emb.sparse(q, True)
        return qm.SparseVector(indices=idx, values=val) if idx else None

    def keyword():
        sv = sparse_q()
        if sv is None:
            return []
        return cl.query_points(col, query=sv, using="bm25", query_filter=f, limit=top,
                               with_payload=True).points

    if mode == "keyword":
        return keyword(), "keyword"
    dv = emb.dense(q, True)
    if mode == "hybrid":
        wide = max(20, top * 4)
        pre = [qm.Prefetch(query=dv, using="dense", filter=f, limit=wide, score_threshold=floor)]
        sv = sparse_q()
        if sv is not None:
            pre.append(qm.Prefetch(query=sv, using="bm25", filter=f, limit=wide))
        return cl.query_points(col, prefetch=pre, query=qm.FusionQuery(fusion=qm.Fusion.RRF),
                               limit=top, with_payload=True).points, "hybrid"
    pts = cl.query_points(col, query=dv, using="dense", query_filter=f, limit=top,
                          score_threshold=floor, with_payload=True).points
    if pts:
        return pts, "dense"
    return keyword(), "keyword"                 # nothing above the floor → BM25 leg


def _venv_main(op):
    p = json.loads(sys.stdin.read() or "{}")
    s = p.get("settings") or _bridge_settings()
    if op == "fetch-model":                     # deploy only: network allowed here
        from fastembed import SparseTextEmbedding, TextEmbedding
        name = s.get("embed", "gemma")
        if name != "fake":
            TextEmbedding(EMBEDDERS[name][0], cache_dir=s["models"])
            SparseTextEmbedding(BM25_MODEL, cache_dir=s["models"], language=BM25_LANGUAGE)
        return {"ok": True, "model": EMBEDDERS[name][0]}
    cl = _client(s)
    try:
        if op == "count":
            col = s["collection"]
            n = cl.count(col, exact=True).count if cl.collection_exists(col) else 0
            return {"ok": True, "points": n}
        if op == "delete":
            from qdrant_client import models as qm
            if cl.collection_exists(s["collection"]):
                cl.delete(s["collection"], points_selector=qm.PointIdsList(points=p["ids"]),
                          wait=True)
            return {"ok": True}
        emb = _embedder(s)
        if op == "index":
            _ensure_collection(cl, s, emb.dim)
            return {"ok": True, "n": _index(cl, emb, s, p.get("records") or [])}
        if op == "rebuild":
            live, _, _ = journal_read(s["journal"])
            _ensure_collection(cl, s, emb.dim, recreate=True)
            return {"ok": True, "n": _index(cl, emb, s, live)}
        if op == "query":
            pts, mode = _query(cl, emb, s, p)
            rows = []
            for pt in pts:
                pl = pt.payload or {}
                rows.append(row(pl, round(float(pt.score), 4), mode))
            return {"ok": True, "rows": rows}
        return {"ok": False, "reason": f"unknown op {op!r}"}
    finally:
        cl.close()


if __name__ == "__main__":
    op = sys.argv[1] if len(sys.argv) > 1 else ""
    t0 = time.perf_counter()
    try:
        res = _venv_main(op)
    except Exception as e:                      # one JSON line, never a traceback dump
        res = {"ok": False, "reason": str(e).splitlines()[0][:240] if str(e) else type(e).__name__}
    res["elapsed_s"] = round(time.perf_counter() - t0, 3)
    print(json.dumps(res, ensure_ascii=False))
