# BA-kit Instructions For Antigravity

## Canonical Sources

- `core/contract.yaml`
- `core/contract-behavior.md` plus the command shard in `core/behavior/` listed by `core/contract.yaml.behavior_shards`
- `skills/ba-start/SKILL.md`

For lifecycle work, read `contract.yaml`, then shared behavior, then only the selected command behavior shard and step file.

For non-trivial BA work, start from `skills/ba-start/SKILL.md` instead of improvising from the prompt alone.

## Automatic BA Routing

| User intent | Read this file | Then do |
| --- | --- | --- |
| Publishing to Notion | `skills/ba-notion/SKILL.md` | publish |
| Module claim/review/conflict/approve/integrate or GitHub handoff | `skills/ba-collab/SKILL.md` | collab |
| Checking status, completion, or missing artifacts | `skills/ba-start/SKILL.md` | run `status` |
| Continuing/resuming a project | `skills/ba-next/SKILL.md` | inspect and recommend |
| Asking what the next BA step should be | `skills/ba-next/SKILL.md` | inspect and recommend |
| Adding, changing, removing, or correcting a requirement or rule | `skills/ba-start/SKILL.md` | run `impact` |
| Naming a lifecycle step | `skills/ba-start/SKILL.md` | run that step |
| Providing raw requirements for a new engagement | `skills/ba-start/SKILL.md` | run lifecycle from intake |
| Other freeform BA requests | `skills/ba-do/SKILL.md` | route |

Prefer `impact` for ambiguous requirement corrections unless the user explicitly asks to update, overwrite, regenerate, or rerun a named artifact.

## Runtime Defaults

- Write BA deliverables in Vietnamese unless the user explicitly requests English.
- Default to `hybrid` mode for solo IT BA work.
- Persist memory in BA-kit artifacts, not runtime chat memory.
- Preserve HITL guarantees from the shared behavior contract and selected command shard.

## Delivery Expectations

- Use `templates/` when a matching template exists.
- Keep final compiled HTML under `plans/{slug}-{date}/04_compiled/`.
- Keep active delegation trackers under `plans/{slug}-{date}/delegation/`.
- Prefer narrow handoff context to sub-agents instead of dumping full upstream documents.

## BA-Friendly Language

Accept Vietnamese first, then show internal step: tao du an -> intake; tiep tuc -> next; thay doi -> impact; handoff UI -> wireframes; ban giao -> package; trang thai -> status.

Collab NLP -> `ba-collab`; GitHub commit/push/PR/merge requires explicit approval.
