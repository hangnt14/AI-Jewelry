---
type: backbone
status: draft
created: 2026-07-20
updated: 2026-07-20
owner: "@hangnt14"
changelog:
  - 2026-07-20 | /ba-start backbone | initial backbone từ proposal v1.0 + OQ resolution
---

# Xương sống yêu cầu (Requirements Backbone)

**Dự án:** AI Jewelry Design Assistant — Proof of Concept
**Slug:** ai-jewelry-poc
**Ngày:** 260720-1430
**Chế độ triển khai:** hybrid
**Chủ sở hữu:** @hangnt14

---

## Tóm tắt phạm vi đã chốt

- **Vấn đề kinh doanh:** Designer jewelry tại Hong Kong phụ thuộc freelancer cho ideation và visualization; cycle dài và tốn chi phí.
- **Kết quả mong muốn:** PoC AI chatbot giúp designer tự tạo design concepts (moodboard → 2D sketch → render → 3D mesh) qua natural language và image upload; deployed trên AWS account của client.
- **Ngoài phạm vi:** Production-ready infra; CAD file generation; manufacturing-ready designs; integration với hệ thống có sẵn của client.
- **Quyết định đã chốt:**
  - Deployment: standalone AWS (EC2 + Bedrock + CloudFront + S3)
  - AI stack: Claude (orchestration) + Stability AI (image gen) + Trellis (3D mesh)
  - 3D export: `.stl` standard; `.step` optional add-on (không mặc định vào scope)
  - Authentication: username/password đơn giản (multi-user support)
  - UI language: English (PoC)
  - UI framework: **TBD** — cần confirm (Streamlit vs React)

---

## Mục tiêu kinh doanh và chỉ số thành công

| Goal ID | Mục tiêu | Chỉ số / Kết quả đo lường | Chủ sở hữu |
| --- | --- | --- | --- |
| BG-01 | Giảm phụ thuộc freelancer cho ideation | Designer có thể hoàn thành 1 design cycle (moodboard → render) mà không cần thuê ngoài | Client (HK jewelry designer) |
| BG-02 | Tăng tốc design cycle | Thời gian từ prompt → render output giảm so với quy trình hiện tại (baseline TBD — cần confirm với client) | Client |
| BG-03 | Trao quyền kiểm soát trực tiếp cho designer | Designer tự vận hành 4 pipeline stages mà không cần kỹ thuật hỗ trợ | Client |
| BG-04 | Validate khả thi của AI-assisted jewelry design trên AWS | PoC được client sign-off sau UAT; decision có thể được đưa ra về đầu tư tiếp theo | Client + SoftwareOne |

> **OQ-02 [hold]:** Success criteria định lượng (KPI cụ thể) chưa được confirm — cần workshop Sprint 1.

---

## Nhóm người dùng và tác nhân

| Actor ID | Vai trò | Mục tiêu chính | Ghi chú |
| --- | --- | --- | --- |
| ACT-01 | Jewelry Designer (HK) | Tạo design concepts qua AI chatbot, chọn outputs, export 3D | End user chính; 1–N người (OQ-01: multi-user support đã chốt) |
| ACT-02 | System (AI Orchestrator) | Interpret prompt → dispatch tới image/3D services → trả output | Claude Bedrock; không phải human actor |
| ACT-03 | Admin / Operator | Quản lý user accounts, monitor instance, access S3 | Có thể là client IT hoặc SotaTek handover; cần xác nhận scope |

---

## Ma trận portal và sở hữu điều hướng (Portal Matrix)

| Portal ID | Portal Name | Target Actor | Owned Screen Families | Default Entry |
| --- | --- | --- | --- | --- |
| PORTAL-CHAT | Chatbot Portal | ACT-01 (Jewelry Designer) | Login, Chat/Pipeline, Asset Library | Login → Chat |
| PORTAL-ADMIN | Admin Portal | ACT-03 (Admin/Operator) | User Management, System Monitor | Login → Dashboard |

> **Note:** PORTAL-ADMIN scope còn TBD — cần xác nhận với client xem PoC có cần admin UI không hay chỉ cần AWS Console access.

---

## Bản đồ tính năng và phạm vi (Feature Map)

