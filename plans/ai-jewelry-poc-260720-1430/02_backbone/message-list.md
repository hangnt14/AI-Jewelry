# Message List Registry

**Slug:** ai-jewelry-poc | **Date:** 260720-1430
**Scope:** System-level — applies across all modules unless noted

---

## Error Messages (MSG-ERR)

| Message Code | Canonical Text | Surface | Applies To |
| --- | --- | --- | --- |
| MSG-ERR-02 | "Something went wrong while generating your design. Please try again." | toast | SCR-02 (Chat) — generation failure (Bedrock/Stability AI error) |
| MSG-ERR-03 | "File type not supported. Please upload a JPEG, PNG, or WEBP image." | inline (below upload) | SCR-02 — invalid image format upload |
| MSG-ERR-04 | "File is too large. Maximum size is {limit}." | inline (below upload) | SCR-02 — image exceeds size limit (limit TBD per OQ-07) |
| MSG-ERR-05 | "3D model generation failed. Please try with a different render." | toast | SCR-04 (3D Viewer) — Trellis generation failure |

## Success Messages (MSG-SUC)

| Message Code | Canonical Text | Surface | Applies To |
| --- | --- | --- | --- |
| MSG-SUC-01 | "Your design has been saved." | toast | SCR-02 — asset successfully persisted to S3 |
| MSG-SUC-02 | "3D model ready. You can now inspect and download it." | toast | SCR-04 — Trellis generation complete |
| MSG-SUC-03 | ".stl file downloaded successfully." | toast | SCR-04 — .stl download complete |

## Warning Messages (MSG-WRN)

| Message Code | Canonical Text | Surface | Applies To |
| --- | --- | --- | --- |
| MSG-WRN-01 | "Generation is taking longer than usual. Please wait…" | banner | SCR-02, SCR-04 — slow response from Bedrock or Trellis |
| MSG-WRN-02 | "Your session will expire in {N} minutes." | banner | All screens — session expiry warning |

## Info Messages (MSG-INF)

| Message Code | Canonical Text | Surface | Applies To |
| --- | --- | --- | --- |
| MSG-INF-01 | "Select a concept direction to continue to sketching." | inline (in chat) | SCR-02 — after Ideation output, prompting user action |
| MSG-INF-02 | "Select a sketch to continue to rendering." | inline (in chat) | SCR-02 — after Sketching output |
| MSG-INF-03 | "Select a render to generate your 3D model." | inline (in chat) | SCR-02 — after Rendering output |
| MSG-INF-04 | "Note: The .step file is a visual reference only and is not suitable for manufacturing." | inline (below download) | SCR-04 — when .step export option shown |
