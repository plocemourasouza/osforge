#!/usr/bin/env python3
"""
stream_assert.py — veredito de um stream-json do `claude -p`, por BLOCO (B-010, E-A45).

O harness decidia com `grep` por linha. Uma linha do stream é uma MENSAGEM inteira, com
vários blocos de conteúdo: um `text` que cita `skills/x/SKILL.md` e, no mesmo evento, um
`tool_use` de Read de OUTRO arquivo passavam como "skill alcançada". Aqui o par
(ferramenta, caminho) tem de estar no MESMO bloco `tool_use` — é isso que distingue ter
lido a skill de ter falado dela.

Subcomandos (exit 0 = evidência encontrada, 1 = não; stdout vazio salvo em `--explain`):
  skill-triggered  LOG NOME            ferramenta Skill com esse nome (aceita "ns:nome")
  skill-resolved   LOG REL             Read/Glob/Grep/Bash de skills/REL/SKILL.md, ou
                                       despacho de subagente que cita o SKILL.md / o nome
  agent-routed     LOG "a|b"           anúncio @a, despacho subagent_type=a, ou leitura de agents/a
  agent-dispatched LOG "a|b"           SÓ despacho real (Task/Agent com subagent_type ou nome no prompt)
  tier             LOG "sonnet|opus"   palavra de tier no texto do assistant
  text             LOG                 imprime o texto do assistant concatenado
  tokens           LOG...              soma `usage` dos logs: "in out cache_read cache_create"
Uso pela biblioteca bash `harness-assertions.sh`; testado offline por tests/test-assertions.sh.
"""
import json
import re
import sys

READ_TOOLS = {"Read", "Glob", "Grep", "Bash"}
DISPATCH_TOOLS = {"Task", "Agent"}


def blocks(log_path):
    """Yield (role, block) for every content block of every message in the stream."""
    try:
        fh = open(log_path, encoding="utf-8", errors="replace")
    except OSError:
        return
    with fh:
        for line in fh:
            line = line.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                evt = json.loads(line)
            except ValueError:
                continue
            if not isinstance(evt, dict):
                continue
            msg = evt.get("message")
            role = (msg or {}).get("role") or evt.get("type") or ""
            content = (msg or {}).get("content") if isinstance(msg, dict) else evt.get("content")
            if isinstance(content, str):
                yield role, {"type": "text", "text": content}
            elif isinstance(content, list):
                for b in content:
                    if isinstance(b, dict):
                        yield role, b


def tool_uses(log_path, names=None):
    for _role, b in blocks(log_path):
        if b.get("type") != "tool_use":
            continue
        if names is None or b.get("name") in names:
            yield b


def block_text(log_path):
    return "\n".join(b.get("text", "") for role, b in blocks(log_path)
                     if b.get("type") == "text" and role in ("assistant", ""))


def _input_str(block):
    try:
        return json.dumps(block.get("input", {}), ensure_ascii=False)
    except (TypeError, ValueError):
        return str(block.get("input", ""))


def skill_triggered(log, name):
    pat = re.compile(r"^([^:]*:)?" + re.escape(name) + r"$")
    for b in tool_uses(log, {"Skill"}):
        inp = b.get("input") or {}
        val = inp.get("skill") or inp.get("name") or inp.get("command") or ""
        if isinstance(val, str) and pat.match(val.strip()):
            return True
    return False


def skill_resolved(log, rel):
    """Read/Glob/Grep/Bash whose OWN input names skills/<rel>/SKILL.md, or a subagent
    dispatch citing it (the read then happens inside the subagent, invisible here)."""
    if not rel:
        return False
    needle = f"skills/{rel}/SKILL.md"
    for b in tool_uses(log, READ_TOOLS):
        if needle in _input_str(b):
            return True
    base = rel.rsplit("/", 1)[-1]
    word = re.compile(r"\b" + re.escape(base) + r"\b")
    for b in tool_uses(log, DISPATCH_TOOLS):
        s = _input_str(b)
        if needle in s or word.search(s):
            return True
    return False


def agent_dispatched(log, alts):
    for a in [x for x in alts.split("|") if x]:
        word = re.compile(r"\b" + re.escape(a) + r"\b")
        for b in tool_uses(log, DISPATCH_TOOLS):
            inp = b.get("input") or {}
            if isinstance(inp, dict) and inp.get("subagent_type") == a:
                return True
            if word.search(_input_str(b)):
                return True
        # despacho registrado fora de um bloco tool_use (formatos antigos do stream)
        for _role, blk in blocks(log):
            if blk.get("type") == "tool_use":
                continue
            if isinstance(blk, dict) and blk.get("subagent_type") == a:
                return True
    return False


def agent_routed(log, alts):
    if agent_dispatched(log, alts):
        return True
    text = block_text(log)
    for a in [x for x in alts.split("|") if x]:
        # nomeação deliberada: @nome, `nome`, **nome** — menção nua em prosa não conta
        if re.search(r"(@%s|\*\*%s\*\*|`%s`)" % (re.escape(a), re.escape(a), re.escape(a)), text):
            return True
        for b in tool_uses(log, {"Read", "Bash"}):
            if f"agents/{a}" in _input_str(b):
                return True
    return False


def tier_mentioned(log, tiers):
    text = block_text(log)
    for t in [x for x in tiers.split("|") if x]:
        if re.search(r"\b" + re.escape(t) + r"\b", text, re.I):
            return True
    return False


def tokens(paths):
    """Soma o usage de cada mensagem do assistente, uma vez por message.id (o stream
    repete a mesma mensagem por bloco de conteúdo). Devolve os quatro totais."""
    tot = {"input_tokens": 0, "output_tokens": 0,
           "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    seen = set()
    for path in paths:
        try:
            fh = open(path, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                if '"usage"' not in line:
                    continue
                try:
                    evt = json.loads(line)
                except ValueError:
                    continue
                msg = evt.get("message") if isinstance(evt, dict) else None
                if not isinstance(msg, dict) or msg.get("role") != "assistant":
                    continue
                u = msg.get("usage")
                if not isinstance(u, dict):
                    continue
                mid = (path, msg.get("id") or evt.get("uuid"))
                if mid in seen:
                    continue
                seen.add(mid)
                for k in tot:
                    v = u.get(k)
                    if isinstance(v, (int, float)):
                        tot[k] += int(v)
    return tot


def main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    cmd, log = argv[0], argv[1]
    arg = argv[2] if len(argv) > 2 else ""
    fn = {"skill-triggered": skill_triggered, "skill-resolved": skill_resolved,
          "agent-routed": agent_routed, "agent-dispatched": agent_dispatched,
          "tier": tier_mentioned}.get(cmd)
    if cmd == "text":
        print(block_text(log))
        return 0
    if cmd == "tokens":
        t = tokens(argv[1:])
        print("%d %d %d %d" % (t["input_tokens"], t["output_tokens"],
                               t["cache_read_input_tokens"], t["cache_creation_input_tokens"]))
        return 0
    if fn is None:
        print(f"subcomando desconhecido: {cmd}", file=sys.stderr)
        return 2
    return 0 if fn(log, arg) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
