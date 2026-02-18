# StoryVerse Evaluation Gating Spec (v1)

This document defines a unified, benchmark-aligned evaluation gate for:
- `sv-intake`
- `sv-plan`
- `sv-script`
- `sv-assets`
- `sv-system-script`
- `sv-storyboard`
- `sv-shots`
- `sv-voice`
- `sv-consistency` (repair mode)
- `sv-edit`
- `sv-review`

The goal is strict progression control: a stage cannot proceed unless its evaluation passes.

## 1) Architecture Decision

Use a hybrid model:
- Embedded execution in each stage command: evaluation runs automatically before stage completion.
- Separate evaluation artifacts on disk: structured outputs saved in `evaluations/` for audit and retries.

Reason:
- Embedded gates enforce flow control.
- Separate files make debugging, benchmarking, and LangSmith tracking easier.

## 2) Rubric Baseline (from `Storyverse benchmark rubric.pdf`)

Global benchmark categories:
- Foundational Quality: `20 pts`
  - Consistency `7`
  - Fidelity `7`
  - Physics `6`
  - Critical rule: foundational failure caps overall score at `40`.
- Narrative Quality: `20 pts`
  - Conflict/Stakes `4`
  - Character Arc `4`
  - Storyline Logic `4`
  - Hook Density `4`
  - Dialogue `4`
  - Critical rule: dialogue failure caps narrative score at `8/20`.
- Cinematic Grammar: `30 pts`
  - Composition `10`
  - Dynamics `10`
  - Editing `10`
- Advanced Categories: `30 pts`
  - Acting `10`
  - IP Extensibility `10`
  - Artistic Mastery `10`

## 3) Unified Eval Output Schema

All stages output the same top-level format:

```json
{
  "schema_version": "storyverse_eval_gate_v1",
  "stage": "intake|plan|script|assets|system_script|storyboard|shots|voice|consistency|edit|review",
  "project_id": "string",
  "episode_number": 1,
  "run_id": "uuid",
  "input_refs": {
    "source_files": [],
    "artifact_files": []
  },
  "score": {
    "overall": 0,
    "overall_max": 100,
    "pass_threshold": 85,
    "passed": false,
    "caps_applied": [
      {
        "cap_type": "foundational_cap_40|dialogue_cap_8",
        "reason": "string"
      }
    ]
  },
  "rubric_scores": {
    "foundational": {"score": 0, "max": 20, "passed": false},
    "narrative": {"score": 0, "max": 20, "passed": false},
    "cinematic_grammar": {"score": 0, "max": 30, "passed": false},
    "advanced": {"score": 0, "max": 30, "passed": false}
  },
  "hard_failures": [
    {
      "code": "string",
      "message": "string",
      "evidence": ["string"]
    }
  ],
  "checks": [
    {
      "check_id": "string",
      "category": "foundational|narrative|cinematic_grammar|advanced",
      "severity": "hard|soft",
      "passed": false,
      "score": 0,
      "max": 0,
      "evidence": ["string"],
      "fix_hint": "string"
    }
  ],
  "issues": [
    {
      "severity": "critical|major|minor",
      "type": "string",
      "message": "string"
    }
  ],
  "retry": {
    "attempt": 1,
    "max_attempts": 3,
    "next_action": "proceed|retry|stop"
  },
  "can_proceed": false,
  "generated_at": "2026-02-17T00:00:00Z"
}
```

## 4) File Naming Convention

- `evaluations/script_eval.json`
- `evaluations/assets_eval.json`
- `evaluations/system_script_eval.json`
- `evaluations/storyboard_eval.json`
- `evaluations/shots_eval.json`
- `evaluations/intake_eval.json`
- `evaluations/plan_eval.json`
- `evaluations/voice_eval.json`
- `evaluations/consistency_eval.json`
- `evaluations/edit_eval.json`
- `evaluations/review_eval.json`
- Optional per-episode detail:
  - `evaluations/script/episode_{N}.json`
  - `evaluations/assets/episode_{N}.json`
  - `evaluations/storyboard/episode_{N}.json`
  - `evaluations/shots/episode_{N}.json`

## 5) Stage Gate Profiles

## 5.0 Operational Stage Gates

These stages are evaluated for completeness/integrity rather than cinematic scoring:
- `sv-intake` → `evaluations/intake_eval.json`
  - required brief fields present, enums valid
- `sv-plan` → `evaluations/plan_eval.json`
  - settings schema and range validation
- `sv-voice` → `evaluations/voice_eval.json`
  - voice-output count parity, intelligibility, no severe desync/artifacts
- `sv-consistency` (repair mode) → `evaluations/consistency_eval.json`
  - all reviewed frames have explicit status/action, unresolved critical issues = 0
- `sv-edit` → `evaluations/edit_eval.json`
  - final video/subtitle/audio outputs exist and are coherent
