# Mobile Platform Profile

> Loaded by `qc-uc-review` skill when `--platform mobile` is specified.
> This profile defines all mobile-specific framing, paths, edge cases, and KA adjustments.

---

## Subject Framing — CHỈ Mobile Client

Mọi phát biểu trong output PHẢI đặt **chủ ngữ là App/Client**, KHÔNG đặt chủ ngữ là API/Server.

| ❌ SAI (focus API) | ✅ ĐÚNG (focus Client) |
|---|---|
| API Tin tức trả về danh sách 5 tin | App nhận response Tin tức → render tối đa 5 tin |
| Timeout tối đa 10s cho API calls | App không nhận response trong 10s → hiển thị message + nút Thử lại |
| API có lọc theo role? | App có expected dataset khác nhau giữa các role? |
| Server xử lý timeout sau 10s | App phát hiện không có response sau 10s → hiển thị thông báo |
| API Biểu đồ trả về dữ liệu chart | App nhận dữ liệu → render biểu đồ theo format |

**Scope boundary:** Only raise questions about CLIENT-SIDE behavior. Do NOT question API/backend logic. Do NOT audit API logic, evaluate backend, or ask questions about server-side processing.

---

## Input Contract

- CMR: `docs/BA/SRS-mobile/Common rule/CMR_Mobile.md` (read first)
- UC folder: `docs/BA/SRS-mobile/[UC-folder-name]/`
- Question Backlog: `docs/QC-MOBILE/review-doc/[UC-folder-name]/*_question-backlog.md` (if exists)
- Important: Check input directory for existing versions, read the highest version.

## Output Contract

- Output folder: `docs/QC-MOBILE/review-doc/[UC-folder-name]/`
- Versioning: If `v[N]` exists → `v[N+1]`. NEVER overwrite.

---

## Edge Case Checklist (Mobile-specific)

Apply during KA #6 — Object Attributes & Behavior Definition.
If UC does not mention an item → record gap + question.

| Group | Key checks |
|---|---|
| A — Extreme Data | Text overflow (truncate/wrap?), numeric 0/negative/max, empty list vs max items, null from API → placeholder? |
| B — Network | Slow API → loading/skeleton?, partial failure → independent or block all?, double-tap → debounce?, network loss mid-load? |
| C — Abnormal Interaction | Rapid taps → block multiple nav?, back button when modal open?, screen rotation? |
| D — Permissions & Session | Session expire → redirect/notify?, force-close → return screen?, different roles → different UI? |
| E — i18n | Language change → immediate update?, long text languages → layout break?, language persistence? |

> Edge cases only check CLIENT-SIDE behavior. Do NOT deduct points for gaps found here (bonus coverage).

**Rule 6.4 threshold:** ≥70% items covered across groups A-E → Clear (4pts). 40–<70% → Partial (2pts). <40% → Missing (0pts).

---

## KA Adjustments (Mobile)

### KA #3 — Actors & User Roles
- 3.3 Permission rules: focus on what each actor can **tap** / **see** on the mobile screen.
- 3.4 Fallback: role not in enum → how does the **App UI** handle it?

### KA #5 — UI Object Inventory & Mapping
- 5.2 UC ↔ Wireframe consistency: check label names, positions, component types match between UC and mobile wireframe/mockup.
- 5.4 CMR Cross-Check: reference `CMR_Mobile.md`. ≥85% applicable CMRs referenced → Clear.

### KA #7 — Functional Logic & Workflow Decomposition
- 7.3 Exception & Error Flows: error handling for every **API call from the client** — what does the App display/do when the call fails or times out?

### KA #10 — Non-functional Requirements
- 10.3 Accessibility: touch target size, contrast ratio, screen reader support.
- 10.4 Compatibility: iOS/Android OS versions, screen sizes, orientations.

---

## CMR Path

```
docs/BA/SRS-mobile/Common rule/CMR_Mobile.md
```

Read CMR before scoring KA #5 (5.4 CMR Cross-Check) and before flagging any cross-artefact conflicts.

---

## Output Naming Convention

```
docs/QC-MOBILE/review-doc/[UC-folder-name]/[UC-ID]_audited_[feature-slug]_v[N].md
docs/QC-MOBILE/review-doc/[UC-folder-name]/[UC-ID]_question-backlog.md
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

## Examples — Mobile Subject Framing in Gap Reports

**Gap: Missing network error handling**
- ❌ "API call fails → server returns 500"
- ✅ "App receives error response / no response → what does the screen display? Is there a retry button?"

**Gap: Missing role-based UI difference**
- ❌ "API filters data by role"
- ✅ "App renders different dataset / different action buttons depending on logged-in role?"

**Gap: Missing loading state**
- ❌ "API response takes time"
- ✅ "App has no loading indicator / skeleton screen defined while waiting for data"

**Gap: Missing debounce on navigation**
- ❌ "Backend receives duplicate requests"
- ✅ "App: rapid double-tap on nav button → does it navigate twice? Is there a tap guard?"

**Gap: Missing empty state**
- ❌ "API returns empty array"
- ✅ "App receives empty list → what does the screen render? Placeholder text? Illustration?"