| Feature ID | Tính năng / Capability | Mô tả | Ưu tiên | In Scope | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| F-01 | Authentication | Username/password login; session management; multi-user support | Must | Yes | Đã chốt: multi-user, simple auth |
| F-02 | Ideation Pipeline | Nhập prompt → generate moodboard, concept images, trend references | Must | Yes | Bedrock: Claude + Stability AI |
| F-03 | Sketching Pipeline | Chọn concept direction → generate 2D sketch variations | Must | Yes | Bedrock: Stability AI |
| F-04 | Rendering Pipeline | Chọn sketch → generate photorealistic renders (multi-metal, multi-angle) | Must | Yes | Bedrock: Stability AI higher-fidelity |
| F-05 | 3D Modeling Pipeline | Chọn render → convert image-to-3D → export .stl mesh | Must | Yes | Trellis trên EC2 GPU |
| F-06 | In-app 3D Preview | Inspect, rotate, kiểm tra dimensions của mesh trong browser | Must | Yes | Tech stack TBD |
| F-07 | Image Upload (Reference) | User upload reference images vào chatbot | Must | Yes | Format/size limit: OQ-07 |
| F-08 | Asset Management / S3 Storage | Generated assets persist S3; user có thể access/download | Must | Yes | Retention policy: OQ-06 |
| F-09 | Optional .step Export | Mesh-to-STEP export cho CAD software compatibility | Could | TBD | Facet-based wrapper; cần client confirm trước khi đưa vào sprint |
| F-10 | Admin User Management | Tạo/xóa/reset user accounts | Should | TBD | Phụ thuộc PORTAL-ADMIN scope decision |

---

## Danh sách module

| Module ID | Tên module | Mô tả | Feature | Module BA | Portal | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| MOD-01 | auth | Authentication & session management | F-01 | @hangnt14 | PORTAL-CHAT, PORTAL-ADMIN | recommended |
| MOD-02 | ideation | Ideation pipeline — moodboard & concept generation | F-02, F-07 | @hangnt14 | PORTAL-CHAT | recommended |
| MOD-03 | sketching | 2D sketch variation pipeline | F-03 | @hangnt14 | PORTAL-CHAT | recommended |
| MOD-04 | rendering | Photorealistic render pipeline | F-04 | @hangnt14 | PORTAL-CHAT | recommended |
| MOD-05 | modeling-3d | 3D mesh generation, preview, export | F-05, F-06, F-09 | @hangnt14 | PORTAL-CHAT | recommended |
| MOD-06 | asset-management | S3 asset persistence, access, download | F-08 | @hangnt14 | PORTAL-CHAT | recommended |

---

## Backbone yêu cầu chức năng (Functional Backbone)

| FR ID | Yêu cầu | Giá trị kinh doanh | Nguồn | AC tóm tắt |
| --- | --- | --- | --- | --- |
| FR-01 | User login bằng username/password | Chỉ user authorized mới truy cập chatbot | OQ-05 resolved | Login thành công → vào Chat; sai credentials → error message |
| FR-02 | User nhập natural language prompt để bắt đầu ideation | Giảm barrier sáng tạo | Proposal §Overview | Prompt submitted → system generate ≥1 moodboard/concept image trong session |
| FR-03 | User upload reference image để guide generation | Tăng độ chính xác output | Proposal §Scope | Image uploaded → visible trong chat; dùng được làm input cho pipeline |
| FR-04 | System generate moodboard / concept images từ prompt | Stage 1 của pipeline | Proposal §Scope | Output hiển thị ≥1 concept image; user có thể chọn direction |
| FR-05 | System generate 2D sketch variations từ concept đã chọn | Stage 2 của pipeline | Proposal §Scope | ≥1 sketch variation hiển thị; user có thể chọn sketch để đi tiếp |
| FR-06 | System generate photorealistic renders đa kim loại và đa góc | Stage 3 của pipeline | Proposal §Scope | ≥1 render/metal/angle combination hiển thị; user có thể chọn render |
| FR-07 | System convert selected render thành 3D mesh (.stl) | Stage 4 của pipeline | Proposal §Scope | .stl file được tạo và available để download |
| FR-08 | User inspect 3D mesh in-app (rotate, zoom, check dimensions) | Designer xem trước model trước khi export | Proposal §Epic 4 | 3D viewer load mesh; user có thể rotate và zoom |
| FR-09 | Generated assets tự động persist lên S3 | Asset không bị mất khi session kết thúc | Proposal §Assumptions | Asset có URL/link accessible sau session; không mất khi reload |
| FR-10 | Session state được duy trì trong conversation | Conversation coherent qua nhiều turns | Proposal §Epic 2 | User có thể refer lại output cũ trong cùng session |

