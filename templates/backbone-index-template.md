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

## Producer Instructions (BẮT BUỘC — KHÔNG ĐƯỢC BỎ QUA)

Khi tạo backbone-index.md, PHẢI tuân thủ các quy tắc sau:

### 1. source_hash — PHẢI tính SHA256 thật
- Đọc file `backbone.md`.
- Chạy `python3 -c "import hashlib; print(hashlib.sha256(open('backbone.md','rb').read()).hexdigest())"`.
- Điền kết quả vào `source_hash`. KHÔNG để `[sha256]`, KHÔNG để `to-be-computed`, KHÔNG để placeholder.

### 2. Anchor / Heading — PHẢI khớp CHÍNH XÁC với backbone.md
- Copy-paste nguyên văn heading từ `backbone.md` (bao gồm cả dấu câu, khoảng trắng, chữ hoa/thường).
- Ví dụ: nếu backbone.md có heading `Mục tiêu kinh doanh và chỉ số thành công`, thì Anchor/Heading cũng phải là `Mục tiêu kinh doanh và chỉ số thành công`, KHÔNG viết tắt thành `Mục tiêu kinh doanh`.

### 3. Trace IDs — MỖI DÒNG PHẢI CÓ ÍT NHẤT 1 ID
- Mỗi dòng index PHẢI có ít nhất 1 Trace ID hợp lệ từ backbone.md.
- KHÔNG dùng `—` (em dash) nếu không có ID.
- ID family tương ứng với section:
  - BG-* → Mục tiêu kinh doanh
  - ACT-* → Nhóm người dùng và tác nhân
  - PORTAL-* → Ma trận portal
  - F-* → Bản đồ tính năng
  - FR-* → Backbone yêu cầu chức năng
  - NFR-* → Backbone yêu cầu phi chức năng
  - EP-* → Story Map
  - SCR-* → UI và màn hình
  - A1, A2, ... → Assumptions
  - R-* → Risks

### 4. Mỗi section trong backbone.md PHẢI có 1 dòng index
- Tất cả các heading cấp ≤ 3 trong backbone.md đều phải có dòng index tương ứng.
- KHÔNG được bỏ sót section nào.

### 5. Sau khi write — CHẠY NGAY validator
```bash
ba-kit validate-index --index-key backbone_index --slug {slug} --date {date} --writeback
```