- `sv-review` → `evaluations/review_eval.json`
  - notes are complete, uniquely identified, and actionable

For these operational gates, `can_proceed=true` requires:
- zero hard failures
- required outputs present and parseable
- `score.overall >= score.pass_threshold`

Operational pass thresholds (numeric):
- `sv-intake`: `pass_threshold = 90`
- `sv-plan`: `pass_threshold = 95`
- `sv-voice`: `pass_threshold = 82`
- `sv-consistency`: `pass_threshold = 85`
- `sv-edit`: `pass_threshold = 85`
- `sv-review`: `pass_threshold = 90`

## 5.1 Script Gate (`sv-script`)

Mandatory hard checks:
- `locked_dialogue_recall_100`: all source dialogue/locked lines preserved.
- `speaker_attribution_exact`: original speaker labels preserved.
- `source_order_integrity`: no event leakage/reordering.
- `no_hallucinated_world_rules`: no invented system rules or physical rules.
- `dialogue_expansion_grounded`: expanded dialogue (if any) must stay source-entailed.

Dialogue expansion policy:
- Expansion is allowed only when source text is too sparse for performability.
- Must preserve source facts, causality, relationships, and outcomes.
- Added dialogue ratio must remain `<= 40%` of total dialogue lines.
- Never replace locked lines with generated lines.

Passing thresholds:
- Narrative: `>= 16/20`
- Foundational text-proxy checks: `>= 8/10` (stored under foundational evidence)
- Overall normalized score: `>= 85/100`
- Any hard check fail => `can_proceed=false`

## 5.2 Assets Gate (`sv-assets`)

Mandatory hard checks:
- `character_reference_match`: generated character matches intended character ID.
- `environment_reference_match`: generated scene matches intended environment ID.
- `anatomy_integrity`: no severe anatomy defects (extra fingers/extra limbs/distorted joints).
- `no_identity_swap`: no cross-character appearance leakage.

Passing thresholds:
- Foundational: `>= 16/20`
- Narrative alignment (character/scene intent fit): `>= 15/20`
- Overall normalized score: `>= 83/100`
- Any hard check fail => `can_proceed=false`

## 5.3 Storyboard Gate (`sv-storyboard`)

Mandatory hard checks:
- `beat_to_keyframe_alignment`: frame content matches beat key point.
- `character_presence_accuracy`: required character IDs present, missing IDs fail.
- `environment_accuracy`: frame location matches scene ID.
- `anatomy_integrity`: no severe anatomy defects.
- `spatial_continuity`: no impossible blocking or clipping between adjacent beats.

Passing thresholds:
- Foundational: `>= 16/20`
- Narrative: `>= 15/20`
- Cinematic grammar: `>= 20/30`
- Overall normalized score: `>= 84/100`
- Any hard check fail => `can_proceed=false`

## 5.4 Shots Gate (`sv-shots`)

Mandatory hard checks:
- `character_environment_binding`: shot matches target character/environment IDs.
- `physics_integrity`: no clipping, broken motion logic, or severe jitter glitches.
- `anatomy_integrity_temporal`: no persistent extra fingers/limb deformation across frames.
- `dialogue_alignment`: spoken/dialogue timing aligns with script intent.

Rubric caps (strict):
- If foundational fails, cap overall score at `40` and block progression.
- If dialogue fails, cap narrative at `8/20`.

Passing thresholds:
- Foundational: `>= 16/20`
- Narrative: `>= 15/20`
- Cinematic grammar: `>= 24/30`
- Advanced: `>= 21/30`
- Overall score: `>= 85/100`
- Any hard check fail => `can_proceed=false`

## 6) Retry and Stop Policy

- Auto-retry max: `3` attempts per failed item.
- Retry strategy order:
  1) Prompt correction
  2) Stronger reference binding (character/environment)
  3) Model/tool fallback
- Stop conditions:
  - Hard failure persists after max retries
  - Overall score remains below threshold after max retries

## 7) Pipeline Enforcement Rules

Pipeline progression rule:
- Next stage is blocked unless current stage `can_proceed=true`.

`sv-pipeline` behavior:
- Runs stage eval after each stage artifact write.
- Writes/updates corresponding `evaluations/*_eval.json`.
- Stops immediately on failure with:
  - hard_fail summary
  - failed checks
  - recommended retry action

## 8) Backward Compatibility

Keep current shot fields:
- `quality_score`
- `quality_issues`

Add gate metadata in parallel:
- `eval_gate_summary` at shot version level (optional compact snapshot)
- Full details remain in `evaluations/shots_eval.json`

## 9) Implementation Sequence

1. Add schema references in `context/json-schemas.md` (new QA Gate section).
2. Update `sv-script`, `sv-assets`, `sv-storyboard`, `sv-shots` to run stage gate.
3. Update `sv-pipeline` to enforce `can_proceed` between stages.
4. Keep `/sv-judge` as human feedback loop (not gate replacement).
