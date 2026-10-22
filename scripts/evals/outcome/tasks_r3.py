"""tasks_r3.py -- round-3 task table of the outcome eval (loaded by driver.py --round r3).

Measures P-01, P-02 and P-03 of the Ponytail intake before adoption (docs/intake/ponytail/
MEDICAO-r3.md). Same layout as r2, under r3/: tasks/<target>/<task>.md (prompt),
tasks/<target>/<task>.truth.md (ground truth, appended to the judge rubric), rubrics/<task>.md,
rubrics/<EXTRA_RUBRIC[target]>, schemas/<target>.json, variants/<target>.<arm>.md (built by
build_variants.py --round r3).

One r3-only addition: TASK_DIRS lets a target reuse another target's task files. `ponytail-ref`
grades the very same cg1-cg6 prompts and truths as `coding-guidelines` (MEDICAO-r3: "reusa as
tarefas cg1-cg6"), so they are read from tasks/coding-guidelines/ instead of being copied.

`ponytail-ref` is OPTIONAL (decision D-P1 is still open): run it or leave it out with
`driver.py --skip ponytail-ref` (or `--only` with the other four). With --runs 3:
  coding-guidelines + code-review + repo-audit  13 tasks x 3 arms x 3 = 117 exec + 117 judge = 234
  mapa-repo                                      3 tasks x 3 arms x 3 =  27 exec +  27 judge =  54
  ponytail-ref (optional)                        6 tasks x 3 arms x 3 =  54 exec +  54 judge = 108
  total 396 calls (288 without ponytail-ref).
"""

_CG = {
    "cg1": {"criteria": ["reuses_house_input", "no_new_dependency", "native_date_input", "range_on_client",
                         "server_validates_date", "uses_day_helper", "proportionate"],
            "critical": ["reuses_house_input", "no_new_dependency"]},
    "cg2": {"criteria": ["uses_platform_id", "no_new_dependency", "readable_alphabet", "unique_enforced",
                         "collision_handled", "existing_rows", "proportionate"],
            "critical": ["uses_platform_id", "no_new_dependency"]},
    "cg3": {"criteria": ["reuses_existing_helper", "all_prices_formatted", "no_new_formatter", "surgical",
                         "proportionate"],
            "critical": ["reuses_existing_helper"]},
    "cg4": {"criteria": ["keeps_signature_check", "validates_at_boundary", "uses_installed_zod",
                         "no_new_dependency", "amount_checked", "unknown_events_acked", "proportionate"],
            "critical": ["keeps_signature_check", "validates_at_boundary"]},
    "cg5": {"criteria": ["fix_in_shared_helper", "handles_local_workaround", "all_callers_checked",
                         "regression_test", "no_scope_creep"],
            "critical": ["fix_in_shared_helper", "handles_local_workaround"]},
    "cg6": {"criteria": ["keeps_accessibility", "no_behavior_lost", "removes_unused_props", "native_element",
                         "callers_ok", "proportionate"],
            "critical": ["keeps_accessibility", "no_behavior_lost"]},
}

TASKS = {
    "coding-guidelines": dict(_CG),
    "code-review": {
        "cr1": {"criteria": ["found_outside_diff", "explains_failure_mode", "rollout_noted", "verdict_right",
                             "actionable", "no_manufactured_high"],
                "critical": ["found_outside_diff", "no_manufactured_high"], "seeded": 1},
        "cr2": {"criteria": ["found_race_under_load", "fix_atomic", "reservation_atomic", "severity_right",
                             "actionable", "no_manufactured_high"],
                "critical": ["found_race_under_load"], "seeded": 1},
        "cr3": {"criteria": ["found_real_bug", "fix_right", "shortcut_not_blocking", "verdict_right", "actionable",
                             "no_manufactured_high"],
                "critical": ["found_real_bug", "shortcut_not_blocking"], "seeded": 1},
        "cr4": {"criteria": ["approves", "no_manufactured_high", "low_noise", "shows_work"],
                "critical": ["no_manufactured_high", "approves"], "seeded": 0},
    },
    "repo-audit": {
        "ra1": {"criteria": ["found_service_role", "found_rls", "key_rotation", "todo_not_high", "ranked_right",
                             "actionable", "no_manufactured_high"],
                "critical": ["found_service_role", "found_rls", "no_manufactured_high"], "seeded": 2},
        "ra2": {"criteria": ["found_race", "found_float_money", "found_unbounded_query", "ranked_right",
                             "actionable", "no_manufactured_high"],
                "critical": ["found_race", "found_float_money", "ranked_right"], "seeded": 3},
        "ra3": {"criteria": ["no_manufactured_high", "clear_verdict", "shortcut_not_high", "low_noise",
                             "shows_work"],
                "critical": ["no_manufactured_high"], "seeded": 0},
    },
    # Map variants: the helper file (components/ui/input.tsx, lib/format.ts, lib/money.ts) is NOT in
    # the prompt; arm C carries the repository exports map (ponytail-map.js format) in the system prompt.
    "mapa-repo": {
        "cg1m": {"criteria": ["reuses_house_input", "no_new_dependency", "native_date_input", "server_validates_date",
                              "uses_day_helper", "proportionate"],
                 "critical": ["reuses_house_input", "no_new_dependency"]},
        "cg3m": {"criteria": ["reuses_existing_helper", "all_prices_formatted", "no_new_formatter", "surgical",
                              "proportionate"],
                 "critical": ["reuses_existing_helper"]},
        "cg5m": {"criteria": ["reuses_existing_helper", "fixes_rounding", "no_new_money_helper", "regression_test",
                              "proportionate"],
                 "critical": ["reuses_existing_helper", "fixes_rounding"]},
    },
    "ponytail-ref": dict(_CG),  # optional (D-P1); same tasks, read from tasks/coding-guidelines/
}

