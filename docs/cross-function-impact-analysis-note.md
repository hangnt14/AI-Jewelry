# Cross-Function Impact Analysis — Future Design Note

**Origin:** QC-kit gap analysis, 2026-05-29
**Updated:** 2026-05-29 — added cross-module design + resolution rules

## Problem

BA-kit UCs capture trace links (UC → screens → stories) but don't model cross-function relationships:

- Function A output is Function B's input
- Cross-UC workflow ordering (UC-01 must complete before UC-02)
- Impact propagation when Function A changes
- Shared data entities with conflicting read/write access across UCs

QC-kit's KA #8 (Functional Integration Analysis, 20pts) evaluates this. BA-kit has `srs/spec.md` `## API / Integration Constraints` but that's for external integrations, not internal cross-function analysis.

## Additional Complexity: Cross-Module Dependencies

In multi-BA projects, different BAs own different modules. Module A may finish before Module B. Cross-module dependencies can't be fully resolved at authoring time.

## Design: Produce-First, Resolve-Later

Module A declares what it **produces** for external consumers. Module B (when it eventually exists) declares what it **consumes**. Neither needs the other to exist at authoring time.

### UC Template Addition

```markdown
## Cross-Function Impact

### Within Module
| Direction | UC | Data / State | Type |
|-----------|-----|--------------|------|
| Depends on | UC-cart | cart_id, cart_items | Input |
| Produces for | UC-tracking | order_id, order_status | Output |

### Across Modules
| Direction | Target Module | Expected UC / Backbone Ref | Data / State | Type |
|-----------|---------------|---------------------------|--------------|------|
| Produces for | shipping | FEAT-SHP-01 | order_id, order_status | Output |
| Consumes from | auth | FEAT-AUTH-03 | user_id, token | Input |
```

Three dependency types: Input, Output/Trigger, Shared State.

### Resolution Rules

1. **Intra-module**: BA resolves directly during UC authoring. Full knowledge.

2. **Inter-module "produces for"**: Module A BA writes it. References backbone feature ID. The consuming UC doesn't need to exist yet.

3. **Inter-module "consumes from"**: Module B BA writes it when their module starts. Backbone defines the contract. Module A's existing declarations are hints, not requirements.

4. **Compile time**: Assembler cross-references all modules. If Module A says "produces for shipping: order_id" and Module B's UC-shipment says "consumes from payment: order_id" → resolved. If mismatch → flagged. If one side missing → noted as pending.

5. **Export time** (to QC-kit): Only resolved dependencies appear. Pending ones become "Expected consumer/producer: TBD" — QC-kit treats as known limitation, not a gap.

### Backbone is the Anchor

Backbone (`02_backbone/backbone.md`) already defines cross-module boundaries, shared entities, and feature map. Cross-function declarations just reference backbone IDs. No new coordination protocol needed — backbone IS the protocol.

Module B not finished yet → Module A's external table has TBD entries. That's fine. The analysis is partial by design, not broken.

## Open Questions

- Does this aggregate into compiled SRS as a dependency matrix or per-UC section?
- Should `ba-impact` consume this for automated change impact analysis?
- Does `qc-uc-review` need a KA #8 scoring adjustment to leverage this?
- Should the compile step produce a module-level dependency graph from the per-UC declarations?

## Related

- QC-kit repo: https://github.com/Sotatek-PhuongTran/qc-kit
- BA-kit qc-uc-review skill: `skills/qc-uc-review/`
- UC template: `templates/usecase-item-template.md`
- Bridge skill note: `docs/ba-qc-export-bridge-note.md`
