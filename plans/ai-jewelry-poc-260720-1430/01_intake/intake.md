---
type: intake
status: draft
created: 2026-07-20
updated: 2026-07-20
owner: "@hangnt14"
source_file: requirement/INTERNAL_Sotatek_AI Jewelry Design Assistant_Proposal_v1.0.md
changelog:
  - 2026-07-20 | /ba-start intake | initial draft từ proposal v1.0
---

# Phiếu tiếp nhận yêu cầu (Intake Form)

## Thông tin dự án (Project Information)

| Trường (Field) | Giá trị (Value) |
| --- | --- |
| Tên dự án (Project name) | AI Jewelry Design Assistant — Proof of Concept |
| Ngày (Date) | 2026-07-20 |
| Người yêu cầu (Requester) | Client: Hong Kong-based jewelry designer (qua SoftwareOne) |
| Tài liệu gốc (Source file) | `requirement/INTERNAL_Sotatek_AI Jewelry Design Assistant_Proposal_v1.0.md` |
| Ngày tài liệu gốc (Source date) | 9 Jul 2026 |
| Vendor thực hiện (Delivery vendor) | SotaTek JSC |

## Bối cảnh kinh doanh (Business Context)

### Vấn đề cần giải quyết (Problem Statement)

Client là một jewelry designer tại Hong Kong đang phụ thuộc nhiều vào freelancer bên ngoài để hiện thực hóa ý tưởng thiết kế. Quá trình ideation đến concept đang chậm và tốn chi phí. Giải pháp cần giúp designer tự tạo ra design concepts thông qua natural language và image upload — từ moodboard đến 3D preview — mà không cần qua bên thứ ba.

### Mục tiêu kinh doanh (Business Goals)

1. **Giảm phụ thuộc freelancer** — Designer có thể tự explore và hiện thực hóa ý tưởng mà không cần thuê ngoài cho giai đoạn ideation và sketching.
2. **Tăng tốc design cycle** — Rút ngắn thời gian từ ý tưởng đến visual concept/render.
3. **Trao quyền sáng tạo** — Designer kiểm soát trực tiếp pipeline từ moodboard → 2D sketch → photorealistic render → 3D mesh.
4. **PoC validation** — Chứng minh tính khả thi của AI-assisted jewelry design trên AWS stack (Bedrock + EC2 GPU + S3) trước khi đầu tư sản xuất toàn diện.

### Các bên liên quan (Stakeholders Mentioned)

| Tên / Vai trò | Mức quan tâm / Ảnh hưởng | Ghi chú |
| --- | --- | --- |
| Client — HK jewelry designer | Cao / Cao | End user chính; chủ sở hữu AWS account và IP |
| SoftwareOne | Cao / Trung bình | Project Manager; không thuộc delivery team |
| SotaTek JSC | Trung bình / Cao | Solution architecture, BA, và engineering delivery |
| Pre-Sales / SA (SotaTek) | Trung bình / Cao | Part-time; validate architecture và Bedrock availability |
| Cloud/AI Engineer (SotaTek) | Trung bình / Cao | 1 FTE; toàn bộ build và infra |

## Yêu cầu thô (Raw Requirements)

<!-- Trích nguyên văn từ tài liệu gốc -->

1. AI chatbot hỗ trợ 4 giai đoạn thiết kế: **Ideation** (moodboard, concept, trend references), **Sketching 2D** (sketch variations), **Rendering** (photorealistic renders đa góc, đa chất liệu kim loại), **3D Modeling** (mesh file inspectable và exportable).
2. Interaction qua natural language prompts và image uploads.
3. Deployment trên AWS account của client (EC2, Bedrock, CloudFront, S3).
4. Bedrock integration: Claude (orchestration) + Stability AI (image generation).
5. 3D generation: Trellis (image-to-3D) chạy trên EC2 GPU instance.
6. Export 3D: file `.stl` (standard); `.step` (optional add-on — facet-based wrapper, không phải CAD thực sự).
7. Generated assets persist trên Amazon S3.
8. Streamlit-based chatbot UI.
9. CloudFront CDN + encryption.
10. Conversation/session state handling.

## Màn hình và giao diện (Screens and UI)

| Màn hình / Thành phần | Mô tả | Ghi chú |
| --- | --- | --- |
| Chatbot UI (main) | Giao diện chat chính — nhập prompt, upload ảnh, xem output từng stage | Streamlit; cần xác nhận responsive/mobile |
| Ideation output view | Hiển thị moodboard, concept cards, trend references | Có thể là inline trong chat |
| Sketch / Render gallery | Hiển thị 2D sketch variations và renders đa góc/đa kim loại | Cho phép chọn variant để đi tiếp |
| 3D preview viewer | Inspect, rotate, kiểm tra dimensions của mesh 3D | In-app; cần xác nhận tech stack cho viewer |

