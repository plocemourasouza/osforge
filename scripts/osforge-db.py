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
"""

import sqlite3, sys, os, json, textwrap
from datetime import datetime, timezone
from pathlib import Path

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
    conn.execute("""
        INSERT INTO decisions (project_id, content, category)
        VALUES (?, ?, ?)
    """, (p["id"], content, category))
    conn.execute("UPDATE projects SET updated_at=? WHERE id=?",
                 (_now(), p["id"]))
    conn.commit()
    _ok(f"Decisão ({category}) adicionada a '{slug}'")

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

    cat_arg    = next((a for a in args if a.startswith("--category=")), None)
    wait_arg   = next((a for a in args if a.startswith("--waiting=")), None)
    proj_arg   = next((a for a in args if a.startswith("--project=")), None)
    limit_arg  = next((a for a in args if a.startswith("--limit=")), None)
    status_arg = next((a for a in args if a.startswith("--status=")), None)
    phase_arg  = next((a for a in args if a.startswith("--phase=")), None)
    wave_arg   = next((a for a in args if a.startswith("--wave=")), None)
    deps_arg   = next((a for a in args if a.startswith("--depends=")), None)
    prio_arg   = next((a for a in args if a.startswith("--priority=")), None)
    category   = cat_arg.split("=",1)[1]  if cat_arg  else None
    waiting    = wait_arg.split("=",1)[1] if wait_arg  else None
    proj_flt   = proj_arg.split("=",1)[1] if proj_arg  else None
    limit      = int(limit_arg.split("=",1)[1]) if limit_arg else 5
    st_flag    = status_arg.split("=",1)[1] if status_arg else None
    st_filter  = st_flag if st_flag else "active"
    phase_flt  = phase_arg.split("=",1)[1] if phase_arg else None
    wave_flt   = wave_arg.split("=",1)[1]  if wave_arg  else None
    deps_flt   = deps_arg.split("=",1)[1]  if deps_arg  else None
    prio_flt   = prio_arg.split("=",1)[1]  if prio_arg  else None
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
    else:
        _err(f"Comando desconhecido: '{cmd}'. Use 'osforge-db' sem args para ajuda.")

    conn.close()

if __name__ == "__main__":
    main()
