# Chỉ mục SRS (SRS Index)

## Metadata

| Field | Value |
| --- | --- |
| index_type | srs |
| source_artifact | `plans/{slug}-{date}/03_modules/{module_slug}/srs.md` |
| source_hash | [sha256] |
| generated_at | [YYYY-MM-DDTHH:mm:ssZ] |
| generated_by_command | `ba-start srs` |
| stale_status | unknown |
| validated_at | [YYYY-MM-DDTHH:mm:ssZ after validator pass; blank when pending or failed] |
| validated_by | [`validate-index-quality` or runtime validator id; blank when pending or failed] |
| coverage_summary | [Use case, screen, rule, message và test trace anchors] |

Producer note: index mới sinh phải giữ `stale_status: unknown`; chỉ validator mới được điền `validated_at`, `validated_by`, và nâng lên `current`.

## SRS Index

| Group | UC / SCR / Rule / Message IDs | Screen / Flow | Path / Heading | Dependency |
| --- | --- | --- | --- | --- |
| group-a | UC-01, SCR-01 | [Flow] | [Heading or group file] | US-001 / FR-01 |
