# Wireframes Behavior

## Read Scope

- Must read: `core/contract.yaml`, `core/contract-behavior.md`, `paths.wireframe_input`, and `skills/ba-start/steps/wireframes.md`.
- May read: `paths.project_memory` or hot decisions, `paths.design_doc`, module warm shard, and `paths.srs_index` for targeted screen lookup.
- Must not read: `log.md`, `cold/`, other module shards, unrelated module artifacts.

## Design Document Handling

- `paths.design_doc` is the runtime design constraint source for UI-backed modules.
- If it exists, ask whether to reuse, refresh, or stop before changing it.
- If absent or refresh is approved, synthesize it from approved decisions using `templates/design-md-template.md`.
- Keep `defaults.ui_baseline` as fallback only when the approved design document does not specify another direction.
- Do not proceed when design direction, portal navigation schema, or active-menu rules remain unresolved.

## Wireframe-State Behavior

- Use values from `states.wireframe` only: `completed`, `skipped`, `not-applicable`, or `missing`.
- `wireframes` is read-only on upstream BA artifacts.
- It may regenerate only the runtime `DESIGN.md`, wireframe input pack, wireframe map, and wireframe state.

## Allowed Outputs

- `paths.design_doc`
- `paths.wireframe_input`
- `paths.wireframe_map`
- `paths.wireframe_state`

The wireframe map/checklist is a handoff artifact, not the source of truth for requirements. Screen and behavior changes discovered during wireframing route through `impact`.
