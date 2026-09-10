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

── User grant (liberação por confirmação do usuário) ───────────────────────────
  O mesmo script roda também como hook UserPromptSubmit. Quando o prompt do
  usuário contém uma autorização explícita ("tem permissão", "pode executar",
  "autorizo", "go ahead", ou uma afirmativa curta como "sim"/"pode"/"ok"), o
  hook grava um grant no estado da sessão; enquanto ativo, os gates permitem a
  operação e registram GRANT-ALLOW em denials.log. O grant vale até a próxima
  mensagem do usuário que não seja autorização, com teto GRANT_TTL_S
  (OSFORGE_GATEGUARD_GRANT_TTL, segundos, padrão 900).
  "gateguard: sessão liberada" abre o gate até o fim da sessão;
  "gateguard: ativa" / "revogo a permissão" fecham na hora.

── Session state ────────────────────────────────────────────────────────────────
  JSON file in ~/.osforge/gateguard/ keyed by CLAUDE_SESSION_ID or project path.
  Atomic write (write tmp + rename). Expires after 30 min of inactivity.

── Output format ────────────────────────────────────────────────────────────────
  Claude Code PreToolUse hooks must write JSON to stdout.
  Allow : exit 0, stdout empty or {"continue": true}
  Deny  : exit 0 (NOT exit 2), stdout JSON with hookSpecificOutput.permissionDecision="deny"
  The scan-secrets.sh convention uses {"continue": false, "permission": "deny", ...}
  This hook uses the newer hookSpecificOutput format (same effect, more structured).

Usage (PreToolUse, matcher Edit|Write|Bash — e também UserPromptSubmit):
  python3 ~/.claude/hooks/gateguard.py
O evento é detectado pelo campo hook_event_name do payload.
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


def _grant_ttl_s() -> int:
    """Teto absoluto (s) de um grant concedido por prompt. Env inválido → padrão."""
    try:
        v = int(os.environ.get("OSFORGE_GATEGUARD_GRANT_TTL", "") or 15 * 60)
        return v if v > 0 else 15 * 60
    except ValueError:
        return 15 * 60


GRANT_TTL_S         = _grant_ttl_s()
GRANT_SESSION_TTL_S = 12 * 60 * 60   # "gateguard: sessão liberada" — teto de segurança

DISABLE_VALUES = {"0", "false", "off", "disabled", "disable"}

STATE_DIR = Path(os.environ.get("OSFORGE_GATEGUARD_STATE_DIR", "") or
                 Path.home() / ".osforge" / "gateguard")

# ── Destructive Bash patterns ──────────────────────────────────────────────────

# Regex applied to quote-stripped command text (case-insensitive).
# High-signal only: patterns that irreversibly destroy data/history.

# SQL destrutivo so conta quando o comando de fato INVOCA um cliente de banco.
# Sem essa exigencia o verbo sozinho virava o sinal, e o verbo sozinho aparece em
# todo lugar. Cinco falsos positivos medidos numa unica sessao, todos reais:
#   grep -rn "DROP TABLE" prisma/migrations/
#   grep -rn "truncate" src/components/       (classe utilitaria do Tailwind)
#   cat src/utils/truncate-text.ts
#   echo "rode DROP TABLE x;" >> PROGRESS.md  (documentar o comando era bloqueado)
# Verbo em prosa nao e perigo. Verbo dentro de uma chamada a psql/mysql/prisma e.
_SQL_CLIENT = re.compile(
    r'(?:^|[\s;&|(`$])(?:'
    r'psql|mysql|mysqladmin|mariadb|sqlite3|mongosh|mongo|pgcli|mycli'
    r'|cockroach|clickhouse-client|duckdb|sqlcmd|dbmate|flyway|liquibase'
    r')\b'
    r'|\bprisma\s+(?:db\s+execute|db\s+push|migrate)\b',
    re.IGNORECASE,
)

