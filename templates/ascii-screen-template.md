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
| {field} | {label, placeholder, visibility} | {interaction behavior} | {validation, error surface, MSG-ERR-NN} |

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
