#!/usr/bin/env python3
"""
session-save.py — Stop hook
Lê transcript_path do stdin (JSON do Claude Code), extrai um resumo compacto
da sessão e chama `osforge-db set-resume <slug> "<resumo>"` automaticamente.

Regras:
- Python stdlib exclusivamente (json, sys, subprocess, pathlib, os).
- Silencioso e exit 0 se projeto não registrado, transcript ausente ou qualquer erro.
- Caminhos absolutos.
- Log de diagnóstico em /tmp/osforge-session-save.log (opcional, não bloqueia).
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# ── Configuração ──────────────────────────────────────────────────────────────

MAX_STDIN     = 1024 * 1024  # 1 MB
MAX_LINES     = 2000          # linhas máximas do transcript a processar
MAX_USR_MSGS  = 8             # últimas mensagens do usuário a incluir
MAX_FILES     = 20            # arquivos modificados a incluir
LOG_FILE      = "/tmp/osforge-session-save.log"
ENABLE_LOG    = os.environ.get("OSFORGE_HOOK_DEBUG", "") == "1"


def _log(msg: str) -> None:
    if not ENABLE_LOG:
        return
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{msg}\n")
    except Exception:
        pass


# ── Localiza osforge-db ───────────────────────────────────────────────────────

def _find_osforge_db() -> list[str]:
    """Retorna o comando (lista de strings) para invocar osforge-db."""
    home = Path.home()
    candidates = [
        home / ".local" / "bin" / "osforge-db",
        home / "Development" / "osforge" / "scripts" / "osforge-db.py",
        Path(__file__).resolve().parent.parent / "scripts" / "osforge-db.py",
    ]
    for c in candidates:
        if c.exists():
            if c.suffix == ".py":
                return ["python3", str(c)]
            return [str(c)]
    return []


# ── Resolve slug do projeto ───────────────────────────────────────────────────

def _resolve_slug(db_cmd: list[str]) -> str | None:
    """
    Deriva o slug a partir do basename do cwd (lowercase, underscores → hífens)
    e verifica se existe no banco global.
    """
    cwd = os.getcwd()
    slug = Path(cwd).name.lower().replace("_", "-")
    if not slug:
        return None

    try:
        result = subprocess.run(
            db_cmd + ["list-projects", "--status=all", "--json"],
            capture_output=True, text=True, timeout=5
        )
        projects = json.loads(result.stdout) if result.stdout.strip() else []
        match = next((p for p in projects if p.get("slug") == slug), None)
        if match:
            return slug
    except Exception as exc:
        _log(f"[session-save] slug resolve error: {exc}")

    return None


# ── Extrai resumo do transcript JSONL ────────────────────────────────────────

def _extract_summary(transcript_path: str) -> str | None:
    """
    Parseia o JSONL do transcript e extrai:
    - Últimas mensagens do usuário
    - Arquivos modificados (Edit/Write/MultiEdit)
    - Ferramentas usadas (top-5)
    Retorna uma string compacta adequada para set-resume.
    """
    try:
        p = Path(transcript_path)
        if not p.exists():
            _log(f"[session-save] transcript não encontrado: {transcript_path}")
            return None

        user_messages: list[str] = []
        files_modified: set[str] = set()
        tools_used: set[str] = set()
        parse_errors = 0

        with open(p, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i >= MAX_LINES:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    parse_errors += 1
                    continue

                role = (entry.get("role") or
                        entry.get("type") or
                        entry.get("message", {}).get("role", ""))

                # Mensagens do usuário
                if role == "user":
                    raw = (entry.get("message", {}).get("content")
                           or entry.get("content") or "")
                    if isinstance(raw, str):
                        text = raw.strip()
                    elif isinstance(raw, list):
                        text = " ".join(
                            b.get("text", "") for b in raw
                            if isinstance(b, dict) and b.get("type") == "text"
                        ).strip()
                    else:
                        text = ""
                    if text:
                        # Remove system-reminder injections para não poluir o resumo
                        first_line = text.split("\n")[0][:200]
                        if first_line and not first_line.startswith("<system-reminder"):
                            user_messages.append(first_line)

                # Tool uses diretos
                if role in ("tool_use",) or entry.get("type") == "tool_use":
                    tool_name = entry.get("tool_name") or entry.get("name") or ""
                    if tool_name:
                        tools_used.add(tool_name)
                    file_path = (entry.get("tool_input", {}) or {}).get("file_path") or ""
                    if file_path and tool_name in ("Edit", "Write", "MultiEdit"):
                        files_modified.add(file_path)

                # Content blocks dentro de mensagens assistant (formato Claude Code JSONL)
                if role in ("assistant",):
                    for block in (entry.get("message", {}).get("content") or []):
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "tool_use":
                            tool_name = block.get("name") or ""
                            if tool_name:
                                tools_used.add(tool_name)
                            fp = (block.get("input") or {}).get("file_path") or ""
                            if fp and tool_name in ("Edit", "Write", "MultiEdit"):
                                files_modified.add(fp)

        if parse_errors > 0:
            _log(f"[session-save] {parse_errors} linhas não parseáveis no transcript")

        if not user_messages:
            _log("[session-save] nenhuma mensagem do usuário extraída")
            return None

        parts: list[str] = []

        last_msgs = user_messages[-MAX_USR_MSGS:]
        parts.append("tarefas: " + " | ".join(last_msgs))

        if files_modified:
            sorted_files = sorted(files_modified)[:MAX_FILES]
            parts.append("arquivos: " + ", ".join(sorted_files))

        if tools_used:
            top_tools = sorted(tools_used)[:5]
            parts.append("ferramentas: " + ", ".join(top_tools))

        return "; ".join(parts)

    except Exception as exc:
        _log(f"[session-save] erro ao extrair resumo: {exc}")
        return None


# ── Persiste o resumo ─────────────────────────────────────────────────────────

def _save_resume(db_cmd: list[str], slug: str, summary: str) -> None:
    # Trunca para evitar resumos gigantes no banco
    truncated = summary[:800]
    try:
        result = subprocess.run(
            db_cmd + ["set-resume", slug, truncated],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            _log(f"[session-save] set-resume falhou: {result.stderr.strip()}")
        else:
            _log(f"[session-save] resume salvo para '{slug}'")
    except Exception as exc:
        _log(f"[session-save] subprocess error: {exc}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    # Lê stdin (JSON do hook do Claude Code)
    stdin_data = sys.stdin.read(MAX_STDIN)

    transcript_path: str | None = None
    try:
        hook_input = json.loads(stdin_data)
        tp = hook_input.get("transcript_path")
        if isinstance(tp, str) and tp:
            transcript_path = tp
    except Exception:
        pass  # stdin ausente ou malformado — continua sem transcript

    # Fallback: variável de ambiente (Claude Code expõe em alguns contextos)
    if not transcript_path:
        transcript_path = os.environ.get("CLAUDE_TRANSCRIPT_PATH") or None

    # Hardening: só aceitar transcript dentro de ~/.claude (evita ler arquivos
    # arbitrários se o payload do hook for adulterado). Fora do prefixo → ignora.
    if transcript_path:
        try:
            allowed = (Path.home() / ".claude").resolve()
            if not Path(transcript_path).resolve().is_relative_to(allowed):
                _log(f"[session-save] transcript_path fora de ~/.claude, ignorado: {transcript_path}")
                transcript_path = None
        except Exception:
            transcript_path = None

    db_cmd = _find_osforge_db()
    if not db_cmd:
        _log("[session-save] osforge-db não encontrado")
        return

    slug = _resolve_slug(db_cmd)
    if not slug:
        _log("[session-save] projeto não registrado no osforge-db — nada a fazer")
        return

    if not transcript_path:
        _log("[session-save] transcript_path ausente — nada a fazer")
        return

    summary = _extract_summary(transcript_path)
    if not summary:
        _log("[session-save] resumo vazio — set-resume ignorado")
        return

    _save_resume(db_cmd, slug, summary)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        _log(f"[session-save] erro fatal (suprimido): {exc}")
    sys.exit(0)
