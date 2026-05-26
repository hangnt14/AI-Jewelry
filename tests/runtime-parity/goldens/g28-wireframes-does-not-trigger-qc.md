# Golden: F28 - Wireframes Stays Downstream And Does Not Trigger QC

## Behavior Envelope

| Field | Expected Value |
| --- | --- |
| resolved_command | ba-start wireframes |
| resolved_slug | test-project |
| source_of_truth_artifact | plans/test-project-20260526/03_modules/auth-flow/wireframe-input.md |
| read_scope | core/contract.yaml, core/contract-behavior.md, core/behavior/wireframes.md, plans/test-project-20260526/03_modules/auth-flow/wireframe-input.md, plans/test-project-20260526/03_modules/auth-flow/srs.md, plans/test-project-20260526/03_modules/auth-flow/qc-review/auth-flow-qc-review-report-v1.md |
| write_target | plans/test-project-20260526/03_modules/auth-flow/wireframe-state.md |
| approval_gate | NOT_REQUIRED |
| activation_level | Base |
| fallback_code | NONE |

## Runtime Parity Check

| Runtime | Status |
| --- | --- |
| Claude Code | EXEMPT v1 maintainer decision |
| Codex | EXEMPT v1 maintainer decision |
| Antigravity | EXEMPT v1 maintainer decision |

## Notes

- QC already happened after `srs`. `wireframes` must not create `auth-flow-qc-review-report-v2.md`.
- Aggregate cross-artifact validation is deferred to `ba-start package`.
