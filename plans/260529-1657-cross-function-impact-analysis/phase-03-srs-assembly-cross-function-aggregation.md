---
phase: 3
title: "SRS Assembly Cross-Function Aggregation"
status: completed
priority: P2
effort: "1h"
dependencies: [1]
---

# Phase 3: SRS Assembly Cross-Function Aggregation

<!-- Updated: Validation Session 1 — per-UC inline (not standalone section), Step 10.5 numbering -->

## Overview

Extend SRS assembly step (`skills/ba-start/steps/srs-assembly.md`) to inline cross-function declarations into each UC entry in the compiled SRS. Cross-function data stays with its UC in the Use Cases section — no standalone matrix section. Resolve cross-module references using backbone feature IDs. Flag mismatches and pending (TBD) dependencies.

## Requirements

- Functional: Compile step reads `## Cross-Function Impact` from each UC, inlines it into that UC's compiled entry, flags unresolved cross-module refs
- Non-functional: Partial data is OK — Module B not finished yet → TBD entries flagged as pending not errors

## Architecture

### Aggregation Logic

```
For each UC in module:
  Read ## Cross-Function Impact
    → Within Module table → inline as-is (all UCs in same module, fully resolved)
    → Across Modules table → cross-reference with backbone + other modules

For each Across Module entry:
  - "produces for" → check if target module has matching "consumes from"
  - "consumes from" → check if source module has matching "produces for"
  - Match found → mark Resolved
  - No match → mark Pending (not an error — other module may not be authored yet)
  - Conflicting declarations → flag Mismatch

Inline into compiled UC entry (within Use Cases section):
  Append cross-function subsection after the UC's flow/description,
  before the next UC entry.
```

### Compiled SRS Format (per-UC inline)

Each UC entry in the compiled `srs.md` Use Cases section gets a cross-function subsection:

```markdown
##### UC-checkout: Thanh toán đơn hàng

... (existing UC content from source) ...

###### Cross-Function Impact

**Within Module:**
| Direction | UC | Data / State | Type |
|-----------|-----|--------------|------|
| Depends on | UC-cart | cart_id, cart_items | Input |
| Produces for | UC-tracking | order_id, order_status | Output |

**Across Modules:**
| Direction | Target Module | Backbone Ref | Data / State | Type | Status |
|-----------|---------------|-------------|--------------|------|--------|
| Produces for | shipping | FEAT-SHP-01 | order_id, order_status | Output | Pending |
| Consumes from | auth | FEAT-AUTH-03 | user_id, token | Input | Resolved |
```

### Assembly Step Changes

In `skills/ba-start/steps/srs-assembly.md`, insert **Step 10.5** between Step 10.1 (`Produce Shared Traceability And Definitions`) and Step 11 (`Partial Compile And Receipt`):

```
Step 10.5 - Cross-Function Impact Inlining

During UC compilation (Step 11, substep 4 — usecases), for each UC that declares
## Cross-Function Impact:

a. Read Within Module table → inline as-is
b. Read Across Modules table → cross-reference with other modules' declarations:
   - "produces for" entries → check if target module UC declares matching "consumes from"
   - "consumes from" entries → check if source module UC declares matching "produces for"
c. Mark each inter-module edge: Resolved / Pending / Mismatch
d. Add Status column to Across Modules table in compiled output
e. Inline the cross-function subsection into the UC's compiled entry
```

### Cross-Reference Resolution

```text
Module A UC-checkout: "produces for shipping / FEAT-SHP-01 / order_id, order_status"
Module B UC-shipment: "consumes from payment / order_id, order_status"
→ Match on backbone ID FEAT-SHP-01 + data → Resolved

Module A UC-checkout: "produces for shipping / FEAT-SHP-01 / order_id"
Module B: (no matching consume) → Pending

Module A: "produces for shipping / order_id" (type: Output)
Module B: "consumes from payment / order_id" (type: Shared State) → Mismatch
```

## Related Code Files

- Modify: `skills/ba-start/steps/srs-assembly.md`

## Implementation Steps

1. Read current `srs-assembly.md` full file
2. Insert Step 10.5 between Step 10.1 and Step 11
3. Define inlining procedure: read → cross-reference → classify → inline per UC
4. Define mismatch detection rules (same data, different type = mismatch)
5. Define pending vs resolved classification
6. Update Step 11 substep 4 (usecases compilation) to call cross-function inlining
7. Update compile receipt template to include cross-function aggregation status
8. Test with sample data (two UCs with cross-function declarations)

## Success Criteria

- [ ] Step 10.5 exists in srs-assembly.md between Step 10.1 and Step 11
- [ ] Each UC with cross-function declarations gets inline subsection in compiled SRS
- [ ] Within Module table inlined as-is (no cross-referencing needed)
- [ ] Across Module table gets Status column: Resolved / Pending / Mismatch
- [ ] Pending edges are NOT treated as errors (partial data is valid)
- [ ] Mismatch edges flagged with conflict details
- [ ] UCs without cross-function section → no subsection added (no noise)
- [ ] Compile receipt records cross-function inlining status
- [ ] No new section heading added to srs-template.md (per-UC inline, no standalone section)

## Risk Assessment

- **Low risk**: Inline approach is additive — doesn't change existing compile structure, just enriches each UC entry
- UCs without cross-function section → no change to compiled output (graceful degradation)
- Cross-module resolution depends on backbone feature IDs being consistent — if wrong, resolution marks Pending
