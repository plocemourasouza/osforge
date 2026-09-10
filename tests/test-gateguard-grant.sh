#!/usr/bin/env bash
# =============================================================================
# test-gateguard-grant.sh — trava a LIBERAÇÃO POR CONFIRMAÇÃO DO USUÁRIO
#                           do GateGuard (hook UserPromptSubmit + gates)
# =============================================================================
#
# Problema medido: o gate libera um comando destrutivo só na segunda tentativa
# IDÊNTICA (mesmo hash). Quando o usuário responde "tem permissão, pode rodar",
# o agente reformula o comando (novo hash → novo bloqueio) ou o estado de 30
# min já expirou — e a autorização do usuário vira mais um round-trip.
#
# Este teste cobre três camadas, todas sem rede, sem API, sem banco:
#   1. classify_prompt(): o que conta (PT/EN, afirmativa curta, revogação,
#      sessão) e o que NUNCA conta (negação, afirmativo perdido em mensagem
#      longa, menções ao gateguard em prosa)
#   2. apply_prompt_to_state(): ciclo de vida do grant (turno, sessão, TTL)
#   3. o hook de ponta a ponta via stdin: comando REFORMULADO passa com grant,
#      volta a ser barrado depois de um prompt comum
#
# USO:  ./tests/test-gateguard-grant.sh
# =============================================================================

set -uo pipefail

HOOK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/hooks/gateguard.py"

if [[ ! -f "$HOOK" ]]; then
    echo "FALHA: hook nao encontrado em $HOOK"
    exit 1
fi

STATE_DIR="$(mktemp -d)"
trap 'rm -rf "$STATE_DIR"' EXIT

GATEGUARD_HOOK="$HOOK" OSFORGE_GATEGUARD_STATE_DIR="$STATE_DIR" python3 - <<'PY'
import importlib.util
import json
import os
import subprocess
import sys
import time

HOOK = os.environ["GATEGUARD_HOOK"]
spec = importlib.util.spec_from_file_location("gg", HOOK)
gg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gg)

falhas = []
total = 0

def check(nome, obtido, esperado):
    global total
    total += 1
    ok = obtido == esperado
    if not ok:
        falhas.append((nome, esperado, obtido))
    print("  {}  {:<62} esperado={!s:<8} obtido={!s}".format(
        "ok  " if ok else "FALHA", nome[:62], esperado, obtido))

