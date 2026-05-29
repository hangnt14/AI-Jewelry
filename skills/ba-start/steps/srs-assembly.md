# BA Start Step - SRS Assembly

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`

## Step 10.1 - Produce Shared Traceability And Definitions

Produce the shared traceability and definitions artifacts from the completed source set. Prefer `ba-documentation-manager` ownership when delegated.

Outputs:
- `paths.shared_traceability` — backbone → userstories → usecases → screens/SRS source map
- `paths.shared_definitions` — canonical term definitions used across module artifacts

## Step 10.5 - Cross-Function Impact Inlining

During UC compilation (Step 11, substep 4 — usecases), for each UC that declares `## Cross-Function Impact`:

1. Read `### Within Module` table → inline as-is into the UC's compiled entry.
2. Read `### Across Modules` table → cross-reference with other modules' declarations:
   - "produces for" entries → check if target module UC declares matching "consumes from"
   - "consumes from" entries → check if source module UC declares matching "produces for"
3. Mark each inter-module edge:
   - Match found on backbone feature ID + matching data/state → **Resolved**
   - No matching declaration in target/source module → **Pending** (other module may not be authored yet)
   - Declarations exist but data/type conflicts → **Mismatch**
4. Add `Status` column to Across Modules table in compiled output.
5. Inline the cross-function subsection into the UC's compiled entry (after UC flow content, before next UC).
6. UCs without `## Cross-Function Impact` → no subsection added (no noise).

Pending edges are NOT errors — partial data is valid when other modules haven't been authored yet.

## Step 11 - Partial Compile And Receipt

The orchestrator compiles `paths.srs` from the source set inline. Do not delegate assembly. `paths.srs` is a compiled deliverable only — never a source of truth.

Assembly procedure:

1. Parse requested compile scope (full / spec / usecases / screens / flows / states / erd / mixed).
2. Identify included sources from `paths.srs_spec`, `paths.usecases_index` + usecase files, `paths.ascii_screen_index` + screen files, `paths.usecase_diagrams`, `paths.srs_flows`, `paths.srs_states`, `paths.srs_erd` as applicable.
3. Write the SRS skeleton to `paths.srs` using the `srs-template.md` heading structure.
4. Compile near-verbatim from source files into the matching sections:
   - `srs/spec.md` → Functional Requirements, NFR, Business Rules
   - `usecases/uc-*.md` → Use Cases section, including UC diagrams
   - `ascii-screen/*.md` → Screen Descriptions, including state visual coverage, overlay context, ASCII wireframes
   - `srs/flows.md` → Data Flow / Module Flow sections
   - `srs/states.md` → State Registry section
   - `srs/erd.md` → ERD section
5. Write `paths.srs_compile_receipt` using `templates/srs-compile-receipt-template.md`, recording:
   - `compile_scope`
   - `requested_sections`
   - `included_sources`
   - `excluded_sources`
   - `source_hashes` for each included source
6. After assembly, run cross-artifact consistency check:
   - every UC step maps to a screen field or action and vice versa
   - UC actor actions use the same wording as screen User Actions
   - UC system responses match screen Behaviour Rules
   - alternate flows are reflected in screen error states
   - every UI-backed screen canon file has `ascii_status: current` and required `## ASCII Wireframe` state subsections
   - user story acceptance criteria are covered by UC postconditions and screen validation rules
   - final screen descriptions do not redefine `Portal ID`, `Nav Schema ID`, or active/highlight behavior
   - run `python3 scripts/validate-navigation-consistency.py --design {paths.design_doc} --screen-contract {ascii_screen_item_1} --screen-contract {ascii_screen_item_2} ...` (pass each individual `ascii-screen/*.md` file, not the index) when UI-backed screens and `paths.design_doc` exist
   - treat `MENU_SCHEMA_MISMATCH`, `NAV_SCHEMA_MISMATCH`, and `MENU_ACTIVE_MISSING` as blocking before assembly is accepted
7. Resolve placeholder references and ID conflicts inline.
8. Verify every SCR and UC traces back to user stories.
9. Do not delete canonical source files.

Execution order:

```text
srs/spec.md
  -> usecases/ + usecases/diagrams.md  (with cross-function impact inlining per Step 10.5)
  -> ascii-screen/ (with ASCII coverage verified)
  -> srs/flows.md (when justified)
  -> srs/states.md (when justified)
  -> srs/erd.md (when justified)
  -> shared/traceability.md + shared/definitions.md
  -> compile to srs.md
  -> write srs-compile-receipt.json
```

If a source file is missing for a requested scope section, stop and route back to the owning step.
