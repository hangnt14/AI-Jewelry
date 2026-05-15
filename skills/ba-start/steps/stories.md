# BA Start Step - Stories

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`

## Memory Read Scope

- **Must read:** `core/contract.yaml`, `core/contract-behavior.md`, `paths.backbone_index`
- **May read:** targeted `paths.backbone` sections, `paths.plan`, `paths.frd` (when exists), `paths.project_memory` or (`paths.memory_hot_vocabulary` + `paths.memory_hot_decisions`) when shard mode is active
- **Must NOT read:** `log.md`, `cold/`, `warm/` shards, unrelated module shards

## Governance Gate

Before mutating this artifact:
1. **Skip this gate for first-pass creation** (when `paths.stories` does not yet exist).
2. For reruns (artifact already exists): verify write authority and locate the active impact receipt at `paths.impact_receipt`. If no active receipt exists and `change_class` is not `wording-only`, emit `GOVERNANCE_BLOCK: impact_receipt missing or invalidated` and stop.
3. If either check fails on a rerun: emit `GOVERNANCE_BLOCK: {reason}` and stop.
4. After mutation completes: offer to file the change into canonical memory using `templates/project-memory-fileback-record-template.md`.

Receipt reference: `templates/impact-receipt-template.md`

## Scope

Run Step 7 only.

## Prerequisites

- Resolve slug, date, and module using the shared contract.
- Require `paths.backbone`.
- Prefer `paths.backbone_index` for routing. If it is missing and the backbone is large, stop and ask to refresh the index.
- If backbone is missing, print the exact missing path and stop.
- Run a narrow stories preflight:
  - read `paths.backbone_index` first
  - read only targeted `paths.backbone` sections
  - read `paths.plan` only when it adds needed scope context
  - read `paths.frd` only when it already exists and adds needed vocabulary or workflow structure
  - do not scan unrelated module folders once slug, date, and module are resolved

## Output

- `paths.stories`
- `paths.stories_index`

## Step 7 - Produce user stories

Generate Agile user stories from the backbone feature map and FR draft using [../../../templates/user-story-template.md](../../../templates/user-story-template.md):

- Epic and feature breakdown
- User stories with acceptance criteria (Given/When/Then)
- INVEST validation
- Story-to-screen alignment when UI exists

Execution rules:

- Start from `paths.backbone_index`, then the exact targeted backbone sections, plus the exact plan path when genuinely needed.
- Pull the FRD only when it already exists or the current mode requires it.
- If the user already confirmed that story generation should proceed, continue from the resolved backbone instead of reopening discovery.
- Treat generated index/state/memory artifacts as `agent_facing` or `machine_facing`; keep them compact and do not duplicate source-of-truth requirement text.

Save to `paths.stories`.
After generation, create or refresh `paths.stories_index` using [../../../templates/user-stories-index-template.md](../../../templates/user-stories-index-template.md). Keep it as a navigator over epics, stories, acceptance-criteria counts, screen IDs, and source headings.
Generate `paths.stories_index` with `stale_status: unknown`, leave `validated_at` and `validated_by` blank, then run `python3 scripts/validate-index-quality.py --repo . --index-key stories_index --slug <slug> --date <date> --module <module> --writeback` before any downstream routing trusts the index as `current`.
