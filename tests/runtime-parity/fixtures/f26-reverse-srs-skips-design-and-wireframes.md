## Scenario

BA runs `ba-start srs` for a module in a project with an active reverse lane and validated reverse evidence, but no `DESIGN.md` or wireframe artifacts.

## Input State

Project set exists with:
- `02_backbone/backbone.md`
- `03_modules/auth-flow/user-stories.md`
- `00_reverse/reverse-baseline-lock.json` with confirmed focus selection
- `00_reverse/reverse-index.md` marked current
- `00_reverse/reverse-focus-excerpts.md`
- `00_reverse/reverse-evidence-ledger.md`
- `00_reverse/reverse-drift-state.json` marked current

Missing on purpose:
- `designs/test-project/DESIGN.md`
- `03_modules/auth-flow/wireframe-input.md`
- `03_modules/auth-flow/wireframe-map.md`
- `03_modules/auth-flow/wireframe-state.md`

## Input Command

ba-start srs --slug test-project --module auth-flow

## Expected Behavior

- Resolves the active reverse lane before applying forward UI gating.
- Uses reverse evidence as the blocking prerequisite for reverse-backed SRS work.
- Does not stop to request `DESIGN.md`.
- Does not stop to request `wireframe-input`, `wireframe-map`, or `wireframe-state`.
- Treats wireframes as `not-applicable` for this reverse-backed pass.
- Routes future-state UI changes back through `impact` instead of inventing design prerequisites.

## Expected Outcome

| Field | Value |
| --- | --- |
| resolved_command | ba-start srs |
| source_of_truth_artifact | backbone |
| write_target | plans/test-project-20260424/03_modules/auth-flow/srs.md |
| approval_gate | NONE |
| activation_level | Base |
| fallback_code | NONE |