---

## Backbone yêu cầu phi chức năng (Non-Functional Backbone)

| NFR ID | Danh mục | Yêu cầu | Trigger / Gate |
| --- | --- | --- | --- |
| NFR-01 | Performance | Image generation (moodboard/sketch/render) có response time chấp nhận được từ HK | Cần confirm target latency với client — Bedrock region dependency (OQ-03) |
| NFR-02 | Performance | 3D mesh generation (Trellis) hoàn thành trong khoảng thời gian reasonable cho PoC | EC2 GPU instance size cần được confirm (proposal: G5 family) |
| NFR-03 | Security | Chỉ authenticated user mới access chatbot và assets | Authentication gate (FR-01); S3 bucket policy |
| NFR-04 | Security | Generated design assets (IP của client) được bảo vệ trên S3 | Access control + encryption; chi tiết phụ thuộc OQ-06 |
| NFR-05 | Availability | PoC deployment không yêu cầu production SLA | Phù hợp PoC scope; EC2 không cần multi-AZ |
| NFR-06 | Scalability | Hỗ trợ multi-user đồng thời (số lượng cụ thể TBD) | Session isolation cần được thiết kế từ đầu |
| NFR-07 | Deployability | Toàn bộ infra deploy trên AWS account của client | Không dùng SotaTek-managed infra |
| NFR-08 | Usability | UI bằng tiếng Anh; accessible từ Hong Kong qua CloudFront | OQ-04 resolved: English for PoC |

---

## Story Map sơ bộ (Preliminary Story Map)

| Epic | Capability | Story / Outcome | Ưu tiên | Ghi chú |
| --- | --- | --- | --- | --- |
| Authentication | Login | Designer logs in với username/password để access chatbot | Must | MOD-01 |
| Ideation | Prompt input | Designer enters a text prompt describing a jewelry concept to start ideation | Must | MOD-02 |
| Ideation | Image reference | Designer uploads a reference image to guide concept generation | Must | MOD-02 |
| Ideation | Concept selection | Designer reviews generated moodboard/concepts and selects a direction | Must | MOD-02 |
| Sketching | Sketch generation | Designer receives 2D sketch variations of the selected concept | Must | MOD-03 |
| Sketching | Sketch selection | Designer selects a sketch to proceed to rendering | Must | MOD-03 |
| Rendering | Render generation | Designer receives photorealistic renders of the sketch in multiple metals/angles | Must | MOD-04 |
| Rendering | Render selection | Designer selects a render to proceed to 3D modeling | Must | MOD-04 |
| 3D Modeling | Mesh generation | Designer receives a 3D mesh (.stl) of the selected render | Must | MOD-05 |
| 3D Modeling | 3D preview | Designer inspects and rotates the 3D model in-app | Must | MOD-05 |
| 3D Modeling | .stl export | Designer downloads the .stl file | Must | MOD-05 |
| Asset Management | Asset access | Designer can access previously generated assets from past sessions | Should | MOD-06 |

---

## UI và màn hình cần tài liệu (UI and Screen Coverage)

| Screen ID | Portal ID | Màn hình / Luồng | Mức độ phức tạp | Cần wireframe | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| SCR-01 | PORTAL-CHAT | Login Screen | Low | No | Simple form |
| SCR-02 | PORTAL-CHAT | Chat / Main Pipeline Screen | High | Critical | Core screen — prompt input, output display, stage progression |
| SCR-03 | PORTAL-CHAT | Concept/Sketch/Render Gallery (inline) | Medium | Yes | Selection UX trong chat flow |
| SCR-04 | PORTAL-CHAT | 3D Viewer Screen / Panel | High | Yes | In-app mesh viewer; rotate/zoom |
| SCR-05 | PORTAL-CHAT | Asset Library / History | Medium | No | Xem lại past outputs; scope TBD |
| SCR-06 | PORTAL-ADMIN | Admin: User Management | Medium | No | Scope TBD — phụ thuộc PORTAL-ADMIN decision |

---

## Hướng thiết kế UI cần chốt trước wireframe

