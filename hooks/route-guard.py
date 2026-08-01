#!/usr/bin/env python3
"""
route-guard.py — Stop hook

Enforcement DETERMINÍSTICO do contrato de roteamento (CLAUDE.md §route line),
no espírito do GateGuard: prosa pede, hook garante. Medido antes dele existir:
a linha de rota disparava em 14/16 demandas e a skill declarada era carregada
em ~metade — prompt-only chega nesse teto e para.

Verifica, na última resposta do assistant:
  1. Demanda acionável sem linha de rota  → bloqueia 1x pedindo a linha.
  2. Linha declara `skill: X` sem evidência de carga no transcript (invocação
     da Skill tool, Read/Bash do SKILL.md, ou despacho de subagente citando a
     skill) → bloqueia 1x: carregue ou declare `skill: none`.

Regras de segurança (aprendidas nos hooks anteriores):
- stop_hook_active no payload → exit 0 imediato (nunca criar loop de bloqueio).
- Falhou qualquer parse → exit 0 silencioso. Um guard que quebra a sessão é
  pior que nenhum guard.
- Respostas curtas/conversacionais (sem tool use e < LIMIAR chars) são tratadas
  como QUESTION → isentas, como o contrato define.
- Kill-switch: OSFORGE_ROUTEGUARD=off.

Saída de bloqueio (contrato de Stop hook do Claude Code):
  {"decision": "block", "reason": "<instrução>"}
"""

import json
import os
import re
import sys
from pathlib import Path

MAX_STDIN = 1024 * 1024
MAX_LINES = 4000
MIN_ACTIONABLE_CHARS = 700   # resposta menor e sem tools = conversa/QUESTION
LOG = "/tmp/osforge-route-guard.log"
DEBUG = os.environ.get("OSFORGE_HOOK_DEBUG", "") == "1"

ROUTE_RE = re.compile(r"🤖\s*route:", re.I)
SKILL_DECL_RE = re.compile(r"skill:\s*((?:`[^`]+`|\S+)(?:\s*\+\s*`[^`]+`)*)", re.I)


def log(msg):
    if DEBUG:
        try:
            with open(LOG, "a") as f:
                f.write(msg + "\n")
        except OSError:
            pass


def allow():
    sys.exit(0)


def block(reason):
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def main():
    if os.environ.get("OSFORGE_ROUTEGUARD", "") == "off":
        allow()
    try:
        payload = json.loads(sys.stdin.read(MAX_STDIN))
    except Exception:
        allow()

    # Nunca bloquear duas vezes — evita loop de Stop hook.
    if payload.get("stop_hook_active"):
        allow()

    tp = payload.get("transcript_path", "")
    if not tp or not Path(tp).exists():
        allow()

    try:
        lines = Path(tp).read_text(errors="replace").splitlines()[-MAX_LINES:]
    except OSError:
        allow()

    # Reconstituir a ÚLTIMA resposta do assistant: blocos de texto + tools usadas.
    texts, tools, skills_invoked, files_touched = [], [], set(), []
    last_user_seen = False
    for ln in reversed(lines):
        if not ln.strip().startswith("{"):
            continue
        try:
            e = json.loads(ln)
        except Exception:
            continue
        t = e.get("type")
        if t == "user" and not e.get("isMeta"):
            # paramos na última mensagem humana: tudo acima já é outra rodada
            content = (e.get("message") or {}).get("content")
            if isinstance(content, str) or (isinstance(content, list) and any(
                    isinstance(c, dict) and c.get("type") == "text" for c in content)):
                last_user_seen = True
                break
        if t == "assistant":
            for c in ((e.get("message") or {}).get("content") or []):
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "text":
                    texts.append(c.get("text", ""))
                elif c.get("type") == "tool_use":
                    name = c.get("name", "")
                    tools.append(name)
                    inp = json.dumps(c.get("input", {}), ensure_ascii=False)
                    if name == "Skill":
                        m = re.search(r'"skill":\s*"([^"]+)"', inp)
                        if m:
                            skills_invoked.add(m.group(1).split(":")[-1])
                    for m in re.finditer(r"skills/([a-zA-Z0-9_/-]+)/SKILL\.md", inp):
                        skills_invoked.add(m.group(1).split("/")[-1])
                    if name in ("Task", "Agent"):
                        files_touched.append(inp)  # despacho conta como carga por procuração

    if not last_user_seen and not texts:
        allow()

    response = "\n".join(reversed(texts))

    # QUESTION/conversa: sem tools e resposta curta → isento por contrato.
    actionable = bool(tools) or len(response) >= MIN_ACTIONABLE_CHARS
    if not actionable:
        allow()

    # 1. Linha de rota presente?
    if not ROUTE_RE.search(response):
        log("block: sem linha de rota")
        block(
            "Contrato de roteamento (CLAUDE.md): resposta acionável sem linha de rota. "
            "Adicione como PRIMEIRA linha: `🤖 route: @<agent> · skill: `<name>`|none · "
            "model: <haiku|sonnet|opus|fable>` — tokens nunca traduzidos — e então conclua."
        )

    # 2. Skill declarada foi carregada?
    m = SKILL_DECL_RE.search(response)
    if m:
        decl_raw = m.group(1)
        declared = [d.strip("`* ").split("/")[-1] for d in re.findall(r"`([^`]+)`", decl_raw)] or \
                   ([] if "none" in decl_raw.lower() else [decl_raw.strip().split("/")[-1]])
        dispatch_blob = " ".join(files_touched)
        missing = [d for d in declared
                   if d and d.lower() != "none"
                   and d not in skills_invoked
                   and d not in dispatch_blob]
        if missing:
            log(f"block: declaradas sem carga: {missing}")
            block(
                f"Contrato de roteamento (CLAUDE.md): a linha de rota declara skill(s) "
                f"{missing} mas nenhuma evidência de carga existe no transcript. Declarar "
                f"OBRIGA carregar: core → invoque via Skill tool; manifesto → leia o "
                f"SKILL.md; pesada → despache o subagente que a lê. Carregue agora e "
                f"aplique a disciplina, ou corrija a linha para `skill: none` assumindo a escolha."
            )

    allow()


if __name__ == "__main__":
    main()
