# BA-kit

BA-kit là playbook Business Analysis cho Claude Code, Codex, và Antigravity. Repo này biến agent thành một BA workstation có lifecycle rõ ràng, artifact có cấu trúc, collaboration theo module, và handoff đủ chuẩn cho stakeholder/engineering.

## License

BA-kit is distributed under a commercial proprietary source-available license.
This commercial proprietary license is provided on a source-available basis.

Access to this repository does not grant redistribution rights. Customers may
use, privately fork, and internally customize BA-kit only within the single
legal entity that purchased or was granted access, subject to the terms in
`LICENSE` and any applicable order form or MSA.

Tài liệu chi tiết: [BA-kit GitBook](https://bakit.gitbook.io/)

## BA Làm Gì Với BA-kit?

BA có thể dùng ngôn ngữ tự nhiên thay vì nhớ command:

```text
Tôi có tài liệu yêu cầu mới, hãy tạo dự án BA
Tiếp tục dự án warehouse-rfp, bước tiếp theo là gì?
Đánh giá thay đổi: Export CSV phải có audit log
Phân tích ngược hệ thống hiện tại để tạo as-built SRS
Tôi nhận module auth-flow
Gửi module auth-flow cho Lead BA review
Đồng bộ module reporting với main trước khi làm tiếp
Xuất gói bàn giao cho stakeholder
```

Agent sẽ map intent sang workflow an toàn:

- Lifecycle BA: intake, options khi cần, backbone, stories, FRD, SRS, wireframe handoff, package.
- Reverse BA: quét code/evidence để dựng as-built SRS, khóa baseline commit, theo dõi drift, và chỉ promote nội dung có evidence rõ.
- Collaboration BA: claim module, check conflict, create review packet, optional GitHub PR handoff.
- Git/GitHub là implementation detail; commit, push, PR, merge chỉ chạy khi user approve rõ.

## Flow Hiện Tại

```text
Raw input
-> Intake + Gap Analysis
-> PROJECT-HOME.md
-> Option pack + comparison khi intake cần nhiều hướng solution
-> Requirements Backbone
-> Module artifacts: FRD / Stories / SRS / Screen Contract Plus
-> DESIGN.md + wireframe-input.md + wireframe-map.md
-> optional tool lane: screen-field-contract + Make control pack + conformance review
-> User tự tạo mockup / wireframe
-> Final SRS + HTML package
```

Với teamwork:

```text
Lead BA chia module
-> COLLAB-HOME.md
-> Module BA nhận module
-> MODULE-HOME.md
-> Module BA tạo/cập nhật artifact trong module scope
-> review packet
-> Lead BA review / approve / integrate
-> optional GitHub PR, approval-gated
```

## Artifact Chính

| Artifact | Vai trò |
| --- | --- |
| `PROJECT-HOME.md` | Dashboard BA-facing: trạng thái, bước tiếp theo, câu hỏi cần chốt, prompt nhanh cho runtime |
| `01_intake/intake.md` | Input đã chuẩn hóa, gap analysis, câu hỏi mở |
| `01_intake/plan.md` | Kế hoạch artifact sẽ sinh theo mode/gate |
| `01_intake/options/*` | Bộ phương án solution và bảng so sánh trước backbone |
| `02_backbone/backbone.md` | Source of truth sau scope lock |
| `02_backbone/project-memory.md` | Bộ nhớ dự án: thuật ngữ, quyết định, assumptions, corrections |
| `COLLAB-HOME.md` | Dashboard cộng tác: ai làm module nào, review status, blocker |
| `03_modules/{module}/MODULE-HOME.md` | Dashboard riêng cho Module BA: scope được sửa, checklist review |
| `03_modules/{module}/frd.md` | Functional Requirements Document theo module |
| `03_modules/{module}/user-stories.md` | User stories và acceptance criteria |
| `03_modules/{module}/srs.md` | SRS/use case/screen spec theo module |
| `03_modules/{module}/screen-field-contract.yaml` | Contract máy đọc được cho field/rule/state/navigation sau Step 8.1 |
| `wireframe-input.md` / `wireframe-map.md` | Gói constraint và map để user tự tạo mockup |
| `03_modules/{module}/tool-lane-state.md` | Lane đã chọn cho Step 9: `manual` mặc định hoặc tool lane opt-in |
| `05_tool-lanes/figma-make/*` | Shared rules và shared prompt skeleton cho Figma Make |
| `03_modules/{module}/make-*.md` | Gói guideline và prompt theo module cho Figma Make |
| `03_modules/{module}/prototype-conformance-*.md` | Checklist và report reject gate cho output từ tool lane |
| `delegation/review-packets/{module}.md` | Gói gửi Lead BA review |
| `04_compiled/*.html` | Bản HTML stakeholder review/edit trong browser |
| `designs/{slug}/DESIGN.md` | Design direction runtime cho UI handoff |

`PROJECT-HOME.md`, `COLLAB-HOME.md`, và `MODULE-HOME.md` là dashboard. Source of truth vẫn là `backbone.md`, sau đó là `intake.md` và module artifacts.

## Cấu Trúc Thư Mục

```text
plans/
  {slug}-{date}/
    PROJECT-HOME.md
    COLLAB-HOME.md
    00_source/
    01_intake/
      intake.md
      plan.md
      options/
        index.md
        option-01.md
        option-02.md
        option-03.md
        comparison.md
    02_backbone/
      backbone.md
      project-memory.md
      project-memory/
    03_modules/
      {module_slug}/
        MODULE-HOME.md
        frd.md
        user-stories.md
        srs.md
        srs-group-a.md
        srs-group-b.md
        srs-group-c.md
        wireframe-input.md
        wireframe-map.md
        wireframe-state.md
    04_compiled/
    delegation/
      packets/
      review-packets/

designs/
  {slug}/
    DESIGN.md
```

## Cài Đặt Nhanh

> Repo access is granted per licensed customer account. If you need access for
> another legal entity, affiliate, contractor, or client organization, that use
> requires a separate written commercial grant.

### Claude Code

```bash
git clone https://github.com/anhdam2/bakit.git
cd bakit
./install.sh
```

Sau đó restart Claude Code.

### Codex

Repo-native: mở repo này trong Codex, Codex đọc `AGENTS.md`.

Bundle install:

```bash
bash scripts/install-codex-ba-kit.sh
```

### Antigravity

```bash
bash scripts/install-antigravity-ba-kit.sh
```

Script cài CLI `ba-kit`, ghi installation manifest, và tạo Knowledge Item workflow cho Antigravity.

## Command Surface

BA non-tech nên bắt đầu bằng natural language qua router:

```text
/ba-do Tôi có tài liệu yêu cầu mới, hãy tạo dự án BA
/ba-do Tiếp tục dự án warehouse-rfp
/ba-do Phân tích ngược hệ thống hiện tại để tạo as-built SRS
/ba-do Tôi nhận module auth-flow
/ba-do Gửi module auth-flow cho Lead BA review
```

Command-level fallback:

```text
/ba-start
/ba-start options --slug warehouse-rfp
/ba-start options --slug warehouse-rfp --select option-02
/ba-start options --slug warehouse-rfp --skip
/ba-start backbone --slug warehouse-rfp
/ba-start srs --slug warehouse-rfp --module auth-flow
/ba-start wireframes --slug warehouse-rfp --module auth-flow
/ba-start package --slug warehouse-rfp
/ba-start status --slug warehouse-rfp
/ba-start reverse --slug warehouse-rfp
/ba-start reverse impact --slug warehouse-rfp
/ba-collab Tôi nhận module auth-flow
/ba-collab Gửi module auth-flow cho Lead BA review
```

Dùng `options` khi intake cho thấy cần 1-3 hướng solution trước khi viết `backbone.md`. Step này tạo option pack + comparison dưới `01_intake/options/*`, rồi chốt `--select` hoặc `--skip` rõ ràng trước khi sang backbone.

Dùng `reverse` khi mục tiêu là dựng tài liệu as-built từ hệ thống đang chạy hoặc code đã commit. Reverse lane chỉ promote nội dung có evidence rõ, không suy diễn business intent, không dùng cho future-state request, và bỏ qua wireframes vì không đề xuất UI mới. Nếu user đang yêu cầu thay đổi mong muốn trong tương lai, chuyển sang `impact` hoặc lifecycle forward bình thường.

## Tool Lane Cho Step 9

- `manual` vẫn là mặc định. Flow cũ không bị phá.
- Nếu user opt-in `figma-make`, BA-kit không dùng raw `srs.md` làm prompt chính.
- `srs` phải compile `screen-field-contract.yaml` sau Group C / Step 8.1.
- `wireframes` đọc contract này để sinh:
  - shared rules ở `05_tool-lanes/figma-make/`
  - `make-guidelines.md`
  - `make-prompt-pack.md`
  - `prototype-conformance-checklist.md`
  - `prototype-conformance-report.md`
- Requirement drift phát hiện từ prototype phải route qua `impact`, không back-write vào SRS.

Chi tiết: [docs/figma-make-lane.md](./docs/figma-make-lane.md)

CLI helper:

```bash
ba-kit doctor
ba-kit install-plantuml
ba-kit update
ba-kit status --slug warehouse-rfp
ba-kit collab status --slug warehouse-rfp
```

## Teamwork Và GitHub

BA-kit hỗ trợ module collaboration nhưng không bắt BA học Git trước.

BA nói:

```text
Tôi nhận module reporting
Đồng bộ module reporting với main
Kiểm tra module reporting trước khi gửi review
Tạo PR cho module reporting
```

Agent xử lý nội bộ:

- Resolve đúng project/module.
- Kiểm tra module ownership và write scope.
- Cập nhật `COLLAB-HOME.md`, `MODULE-HOME.md`, review packet.
- Chạy impact nếu thay đổi chạm requirement/shared decision.
- Chỉ commit/push/PR/merge khi user approve rõ.
- Nếu conflict nghiệp vụ hoặc Git conflict, dừng và báo file/section cần Lead BA quyết định.

## Wireframe Handoff

`/ba-start wireframes` giữ tên để tương thích ngược, nhưng không generate hình UI. Bước này chỉ chuẩn bị manual handoff pack:

- `designs/{slug}/DESIGN.md`
- `03_modules/{module}/wireframe-input.md`
- `03_modules/{module}/wireframe-map.md`
- `03_modules/{module}/wireframe-state.md`

User hoặc designer tự tạo mockup/wireframe rồi attach vào đúng section trong SRS. Mockup không phải source of truth.

## Nâng Cấp

```bash
ba-kit doctor
ba-kit install-plantuml
ba-kit update
```

`ba-kit doctor` kiểm tra runtime readiness. `ba-kit install-plantuml` auto cài PlantUML local bằng package manager phù hợp để HTML packaging ưu tiên render diagram tại máy. `ba-kit update` fast-forward source repo và reinstall các runtime đã cài.

## Đọc Tiếp

- [BA-kit GitBook](https://bakit.gitbook.io/)
- [Getting Started](docs/getting-started.md)
- [Codex Setup](docs/codex-setup.md)
- [Antigravity Setup](docs/antigravity-setup.md)
- [Skill Catalog](docs/skill-catalog.md)
- [BA Methodology Guide](docs/ba-methodology-guide.md)
- [Design Artifacts](designs/README.md)
