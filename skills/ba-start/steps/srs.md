# BA Start Step - SRS Router

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`
- `core/behavior/srs.md`

## Governance Gate

Before mutating any SRS artifact:
1. **Skip this gate for first-pass creation** (when `paths.srs_spec` and `paths.srs` do not yet exist).
2. For reruns (artifacts already exist): verify write authority and locate the active impact receipt at `paths.impact_receipt`. If no active receipt exists and `change_class` is not `wording-only`, emit `GOVERNANCE_BLOCK: impact_receipt missing or invalidated` and stop.
3. If either check fails on a rerun: emit `GOVERNANCE_BLOCK: {reason}` and stop.
4. After mutation completes: offer to file the change into canonical memory using `templates/project-memory-fileback-record-template.md`.

## Backbone Authority Gate

Before writing any SRS source artifact, run backbone alignment validation per `core/behavior/srs.md`. Misalignment produces `BACKBONE_ALIGNMENT_FAIL: {scope}` and stops execution.

## Scope

Run Steps 8-11 only. This path stays split so SRS execution can load only the instructions needed for the current pass.

## Read Order

1. Read this router for SRS preflight and orchestration.
2. Read [srs-core.md](./srs-core.md) for source set generation (spec, usecases, ascii-screen).
3. Read [srs-wireframes.md](./srs-wireframes.md) for ASCII wireframe gates and DESIGN.md gating.
4. Read [srs-assembly.md](./srs-assembly.md) for partial compile and receipt generation.

## Prerequisites

- Resolve slug, date, and module using the shared contract.
- Require `paths.backbone`, `paths.backbone_index`, and `paths.userstories_index`.
- If a required artifact is missing, print the exact missing path, tell the user which subcommand to run first, and stop.
- Run preflight from indexes first; read only targeted backbone/story sections, optional module FRD, and `paths.plan` when it exists.
- In reverse mode, gate on a valid reverse baseline, current drift state, and traceable reverse evidence; do not require `paths.design_doc`.

## Outputs

- `paths.srs_spec` — FR/NFR/business rules/API/data constraints
- `paths.srs_flows` — module/system flows (not UC-level diagrams)
- `paths.srs_states` — module state registry
- `paths.srs_erd` — business data model when justified
- `paths.usecases_index` + `paths.usecase_item` files — use case canon
- `paths.usecase_diagrams` — UC-specific diagrams
- `paths.ascii_screen_index` + `paths.ascii_screen_item` files — screen canon with mandatory ASCII wireframes
- `paths.srs` — compiled output only (requested-scope compile)
- `paths.srs_compile_receipt` — receipt with compile scope and source hashes
- `paths.screen_field_contract` — normalized machine-facing screen truth
- `paths.design_doc` when Step 8.2 confirms or refreshes the UI design direction

Do NOT create `srs-index.md`, `screens/`, `data/`, `flows/`, or `srs-groups/`.

Treat generated index artifacts as `agent_facing`; keep them compact.
When `paths.usecases_index` or `paths.ascii_screen_index` is written or refreshed, keep `stale_status: unknown`, leave `validated_at` and `validated_by` blank, then run:

```bash
python3 scripts/validate-index-quality.py --repo . --index-key usecases_index --slug <slug> --date <date> --module <module> --writeback
python3 scripts/validate-index-quality.py --repo . --index-key ascii_screen_index --slug <slug> --date <date> --module <module> --writeback
```

before downstream work treats the indexes as `current`.

Treat `paths.srs` as the compiled, reader-facing deliverable. Direct edits to `paths.srs` are blocked by default; canonical edits belong in the module source files and must compile back into `paths.srs` via the partial compile routine.

## Partial Compile Semantics

Parse `--scope` flag or user request to determine compile scope:
- `full` — compile all source files
- `spec` — compile `srs/spec.md` only
- `usecases` — compile `usecases/index.md` + selected UC files + diagrams
- `screens` — compile `ascii-screen/index.md` + selected screen files
- `flows` — compile `srs/flows.md`
- `states` — compile `srs/states.md`
- `erd` — compile `srs/erd.md`
- `mixed` — compile user-requested combination

Receipt must define `compile_scope`, `requested_sections`, `included_sources`, `excluded_sources`, and `source_hashes`. Source changes outside requested scope do not mark receipt stale.

## Execution Order

```text
Backbone alignment gate
Step 8   -> srs-core.md  (generate source set)
Step 8.2 -> srs-wireframes.md  (DESIGN.md gate, ASCII coverage)
Step 10  -> srs-wireframes.md  (screen field contract)
Step 10.1 + 11 -> srs-assembly.md  (partial compile, receipt)
```
