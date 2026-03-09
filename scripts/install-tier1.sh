#!/bin/bash
# ============================================
# 🚀 Instalador de Skills Tier 1
# Instala as skills essenciais num projeto
# ============================================
# Uso: bash install-tier1.sh /caminho/do/projeto
# Sem argumento: instala no diretório atual

set -e

PROJECT_DIR="${1:-.}"
SKILLS_BASE="$HOME/Development/agent-skills-consolidado"
TARGET="$PROJECT_DIR/.claude/skills"

if [ ! -d "$SKILLS_BASE" ]; then
    echo "❌ Pasta de skills não encontrada em $SKILLS_BASE"
    exit 1
fi

mkdir -p "$TARGET"

echo ""
echo "🎯 Instalando Agent Skills Tier 1 em: $TARGET"
echo "================================================"

echo ""
echo "📦 [1/5] Anthropic (document + design + dev)..."
for skill in frontend-design docx pdf xlsx pptx mcp-builder skill-creator webapp-testing; do
    if [ -d "$SKILLS_BASE/01-anthropic/$skill" ]; then
        cp -R "$SKILLS_BASE/01-anthropic/$skill" "$TARGET/"
        echo "  ✓ $skill"
    fi
done

echo ""
echo "🔵 [2/5] Superpowers (workflow de desenvolvimento)..."
for skill in brainstorming writing-plans executing-plans test-driven-development systematic-debugging subagent-driven-development requesting-code-review receiving-code-review verification-before-completion using-git-worktrees finishing-a-development-branch dispatching-parallel-agents writing-skills; do
    if [ -d "$SKILLS_BASE/02-superpowers/$skill" ]; then
        cp -R "$SKILLS_BASE/02-superpowers/$skill" "$TARGET/"
        echo "  ✓ $skill"
    fi
done

echo ""
echo "🟢 [3/5] Vercel (React / Next.js / Web Design)..."
for skill in react-best-practices web-design-guidelines composition-patterns; do
    if [ -d "$SKILLS_BASE/04-vercel/$skill" ]; then
        cp -R "$SKILLS_BASE/04-vercel/$skill" "$TARGET/"
        echo "  ✓ $skill"
    fi
done

echo ""
echo "🟩 [4/5] Supabase (PostgreSQL best practices)..."
if [ -d "$SKILLS_BASE/08-supabase/supabase-postgres-best-practices" ]; then
    cp -R "$SKILLS_BASE/08-supabase/supabase-postgres-best-practices" "$TARGET/"
    echo "  ✓ supabase-postgres-best-practices"
fi

echo ""
echo "🔒 [5/5] Trail of Bits (segurança)..."
for skill in static-analysis insecure-defaults sharp-edges modern-python audit-context-building; do
    if [ -d "$SKILLS_BASE/07-trailofbits/$skill" ]; then
        cp -R "$SKILLS_BASE/07-trailofbits/$skill" "$TARGET/"
        echo "  ✓ $skill"
    fi
done

echo ""
echo "================================================"
TOTAL=$(find "$TARGET" -name "SKILL.md" | wc -l | tr -d ' ')
echo "✅ Instalação concluída! $TOTAL skills instaladas em $TARGET"
echo ""
echo "💡 Para instalar claude-mem (memória persistente), execute no Claude Code:"
echo "   /plugin marketplace add thedotmack/claude-mem"
echo "   /plugin install claude-mem"
echo ""
