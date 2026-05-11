# Impact Behavior

## Read Scope

- Must read: `core/contract.yaml`, `core/contract-behavior.md`, `paths.intake`, `paths.backbone_index` when present, and `paths.backbone`.
- May read: `paths.project_memory`, `paths.memory_index`, hot shards, selected warm module shard, relevant downstream indexes and artifacts.
- Must not read: `cold/` unless escalated.
- `log.md` may be read only for explicit audit or recent-history requests.

## Routing And Scope

- `impact` is analysis-only until the user approves a mutating rerun path.
- Map each change to the narrowest owning source-of-truth layer: intake/scope lock, backbone, stories, SRS, or wireframes.
- Prefer stable IDs and sections over whole-file rewrites.
- When the change affects UI information architecture or active-menu behavior, include a wireframes follow-up route.
- Emit exact stale artifact paths and the command needed to refresh them.

## Broad-Read Exception

`impact` is the only command that may read across warm module shards by default when Modular or Program activation is detected. Use `paths.memory_index` first and read only routed shards.

## Governance And File-Back

- Verify write authority before recommending mutation.
- Lead BA approves global hot shards, cross-module file-back, and index changes.
- Module owner approves module-local warm shard file-back.
- End-user approval is required when filed-back content changes accepted business scope or policy.
- Ambiguous classification forces explicit end-user approval before file-back.
- Command-level approval alone is not sufficient for file-back.

Filed-back memory items must carry source artifact, source IDs, promotion target, approver, role, approval time, approval basis, approval trigger, impact reference, and supersession fields.

Before mutating `backbone`, `frd`, `stories`, `srs`, or `wireframes`, confirm an approved impact run unless this is first-pass backbone creation or an explicitly approved wording-only rerun. If validation fails, emit `GOVERNANCE_BLOCK: {reason}` and stop.
