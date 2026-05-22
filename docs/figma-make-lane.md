# Figma Make Lane

BA-kit vẫn coi `manual` là lane mặc định ở Step 9. Figma Make là lane opt-in cho team muốn prototype nhanh nhưng vẫn giữ hard guardrails ở upstream BA artifacts.

## Artifact flow

1. `srs` viết Group B + Group C như bình thường.
2. Step 8.1 sinh:
   - `03_modules/{module}/wireframe-input.md`
   - `03_modules/{module}/screen-field-contract.yaml`
3. `wireframes` resolve lane:
   - `manual`
   - `figma-make`
4. Nếu lane là `figma-make`, `wireframes` sinh:
   - `05_tool-lanes/figma-make/shared-rules.md`
   - `05_tool-lanes/figma-make/shared-prompt-skeleton.md`
   - `05_tool-lanes/figma-make/shared-component-contracts.md`
   - `03_modules/{module}/make-guidelines.md`
   - `03_modules/{module}/make-prompt-pack.md`
   - `03_modules/{module}/prototype-conformance-checklist.md`
5. Sau khi Make tạo prototype, team dùng checklist + report để reject drift.

## Source of truth split

- `srs.md` và `srs-group-c.md`: source of truth nghiệp vụ.
- `screen-field-contract.yaml`: bản normalize máy đọc được của screen truth.
- `DESIGN.md`: visual baseline và navigation schema baseline.
- `make-guidelines.md` + `make-prompt-pack.md`: downstream control artifacts, không phải source of truth.

## Hard rules

- Không dùng raw `srs.md` làm Make prompt chính.
- Không thêm field ngoài allowlist trong `screen-field-contract.yaml`.
- Không đổi `Portal ID`, `Nav Schema ID`, `Expected Active Menu Item`.
- Nếu rule thiếu, bỏ qua thay vì tự phát minh.
- Drift phát hiện sau prototype phải route qua `ba-start impact`.

## Pre-flight

Chạy:

```bash
python3 scripts/validate-tool-control-pack.py --repo . --slug <slug> --date <YYMMDD-HHmm> --module <module>
```

Nếu lane là `manual`, validator sẽ `skip`. Nếu lane là `figma-make`, validator fail khi thiếu:

- `screen-field-contract.yaml`
- shared rules / prompt skeleton / component contracts
- `make-prompt-pack.md`
- `prototype-conformance-checklist.md`

## Report

Sinh skeleton report:

```bash
python3 scripts/generate-prototype-conformance-report.py --repo . --slug <slug> --date <YYMMDD-HHmm> --module <module>
```

Report mặc định list từng `screen_id` để reviewer mark `pass`, `fail`, `blocked`, hoặc `needs-impact`.
