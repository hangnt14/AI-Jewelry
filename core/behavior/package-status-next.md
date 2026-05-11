# Package, Status, And Next Behavior

## Read Scope

- `package` must read `core/contract.yaml`, `core/contract-behavior.md`, and `paths.backbone_index` when present.
- `package` may read `paths.stories_index`, `paths.srs_index`, `paths.project_memory` compact summary, and `paths.memory_index` for health overview.
- `package` must not read raw source, full intake, `log.md`, `cold/`, `warm/` shards, or full source-of-truth artifacts for discovery when indexes are current.
- `status` and `next` may read `paths.project_home`, project memory header, and `paths.memory_index` activation/freshness. They must not read `log.md` unless `--audit`, or warm/cold shards by default.

## Package Behavior

- `package` is a validation-and-compile step, not a full rebuild.
- Markdown artifacts remain the source of truth.
- HTML output belongs under `paths.compiled_root`.
- Use indexes first for cross-reference discovery and load full source artifacts only when compilation or validation needs exact content.
- Block package only when wireframe state is `missing` under the shared prerequisite rule.

## Status And Next

- Use one lifecycle status vocabulary: `recommended`, `in-progress`, `completed`, `skipped`, and `not-needed`.
- Do not introduce parallel labels such as `todo`, `doing`, or `done`.
- Treat `paths.project_home` as a BA-facing dashboard for resume/status guidance, not as a source of truth.
- If Project Home conflicts with intake, backbone, or module artifacts, report the conflict and trust the source-of-truth artifact.
- `next` recommends the next command and does not mutate artifacts.
