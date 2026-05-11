# BA-kit Behavior Shards

`core/contract-behavior.md` contains shared behavior every runtime must read.

Command-specific behavior lives in this folder. Runtime adapters must load:

1. `core/contract.yaml`
2. `core/contract-behavior.md`
3. the shard(s) listed in `behavior_shards.<command>`
4. the selected step file
5. templates and upstream artifacts only when the active step needs them

Shard files are policy overlays. They must not redefine literal paths or thresholds from `core/contract.yaml`.
