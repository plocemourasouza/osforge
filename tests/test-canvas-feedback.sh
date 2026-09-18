#!/usr/bin/env bash
# tests/test-canvas-feedback.sh — B-020: dreno do feedback do Canvas (Stop hook) + validação no servidor.
#
# Parte A (sem Bun): hooks/canvas-feedback.py contra um data dir semeado e um servidor de
# health falso em Python. Verifica por execução:
#   1. feedback pendente do projeto atual → Stop bloqueia UMA vez com o conteúdo (sem segredos)
#   2. segundo Stop → passa (entregue); novo envio → bloqueia de novo
#   3. feedback de outro projeto → nunca aparece
#   4. stop_hook_active → passa mesmo com pendência (nunca em laço)
#   5. servidor fora do ar → passa; kill-switch → passa; payload inválido → exit 0
#   6. feedback de revisão antiga → entregue com marca DESATUALIZADO
# Parte B (com Bun; pulada se ausente): scripts/canvas/server.ts real em porta aleatória:
#   7. artefato inexistente → 404 · revision divergente → 409 · action fora do enum → 400
#      · bloco/item desconhecido → 400 · Origin não-loopback → 403 · Origin loopback → 200
#      · válido → 200 com receivedAt · hook real contra o servidor real → bloqueia
# Offline. Uso: tests/test-canvas-feedback.sh
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"; trap 'kill $(jobs -p) 2>/dev/null; rm -rf "$WORK"' EXIT
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  ✅ $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  ❌ $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
section(){ echo ""; echo "── $1"; }

export HOME="$WORK/home"; mkdir -p "$HOME"
export OSFORGE_DB="$WORK/db.sqlite" OSFORGE_LOG_DIR="$WORK/logs"
unset OSFORGE_PROJECT OSFORGE_CANVAS_FEEDBACK
HOOK="$REPO/hooks/canvas-feedback.py"
GIT="git -c user.name=t -c user.email=t@t -c init.defaultBranch=main -c commit.gpgsign=false"
DATA="$WORK/canvas"; mkdir -p "$DATA/artifacts" "$DATA/feedback"
PROJ="$WORK/proj"; mkdir -p "$PROJ" && (cd "$PROJ" && $GIT init -q && echo x > f && $GIT add f && $GIT commit -qm i)
python3 "$REPO/scripts/osforge-db.py" upsert-project alpha "a" standard active --root="$PROJ" >/dev/null 2>&1

artifact(){ # artifact <id> <rev>
  cat > "$DATA/artifacts/$1.json" <<EOF
{"\$schema":"osforge-canvas/v1","id":"$1","title":"Plano $1","accent":"teal","createdAt":"2026-09-18T00:00:00Z","revision":$2,
 "blocks":[{"type":"heading","id":"h","level":2,"text":"H"},
           {"type":"checklist","id":"acs","title":"ACs","items":[{"id":"a1","text":"cobertura 80%"},{"id":"a2","text":"zero downtime"}]},
           {"type":"form","id":"params","fields":[{"id":"strategy","kind":"select","options":["canary","big-bang"]}]},
           {"type":"decision","id":"go","prompt":"Aprovar?","options":["approve","edit","reject"],"commentRequiredFor":["reject"]}]}
EOF
}
feedback(){ # feedback <id> <rev> <submittedAt> [comment]
  local extra=""; [ -n "${4:-}" ] && extra=",\"comment\":\"$4\""
  cat > "$DATA/feedback/$1.json" <<EOF
{"artifactId":"$1","revision":$2,"submittedAt":"$3","responses":{"acs":{"type":"checklist","checked":["a1"]},
 "params":{"type":"form","values":{"strategy":"canary"}},"go":{"type":"decision","action":"edit","comment":"rotacionar o refresh token"}}$extra}
EOF
}
run_hook(){ # run_hook <payload-json> → $OUT $RC
  OUT="$(cd "$PROJ" && printf '%s' "$1" | python3 "$HOOK" 2>/dev/null)"; RC=$?
}
reason(){ python3 -c "import json,sys; d=json.loads(sys.argv[1]); assert d['decision']=='block'; print(d['reason'])" "$1" 2>/dev/null; }

section "Parte A — hook com servidor de health falso"
python3 - "$DATA" "$WORK/port" <<'EOF' &
import json, sys, http.server, socketserver
data, portfile = sys.argv[1:3]
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"ok": True, "service": "osforge-canvas", "version": 1, "dir": data}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass
with socketserver.TCPServer(("127.0.0.1", 0), H) as s:
    open(portfile, "w").write(str(s.server_address[1])); s.serve_forever()
