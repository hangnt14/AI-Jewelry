# BA Start Step - SRS Core

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`
- `core/behavior/srs.md`

## Step 8 - Produce SRS Core, Use Cases, And Screen Contract Plus

Produce only the slices justified by mode and artifact gates. Use the accepted scope from the resolved backbone and user stories; do not reopen discovery after the user has approved SRS authoring.

Mode defaults:

- `lite`: run SRS only when explicitly requested.
- `hybrid`: cover complex flows, risky validations, integrations, and delivery-critical screens.
- `formal`: emit the full SRS set.

Upstream context:

- matching intake summary
- backbone features, gates, and risks
- user stories with acceptance criteria
- FRD features and business rules when FRD exists or mode requires it

### Group A - Core

Sections:

- Purpose and Scope
- Overall Description
- Functional Requirements table

Output: `paths.srs_group` with `group=a`

### Group B - Behavioral

Sections:

- Use Case Specifications

Output: `paths.srs_group` with `group=b`

Consistency rules:

- each use case links to user stories and screens
- actor actions use the same terminology as user stories and FRD

### Group C - Screen Contract Plus

Sections:

- Screen Contract Plus
- Screen Inventory

Output: `paths.srs_group` with `group=c`

Before Group C for UI-backed screens, apply the navigation schema gate in `core/behavior/srs.md`. If `paths.design_doc` is missing or unresolved, run Step 8.2 from `srs-wireframes.md` first.

If the required active-menu item or schema route is absent, stop with `MENU_SCHEMA_GAP` instead of guessing a replacement path.

After Group C, run:

```text
python3 scripts/validate-navigation-consistency.py --design {paths.design_doc} --screen-contract {paths.srs_group group=c}
```

Fix blocking navigation validator findings before continuing.

## Step 8.1 - Build Normalized Screen Truth

When the module has UI-backed screens, also compile `paths.screen_field_contract` as the machine-facing field contract consumed by AI tool lanes.

Source inputs:

- `paths.srs_group` with `group=b`
- `paths.srs_group` with `group=c`
- relevant portal snapshot from `paths.backbone`
- relevant FRD and user-story excerpts for traceability

`paths.screen_field_contract` must include:

- one normalized screen entry per UI-backed primary screen
- exact `Portal ID`, `Nav Schema ID`, and `Expected Active Menu Item`
- explicit field allowlist and `no_extra_fields` constraint
- required states and navigation lock
- Display / Behaviour / Validation rule slices, rule codes, and message codes
- one required ASCII coverage row per documented state so screen canon authors cannot skip visual coverage
- short raw source excerpts when a rule cannot be atomized safely without loss