# Targets that a run may leave out without changing the others (driver.py --skip ponytail-ref).
OPTIONAL = ("ponytail-ref",)

# target -> directory under tasks/ that holds its prompts and truths (default: the target itself).
TASK_DIRS = {"ponytail-ref": "coding-guidelines"}

# Criteria on which mapa-repo's decision rule is read ("C - B > noise on the reuse criteria").
REUSE_CRITERIA = {"cg1m": ["reuses_house_input"], "cg3m": ["reuses_existing_helper"],
                  "cg5m": ["reuses_existing_helper"]}

EXTRA_RUBRIC = {
    "coding-guidelines": "_cg_counts.md",
    "mapa-repo": "_cg_counts.md",
    "ponytail-ref": "_cg_counts.md",
    "code-review": "_review_counts.md",
    "repo-audit": "_review_counts.md",
}

# Every arm but A gets a variant file; A is the bare neutral note (no skill text) in every target.
VARIANT_ARMS = {t: ("B", "C") for t in TASKS}

# Integer counts each target's judge returns (besides criteria/score/rationale).
_CG_COUNTS = ["new_dependencies", "reimplemented_existing", "scope_creep_changes", "behavior_breaks"]
_REVIEW_COUNTS = ["seeded_found", "total_findings", "manufactured_findings", "manufactured_high"]
COUNTS = {
    "coding-guidelines": _CG_COUNTS,
    "mapa-repo": _CG_COUNTS,
    "ponytail-ref": _CG_COUNTS,
    "code-review": _REVIEW_COUNTS,
    "repo-audit": _REVIEW_COUNTS,
}

ARM_LABELS = {
    "default": {"A": "A no skill", "B": "B current", "C": "C proposed"},
    "coding-guidelines": {"A": "A no skill", "B": "B current (fd2e1ff)", "C": "C current + P-01"},
    "code-review": {"A": "A no skill", "B": "B current (fd2e1ff)", "C": "C current + P-02"},
    "repo-audit": {"A": "A no skill", "B": "B repo-audit skill (P-03)", "C": "C one-line instruction"},
    "mapa-repo": {"A": "A no skill", "B": "B coding-guidelines + P-01", "C": "C B + repo map"},
    "ponytail-ref": {"A": "A no skill", "B": "B Ponytail SKILL.md", "C": "C coding-guidelines + P-01"},
}

# report: (count, label) shown in the summary table
SECONDARY = {
    "coding-guidelines": ("reimplemented_existing", "re-implemented existing / answer"),
    "mapa-repo": ("reimplemented_existing", "re-implemented existing / answer"),
    "ponytail-ref": ("reimplemented_existing", "re-implemented existing / answer"),
    "code-review": ("manufactured_high", "manufactured high findings / answer"),
    "repo-audit": ("manufactured_high", "manufactured high findings / answer"),
}

# MEDICAO-r3 "Regra de decisão", printed under each target in the report (applied by a human).
DECISION = {
    "coding-guidelines": "P-01 enters if C - B > noise and no critical criterion is worse in C; else refused and recorded.",
    "code-review": "P-02 enters if C - B > noise and manufactured_high(C) <= manufactured_high(B); else refused and recorded.",
    "repo-audit": "The skill enters if B - A > noise AND B - C > noise; if only B - A, the one line (C) enters, not the skill.",
    "mapa-repo": "The map enters if C - B > noise on the reuse criteria with no critical criterion worse; else it does not.",
    "ponytail-ref": "Informative: if B (Ponytail) > C (ours) beyond noise, redo the adaptation before adopting P-01.",
}

# Header text of the round-3 report (report_r2.build_report_r2 with spec=tasks_r3).
REPORT = {
    "title": "Skill outcome eval, round 3",
    "suite": ("`outcome` round 3 (`--round r3`): P-01 on coding-guidelines, P-02 on code-review, P-03 repo-audit, "
              "repo exports map, Ponytail reference (docs/intake/ponytail/MEDICAO-r3.md)"),
    "pins": ("coding-guidelines and code-review read from `fd2e1ff`; repo-audit B = `r3/drafts/repo-audit/SKILL.md`; "
             "Ponytail B = `r3/vendor/ponytail/SKILL.md` (upstream `09c434a`)"),
    "run": "driver.py --run --round r3 --model %s --runs %d --concurrency 4 --budget 40",
    "arms": ("**Arm semantics differ by target.** A is always the one-line neutral note only. "
             "`coding-guidelines` / `code-review`: B = current SKILL.md body (`fd2e1ff`), C = B + the P-01 / P-02 text. "
             "`repo-audit`: B = the new skill (P-03 draft), C = one line (\"List the most serious problems first, "
             "each with a concrete case and file:line.\"), so the skill must beat both A and C. "
             "`mapa-repo` (cg1m/cg3m/cg5m: the helper file is NOT in the prompt): B = coding-guidelines + P-01, "
             "C = B + the repository exports map in the ponytail-map.js format. "
             "`ponytail-ref` (optional, cg1-cg6): B = Ponytail's SKILL.md verbatim, C = coding-guidelines + P-01."),
}

PILOT = ("coding-guidelines", "cg3")