# ── 1. classify_prompt ───────────────────────────────────────────────────────
print("\n[1] classify_prompt")
CASOS = [
    # autorizações explícitas em português
    ("PT1 'você tem permissão'", "Você tem permissão para apagar a tabela.", "grant"),
    ("PT2 'tem permissão, pode rodar'", "tem permissão, pode rodar", "grant"),
    ("PT3 'autorizo'", "Autorizo a execução do drop.", "grant"),
    ("PT4 'pode executar' sozinho", "pode executar", "grant"),
    ("PT5 'pode apagar' no meio da frase", "isso mesmo, pode apagar a pasta build", "grant"),
    ("PT6 negação em OUTRA oração não anula", "Não precisa pedir, pode executar.", "grant"),
    ("PT7 'está autorizado'", "está autorizado, segue", "grant"),
    ("PT8 'vai em frente'", "vai em frente", "grant"),
    ("PT9 'no' = 'em o', não é negação", "rode no servidor de staging, pode executar", "grant"),
    # afirmativas curtas (mensagem inteira)
    ("SH1 'sim'", "sim", "grant"),
    ("SH2 'Sim, pode.'", "Sim, pode.", "grant"),
    ("SH3 'ok'", "ok", "grant"),
    ("SH4 'vai'", "vai", "grant"),
    ("SH5 'pode sim, por favor'", "pode sim, por favor", "grant"),
    ("SH6 'yes'", "yes", "grant"),
    ("SH7 'go ahead'", "go ahead", "grant"),
    ("SH8 'do it'", "do it", "grant"),
    # inglês
    ("EN1 'you have my permission'", "You have my permission.", "grant"),
    ("EN2 'you are authorized'", "you are authorized to drop it", "grant"),
    ("EN3 'I approve'", "I approve, run it", "grant"),
    # NUNCA conta
    ("NEG1 'não tem permissão'", "você não tem permissão para isso", "none"),
    ("NEG2 'não pode apagar'", "não pode apagar nada", "none"),
    ("NEG3 'não te autorizo'", "não te autorizo a rodar isso", "none"),
    ("NEG4 \"don't do it\"", "don't do it", "none"),
    ("NEG5 'do not proceed'", "do not proceed", "none"),
    ("NEG6 'não' sozinho", "não", "none"),
    ("NEG7 'não, espera'", "não, espera", "none"),
    ("NEG8 'you are not authorized'", "you are not authorized", "none"),
    ("NONE1 instrução comum", "ajusta o css do header", "none"),
    ("NONE2 afirmativo perdido em mensagem longa",
     "sim, mas primeiro me explica o que o comando faz", "none"),
    ("NONE3 'pode ser'", "pode ser que o teste falhe", "none"),
    ("NONE4 'pode me mostrar'", "pode me mostrar o diff?", "none"),
    ("NONE5 gateguard em prosa",
     "Quero que o gateguard seja flexível quando eu enviar uma confirmação", "none"),
    ("NONE6 gateguard em prosa 2", "o gateguard continua barrando", "none"),
    ("NONE7 vazio", "", "none"),
    ("NONE8 só espaços", "   \n ", "none"),
    # revogação e sessão
    ("REV1 'revogo a permissão'", "revogo a permissão", "revoke"),
    ("REV2 'gateguard: ativa'", "gateguard: ativa", "revoke"),
    ("REV3 revogação vence autorização no mesmo texto",
     "cancela a permissão que eu tinha dado, você não pode executar", "revoke"),
    ("SES1 'gateguard: sessão liberada'", "gateguard: sessão liberada", "session"),
    ("SES2 'gateguard off'", "gateguard off", "session"),
]
for nome, texto, esperado in CASOS:
    check(nome, gg.classify_prompt(texto), esperado)

# ── 2. apply_prompt_to_state: ciclo de vida ──────────────────────────────────
print("\n[2] ciclo de vida do grant")
st = {"checked": []}
st, v = gg.apply_prompt_to_state(st, "pode executar")
check("grant de turno criado", bool(gg._active_grant(st)), True)
check("scope = turn", st["grant"]["scope"], "turn")
check("TTL respeita GRANT_TTL_S",
      int(st["grant"]["expires_at"] - st["grant"]["granted_at"]), gg.GRANT_TTL_S)

st, v = gg.apply_prompt_to_state(st, "agora ajusta o css")
check("prompt comum encerra grant de turno", gg._active_grant(st), None)

st, v = gg.apply_prompt_to_state(st, "gateguard: sessão liberada")
check("grant de sessão criado", st["grant"]["scope"], "session")
st, v = gg.apply_prompt_to_state(st, "agora ajusta o css")
check("prompt comum NÃO encerra grant de sessão", bool(gg._active_grant(st)), True)
st, v = gg.apply_prompt_to_state(st, "revogo a permissão")
check("revogação encerra grant de sessão", gg._active_grant(st), None)

st, v = gg.apply_prompt_to_state({"checked": []}, "sim")
st["grant"]["expires_at"] = time.time() - 1
check("grant expirado não é ativo", gg._active_grant(st), None)
check("grant corrompido não é ativo", gg._active_grant({"grant": "lixo"}), None)
check("grant sem expires_at não é ativo", gg._active_grant({"grant": {}}), None)

# ── 3. hook de ponta a ponta via stdin ───────────────────────────────────────
print("\n[3] hook via stdin (estado em {})".format(os.environ["OSFORGE_GATEGUARD_STATE_DIR"]))

