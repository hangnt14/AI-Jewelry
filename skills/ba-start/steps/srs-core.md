# BA Start Step - SRS Core

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`
- `core/behavior/srs.md`

## Step 8 - Produce SRS Source Set

Produce only the slices justified by mode and artifact gates. Use the accepted scope from the resolved backbone and user stories; do not reopen discovery after the user has approved SRS authoring.

Run backbone alignment gate before writing any artifact (see `core/behavior/srs.md`).

Mode defaults:

- `lite`: run SRS only when explicitly requested.
- `hybrid`: cover complex flows, risky validations, integrations, and delivery-critical screens.
- `formal`: emit the full SRS set.

Upstream context:

- matching intake summary
- backbone features, gates, and risks
- user stories via `paths.userstories_index` + targeted `userstory_item` files
- FRD features and business rules when FRD exists or mode requires it

### Source: srs/spec.md

Output: `paths.srs_spec`

Sections:
- Functional Requirements table (FR-{module}-NNN)
- Non-Functional Requirements (NFR-{module}-NNN)
- Business Rules (CR-VAL-NN)
- API/integration constraints when justified
- Data constraints when justified

### Source: usecases/

Output: `paths.usecases_index` + `paths.usecase_item` files + `paths.usecase_diagrams`

Consistency rules:
- each use case links to user stories and screens
- actor actions use the same terminology as user stories and FRD
- UC diagrams go in `usecases/diagrams.md`; module/system flows go in `srs/flows.md`

### Source: ascii-screen/

Output: `paths.ascii_screen_index` + `paths.ascii_screen_item` files

Before authoring UI-backed screens, apply the navigation schema gate in `core/behavior/srs.md`. If `paths.design_doc` is missing or unresolved, run Step 8.2 from `srs-wireframes.md` first.

If the required active-menu item or schema route is absent, stop with `MENU_SCHEMA_GAP` instead of guessing a replacement path.

After screen authoring, run:

```text
python3 scripts/validate-navigation-consistency.py --design {paths.design_doc} \
  --screen-contract {ascii_screen_item_1} --screen-contract {ascii_screen_item_2} ...
```

Pass each individual `ascii-screen/*.md` file (not the index) as a separate `--screen-contract` argument.

Fix blocking navigation validator findings before continuing.

## Step 8.1 - Build Normalized Screen Truth

When the module has UI-backed screens, compile `paths.screen_field_contract` as the machine-facing field contract consumed by AI tool lanes.

Source inputs:

- `paths.usecases_index` + targeted usecase files
- `paths.ascii_screen_index` + targeted screen files
- relevant portal snapshot from `paths.backbone`
- relevant FRD and user-story excerpts for traceability

`paths.screen_field_contract` must include:

- one normalized screen entry per UI-backed primary screen
- exact `Portal ID`, `Nav Schema ID`, and `Expected Active Menu Item`
- explicit field allowlist and `no_extra_fields` constraint
- required states and navigation lock
- Display / Behaviour / Validation rule slices, rule codes, and message codes
- one required ASCII coverage row per documented state
- short raw source excerpts when a rule cannot be atomized safely without loss
