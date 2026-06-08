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
- **[BẮT BUỘC]** Immediately after writing `paths.backbone_index`, run `ba-kit validate-index --index-key backbone_index --slug <slug> --date <date> --writeback`. If validation fails, stop. Do not proceed to downstream commands. The PostToolUse hook serves as fallback, but this inline call is the primary enforcement.
- **When UI-backed scope exists:** create `paths.design_doc` and `paths.shared_shell_contract` during backbone. These are system-level artifacts owned by Lead BA.
  - `paths.design_doc` must cover ALL portals from the backbone Portal Matrix, not just one module.
  - `paths.shared_shell_contract` must declare every nav schema, shell variant, and layout variant used by any portal.
  - Module BAs are PROHIBITED from creating new portals, new nav schemas, new shell variants, or new shared components in these files.
  - Module BAs MAY add menu items to an existing nav schema with explicit user confirmation, then flag in review packet.
  - If a module needs a portal not yet in DESIGN.md or shared-shell-contract.md, escalate to Lead BA via `impact`.
- Initialize or refresh project memory from accepted intake/backbone decisions.
- Compact memory (`paths.project_memory`) stores stable vocabulary, approved decisions, accepted assumptions, rejected assumptions, corrections, and push-back triggers.
- Shard memory is optional. If present, `paths.memory_index` is a bounded navigator and must not become a second monolith.
- `log.md` is optional chronology support and excluded from normal command reads.
- `cold/` is never loaded by default.
