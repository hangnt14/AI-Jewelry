# BA Start Step - Wireframes

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`
- `core/behavior/wireframes.md`

## Scope

Run Step 9 only. This path is read-only on upstream BA artifacts and may regenerate only the runtime `DESIGN.md`, wireframe constraint pack, wireframe handoff checklist, and wireframe state marker.

## Prerequisites

- Resolve slug, date, and module using the shared contract.
- Resolve the wireframe source in this order:
  1. `paths.wireframe_input`
  2. exact pair of `paths.srs_group` with `group=b` and `group=c`
  3. `paths.srs` only when Use Case Specifications, Screen Contract Plus, and Screen Inventory are already assembled there
- If source 2 or 3 is used, require exact `paths.backbone`, rebuild `paths.wireframe_input`, and save it before continuing.
- If none of the sources exist, print all expected paths and stop.

## Outputs

- `paths.design_doc`
- `paths.wireframe_input`
- `paths.wireframe_map`
- `paths.wireframe_state`

## Step 9.1 - Resolve Wireframe Input Pack

Use `paths.wireframe_input` as the primary constraint source.

If the pack is missing but fallback sources exist, assemble it from exact use case excerpts, Screen Contract Plus, Screen Inventory, and the exact portal snapshot from `paths.backbone`.

Parse the input pack to build the handoff plan:

- group related screens by flow, module, or journey
- treat modal, dialog, and drawer overlays with flow impact as primary screens
- derive supporting frames from documented states, validation rules, list behavior, and feedback surfaces
- verify each group has portal, navigation schema, and active-menu evidence before planning
- run the navigation validator described in `core/behavior/srs.md` when Group C is available
- carry forward the runtime design target `paths.design_doc`

## Step 9.2 - Ask For Or Refresh Runtime DESIGN.md

Apply the design document handling rules in `core/behavior/wireframes.md`.

Minimum decision set: reference direction, visual tone, color, typography, component feel, layout priority, portal navigation schema, active-menu rule, breadcrumb/back behavior, hidden navigation exceptions, hard constraints, and anti-patterns.

Stop if the user declines to approve a design direction.

## Step 9.3 - Wireframe Handoff Preference

If Step 9 runs as part of the lifecycle or SRS pipeline and the user did not explicitly ask to skip or choose screens:

- `lite`: skip unless a screen is explicitly critical.
- `hybrid`: prepare critical-screen constraints automatically.
- `formal`: prepare the full approved screen set.

Persist `paths.wireframe_state` with `State: skipped`, `not-applicable`, `missing`, or `completed` according to `core/behavior/wireframes.md`.

## Step 9.4 - Build Manual Wireframe Handoff Pack And Checklist

For each approved screen group:

1. Read linked use case excerpts, Screen Contract Plus entries, portal snapshots, and Screen Inventory rows from the input pack.
2. Read `paths.design_doc`.
3. Verify constraints against portal ownership, menu schema, active/highlight behavior, actions, flow steps, states, and approved design decisions.
4. Stop if the group lacks a portal snapshot or approved navigation schema.
5. Expand or refresh `paths.wireframe_input` with the full manual-design constraint set.
6. Persist `paths.wireframe_map` as a manual handoff checklist covering screens, supporting states, portal/schema, active-menu evidence, allowed hidden-nav cases, attachment location, labels, actions, validation cues, and navigation regions.

State in both artifacts that BA-kit does not generate the wireframe itself in this flow; the user designs it manually and inserts the final mockup reference into the final document.
