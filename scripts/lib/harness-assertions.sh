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

# ── Relatório versionável (B-012) ───────────────────────────────────────────
# emit_eval_report <suite> <arquivo_md> <casos.jsonl> <epoch_inicio> <comando> [logs...]
# Junta metadados (SHA, versão, modelo, HOME, tempo) + tokens somados dos streams e
# chama lib/eval_report.py. Sem isto, um número de eval em prosa não diz de quando é.
emit_eval_report() {
    local suite="$1" out="$2" cases="$3" started="$4" cmd="$5"; shift 5
    local toks; toks="$(python3 "${REPO_ROOT}/scripts/lib/stream_assert.py" tokens "$@" 2>/dev/null || echo '0 0 0 0')"
    local sha dirty version
    sha="$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    dirty="$(git -C "$REPO_ROOT" status --porcelain 2>/dev/null | head -1)"
    version="$(tr -d '[:space:]' < "$REPO_ROOT/VERSION" 2>/dev/null || echo dev)"
    python3 - "$suite" "$cases" "$started" "$cmd" "$sha" "$version" "$dirty" \
              "${MODEL:-?}" "${RUNS:-1}" "${HOME_OVERRIDE:-$HOME}" "$toks" "$out" \
              "${REPO_ROOT}/scripts/lib/eval_report.py" <<'PY' >/dev/null
import json, subprocess, sys, time, os
suite, cases, started, cmd, sha, version, dirty, model, runs, home, toks, out, gen = sys.argv[1:14]
rows = [json.loads(l) for l in open(cases, encoding="utf-8") if l.strip()]
i, o, cr, cc = (int(x) for x in toks.split())
payload = {
    "suite": suite, "model": model, "runs": int(runs), "command": cmd.strip(),
    "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(started))),
    "duration_s": int(time.time()) - int(started),
    "repo_sha": sha, "repo_version": version, "dirty": bool(dirty), "home": home,
    "tokens": {"input": i, "output": o, "cache_read": cr, "cache_create": cc},
    "cases": rows,
}
p = subprocess.run([sys.executable, gen, out], input=json.dumps(payload), text=True)
sys.exit(p.returncode)
PY
    echo "Relatório: $out"
}