# Verbos que destroem esquema ou dados de forma irreversivel.
# A lista antiga tinha so table/database/truncate/delete-from e deixava passar
# cinco formas medidas, todas por psql, todas sem gate nenhum:
#   ALTER TABLE x DROP CONSTRAINT y       (via docker exec ... psql <<SQL)
#   DROP SCHEMA public CASCADE
#   DROP ROLE mira_app
#   ALTER TABLE t DROP COLUMN c
#   DROP INDEX idx_x
# A alternativa `alter table ... drop` cobre a forma implicita do Postgres, em
# que a palavra COLUMN e opcional (ALTER TABLE x DROP c).
_DESTRUCTIVE_SQL = re.compile(
    r'\b(?:'
    r'drop\s+(?:table|database|schema|role|user|index|materialized\s+view|view'
    r'|sequence|constraint|column|type|domain|function|procedure|trigger'
    r'|policy|extension|tablespace|publication|subscription)\b'
    r'|alter\s+table\b[\s\S]{0,400}?\bdrop\b'
    r'|truncate\b'
    r'|delete\s+from\b'
    r')',
    re.IGNORECASE,
)


def _is_destructive_sql(cmd: str) -> bool:
    """True so quando um verbo destrutivo aparece num comando que invoca um
    cliente de banco. As duas condicoes sao necessarias: o verbo isolado gera
    falso positivo em prosa e em busca de texto; o cliente isolado e rotina.

    Checado no texto RAW, nao no _strip_quoted: SQL quase sempre vem citado
    (psql -c "..."), e remover aspas apagaria exatamente o conteudo perigoso.

    Limite conhecido e aceito: `psql -f arquivo.sql` nao e inspecionado -- o
    verbo mora no arquivo, fora do alcance de um hook que so ve o comando.
    """
    return bool(_SQL_CLIENT.search(cmd) and _DESTRUCTIVE_SQL.search(cmd))


# Ferramentas que apagam o banco inteiro sem que nenhum verbo SQL apareca no
# comando. Achado NOVO, fora dos falsos positivos/negativos relatados: nenhum
# padrao do guard cobria `prisma migrate reset`, que derruba e recria o schema.
# Nao depende de _SQL_CLIENT porque o proprio subcomando ja e o sinal.
_DESTRUCTIVE_TOOLING = re.compile(
    r'\bprisma\s+migrate\s+reset\b'
    r'|\bprisma\s+db\s+push\b[^\n]*--force-reset\b'
    r'|\brun\s+db:reset\b',
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
    """True for git push --force, git reset --hard, git clean -f (irreversível/compartilhado)."""
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
        # NOTA: `git commit --amend` e `git checkout/switch` foram REMOVIDOS do
        # gate — são rotina diária em dev local. Mantém-se só o que reescreve
        # história compartilhada (push --force) ou perde trabalho em massa
        # (reset --hard, clean -f).
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

    # SQL destrutivo: exige verbo destrutivo E invocacao de cliente de banco.
    # Ver _is_destructive_sql para os falsos positivos e negativos medidos que
    # motivaram cada metade da condicao.
    if _is_destructive_sql(raw):
        return True
    if _DESTRUCTIVE_TOOLING.search(raw):
        return True
    if _is_destructive_rm(raw):
        return True
    if _is_destructive_git(raw):
        return True
    # NOTA: overwrite-redirect (`> file`) foi REMOVIDO do gate — é operação
    # rotineira em trabalho local e gerava bloqueios constantes. O gate foca
    # apenas no irreversível/compartilhado (rm -rf, push --force, reset --hard,
    # clean -f, DROP/TRUNCATE/DELETE).
    return False


# ── User grant: liberação por confirmação explícita do usuário ────────────────
#
# Problema medido: o gate libera um comando destrutivo só na segunda tentativa
# IDÊNTICA (mesmo hash). Quando o usuário responde "tem permissão, pode rodar",
# o agente reformula o comando (novo hash → novo bloqueio) ou o estado de 30 min
# já expirou. O usuário autorizou, o gate seguiu barrando, e a autorização virou
# round-trip. O gate existe para forçar fatos ANTES de uma ação irreversível —
# não para desconfiar do próprio usuário.
#
# Mecanismo: este script roda também como hook UserPromptSubmit. Cada prompt do
# usuário passa por classify_prompt():
#   "grant"    → state["grant"] = {granted_at, expires_at, scope: "turn", excerpt}
#   "session"  → idem, scope "session": sobrevive a prompts comuns, só revoga
#   "revoke"   → apaga o grant
#   "none"     → apaga um grant de turno (a liberação vale só para o turno em
#                que foi dada); preserva um grant de sessão
# Enquanto o grant estiver ativo, os gates permitem a operação, registram
# GRANT-ALLOW em denials.log (auditável) e marcam o item como checado.
#
# O que NUNCA conta como autorização: negação a até 1 palavra antes da frase
# ("não tem permissão", "don't do it") e afirmativas curtas perdidas no meio de
# uma mensagem sobre outro assunto (a afirmativa curta só vale como mensagem
# inteira).

# "no" fica de fora: em português é "em o" ("rode no servidor, pode executar").
_NEG_WORD = r"(?:n[aã]o|nunca|jamais|nem|don'?t|do\s+not|never|not)"

# Uma negação até 1 palavra antes do ponto de match anula a autorização
# ("não tem permissão", "não te autorizo", "don't do it"). Mais longe que isso
# já é outra oração ("não precisa pedir, pode executar" é autorização).
_NEGATED_BEFORE = re.compile(_NEG_WORD + r"\s+(?:\S+\s+){0,1}$", re.IGNORECASE)

_AUTH_PHRASE = re.compile(
    r"(?:"
    # "você tem permissão", "possui autorização", "está autorizado/liberado"
    r"\b(?:tem|t[eê]m|tens|possui|possuem|est[aá]|est[aã]o|t[aá])\s+"
    r"(?:a\s+|minha\s+|total\s+|plena\s+|toda\s+a?\s*)?"
    r"(?:permiss[aã]o|autoriza[cç][aã]o|autorizad[oa]s?|liberad[oa]s?|aprovad[oa]s?|carta\s+branca)\b"
    # "autorizo", "libero", "aprovo", "confirmo"
    r"|\b(?:eu\s+)?(?:autorizo|libero|aprovo|confirmo|permito|concedo)\b"
    # "pode executar/apagar/…" (verbo de ação logo depois)
    r"|\bpode(?:m|s)?\s+(?:executar|rodar|apagar|deletar|excluir|remover|derrubar|dropar"
    r"|resetar|prosseguir|seguir|continuar|fazer|ir|aplicar|sobrescrever|for[cç]ar|limpar"
    r"|editar|escrever|criar|alterar|mudar|modificar|mexer|trocar|substituir|refatorar)\b"
    r"|\bvai\s+em\s+frente\b|\bmanda\s+(?:ver|bala)\b|\bsegue\s+o\s+jogo\b"
    # English
    r"|\byou\s+(?:have|got)\s+(?:my\s+|full\s+)?(?:permission|authorization|approval|the\s+green\s+light)\b"
    r"|\byou(?:'re|\s+are)\s+(?:authorized|allowed|cleared|approved)\b"
    r"|\bi\s+(?:authorize|approve|confirm|allow|grant)\b"
    r"|\bgo\s+ahead\b|\bproceed\b|\bdo\s+it\b|\bpermission\s+granted\b|\bgreen\s+light\b"
    r")",
    re.IGNORECASE,
)

# Afirmativa curta: a mensagem INTEIRA é composta só destas palavras.
_AFFIRM_WORDS = {
    "sim", "pode", "ok", "okay", "okey", "beleza", "blz", "isso", "certo", "claro",
    "confirmo", "confirmado", "autorizado", "autorizo", "liberado", "libera", "aprovado",
    "vai", "manda", "bora", "segue", "prossiga", "prossegue", "continua", "continue",
    "executa", "execute", "roda", "rode", "faz", "faça", "faca", "aplica", "aplique",
    "yes", "y", "yep", "yeah", "yup", "sure", "go", "approved", "confirmed",
    "affirmative", "granted", "proceed", "allowed",
}
_FILLER_WORDS = {
    "por", "favor", "please", "pls", "pf", "então", "entao", "agora", "já", "ja",
    "e", "a", "o", "de", "isso", "aí", "ai", "lá", "la", "mesmo", "senhor", "amigo",
    "ahead", "it", "do", "tudo", "com", "essa", "esse", "essas", "esses", "assim",
    "tá", "ta", "sim", "ok", "pode", "claro",
}
_SHORT_MAX_WORDS = 6

_SESSION_GRANT = re.compile(
    r"\bgateguard\b[\s:\-—]*(?:sess[aã]o\s+)?(?:liberad[ao]|liberar|off|desativa[r]?|desligad?[ao]?|release[d]?|disable[d]?)\b",
    re.IGNORECASE,
)
_REVOKE = re.compile(
    r"\bgateguard\b[\s:\-—]*(?:on|ativa[r]?|liga[r]?|volta[r]?|enable[d]?|ativad[ao])\b"
    r"|\b(?:revog[oa]|cancel[oa]|retir[oa]|remov[oa])\s+(?:a\s+|essa\s+|minha\s+)?(?:permiss[aã]o|autoriza[cç][aã]o|libera[cç][aã]o)\b"
    r"|\brevoke\b|\bpara\s+tudo\b|\bstop\s+everything\b",
    re.IGNORECASE,
)


def _tokens(text: str) -> list:
    return re.findall(r"[a-záàâãéêíóôõúüç']+", text.lower())


def _is_short_affirmative(prompt: str) -> bool:
    words = _tokens(prompt)
    if not words or len(words) > _SHORT_MAX_WORDS:
        return False
    if any(re.fullmatch(_NEG_WORD, w) for w in words):
        return False
    if not any(w in _AFFIRM_WORDS for w in words):
        return False
    return all(w in _AFFIRM_WORDS or w in _FILLER_WORDS for w in words)


def _has_auth_phrase(prompt: str) -> bool:
    for m in _AUTH_PHRASE.finditer(prompt):
        window = prompt[max(0, m.start() - 40):m.start()]
        if _NEGATED_BEFORE.search(window):
            continue
        return True
    return False


def classify_prompt(prompt: str) -> str:
    """Classifica um prompt do usuário: 'revoke' | 'session' | 'grant' | 'none'.

    Ordem importa: uma revogação explícita vence qualquer frase de autorização
    presente no mesmo texto ("revogo a permissão que dei")."""
    text = (prompt or "").strip()
    if not text:
        return "none"
    if _REVOKE.search(text):
        return "revoke"
    if _SESSION_GRANT.search(text):
        return "session"
    if _has_auth_phrase(text) or _is_short_affirmative(text):
        return "grant"
    return "none"


def _active_grant(state: dict):
    """Retorna o grant se existir e não tiver expirado; senão None."""
    g = state.get("grant")
    if not isinstance(g, dict):
        return None
    try:
        if float(g.get("expires_at", 0)) > time.time():
            return g
    except (TypeError, ValueError):
        pass
    return None


def apply_prompt_to_state(state: dict, prompt: str) -> tuple:
    """Aplica a classificação do prompt ao estado. Retorna (state, verdict)."""
    verdict = classify_prompt(prompt)
    now = time.time()
    if verdict == "revoke":
        state.pop("grant", None)
    elif verdict in ("grant", "session"):
        ttl = GRANT_SESSION_TTL_S if verdict == "session" else GRANT_TTL_S
        state["grant"] = {
            "granted_at": now,
            "expires_at": now + ttl,
            "scope": verdict if verdict == "session" else "turn",
            "excerpt": (prompt or "").strip().replace("\n", " ")[:120],
        }
    else:
        g = state.get("grant")
        if isinstance(g, dict) and g.get("scope") != "session":
            state.pop("grant", None)
    return state, verdict


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


def _log_denial(kind: str, detail: str) -> None:
    """Registra cada bloqueio em ~/.osforge/gateguard/denials.log para que o
    usuário possa monitorar a frequência do gate. Best-effort, nunca lança."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        line = "{}\t{}\t{}\n".format(
            time.strftime("%Y-%m-%dT%H:%M:%S"),
            kind,
            (detail or "").replace("\n", " ").replace("\t", " ")[:160],
        )
        with open(STATE_DIR / "denials.log", "a", encoding="utf-8") as fh:
            fh.write(line)
    except OSError:
        pass


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

_GRANT_HINT = (
    "\n\nSe o usuário já autorizou esta ação, NÃO reformule o comando: peça a ele uma "
    "confirmação explícita (ex.: \"tem permissão\", \"pode executar\", ou só \"sim\"). "
    "O GateGuard libera automaticamente para o turno seguinte."
)
_RECOVERY_HINT = (
    _GRANT_HINT
    + "\nRecovery: para desabilitar o gate nesta sessão, defina OSFORGE_GATEGUARD=off."
)


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
        + _GRANT_HINT
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


# ── UserPromptSubmit handler ──────────────────────────────────────────────────

def _handle_user_prompt(data: dict) -> None:
    """Classifica o prompt e persiste/limpa o grant. Best-effort: nunca bloqueia
    o prompt. Quando concede, injeta uma linha de contexto para o agente não
    gastar um round-trip apresentando fatos que o usuário já dispensou."""
    prompt = data.get("prompt")
    if not isinstance(prompt, str):
        return
    session_key = _resolve_session_key(data)
    state_path  = _state_path(session_key)
    state       = _load_state(state_path)
    state, verdict = apply_prompt_to_state(state, prompt)
    if verdict == "none":
        # Só toca o disco se havia algo a limpar.
        if state_path.exists():
            _save_state(state_path, state)
        return
    _save_state(state_path, state)
    _log_denial(f"GRANT-{verdict.upper()}", prompt)
    if verdict == "revoke":
        ctx = "[GateGuard] Liberação revogada pelo usuário: o gate volta a exigir fatos."
    elif verdict == "session":
        ctx = "[GateGuard] Usuário liberou o gate para o resto da sessão. Execute sem apresentar os fatos do gate; ainda assim diga o que vai rodar."
    else:
        ctx = (f"[GateGuard] Usuário autorizou explicitamente: gate liberado até a próxima "
               f"mensagem dele (máx. {GRANT_TTL_S // 60} min). Execute sem apresentar os "
               f"fatos do gate; ainda assim diga o que vai rodar.")
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": ctx,
        }
    }), flush=True)


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

    # ── UserPromptSubmit: classificar confirmação do usuário ──────────────────
    event = (data.get("hook_event_name") or "").strip()
    if event == "UserPromptSubmit" or ("prompt" in data and not data.get("tool_name")):
        try:
            _handle_user_prompt(data)
        except Exception as exc:  # FAIL-OPEN: um prompt nunca pode ser bloqueado por nós
            _warn_stderr(f"user-prompt handler failed ({exc!r}); ignoring.")
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

    grant = _active_grant(state)

    # ── Edit / Write gate ──────────────────────────────────────────────────────
    if tool_name in ("Edit", "Write"):
        file_path = (tool_input.get("file_path") or "").strip()

        if not file_path or _is_claude_settings(file_path):
            _allow()

        if not _is_checked(state, file_path):
            state = _mark_checked(state, file_path)
            if grant:
                _log_denial("GRANT-ALLOW", f"{tool_name} {file_path}")
                _save_state(state_path, state)
                _allow()
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
                if grant:
                    _log_denial("GRANT-ALLOW", f"MultiEdit {file_path}")
                    continue
                ok = _save_state(state_path, state)
                if not ok:
                    _warn_stderr(
                        "state could not be persisted (MultiEdit); allowing to avoid retry loop."
                    )
                    _allow()
                _deny(_edit_gate_msg(file_path))

        _save_state(state_path, state)
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
                if grant:
                    # Usuário autorizou explicitamente neste turno: permite,
                    # registra para auditoria e marca como checado.
                    _log_denial("GRANT-ALLOW", command)
                    state = _mark_checked(state, destructive_key)
                    _save_state(state_path, state)
                    _allow()
                _log_denial("BASH-DESTRUCTIVE", command)
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
