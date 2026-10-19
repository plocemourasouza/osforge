#!/usr/bin/env bash
# release.sh — prepare a release PR (ADR-018). Does NOT tag: the tag and the GitHub Release
# are created by .github/workflows/release.yml once the VERSION bump is on main and CI is green.
#
# Usage: scripts/release.sh <x.y.z> [--no-pr]
#   1. requires a clean tree on an up-to-date main, and x.y.z > the current VERSION
#   2. bumps VERSION, turns `## [Unreleased]` into `## [x.y.z] — <date>` (fresh empty
#      `## [Unreleased]` above it)
#   3. commits on branch release/x.y.z and opens a PR (skipped with --no-pr)
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
NEW=""; OPEN_PR=true
for arg in "$@"; do
  case $arg in
    --no-pr) OPEN_PR=false ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown flag: $arg" >&2; exit 1 ;;
    *) [ -z "$NEW" ] || { echo "only one version allowed" >&2; exit 1; }; NEW="$arg" ;;
  esac
done
[ -n "$NEW" ] || { echo "usage: scripts/release.sh <x.y.z> [--no-pr]" >&2; exit 1; }
die() { echo "❌ $1" >&2; exit 1; }

printf '%s' "$NEW" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' || die "'$NEW' is not MAJOR.MINOR.PATCH"
CUR="$(tr -d '[:space:]' < "$REPO/VERSION")"
python3 - "$CUR" "$NEW" <<'PYEOF' || die "$NEW is not greater than the current VERSION $CUR"
import sys
v = lambda s: tuple(int(x) for x in s.split("."))
sys.exit(0 if v(sys.argv[2]) > v(sys.argv[1]) else 1)
PYEOF

cd "$REPO"
[ "$(git symbolic-ref --short -q HEAD || true)" = "main" ] || die "not on main — releases are cut from main"
[ -z "$(git status --porcelain)" ] || die "working tree is not clean"
git fetch -q origin main || die "git fetch origin main failed (offline?)"
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || die "local main is not up to date with origin/main (pull or push first)"
git rev-parse -q --verify "refs/tags/v$NEW" >/dev/null && die "tag v$NEW already exists"
git rev-parse -q --verify "refs/heads/release/$NEW" >/dev/null && die "branch release/$NEW already exists"
grep -q '^## \[Unreleased\]' CHANGELOG.md || die "CHANGELOG.md has no '## [Unreleased]' section"

DATE="$(date +%Y-%m-%d)"
python3 - "$NEW" "$DATE" <<'PYEOF'
import re, sys
new, date = sys.argv[1:3]
text = open("CHANGELOG.md", encoding="utf-8").read()
text, n = re.subn(r"^## \[Unreleased\][ \t]*$", f"## [Unreleased]\n\n## [{new}] — {date}", text, count=1, flags=re.M)
if n != 1:
    sys.exit("CHANGELOG.md: '## [Unreleased]' heading not found on a line of its own")
open("CHANGELOG.md", "w", encoding="utf-8").write(text)
PYEOF
printf '%s\n' "$NEW" > VERSION

git checkout -q -b "release/$NEW"
git add VERSION CHANGELOG.md
git commit -q -m "chore(release): v$NEW

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
echo "✅ release/$NEW committed (VERSION $CUR → $NEW, CHANGELOG dated $DATE)"

if $OPEN_PR; then
  command -v gh >/dev/null 2>&1 || die "gh not found — push release/$NEW and open the PR by hand, or re-run with --no-pr"
  git push -q -u origin "release/$NEW"
  gh pr create --base main --head "release/$NEW" --title "chore(release): v$NEW" \
    --body "Release v$NEW. Merging this to main makes \`.github/workflows/release.yml\` tag v$NEW and publish the GitHub Release once CI is green."
else
  echo "   --no-pr: push with  git push -u origin release/$NEW  and open the PR yourself"
fi
