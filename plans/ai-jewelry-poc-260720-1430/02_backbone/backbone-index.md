# Chỉ mục backbone (Backbone Index)

## Metadata

| Field | Value |
| --- | --- |
| index_type | backbone |
| source_artifact | `plans/ai-jewelry-poc-260720-1430/02_backbone/backbone.md` |
| source_hash | 2f9ac58e8a321f6aaa0e7d10dd0335405484363475e5fc224bcd76b15eb7c6d1 |
| generated_at | 2026-07-21T08:00:00Z |
| generated_by_command | `ba-start backbone` |
| stale_status | `current` |
| validated_at | `2026-07-21T04:01:45Z` |
| validated_by | `scripts/validate-index-quality.py` |
| coverage_summary | Scope lock, BG-01–04, ACT-01–02, PORTAL-CHAT, F-02–09, MOD-02–06, FR-02–10, NFR-01–02/04–05/07–08, Story Map, SCR-02–05, OQ-01–09 |

## Section Index

| Section | Anchor / Heading | Trace IDs | Module / Feature | Short Summary |
| --- | --- | --- | --- | --- |
| Scope lock | Tóm tắt phạm vi đã chốt | BG-01, ACT-01, PORTAL-CHAT | All | Problem, outcomes, out-of-scope (no auth, no admin), key decisions |
| Business Goals | Mục tiêu kinh doanh và chỉ số thành công | BG-01, BG-02, BG-03, BG-04 | All | 4 goals: giảm freelancer, tăng tốc, trao quyền, validate PoC |
| Actors | Nhóm người dùng và tác nhân | ACT-01, ACT-02 | All | Designer (HK, direct access), AI orchestrator |
| Portal Matrix | Ma trận portal và sở hữu điều hướng (Portal Matrix) | PORTAL-CHAT | MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 1 portal — PORTAL-CHAT only; no admin portal |
| Feature Map | Bản đồ tính năng và phạm vi (Feature Map) | F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09 | MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 8 features; F-09 (.step) TBD; no auth/admin features |
| Module List | Danh sách module | F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09 | MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 5 modules; no MOD-01 auth |
| FR Backbone | Backbone yêu cầu chức năng (Functional Backbone) | FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, FR-09, FR-10 | MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 9 FRs — 4 pipelines, image upload, 3D preview, S3, session; no login FR |
| NFR Backbone | Backbone yêu cầu phi chức năng (Non-Functional Backbone) | NFR-01, NFR-02, NFR-04, NFR-05, NFR-07, NFR-08 | MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | Performance, Security (S3 IP), Availability, Deployability; no auth/scalability NFR |
| Story Map | Story Map sơ bộ (Preliminary Story Map) | F-02, F-03, F-04, F-05, F-06, F-07, F-08 | MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 11 stories across 5 epics; no auth epic |
| UI Screen Coverage | UI và màn hình cần tài liệu (UI and Screen Coverage) | SCR-02, SCR-03, SCR-04, SCR-05 | MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | 4 screens; SCR-02 (Chat) và SCR-04 (3D viewer) critical; no login/admin screens |
| UI Design Direction | Hướng thiết kế UI cần chốt trước wireframe | PORTAL-CHAT | MOD-02, MOD-03, MOD-04, MOD-05 | UI framework TBD; single-page chat, no nav menu needed |
| Artifact Gates | Điều kiện tiến hành từng tài liệu | FR-02, FR-03, FR-04, FR-05, NFR-01, NFR-04, SCR-02, SCR-04 | MOD-02, MOD-03, MOD-04, MOD-05, MOD-06 | FRD/stories/SRS required; package optional for PoC |
| Assumptions | Assumptions | ACT-01, PORTAL-CHAT, NFR-01, NFR-07 | All | 9 assumptions; Bedrock availability, EC2 GPU, S3 persistence, no-auth PoC |
| Risks | Risks | R-01, R-02, R-03, R-04, R-05, R-06 | All | Top risk: Bedrock region (High); UI framework delay (Medium) |
| Open Questions | Open Questions | ACT-01, PORTAL-CHAT, SCR-02, SCR-04 | All | OQ-01/04/05/08 resolved; OQ-02/03/06/07/09 open |
