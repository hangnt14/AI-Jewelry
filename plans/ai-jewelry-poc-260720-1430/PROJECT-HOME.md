---
type: project-home
status: in-progress
created: 2026-07-20
updated: 2026-07-20
---

# AI Jewelry Design Assistant — PoC

**Slug:** ai-jewelry-poc | **Date:** 260720-1430 | **Mode:** hybrid | **Owner:** @hangnt14

## Trạng thái lifecycle

| Bước | Trạng thái | File |
| --- | --- | --- |
| 1. Intake | completed | [01_intake/intake.md](01_intake/intake.md) |
| 2. Backbone | completed | [02_backbone/backbone.md](02_backbone/backbone.md) |
| 3. FRD (per module) | recommended | `03_modules/{module}/frd.md` |
| 4. User Stories | recommended | `03_modules/{module}/userstories/` |
| 5. SRS | recommended | `03_modules/{module}/srs.md` |
| 6. Package | not-needed (PoC) | — |

## Modules

| Module | Trạng thái |
| --- | --- |
| MOD-01 auth | recommended |
| MOD-02 ideation | recommended |
| MOD-03 sketching | recommended |
| MOD-04 rendering | recommended |
| MOD-05 modeling-3d | recommended |
| MOD-06 asset-management | recommended |

## Open Questions cần resolve

- OQ-02: PoC success criteria / KPI (Sprint 1 workshop)
- OQ-03: AWS region
- OQ-06: Asset retention & IP policy
- OQ-07: Image upload formats/limits
- OQ-08: Admin Portal scope
- OQ-09: UI framework (Streamlit vs React)

## Lệnh tiếp theo

```
/ba-start frd --slug ai-jewelry-poc --module ideation
/ba-start frd --slug ai-jewelry-poc --module auth
```
