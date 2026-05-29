---
phase: 1
title: "UC Template Cross-Function Section"
status: completed
priority: P1
effort: "30m"
dependencies: []
---

# Phase 1: UC Template Cross-Function Section

## Overview

Add `## Cross-Function Impact` section to the UC template (`templates/usecase-item-template.md`). This is the foundation all other phases build on — UC authors declare what their UC depends on and what it produces.

## Requirements

- Functional: New template section with two tables (Within Module, Across Modules) and three dependency types (Input, Output/Trigger, Shared State)
- Non-functional: Backward compatible — existing UCs without this section are valid, just have no declared dependencies

## Architecture

New section inserted between `## Postconditions` and `## Diagram` in the UC template. Positioned after the flow description but before the visual diagram — semantically grouped with behavioral specification.

### Template Content

```markdown
## Cross-Function Impact

### Within Module

| Direction | UC | Data / State | Type |
|-----------|-----|--------------|------|
| Depends on | UC-{slug} | {data_or_state} | Input |
| Produces for | UC-{slug} | {data_or_state} | Output |

### Across Modules

| Direction | Target Module | Expected UC / Backbone Ref | Data / State | Type |
|-----------|---------------|---------------------------|--------------|------|
| Produces for | {module_slug} | {backbone_feature_id} | {data_or_state} | Output |
| Consumes from | {module_slug} | {backbone_feature_id} | {data_or_state} | Input |

**Dependency Types:** Input (this UC needs data from another), Output/Trigger (this UC produces data another needs), Shared State (both read/write same entity).
```

### Resolution Rules (not in template — in SKILL.md guidance)

1. **Intra-module**: BA resolves directly during UC authoring. Full knowledge of both UCs.
2. **Inter-module "produces for"**: Module A BA writes it. References backbone feature ID. Consumer UC doesn't need to exist yet.
3. **Inter-module "consumes from"**: Module B BA writes it when their module starts. Backbone defines the contract.
4. **Compile time**: Assembler cross-references all modules for mismatch detection.
5. **Export time**: Only resolved dependencies appear in QC-kit output. Pending ones → "Expected: TBD".

## Related Code Files

- Modify: `templates/usecase-item-template.md`

## Implementation Steps

1. Read current `templates/usecase-item-template.md`
2. Insert `## Cross-Function Impact` section between `## Postconditions` and `## Diagram`
3. Add `### Within Module` subsection with example table
4. Add `### Across Modules` subsection with example table
5. Add `**Dependency Types:**` legend below tables
6. Verify template renders correctly (no broken markdown, tables parse)
7. Add changelog entry to template if applicable

## Success Criteria

- [ ] `## Cross-Function Impact` section exists in UC template
- [ ] Within Module table has columns: Direction, UC, Data/State, Type
- [ ] Across Modules table has columns: Direction, Target Module, Expected UC/Backbone Ref, Data/State, Type
- [ ] Three dependency types documented: Input, Output/Trigger, Shared State
- [ ] Existing template sections unchanged (no regressions)
- [ ] Section positioned between Postconditions and Diagram

## Risk Assessment

- **Low risk**: Template-only change, no runtime behavior affected
- Existing UCs without this section remain valid — no migration required
