# BA Start Step - Status

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`

## Discovery Strategy: Canonical-Summary-First

Status must emit a compact, deterministic checklist without broad artifact reads.

Resolution order:
1. If a current package snapshot exists at `plans/{slug}-{date}/02_backbone/package-snapshot.md`,
   read it and derive artifact presence directly from its `artifacts` list.
2. Otherwise, resolve artifact existence from filesystem stat checks only (no content reads).
3. Read `paths.project_memory` header fields and `paths.memory_index` for activation state
   and shard freshness only — do not read shard content.

## Memory Read Scope

- **Must read:** `core/contract.yaml`, `core/contract-behavior.md`
- **Snapshot path (preferred):** `plans/{slug}-{date}/02_backbone/package-snapshot.md` when present
- **May read:** `paths.project_memory` header fields, `paths.memory_index` (activation state + shard freshness)
- **Must NOT read:** `log.md` (unless `--audit` flag), `warm/` shards, `cold/`, full backbone, full stories, full SRS

## Scope

Inspect the project set and print artifact status, dates, Project Home, and delegated slices.
Emit a compact canonical summary — no content reads beyond the snapshot or stat checks.

## Prerequisites

- Resolve slug and date using the shared contract.
- If slug or date resolution is ambiguous, stop and ask.

## Output Format

Print a checklist like this:

```text
Project: {slug}
Date set: {date}
Snapshot: current | degraded | absent

[Core]
- [x] PROJECT-HOME.md (BA-facing dashboard) — 2026-03-26
- [x] 01_intake/intake.md — 2026-03-26
- [x] 02_backbone/backbone.md — 2026-03-26

[Module: auth-flow]
- [x] 03_modules/auth-flow/user-stories.md — 2026-03-26
- [ ] 03_modules/auth-flow/srs.md — missing
- [ ] 03_modules/auth-flow/wireframe-input.md — missing

[Compiled]
- [x] 04_compiled/compiled-frd.html — 2026-03-26
- [x] 04_compiled/compiled-srs.html — 2026-03-26

[Designs]
- [ ] designs/{slug}/DESIGN.md — missing
- [!] wireframe handoff — skipped — 2026-03-26

```

Status rules:

- When snapshot is current, derive artifact presence and mtime from snapshot `artifacts` list.
- When snapshot is absent or degraded, derive artifact presence from filesystem stat only.
- For regular artifacts, print `exists` or `missing` with the last-modified date when present.
- For wireframe handoff, print the explicit wireframe state plus the marker date.
- When wireframe handoff is `completed`, also list the detected runtime design file, wireframe input pack, and wireframe map.
- Print compact memory, shard index, activation, owner, freshness, file-back, and packet registry metadata from `paths.project_memory` and `paths.memory_index` only.
- For delegated slices under `paths.delegation_root`, print the tracker state directly and mark `likely stalled` when the last heartbeat exceeds `states.stall_after_minutes`.
- Do not read artifact content to produce this output.
