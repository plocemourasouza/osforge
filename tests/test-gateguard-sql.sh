#!/usr/bin/env bash
# =============================================================================
# test-gateguard-sql.sh — trava os falsos positivos e negativos MEDIDOS do
#                         detector de SQL destrutivo do GateGuard
# =============================================================================
#
# Cada caso aqui foi observado de verdade contra a funcao real, nao imaginado.
# Os seis "passa" eram bloqueios que aconteceram numa unica sessao de trabalho e
# custaram round-trips; os cinco "BLOQ" da familia FN executaram DDL destrutivo
# sem gate nenhum, incluindo um `ALTER TABLE ... DROP CONSTRAINT` por
# `docker exec ... psql` com heredoc.
#
# A regra que separa os dois grupos: verbo destrutivo NAO e sinal por si so.
# O sinal e verbo destrutivo DENTRO de uma invocacao de cliente de banco.
#
# USO:  ./tests/test-gateguard-sql.sh
# Roda em milissegundos, sem rede, sem API, sem banco.
# =============================================================================

set -uo pipefail

HOOK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/hooks/gateguard.py"

if [[ ! -f "$HOOK" ]]; then
    echo "FALHA: hook nao encontrado em $HOOK"
    exit 1
fi

GATEGUARD_HOOK="$HOOK" python3 - <<'PY'
import importlib.util
import os
import sys

spec = importlib.util.spec_from_file_location("gg", os.environ["GATEGUARD_HOOK"])
gg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gg)

# (nome, comando, deve_bloquear)
CASOS = [
    # ── Falsos positivos medidos: verbo em prosa ou em busca de texto ─────────
    ("FP1 componente com 'Drop' no nome",
     'grep -rn "DropdownMenu" src/', False),
    ("FP2 buscar o verbo dentro das migracoes",
     'grep -rn "DROP TABLE" prisma/migrations/', False),
    ("FP3 documentar o comando num arquivo",
     'echo "rode DROP TABLE trilhas_fake;" >> PROGRESS.md', False),
    ("FP4 classe utilitaria truncate do Tailwind",
     'grep -rn "truncate" src/components/', False),
    ("FP5 prosa contendo 'delete from'",
     'echo "we delete from the list when the user opts out"', False),
    ("FP6 arquivo cujo nome contem o verbo",
     'cat src/utils/truncate-text.ts', False),
    ("FP7 migrate de rotina, sem verbo destrutivo",
     'bunx prisma migrate deploy', False),
    ("FP8 psql de leitura",
     'psql -U mira -d mira_manager -c "select count(*) from users"', False),

    # ── Falsos negativos medidos: DDL destrutivo que executou sem gate ────────
    ("FN1 alter/drop constraint por docker exec psql com heredoc",
     'docker exec -i mira-manager-db psql -U mira <<SQL\n'
     'ALTER TABLE startups DROP CONSTRAINT startups_pkey;\nSQL', True),
    ("FN2 drop schema cascade",
     'psql -c "DROP SCHEMA public CASCADE"', True),
    ("FN3 drop role",
     'psql -c "DROP ROLE mira_app"', True),
    ("FN4 drop column",
     'psql -c "ALTER TABLE startups DROP COLUMN cnpj"', True),
    ("FN5 drop index",
     'psql -c "DROP INDEX idx_startups_org"', True),
    ("FN6 drop de coluna na forma implicita do Postgres (sem COLUMN)",
     'psql -c "ALTER TABLE startups DROP cnpj"', True),
    ("FN7 sql destrutivo via prisma db execute",
     'bunx prisma db execute --stdin <<SQL\nDROP TABLE trilhas_fake;\nSQL', True),
    ("FN8 reset do banco inteiro, sem nenhum verbo SQL no comando",
     'bunx prisma migrate reset --force', True),
    ("FN9 reset pelo script do package.json",
     'bun run db:reset', True),

    # ── Verdadeiros positivos que ja funcionavam: nao podem regredir ──────────
    ("TP1 drop table por psql", 'psql -c "DROP TABLE trilhas_fake;"', True),
    ("TP2 truncate por psql", 'psql -c "TRUNCATE TABLE users"', True),
    ("TP3 delete from por mysql", 'mysql -e "DELETE FROM users"', True),

    # ── Outros tiers do guard: guarda de regressao cruzada ───────────────────
    ("TP4 rm -rf continua bloqueado", 'rm -rf build/', True),
    ("TP5 push --force continua bloqueado", 'git push --force origin main', True),
    ("TP6 reset --hard continua bloqueado", 'git reset --hard HEAD~3', True),
]

falhas = []
for nome, cmd, esperado in CASOS:
    obtido = gg.is_destructive_bash(cmd)
    marca = "ok  " if obtido == esperado else "FALHA"
    if obtido != esperado:
        falhas.append((nome, esperado, obtido))
    print("  {}  {:<58} esperado={:<5} obtido={}".format(
        marca, nome, "BLOQ" if esperado else "passa",
        "BLOQ" if obtido else "passa"))

print()
if falhas:
    print("FALHOU: {} de {} casos".format(len(falhas), len(CASOS)))
    for nome, esperado, obtido in falhas:
        print("  - {}: esperava {}, obteve {}".format(
            nome, "BLOQ" if esperado else "passa",
            "BLOQ" if obtido else "passa"))
    sys.exit(1)

print("PASSOU: {}/{} casos".format(len(CASOS), len(CASOS)))
PY

exit $?
