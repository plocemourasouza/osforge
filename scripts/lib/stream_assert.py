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
  run-status       LOG                 ok | error | quota (B-026, SPEC-L01 Parte B / B1)
  quota            LOG                 imprime o último `rate_limit_info` (JSON numa linha) ou nada
Uso pela biblioteca bash `harness-assertions.sh`; testado offline por tests/test-assertions.sh.
Regra de quota (B1) também usada por scripts/lib/judge.py, que importa is_quota_result() daqui em
vez de reimplementá-la -- as duas não podem divergir.
"""
import json
import re
import sys

READ_TOOLS = {"Read", "Glob", "Grep", "Bash"}
DISPATCH_TOOLS = {"Task", "Agent"}

# Same rule as scripts/lib/judge.py's is_quota(): a `result` event with `is_error` AND either
# the last `rate_limit_event`'s status is "rejected", or the result text carries rate-limit
# wording. No heuristic beyond these two (SPEC-L01 Part B, B1: "Nenhuma heurística além dessas
# duas").
RATE_LIMIT_TEXT_RE = re.compile(r"rate[ _-]?limit|usage limit|quota exceeded|limit reached", re.I)


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


def raw_events(log_path):
    """Yield each parsed top-level JSON object from a stream-json log, one per line. Tolerant
    of blank lines and malformed JSON (skipped silently). Unlike blocks(), this yields whole
    EVENTS (including `result` and `rate_limit_event`, which have no `message` wrapper), needed
    by run_status()/quota_info() below."""
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
            if isinstance(evt, dict):
                yield evt


def is_quota_result(result_event, rate_limit_info):
    """The exact B1 rule: a `result` event with `is_error` AND (the last `rate_limit_info`'s
    status is "rejected" OR the result text carries rate-limit wording). Mirrored by
    scripts/lib/judge.py's is_quota(), which imports this instead of reimplementing it."""
    if not result_event or not result_event.get("is_error"):
        return False
    if isinstance(rate_limit_info, dict) and rate_limit_info.get("status") == "rejected":
        return True
    text = " ".join(str(result_event.get(k, "")) for k in ("result", "error", "message"))
    return bool(RATE_LIMIT_TEXT_RE.search(text))


def _last_result_and_rate_limit(log_path):
    """Single pass over the log: the last `result` event and the last `rate_limit_info` seen
    (from `rate_limit_event`), each or None."""
    result = None
    rate_limit_info = None
    for evt in raw_events(log_path):
        t = evt.get("type")
        if t == "result":
            result = evt
        elif t == "rate_limit_event":
            candidate = evt.get("rate_limit_info")
            if isinstance(candidate, dict):
                rate_limit_info = candidate
    return result, rate_limit_info


def run_status(log_path):
    """B1: "ok" | "error" | "quota". No `result` event at all (e.g. a stream truncated by an
    external timeout kill) counts as "ok" -- absence of evidence is not evidence of quota, and
    the caller's own exit_code==124 timeout handling already covers that case."""
    result, rate_limit_info = _last_result_and_rate_limit(log_path)
    if result is None or not result.get("is_error"):
        return "ok"
    if is_quota_result(result, rate_limit_info):
        return "quota"
    return "error"


def quota_info(log_path):
    """The last `rate_limit_info` seen in the stream, or None."""
    _result, rate_limit_info = _last_result_and_rate_limit(log_path)
    return rate_limit_info


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
    if cmd == "run-status":
        print(run_status(log))
        return 0
    if cmd == "quota":
        info = quota_info(log)
        if info is not None:
            print(json.dumps(info))
        return 0
    if fn is None:
        print(f"subcomando desconhecido: {cmd}", file=sys.stderr)
        return 2
    return 0 if fn(log, arg) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
