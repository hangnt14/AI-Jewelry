# Chỉ mục rule/message dùng chung (Shared Rule Message Index)

## Metadata

| Field | Value |
| --- | --- |
| index_type | shared-rule-message |
| source_common_rules | `plans/ai-jewelry-poc-260720-1430/02_backbone/common-rules.md` |
| source_message_list | `plans/ai-jewelry-poc-260720-1430/02_backbone/message-list.md` |
| generated_at | 2026-07-20T10:10:16Z |
| generated_by_command | `validate-shared-rule-message-registry --write-index` |
| stale_status | current |
| validated_at | 2026-07-20T10:10:16Z |
| validated_by | `validate-shared-rule-message-registry` |

## Rule Code Index

| code | type | summary | source_anchor | applies_to | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| CR-DIS-01 | DIS | Required field marked with `*` | Display Rules (CR-DIS) | All form fields | @hangnt14 | active |
| CR-DIS-02 | DIS | Placeholder text in empty inputs | Display Rules (CR-DIS) | Text input fields — Login | @hangnt14 | active |
| CR-DIS-03 | DIS | Generated images inline gallery with spinner | Display Rules (CR-DIS) | SCR-02 Chat — pipeline output | @hangnt14 | active |
| CR-DIS-04 | DIS | 3D viewer full panel with overlay controls | Display Rules (CR-DIS) | SCR-04 3D Viewer | @hangnt14 | active |
| CR-BEH-01 | BEH | Submit button disabled until valid | Behaviour Rules (CR-BEH) | SCR-01 Login; all forms | @hangnt14 | active |
| CR-BEH-02 | BEH | Pipeline stage unlock after selection | Behaviour Rules (CR-BEH) | SCR-02 Chat — stage progression | @hangnt14 | active |
| CR-BEH-03 | BEH | Upload button with thumbnail preview | Behaviour Rules (CR-BEH) | SCR-02 — image upload (F-07) | @hangnt14 | active |
| CR-BEH-04 | BEH | Auto-persist assets to S3 after generation | Behaviour Rules (CR-BEH) | All pipeline outputs | @hangnt14 | active |
| CR-VAL-03 | VAL | Prompt: not empty, max length TBD | Validation Rules (CR-VAL) | SCR-02 Chat — prompt input | @hangnt14 | active |
| CR-VAL-04 | VAL | Image upload: JPEG/PNG/WEBP only, max size TBD | Validation Rules (CR-VAL) | SCR-02 — image upload (F-07) | @hangnt14 | active |

## Message Code Index

| code | type | summary | source_anchor | applies_to | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| MSG-ERR-02 | ERR | Generation failure (Bedrock/Stability AI) | Error Messages (MSG-ERR) | SCR-02 Chat | @hangnt14 | active |
| MSG-ERR-03 | ERR | Unsupported image format | Error Messages (MSG-ERR) | SCR-02 — image upload | @hangnt14 | active |
| MSG-ERR-04 | ERR | Image file too large | Error Messages (MSG-ERR) | SCR-02 — image upload | @hangnt14 | active |
| MSG-ERR-05 | ERR | 3D model generation failure | Error Messages (MSG-ERR) | SCR-04 3D Viewer | @hangnt14 | active |
| MSG-SUC-01 | SUC | Asset saved to S3 | Success Messages (MSG-SUC) | SCR-02 Chat | @hangnt14 | active |
| MSG-SUC-02 | SUC | 3D model ready | Success Messages (MSG-SUC) | SCR-04 3D Viewer | @hangnt14 | active |
| MSG-SUC-03 | SUC | .stl downloaded | Success Messages (MSG-SUC) | SCR-04 3D Viewer | @hangnt14 | active |
| MSG-WRN-01 | WRN | Generation slow / timeout warning | Warning Messages (MSG-WRN) | SCR-02, SCR-04 | @hangnt14 | active |
| MSG-WRN-02 | WRN | Session expiry countdown | Warning Messages (MSG-WRN) | All screens | @hangnt14 | active |
| MSG-INF-01 | INF | Prompt user to select concept direction | Info Messages (MSG-INF) | SCR-02 Chat — post Ideation | @hangnt14 | active |
| MSG-INF-02 | INF | Prompt user to select sketch | Info Messages (MSG-INF) | SCR-02 Chat — post Sketching | @hangnt14 | active |
| MSG-INF-03 | INF | Prompt user to select render for 3D | Info Messages (MSG-INF) | SCR-02 Chat — post Rendering | @hangnt14 | active |
| MSG-INF-04 | INF | .step disclaimer — visual reference only | Info Messages (MSG-INF) | SCR-04 — .step export option | @hangnt14 | active |

## Collision And Scope Signals

| signal | value |
| --- | --- |
| rule_count | 10 |
| message_count | 13 |
| duplicate_codes | 0 |
| stale_refs | 0 |
| module_local_definitions | 0 |
| error_count | 0 |
