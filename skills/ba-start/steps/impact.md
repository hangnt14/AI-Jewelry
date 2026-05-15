# BA Start Step - Impact

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`

## Memory Read Scope

- **Must read:** `core/contract.yaml`, `core/contract-behavior.md`, `paths.intake`, `paths.backbone`
- **May read:** `paths.project_memory`, `paths.memory_index`, `paths.memory_hot_*`, selected `warm/` shard; downstream artifacts (frd, stories, srs, wireframes); `log.md` only when user requests audit
- **Must NOT read:** `cold/` (unless escalated)
- **Note:** `impact` is the only broad-read command.

## Promotion Guidance

After impact analysis and user approval of a rerun path:
1. Document which memory shards/vocabulary/decisions need updating.
2. Prepare file-back record outline using `templates/project-memory-fileback-record-template.md`.
3. Pass outline to user for review before mutating step executes.

## Scope

Run the change-impact triage path only. Do not mutate artifacts.

## Prerequisites

- Resolve slug, date, and module scope through the shared contract.
- Require change input: direct file path or pasted change text.
- Require `paths.intake`. If missing, print exact path and stop.
- Read `paths.backbone` when it exists.
- Read module-scoped downstream artifacts only when relevant to suspected impact:
  `paths.frd`, `paths.stories`, `paths.srs`, `paths.wireframe_input`, `paths.wireframe_map`, `paths.wireframe_state`, `paths.design_doc`, `paths.plan`

## Decision Rules

Treat the current source of truth in this order:

1. `backbone`
2. otherwise `intake`

Reverse lane detection: if `paths.reverse_baseline_lock` exists, apply reverse classification before forward-lifecycle rules.

Classify the change into one or more buckets:

Standard: `wording-only`, `clarification-only`, `backbone-change`, `scope-lock-change`, `ui-impact`

Reverse lane (when reverse_baseline_lock exists):
- `as_built_drift` — code exists but is undocumented or contradicts baseline
- `future_state_request` — desired behavior not yet in code
- `mixed_change` — both; must be split before promotion
- `unverifiable_in_v1` — cannot classify from source alone; do not guess

Never merge `as_built_drift` and `future_state_request` into one rerun recommendation.

Impact anchors:

- intake: business problem, goals, out-of-scope, success metrics
- backbone: scope lock summary, feature map, FR/NFR backbone, actors, portal matrix, story map, UI coverage, artifact gates
- FRD: feature wording, workflows, business rules, integration points
- user stories: story intent and acceptance criteria
- SRS: use cases, Screen Contract Plus, validation rules, screen inventory, final screen descriptions
- wireframe artifacts: manual wireframe constraint pack, runtime `DESIGN.md` assumptions, handoff checklist, wireframe state

## Routing Rules

- Goals, out-of-scope, success metrics, scope decisions → route to `intake` first.
- Feature scope, FR/NFR intent, actors, acceptance-criteria intent, portal ownership, global nav schema → route to `backbone` first.
- Story wording or testable acceptance detail within existing backbone intent → route to `stories`.
- Use case flow, validation behavior, error states, screen behavior within existing backbone+story intent → route to `srs`.
- Screen inventory, state variants, navigation, overlays, field interactions → mark `ui-impact`; include `wireframes` after upstream rerun.
- Never recommend `package` as first remediation step after a real requirement change.

Reverse lane routing (when reverse_baseline_lock exists):
- `as_built_drift` → `ba-start reverse promote --slug <slug> --evidence-ids <ids>`
- `future_state_request` → forward lifecycle (backbone / stories / srs)
- `mixed_change` → `ba-start reverse impact --slug <slug> --evidence-ids <ids>` to split first
- `unverifiable_in_v1` → surface to user; do not guess lane

## Output

Print: project/date, detected step, change type, source of truth, affected_node_ids, owner_artifact, stale_artifacts, read_escalation, affected/unaffected artifacts, recommended path, exact commands, focused questions only.

```text
Impact Delta

affected_node_ids: [scope | actor | FR/NFR | story | UC | SCR | rule | message IDs]
owner_artifact: [intake | backbone | stories | srs | wireframe artifacts | reverse_evidence_ledger]
stale_artifacts: [indexes or artifacts that must be refreshed by the rerun]
read_escalation: [none | READ_ESCALATION: impact read {path} due to {reason}]
reverse_lane: [absent | as_built_drift | future_state_request | mixed_change | unverifiable_in_v1]
```

Rules:
- Map change to `affected_node_ids` before opening broad downstream context.
- Use `owner_artifact` to choose the smallest rerun path.
- Include index files in `stale_artifacts` when a CR can invalidate backbone_index, stories_index, srs_index, wireframe_input, or wireframe_map.
- If CR cannot be mapped to a node, emit `read_escalation` and ask focused questions.
- When `reverse_lane` is not `absent`, print the exact reverse lane command before forward lifecycle commands.
- Never omit `reverse_lane` field when `reverse_baseline_lock` exists.