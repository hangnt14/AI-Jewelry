---
type: screen
module: "{module_slug}"
screen_id: "SCR-{NN}"
slug: "{screen-slug}"
portal_id: "{PORTAL-ID}"
nav_schema_id: "{NAV-SCHEMA-ID}"
expected_active_menu: "{menu item}"
actor: "{actor}"
ascii_status: pending
status: draft
linked_usecases: []
linked_stories: []
source_backbone_ids: []
created: "{YYYY-MM-DD}"
owner: "{@handle}"
changelog:
  - {YYYY-MM-DD} | /srs | initial draft
---

# SCR-{NN}: {screen title}

## Overview

| Field | Value |
|---|---|
| Portal ID | {PORTAL-ID} |
| Nav Schema ID | {NAV-SCHEMA-ID} |
| Expected Active Menu Item | {menu item} |
| Navigation Region Visible | Yes / No |
| Entry Conditions | {condition} |
| Exit Conditions | {condition} |
| Actor | {actor} |
| Linked Use Cases | UC-{slug} |
| Linked Stories | US-{NNN} |

## Fields

| Field Name | Display Rules | Behaviour Rules | Validation Rules |
|---|---|---|---|
| {field} | {label, placeholder, visibility, default, read-only} | Bấm -> mở SCR-XXX, hiển thị toast MSG-INF-01, hoặc enable/disable field Y theo trạng thái nghiệp vụ. | {required/format/range, inline/toast/banner, MSG-ERR-NN} |

### Behaviour Rules Naming Sheet

Use these patterns, not technical language:

| Pattern | Correct (Business) | Wrong (Technical) |
|---|---|---|
| Navigate to screen | Bấm -> mở SCR-LRN-12 (My Learning) | Click -> redirect /learn |
| Open overlay | Bấm -> mở modal SCR-FORGOT-PW | Click -> showModal('forgot') |
| Close overlay | Bấm ngoài modal -> đóng, quay về màn cha | Click -> close() |
| Submit form | Bấm -> validate -> gọi xác thực -> đúng: vào SCR-XXX, sai: toast MSG-ERR-01 | Click -> POST /api/auth |
| Show message | Sau khi gửi -> toast xanh MSG-SUC-01 "Đã gửi link reset" | showSuccessToast() |
| Toggle state | Bấm -> enable/disable field Y, hiển thị section Z | setDisabled(false) |

## User Actions

| Action | Trigger | Outcome |
|---|---|---|
| {action label} | {user gesture} | {system response or navigation} |

## States

| State ID | Name | Description |
|---|---|---|
| {SCR-NN-DEFAULT} | Default | {description} |
| {SCR-NN-EMPTY} | Empty | {description} |
| {SCR-NN-ERROR} | Error | {description} |

## Validation Rules

- {CR-VAL-NN}: {rule description}

## ASCII Wireframe

### Default State

```
+--------------------------------------------------+
| {Screen Title}                                   |
+--------------------------------------------------+
| {field label}: [________________]                |
|                                                  |
| [{Action Button}]                                |
+--------------------------------------------------+
```

### Empty State

```
+--------------------------------------------------+
| {Screen Title}                                   |
+--------------------------------------------------+
| (No items yet)                                   |
| [{Call to Action}]                               |
+--------------------------------------------------+
```

### Error State

```
+--------------------------------------------------+
| {Screen Title}                                   |
+--------------------------------------------------+
| {field label}: [________________]                |
| ! {error message}                                |
| [{Action Button}]                                |
+--------------------------------------------------+
```

## Overlay Context (if applicable)

| Field | Value |
|---|---|
| Parent Screen | SCR-{NN} |
| Entry Trigger | {trigger} |
| Render Mode | modal / drawer / dialog |
| Close Behavior | {behavior} |
| Success Return | {behavior} |
| Error Return | {behavior} |
