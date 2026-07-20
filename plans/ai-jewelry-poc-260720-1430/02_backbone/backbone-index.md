# Chỉ mục backbone (Backbone Index)

## Metadata

| Field | Value |
| --- | --- |
| index_type | backbone |
| source_artifact | `plans/ai-jewelry-poc-260720-1430/02_backbone/backbone.md` |
| source_hash | 5cf6799ccdf60d51cc0e4a11f32b8220af0b4966869fd5420e544ca935bbc7f9 |
| generated_at | 2026-07-20T14:30:00Z |
| generated_by_command | `ba-start backbone` |
| stale_status | `current` |
| validated_at | `2026-07-20T10:04:11Z` |
| validated_by | `scripts/validate-index-quality.py` |
| coverage_summary | Scope lock, BG-01–04, ACT-01–03, PORTAL-CHAT/ADMIN, F-01–10, MOD-01–06, FR-01–10, NFR-01–08, Story Map, SCR-01–06, OQ-01–09 |

## Section Index

| Section | Anchor / Heading | Trace IDs | Module / Feature | Short Summary |
| --- | --- | --- | --- | --- |
| Scope lock | Tóm tắt phạm vi đã chốt | BG-01, ACT-01, PORTAL-CHAT | All | Problem, outcomes, out-of-scope, key decisions (auth, stack, language) |
| Business Goals | Mục tiêu kinh doanh và chỉ số thành công | BG-01, BG-02, BG-03, BG-04 | All | 4 goals: giảm freelancer, tăng tốc, trao quyền, validate PoC |
| Actors | Nhóm người dùng và tác nhân | ACT-01, ACT-02, ACT-03 | All | Designer (HK), AI orchestrator, Admin/Operator |
| Portal Matrix | Ma trận portal và sở hữu điều hướng (Portal Matrix) | PORTAL-CHAT, PORTAL-ADMIN | MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 2 portals; PORTAL-ADMIN scope TBD |
| Feature Map | Bản đồ tính năng và phạm vi (Feature Map) | F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10 | MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 10 features; F-09/F-10 scope TBD |
| Module List | Danh sách module | F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10 | MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 6 modules; tất cả status recommended |
| FR Backbone | Backbone yêu cầu chức năng (Functional Backbone) | FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, FR-09, FR-10 | MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 10 FRs covering auth, 4 pipelines, 3D preview, S3, session |
| NFR Backbone | Backbone yêu cầu phi chức năng (Non-Functional Backbone) | NFR-01, NFR-02, NFR-03, NFR-04, NFR-05, NFR-06, NFR-07, NFR-08 | MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | Performance (latency, GPU), Security (auth, S3), Availability, Scalability |
| Story Map | Story Map sơ bộ (Preliminary Story Map) | F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08 | MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 12 stories across 6 epics (auth → ideation → sketch → render → 3D → asset) |
| UI Screen Coverage | UI và màn hình cần tài liệu (UI and Screen Coverage) | SCR-01, SCR-02, SCR-03, SCR-04, SCR-05, SCR-06 | MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 6 screens; SCR-02 (Chat) và SCR-04 (3D viewer) critical |
| UI Design Direction | Hướng thiết kế UI cần chốt trước wireframe | PORTAL-CHAT, PORTAL-ADMIN | MOD-02, MOD-03, MOD-04, MOD-05 | UI framework TBD; 8 decisions cần chốt trước SRS |
| Artifact Gates | Điều kiện tiến hành từng tài liệu | FR-01, FR-02, FR-03, FR-04, FR-05, NFR-01, NFR-03, SCR-01, SCR-02 | MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | FRD/stories/SRS required; package optional for PoC |
| Assumptions | Assumptions | ACT-01, PORTAL-CHAT, NFR-01, NFR-07 | All | 9 assumptions; Bedrock availability, EC2 GPU, S3 persistence, auth scope |
| Risks | Risks | R-01, R-02, R-03, R-04, R-05, R-06 | All | Top risk: Bedrock region (High); UI framework delay (Medium) |
| Open Questions | Open Questions | ACT-01, PORTAL-ADMIN, SCR-02, SCR-04 | All | 9 OQs; OQ-04/OQ-05 resolved; OQ-09 UI framework TBD |
