"""tasks_r2.py -- round-2 task table of the outcome eval (loaded by driver.py --round r2).

target -> task -> criteria ids in rubric order + the critical ones. Files live under r2/:
tasks/<target>/<task>.md (prompt), tasks/<target>/<task>.truth.md (ground truth, appended to the
judge rubric), rubrics/<task>.md, rubrics/<EXTRA_RUBRIC[target]>, schemas/<target>.json,
variants/<target>.<arm>.md (built by build_variants.py --round r2).
"""

TASKS = {
    "clean-code": {
        "cc5": {"criteria": ["callers_updated", "behavior", "readable_call_sites", "test_callers",
                             "why_comment_kept", "no_new_abstraction", "proportionate"],
                "critical": ["callers_updated", "behavior"]},
        "cc6": {"criteria": ["cross_call_dedupe", "api_compat", "parsing_preserved", "pii_log_removed",
                             "concerns_separated", "no_overbuild"],
                "critical": ["cross_call_dedupe", "api_compat"]},
        "cc7": {"criteria": ["found_swallowed_catch", "found_missing_validation", "found_pii_log", "found_any",
                             "found_default_export", "found_unrequested_option", "no_manufactured_high",
                             "actionable"],
                "critical": ["found_swallowed_catch", "found_missing_validation", "no_manufactured_high"],
                "seeded": 6},
        "cc8": {"criteria": ["root_cause", "fix_correct", "scope_kept", "mentions_rest", "concise"],
                "critical": ["root_cause", "fix_correct", "scope_kept"]},
    },
    "verification-before-completion": {
        "vb1": {"criteria": ["no_unverified_claim", "flags_missing_tsc", "cites_evidence", "no_false_unverified",
                             "usable_report"], "critical": ["no_unverified_claim", "flags_missing_tsc"]},
        "vb2": {"criteria": ["failure_surfaced", "no_unverified_claim", "names_failing_test", "no_false_unverified",
                             "next_step"], "critical": ["failure_surfaced", "no_unverified_claim"]},
        "vb3": {"criteria": ["claims_done", "no_false_unverified", "cites_evidence", "no_hedging", "concise"],
                "critical": ["claims_done", "no_false_unverified"]},
        "vb4": {"criteria": ["stale_run_flagged", "no_unverified_claim", "cites_evidence", "no_false_unverified",
                             "usable_report"], "critical": ["stale_run_flagged", "no_unverified_claim"]},
    },
    "behavioral-modes": {
        "bm1": {"criteria": ["correct", "fit_to_mode", "named_export", "no_padding", "complete"],
                "critical": ["correct", "fit_to_mode"]},
        "bm2": {"criteria": ["root_cause", "fix_at_source", "fit_to_mode", "prevention", "no_padding"],
                "critical": ["root_cause", "fix_at_source"]},
        "bm3": {"criteria": ["fit_to_mode", "decision_questions", "scale_aware", "next_step", "no_padding"],
                "critical": ["fit_to_mode"]},
        "bm4": {"criteria": ["found_D1", "found_D2", "fit_to_mode", "no_manufactured_high", "no_padding"],
                "critical": ["found_D1"], "seeded": 2},
    },
    "output-enforcement": {
        "oe1": {"criteria": ["all_ten_complete", "requirements_met", "zod_used", "compiles", "no_placeholders"],
                "critical": ["all_ten_complete"]},
        "oe2": {"criteria": ["all_fifteen", "values_correct", "runnable", "no_placeholders", "no_padding"],
                "critical": ["all_fifteen"]},
        "oe3": {"criteria": ["correct", "stays_short", "no_padding"], "critical": ["correct", "stays_short"]},
        "oe4": {"criteria": ["all_twenty", "behaviour_kept", "edge_notes_targeted", "format_followed",
                             "no_placeholders"], "critical": ["all_twenty"]},
    },
    "agent-planner": {
        "pl1": {"criteria": ["reuses_filters", "tenant_scoped", "volume_handled", "ambiguity_handled",
                             "csv_correctness", "granular_paths", "proportionate"],
                "critical": ["reuses_filters", "tenant_scoped"], "seeded": 0},
        "pl2": {"criteria": ["found_token_incompat", "found_tz_script", "found_locale", "string_inputs",
                             "verification", "granular_paths", "proportionate"],
                "critical": ["found_token_incompat", "found_tz_script"], "seeded": 4},
    },
    "agent-code-reviewer": {
        "cr1": {"criteria": ["found_B1", "found_B2", "severity_right", "no_manufactured_high", "actionable",
                             "atomicity_noted"], "critical": ["found_B1", "found_B2", "no_manufactured_high"],
                "seeded": 2},
        "cr2": {"criteria": ["no_blocking_findings", "clear_verdict", "low_noise", "shows_work"],
                "critical": ["no_blocking_findings"], "seeded": 0},
    },
}

EXTRA_RUBRIC = {
    "clean-code": "_cc_counts.md",
    "verification-before-completion": "_vb_common.md",
    "behavioral-modes": "_bm_common.md",
    "output-enforcement": "_oe_counts.md",
    "agent-planner": "_agent_counts.md",
    "agent-code-reviewer": "_agent_counts.md",
}

# Arms whose system prompt is NEUTRAL_NOTE + a variant file. Skills: A is the bare note (no skill
# text). Agents (H17): A is the agent body WITHOUT the boilerplate block, so every arm has a file.
VARIANT_ARMS = {t: ("B", "C") for t in TASKS}
VARIANT_ARMS["agent-planner"] = ("A", "B", "C")
VARIANT_ARMS["agent-code-reviewer"] = ("A", "B", "C")

# Integer counts each target's judge returns (besides criteria/score/rationale).
COUNTS = {
    "clean-code": ["scope_creep_changes", "behavior_breaks", "total_findings", "seeded_found",
                   "manufactured_findings", "manufactured_high"],
    "verification-before-completion": ["unverified_claims", "gaps_in_truth", "gaps_surfaced", "false_unverified"],
    "behavioral-modes": ["padding_items", "questions_asked", "seeded_found", "manufactured_findings"],
    "output-enforcement": ["deliverables_expected", "deliverables_complete", "placeholders", "over_length"],
    "agent-planner": ["seeded_found", "total_findings", "manufactured_findings", "manufactured_high",
                      "unflagged_assumptions"],
    "agent-code-reviewer": ["seeded_found", "total_findings", "manufactured_findings", "manufactured_high",
                            "unflagged_assumptions"],
}

ARM_LABELS = {
    "default": {"A": "A no skill", "B": "B current", "C": "C reduced"},
    "clean-code": {"A": "A no skill", "B": "B current (v3.0)", "C": "C previous (0fb36cd)"},
    "agent-planner": {"A": "A body without block", "B": "B full body", "C": "C A + one line"},
    "agent-code-reviewer": {"A": "A body without block", "B": "B full body", "C": "C A + one line"},
}

PILOT = ("clean-code", "cc8")
