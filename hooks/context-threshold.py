#!/usr/bin/env python3
"""
context-threshold.py — UserPromptSubmit hook: aviso de contexto pelo USO REAL (B-021, R-06) +
aviso de janela de cota (B-027, SPEC-L01 Parte A3, D-2).

`claude-code/SKILLS.md` § "Context Budget" define as faixas (120–150k: salve estado e
termine o passo; >150k: PARE, compacte ou passe adiante) — mas até aqui a única fonte era a
intuição do modelo sobre o próprio contexto, que é ruim. Este hook lê o `message.usage` da
última resposta do assistente no transcript (input + cache_read + cache_creation = o que
realmente foi enviado ao modelo) e injeta o aviso da faixa UMA vez por faixa por sessão.

Faixas (tokens, sobrepostas por OSFORGE_CONTEXT_BANDS="120000,150000"):
  ≥ banda 1 → "salve estado e termine o passo atual"
  ≥ banda 2 → "PARE: handoff (osforge-db set-resume ou plano) e compacte / nova sessão"
Estado por sessão: $OSFORGE_CONTEXT_STATE_DIR (padrão ~/.osforge/context-threshold/<session_id>.json).
Lê só o FIM do transcript (últimos 512 KB) — < 40 ms mesmo em transcripts de dezenas de MB.
Padrão de leitura do `usage` visto no ECC `transcript-context.js` (MIT, E-B19); código próprio.

D-2: em vez de um hook novo (a contagem de "11 hooks" fica igual, EV-O12), o aviso de cota
(hooks/lib/quota.py) roda dentro deste mesmo UserPromptSubmit. É um processo a menos por
prompt e o mesmo padrão de estado — mas é uma checagem INDEPENDENTE: cada aviso (contexto,
cota) tem sua própria chave de desligamento e sua própria condição de disparo; os dois podem
aparecer juntos no mesmo `additionalContext`, um por linha.

Saída: {"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":…}} ou nada.
Silencioso e exit 0 em qualquer erro. Kill-switches: OSFORGE_CONTEXT_THRESHOLD=off (contexto),
OSFORGE_QUOTA_THRESHOLD=off (cota).
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
try:
    from quota import pending_warning as _quota_pending_warning
except Exception:                                    # pragma: no cover — never block the prompt
    _quota_pending_warning = None

MAX_STDIN = 1024 * 1024
TAIL_BYTES = 512 * 1024
DEFAULT_BANDS = (120_000, 150_000)
STATE_DIR = os.environ.get("OSFORGE_CONTEXT_STATE_DIR") or os.path.expanduser("~/.osforge/context-threshold")

MESSAGES = {
    1: ("Contexto em {tokens:,} tokens (faixa 120–150k do Context Budget): salve estado "
        "(`osforge-db set-resume` ou plano) e termine o passo atual; não comece tarefa nova nesta sessão."),
    2: ("Contexto em {tokens:,} tokens (>150k, dumb zone): PARE o que está fazendo, escreva o handoff "
        "(`osforge-db set-resume <slug> \"…\"` ou um plano) e compacte ou abra uma sessão nova. "
        "Não empurre a tarefa adiante neste contexto."),
}


def _bands():
    raw = os.environ.get("OSFORGE_CONTEXT_BANDS", "")
    try:
        vals = tuple(sorted(int(x) for x in raw.split(",") if x.strip()))
        return vals if len(vals) == 2 else DEFAULT_BANDS
    except ValueError:
        return DEFAULT_BANDS


def _payload():
    try:
        raw = sys.stdin.read(MAX_STDIN)
        d = json.loads(raw) if raw.strip() else {}
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def last_context_tokens(transcript_path):
    """Context size of the last assistant turn = input + cache_read + cache_creation. None if unknown."""
    try:
        size = os.path.getsize(transcript_path)
        with open(transcript_path, "rb") as f:
            if size > TAIL_BYTES:
                f.seek(size - TAIL_BYTES)
                f.readline()
            data = f.read().decode("utf-8", "replace")
    except OSError:
        return None
    for line in reversed(data.splitlines()):
        if '"usage"' not in line:
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        msg = e.get("message") if isinstance(e, dict) else None
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        u = msg.get("usage")
        if not isinstance(u, dict):
            continue
        total = 0
        for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
            v = u.get(k)
            if isinstance(v, (int, float)):
                total += int(v)
        return total
    return None


def band_for(tokens, bands):
    if tokens >= bands[1]:
        return 2
    if tokens >= bands[0]:
        return 1
    return 0


def _state_path(session_id):
    safe = "".join(c for c in str(session_id) if c.isalnum() or c in "-_")[:80] or "unknown"
    return os.path.join(STATE_DIR, safe + ".json")


def context_message(p):
    """The Context Budget message for this prompt, or None. Own kill-switch
    (OSFORGE_CONTEXT_THRESHOLD=off); independent of the quota warning below."""
    if os.environ.get("OSFORGE_CONTEXT_THRESHOLD", "").strip().lower() in ("off", "0", "false"):
        return None
    tp = p.get("transcript_path")
    if not isinstance(tp, str) or not tp:
        return None
    try:                                            # same hardening as session-save: only ~/.claude
        allowed = os.path.realpath(os.path.expanduser("~/.claude"))
        if not os.path.realpath(tp).startswith(allowed + os.sep):
            return None
    except Exception:
        return None
    tokens = last_context_tokens(tp)
    if tokens is None:
        return None
    band = band_for(tokens, _bands())
    if band == 0:
        return None
    sp = _state_path(p.get("session_id") or os.path.basename(tp))
    try:
        with open(sp, encoding="utf-8") as f:
            st = json.load(f)
        warned = int(st.get("band", 0)) if isinstance(st, dict) else 0
    except (OSError, ValueError):
        warned = 0
    if band <= warned:
        return None                                 # this band (or a higher one) already warned
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        tmp = sp + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"band": band, "tokens": tokens}, f)
        os.replace(tmp, sp)
    except OSError:
        pass                                        # still warn; may repeat once
    return "[OSForge context-threshold] " + MESSAGES[band].format(tokens=tokens)


def quota_message():
    """The quota-window message (A3), or None. Own kill-switch (OSFORGE_QUOTA_THRESHOLD=off);
    reads ~/.osforge/quota.json (hooks/lib/quota.py), not the transcript."""
    if _quota_pending_warning is None:
        return None
    try:
        return _quota_pending_warning()
    except Exception:
        return None


def main():
    p = _payload()
    parts = [m for m in (context_message(p), quota_message()) if m]
    if not parts:
        return
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                             "additionalContext": "\n".join(parts)}},
                     ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
