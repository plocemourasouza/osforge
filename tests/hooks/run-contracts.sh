#!/usr/bin/env bash
# =============================================================================
# run-contracts.sh — testes de CONTRATO dos hooks (B-006, ADR-015)
# =============================================================================
#
# Para cada linha de cases.tsv: pega a STRING DE COMANDO REAL do JSON de hooks
# (hooks/hooks-claude-code.json ou hooks/hooks.json), roda com a fixture no stdin,
# HOME/TMPDIR/estado num sandbox, e confere:
#   1. exit code 0                        — um hook nunca derruba a sessão
#   2. stdout vazio OU JSON válido         — inclusive com payload de 1 MB e payload que não é objeto
#   3. o veredito esperado, no contrato do harness (ver cabeçalho do cases.tsv)
#   4. nenhum arquivo novo em /tmp fora do sandbox   — pega logs em caminho fixo
#
# Sem rede, sem API, sem banco: ~segundos. Roda no preflight do deploy e no CI.
# USO:  ./tests/hooks/run-contracts.sh [--only CC-4]   (filtro por prefixo de id)
# =============================================================================
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ONLY="${2:-}"; [[ "${1:-}" == "--only" ]] || ONLY=""

SANDBOX="$(mktemp -d)"; trap 'rm -rf "$SANDBOX"' EXIT
export HOME="$SANDBOX/home"; mkdir -p "$HOME/.claude/hooks" "$HOME/.cursor/hooks" "$HOME/proj" "$SANDBOX/tmp"
export TMPDIR="$SANDBOX/tmp" OSFORGE_GATEGUARD_STATE_DIR="$SANDBOX/gg" OSFORGE_LOG_DIR="$SANDBOX/logs"
export OSFORGE_HOOK_DEBUG=1
# Nunca falar com um Canvas real nem com o banco real: o contrato é do hook, não do ambiente.
export OSFORGE_CANVAS_HEALTH_URL="http://127.0.0.1:1/api/health" OSFORGE_DB="$SANDBOX/db.sqlite"
unset OSFORGE_PROJECT
unset CLAUDE_SESSION_ID CLAUDE_PROJECT_DIR CLAUDE_TRANSCRIPT_PATH
cp "$ROOT"/hooks/*.sh "$ROOT"/hooks/*.py "$HOME/.claude/hooks/"; cp "$ROOT"/hooks/*.sh "$ROOT"/hooks/*.py "$HOME/.cursor/hooks/"
chmod +x "$HOME"/.claude/hooks/* "$HOME"/.cursor/hooks/*

ROOT="$ROOT" ONLY="$ONLY" SANDBOX="$SANDBOX" python3 - <<'PY'
import json, os, re, subprocess, sys, time, glob
ROOT, ONLY, SANDBOX = os.environ["ROOT"], os.environ["ONLY"], os.environ["SANDBOX"]
FIX = os.path.join(ROOT, "tests/hooks/fixtures")
HOME = os.environ["HOME"]
start = time.time() - 1

cc = json.load(open(os.path.join(ROOT, "hooks/hooks-claude-code.json")))["hooks"]
cu = json.load(open(os.path.join(ROOT, "hooks/hooks.json")))["hooks"]

def commands(harness, event, hook):
    conf = cc if harness == "claude-code" else cu
    out = []
    for entry in conf.get(event, []):
        # Claude Code: {"matcher", "hooks": [{"command"}]} · Cursor: {"command"}
        hs = entry.get("hooks") if isinstance(entry.get("hooks"), list) else [entry]
        for h in hs:
            cmd = h.get("command", "")
            if cmd and (hook == "*" or hook in cmd):
                out.append(cmd)
    return out

big = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash", "session_id": "big",
                  "tool_input": {"command": "echo " + "x" * (1024 * 1024 + 100)}})

def fixture(path):
    if path == "__BIG__":
        return big
    raw = open(os.path.join(FIX, path), encoding="utf-8").read()
    return raw.replace("__HOME__", HOME).replace("__FIXTURES__", FIX)

def verdict(harness, event, out):
    if out is None:
        return "silent"
    if out == "INVALID":
        return "invalid-json"
    if out == "TEXT":
        return "context" if event in ("SessionStart", "sessionStart") else "text"
    if harness == "cursor":
        return out.get("permission") or ("silent" if not out else "json")
    hso = out.get("hookSpecificOutput") or {}
    if hso.get("permissionDecision") == "deny":
        return "deny"
    if out.get("decision") == "block":
        return "block"
    if hso.get("additionalContext"):
        return "context"
    return "allow"

def tmp_snapshot():
    snap = {}
    for p in glob.glob("/tmp/agent-hooks.log") + glob.glob("/tmp/osforge-*"):
        try:
            snap[p] = os.path.getmtime(p)
        except OSError:
            pass
    return snap

def tmp_new_files(before):
    after = tmp_snapshot()
    return sorted(p for p, m in after.items() if p not in before or m > before[p])

fails, total = [], 0
for line in open(os.path.join(ROOT, "tests/hooks/cases.tsv"), encoding="utf-8"):
    line = line.rstrip("\n")
    if not line or line.startswith("#"):
        continue
    cid, harness, event, hook, fx, expect = line.split("\t")
    if ONLY and not cid.startswith(ONLY):
        continue
    cmds = commands(harness, event, hook)
    if not cmds:
        total += 1; fails.append((cid, "nenhum hook casa com evento/hook no JSON")); print(f"  FALHA {cid}: sem comando para {event}/{hook}"); continue
    payload = fixture(fx)
    for cmd in cmds:
        total += 1
        name = os.path.basename(cmd.split()[-1])
        before = tmp_snapshot()
        try:
            r = subprocess.run(["bash", "-c", cmd], input=payload, capture_output=True, text=True, timeout=20,
                               cwd=os.path.join(HOME, "proj"))
            rc, so = r.returncode, r.stdout.strip()
        except subprocess.TimeoutExpired:
            rc, so = "timeout", ""
        if not so:
            out = None
        else:
            try:
                out = json.loads(so)
                if not isinstance(out, dict):
                    out = "INVALID"
            except Exception:
                out = "TEXT" if (event in ("SessionStart", "sessionStart") and "{" not in so) else "INVALID"
        got = verdict(harness, event, out)
        problems = []
        if rc != 0:
            problems.append(f"exit={rc}")
        if out == "INVALID":
            problems.append("stdout não é JSON")
        if expect not in ("any",):
            ok = (got == expect) or (expect == "allow" and got in ("allow", "silent")) or (expect == "silent" and got == "allow" and harness == "claude-code" and not so)
            if not ok:
                problems.append(f"esperado={expect} obtido={got}")
        leaks = tmp_new_files(before)
        if leaks:
            problems.append("escreveu fora do sandbox: " + ", ".join(leaks))
        status = "ok  " if not problems else "FALHA"
        print(f"  {status} {cid:<6} {harness:<11} {event:<20} {name:<20} → {got}" + (f"   [{'; '.join(problems)}]" if problems else ""))
        if problems:
            fails.append((cid, name, "; ".join(problems)))

print()
if fails:
    print(f"FALHOU: {len(fails)} de {total} verificações")
    for f in fails: print("  -", *f)
    sys.exit(1)
print(f"PASSOU: {total}/{total} verificações")
PY
exit $?
