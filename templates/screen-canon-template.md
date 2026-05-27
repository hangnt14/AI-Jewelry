# Screen Canon Template

## Frontmatter

```yaml
---
artifact_type: screen-canon
screen_id: SCR-XXX-01
screen_name: [Screen Name]
module_slug: [module-slug]
status: draft
screen_type: primary
parent_screen_id: N/A
portal_id: [PORTAL-ID]
nav_schema_id: [NAV-SCHEMA-ID]
expected_active_menu_item: [menu-key]
shell_variant: [SHELL-VARIANT]
layout_variant: [LAYOUT-VARIANT]
navigation_region_visible: true
primary_actor: [Actor]
goal: [Primary screen goal]
ascii_status: current
figma_sync_eligible: false
figma_sync_status: not-run
trace:
  user_stories: [US-001]
  use_cases: [UC-xxx]
  functional_requirements: [FR-module-001]
  business_rules: [BR-module-001]
  messages: [MSG-INF-01]
---
```

## Purpose

- Primary intent:
- User value:
- Scope notes:

## Entry And Exit

- Entry conditions:
- Entry triggers:
- Exit outcomes:

## Regions

| region_id | region_type | label | visible | notes |
| --- | --- | --- | --- | --- |
| REG-HEADER | page_header | [Label] | Yes | [Notes] |

## Fields

| field_id | label | control_type | region_id | display_rules | behaviour_rules | validation_rules | rule_codes | message_codes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FLD-001 | [Label] | [text_input] | REG-HEADER | [Rules] | [Rules] | [Rules] | [CR-DIS-01] | [MSG-ERR-01] |

## Actions

| action_id | label | scope | trigger | outcome | target |
| --- | --- | --- | --- | --- | --- |
| ACT-001 | [Action] | page | click | [Outcome] | [Target/N/A] |

## States

| state_id | state_name | trigger | user_visible_result | message_code |
| --- | --- | --- | --- | --- |
| ST-DEFAULT | default | initial_load_success | [Visible result] | N/A |

## State Visual Coverage

| state_id | state_name | trigger | user_impact | visual_level | ascii_required | figma_required | parent_context_required | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ST-DEFAULT | default | initial_load_success | baseline experience | L3 | Yes | Yes | No | Primary baseline |

## Navigation Behavior

| field | value |
| --- | --- |
| breadcrumb_back_behavior | [Rule] |
| local_navigation_notes | [Rule] |
| hidden_navigation_exception | [None / Rule] |

## Overlay Context

Use this section only when `screen_type` is overlay-like.

| field | value |
| --- | --- |
| parent_screen_id | [SCR-XXX-00] |
| entry_trigger | [ACT-XXX] |
| render_mode | [parent_dimmed_snapshot] |
| background_context_required | [Yes/No] |
| navigation_region_visible | [No] |
| close_behavior | [Rule] |
| success_behavior | [Rule] |
| error_behavior | [Rule] |

## Trace Links

| trace_type | ids |
| --- | --- |
| user_stories | [US-001] |
| use_cases | [UC-xxx] |
| functional_requirements | [FR-module-001] |

## ASCII Wireframe

### ST-DEFAULT

```text
+--------------------------------------------------+
| Header                                           |
+--------------------------------------------------+
| Navigation / Filters / Main content              |
+--------------------------------------------------+
```

## Figma Frame Map

| state_id | frame_name | required |
| --- | --- | --- |
| ST-DEFAULT | SCR-XXX-01__DEFAULT | Yes |

## Figma Sync Notes

- Page / section target:
- Variant or component hints:
- Known exclusions:
