#!/usr/bin/env bash
# =============================================================================
# harness-assertions.sh — lógica de veredito do harness de triggering
# =============================================================================
#
# Biblioteca compartilhada por:
#   scripts/test-skill-triggering.sh   (roda de verdade, consome API)
#   tests/test-assertions.sh           (exercita esta lógica offline)
#
# Existe como ARQUIVO, e não como trecho extraído do harness com sed, porque a
# extração por sed + `source <(...)` falhou silenciosamente no bash 3.2 do
# macOS: nenhuma função era definida, e como as chamadas eram feitas dentro de
# um wrapper que redirecionava stderr, o resultado parecia "asserção falhou"
# em vez de "biblioteca não carregou". Um arquivo sourceado normalmente não tem
# esse modo de falha.
#
# Requer definidos pelo chamador:
#   REPO_ROOT     raiz do repo OSForge
#   OUTPUT_BASE   diretório de trabalho (para o mapa de skills)
#
# O VEREDITO em si mora em lib/stream_assert.py (B-010): uma linha do stream é uma
# MENSAGEM com vários blocos, e o grep por linha deixava passar "texto que cita o
# caminho + tool_use de outro arquivo" como se a skill tivesse sido lida. O par
# (ferramenta, caminho) é conferido dentro do MESMO bloco tool_use. As funções abaixo
# são a interface bash desse motor e mantêm a assinatura antiga.
# =============================================================================

# Extrai skills acionadas do log (nome do campo "skill" nos eventos)
extract_triggered_skills() {
    local log_file="$1"
    grep -o '"skill":"[^"]*"' "$log_file" 2>/dev/null | \
        sed 's/"skill":"//;s/"//' | sort -u || true
}

# ── Invocação nativa ────────────────────────────────────────────────────────
# Evento da ferramenta Skill com o nome esperado (aceita namespace "ns:nome").

STREAM_ASSERT="${STREAM_ASSERT:-}"
_stream_assert() {
    if [ -z "$STREAM_ASSERT" ]; then
        STREAM_ASSERT="${REPO_ROOT}/scripts/lib/stream_assert.py"
    fi
    python3 "$STREAM_ASSERT" "$@"
}

check_skill_triggered() {
    _stream_assert skill-triggered "$1" "$2"
}

# ── Resolução via manifesto (Model A) ───────────────────────────────────────
# Só as skills de claude-code/skills-core.txt vivem em ~/.claude/skills e podem
# ser invocadas pela ferramenta Skill. As demais são alcançadas lendo o SKILL.md
# apontado pelo MANIFEST — exigir invocação nativa delas reprovaria 100% dos
# casos por construção, e o Model A ficaria sem critério de aceite.

SKILL_MAP_FILE="${OUTPUT_BASE:-/tmp}/skill-map.tsv"

# Mapa nome→path relativo. Indexa tanto o nome do diretório quanto o `name` do
# frontmatter, porque divergem em algumas skills (skills/evolve → osforge-evolve).
build_skill_map() {
    mkdir -p "$(dirname "$SKILL_MAP_FILE")"
    python3 - "$REPO_ROOT" > "$SKILL_MAP_FILE" <<'PY'
import re, sys
from pathlib import Path
root = Path(sys.argv[1]) / "skills"
for sf in sorted(root.rglob("SKILL.md")):
    rel = sf.parent.relative_to(root).as_posix()
    m = re.match(r"^---\s*\n(.*?)\n---", sf.read_text(encoding="utf-8", errors="replace"), re.S)
    fm = m.group(1) if m else ""
    n = re.search(r'^name:\s*["\']?([^"\'#\n]+)["\']?\s*$', fm, re.M)
    keys = {sf.parent.name}
    if n:
        keys.add(n.group(1).strip())
    for k in keys:
        print(f"{k}\t{rel}")
PY
}

skill_rel_path() {
    awk -F'\t' -v n="$1" '$1==n {print $2; exit}' "$SKILL_MAP_FILE" 2>/dev/null || true
}

is_core_skill() {
    local rel="$1"
    [ -z "$rel" ] && return 1
    grep -qxF "$rel" "$REPO_ROOT/claude-code/skills-core.txt" 2>/dev/null
}

# PASS por resolução: o stream mostra uma LEITURA do SKILL.md da skill esperada.
# Nome da ferramenta e caminho têm de estar no MESMO BLOCO tool_use — citar o caminho
# num bloco de texto da mesma mensagem não conta como ter alcançado a skill.
# Carga por procuração: despacho de subagente cujo prompt cita o SKILL.md ou o nome da
# skill — a leitura acontece DENTRO do subagente, invisível no stream principal.
check_skill_resolved() {
    _stream_assert skill-resolved "$1" "$2"
}

# ── Roteamento do orquestrador ──────────────────────────────────────────────
# O CLAUDE.md/orchestrator promete saídas verificáveis: anúncio de persona
# (`@agent-name`), despacho via Task/Agent (`"subagent_type":"<name>"`), ou
# leitura do AGENT.md. Qualquer uma das três evidências conta.

# Texto do assistant concatenado (para asserções de prosa: @agent, tier).
response_text() {
    _stream_assert text "$1"
}

# Agente esperado alcançado? Aceita lista separada por | (alternativas válidas).
# Evidências: anúncio deliberado (@nome, `nome`, **nome**), despacho real, leitura do AGENT.md.
check_agent_routed() {
    _stream_assert agent-routed "$1" "$2"
}

# Delegação DE VERDADE: só despacho de subagente conta (B-010). Casos cujo contrato é
# "isto tem de virar subagente" usam esta asserção — anunciar `@security-auditor` e
# responder sozinho satisfazia a asserção antiga e não é delegar.
check_agent_dispatched() {
    _stream_assert agent-dispatched "$1" "$2"
}

# Tier de modelo citado na resposta (Roster do plano / manifesto de tasks).
check_tier_mentioned() {
    _stream_assert tier "$1" "$2"
}

# ── Guarda de cota (B-026 / SPEC-L01 Parte B) ───────────────────────────────
# B1: ok | error | quota para UMA execução (stream de UM `claude -p`).
run_status_of() {
    _stream_assert run-status "$1"
}

# B3: preflight antes de CADA caso. Reusa hooks/lib/quota.py:read_state() -- o MESMO leitor
# que a A3 usa -- em vez de reimplementar o parse de quota.json aqui. Fail-open por design: sem
# quota.json, com dado stale, ou qualquer erro de leitura -> exit 1 (segue). Cota é parada
# ADVISÓRIA; a ausência do dado nunca deve, por si só, travar a suíte.
#   stdout: uma linha com o motivo, só quando for parar
#   exit:   0 = pare o lote antes deste caso · 1 = siga
quota_preflight_reason() {
    local threshold="${OSFORGE_EVAL_QUOTA_STOP:-85}"
    python3 - "$REPO_ROOT" "$threshold" <<'PY'
import os, sys, time
sys.path.insert(0, os.path.join(sys.argv[1], "hooks", "lib"))
try:
    from quota import read_state
except Exception:
    sys.exit(1)

threshold = float(sys.argv[2])
now = time.time()
state = read_state(now)
if not state:
    sys.exit(1)

five = state.get("five_hour")
if isinstance(five, dict):
    pct = five.get("pct")
    if isinstance(pct, (int, float)) and pct >= threshold:
        print("five_hour.pct=%.0f >= OSFORGE_EVAL_QUOTA_STOP=%.0f" % (pct, threshold))
        sys.exit(0)

rejected = state.get("rejected")
if isinstance(rejected, dict):
    resets_at = rejected.get("resets_at")
    if isinstance(resets_at, (int, float)) and resets_at > now:
        print("rejected, resets_at=%d (ainda no futuro)" % int(resets_at))
        sys.exit(0)

sys.exit(1)
PY
}

# Snapshot de quota.json (read_state() agora) como JSON numa linha, ou "null". Para
# quota_at_start/quota_at_end no relatório (B3).
quota_snapshot() {
    python3 - "$REPO_ROOT" <<'PY'
import os, sys, json, time
sys.path.insert(0, os.path.join(sys.argv[1], "hooks", "lib"))
try:
    from quota import read_state
except Exception:
    print("null")
else:
    state = read_state(time.time())
    print(json.dumps(state) if state is not None else "null")
PY
}

# emit_not_run_case <case_json_file> <id> <n> <critical:0|1> <detail>
# Uma linha "NOT RUN" no formato que suite_verdict()/eval_report.py esperam -- fora do k de N
# (B2/B3): a cota parou o lote antes deste caso rodar, não é um miss.
emit_not_run_case() {
    local case_json="$1" id="$2" n="$3" critical="$4" detail="$5"
    python3 -c '
import json, sys
print(json.dumps({"id": sys.argv[1], "k": 0, "n": int(sys.argv[2]), "verdict": "NOT RUN",
                   "detail": sys.argv[3], "critical": sys.argv[4] == "1"}, ensure_ascii=False))
' "$id" "$n" "$detail" "$critical" >> "$case_json"
}

