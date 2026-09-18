#!/usr/bin/env bash
# =============================================================================
# test-scan-secrets.sh — trava o hook scan-secrets nos DOIS formatos de payload
# =============================================================================
#
# Antes do B-002 o hook lia `command` na raiz do JSON (formato Cursor). No
# Claude Code o comando vem em `tool_input.command`, então o hook respondia
# "allow" para tudo (auditoria 2026-09-18, E-A01). Este teste roda o hook de
# ponta a ponta, offline, com um repositório git temporário e segredos falsos.
#
# USO:  ./tests/test-scan-secrets.sh
# =============================================================================
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK="$ROOT/hooks/scan-secrets.sh"
[[ -x "$HOOK" ]] || { echo "FALHA: hook não encontrado/executável: $HOOK"; exit 1; }
command -v git >/dev/null || { echo "SKIP: git ausente"; exit 0; }

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
export HOME="$WORK/home"; mkdir -p "$HOME"
REPO="$WORK/repo"; mkdir -p "$REPO"
( cd "$REPO" && git init -q && git config user.email t@t && git config user.name t \
  && echo "x" > a.txt && git add a.txt && git commit -qm init )

SCAN_HOOK="$HOOK" SCAN_REPO="$REPO" python3 - <<'PY'
import json, os, subprocess, sys
HOOK, REPO = os.environ["SCAN_HOOK"], os.environ["SCAN_REPO"]
falhas, total = [], 0

def check(nome, obtido, esperado):
    global total; total += 1
    ok = obtido == esperado
    if not ok: falhas.append((nome, esperado, obtido))
    print("  {}  {:<64} esperado={!s:<6} obtido={!s}".format("ok  " if ok else "FALHA", nome[:64], esperado, obtido))

def run(payload, env=None):
    r = subprocess.run([HOOK], input=json.dumps(payload) if payload is not None else "not json",
                       capture_output=True, text=True, timeout=30, env={**os.environ, **(env or {})})
    out = r.stdout.strip()
    try: js = json.loads(out) if out else None
    except Exception: js = "INVALID"
    return r.returncode, js

def cc(cmd):  # Claude Code shape
    return run({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": REPO})
def cursor(cmd):
    return run({"command": cmd, "workspace_roots": [REPO]})
def verdict_cc(res):
    rc, js = res
    if rc != 0: return f"exit{rc}"
    if js is None: return "allow"
    if js == "INVALID": return "invalid-json"
    return (js.get("hookSpecificOutput") or {}).get("permissionDecision", "allow")
def verdict_cursor(res):
    rc, js = res
    if rc != 0: return f"exit{rc}"
    if not isinstance(js, dict): return "invalid"
    return js.get("permission")

def stage(name, content):
    with open(os.path.join(REPO, name), "w") as f: f.write(content)
    subprocess.run(["git", "add", name], cwd=REPO, check=True)
def unstage_all():
    subprocess.run(["git", "reset", "-q"], cwd=REPO, check=True)

print("\n[1] rm -rf de raiz — Claude Code (E-A01)")
for cmd in ["rm -rf ~", "rm -rf /", "rm -fr $HOME", "rm -r -f ../", 'rm -rf "$HOME"', "cd /tmp && rm -rf ~", "sudo rm -rf /*"]:
    check(f"CC deny: {cmd}", verdict_cc(cc(cmd)), "deny")
for cmd in ["rm -rf build/", "rm -rf ./node_modules", "ls -la ~", "echo rm -rf /", "rm -f /tmp/x.log"]:
    check(f"CC allow: {cmd}", verdict_cc(cc(cmd)), "allow")
print("\n[2] rm -rf de raiz — Cursor")
check("Cursor deny rm -rf ~", verdict_cursor(cursor("rm -rf ~")), "deny")
check("Cursor allow ls", verdict_cursor(cursor("ls")), "allow")

print("\n[3] secrets no diff staged")
check("commit sem staged → allow", verdict_cc(cc("git commit -m x")), "allow")
stage("cfg.py", "API_KEY = 'sk-ant-api03-" + "A" * 40 + "'\n")
check("CC: sk-… staged bloqueia commit", verdict_cc(cc("git commit -m x")), "deny")
check("CC: bloqueio cita o arquivo", "cfg.py" in json.dumps(cc("git commit -m x")[1]), True)
check("Cursor: mesmo caso bloqueia", verdict_cursor(cursor("git commit -m x")), "deny")
check("CC: push também é checado", verdict_cc(cc("git push origin main")), "deny")
check("CC: comando não-git com secret staged passa", verdict_cc(cc("npm test")), "allow")
unstage_all()
stage("tok.env", "GITHUB_TOKEN=ghp_" + "b" * 36 + "\n")
check("ghp_ token bloqueia", verdict_cc(cc("git commit -am x")), "deny")
unstage_all()
stage("aws.txt", "AKIAIOSFODNN7EXAMPLE\n")
check("AKIA bloqueia", verdict_cc(cc("git commit -m x")), "deny")
unstage_all()
stage("db.txt", "postgres://user:s3cretpass@db.internal:5432/app\n")
check("credencial em URL bloqueia", verdict_cc(cc("git commit -m x")), "deny")
unstage_all()
stage("key.pem", "-----BEGIN RSA PRIVATE KEY-----\nabc\n")
check("bloco PEM bloqueia", verdict_cc(cc("git commit -m x")), "deny")
unstage_all()
stage("legacy.py", "password = \"hunter2hunter2\"\n")
check("password = … (regra legada) bloqueia", verdict_cc(cc("git commit -m x")), "deny")
unstage_all()
stage("fixture.py", "KEY = 'sk-ant-" + "C" * 40 + "'  # osforge:allow-secret\n")
check("marca osforge:allow-secret libera fixture", verdict_cc(cc("git commit -m x")), "allow")
unstage_all()
stage("normal.py", "def f():\n    return 'sketchy but fine'\n")
check("conteúdo normal passa", verdict_cc(cc("git commit -m x")), "allow")
unstage_all()

print("\n[4] contratos e falha aberta")
check("CC allow = stdout vazio", cc("ls")[1], None)
check("Cursor allow = JSON permission allow", cursor("ls")[1], {"continue": True, "permission": "allow"})
check("JSON inválido → allow, exit 0", run(None)[0], 0)
check("payload sem comando → allow", verdict_cc(run({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {}})), "allow")
check("kill-switch OSFORGE_SCAN_SECRETS=off", verdict_cc(run({"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rm -rf ~"}}, {"OSFORGE_SCAN_SECRETS":"off"})), "allow")
big = "echo " + "x" * (2 * 1024 * 1024)
check("payload > 1 MB não derruba", run({"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command": big}})[0], 0)

print()
if falhas:
    print("FALHOU: {} de {} casos".format(len(falhas), total))
    for n, e, o in falhas: print("  - {}: esperava {!r}, obteve {!r}".format(n, e, o))
    sys.exit(1)
print("PASSOU: {}/{} casos".format(total, total))
PY
exit $?
