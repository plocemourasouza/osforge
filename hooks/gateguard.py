#!/usr/bin/env python3
"""
PreToolUse Hook: GateGuard — Fact-Forcing Gate (OSForge edition)

Forces investigation before Edit/Write/Bash. Instead of asking "are you sure?"
(which LLMs always answer "yes"), this hook demands concrete facts.
The act of investigation creates awareness that self-evaluation never did.

Based on the ecc GateGuard mechanism (+2.25 pts vs ungated, two independent A/B tests).
Adapted for OSForge: Python stdlib only, zero dependencies, minimalista.

── Gates ──────────────────────────────────────────────────────────────────────
  Edit/Write   : first touch per file per session → demand importers, API surface,
                 data schema, verbatim instruction.
  Bash (destr.): each occurrence → demand targets list, rollback plan, verbatim
                 instruction.

── Fail-open / Fail-closed policy ─────────────────────────────────────────────
  FAIL-CLOSED for destructive Bash (rm -rf, git push --force, DROP/TRUNCATE, etc.)
    when the JSON input is valid but command cannot be parsed: we deny and ask for
    facts. This is the high-signal gate and must not silently pass.
  FAIL-OPEN for everything else (JSON parse error, unknown tool name, state I/O
    failure): we allow with a stderr warning. A broken hook must never permanently
    block a working session.

── Kill-switch ─────────────────────────────────────────────────────────────────
  OSFORGE_GATEGUARD=off  (also: 0, false, disabled, disable)  → exit 0, allow all.
  OSFORGE_GATEGUARD=on   (also: 1, true, enabled, enable)     → normal operation.
  Default: on.

── Session state ────────────────────────────────────────────────────────────────
  JSON file in ~/.osforge/gateguard/ keyed by CLAUDE_SESSION_ID or project path.
  Atomic write (write tmp + rename). Expires after 30 min of inactivity.

── Output format ────────────────────────────────────────────────────────────────
  Claude Code PreToolUse hooks must write JSON to stdout.
  Allow : exit 0, stdout empty or {"continue": true}
  Deny  : exit 0 (NOT exit 2), stdout JSON with hookSpecificOutput.permissionDecision="deny"
  The scan-secrets.sh convention uses {"continue": false, "permission": "deny", ...}
  This hook uses the newer hookSpecificOutput format (same effect, more structured).

Usage (PreToolUse, matcher Edit|Write|Bash):
  python3 ~/.claude/hooks/gateguard.py
"""

import hashlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────

SESSION_TIMEOUT_S = 30 * 60          # 30 minutes of inactivity expires session
MAX_CHECKED       = 500              # cap checked[] list to prevent unbounded growth

DISABLE_VALUES = {"0", "false", "off", "disabled", "disable"}

STATE_DIR = Path(os.environ.get("OSFORGE_GATEGUARD_STATE_DIR", "") or
                 Path.home() / ".osforge" / "gateguard")

# ── Destructive Bash patterns ──────────────────────────────────────────────────

# Regex applied to quote-stripped command text (case-insensitive).
# High-signal only: patterns that irreversibly destroy data/history.
_DESTRUCTIVE_SQL = re.compile(
    r'\b(drop\s+table|drop\s+database|truncate\s+table|truncate\b|'
    r'delete\s+from\b)',
    re.IGNORECASE,
)


def _strip_quoted(cmd: str) -> str:
    """Remove single- and double-quoted strings to reduce false positives."""
    cmd = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', ' ', cmd)
    cmd = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", ' ', cmd)
    return cmd


def _is_destructive_rm(cmd: str) -> bool:
    """True for rm -rf / rm -fr variants, but not safe targeted removes."""
    for segment in re.split(r'[;&|]', cmd):
        tokens = segment.split()
        if not tokens:
            continue
        basename = os.path.basename(tokens[0])
        if basename not in ("rm", "sudo"):
            continue
        flags = ""
        for t in tokens[1:]:
            if t.startswith("--"):
                if t == "--recursive":
                    flags += "r"
                if t == "--force":
                    flags += "f"
            elif t.startswith("-"):
                flags += t[1:]
        if "r" in flags and "f" in flags:
            return True
    return False


