---
phase: 4
title: "BA Impact Cross-Function Awareness"
status: completed
priority: P3
effort: "45m"
dependencies: [1]
---

# Phase 4: BA Impact Cross-Function Awareness

## Overview

Extend `ba-impact` skill to consume cross-function declarations when analyzing change impact. When a UC changes, the impact report should trace downstream effects through the dependency graph (who consumes this UC's output?) and upstream effects (what does this UC depend on?).

## Requirements

- Functional: Impact report includes cross-function propagation when changed UC has `## Cross-Function Impact` declarations
- Non-functional: Read-only — ba-impact never mutates artifacts. Cross-function data is read, not written.

## Architecture

### Current Impact Flow

```
Change statement → resolve artifact set → analyze affected sections → recommend commands
```

### Enhanced Impact Flow

```
Change statement → resolve artifact set → analyze affected sections
  → if UC changed, read ## Cross-Function Impact
    → trace downstream: who consumes this UC's output?
    → trace upstream: what does this UC depend on?
  → add cross-function propagation to impact report
  → recommend commands (including cross-module warnings)
```

### Impact Report Addition

Add to impact report output:

```markdown
### Cross-Function Propagation

**Downstream impact** (UCs that consume this UC's output):
| UC | Module | Data / State | Impact |
|----|--------|--------------|--------|
| UC-tracking | payment | order_status | UC-checkout changed order_status format |

**Upstream impact** (UCs this UC depends on):
| UC | Module | Data / State | Impact |
|----|--------|--------------|--------|
| UC-cart | payment | cart_items | If cart_items structure changes, UC-checkout breaks |

**Cross-module warnings:**
- UC-checkout produces `order_id` for module `shipping` (FEAT-SHP-01) — shipping module not yet authored
```

### Resolution Rule Application

- **Intra-module**: Full traceability — impact report lists all affected UCs with specific data/state items
- **Inter-module "produces for"**: Warning-level — consumer may not exist yet, flag as potential impact area
- **Inter-module "consumes from"**: Warning if producer UC changes — upstream change may break this UC's assumptions

## Related Code Files

- Modify: `core/behavior/impact.md`
- Modify: `skills/ba-impact/SKILL.md` (reference update only — behavior lives in core/behavior/)

## Implementation Steps

1. Read current `core/behavior/impact.md`
2. Add cross-function scanning step after artifact resolution
3. For each affected UC, read `## Cross-Function Impact` section
4. Build downstream impact list from "Produces for" entries
5. Build upstream impact list from "Depends on" / "Consumes from" entries
6. Classify each impact: intra-module (certain) vs inter-module (potential)
7. Add cross-function section to impact report output format
8. Update `skills/ba-impact/SKILL.md` if needed

## Success Criteria

- [ ] Impact report includes cross-function propagation when UC has dependency declarations
- [ ] Downstream UCs listed with specific data/state items affected
- [ ] Upstream UCs listed with specific data/state items depended on
- [ ] Cross-module warnings shown for inter-module dependencies
- [ ] UCs without cross-function section → no cross-function section in impact report (no false positives)
- [ ] ba-impact remains read-only (no artifact mutation)

## Risk Assessment

- **Low risk**: Read-only analysis, additive to existing impact report
- Impact report may grow longer for UCs with many dependencies — keep cross-function section collapsible/summary-first
