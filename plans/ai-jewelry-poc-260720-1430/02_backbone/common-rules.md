# Common Rules Registry

**Slug:** ai-jewelry-poc | **Date:** 260720-1430
**Scope:** System-level — applies across all modules unless noted

---

## Display Rules (CR-DIS)

| Rule Code | Mô tả | Applies To | Edge Cases |
| --- | --- | --- | --- |
| CR-DIS-01 | Required field được đánh dấu bằng dấu `*` bên cạnh label | Tất cả form fields được đánh dấu bắt buộc | Khi field trở thành optional theo điều kiện, ẩn dấu `*` dynamically |
| CR-DIS-02 | Placeholder text hiển thị khi field trống; biến mất khi focus | Text input fields trong Login screen | Placeholder không phải label — không dùng thay label |
| CR-DIS-03 | Generated images hiển thị trong gallery inline trong chat; loading state hiển thị spinner | SCR-02 (Chat) — Ideation/Sketch/Render output | Nếu generation fail, hiển thị error state thay vì spinner treo |
| CR-DIS-04 | 3D viewer chiếm toàn bộ panel area; controls (rotate/zoom) hiển thị overlay | SCR-04 (3D Viewer) | Trên mobile/small screen: cần confirm fallback behavior |

## Behaviour Rules (CR-BEH)

| Rule Code | Mô tả | Applies To | Edge Cases |
| --- | --- | --- | --- |
| CR-BEH-01 | Submit button disabled cho đến khi tất cả required fields được điền hợp lệ | SCR-01 (Login), bất kỳ form có required fields | Validation chỉ trigger sau first submit attempt hoặc on-blur, không realtime |
| CR-BEH-02 | Pipeline stage tiếp theo chỉ unlock sau khi user đã chọn output từ stage hiện tại | SCR-02 (Chat) — stage progression | Nếu user muốn quay lại stage trước, cần confirm behavior (restart hay giữ context) |
| CR-BEH-03 | Upload button accept file; sau khi upload thành công, preview thumbnail hiển thị inline | F-07 (Image Upload) trong SCR-02 | File quá lớn hoặc format không hỗ trợ → error message theo MSG-ERR-03 |
| CR-BEH-04 | Session tự động persist generated assets lên S3 sau mỗi generation step thành công | F-08, F-09 — tất cả pipeline outputs | Network failure khi persist → retry logic; user cần được thông báo nếu persist fail |

## Validation Rules (CR-VAL)

| Rule Code | Mô tả | Applies To | Edge Cases |
| --- | --- | --- | --- |
| CR-VAL-03 | Prompt text: không được trống trước khi submit; max length TBD | SCR-02 (Chat) — prompt input | Whitespace-only string được treat như empty |
| CR-VAL-04 | Image upload: chỉ accept JPEG/PNG/WEBP; max size TBD (OQ-07) | F-07 — image upload trong SCR-02 | File extension check phía client; MIME type check phía server |