EOF
for _ in $(seq 40); do [ -s "$WORK/port" ] && break; sleep 0.1; done
export OSFORGE_CANVAS_HEALTH_URL="http://127.0.0.1:$(cat "$WORK/port")/api/health"

artifact alpha-plan 2; artifact other-plan 1
feedback alpha-plan 2 "2026-09-18T10:00:00Z" "token sk-ant-api03-SEGREDOCANVAS12345678 no comentário"
feedback other-plan 1 "2026-09-18T10:00:00Z"
run_hook '{"session_id":"s","stop_hook_active":false}'
R="$(reason "$OUT")"
check "feedback pendente → Stop bloqueia" '[ $RC -eq 0 ] && [ -n "$R" ]'
check "conteúdo: decisão, checklist, form e comentário" 'grep -q "decisão \`go\`: \*\*edit\*\* — rotacionar" <<<"$R" && grep -q "checklist \`acs\`: 1/2 marcados: cobertura 80%" <<<"$R" && grep -q "strategy=canary" <<<"$R"'
check "título e revisão do artefato" 'grep -q "Plano alpha-plan (\`alpha-plan\`, rev 2)" <<<"$R"'
check "segredo do comentário limpo" '! grep -q "SEGREDOCANVAS" <<<"$R" && grep -q "redacted:key" <<<"$R"'
check "feedback de OUTRO projeto não aparece" '! grep -q "other-plan" <<<"$R"'
check "estado de entrega gravado" 'grep -q "alpha-plan" "$DATA/.delivered.json"'
run_hook '{"stop_hook_active":false}'
check "segundo Stop → passa (já entregue)" '[ $RC -eq 0 ] && [ -z "$OUT" ]'
feedback alpha-plan 2 "2026-09-18T11:00:00Z"
run_hook '{"stop_hook_active":false}'
check "novo envio (submittedAt novo) → bloqueia de novo" '[ -n "$(reason "$OUT")" ]'
feedback alpha-plan 2 "2026-09-18T12:00:00Z"
run_hook '{"stop_hook_active":true}'
check "stop_hook_active → passa mesmo com pendência" '[ $RC -eq 0 ] && [ -z "$OUT" ]'
run_hook '{"stop_hook_active":false}'; check "…e a pendência continua lá para o próximo Stop normal" '[ -n "$(reason "$OUT")" ]'
artifact alpha-plan 3; feedback alpha-plan 2 "2026-09-18T13:00:00Z"
run_hook '{}'
check "feedback de revisão antiga → entregue com DESATUALIZADO" 'reason "$OUT" | grep -q "rev 2, DESATUALIZADO"'
feedback alpha-plan 3 "2026-09-18T14:00:00Z"
OUT="$(cd "$PROJ" && echo '{}' | OSFORGE_CANVAS_HEALTH_URL="http://127.0.0.1:1/api/health" python3 "$HOOK" 2>/dev/null)"; RC=$?
check "servidor fora do ar → passa, exit 0" '[ $RC -eq 0 ] && [ -z "$OUT" ]'
OUT="$(cd "$PROJ" && echo '{}' | OSFORGE_CANVAS_FEEDBACK=off python3 "$HOOK" 2>/dev/null)"; RC=$?
check "kill-switch → passa" '[ $RC -eq 0 ] && [ -z "$OUT" ]'
run_hook 'not json'; check "payload inválido → exit 0 (e ainda entrega: fail-open)" '[ $RC -eq 0 ] && [ -n "$(reason "$OUT")" ]'
feedback alpha-plan 3 "2026-09-18T14:30:00Z"
run_hook '[1,2]'; check "payload não-objeto → exit 0 (e ainda entrega)" '[ $RC -eq 0 ] && [ -n "$(reason "$OUT")" ]'
OUT="$(cd "$WORK" && echo '{}' | python3 "$HOOK" 2>/dev/null)"; RC=$?
check "cwd sem projeto → passa" '[ $RC -eq 0 ] && [ -z "$OUT" ]'
check "hook não escreveu em /tmp" '[ -z "$(find /tmp -maxdepth 1 -newer "$HOOK" -name "*canvas*" 2>/dev/null)" ]'
kill %1 2>/dev/null; unset OSFORGE_CANVAS_HEALTH_URL

section "Parte B — servidor real (Bun)"
if ! command -v bun >/dev/null 2>&1; then
  echo "  ⟳  bun ausente — validação do servidor não testada aqui (roda onde o Canvas roda)"