def _is_destructive_git(cmd: str) -> bool:
    """True for git push --force, git reset --hard, git clean -f, git commit --amend."""
    for segment in re.split(r'[;&|]', cmd):
        tokens = segment.split()
        if not tokens:
            continue
        if os.path.basename(tokens[0]) != "git":
            continue
        subcmd = None
        rest = []
        skip_next = False
        for i, t in enumerate(tokens[1:], 1):
            if skip_next:
                skip_next = False
                continue
            if t in ("-C", "-c", "--git-dir", "--work-tree"):
                skip_next = True
                continue
            if t.startswith("-"):
                continue
            subcmd = t.lower()
            rest = tokens[i + 1:]
            break
        if subcmd is None:
            continue
        if subcmd == "push":
            has_force = any(
                t == "--force" or (t.startswith("-") and not t.startswith("--") and "f" in t[1:])
                for t in rest
            )
            has_lease = any(t.startswith("--force-with-lease") for t in rest)
            if has_force and not has_lease:
                return True
        elif subcmd == "reset":
            if "--hard" in rest:
                return True
        elif subcmd == "clean":
            flags = "".join(
                t[1:] for t in rest
                if t.startswith("-") and not t.startswith("--")
            )
            if "f" in flags:
                return True
        elif subcmd == "commit":
            if "--amend" in rest:
                return True
        elif subcmd in ("checkout", "switch"):
            for t in rest:
                if t in ("--force", "--discard-changes", "--"):
                    return True
                if t.startswith("-") and not t.startswith("--") and "f" in t[1:]:
                    return True
    return False


def _is_destructive_redirect(cmd: str) -> bool:
    """True for > file (overwrite redirect) outside of >> (append)."""
    stripped = _strip_quoted(cmd)
    # Detecta overwrite `> file`, `1> file`, `2> file`, `&> file`; ignora append `>>`.
    # Lookbehind negativo só de `>` — excluir fd-prefixos (1/2/&) deixaria passar
    # redirects destrutivos legítimos (2>file SOBRESCREVE file).
    return bool(re.search(r'(?<!>)\s*>\s+\S', stripped))


def is_destructive_bash(cmd: str) -> bool:
    """
    Returns True if cmd contains a pattern that could irreversibly destroy data.
    Errs toward false-negative (miss) over false-positive (false block).
    Only genuinely high-signal patterns are included.
    """
    raw = cmd or ""
    stripped = _strip_quoted(raw)

    if _DESTRUCTIVE_SQL.search(stripped):
        return True
    if _is_destructive_rm(raw):
        return True
    if _is_destructive_git(raw):
        return True
    if _is_destructive_redirect(raw):
        return True
    return False


# ── Kill-switch ────────────────────────────────────────────────────────────────

def _is_disabled() -> bool:
    val = os.environ.get("OSFORGE_GATEGUARD", "").strip().lower()
    if not val:
        return False
    return val in DISABLE_VALUES


# ── Session state ──────────────────────────────────────────────────────────────

def _resolve_session_key(data: dict) -> str:
    """Derive a stable, safe session key from hook input or env."""
    for candidate in [
        data.get("session_id"),
        data.get("sessionId"),
        os.environ.get("CLAUDE_SESSION_ID"),
        os.environ.get("ECC_SESSION_ID"),
    ]:
        if candidate and isinstance(candidate, str) and candidate.strip():
            safe = re.sub(r"[^a-zA-Z0-9_-]", "_", candidate.strip())[:64]
            if safe:
                return safe

    transcript = (
        data.get("transcript_path") or
        data.get("transcriptPath") or
        os.environ.get("CLAUDE_TRANSCRIPT_PATH", "")
    )
    if transcript and isinstance(transcript, str) and transcript.strip():
        return "tx-" + hashlib.sha256(
            os.path.realpath(transcript.strip()).encode()
        ).hexdigest()[:24]

    project = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    return "proj-" + hashlib.sha256(
        os.path.realpath(project).encode()
    ).hexdigest()[:24]


def _state_path(session_key: str) -> Path:
    return STATE_DIR / f"state-{session_key}.json"


def _load_state(path: Path) -> dict:
    try:
        if path.exists():
            raw = json.loads(path.read_text("utf-8"))
            last_active = raw.get("last_active", 0)
            if time.time() - last_active > SESSION_TIMEOUT_S:
                try:
                    path.unlink()
                except OSError:
                    pass
                return {"checked": [], "last_active": time.time()}
            return raw
    except (OSError, json.JSONDecodeError, ValueError):
        pass
    return {"checked": [], "last_active": time.time()}


