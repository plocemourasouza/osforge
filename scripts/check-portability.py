#!/usr/bin/env python3
"""
check-portability.py — o que quebra na máquina do usuário, não aqui (B-008).

O CI roda `bash -n`, que só faz o parse: um `mapfile` num script bash passa a
verificação e só falha em tempo de execução, no /bin/bash 3.2 do macOS. Foi assim que
`scripts/install-skill.sh` — deployado em `~/.local/bin` e peça central do Model A —
ficou quebrado no Mac sem nenhum teste ou gate perceber.

Este script procura, nos arquivos que RODAM na máquina do usuário (deploy.sh, hooks/,
scripts/), construções que só existem no bash 4+ ou no userland GNU. Cada achado tem de
sumir ou ganhar uma exceção explícita na própria linha: `# portable-ok: <motivo>`.

Uso:  scripts/check-portability.py [ARQUIVO ...]     (padrão: os shell scripts versionados)
Exit 0 limpo, 1 com achados.
"""
import os
import re
import subprocess
import sys

WAIVER = "portable-ok"

# (regex, o que é, o que usar no lugar)
RULES = [
    (r"\bmapfile\b|\breadarray\b", "bash 4+ (mapfile/readarray)",
     "while IFS= read -r x; do arr+=(\"$x\"); done < <(...)"),
    (r"declare\s+-A|local\s+-A", "bash 4+ (array associativo)",
     "duas listas paralelas, um arquivo TSV, ou python3"),
    (r"\$\{[A-Za-z_][A-Za-z0-9_]*(,,|\^\^)", "bash 4+ (${v,,} / ${v^^})",
     "tr '[:upper:]' '[:lower:]'"),
    (r";;&|;&\s*$", "bash 4+ (fallthrough em case)", "repetir o ramo"),
    (r"\bgrep\b[^|;]*\s-[A-Za-z]*P", "GNU grep (-P)", "grep -E"),
    (r"\bsed\b\s+-i\s+(-e\s+)?['\"]?[^-'\" ]", "GNU sed (-i sem sufixo)",
     "sed -i '' no BSD, ou python3 / arquivo temporário"),
    (r"\bstat\s+-c\b", "GNU stat (-c)", "stat -c … 2>/dev/null || stat -f …"),
    (r"\bdate\s+-d\b", "GNU date (-d)", "python3 -c 'import time…'"),
    (r"\breadlink\s+-f\b", "GNU readlink (-f)", "python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))'"),
    (r"\bsha256sum\b", "GNU coreutils (sha256sum)",
     "command -v sha256sum >/dev/null && sha256sum || shasum -a 256"),
    (r"\btimeout\s+[0-9]", "GNU coreutils (timeout)",
     "detectar timeout/gtimeout e degradar sem limite"),
]

# Arquivos que só rodam em CI/dev (ubuntu + macos do GitHub, ou esta máquina).
# Continuam checados, mas um fallback na MESMA linha já basta — é o padrão `|| stat -f`.
def has_fallback(line):
    return ("||" in line or "command -v" in line or "2>/dev/null" in line
            or WAIVER in line)


def shell_files(argv):
    if argv:
        return argv
    try:
        out = subprocess.run(["git", "ls-files", "*.sh"], capture_output=True, text=True,
                             check=False).stdout.split()
    except OSError:
        out = []
    return [f for f in out if os.path.isfile(f)]


def main(argv):
    files = shell_files(argv)
    hits = 0
    for path in files:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue                      # comentário: só documenta
            for rx, what, fix in RULES:
                if not re.search(rx, line):
                    continue
                if has_fallback(line):
                    continue                  # já degrada sozinho
                hits += 1
                print(f"  ❌ {path}:{i}  {what}")
                print(f"     {stripped[:100]}")
                print(f"     use: {fix}   (ou `# {WAIVER}: <motivo>` na linha)")
    print(f"check-portability: {len(files)} script(s), {hits} construção(ões) não portável(is)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
