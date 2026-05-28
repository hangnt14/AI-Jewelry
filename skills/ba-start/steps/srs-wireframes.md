# BA Start Step - SRS Wireframes

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`
- `core/behavior/srs.md`

## Step 8.2 - Capture Design Decisions And Persist Runtime DESIGN.md

Skip this step when reverse mode is the active lane. Reverse-backed SRS work must use reverse evidence,
not `DESIGN.md`, as the blocking prerequisite.

Before BA-kit writes screen canon for UI-backed screens or generates mandatory ASCII wireframes, ask the user to approve the project runtime `DESIGN.md` direction.

Decision intake must cover reference direction, visual tone/density, color and contrast, typography, component feel, layout priority, portal navigation schema, active-menu rule, breadcrumb/back behavior, hidden navigation exceptions, hard constraints, and anti-patterns.

If `paths.design_doc` already exists, ask whether to reuse it, refresh it, or stop. If no file exists or refresh is approved, synthesize it from approved decisions using [../../../templates/design-md-template.md](../../../templates/design-md-template.md). Stop if design decisions remain unresolved.
Treat `paths.design_doc` as the visual-direction artifact. Shared portal/navigation ownership lives in `paths.shared_shell_contract` and `paths.shared_shell_index`.

## Source: srs/flows.md

Output: `paths.srs_flows`

Produce only when module/system flows, cross-module interactions, or data flow diagrams are justified. UC-level diagrams belong in `usecases/diagrams.md`, not here.

## Source: srs/states.md

Output: `paths.srs_states`

Produce the module state registry when the module has meaningful state transitions across screens or use cases.

## Source: srs/erd.md

Output: `paths.srs_erd`

Produce only when data modelling, ERD, or API handoff needs justify it.

## Step 9 - Generate And Validate Mandatory ASCII Wireframes

Skip this step when reverse mode is the active lane. Reverse mode documents existing behavior from evidence and does not generate future-state wireframes.

For every UI-backed primary screen in `paths.ascii_screen_root`, create or refresh the `## ASCII Wireframe` section directly inside the matching `ascii-screen/*.md` file. ASCII wireframes are mandatory review evidence and must be derived from the screen canon itself.

Mode defaults inside the SRS pipeline:

- `lite`: generate ASCII for every UI-backed primary screen that exists in scope.
- `hybrid`: generate ASCII for every UI-backed primary screen and every L3 state.
- `formal`: generate ASCII for the full approved screen set, including supporting states.

Required screen canon result:
- canonical screen/use case artifacts authored first
- `ascii_status: current`
- `## ASCII Wireframe` present
- one ASCII subsection per required state listed in State Visual Coverage
- Figma sync run as a separate consumer skill
- compiled `paths.srs` refreshed after canon changes

## Step 10 - Produce Final Screen Field Contract

After Step 9 resolves, expand final screen field contract from use case canon, screen canon, and backbone.

Manual mockup insertion into the final document is out of band and optional; it never replaces required ASCII in screen canon.
If reverse mode is active, expand screen descriptions from reverse evidence, promoted claims, and screen canon only.

Screen field contract rules:

- enrich the pre-wireframe screen spec; do not redefine portal ownership
- do not change `Nav Schema ID`, `Expected Active Menu Item`, or active/highlight behavior
- treat compiled `paths.srs` as a deliverable assembled from canon sources, not the primary edit surface
- if IA or menu behavior must change, route through `impact`
- run the navigation validator described in `core/behavior/srs.md` before finalizing when UI-backed screens exist

Screen field table format:

| Ten truong (Field Name) | Loai truong (Field Type) | Mo ta (Description) |
| --- | --- | --- |
| [Field] | [Type] | **Display Rules:** [visibility, defaults, read-only conditions, formatting] |
| | | **Behaviour Rules:** [on-change actions, auto-fill, cascading, navigation triggers] |
| | | **Validation Rules:** [required, format, range, cross-field, error message triggers] |
| | | **Rule Codes:** [CR-DIS-01, CR-VAL-01, v.v.] |
| | | **Message Codes:** [MSG-ERR-01, MSG-SUC-01, v.v.] |
