#!/usr/bin/env python3
"""
scan-secrets.py — PreToolUse (Bash) hook for Claude Code and Cursor.

Blocks (1) `rm -rf` aimed at /, ~, $HOME or a parent directory and (2) `git commit`
/ `git push` when the STAGED DIFF adds something that looks like a credential.

History. The bash version read `command` at the JSON root, which is the Cursor
payload shape; Claude Code sends `tool_input.command`, so under Claude Code the
hook always answered "allow" (audit 2026-09-18, E-A01, B-002). This rewrite reads
both shapes, answers in each harness's own contract, scans diff CONTENT instead
of grepping file names, and uses bounded patterns (unbounded ones caused
catastrophic backtracking upstream in ECC #2278).

Contracts
  Claude Code  deny  → exit 0, {"hookSpecificOutput": {"permissionDecision": "deny", ...}}
               allow → exit 0, empty stdout
  Cursor       deny  → {"continue": false, "permission": "deny", "userMessage", "agentMessage"}
               allow → {"continue": true, "permission": "allow"}
Fail-open: unreadable payload, git absent, or any internal error → allow.
Escape hatch on a line: `osforge:allow-secret` (test fixtures with fake keys).
Kill-switch: OSFORGE_SCAN_SECRETS=off.
Stdlib only. Python 3.9+.
"""
import json
import os
import re
import shlex
import subprocess
import sys

MAX_STDIN = 1024 * 1024
DISABLE_VALUES = {"0", "false", "off", "disabled", "disable"}
ALLOW_MARK = "osforge:allow-secret"

# Bounded on purpose: every quantifier has an upper limit.
SECRET_PATTERNS = [
    ("Anthropic/OpenAI-style key",  re.compile(r"\bsk-[A-Za-z0-9_-]{20,120}\b")),
    ("GitHub token",                re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,255}\b")),
    ("GitHub fine-grained token",   re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,255}\b")),
    ("AWS access key id",           re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token",                 re.compile(r"\bxox[abpsr]-[A-Za-z0-9-]{10,200}\b")),
    ("Credential inside URL",       re.compile(r"://[^/\s:@]{1,64}:[^@\s/]{3,128}@")),
    ("Private key block",           re.compile(r"-----BEGIN [A-Z ]{0,40}PRIVATE KEY-----")),
    ("Assignment to a secret name", re.compile(
        r"(?i)\b(?:private_key|secret_key|api_secret|aws_secret[a-z_]{0,32}|client_secret|"
        r"password|passwd|auth_token|access_token)\b\s*[=:]\s*['\"]?[^\s'\"]{8,256}")),
]

ROOT_TARGETS = {"/", "~", "$HOME", "${HOME}", "/*", "~/", "$HOME/", "..", "../", "../*"}


def _disabled() -> bool:
    return os.environ.get("OSFORGE_SCAN_SECRETS", "").strip().lower() in DISABLE_VALUES


def _read_payload():
    try:
        raw = sys.stdin.read(MAX_STDIN)
        data = json.loads(raw) if raw.strip() else {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _harness(payload: dict) -> str:
    # Claude Code always sends hook_event_name and nests the command in tool_input.
    if payload.get("hook_event_name") or isinstance(payload.get("tool_input"), dict):
        return "claude-code"
    return "cursor"


def _command(payload: dict) -> str:
    ti = payload.get("tool_input")
    if isinstance(ti, dict) and isinstance(ti.get("command"), str):
        return ti["command"]
    cmd = payload.get("command")
    return cmd if isinstance(cmd, str) else ""


def _cwd(payload: dict) -> str:
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and cwd:
        return cwd
    roots = payload.get("workspace_roots")
    if isinstance(roots, list) and roots and isinstance(roots[0], str):
        return roots[0]
    return os.getcwd()


def _emit_allow(harness: str):
    if harness == "cursor":
        print(json.dumps({"continue": True, "permission": "allow"}))
    sys.exit(0)


def _emit_deny(harness: str, user_msg: str, agent_msg: str):
    if harness == "cursor":
        print(json.dumps({"continue": False, "permission": "deny",
                          "userMessage": user_msg, "agentMessage": agent_msg}))
    else:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"[scan-secrets] {agent_msg} (disable: OSFORGE_SCAN_SECRETS=off)",
        }}))
    sys.exit(0)


def _segments(command: str):
    """Split a shell line on ; && || | and newlines, then shlex each piece."""
    for seg in re.split(r"(?:&&|\|\||[;|\n])", command):
        seg = seg.strip()
        if not seg:
            continue
        try:
            yield shlex.split(seg, posix=True)
        except ValueError:
            yield seg.split()


def is_root_rm(command: str) -> bool:
    for toks in _segments(command):
        # skip env assignments / wrappers: FOO=1 sudo env rm ...
        i = 0
        while i < len(toks) and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[i]) or toks[i] in ("sudo", "env", "command", "nice")):
            i += 1
        if i >= len(toks) or toks[i] != "rm":
            continue
        flags, targets = "", []
        for t in toks[i + 1:]:
            if t.startswith("-") and not targets:
                flags += t.lstrip("-")
            else:
                targets.append(t)
        if not ("r" in flags.lower() and "f" in flags):
            continue
        for t in targets:
            t2 = t.strip("'\"")
            if t2 in ROOT_TARGETS or t2.rstrip("/") in ("", "~", "$HOME", "${HOME}", ".."):
                return True
            if os.path.expanduser(os.path.expandvars(t2)).rstrip("/") in ("", os.path.expanduser("~")):
                return True
    return False


def is_git_commit_or_push(command: str) -> bool:
    for toks in _segments(command):
        if "git" in toks:
            j = toks.index("git")
            rest = [t for t in toks[j + 1:] if not t.startswith("-")]
            if rest and rest[0] in ("commit", "push"):
                return True
    return False


def scan_staged(cwd: str):
    """Return [(file, label)] for added lines in the staged diff that look like secrets."""
    try:
        out = subprocess.run(["git", "diff", "--cached", "-U0", "--no-color"],
                             cwd=cwd, capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return []
    hits, current = [], "?"
    for line in out.splitlines():
        if line.startswith("+++ "):
            current = line[4:].removeprefix("b/")
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if ALLOW_MARK in line:
            continue
        for label, rx in SECRET_PATTERNS:
            if rx.search(line):
                hits.append((current, label))
                break
    return hits


def main():
    harness = "claude-code"
    try:
        payload = _read_payload()
        harness = _harness(payload)
        if _disabled():
            _emit_allow(harness)
        command = _command(payload)
        if not command:
            _emit_allow(harness)
        if is_root_rm(command):
            _emit_deny(harness, "⛔ Comando destrutivo bloqueado",
                       "Blocked: rm -rf aimed at /, ~, $HOME or a parent directory. Never run it there.")
        if is_git_commit_or_push(command):
            hits = scan_staged(_cwd(payload))
            if hits:
                files = sorted({f"{f} ({l})" for f, l in hits})
                _emit_deny(harness,
                           "⛔ Possíveis secrets no diff staged: " + ", ".join(files),
                           "BLOCKED: staged changes add credential-looking content: "
                           + ", ".join(files)
                           + ". Remove the secret, use an env var, or add 'osforge:allow-secret' on a fixture line.")
        _emit_allow(harness)
    except SystemExit:
        raise
    except Exception as exc:  # fail-open, never break the session
        print(f"[scan-secrets] internal error, allowing: {exc!r}", file=sys.stderr)
        _emit_allow(harness)


if __name__ == "__main__":
    main()
