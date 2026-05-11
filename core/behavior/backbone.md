# Backbone Behavior

## Read Scope

- Must read for `options`: `core/contract.yaml`, `core/contract-behavior.md`, `paths.intake`, and `paths.plan` when present.
- Must read for `backbone`: `core/contract.yaml`, `core/contract-behavior.md`, `paths.intake`, and `paths.plan` when present.
- May read: selected option file only when optioning is completed, `paths.project_memory`, `paths.memory_index` as navigator, hot vocabulary and decisions shards.
- Must not read: `log.md`, `cold/`, unrelated `warm/` shards, downstream module artifacts.

## Options Decision-Ledger Gate

Treat `paths.plan` as the execution decision ledger whenever intake seeds options status, whether or not `paths.options_root` exists.

- Intake may seed only `recommended` or `not-needed`.
- Recommendation strength stays in prose, not a parallel enum.
- `options` moves lifecycle to `in-progress`, then `completed` when `selected option` is recorded, or `skipped` when the user explicitly bypasses optioning.
- `backbone` must stop when ledger status is `recommended` or `in-progress`.
- `backbone` may proceed only when the ledger records `not-needed`, `selected option` (`completed`), or `skipped`.
- `paths.options_root` is evidence that option artifacts exist; it does not control whether backbone gating applies.
- For `options`, `--select <option-id>` and `--skip` are mutually exclusive.

Stop when the requested option file does not exist, multiple options exist without approved selection/skip, or a selection names an unknown option id.

## Backbone And Memory

- Backbone creation is the first source-of-truth consolidation after intake and accepted options.
- First-pass backbone creation may skip impact/governance pre-mutation checks because no accepted backbone exists yet.
- Refresh `paths.backbone_index` after backbone creation or approved rerun.
- Initialize or refresh project memory from accepted intake/backbone decisions.
- Compact memory (`paths.project_memory`) stores stable vocabulary, approved decisions, accepted assumptions, rejected assumptions, corrections, and push-back triggers.
- Shard memory is optional. If present, `paths.memory_index` is a bounded navigator and must not become a second monolith.
- `log.md` is optional chronology support and excluded from normal command reads.
- `cold/` is never loaded by default.