## Quy trình và luồng công việc (Processes and Workflows)

| Quy trình / Luồng | Mô tả | Ghi chú |
| --- | --- | --- |
| Ideation pipeline | User nhập prompt → Claude interpret → Stability AI generate moodboard/concepts | Stage 1 |
| Sketching pipeline | User chọn concept direction → Claude orchestrate → Stability AI generate 2D sketch variations | Stage 2 |
| Rendering pipeline | User chọn sketch → Claude orchestrate → Stability AI generate photorealistic multi-metal/multi-angle renders | Stage 3 |
| 3D modeling pipeline | User chọn render → Trellis convert image-to-3D → export .stl mesh (+ optional .step) → persist S3 | Stage 4 |
| Asset management | Generated assets lưu S3; user có thể access/download | Flow chưa được mô tả chi tiết |

## Ràng buộc và giả định (Constraints and Assumptions)

### Ràng buộc (Constraints)

- Deployment phải trên AWS account của client (không phải SotaTek-managed infra).
- Infrastructure và model token costs do client tự chi trả qua AWS credits — không bao gồm trong phí SotaTek.
- Không phải production-ready infrastructure (PoC scope).
- Không có CAD generation: `.step` export là facet-based wrapper, không thể dùng cho manufacturing.
- Không có manufacturing-ready designs.
- Timeline: 6–7 tuần build + 2 tuần UAT.

### Giả định (Assumptions)

- Amazon Bedrock model availability (Claude, Stability AI) đã được confirm cho target AWS region; latency chấp nhận được từ HK.
- EC2 GPU instance size (G5 family) đã được confirm phù hợp với concurrency và render/3D turnaround mong đợi.
- Generated assets (renders, 3D files) được persist trên Amazon S3 thay vì local instance storage.
- Bedrock integration dùng Claude Sonnet-tier model hiện tại (không pin fixed version) để tránh deprecation risk.
- Exact user flows sẽ được finalize trong requirements workshops sprint đầu tiên.
- Project Management do SoftwareOne cung cấp; SotaTek chỉ phụ trách SA, BA, và engineering delivery.

## Tuân thủ và quy định (Compliance and Regulatory Needs)

- Chưa có yêu cầu compliance cụ thể trong proposal (không đề cập GDPR, PDPA, hay data residency rõ ràng).
- IP của client (generated designs) cần được bảo vệ trên S3 — cần xác nhận access policy và encryption requirements.

## Câu hỏi mở (Open Questions)

- [ ] OQ-01: **End user scope** — Chỉ 1 designer hay có thể 2–3 người dùng đồng thời? Ảnh hưởng đến authentication design và session isolation.
- [ ] OQ-02: **PoC success criteria** — "PoC thành công" được định nghĩa như thế nào cụ thể? KPI nào client dùng để sign-off? (vd: 1 design cycle < X phút, quality đủ để hand-off cho CAD designer)
- [ ] OQ-03: **AWS region** — Target region cụ thể là gì? (quan trọng cho Bedrock model availability và latency từ HK)
- [ ] OQ-04: **UI language** — Chatbot interface tiếng Anh, Tiếng Trung phồn thể (Traditional Chinese), hay hỗ trợ cả hai?
- [ ] OQ-05: **Authentication** — Có yêu cầu đăng nhập không, hay đây là single-user private deployment (chỉ 1 URL + password đơn giản)?
- [ ] OQ-06: **Asset retention & IP protection** — Generated assets lưu S3 bao lâu? Có yêu cầu confidentiality policy đặc biệt cho design IP không?
- [ ] OQ-07: **Image upload formats** — Chatbot nhận ảnh định dạng nào khi user upload reference images? (JPG/PNG/WEBP/HEIC; size limit?)

## Ghi chú phân tích (Parsing Notes)

- Proposal là technical + commercial proposal của SotaTek; không phải functional spec. User flows chi tiết chưa tồn tại — sẽ được viết trong sprint 1 (Epic 1, Task "Document detailed chatbot workflows & functional spec").
- `.step` export được mô tả rõ là optional add-on, không mặc định vào scope — cần confirm với client trước khi đưa vào backlog.
- Architecture diagram (image2) không readable từ markdown — cần xem file gốc hoặc yêu cầu SA cung cấp dạng text/diagram.
- Không có thông tin về Bedrock pricing tier hay concurrency estimate trong proposal hiện tại.
