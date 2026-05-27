# Package, Status, And Next Behavior

## Read Scope

- `package` must read `core/contract.yaml`, `core/contract-behavior.md`, and `paths.backbone_index` when present.
- `package` may read `paths.stories_index`, `paths.srs_index`, `paths.project_memory` compact summary, and `paths.memory_index` for health overview.
- `package` must not read raw source, full intake, `log.md`, `cold/`, `warm/` shards, or full source-of-truth artifacts for discovery when indexes are current.
- `status` and `next` may read `paths.project_home`, project memory header, and `paths.memory_index` activation/freshness. They must not read `log.md` unless `--audit`, or warm/cold shards by default.

## Package Behavior

- `package` is a validation-and-compile step, not a full rebuild.
- Markdown canon artifacts remain the source of truth. Compiled `paths.srs` is a deliverable assembled from module canon files and `paths.srs_compile_receipt`.
- HTML output belongs under `paths.compiled_root`.
- Use indexes first for cross-reference discovery and load full source artifacts only when compilation or validation needs exact content.
- Block package when `paths.srs` exists but `paths.srs_compile_receipt` is missing or stale.
- Block package when UI-backed canon screens are missing required ASCII coverage or the compile receipt is stale.

## Status And Next

- Use one lifecycle status vocabulary: `recommended`, `in-progress`, `completed`, `skipped`, and `not-needed`.
- Do not introduce parallel labels such as `todo`, `doing`, or `done`.
- Treat `paths.project_home` as a BA-facing dashboard for resume/status guidance, not as a source of truth.
- If Project Home conflicts with intake, backbone, or module artifacts, report the conflict and trust the source-of-truth artifact.
- `status` must show canon SRS state explicitly: `paths.srs_index`, screen/use case/data/flow source counts, `paths.srs`, and `paths.srs_compile_receipt`.
- `status` must show shared shell state separately: `paths.design_doc`, `paths.shared_shell_contract`, and `paths.shared_shell_index`.
- `next` must recommend `ba-start srs` when canon sources, `srs-index.md`, or the compile receipt are missing/stale.
- `next` must not recommend legacy `wireframes`; missing or stale ASCII coverage is fixed by `ba-start srs`.
- Figma sync readiness is downstream-only: current canon + current compile receipt + shared shell + `DESIGN.md`. Any Figma mismatch belongs in `paths.figma_mismatch_report`, not in canon files.
- `next` recommends the next command and does not mutate artifacts.
