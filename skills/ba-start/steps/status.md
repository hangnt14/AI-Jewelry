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
For UI-backed SRS modules, include canon source, compile, and Figma readiness signals from file presence only.

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
- [x] 03_modules/auth-flow/srs-index.md — 2026-03-26
- [x] 03_modules/auth-flow/screens/*.md — 4 file(s)
- [x] 03_modules/auth-flow/usecases/*.md — 3 file(s)
- [ ] 03_modules/auth-flow/data/*.md — missing
- [ ] 03_modules/auth-flow/flows/*.md — missing
- [ ] 03_modules/auth-flow/srs.md — missing
- [!] srs-compile-receipt.json — missing; rerun ba-start srs

[Shared Shell]
- [x] designs/{slug}/DESIGN.md — 2026-03-26
- [x] 02_backbone/shared-shell-contract.md — 2026-03-26
- [x] 02_backbone/shared-shell-index.md — 2026-03-26

[Compiled]
- [x] 04_compiled/compiled-frd.html — 2026-03-26

[Designs]
- [ ] designs/{slug}/DESIGN.md — missing
- [x|!| ] screen canon ASCII — current/missing/stale

[Reverse Lane]  ← omit section when reverse_baseline_lock absent
- [x|!| ] reverse-baseline-lock.json — {scan_timestamp} | absent
- [x|!| ] reverse-index.md — stale_status: {unknown|current|stale} | absent
- [x| ] reverse-focus-excerpts.md — {entry_count} excerpts | absent
- [x| ] reverse-evidence-ledger.md — {total} entries | absent
- [x| ] reverse-drift-state.json — present | absent

```

Status rules:

- Derive artifact presence from snapshot `artifacts` list when current; otherwise filesystem stat only.
- Print `exists` or `missing` with last-modified date. For screen canon ASCII, report current/missing/stale from screen canon validation.
- Report SRS canon directories by markdown file count only; do not read screen/use case content.
- Report `srs-compile-receipt.json` as `current`, `missing`, `stale`, or `not applicable` using file presence and modified times against canon source directories.
- Report shared shell files separately from module SRS files because shell/menu ownership is system-level.
- Report Figma readiness indirectly: current canon sources + current compile receipt + shared shell + `DESIGN.md` present. Actual Figma sync status belongs to the downstream sync report, not `ba-start status`.
- Print compact memory/shard/activation metadata from `paths.project_memory` and `paths.memory_index` only.
- For delegated slices, print tracker state; mark `likely stalled` when heartbeat exceeds `stall_after_minutes`.
- Do not read artifact content to produce this output.

Reverse lane status rules:
- Omit `[Reverse Lane]` when `reverse_baseline_lock` absent (stat only).
- When present: stat checks only — do not open reverse lane files to count entries.
- Mark reverse-index `[!]` when stale_status `unknown` or `stale`; suggest `ba-start reverse --slug <slug>`.
- When evidence counts unknown from stat: print `unclassified: unknown — run ba-start reverse status`.
- When all promoted and none unclassified: `Reverse lane complete. Consider /ba-start backbone --slug <slug>.`