# ── Veredito da suíte com casos críticos (N-01 / B-025) ─────────────────────
# Um caso `critical` (negação, ou positivo caro de errar) pesa mais que os
# outros: reprova a suíte mesmo com --allow-flaky, e se ele nem chegou a
# rodar (cota esgotada — NOT RUN, L-01), a suíte não é aprovada nem
# reprovada: fica INCOMPLETE. Um caso não-crítico continua com a regra de
# sempre (FAIL/TIMEOUT reprovam; FLAKY reprova só sem --allow-flaky).
#
# suite_verdict <casos.jsonl> <allow_flaky:0|1>
#   casos.jsonl: uma linha por caso, {"verdict": "PASS|FLAKY|FAIL|TIMEOUT|NOT RUN", "critical": bool}
#   stdout: PASS | FAIL | INCOMPLETE
#   exit:   0 (PASS) | 1 (FAIL) | 2 (INCOMPLETE)
suite_verdict() {
    local cases_jsonl="$1" allow_flaky="$2"
    python3 - "$cases_jsonl" "$allow_flaky" <<'PY'
import json, sys

path, allow_flaky = sys.argv[1], sys.argv[2] == "1"
with open(path, encoding="utf-8") as fh:
    cases = [json.loads(line) for line in fh if line.strip()]

bad = {"FAIL", "TIMEOUT", "FLAKY"}
crit_bad = [c for c in cases if c.get("critical") and c.get("verdict") in bad]
crit_not_run = [c for c in cases if c.get("critical") and c.get("verdict") == "NOT RUN"]
noncrit_bad = [c for c in cases if not c.get("critical") and c.get("verdict") in ("FAIL", "TIMEOUT")]
noncrit_flaky = [c for c in cases if not c.get("critical") and c.get("verdict") == "FLAKY"]

if crit_bad:
    print("FAIL"); sys.exit(1)
if crit_not_run:
    print("INCOMPLETE"); sys.exit(2)
if noncrit_bad:
    print("FAIL"); sys.exit(1)
if noncrit_flaky and not allow_flaky:
    print("FAIL"); sys.exit(1)
print("PASS"); sys.exit(0)
PY
}

# ── Relatório versionável (B-012) ───────────────────────────────────────────
# emit_eval_report <suite> <arquivo_md> <casos.jsonl> <epoch_inicio> <comando> [logs...]
# Junta metadados (SHA, versão, modelo, HOME, tempo) + tokens somados dos streams e
# chama lib/eval_report.py. Sem isto, um número de eval em prosa não diz de quando é.
#
# Cota (B-026, B3): se as variáveis QUOTA_AT_START/QUOTA_AT_END estiverem definidas no
# ambiente (JSON de quota_snapshot(), ou "null"), entram no payload como quota_at_start/
# quota_at_end. Env em vez de parâmetro posicional para não quebrar as três chamadas
# existentes -- os dois são opcionais e ausentes vira "sem dados" no relatório.
emit_eval_report() {
    local suite="$1" out="$2" cases="$3" started="$4" cmd="$5"; shift 5
    local toks; toks="$(python3 "${REPO_ROOT}/scripts/lib/stream_assert.py" tokens "$@" 2>/dev/null || echo '0 0 0 0')"
    local sha dirty version
    sha="$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    dirty="$(git -C "$REPO_ROOT" status --porcelain 2>/dev/null | head -1)"
    version="$(tr -d '[:space:]' < "$REPO_ROOT/VERSION" 2>/dev/null || echo dev)"
    python3 - "$suite" "$cases" "$started" "$cmd" "$sha" "$version" "$dirty" \
              "${MODEL:-?}" "${RUNS:-1}" "${HOME_OVERRIDE:-$HOME}" "$toks" "$out" \
              "${REPO_ROOT}/scripts/lib/eval_report.py" "${QUOTA_AT_START:-null}" "${QUOTA_AT_END:-null}" <<'PY' >/dev/null
import json, subprocess, sys, time, os
suite, cases, started, cmd, sha, version, dirty, model, runs, home, toks, out, gen, qstart, qend = sys.argv[1:16]
rows = [json.loads(l) for l in open(cases, encoding="utf-8") if l.strip()]
i, o, cr, cc = (int(x) for x in toks.split())
try:
    quota_start = json.loads(qstart)
except ValueError:
    quota_start = None
try:
    quota_end = json.loads(qend)
except ValueError:
    quota_end = None
payload = {
    "suite": suite, "model": model, "runs": int(runs), "command": cmd.strip(),
    "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(started))),
    "duration_s": int(time.time()) - int(started),
    "repo_sha": sha, "repo_version": version, "dirty": bool(dirty), "home": home,
    "tokens": {"input": i, "output": o, "cache_read": cr, "cache_create": cc},
    "quota_at_start": quota_start, "quota_at_end": quota_end,
    "cases": rows,
}
p = subprocess.run([sys.executable, gen, out], input=json.dumps(payload), text=True)
sys.exit(p.returncode)
PY
    echo "Relatório: $out"
}
