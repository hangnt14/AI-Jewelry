# Chỉ mục backbone (Backbone Index)

## Metadata

| Field | Value |
| --- | --- |
| index_type | backbone |
| source_artifact | `plans/{slug}-{date}/02_backbone/backbone.md` |
| source_hash | [sha256] |
| generated_at | [YYYY-MM-DDTHH:mm:ssZ] |
| generated_by_command | `ba-start backbone` |
| stale_status | unknown |
| validated_at | [YYYY-MM-DDTHH:mm:ssZ after validator pass; blank when pending or failed] |
| validated_by | [`validate-index-quality` or runtime validator id; blank when pending or failed] |
| coverage_summary | [Các section và trace anchor trong backbone] |

Producer note: index mới sinh phải giữ `stale_status: unknown`; chỉ validator mới được điền `validated_at`, `validated_by`, và nâng lên `current`.

## Section Index

| Section | Anchor / Heading | Trace IDs | Module / Feature | Short Summary |
| --- | --- | --- | --- | --- |
| [Section name] | [Heading] | [FR-01, ACT-01] | [module/feature] | [1-2 dòng tóm tắt] |
