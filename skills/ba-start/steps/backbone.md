# BA Start Step - Backbone

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`

## Memory Read Scope

- **Must read:** `core/contract.yaml`, `core/contract-behavior.md`, `paths.intake`
- **Must read when it exists:** `paths.plan`
- **Must read when optioning is completed:** the selected option file only
- **May read:** `paths.project_memory`, `paths.memory_index` (navigation only), `paths.memory_hot_vocabulary`, `paths.memory_hot_decisions`
- **Must NOT read:** `log.md`, `cold/`, `warm/` shards

## Governance Gate

Before mutating this artifact:
1. Always verify write authority for the target artifact and its owning memory shard.
2. For first-pass creation (when `paths.backbone` does not yet exist), skip only the impact-receipt requirement.
3. For reruns (artifact already exists): locate the active impact receipt at `paths.impact_receipt` (or the canonical receipt path for this slug/date). If no active receipt exists and `change_class` is not `wording-only`, emit `GOVERNANCE_BLOCK: impact_receipt missing or invalidated` and stop.
4. If either check fails: emit `GOVERNANCE_BLOCK: {reason}` and stop.
5. After mutation completes: offer to file the change into canonical memory using `templates/project-memory-fileback-record-template.md`.

Receipt reference: `templates/impact-receipt-template.md`

## Scope

Run Step 5 only.

## Prerequisites

- Resolve slug and date using the shared contract.
- Require `paths.intake`.
- If intake is missing, print the exact missing path and stop.
- Read `paths.plan` when it exists.
- Run a narrow backbone preflight:
  - read only `paths.intake` and `paths.plan` when it exists
  - do not scan other folders once slug and date are resolved
  - when `paths.plan` records `options status: recommended` or `options status: in-progress`, stop because optioning is unresolved
  - when `paths.plan` records `options status: completed` or `options status: skipped`, treat that as the backbone decision gate
  - require `paths.plan` to state either `options status: skipped`, `options status: completed`, or `options status: not-needed` before proceeding
  - if completed, require a `selected option` AND an active options receipt at `paths.options_receipt`; if the receipt is missing, emit `GOVERNANCE_BLOCK: options_receipt missing` and stop
  - if completed, read only the selected option file as the decision overlay
  - never require `paths.options_root` to exist before honoring the decision-ledger gate
  - options receipt reference: `templates/options-receipt-template.md`

## Output

- `paths.project_home`
- `paths.backbone`
- `paths.backbone_index`
- `paths.project_memory`

## Step 5 - Build the requirements backbone

Create the persisted source-of-truth artifact using [../../../templates/requirements-backbone-template.md](../../../templates/requirements-backbone-template.md).

The backbone must contain:

- scope lock summary
- selected engagement mode (`lite`, `hybrid`, or `formal`)
- business goals and success metrics
- actors and feature map
- system-level portal matrix for UI-backed scope
- FR/NFR draft inventory
- preliminary story map
- UI/screen coverage assessment
- artifact emission gates
- assumptions, risks, and open questions

After writing the backbone, initialize or refresh `paths.project_memory` using [../../../templates/project-memory-template.md](../../../templates/project-memory-template.md).
Also create or refresh `paths.backbone_index` using [../../../templates/backbone-index-template.md](../../../templates/backbone-index-template.md).
Generate the index with `stale_status: unknown`, leave `validated_at` and `validated_by` blank, then run:

```bash
ba-kit validate-index --index-key backbone_index --slug <slug> --date <date> --writeback
```

before any downstream action treats the index as `current`.

Also refresh `paths.project_home` using [../../../templates/project-home-template.md](../../../templates/project-home-template.md) so non-technical BAs can resume without understanding slug/date/module internals.

Project Home refresh must summarize phạm vi đã chốt, điều kiện tiến hành từng tài liệu, bước tiếp theo an toàn, and runtime quick prompts. Apply the wording-layer policy from `core/contract-behavior.md`: replace internal terms (`source of truth`, `decision ledger`, `artifact gate`, `canon`, `compile receipt`, `index`) with the approved Vietnamese labels. It is a dashboard only; do not duplicate full requirements or replace `backbone.md`.

The project memory must persist only the reusable anti-hallucination layer:

- canonical vocabulary and naming
- approved scope, actor, navigation, and rule decisions
- accepted assumptions with triggers for re-validation
- rejected assumptions or false trails that must not reappear
- accepted corrections and push-back triggers

Backbone rules:

- treat the backbone as the primary authoring source after intake
- do not draft FRD, stories, or SRS directly from raw intake once the backbone exists
- when UI-backed scope exists, lock portal ownership and route-group ownership here before any module-level screen work starts
- promote only the selected option's portal/module/actor/constraint decisions
- do not import rejected options or the full comparison into `backbone.md`
- keep the artifact concise and decision-oriented
- treat generated index/state/memory artifacts as `agent_facing` or `machine_facing`; keep them compact and do not duplicate source-of-truth requirement text
- keep `paths.backbone_index` as a navigator only: section names, trace IDs, module/feature hints, and short summaries; do not duplicate full requirement text
- do not self-certify `paths.backbone_index` as `current`; only the validator may promote it from `unknown`
- keep `project-memory.md` runtime-neutral so Claude Code, Codex, and Antigravity can all resume from the same accepted facts
