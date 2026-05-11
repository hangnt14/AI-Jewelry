# Runtime-Neutral Token Optimization

BA-kit uses a runtime-neutral read order to keep Codex, Claude Code, and Antigravity aligned while reducing default input surface:

1. `core/contract.yaml`
2. `core/contract-behavior.md`
3. the command behavior shard listed in `behavior_shards.<command>`
4. the selected step file
5. templates and upstream artifacts only when the active step needs them

## Command Read Bundles

| Command | Required behavior shard | Must not load by default |
| --- | --- | --- |
| intake | `core/behavior/intake.md` | memory shards, `log.md`, full raw source when cached summary exists |
| backbone | `core/behavior/backbone.md` | downstream module artifacts |
| impact | `core/behavior/impact.md` | `cold/` unless escalated |
| frd/stories | `core/behavior/module-authoring.md` | unrelated module shards |
| srs | `core/behavior/srs.md` | full backbone/stories when indexes are current |
| wireframes | `core/behavior/wireframes.md` | unrelated module shards |
| package/status/next | `core/behavior/package-status-next.md` | full source-of-truth artifacts when indexes are current |

## Maintainer Notes

- Keep `core/contract.yaml` as the canonical data layer for paths, enums, thresholds, and shard mapping.
- Keep `core/contract-behavior.md` limited to policy that every command must read.
- Put command-specific read scope, gates, and exceptions in the relevant shard.
- Prefer deterministic scripts and `templates/manifest.json` routing metadata over long prose in step files.
- Update `core/token-budget.md` whenever an intentional instruction-surface change changes baselines.

## Acceptance Criteria

- Codex, Claude Code, and Antigravity point to the same contract and shard mapping.
- Runtime adapter files do not duplicate lifecycle policy already present in `core/`.
- `python scripts/check-token-budget.py .` passes on Windows without Bash.
- `scripts/check-token-budget.sh` remains usable on Unix-like environments.
- SRS and wireframe bundles are below the new command-scoped caps.
- No command requires loading unrelated memory shards or full source-of-truth artifacts when a current index exists.
