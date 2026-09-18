#!/usr/bin/env python3
"""
hooks/lib/project_id.py — UMA identidade de projeto para todos os hooks (B-018, E-A19, E-A20, E-A26).

Antes, session-resume.sh usava `basename(pwd)` em minúsculas, observe-capture.py usava o
basename cru e session-save.py uma terceira variante: duas pastas `My_Proj` distintas
recebiam o mesmo resume, um subdiretório do projeto não recebia nenhum, e as observações
podiam cair numa chave diferente do resume do mesmo projeto.

Ordem de resolução (a primeira que casar ganha):
  1. OSFORGE_PROJECT=<slug>                      — explícito vence sempre
  2. projects.root_path  == raiz git do cwd      — ou cwd dentro dela (subdiretório)
  3. projects.remote_hash == hash do remote      — worktrees e clones do mesmo repo
  4. basename normalizado da raiz git (ou cwd)  — compatível com projetos já registrados

Devolve {"slug", "status", "how"} ou None quando nada casa (hooks ficam silenciosos).
`OSFORGE_DB` é honrado por osforge-db.py; este módulo só o repassa no ambiente.

CLI (para hooks em bash):  python3 project_id.py [cwd]  → JSON numa linha, ou nada.
Stdlib apenas; toda chamada externa (git, osforge-db) tem timeout e falha em silêncio.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

_GIT_TIMEOUT = 3
_DB_TIMEOUT = 5


# ── osforge-db location (shared by every hook; no hard-coded ~/Development path) ──

def find_db_cmd():
    """Command list to invoke osforge-db, or [] when it is not installed."""
    home = os.path.expanduser("~")
    cands = [os.path.join(home, ".local", "bin", "osforge-db")]
    anchor = os.path.join(home, ".osforge", "repo-path")
    try:
        with open(anchor, encoding="utf-8") as f:
            cands.append(os.path.join(f.read().strip(), "scripts", "osforge-db.py"))
    except OSError:
        pass
    here = os.path.dirname(os.path.abspath(__file__))
    cands.append(os.path.normpath(os.path.join(here, "..", "..", "scripts", "osforge-db.py")))
    for c in cands:
        if os.path.isfile(c):
            return ["python3", c] if c.endswith(".py") else [c]
    return []


# ── git ──────────────────────────────────────────────────────────────────────

def _git(args, cwd):
    try:
        r = subprocess.run(["git", "-C", cwd] + args, capture_output=True, text=True,
                           timeout=_GIT_TIMEOUT, check=False)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def git_root(cwd):
    """Top-level of the working tree; for a linked worktree, the MAIN repository's root."""
    top = _git(["rev-parse", "--show-toplevel"], cwd)
    if not top:
        return ""
    common = _git(["rev-parse", "--path-format=absolute", "--git-common-dir"], cwd)
    if common and os.path.basename(common) == ".git":
        return os.path.realpath(os.path.dirname(common))
    return os.path.realpath(top)


def normalize_remote(url):
    """Strip credentials/scheme/.git so ssh and https spellings of one repo agree."""
    u = (url or "").strip()
    if not u:
        return ""
    u = re.sub(r"^[a-z+]+://", "", u)                 # scheme
    u = re.sub(r"^[^@/]+@", "", u)                     # user[:pass]@
    u = u.replace(":", "/", 1) if re.match(r"^[^/]+:[^/]", u) else u   # host:org/repo → host/org/repo
    u = re.sub(r"\.git/?$", "", u).rstrip("/").lower()
    return u


def remote_hash(url):
    n = normalize_remote(url)
    return hashlib.sha256(n.encode("utf-8")).hexdigest()[:16] if n else ""


def git_remote_hash(root):
    return remote_hash(_git(["config", "--get", "remote.origin.url"], root)) if root else ""


def slugify(name):
    return re.sub(r"[^a-z0-9-]+", "-", (name or "").lower().replace("_", "-")).strip("-")


# ── resolution ───────────────────────────────────────────────────────────────

def _projects(db_cmd, env):
    if not db_cmd:
        return []
    try:
        r = subprocess.run(db_cmd + ["list-projects", "--status=all", "--json"],
                           capture_output=True, text=True, timeout=_DB_TIMEOUT, check=False, env=env)
        data = json.loads(r.stdout) if r.stdout.strip() else []
        return data if isinstance(data, list) else []
    except (OSError, subprocess.SubprocessError, ValueError):
        return []


def resolve(cwd=None, db_cmd=None, env=None):
    env = dict(env if env is not None else os.environ)
    cwd = os.path.realpath(cwd or env.get("PWD") or os.getcwd())
    forced = (env.get("OSFORGE_PROJECT") or "").strip()
    db_cmd = db_cmd if db_cmd is not None else find_db_cmd()
    projects = _projects(db_cmd, env)
    by_slug = {p.get("slug"): p for p in projects if isinstance(p, dict)}

    if forced:
        p = by_slug.get(forced)
        return {"slug": forced, "status": (p or {}).get("status") or "unregistered", "how": "env"}

    root = git_root(cwd)
    for p in projects:
        rp = (p.get("root_path") or "").rstrip("/")
        if rp and (cwd == rp or cwd.startswith(rp + os.sep) or (root and root == rp)):
            return {"slug": p["slug"], "status": p.get("status"), "how": "root_path"}

    rh = git_remote_hash(root) if root else ""
    if rh:
        for p in projects:
            if p.get("remote_hash") == rh:
                return {"slug": p["slug"], "status": p.get("status"), "how": "remote_hash"}

    base = slugify(os.path.basename(root or cwd))
    if base in by_slug:
        return {"slug": base, "status": by_slug[base].get("status"), "how": "basename"}
    return None


def fallback_slug(cwd=None):
    """Normalised basename for callers that record telemetry even when unregistered."""
    cwd = os.path.realpath(cwd or os.getcwd())
    return slugify(os.path.basename(git_root(cwd) or cwd)) or "unknown"


if __name__ == "__main__":
    try:
        res = resolve(sys.argv[1] if len(sys.argv) > 1 else None)
        if res:
            print(json.dumps(res, ensure_ascii=False))
    except Exception:
        pass
    sys.exit(0)
