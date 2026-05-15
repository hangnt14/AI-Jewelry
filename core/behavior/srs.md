# SRS Behavior

## Read Scope

- Must read: `core/contract.yaml`, `core/contract-behavior.md`, `paths.backbone_index`, `paths.stories_index`, and `skills/ba-start/steps/srs.md`.
- May read: targeted `paths.backbone` and `paths.stories` sections, `paths.srs_index` when refreshing, `paths.project_memory` or hot shards, module warm shard, and `paths.frd` when it exists.
- Must not read: `log.md`, `cold/`, other module shards, full `paths.backbone`, or full `paths.stories` when indexes are current.

Re-entry after long sessions, reruns, or host auto-compact still starts with `paths.backbone_index`, then `paths.stories_index`, before reopening targeted source sections.

## Grouped Execution

- Run SRS in groups to avoid loading or writing the full artifact at once.
- Group A: core purpose, overall description, functional requirements.
- Group B: use case specifications.
- Group C: Screen Contract Plus and Screen Inventory.
- Group D: technical/NFR/API/data slices only when justified.
- Group E: final screen descriptions after wireframe handoff is resolved.
- Group F: validation, glossary, and traceability.
- Assemble inline after all required groups are verified.

When SRS writes or refreshes `paths.srs_index`, generate it with `stale_status: unknown`, leave `validated_at` and `validated_by` blank, and run producer-side validation before any downstream routing treats the index as current.

## Navigation And Screen Contract Rules

- Before Group C for UI-backed screens, require approved `paths.design_doc` with a Navigation Schema for every portal used by the module.
- Treat `paths.design_doc` Navigation Schema as source of truth for `Nav Schema ID`, menu labels, and allowed active-menu paths.
- Copy `Expected Active Menu Item` exactly from an allowed menu item/path in the matching schema.
- If a needed item is absent, emit `MENU_SCHEMA_GAP: {screen_id} needs {active_item} in {portal_id}/{nav_schema_id}` and stop.
- Every screen in the same `Portal ID` must reuse the same `Nav Schema ID` unless an explicit exception is declared.
- Overlay screens inherit the parent portal unless an explicit cross-portal transition is documented.
- If modal, dialog, drawer, or overlay screens hide global navigation, set `Navigation Region Visible` to `No` and state the exception reason.
- Primary screens must link to use cases and user stories and define portal, role, nav schema, active menu, navigation visibility, breadcrumbs/back behavior, entry/exit conditions, actions, and states.

Run `python3 scripts/validate-navigation-consistency.py --design {paths.design_doc} --screen-contract {paths.srs_group group=c}` after Group C and before Group E when UI-backed screens exist. Treat `NAV_SCHEMA_MISMATCH`, `MENU_SCHEMA_MISMATCH`, and `MENU_ACTIVE_MISSING` as blocking.

## Wireframe Handoff Gates

- If `paths.design_doc` is missing or unresolved, run Step 8.2 from `srs-wireframes.md` and stop if the user does not approve the design direction.
- Build `paths.wireframe_input` after Groups B and C from exact use case, screen contract, portal, navigation, and trace excerpts.
- Manual wireframe insertion is out-of-band; do not block final screen descriptions on an attached mockup.
- If IA or menu behavior must change after Group C, route through `impact` instead of silently rewriting Group E.
