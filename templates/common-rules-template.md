# Danh mục quy tắc dùng chung (Common Rules)

## Metadata

| Field | Value |
| --- | --- |
| source_artifact | `plans/{slug}-{date}/02_backbone/backbone.md` |
| generated_by_command | `ba-start backbone` |
| status | draft |
| owner | Lead BA |

## Common Rules

| code | type | rule_statement | applies_to | owner | status | source | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CR-VAL-01 | VAL | [Canonical validation rule statement] | [module/screen/field scope] | Lead BA | active | [source] | [notes] |

## Usage Rules

- Module artifacts must reference these codes instead of redefining shared rules.
- New `CR-*` codes must be added here before module screens or contracts can use them.
- Reusing an existing code with different meaning is blocked.