else
  DATA2="$WORK/canvas2"; mkdir -p "$DATA2/artifacts" "$DATA2/feedback"
  PORT="$(python3 -c "import socket; s=socket.socket(); s.bind(('127.0.0.1',0)); print(s.getsockname()[1])")"
  CANVAS_PORT="$PORT" bun "$REPO/scripts/canvas/server.ts" --dir="$DATA2" >"$WORK/server.log" 2>&1 &
  for _ in $(seq 50); do curl -sf "http://127.0.0.1:$PORT/api/health" >/dev/null 2>&1 && break; sleep 0.1; done
  check "servidor no ar" 'curl -sf "http://127.0.0.1:$PORT/api/health" | grep -q "\"dir\""'
  DATA="$DATA2"; artifact alpha-plan 2
  post(){ # post <id> <json> [extra curl args...] → status code
    local id="$1" body="$2"; shift 2
    curl -s -o "$WORK/resp" -w '%{http_code}' -X POST "http://127.0.0.1:$PORT/api/feedback/$id" -H 'Content-Type: application/json' "$@" --data "$body"
  }
  VALID='{"artifactId":"alpha-plan","revision":2,"submittedAt":"2026-09-18T15:00:00Z","responses":{"acs":{"type":"checklist","checked":["a1"]},"go":{"type":"decision","action":"approve"}},"comment":"ok"}'
  check "artefato inexistente → 404" '[ "$(post ghost "${VALID//alpha-plan/ghost}")" = 404 ]'
  check "revision divergente → 409" '[ "$(post alpha-plan "${VALID//\"revision\":2/\"revision\":1}")" = 409 ] && grep -q "revision mismatch" "$WORK/resp"'
  check "revision negativa → 400" '[ "$(post alpha-plan "${VALID//\"revision\":2/\"revision\":-7}")" = 400 ]'
  check "action fora do enum → 400" '[ "$(post alpha-plan "${VALID//approve/launch-missiles}")" = 400 ] && grep -q "approve|edit|reject" "$WORK/resp"'
  check "bloco desconhecido → 400" '[ "$(post alpha-plan "${VALID//\"go\"/\"nope\"}")" = 400 ] && grep -q "no such block" "$WORK/resp"'
  check "item de checklist desconhecido → 400" '[ "$(post alpha-plan "${VALID//\"a1\"/\"zz\"}")" = 400 ]'
  check "tipo de resposta ≠ tipo do bloco → 400" '[ "$(post alpha-plan "${VALID//\"type\":\"checklist\"/\"type\":\"form\"}")" = 400 ]'
  check "reject sem comentário (commentRequiredFor) → 400" '[ "$(post alpha-plan "${VALID//\"action\":\"approve\"/\"action\":\"reject\"}")" = 400 ]'
  check "Origin não-loopback → 403" '[ "$(post alpha-plan "$VALID" -H "Origin: https://evil.example")" = 403 ]'
  check "Origin null → 403" '[ "$(post alpha-plan "$VALID" -H "Origin: null")" = 403 ]'
  check "Origin loopback de outra porta → 403" '[ "$(post alpha-plan "$VALID" -H "Origin: http://127.0.0.1:1")" = 403 ]'
  check "Origin do próprio servidor → 200" '[ "$(post alpha-plan "$VALID" -H "Origin: http://localhost:$PORT")" = 200 ]'
  check "válido sem Origin (curl) → 200 e receivedAt gravado" '[ "$(post alpha-plan "$VALID")" = 200 ] && grep -q "receivedAt" "$DATA2/feedback/alpha-plan.json"'
  check "nada gravado para os rejeitados" '[ ! -e "$DATA2/feedback/ghost.json" ]'
  OUT="$(cd "$PROJ" && echo '{}' | CANVAS_PORT="$PORT" python3 "$HOOK" 2>/dev/null)"; RC=$?
  check "hook real contra servidor real → bloqueia com o feedback" '[ $RC -eq 0 ] && reason "$OUT" | grep -q "decisão \`go\`: \*\*approve\*\*"'
  OUT="$(cd "$PROJ" && echo '{}' | CANVAS_PORT="$PORT" python3 "$HOOK" 2>/dev/null)"
  check "…e passa no Stop seguinte" '[ -z "$OUT" ]'
fi

echo ""; echo "══ canvas-feedback: $PASS ok, $FAIL falha(s)"
[ "$FAIL" -eq 0 ]