def hook(payload):
    r = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=20)
    out = r.stdout.strip()
    return (r.returncode, json.loads(out) if out else None)

def bash(cmd, sid="s1"):
    return hook({"session_id": sid, "hook_event_name": "PreToolUse",
                 "tool_name": "Bash", "tool_input": {"command": cmd}})

def prompt(text, sid="s1"):
    return hook({"session_id": sid, "hook_event_name": "UserPromptSubmit",
                 "prompt": text})

def decision(res):
    code, out = res
    if code != 0:
        return "exit{}".format(code)
    if out is None:
        return "allow"
    return (out.get("hookSpecificOutput") or {}).get("permissionDecision", "allow")

# cenário real: bloqueio → usuário confirma → comando REFORMULADO passa
check("E2E1 destrutivo sem grant é negado", decision(bash("rm -rf build/")), "deny")
check("E2E1 negação cita a saída pela confirmação",
      "confirmação explícita" in bash("git clean -fd")[1]["hookSpecificOutput"]["permissionDecisionReason"], True)
code, out = prompt("tem permissão, pode rodar")
check("E2E2 confirmação injeta additionalContext",
      "hookSpecificOutput" in (out or {}) and "liberado" in out["hookSpecificOutput"]["additionalContext"], True)
check("E2E3 comando REFORMULADO passa com grant", decision(bash("rm -rf ./build/ dist/")), "allow")
check("E2E4 segundo destrutivo no mesmo turno também passa",
      decision(bash('psql -c "DROP SCHEMA public CASCADE"')), "allow")
check("E2E5 prompt comum não emite contexto", prompt("agora ajusta o css")[1], None)
check("E2E6 depois do prompt comum, volta a negar", decision(bash("git push --force origin main")), "deny")
check("E2E7 afirmativa curta libera", decision((prompt("sim"), bash("git reset --hard HEAD~3"))[1]), "allow")
check("E2E8 negação NÃO libera", decision((prompt("não pode apagar"), bash("rm -rf node_modules/"))[1]), "deny")
check("E2E9 grant é por sessão: outra sessão continua negada",
      decision((prompt("pode executar", sid="s1"), bash("rm -rf build/", sid="s2"))[1]), "deny")
prompt("gateguard: sessão liberada")
prompt("mais uma tarefa qualquer")
check("E2E10 sessão liberada sobrevive a prompt comum", decision(bash("git clean -fdx")), "allow")
prompt("gateguard: ativa")
check("E2E11 revogação fecha na hora", decision(bash("git clean -fdX")), "deny")
check("E2E12 comando não destrutivo nunca é afetado", decision(bash("ls -la")), "allow")
r = subprocess.run([sys.executable, HOOK],
                   input=json.dumps({"session_id": "s1", "hook_event_name": "PreToolUse",
                                     "tool_name": "Bash", "tool_input": {"command": "rm -rf /tmp/x"}}),
                   capture_output=True, text=True, timeout=20,
                   env={**os.environ, "OSFORGE_GATEGUARD": "off"})
check("E2E13 kill-switch OSFORGE_GATEGUARD=off continua funcionando",
      decision((r.returncode, json.loads(r.stdout) if r.stdout.strip() else None)), "allow")

log = open(os.path.join(os.environ["OSFORGE_GATEGUARD_STATE_DIR"], "denials.log"), encoding="utf-8").read()
check("AUD1 liberações ficam auditáveis em denials.log", "GRANT-ALLOW\trm -rf ./build/ dist/" in log, True)
check("AUD2 a confirmação em si é logada", "GRANT-GRANT\ttem permissão, pode rodar" in log, True)

print()
if falhas:
    print("FALHOU: {} de {} casos".format(len(falhas), total))
    for nome, esperado, obtido in falhas:
        print("  - {}: esperava {!r}, obteve {!r}".format(nome, esperado, obtido))
    sys.exit(1)

print("PASSOU: {}/{} casos".format(total, total))
PY

exit $?
