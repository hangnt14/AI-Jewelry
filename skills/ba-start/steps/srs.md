# BA Start Step - SRS Router

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`
- `core/behavior/srs.md`

## Governance Gate

Before mutating any SRS artifact:
1. **Skip this gate for first-pass creation** (when the target `paths.srs_group` or `paths.srs` does not yet exist).
2. For reruns (artifact already exists): verify write authority and locate the active impact receipt at `paths.impact_receipt`. If no active receipt exists and `change_class` is not `wording-only`, emit `GOVERNANCE_BLOCK: impact_receipt missing or invalidated` and stop.
3. If either check fails on a rerun: emit `GOVERNANCE_BLOCK: {reason}` and stop.
4. After mutation completes: offer to file the change into canonical memory using `templates/project-memory-fileback-record-template.md`.

Receipt reference: `templates/impact-receipt-template.md`

## Scope

Run Steps 8-11 only. This path stays split so SRS execution can load only the group instructions needed for the current pass.

## Read Order

1. Read this router for SRS preflight and orchestration.
2. Read [srs-core.md](./srs-core.md) for Step 8 and Step 8.1.
3. Read [srs-wireframes.md](./srs-wireframes.md) for Step 8.2, Step 9, Step 10, and Group D.
4. Read [srs-assembly.md](./srs-assembly.md) for Step 10.1 and Step 11.

## Prerequisites

- Resolve slug, date, and module using the shared contract.
- Require `paths.backbone`, `paths.stories`, `paths.backbone_index`, and `paths.stories_index`.
- If a required artifact is missing, print the exact missing path, tell the user which subcommand to run first, and stop.
- Run preflight from indexes first; read only targeted backbone/story sections, optional module FRD, and `paths.plan` when it exists.

## Outputs

- `paths.srs_group` for groups `a` through `f`
- `paths.srs`
- `paths.srs_index`
- `paths.wireframe_input`
- `paths.design_doc` when Step 8.2/Step 9 confirms or refreshes the UI design direction
- wireframe artifacts and state produced during Step 9

Treat generated index/state/memory artifacts as `agent_facing` or `machine_facing`; keep them compact.
When `paths.srs_index` is written or refreshed, keep `stale_status: unknown`, leave `validated_at` and `validated_by` blank, then run `python3 scripts/validate-index-quality.py --repo . --index-key srs_index --slug <slug> --date <date> --module <module> --writeback` before downstream work treats the index as `current`.

## Execution Order

```text
Step 8   -> srs-core.md
Step 8.2 -> srs-wireframes.md before Group C when UI-backed screens need DESIGN.md
Step 9   -> srs-wireframes.md
Step 10  -> srs-wireframes.md
Step 10.1 + 11 -> srs-assembly.md
```
