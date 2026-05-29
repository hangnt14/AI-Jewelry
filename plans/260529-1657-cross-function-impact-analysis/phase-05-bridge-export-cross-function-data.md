---
phase: 5
title: "Bridge Export Cross-Function Data"
status: completed
priority: P3
effort: "1h"
dependencies: [1, 3]
---

# Phase 5: Bridge Export Cross-Function Data

## Overview

Wire cross-function dependency data into the ba-qc-export bridge (currently a design note at `docs/ba-qc-export-bridge-note.md`). The bridge exports BA-kit UC artifacts into QC-kit's expected per-UC format. Cross-function data should appear in QC-kit's §4 Cross-References section and in the per-UC dependency context.

## Requirements

- Functional: Exported UC files include cross-function declarations; only resolved dependencies appear; pending ones become "Expected: TBD"
- Non-functional: QC-kit treats "TBD" entries as known limitations, not gaps

## Architecture

### Current Bridge Section Mapping

| QC-kit section | BA-kit source |
|---------------|---------------|
| §4 Cross-References | FR table, BR table, common rules, message list |

### Updated §4 with Cross-Function Data

| QC-kit section | BA-kit source |
|---------------|---------------|
| §4 Cross-References | FR table, BR table, common rules, message list, **cross-function dependencies** |

### Cross-Function Data in §4

```markdown
### Functional Integration

#### Dependencies (this UC needs)
| Source UC / Module | Data / State | Type | Status |
|--------------------|--------------|------|--------|
| UC-cart / payment | cart_id, cart_items | Input | Resolved |
| FEAT-AUTH-03 / auth | user_id, token | Input | Resolved |

#### Consumers (this UC provides for)
| Target UC / Module | Data / State | Type | Status |
|--------------------|--------------|------|--------|
| UC-tracking / payment | order_id, order_status | Output | Resolved |
| FEAT-SHP-01 / shipping | order_id, order_status | Output | Expected: TBD |
```

### Export Rules

1. **Resolved dependencies** → appear with full details, Status = "Resolved"
2. **Pending "produces for"** → appear as "Expected: TBD" with backbone feature ID — QC-kit treats as known limitation
3. **Pending "consumes from"** → appear as "Expected: TBD" with backbone feature ID
4. **Mismatches** (flagged in Phase 3 compile) → appear with Status = "Mismatch" and conflict description
5. **No cross-function section** → no Functional Integration subsection in §4

### Resolution: Design Note Open Questions

The bridge design note asks whether cross-function data should be in §4 Cross-References or in a standalone per-UC context. Decision: **§4 Cross-References** is the right place — it's already the "everything this UC connects to" section. No new section needed.

## Related Code Files

- Modify: `docs/ba-qc-export-bridge-note.md` (update section mapping + transformation steps)
- Create: `skills/ba-qc-export/SKILL.md` (if bridge skill is being implemented — currently design note only)

## Implementation Steps

1. Read current `docs/ba-qc-export-bridge-note.md`
2. Update §4 Cross-References mapping to include cross-function dependencies
3. Add Functional Integration subsection format to the spec
4. Define export rules for Resolved / Pending / Mismatch statuses
5. Update known gaps section (remove "no cross-function integration analysis" gap)
6. Update transformation Step 7 (cross-references assembly) to include cross-function data
7. If bridge skill SKILL.md exists, update its section mapping
8. Document that QC-kit KA #8 can now be partially satisfied by bridge output

## Success Criteria

- [ ] Bridge spec §4 mapping includes cross-function dependencies
- [ ] Functional Integration subsection format defined
- [ ] Export rules: Resolved → full details, Pending → "Expected: TBD", Mismatch → flagged
- [ ] "No cross-function integration analysis" removed from known gaps
- [ ] Bridge transformation steps include cross-function data assembly
- [ ] QC-kit compatibility: TBD entries treated as known limitations

## Risk Assessment

- **Low risk**: Design note update — no runtime code changed unless bridge skill is being actively implemented
- If bridge skill doesn't exist yet, this phase just updates the design spec
- Cross-function data is additive — doesn't break existing §4 content
