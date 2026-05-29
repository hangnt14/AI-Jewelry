---
phase: 2
title: "QC UC Review KA8 Enhancement"
status: completed
priority: P2
effort: "1h"
dependencies: [1]
---

# Phase 2: QC UC Review KA8 Enhancement

## Overview

Update `qc-uc-review` scoring rubric KA #8 (Functional Integration Analysis, 9pts) to consume the new `## Cross-Function Impact` UC section. Current KA #8 sub-items (Impact Analysis, Data Consistency, Section-level error isolation) are scored without cross-function declarations — reviewers currently infer dependencies from UC text. After Phase 1, reviewers can check the explicit dependency tables.

## Requirements

- Functional: KA #8 scoring should check for presence and completeness of `## Cross-Function Impact` section
- Non-functional: Backward compatible — UCs without cross-function section still scorable (just lose points on KA #8)

## Architecture

### Current KA #8 (9pts, Critical)

| Sub-item | Clear | Partial | Current Criteria |
|---|:---:|:---:|---|
| 8.1 Impact Analysis | 3 | 1 | Change in one function affects other functions |
| 8.2 Data Consistency | 3 | 1 | Data source → consumer; sync rules |
| 8.3 Section-level error isolation | 3 | 1 | One section failing does not block other sections |

### Proposed KA #8 Update

Keep current sub-items but add cross-function evidence as primary scoring input:

| Sub-item | Clear | Partial | Updated Criteria |
|---|:---:|:---:|---|
| 8.1 Impact Analysis | 3 | 1 | UC declares within-module dependencies (Depends on / Produces for) with data/state; reviewer can trace change propagation |
| 8.2 Data Consistency | 3 | 1 | UC declares across-module dependencies (Produces for / Consumes from) with backbone refs; data source→consumer chain traceable |
| 8.3 Section-level error isolation | 3 | 1 | UC declares Shared State entities; conflicting read/write access identifiable |

**New Clear criteria for 8.1:**
- Within Module table has at least one entry OR explicit "None" marker
- Each entry lists specific data/state items (not vague "order data")
- Dependency type matches direction (Depends on → Input, Produces for → Output)

**New Clear criteria for 8.2:**
- Across Modules table present (even if empty — "None" is valid)
- Each entry references a backbone feature ID (not a vague module name)
- Data/State column is specific and matches backbone entity names

**New Clear criteria for 8.3:**
- Shared State entries declare which entity and which UCs share access
- Conflicting access (read vs write) is detectable from declarations

### SKILL.md Changes

Add to the evidence scanning step:
- Read `## Cross-Function Impact` from each UC file
- For 8.1: Check Within Module table completeness
- For 8.2: Check Across Module table backbone references
- For 8.3: Check Shared State declarations

## Related Code Files

- Modify: `skills/qc-uc-review/references/scoring-rubric.md`
- Modify: `skills/qc-uc-review/SKILL.md`

## Implementation Steps

1. Read current `scoring-rubric.md` KA #8 section
2. Update sub-item criteria to reference `## Cross-Function Impact` section
3. Add Clear/Partial/Missing definitions for cross-function declarations
4. Update `SKILL.md` to scan cross-function section during evidence collection
5. Add cross-function gap pattern to Common Gap Patterns table
6. Verify scoring still works for UCs without cross-function section (backward compat)
7. Run a test audit on a sample UC to validate new scoring

## Success Criteria

- [ ] KA #8.1 Clear criteria reference Within Module dependency table
- [ ] KA #8.2 Clear criteria reference Across Module dependency table + backbone refs
- [ ] KA #8.3 Clear criteria reference Shared State declarations
- [ ] UCs without `## Cross-Function Impact` section score Partial on KA #8 (not auto-fail)
- [ ] SKILL.md evidence collection step includes cross-function section scan
- [ ] New gap pattern added for missing cross-function declarations

## Risk Assessment

- **Medium risk**: Scoring changes can shift audit results. Mitigation: backward-compatible — missing section = Partial, not Missing
- Existing audit reports not retroactively affected
