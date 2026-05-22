# Trạng thái tool lane (Tool Lane State)

- Slug: [initiative-slug]
- Date: [YYMMDD-HHmm]
- Module: [module-slug]
- Selected lane: `manual`
- Lane state: `ready`
- Approval source: [explicit user choice / lifecycle default / reverse carveout]
- Source screen field contract: `plans/{slug}-{date}/03_modules/{module_slug}/screen-field-contract.yaml`
- Source wireframe input: `plans/{slug}-{date}/03_modules/{module_slug}/wireframe-input.md`
- Source design doc: `designs/{slug}/DESIGN.md`
- Stale triggers: [impact on screens, field rules, states, navigation, lane switch]

## Expected downstream artifacts

- `plans/{slug}-{date}/03_modules/{module_slug}/wireframe-map.md`
- `plans/{slug}-{date}/03_modules/{module_slug}/wireframe-state.md`
- `plans/{slug}-{date}/03_modules/{module_slug}/make-guidelines.md` when lane = `figma-make`
- `plans/{slug}-{date}/03_modules/{module_slug}/make-prompt-pack.md` when lane = `figma-make`
- `plans/{slug}-{date}/03_modules/{module_slug}/prototype-conformance-checklist.md` when lane = `figma-make`
- `plans/{slug}-{date}/03_modules/{module_slug}/prototype-conformance-report.md` when lane = `figma-make`
