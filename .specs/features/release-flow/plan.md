# Release flow from main

**Objective.** Deploys come from a released, tagged `main`, not from whatever branch the clone is on.
Approved 2026-10-19 (option "release from main").

## User stories
- US-01 — As the maintainer, merging a VERSION bump to `main` creates tag `v<VERSION>` and a GitHub
  Release whose body is that version's CHANGELOG section. AC: no tag when VERSION is unchanged or the
  tag already exists; no release when CI failed.
- US-02 — `./deploy.sh` refuses to deploy from a non-`main` branch, a dirty tree, or a HEAD that is not
  at a `v*` tag, unless `--force-branch`. AC: refusal names the reason and the flag; `--dry-run` reports
  the guard without aborting; banner shows branch + version; install-state records them.
- US-03 — `./deploy.sh --release` fetches tags and deploys the latest `v*` tag from a detached worktree
  in `~/.osforge/release/`, whatever branch the clone is on. `--doctor` shows installed vs latest tag.
- US-04 — `scripts/release.sh <x.y.z>` bumps VERSION, turns `[Unreleased]` into `[x.y.z] — <date>`,
  commits on `release/<x.y.z>` and opens the PR (`--no-pr` skips gh).

## Tasks (one wave, one agent — all touch deploy.sh / test-deploy-lifecycle.sh)
- T-1 `scripts/release.sh` + `.github/workflows/release.yml` (US-01, US-04)
- T-2 deploy guard + `--force-branch` + banner/state (US-02)
- T-3 `--release` + doctor line (US-03)
- T-4 tests in `tests/test-deploy-lifecycle.sh` (local bare remote, no network), ADR-018, USAGE, root
  CLAUDE.md commands + counts, CHANGELOG [Unreleased]

## Verify
`tests/test-deploy-lifecycle.sh`, `tests/hooks/run-contracts.sh`, all static gates, `bash -n`,
`check-portability.py` (bash 3.2: no mapfile, no `${x,,}`), CI green on the PR.

## Risks & rollback
Guard can block an emergency deploy → `--force-branch`. Release workflow only creates tags → delete tag
+ release to undo. Test suite must keep working in CI, where checkout is a detached PR merge ref
(tests must use `--force-branch` or their own repos).
