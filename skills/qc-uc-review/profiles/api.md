# API Platform Profile

> Loaded by `qc-uc-review` skill when `--platform api` is specified.
> This profile defines all API-specific framing, paths, edge cases, and KA adjustments.

---

## Subject Framing — CHỈ Client SDK / API Consumer

Mọi phát biểu trong output PHẢI đặt **chủ ngữ là Client SDK/Consumer**, KHÔNG đặt chủ ngữ là Server/Backend.

| ❌ SAI (focus Server) | ✅ ĐÚNG (focus Client) |
|---|---|
| Server trả về danh sách 5 bản ghi | Client nhận response → parse và xử lý tối đa 5 bản ghi |
| Timeout tối đa 10s phía server | Client không nhận response trong 10s → throw TimeoutException / retry? |
| API có lọc theo role? | Client gửi request với credentials → nhận dataset khác nhau theo role? |
| Server xử lý rate limit | Client nhận 429 → có retry-after logic? Có backoff strategy? |
| Backend validate input | Client có pre-validation trước khi gửi request? Hay chỉ xử lý error response? |

**Scope boundary:** Only raise questions about CLIENT-SIDE / CONSUMER-SIDE behavior. Do NOT question server implementation logic. Do NOT audit backend processing, database queries, or server-side validation internals.

---

## Input Contract

- CMR: `docs/BA/SRS-api/Common rule/CMR_API.md` (read first)
- UC folder: `docs/BA/SRS-api/{UC-folder-name}/`
- Question Backlog: `docs/QC-API/review-doc/{UC-folder-name}/*_question-backlog.md` (if exists)
- Important: Check input directory for existing versions, read the highest version.

## Output Contract

- Output folder: `docs/QC-API/review-doc/{UC-folder-name}/`
- Versioning: If `v[N]` exists → `v[N+1]`. NEVER overwrite.

---

## Edge Case Checklist (API-specific)

Apply during KA #6 — Object Attributes & Behavior Definition.
If UC does not mention an item → record gap + question.

| Group | Key checks |
|---|---|
| A — Contract | Request/response schema fully defined?, required vs optional fields documented?, nullable fields handled?, breaking vs non-breaking change policy? |
| B — Error Handling | All HTTP error codes mapped to client behavior (400, 401, 403, 404, 409, 422, 500, 503)?, error response body schema defined?, client retry on 5xx?, partial success (207) handled? |
| C — Rate Limiting | Rate limit headers documented (X-RateLimit-*)?, client behavior on 429 defined?, backoff strategy (linear/exponential)?, quota exhaustion notification? |
| D — Pagination | Pagination strategy defined (cursor/offset/page)?, empty page behavior?, last page detection?, page size limits documented? |
| E — Versioning | API version in path/header?, deprecation notice handling?, backward compatibility window?, client behavior when version sunset? |

> Edge cases only check CLIENT-SIDE / CONSUMER-SIDE behavior. Do NOT deduct points for gaps found here (bonus coverage).

**Rule 6.4 threshold:** ≥70% items covered across groups A-E → Clear (4pts). 40–<70% → Partial (2pts). <40% → Missing (0pts).

---

## KA Adjustments (API)

### KA #3 — Actors & User Roles
- 3.3 Permission rules: focus on what each actor/credential can **call** / **receive** from the API.
- 3.4 Fallback: unauthorized role → how does the **Client** handle 401/403 response?

### KA #5 — UI Object Inventory & Mapping (adapted for API)
- 5.2 UC ↔ Contract consistency: treat **endpoints as components** — check endpoint names, HTTP methods, and payload fields match between UC and API contract/spec.
- 5.4 CMR Cross-Check: reference `CMR_API.md`. ≥85% applicable CMRs referenced → Clear.

### KA #7 — Functional Logic & Workflow Decomposition
- 7.3 Exception & Error Flows: error handling for every **API call from the client** — what does the Consumer do when the call fails, times out, or returns unexpected status?

### KA #10 — Non-functional Requirements
- 10.3 Accessibility: N/A for pure API; substitute with **observability** — logging, tracing, error reporting from client side.
- 10.4 Compatibility: API version compatibility, SDK version matrix, deprecation handling.

### KA Interaction Terminology (API)
- Use **HTTP methods as interactions**: GET (read), POST (create), PUT/PATCH (update), DELETE (remove).
- Treat **endpoints as components** in UC object inventory.
- Request/response cycle replaces UI interaction flow — document both happy path and error path payloads.
- Authentication flow (OAuth, API key, JWT) must be documented as a distinct interaction sequence.

---

## CMR Path

```
docs/BA/SRS-api/Common rule/CMR_API.md
```

Read CMR before scoring KA #5 (5.4 CMR Cross-Check) and before flagging any cross-artefact conflicts.

---

## Output Naming Convention

```
docs/QC-API/review-doc/{UC-folder-name}/{UC-ID}_audited_{feature-slug}_v[N].md
docs/QC-API/review-doc/{UC-folder-name}/{UC-ID}_question-backlog.md
```

---

## Routing Check — Output Folder States

| Output folder state | Action |
| :--- | :--- |
| No `*_audited_*_v[N].md` file | → **First audit** workflow |
| Has `*_audited_*` + backlog all Answered | → **Re-audit** workflow |
| Has `*_audited_*` + backlog has Open unanswered | → **WARN** + **ASK** user (see SKILL.md Step 0) |
| Has `*_audited_*` + no backlog | → **ASK** user: view current version or re-audit? |
| UC folder input does not exist | → **STOP** — ask user to verify UC path |
| Output folder does not exist (but UC exists) | → Create folder + continue first-audit |

---

## Examples — API Subject Framing in Gap Reports

**Gap: Missing error handling for 500**
- ❌ "Server returns 500 on DB failure"
- ✅ "Client receives 500 → what does the Consumer do? Retry? Surface error to caller? Log and fail silently?"

**Gap: Missing rate limit handling**
- ❌ "Server enforces 100 req/min limit"
- ✅ "Client receives 429 → is there retry-after logic? Does the SDK expose backoff configuration?"

**Gap: Missing pagination end detection**
- ❌ "API returns cursor for next page"
- ✅ "Client receives response with no next cursor → does it stop fetching? Is there a hasMore flag check?"

**Gap: Missing auth token refresh**
- ❌ "Token expires after 1 hour"
- ✅ "Client receives 401 on expired token → does it auto-refresh? What happens if refresh also fails?"

**Gap: Missing schema for error body**
- ❌ "API returns error details"
- ✅ "Client receives error response → is the error body schema defined? Can the Consumer reliably parse error code and message?"
