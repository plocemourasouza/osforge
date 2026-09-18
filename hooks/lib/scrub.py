#!/usr/bin/env python3
"""
hooks/lib/scrub.py — remove segredos de texto ANTES de persistir ou reinjetar (B-019, E-A14, E-A23).

Um hook que grava o comando Bash, a primeira linha da mensagem do usuário ou o resume
da sessão no osforge-db estava guardando `Authorization: Bearer sk-ant-…` e chaves
coladas por engano, e o session-resume as devolvia ao contexto na sessão seguinte.
Tudo que sai para o banco ou volta para o modelo passa por `scrub()`.

Os padrões são os mesmos de hooks/scan-secrets.py (mantidos em sincronia à mão; o
teste tests/test-session-continuity.sh cobre os dois lados). Stdlib apenas.

    from scrub import scrub
    scrub("curl -H 'Authorization: Bearer sk-ant-abcdefghijklmnopqrstuvwxyz'")
    → "curl -H 'Authorization: Bearer [redacted:key]'"
"""
import re

_PATTERNS = [
    ("key",    re.compile(r"\bsk-[A-Za-z0-9_-]{20,120}\b")),
    ("token",  re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,255}\b")),
    ("token",  re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,255}\b")),
    ("key",    re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("token",  re.compile(r"\bxox[abpsr]-[A-Za-z0-9-]{10,200}\b")),
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}")),
    ("url-credential", re.compile(r"(://[^/\s:@]{1,64}:)[^@\s/]{3,128}@")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]{0,40}PRIVATE KEY-----[\s\S]*?(?:-----END [A-Z ]{0,40}PRIVATE KEY-----|$)")),
    ("secret", re.compile(
        r"(?i)(\b(?:private_key|secret_key|api_secret|api_key|aws_secret[a-z_]{0,32}|client_secret|"
        r"password|passwd|auth_token|access_token)\b\s*[=:]\s*['\"]?)[^\s'\"]{8,256}")),
]


def scrub(text):
    """Return `text` with every secret-looking span replaced by `[redacted:<kind>]`.
    Never raises; non-strings come back unchanged."""
    if not isinstance(text, str) or not text:
        return text
    out = text
    for kind, rx in _PATTERNS:
        if rx.groups:                     # keep the prefix group, redact the value
            out = rx.sub(lambda m, k=kind: f"{m.group(1)}[redacted:{k}]", out)
        else:
            out = rx.sub(f"[redacted:{kind}]", out)
    return out


def has_secret(text):
    return isinstance(text, str) and any(rx.search(text) for _, rx in _PATTERNS)


if __name__ == "__main__":
    import sys
    sys.stdout.write(scrub(sys.stdin.read()))
