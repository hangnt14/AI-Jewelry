# Fixture F28: Wireframes Stays Downstream And Does Not Trigger QC

## Scenario

`ba-start wireframes` runs after a module already passed through the post-`srs` QC boundary. The
runtime may write manual handoff artifacts, but it must not auto-trigger `qc-review` again from
the wireframes step.

## Input State

```text
plans/test-project-20260526/
└── 03_modules/auth-flow/
    ├── srs-index.md
    ├── srs.md
    ├── srs-compile-receipt.json
    ├── qc-review/
    │   └── auth-flow-qc-review-report-v1.md
    ├── wireframe-input.md
    └── tool-lane-state.md
```

The module already has an SRS and an existing QC report from the post-`srs` gate.

## Input Command

```text
ba-start wireframes --slug test-project --module auth-flow
```

## Expected Behavior

- Reads the wireframe handoff inputs and writes downstream wireframe artifacts.
- Keeps QC as a completed upstream event rather than re-running it.
- Does not produce a new QC report version from the wireframes step.
- Leaves aggregate cross-artifact validation to `ba-start package`.

## Expected Outcome

| Field | Expected Value |
| --- | --- |
| resolved_command | ba-start wireframes |
| source_of_truth_artifact | plans/test-project-20260526/03_modules/auth-flow/wireframe-input.md |
| write_target | plans/test-project-20260526/03_modules/auth-flow/wireframe-state.md |
| approval_gate | NOT_REQUIRED |
| activation_level | Base |
| fallback_code | NONE |

## Notes

- This fixture fails parity if `wireframes` auto-invokes `qc-review`.
- Golden: `goldens/g28-wireframes-does-not-trigger-qc.md`