- **Cần `designs/ai-jewelry-poc/DESIGN.md`:** Yes
- **UI framework:** TBD — Streamlit (Python, nhanh cho PoC) vs React (flexible); cần confirm với engineer
- **Quyết định cần chốt trước Step 9 (SRS/wireframe):**
  - UI framework và component library
  - Visual tone: minimal/professional vs creative/editorial
  - Color scheme: neutral (gold/white/dark) hay tùy client brand
  - Navigation schema cho PORTAL-CHAT: single-page chat vs multi-step wizard
  - Active menu / breadcrumb behavior
  - Image gallery UX pattern (carousel vs grid vs inline)
  - 3D viewer tech (three.js / model-viewer / Babylon.js)

---

## Điều kiện tiến hành từng tài liệu

- **FRD:** Required — 4 pipeline modules (ideation, sketching, rendering, modeling-3d) cần FRD riêng để engineer build; auth và asset-management có thể gộp hoặc lite.
- **User stories:** Required — engineer cần stories để plan sprint; UAT team cần stories để test.
- **SRS:** Required cho MOD-02 đến MOD-05 (pipeline modules); lite cho MOD-01 (auth).
- **Wireframes (ASCII screen spec):** Required cho SCR-02 (Chat/Pipeline) và SCR-04 (3D Viewer); optional cho rest.
- **Package HTML:** Optional cho PoC — chỉ nếu client/SoftwareOne yêu cầu formal handoff document.

---

## Assumptions, Risks, Open Questions

### Assumptions

- Amazon Bedrock (Claude + Stability AI) available và latency acceptable từ target AWS region cho HK users.
- EC2 GPU instance (G5 family) đủ capacity cho concurrent render + 3D generation requests.
- Generated assets persist trên S3; không dùng local instance storage.
- Bedrock dùng latest Claude Sonnet-tier (không pin version) để tránh deprecation.
- User flows chi tiết sẽ được finalize trong requirements workshop Sprint 1.
- Project management do SoftwareOne cung cấp; SotaTek lo SA + BA + engineering.
- AWS infra và model token costs do client tự chi trả qua AWS credits.
- Authentication là simple username/password (không phải OAuth/SSO) — đủ cho PoC.
- UI language là English cho PoC.

### Risks

- **R-01 [High]:** Bedrock model/region availability chưa được confirm → có thể ảnh hưởng timeline Sprint 1. Mitigation: SA confirm trước khi bắt đầu build (Epic 1).
- **R-02 [Medium]:** UI framework chưa chốt (TBD) → delay SRS và wireframe nếu quyết định đến muộn. Mitigation: chốt trong Sprint 1 requirements workshop.
- **R-03 [Medium]:** Chất lượng output Stability AI cho jewelry-specific prompts chưa được validate → có thể cần prompt tuning đáng kể. Mitigation: spike testing sớm trong Sprint 1–2.
- **R-04 [Medium]:** Trellis (image-to-3D) chạy trên EC2 GPU — performance và quality chưa được test với jewelry meshes. Mitigation: early spike trong Epic 4.
- **R-05 [Low]:** `.step` optional export có thể tạo expectation sai với client về CAD capability. Mitigation: communicate rõ limitations; không đưa vào sprint mặc định.
- **R-06 [Low]:** Asset retention / IP protection policy chưa xác định → có thể cần S3 encryption và access policy phức tạp hơn dự kiến.

### Open Questions

- [ ] OQ-01: **End user scope** — Số lượng concurrent users cụ thể? Ảnh hưởng đến session isolation design. *(Hướng chốt: multi-user support; auth simple username/password)*
- [ ] OQ-02: **PoC success criteria** — KPI cụ thể để client sign-off? (latency target, quality benchmark, design cycle time) — *cần resolve trong Sprint 1 workshop*
- [ ] OQ-03: **AWS region** — Target region cụ thể? (Bedrock availability + latency từ HK)
- [ ] OQ-04: **UI language** — *(Đã chốt: English cho PoC)*
- [ ] OQ-05: **Authentication** — *(Đã chốt: username/password đơn giản, multi-user)*
- [ ] OQ-06: **Asset retention & IP protection** — S3 retention period và confidentiality policy?
- [ ] OQ-07: **Image upload formats** — Accepted formats và size limit khi user upload reference images?
- [ ] OQ-08: **Admin Portal scope** — Client có cần admin UI để manage users không, hay dùng AWS Console trực tiếp?
- [ ] OQ-09: **UI framework** — Streamlit hay React? Cần confirm với engineer trước SRS. *(Chốt TBD)*
