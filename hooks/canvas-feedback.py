#!/usr/bin/env python3
"""
canvas-feedback.py — Stop hook: drena o feedback pendente do OSForge Canvas (B-020, E-A43).

Antes, a volta do feedback ao agente era prosa na skill ("leia o arquivo no próximo
turno") — e o agente frequentemente agia antes de ler. Agora, quando o agente tenta
encerrar o turno e há feedback do usuário que ele ainda não viu, o Stop é bloqueado
UMA vez com o conteúdo do feedback; o agente responde a ele e o Stop seguinte passa.
Padrão importado do ECC `plan-canvas-pending.js` (MIT; ver .out-of-scope/ecc-imports.md),
reescrito para o modelo de dados do Canvas do OSForge.

Passa (exit 0, stdout vazio) quando:
  - stop_hook_active é true (já estamos num Stop reaberto por hook — nunca em laço);
  - o servidor não responde em 1 s (sem data dir confiável → não adivinha);
  - não há artefato deste projeto com feedback ainda não entregue;
  - OSFORGE_CANVAS_FEEDBACK=off.
Bloqueia ({"decision":"block","reason":…}) quando há feedback novo para um artefato cujo id
começa com o slug do projeto atual (hooks/lib/project_id.py; é assim que a skill separa
projetos num data dir compartilhado). "Novo" = (revision, submittedAt) diferente do que
já foi entregue, registrado em <data dir>/.delivered.json.

Contrato de saída: docs/HOOKS.md. Segredos no feedback passam por lib/scrub.py.
Diagnóstico: OSFORGE_HOOK_DEBUG=1 → ~/.osforge/logs/hooks.log.
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
try:
    from project_id import resolve as _resolve, fallback_slug as _fallback_slug
    from scrub import scrub as _scrub
except Exception:                                   # pragma: no cover
    _resolve = None
    _fallback_slug = lambda: os.path.basename(os.getcwd()).lower().replace("_", "-")
    _scrub = lambda t: t

PORT = os.environ.get("CANVAS_PORT", "4242")
HEALTH_TIMEOUT_S = 1.0
MAX_REASON = 1500
MAX_STDIN = 1024 * 1024
LOG_FILE = os.path.join(os.environ.get("OSFORGE_LOG_DIR", os.path.expanduser("~/.osforge/logs")), "hooks.log")


def _log(msg):
    if os.environ.get("OSFORGE_HOOK_DEBUG") != "1":
        return
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[canvas-feedback] {msg}\n")
    except OSError:
        pass


def _payload():
    try:
        raw = sys.stdin.read(MAX_STDIN)
        d = json.loads(raw) if raw.strip() else {}
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _data_dir():
    """Data dir announced by the running server; None when it is down (→ pass)."""
    url = os.environ.get("OSFORGE_CANVAS_HEALTH_URL") or f"http://127.0.0.1:{PORT}/api/health"
    try:
        with urllib.request.urlopen(url, timeout=HEALTH_TIMEOUT_S) as r:   # noqa: S310 — loopback only
            d = json.loads(r.read().decode("utf-8", "replace"))
        return d.get("dir") if isinstance(d, dict) and isinstance(d.get("dir"), str) else None
    except Exception as exc:
        _log(f"servidor fora do ar: {exc}")
        return None


def _read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else None
    except (OSError, ValueError):
        return None


def _summary(fb, artifact):
    """Compact, scrubbed rendering of one feedback file."""
    lines = []
    blocks = {b.get("id"): b for b in (artifact or {}).get("blocks", []) if isinstance(b, dict)}
    for bid, resp in (fb.get("responses") or {}).items():
        if not isinstance(resp, dict):
            continue
        t = resp.get("type")
        if t == "decision":
            c = resp.get("comment")
            lines.append(f"- decisão `{bid}`: **{resp.get('action')}**" + (f" — {c}" if c else ""))
        elif t == "checklist":
            items = {i.get("id"): i.get("text") for i in (blocks.get(bid) or {}).get("items", []) if isinstance(i, dict)}
            checked = resp.get("checked") or []
            lines.append(f"- checklist `{bid}`: {len(checked)}/{len(items)} marcados"
                         + (": " + ", ".join(str(items.get(x, x)) for x in checked) if checked else ""))
        elif t == "form":
            vals = resp.get("values") or {}
            lines.append(f"- form `{bid}`: " + "; ".join(f"{k}={v}" for k, v in vals.items()))
    if fb.get("comment"):
        lines.append(f"- comentário geral: {fb['comment']}")
    return _scrub("\n".join(lines)) if lines else "(feedback enviado sem respostas)"


def main():
    if os.environ.get("OSFORGE_CANVAS_FEEDBACK", "").strip().lower() in ("off", "0", "false"):
        return
    p = _payload()
    if p.get("stop_hook_active"):
        return                                      # never re-block a Stop we reopened
    data_dir = _data_dir()
    if not data_dir or not os.path.isdir(data_dir):
        return
    slug = None
    try:
        res = _resolve() if _resolve else None
        slug = res["slug"] if res else _fallback_slug()
    except Exception:
        slug = None
    if not slug:
        return

    fb_dir = os.path.join(data_dir, "feedback")
    art_dir = os.path.join(data_dir, "artifacts")
    state_path = os.path.join(data_dir, ".delivered.json")
    delivered = _read_json(state_path) or {}
    prefix = slug + "-"
    try:
        names = sorted(n for n in os.listdir(fb_dir) if n.endswith(".json") and (n.startswith(prefix) or n == slug + ".json"))
    except OSError:
        return

    pending = []
    for n in names:
        aid = n[:-5]
        fb = _read_json(os.path.join(fb_dir, n))
        if not fb:
            continue
        key = f"{fb.get('revision')}|{fb.get('submittedAt')}"
        if delivered.get(aid) == key:
            continue
        artifact = _read_json(os.path.join(art_dir, n))
        stale = bool(artifact) and artifact.get("revision") != fb.get("revision")
        pending.append((aid, key, fb, artifact, stale))
    if not pending:
        return

    parts = []
    for aid, key, fb, artifact, stale in pending:
        title = (artifact or {}).get("title") or aid
        head = f"## {title} (`{aid}`, rev {fb.get('revision')}" + (", DESATUALIZADO: o artefato já está em outra revisão" if stale else "") + ")"
        parts.append(head + "\n" + _summary(fb, artifact))
        delivered[aid] = key
    body = "\n\n".join(parts)
    if len(body) > MAX_REASON:
        body = body[:MAX_REASON] + "\n… [truncado; leia o arquivo completo em " + fb_dir + "]"
    reason = ("OSForge Canvas: o usuário enviou feedback que você ainda não leu. Responda a ele "
              "antes de encerrar (se o feedback pedir mudanças, revise o artefato incrementando "
              "`revision`).\n\n" + body)
    try:
        tmp = state_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(delivered, f, indent=2)
        os.replace(tmp, state_path)
    except OSError as exc:
        _log(f"não consegui gravar {state_path}: {exc}")   # still deliver once; may repeat next Stop
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:                        # fail open, always
        _log(f"erro suprimido: {exc}")
    sys.exit(0)
