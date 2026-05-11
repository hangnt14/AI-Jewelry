# Module Authoring Behavior

FRD and stories must start from `paths.backbone_index`. If the index is current, read targeted `paths.backbone` sections only.

## Read Scope

- FRD must read: `core/contract.yaml`, `core/contract-behavior.md`, `paths.backbone_index`, and `paths.plan`.
- Stories must read: `core/contract.yaml`, `core/contract-behavior.md`, and `paths.backbone_index`.
- May read: targeted `paths.backbone` sections, `paths.frd` for stories when it exists, `paths.project_memory` or hot vocabulary and decisions shards.
- Must not read: `log.md`, `cold/`, unrelated `warm/` shards, unrelated module artifacts, or full `paths.backbone` when the index is current.

## Authoring Rules

- Keep module-scoped outputs inside `paths.module_root`.
- Use exact module resolution and stop on ambiguity.
- Preserve accepted backbone scope, terminology, gates, and risks.
- Route material scope or requirement corrections through `impact` before mutating accepted downstream artifacts.
- Generated module indexes are navigators only. They must include IDs, source headings, trace hints, counts, freshness, and route hints, not duplicated requirement prose.
- If a required upstream decision is absent or contradictory, stop and route back to the owning step instead of inventing prose.
