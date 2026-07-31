# Packaging OSForge as a Claude Code plugin

**Rejected: 2026-07-30** (analysis R10)

Proposed as the distribution mechanism, following mattpocock/skills. Rejected because the problem
it solves — installing skill subsets instead of the whole framework — is already covered:
`skills-core.txt` picks what is global, `install-skill.sh` pulls anything else per project, and
`deploy.sh` owns the sync. A plugin adds a second distribution channel to keep coherent with the
first, for zero new capability while OSForge has a single user.

**Would reopen if:** OSForge is distributed to third parties, where marketplace install and
auto-update change the calculus.
