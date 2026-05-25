# BA Start Step - SRS Wireframes

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`
- `core/behavior/srs.md`
- `core/behavior/wireframes.md`

## Step 8.2 - Capture Design Decisions And Persist Runtime DESIGN.md

Skip this step when reverse mode is the active lane. Reverse-backed SRS work must use reverse evidence,
not `DESIGN.md`, as the blocking prerequisite.

Before BA-kit writes Screen Contract Plus for UI-backed screens or prepares any downstream ASCII/Figma or legacy manual handoff output, ask the user to approve the project runtime `DESIGN.md` direction.

Decision intake must cover reference direction, visual tone/density, color and contrast, typography, component feel, layout priority, portal navigation schema, active-menu rule, breadcrumb/back behavior, hidden navigation exceptions, hard constraints, and anti-patterns.

If `paths.design_doc` already exists, ask whether to reuse it, refresh it, or stop. If no file exists or refresh is approved, synthesize it from approved decisions using [../../../templates/design-md-template.md](../../../templates/design-md-template.md). Stop if design decisions remain unresolved.
Treat `paths.design_doc` as the visual-direction artifact. Shared portal/navigation ownership is moving into `paths.shared_shell_contract` and `paths.shared_shell_index`.

## Group D - Technical

Sections:

- Non-functional requirements
- Data flow diagrams
- ERD
- API specifications
- Constraints

Output: `paths.srs_group` with `group=d`

Produce Group D only when integrations, NFR exposure, data modelling, API handoff, or vendor/governance needs justify it.

## Step 9 - Prepare Manual Wireframe Handoff

Skip this step when reverse mode is the active lane. Reverse mode treats wireframes as `not-applicable`.

Run the standalone wireframe workflow from [wireframes.md](./wireframes.md), using the same slug, date, and module.
Default execution lane stays `manual`. AI-assisted lanes are opt-in and must consume `paths.screen_field_contract`, not raw SRS prose, as the hard-control artifact.
During migration, the manual lane remains transitional only; canon screen/use case/data sources remain the source of truth.

Mode defaults inside the SRS pipeline:

- `lite`: skip wireframe handoff unless explicitly requested.
- `hybrid`: prepare critical-screen wireframe constraints first.
- `formal`: prepare the full approved screen set.

The target future-state flow is:
- canonical screen/use case/data artifacts authored first
- ASCII wireframes generated from screen canon
- Figma sync run as a separate consumer skill
- compiled `paths.srs` refreshed after canon changes

## Step 10 - Produce Final Screen Descriptions

After Step 9 resolves, expand final screen descriptions from Use Case Specifications, Screen Contract Plus, and the canonical module screen/use case sources. During the migration window, `paths.wireframe_input` and `paths.wireframe_map` may still enrich the result for legacy runs.

If wireframes are `skipped` or `not-applicable`, expand screen descriptions from use cases, Screen Contract Plus, and canonical screen sources only. Manual mockup insertion into the final document is out of band.
If reverse mode is active, expand screen descriptions from reverse evidence, promoted claims, and Screen Contract Plus only.

Group E rules:

- enrich the pre-wireframe screen spec; do not redefine portal ownership
- do not change `Nav Schema ID`, `Expected Active Menu Item`, or active/highlight behavior
- treat compiled `paths.srs` as a deliverable assembled from canon sources, not the primary edit surface
- if IA or menu behavior must change, route through `impact`
- run the navigation validator described in `core/behavior/srs.md` before writing Group E when UI-backed screens exist

Output: `paths.srs_group` with `group=e`

Screen field table format:

| Ten truong (Field Name) | Loai truong (Field Type) | Mo ta (Description) |
| --- | --- | --- |
| [Field] | [Type] | **Display Rules:** [visibility, defaults, read-only conditions, formatting] |
| | | **Behaviour Rules:** [on-change actions, auto-fill, cascading, navigation triggers] |
| | | **Validation Rules:** [required, format, range, cross-field, error message triggers] |
| | | **Rule Codes:** [CR-DIS-01, CR-VAL-01, v.v.] |
| | | **Message Codes:** [MSG-ERR-01, MSG-SUC-01, v.v.] |
