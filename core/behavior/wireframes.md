# Wireframes Behavior

## Read Scope

- Must read: `core/contract.yaml`, `core/contract-behavior.md`, `paths.wireframe_input`, and `skills/ba-start/steps/wireframes.md`.
- May read: `paths.project_memory` or hot decisions, `paths.design_doc`, `paths.shared_shell_contract`, `paths.shared_shell_index`, `paths.tool_lane_state`, `paths.screen_field_contract`, module warm shard, and `paths.srs_index` for targeted screen lookup.
- Must not read: `log.md`, `cold/`, other module shards, unrelated module artifacts.

## Transitional Scope

- This behavior remains active only for the legacy manual wireframe handoff lane.
- Canonical requirement ownership does **not** live in `paths.wireframe_input` or `paths.wireframe_map`.
- Canonical screen/UI behavior is moving to module-local `paths.screen_item`, `paths.usecase_item`, `paths.module_erd`, and routing indexes under `paths.srs_index`.
- Future ASCII and Figma generation must consume canon screen sources plus the shared shell contract instead of mutating upstream BA meaning here.

## Design Document Handling

- `paths.design_doc` is the runtime design constraint source for UI-backed modules.
- During the migration window, treat `paths.design_doc` as the visual-direction document and `paths.shared_shell_contract` as the machine-usable ownership contract for portals, nav schemas, shell variants, and active-menu rules.
- If it exists, ask whether to reuse, refresh, or stop before changing it.
- If absent or refresh is approved, synthesize it from approved decisions using `templates/design-md-template.md`.
- Keep `defaults.ui_baseline` as fallback only when the approved design document does not specify another direction.
- Do not proceed when design direction, portal navigation schema, or active-menu rules remain unresolved.

## Wireframe-State Behavior

- Use values from `states.wireframe` only: `completed`, `skipped`, `not-applicable`, or `missing`.
- Use values from `states.tool_lane` for tool-lane selection: `manual`, `figma-make`, or `not-applicable`.
- `wireframes` is read-only on upstream BA artifacts.
- It may regenerate only the runtime `DESIGN.md`, wireframe input pack, wireframe map, and wireframe state.
- Direct edits to `paths.srs` are not the source-of-truth path. If manual wireframe work reveals requirement changes, route through canon source edits first, then recompile `paths.srs`.
- It may also regenerate downstream tool-lane control artifacts that are explicitly listed in `commands.wireframes.outputs`.
- Default lane is `manual` when the user does not explicitly opt into a supported AI lane.
- AI tool lanes must fail closed when `paths.screen_field_contract` is missing or incomplete for the targeted UI-backed screens.
- If the selected tool lane changes, treat prior tool-specific artifacts for that module as stale and regenerate them from current `paths.screen_field_contract`.
- If `impact` changes screen inventory, field rules, navigation, required states, or validation behavior, treat `paths.screen_field_contract`, `paths.make_guidelines`, `paths.make_prompt_pack`, `paths.prototype_conformance_checklist`, and `paths.prototype_conformance_report` as stale until the owning steps rerun.

## Allowed Outputs

- `paths.design_doc`
- `paths.wireframe_input`
- `paths.wireframe_map`
- `paths.wireframe_state`
- `paths.tool_lane_state`
- `paths.make_guidelines`
- `paths.make_prompt_pack`
- `paths.prototype_conformance_checklist`
- `paths.prototype_conformance_report`
- `paths.figma_make_shared_rules`
- `paths.figma_make_shared_prompt_skeleton`
- `paths.figma_make_shared_component_contracts`

The wireframe map/checklist is a handoff artifact, not the source of truth for requirements. Screen and behavior changes discovered during wireframing route through `impact`.
