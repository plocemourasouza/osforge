#!/usr/bin/env python3
"""
observe-capture.py — PostToolUse hook para gravar observações no osforge-db.

Lê o payload JSON do Claude Code via stdin (PostToolUse hook format) e extrai
trigger_text a partir do nome da ferramenta + contexto do tool_input.

Silencioso por design: exit 0 sempre, sem stderr visível, para não bloquear
o fluxo principal em caso de falha de gravação.

Instalação no hooks-claude-code.json (NÃO edite diretamente — edite
hooks/hooks-claude-code.json no repositório osforge e rode ./deploy.sh):

  "PostToolUse": [
    {
      "matcher": "Edit|Write|Bash",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ~/.claude/hooks/observe-capture.py"
        }
      ]
    }
  ]

Variáveis de ambiente respeitadas:
  OSFORGE_OBSERVE_CAPTURE=0   desativa o hook (útil em CI)
  OSFORGE_DB=/path/to/db      caminho do banco (padrão: ~/.osforge/osforge.db)
  OSFORGE_PROJECT=<slug>      slug do projeto para o registro (padrão: detectado por cwd)
"""

import json
import os
import sys
import subprocess

# ──────────────────────────────────────────────
# Guard: desativar se OSFORGE_OBSERVE_CAPTURE=0
# ──────────────────────────────────────────────
if os.environ.get("OSFORGE_OBSERVE_CAPTURE", "1") == "0":
    sys.exit(0)

# ──────────────────────────────────────────────
# Leitura segura do payload stdin
# ──────────────────────────────────────────────
try:
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
except Exception:
    payload = {}

# ──────────────────────────────────────────────
# Extrair campos relevantes
# ──────────────────────────────────────────────
tool_name   = payload.get("tool_name", "")
tool_input  = payload.get("tool_input", {})
tool_result = payload.get("tool_result", {})

# Só captura ferramentas de escrita/execução (mais sinal, menos ruído)
CAPTURE_TOOLS = {"Edit", "Write", "Bash", "MultiEdit"}
if tool_name not in CAPTURE_TOOLS:
    sys.exit(0)

# ──────────────────────────────────────────────
# Construir trigger_text e context a partir do tool_input
# ──────────────────────────────────────────────
def _build_trigger(name: str, inp: dict) -> str:
    """Heurística simples: deriva trigger legível do tool_input."""
    if name in ("Edit", "Write"):
        path = inp.get("file_path", inp.get("path", ""))
        # Extrai extensão e diretório para dar contexto
        basename = os.path.basename(path) if path else ""
        dirname  = os.path.basename(os.path.dirname(path)) if path else ""
        if basename:
            return f"when editing {dirname}/{basename}" if dirname else f"when editing {basename}"
    if name == "Bash":
        cmd = str(inp.get("command", ""))[:80].strip()
        # Remove flags e pipes para simplificar
        first_token = cmd.split()[0] if cmd.split() else "bash"
        return f"when running {first_token}"
    return f"when using {name.lower()}"


def _build_context(name: str, inp: dict, result: dict) -> str:
    """Contexto curto: primeiros 120 chars do comando ou caminho."""
    if name == "Bash":
        return str(inp.get("command", ""))[:120]
    if name in ("Edit", "Write"):
        return str(inp.get("file_path", inp.get("path", "")))[:120]
    return ""


trigger_text = _build_trigger(tool_name, tool_input)
context_text = _build_context(tool_name, tool_input, tool_result)

# ──────────────────────────────────────────────
# Detectar projeto: env var ou basename do cwd
# ──────────────────────────────────────────────
project_slug = os.environ.get("OSFORGE_PROJECT", "")
if not project_slug:
    # Fallback: basename do diretório de trabalho atual
    cwd = os.environ.get("PWD", os.getcwd())
    project_slug = os.path.basename(cwd) or "unknown"

# ──────────────────────────────────────────────
# Chamar osforge-db add-observation
# ──────────────────────────────────────────────
osforge_db_bin = os.path.expanduser("~/.local/bin/osforge-db")
if not os.path.isfile(osforge_db_bin):
    # Fallback: fonte no repo de desenvolvimento (sem resolução por PATH,
    # que seria suscetível a hijack e nem funcionaria com `python3 <nome>`).
    _dev = os.path.expanduser("~/Development/osforge/scripts/osforge-db.py")
    if os.path.isfile(_dev):
        osforge_db_bin = _dev
    else:
        sys.exit(0)  # osforge-db indisponível — observação descartada silenciosamente

cmd = [
    "python3", osforge_db_bin,
    "add-observation",
    project_slug,
    trigger_text,
    f"--context={context_text}",
    f"--tool={tool_name}",
]

try:
    subprocess.run(
        cmd,
        timeout=5,
        capture_output=True,  # silencia stdout/stderr do subprocesso
        check=False,          # não propaga erros como exceção
    )
except Exception:
    pass  # silencioso — nunca bloqueia o Claude Code

sys.exit(0)
