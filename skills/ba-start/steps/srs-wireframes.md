# BA Start Step - SRS Wireframes

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`
- `core/behavior/srs.md`
- `core/behavior/wireframes.md`

## Step 8.2 - Capture Design Decisions And Persist Runtime DESIGN.md

Before BA-kit writes Screen Contract Plus for UI-backed screens or prepares a wireframe handoff pack, ask the user to approve the project runtime `DESIGN.md` direction.

Decision intake must cover reference direction, visual tone/density, color and contrast, typography, component feel, layout priority, portal navigation schema, active-menu rule, breadcrumb/back behavior, hidden navigation exceptions, hard constraints, and anti-patterns.

If `paths.design_doc` already exists, ask whether to reuse it, refresh it, or stop. If no file exists or refresh is approved, synthesize it from approved decisions using [../../../templates/design-md-template.md](../../../templates/design-md-template.md). Stop if design decisions remain unresolved.

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

Run the standalone wireframe workflow from [wireframes.md](./wireframes.md), using the same slug, date, and module.

Mode defaults inside the SRS pipeline:

- `lite`: skip wireframe handoff unless explicitly requested.
- `hybrid`: prepare critical-screen wireframe constraints first.
- `formal`: prepare the full approved screen set.

## Step 10 - Produce Final Screen Descriptions

After Step 9 resolves, expand final screen descriptions from Use Case Specifications, Screen Contract Plus, `paths.wireframe_input`, `paths.wireframe_map`, and supporting frame inventory.

If wireframes are `skipped` or `not-applicable`, expand screen descriptions from use cases and Screen Contract Plus only. Manual mockup insertion into the final document is out of band.

Group E rules:

- enrich the pre-wireframe screen spec; do not redefine portal ownership
- do not change `Nav Schema ID`, `Expected Active Menu Item`, or active/highlight behavior
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
