# Importing ECC's catalog, learning loop, eval harness and installer machinery

**Rejected: 2026-09-18** (docs/ANALISE-COMPARATIVA-ECC.md §5.5, ADR-015)

The comparative audit of `affaan-m/ECC` (dd6ee538) found five mechanisms worth adapting (hook
contract tests, state-aware deploy with id-keyed hook merge, guarded session resume with a stable
project identity, deterministic canvas-feedback drain, real-usage context threshold). Everything
else was rejected, each for a verified reason, not for taste:

- **The catalog** (292 skills, 94 commands, per-language rules): ADR-012 already routes library
  facts to Context7; 23% of the catalog is not engineering; every description costs context in
  every session. Semantic equivalents for the disciplines that matter already exist here (§4.3).
- **The learning loop** (observer daemon, `pending/` queue, `evolved/` output): the observer ships
  disabled, confidence math exists only in docs, generated output is never loaded, and no benefit
  was ever measured. Our own loop has the same dead end (no writer for `instincts`) and is parked
  behind experiment E5 rather than completed on faith.
- **`claude -p` inside hooks** (Stop, PreCompact): unrequested cost and transcript egress; it was
  also what caused the one paid call during the audit.
- **`eval-harness`**: candidate execution is disabled by code (`gate.js:175-177`). Receipts and
  fixture replay are not behavioural evals.
- **`harness-audit`**: presence-only scoring; a tree of 3103 empty files scores 76/80.
- **`skill-comply` as shipped**: LLM-generated spec and LLM classifier grading LLM behaviour; the
  runner does not even allow the Skill tool. Only its prompt-strictness ladder (supportive /
  neutral / competing) is kept as an experimental design.
- **State store in `sql.js`, skill versions/amendments/provenance**: five of seven tables have no
  writer; git already versions skills.
- **Module/component/profile manifests, 15 harness adapters, hook consent gate, settings lock
  with quarantine, 33-cell CI matrix, coverage gate, embedded IOC list**: they serve distribution
  to third parties, which `.out-of-scope/claude-code-plugin-packaging.md` already rejects.
- **tmux worktree orchestrator**: the Agent tool already fans out; ECC's ignores dependencies and
  has no merge step. Worktree isolation for write-waves is deferred (R-15), not the orchestrator.
- **`santa-method`, `council`, `blueprint`, `search-first` as skills**: covered by
  `adversarial-review`, two-stage review, `elicitation-engine`, `grilling`, `PLAN.template.md` and
  ADR-012.

**Would reopen if:** OSForge is distributed to third parties (installer/adapters), or a paired
experiment (§8 of the report) shows a measured gain for a specific rejected mechanism.
