#!/bin/bash
# Cursor Hooks Dashboard — Monitor de atividade
# Uso: ./hooks-dashboard.sh [watch]
# Com 'watch': atualiza automaticamente a cada 5s

LOG=/tmp/cursor-hooks.log
CLEAR="\033[H\033[2J"

show_dashboard() {
  echo "========================================="
  echo "  🪝 CURSOR HOOKS DASHBOARD"
  echo "  $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================="
  echo ""

  if [ ! -f "$LOG" ]; then
    echo "  📭 Nenhuma atividade registrada ainda."
    echo "  O log será criado em $LOG quando os hooks forem acionados."
    return
  fi

  # Contadores
  total=$(wc -l < "$LOG" 2>/dev/null | tr -d ' ')
  test_edits=$(grep -c 'HOOK WARNING.*Test file' "$LOG" 2>/dev/null || echo 0)
  completions=$(grep -c '"completed"' "$LOG" 2>/dev/null || echo 0)
  errors=$(grep -c '"error"' "$LOG" 2>/dev/null || echo 0)
  aborted=$(grep -c '"aborted"' "$LOG" 2>/dev/null || echo 0)

  echo "  📊 RESUMO"
  echo "  ─────────────────────────────────"
  echo "  Total de eventos:        $total"
  echo "  ⚠️  Test files editados:  $test_edits"
  echo "  ✅ Tasks completadas:    $completions"
  echo "  ❌ Tasks com erro:       $errors"
  echo "  🛑 Tasks abortadas:      $aborted"
  echo ""

  # Alertas de segurança
  if [ "$test_edits" -gt 0 ]; then
    echo "  🚨 ALERTAS — Arquivos de teste modificados:"
    echo "  ─────────────────────────────────"
    grep 'HOOK WARNING' "$LOG" | tail -5 | while read -r line; do
      echo "  $line"
    done
    echo ""
  fi

  # Últimos 10 eventos
  echo "  📋 ÚLTIMOS EVENTOS"
  echo "  ─────────────────────────────────"
  tail -10 "$LOG" | while read -r line; do
    echo "  $line"
  done
  echo ""
  echo "  Log: $LOG"
  echo "  Tamanho: $(du -h "$LOG" 2>/dev/null | cut -f1)"
}

# Modo watch ou single run
if [ "$1" = "watch" ]; then
  while true; do
    printf "$CLEAR"
    show_dashboard
    echo ""
    echo "  [Ctrl+C para sair — atualiza a cada 5s]"
    sleep 5
  done
else
  show_dashboard
fi