def _save_state(path: Path, state: dict) -> bool:
    """Atomic write: write to temp file, rename into place."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        checked = state.get("checked", [])
        if len(checked) > MAX_CHECKED:
            state["checked"] = checked[-MAX_CHECKED:]
        state["last_active"] = time.time()
        tmp_fd, tmp_path = tempfile.mkstemp(dir=STATE_DIR, suffix=".tmp")
        try:
            os.write(tmp_fd, json.dumps(state, indent=2).encode("utf-8"))
            os.close(tmp_fd)
            tmp_fd = -1
            os.replace(tmp_path, path)
            return True
        finally:
            if tmp_fd >= 0:
                try:
                    os.close(tmp_fd)
                except OSError:
                    pass
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except OSError:
                pass
    except OSError:
        return False


def _is_checked(state: dict, key: str) -> bool:
    return key in state.get("checked", [])


def _mark_checked(state: dict, key: str) -> dict:
    checked = list(state.get("checked", []))
    if key not in checked:
        checked.append(key)
    state["checked"] = checked
    return state


# ── Claude Code hook output helpers ───────────────────────────────────────────

def _allow():
    """Allow: write nothing to stdout, exit 0."""
    sys.exit(0)


def _deny(reason: str):
    """
    Deny: emit hookSpecificOutput JSON to stdout, exit 0.
    Claude Code interprets permissionDecision=deny as a block.
    """
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(payload), flush=True)
    sys.exit(0)


def _warn_stderr(msg: str):
    print(f"[GateGuard] {msg}", file=sys.stderr, flush=True)


# ── Gate messages ──────────────────────────────────────────────────────────────

_RECOVERY_HINT = "\n\nRecovery: para desabilitar o gate nesta sessão, defina OSFORGE_GATEGUARD=off."


def _edit_gate_msg(file_path: str) -> str:
    safe = file_path[:500].replace("\n", " ")
    return (
        "[GateGuard — Fact-Forcing Gate]\n\n"
        f"Antes de editar `{safe}`, apresente os seguintes fatos:\n\n"
        "1. Liste TODOS os arquivos que importam/usam este arquivo (use Grep)\n"
        "2. Liste as funções/classes públicas afetadas por esta mudança\n"
        "3. Se este arquivo lê/escreve arquivos de dados, mostre nomes dos campos, "
        "estrutura e formato de datas (use valores sintéticos, não dados de produção)\n"
        "4. Cite textualmente a instrução atual do usuário\n\n"
        "Apresente os fatos e então tente a operação novamente."
        + _RECOVERY_HINT
    )


def _write_gate_msg(file_path: str) -> str:
    safe = file_path[:500].replace("\n", " ")
    return (
        "[GateGuard — Fact-Forcing Gate]\n\n"
        f"Antes de criar `{safe}`, apresente os seguintes fatos:\n\n"
        "1. Nomeie o(s) arquivo(s) e linha(s) que vão chamar este novo arquivo\n"
        "2. Confirme que nenhum arquivo existente serve ao mesmo propósito (use Glob)\n"
        "3. Se este arquivo lê/escreve arquivos de dados, mostre nomes dos campos, "
        "estrutura e formato de datas (valores sintéticos, não dados de produção)\n"
        "4. Cite textualmente a instrução atual do usuário\n\n"
        "Apresente os fatos e então tente a operação novamente."
        + _RECOVERY_HINT
    )


def _destructive_bash_msg() -> str:
    return (
        "[GateGuard — Fact-Forcing Gate]\n\n"
        "Comando destrutivo detectado. Antes de executar, apresente:\n\n"
        "1. Liste todos os arquivos/dados que este comando irá modificar ou apagar\n"
        "2. Escreva um procedimento de rollback em uma linha\n"
        "3. Cite textualmente a instrução atual do usuário\n\n"
        "Apresente os fatos e então tente a operação novamente."
    )


# ── Claude settings path guard ────────────────────────────────────────────────

def _is_claude_settings(file_path: str) -> bool:
    """Never gate edits to .claude/settings*.json — that creates a lock-out loop."""
    normalized = file_path.replace("\\", "/").lower()
    return bool(re.search(r'(^|/)\.claude/settings[^/]*\.json$', normalized))


# ── Stale state file pruning ──────────────────────────────────────────────────

def _prune_stale_state_files():
    """Remove state files older than 2x SESSION_TIMEOUT_S (best-effort)."""
    try:
        if not STATE_DIR.exists():
            return
        cutoff = time.time() - SESSION_TIMEOUT_S * 2
        for f in STATE_DIR.iterdir():
            if not (f.name.startswith("state-") and f.name.endswith(".json")):
                continue
            try:
                if f.stat().st_mtime < cutoff:
                    f.unlink()
            except OSError:
                pass
    except OSError:
        pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Kill-switch: immediate pass-through.
    if _is_disabled():
        _allow()

    # Read hook input from stdin.
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        # FAIL-OPEN: if we can't parse the input, allow (don't permanently block).
        _warn_stderr("could not parse hook input (fail-open); allowing.")
        _allow()

    tool_name_raw = (data.get("tool_name") or "").strip()
    tool_input    = data.get("tool_input") or {}

    _TOOL_MAP = {
        "edit":      "Edit",
        "write":     "Write",
        "multiedit": "MultiEdit",
        "bash":      "Bash",
    }
    tool_name = _TOOL_MAP.get(tool_name_raw.lower(), tool_name_raw)

    if tool_name not in ("Edit", "Write", "MultiEdit", "Bash"):
        _allow()

    session_key = _resolve_session_key(data)
    state_path  = _state_path(session_key)
    state       = _load_state(state_path)

    _prune_stale_state_files()

    # ── Edit / Write gate ──────────────────────────────────────────────────────
    if tool_name in ("Edit", "Write"):
        file_path = (tool_input.get("file_path") or "").strip()

        if not file_path or _is_claude_settings(file_path):
            _allow()

        if not _is_checked(state, file_path):
            state = _mark_checked(state, file_path)
            ok = _save_state(state_path, state)
            if not ok:
                # FAIL-OPEN on state I/O error: allow with warning.
                _warn_stderr(
                    "state could not be persisted; allowing to avoid permanent retry loop. "
                    "Check permissions on ~/.osforge/gateguard/"
                )
                _allow()
            msg = _edit_gate_msg(file_path) if tool_name == "Edit" else _write_gate_msg(file_path)
            _deny(msg)

        _allow()

    # ── MultiEdit gate ─────────────────────────────────────────────────────────
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits") or []
        if not isinstance(edits, list):
            _allow()

        for edit in edits:
            if not isinstance(edit, dict):
                continue
            file_path = (edit.get("file_path") or "").strip()
            if not file_path or _is_claude_settings(file_path):
                continue
            if not _is_checked(state, file_path):
                state = _mark_checked(state, file_path)
                ok = _save_state(state_path, state)
                if not ok:
                    _warn_stderr(
                        "state could not be persisted (MultiEdit); allowing to avoid retry loop."
                    )
                    _allow()
                _deny(_edit_gate_msg(file_path))

        _allow()

    # ── Bash gate ──────────────────────────────────────────────────────────────
    if tool_name == "Bash":
        command = (tool_input.get("command") or "").strip()

        if not command:
            _allow()

        cmd_hash = hashlib.sha256(command.encode("utf-8")).hexdigest()[:16]
        destructive_key = f"__destructive__{cmd_hash}"

        try:
            destructive = is_destructive_bash(command)
        except Exception:
            # FAIL-CLOSED: if destructive detection itself raises, treat as
            # destructive and gate it. Better to ask for facts than to silently
            # run an unknown command.
            destructive = True

        if destructive:
            if not _is_checked(state, destructive_key):
                state = _mark_checked(state, destructive_key)
                ok = _save_state(state_path, state)
                if not ok:
                    # FAIL-CLOSED for destructive: deny even on state I/O failure.
                    _warn_stderr(
                        "state could not be persisted for destructive command; "
                        "blocking to enforce fact-forcing gate."
                    )
                    _deny(_destructive_bash_msg())
                _deny(_destructive_bash_msg())
            _allow()

        _allow()

    _allow()


if __name__ == "__main__":
    main()
