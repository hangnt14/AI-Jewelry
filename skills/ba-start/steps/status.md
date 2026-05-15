# BA Start Step - Status

This step requires:

- `core/contract.yaml`
- `core/contract-behavior.md`

## Discovery Strategy: Canonical-Summary-First

Status must emit a compact, deterministic checklist without broad artifact reads.

Resolution order:
1. Package snapshot at `plans/{slug}-{date}/02_backbone/package-snapshot.md` when current — derive artifact presence from its `artifacts` list.
2. Otherwise filesystem stat only (no content reads).
3. `paths.project_memory` header and `paths.memory_index` for activation state only.

## Memory Read Scope

- **Must read:** `core/contract.yaml`, `core/contract-behavior.md`
- **May read:** package snapshot, `paths.project_memory` header, `paths.memory_index`
- **Must NOT read:** `log.md`, `warm/` shards, `cold/`, full backbone, stories, SRS

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
- [x] PROJECT-HOME.md — 2026-03-26
- [x] 01_intake/intake.md — 2026-03-26
- [x] 02_backbone/backbone.md — 2026-03-26

[Module: auth-flow]
- [x] 03_modules/auth-flow/user-stories.md — 2026-03-26
- [ ] 03_modules/auth-flow/srs.md — missing

[Compiled]
- [x] 04_compiled/compiled-frd.html — 2026-03-26

[Designs]
- [ ] designs/{slug}/DESIGN.md — missing
- [!] wireframe handoff — skipped — 2026-03-26

[Reverse Lane]  ← omit section when reverse_baseline_lock absent
- [x|!| ] reverse-baseline-lock.json — {scan_timestamp} | absent
- [x|!| ] reverse-index.md — stale_status: {unknown|current|stale} | absent
- [x| ] reverse-focus-excerpts.md — {entry_count} excerpts | absent
- [x| ] reverse-evidence-ledger.md — {total} entries | absent
- [x| ] reverse-drift-state.json — present | absent

```

Status rules:

- Derive artifact presence from snapshot `artifacts` list when current; otherwise filesystem stat only.
- Print `exists` or `missing` with last-modified date. For wireframe handoff, print state + marker date.
- When wireframe handoff `completed`, list runtime design file, wireframe input pack, and wireframe map.
- Print compact memory/shard/activation metadata from `paths.project_memory` and `paths.memory_index` only.
- For delegated slices, print tracker state; mark `likely stalled` when heartbeat exceeds `stall_after_minutes`.
- Do not read artifact content to produce this output.

Reverse lane status rules:
- Omit `[Reverse Lane]` when `reverse_baseline_lock` absent (stat only).
- When present: stat checks only — do not open reverse lane files to count entries.
- Mark reverse-index `[!]` when stale_status `unknown` or `stale`; suggest `ba-start reverse --slug <slug>`.
- When evidence counts unknown from stat: print `unclassified: unknown — run ba-start reverse status`.
- When all promoted and none unclassified: `Reverse lane complete. Consider /ba-start backbone --slug <slug>.`
