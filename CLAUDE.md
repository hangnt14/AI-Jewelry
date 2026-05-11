# BA-kit Instructions For Claude Code

## Canonical Sources

- `core/contract.yaml`
- `core/contract-behavior.md` plus the command shard in `core/behavior/` listed by `core/contract.yaml.behavior_shards`
- `skills/ba-start/SKILL.md` - lifecycle stub that dispatches into the active step file

For lifecycle work, read `contract.yaml`, then shared behavior, then only the selected command behavior shard and step file.

For non-trivial BA work, start from `skills/ba-start/SKILL.md` instead of improvising from the prompt alone.

## Core Defaults

- Write BA deliverables in Vietnamese unless the user explicitly requests English.
- Default to `hybrid` mode for solo IT BA work.
- Persist project memory on disk; do not rely on Claude chat memory as the system of record.
- Apply runtime-neutral HITL behavior from `core/contract-behavior.md` and the selected shard.

## Artifact Model

- Project root: `plans/{slug}-{date}/`
- Project Home: `PROJECT-HOME.md`
- Intake and plan: `01_intake/`
- Backbone and memory: `02_backbone/`
- Module artifacts: `03_modules/{module_slug}/`
- Compiled HTML: `04_compiled/`
- Delegation and collaboration: `delegation/`, `COLLAB-HOME.md`, `MODULE-HOME.md`

## Delegation

Use agent roles under `agents/` when delegation improves quality or throughput.

- `requirements-engineer` for backbone, FRD, stories, and selective SRS content
- `ui-ux-designer` for wireframe constraint packs and manual handoff checklists
- `ba-documentation-manager` for validation, quality review, and packaging
- `ba-researcher` for domain research

Pass narrow packets: exact path, write scope, trace IDs, and targeted excerpts.

## BA-Friendly UX

Use `PROJECT-HOME.md` to resume. Lead with friendly labels, then show commands: tao du an moi -> intake; tiep tuc -> next; thay doi -> impact; handoff UI -> wireframes; ban giao -> package.

Route module collaboration NLP to `ba-collab`. Commit/push/PR/merge require explicit approval.
