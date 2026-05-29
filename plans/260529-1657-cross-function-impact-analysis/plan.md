---
title: "Cross-Function Impact Analysis Implementation"
description: "Implement cross-function dependency tracking in BA-kit UC template, QC review, SRS assembly, impact analysis, and bridge export."
status: completed
priority: P2
branch: "main"
tags: [ba-kit, cross-function, dependency, qc-kit, traceability]
blockedBy: []
blocks: []
created: "2026-05-29T09:59:06.935Z"
createdBy: "ck:plan"
source: skill
---

# Cross-Function Impact Analysis Implementation

## Overview

Implement UC-level cross-function impact declarations per design in `docs/cross-function-impact-analysis-note.md`. Add `## Cross-Function Impact` section to UC template with within-module and across-module dependency tables. Update qc-uc-review KA #8 scoring to consume these declarations. Extend SRS assembly to inline cross-function data per-UC in compiled output. Give ba-impact full cross-function propagation awareness. Wire cross-function data into the ba-qc-export bridge.

## Source Design

- `docs/cross-function-impact-analysis-note.md` — authoritative design
- `docs/ba-qc-export-bridge-note.md` — bridge export spec (cross-function is known gap)

## Phases

| Phase | Name | Status | Depends On |
|-------|------|--------|------------|
| 1 | [UC Template Cross-Function Section](./phase-01-uc-template-cross-function-section.md) | Completed | — |
| 2 | [QC UC Review KA8 Enhancement](./phase-02-qc-uc-review-ka8-enhancement.md) | Completed | Phase 1 |
| 3 | [SRS Assembly Cross-Function Aggregation](./phase-03-srs-assembly-cross-function-aggregation.md) | Completed | Phase 1 |
| 4 | [BA Impact Cross-Function Awareness](./phase-04-ba-impact-cross-function-awareness.md) | Completed | Phase 1 |
| 5 | [Bridge Export Cross-Function Data](./phase-05-bridge-export-cross-function-data.md) | Completed | Phase 1, Phase 3 |

## Dependencies

- Phase 1 is foundation — all other phases depend on the template section existing
- Phase 2 (QC review) can run in parallel with Phases 3-5
- Phase 3 (SRS assembly) must complete before Phase 5 (bridge export)
- Phase 4 is independent after Phase 1

## Files Affected

| File | Phase | Action |
|------|-------|--------|
| `templates/usecase-item-template.md` | 1 | Add `## Cross-Function Impact` section |
| `skills/qc-uc-review/references/scoring-rubric.md` | 2 | Update KA #8 sub-items |
| `skills/qc-uc-review/SKILL.md` | 2 | Add cross-function evidence scanning |
| `skills/ba-start/steps/srs-assembly.md` | 3 | Add cross-function aggregation step |
| `skills/ba-impact/SKILL.md` | 4 | Add cross-function propagation awareness |
| `core/behavior/impact.md` | 4 | Add dependency graph traversal |
| `docs/ba-qc-export-bridge-note.md` | 5 | Update section mapping for cross-function |

## Validation Log

### Session 1 — 2026-05-29
**Trigger:** `/ck:plan validate` after plan creation
**Questions asked:** 4

#### Questions & Answers

1. **[Architecture]** Where should cross-function dependencies appear in the compiled SRS?
   - Options: New section | Per-UC inline | Both matrix + inline
   - **Answer:** Per-UC inline
   - **Rationale:** Cross-function data stays with its UC in the Use Cases section. No standalone matrix section needed.

2. **[Scope]** Should the compile step produce a standalone module-level dependency graph?
   - Options: Yes, generate | No, keep in matrix only | Defer
   - **Answer:** No, keep in matrix only
   - **Rationale:** Per-UC inline is sufficient. No separate graph artifact.

3. **[Architecture]** Should ba-impact consume cross-function declarations for automated change impact propagation?
   - Options: Yes, full propagation | Yes, surface only | Defer
   - **Answer:** Yes, full propagation
   - **Rationale:** Core value of cross-function data is automated impact tracing when UCs change.

4. **[Architecture]** Phase 3 step numbering fix approach?
   - Options: Fix to match actual steps | Renumber srs-assembly.md
   - **Answer:** Fix to match actual steps
   - **Rationale:** srs-assembly.md uses Step 10.1 and Step 11. Insert Step 10.5 between them.

#### Confirmed Decisions
- Cross-function in compiled SRS: per-UC inline (not standalone section)
- No standalone module-level dependency graph artifact
- ba-impact: full propagation with downstream/upstream tracing
- srs-assembly step: insert as Step 10.5 between Step 10.1 and Step 11

#### Action Items
- [x] Update Phase 3: change from standalone section to per-UC inline aggregation
- [x] Update Phase 3: fix step numbering to Step 10.5
- [x] Remove `templates/srs-template.md` from Files Affected (no new section heading)
- [x] Confirm Phase 4 already plans full propagation (no change needed)

#### Impact on Phases
- Phase 3: Architecture changed (per-UC inline, step 10.5), risk reduced
- Phase 4: Confirmed, no changes needed
- Phase 5: Per-UC format already matches, no changes needed

### Verification Results
- **Tier:** Full (5 phases)
- **Claims checked:** 15
- **Verified:** 13 | **Failed:** 1 | **Unverified:** 1

#### Failures
1. [Fact Checker] Phase 3 step numbering: says "between steps 4 and 5" but `skills/ba-start/steps/srs-assembly.md:8` uses "Step 10.1" and "Step 11" — FIXED to Step 10.5

#### Verified Claims (key)
- `templates/usecase-item-template.md` exists, has Postconditions and Diagram sections
- `skills/qc-uc-review/references/scoring-rubric.md` exists, KA #8 is 9pts (design note says 20pts — plan corrected)
- `skills/ba-start/steps/srs-assembly.md` exists, Steps 10.1 and 11
- `core/behavior/impact.md` exists
- `templates/srs-template.md` exists (no longer needed for Phase 3)
- `skills/ba-qc-export/` does not exist (Phase 5 correctly marks as Create)
- `cross_module_dependency` signal in `contract.yaml:445` — dormant, no producer

### Whole-Plan Consistency Sweep
- Files reread: plan.md, phase-01, phase-02, phase-03, phase-04, phase-05
- Decision deltas checked: 4 (per-UC inline, no graph, full propagation, step 10.5)
- Reconciled stale references: 2 (templates/srs-template.md removed from Files Affected, overview updated to "inline" wording)
- Unresolved contradictions: 0

## Open Questions (resolved in validation)

- ~~Does cross-function aggregate into compiled SRS as dependency matrix or per-UC section?~~ → **Per-UC inline** (Session 1)
- ~~Should `ba-impact` consume this for automated change impact analysis?~~ → **Yes, full propagation** (Session 1)
- ~~Does `qc-uc-review` need KA #8 scoring adjustment?~~ → **Yes, see Phase 2** (design note confirmed)
- ~~Should compile step produce module-level dependency graph?~~ → **No, per-UC inline sufficient** (Session 1)
