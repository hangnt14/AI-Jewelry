# BA Start Step - SRS Assembly

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`

## Step 10.1 - Produce validation pack

Produce the validation and traceability pack from the completed SRS sections. Prefer `ba-documentation-manager` ownership when delegated.

Sections:

- Test Cases
- Glossary
- Traceability cross-references

Output: `paths.srs_group` with `group=f`

## Step 11 - Assembly and quality review

The orchestrator assembles the final SRS inline. Do not delegate assembly. In the canon-first flow, `paths.srs` is a compiled deliverable assembled from canonical module sources and routing indexes.

Assembly procedure:

1. Write the SRS skeleton to `paths.srs` using the `srs-template.md` heading structure.
2. Resolve `paths.srs_index` first. Use its registries to locate canonical `usecases/*.md`, `screens/*.md`, optional `data/erd.md`, and `flows/*.md`.
3. Append group fragments (`A -> B -> C -> D -> E -> F`) into the matching compiled sections when they are emitted.
4. For canon-first sections, compile near-verbatim from source files:
   - use case canon files into the Use Cases section, including the primary diagram
   - screen canon files into Screen Descriptions, including state visual coverage, overlay context, ASCII wireframes, and Figma frame map
   - data/ERD and flow canon files into the Diagrams/Data Model sections
   - `srs-index.md` registries into inventory and traceability summaries
5. Write `paths.srs_compile_receipt` using `templates/srs-compile-receipt-template.md`, recording source paths and hashes used for the compile.
6. After all sections are assembled, run a cross-artifact consistency check on the file on disk:
   - every UC step maps to a screen field or action and vice versa
   - Screen Contract Plus entries have matching canon screen sources and final screen descriptions
   - UC actor actions use the same wording as screen User Actions
   - UC system responses match screen Behaviour Rules
   - alternate flows are reflected in screen error states
   - every UI-backed screen canon file has `ascii_status: current` and required `## ASCII Wireframe` state subsections
   - user story acceptance criteria are covered by UC postconditions and screen validation rules
   - final screen descriptions do not redefine `Portal ID`, `Nav Schema ID`, or active/highlight behavior captured in Group C, screen canon, or the shared shell contract
   - run `python3 scripts/validate-navigation-consistency.py --design {paths.design_doc} --screen-contract {paths.srs_group group=c}` when UI-backed screens and `paths.design_doc` exist
   - treat `MENU_SCHEMA_MISMATCH`, `NAV_SCHEMA_MISMATCH`, and `MENU_ACTIVE_MISSING` as blocking before final assembly is accepted
7. Resolve placeholder references and ID conflicts inline.
8. Verify every SCR and UC traces back to user stories.
9. Do not delete canonical source files. Delete group fragments only after the compiled SRS and receipt are verified.

Execution order:

```text
Group A
  -> Group B
  -> Group D
Group B -> Group C
Group C -> ASCII wireframes
ASCII wireframes -> Group E
Group E -> Group F
Group F -> Canon/index verification -> Assembly -> Compile receipt
```

If a grouped pass fails, retry once. If it still fails, complete that group inline. The merge itself always runs inline.
