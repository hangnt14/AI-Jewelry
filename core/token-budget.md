# Token Budget Baseline

Muc tieu cua file nay la khoa tran kich thuoc cho instruction surface cua BA-kit sau refactor `contract + stub + step files`.

- Don vi dung trong CI la `bytes`, khong phai token.
- `bytes` duoc dung vi on dinh hon tokenization runtime va du tot de bat drift som.
- Cac nguong `max` khong phai muc tieu de lap day; chung chi la guardrail.
- Khi mot thay doi co y mo rong instruction surface, cap nhat ca `baseline` lan `max` trong block JSON ben duoi, roi chay lai budget check.

## Baseline hien tai

- Shared entry runtime hien tai: `core/contract.yaml` + `core/contract-behavior.md` + `skills/ba-start/SKILL.md` = `39,757 bytes`
- Runtime policies hien tai: `AGENTS.md` + `GEMINI.md` + `CLAUDE.md` = `9,732 bytes`
- Cac path dat nhat hien tai:
  - `srs_wireframe_bundle` = `50,073 bytes`
  - `srs_core_bundle` = `46,371 bytes`
  - `wireframes_bundle` = `43,927 bytes`

## Guardrail source

```json
{
  "version": 5,
  "captured_at": "2026-05-11",
  "units": "bytes",
  "notes": "Baselines updated after BA-kit artifact profile metadata landed. Intentional growth is concentrated in core/contract.yaml and the shared runtime bundles; max values keep modest headroom while preserving drift detection.",
  "files": [
    { "path": "core/contract.yaml", "baseline": 11649, "max": 12400, "label": "machine contract" },
    { "path": "core/contract-behavior.md", "baseline": 24912, "max": 26000, "label": "behavior contract" },
    { "path": "skills/ba-start/SKILL.md", "baseline": 3196, "max": 3500, "label": "ba-start stub" },
    { "path": "skills/ba-start/steps/intake.md", "baseline": 5447, "max": 6000, "label": "intake step" },
    { "path": "skills/ba-start/steps/impact.md", "baseline": 4793, "max": 5200, "label": "impact step" },
    { "path": "skills/ba-start/steps/backbone.md", "baseline": 4697, "max": 5000, "label": "backbone step" },
    { "path": "skills/ba-start/steps/frd.md", "baseline": 2407, "max": 2700, "label": "frd step" },
    { "path": "skills/ba-start/steps/stories.md", "baseline": 2797, "max": 3100, "label": "stories step" },
    { "path": "skills/ba-start/steps/srs.md", "baseline": 2476, "max": 2800, "label": "srs router step" },
    { "path": "skills/ba-start/steps/srs-core.md", "baseline": 4113, "max": 4600, "label": "srs core step" },
    { "path": "skills/ba-start/steps/srs-wireframes.md", "baseline": 3702, "max": 4200, "label": "srs wireframes step" },
    { "path": "skills/ba-start/steps/srs-assembly.md", "baseline": 2070, "max": 2400, "label": "srs assembly step" },
    { "path": "skills/ba-start/steps/wireframes.md", "baseline": 6215, "max": 7000, "label": "wireframes step" },
    { "path": "skills/ba-start/steps/package.md", "baseline": 2766, "max": 3100, "label": "package step" },
    { "path": "skills/ba-start/steps/status.md", "baseline": 1980, "max": 2200, "label": "status step" },
    { "path": "AGENTS.md", "baseline": 3952, "max": 4200, "label": "codex runtime policy" },
    { "path": "GEMINI.md", "baseline": 3145, "max": 3600, "label": "antigravity runtime policy" },
    { "path": "CLAUDE.md", "baseline": 2635, "max": 2900, "label": "claude runtime policy" }
  ],
  "bundles": [
    {
      "name": "runtime_policies",
      "baseline": 9732,
      "max": 10800,
      "paths": ["AGENTS.md", "GEMINI.md", "CLAUDE.md"]
    },
    {
      "name": "shared_entry_runtime",
      "baseline": 39757,
      "max": 42000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md"]
    },
    {
      "name": "intake_bundle",
      "baseline": 45204,
      "max": 47500,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/intake.md"]
    },
    {
      "name": "backbone_bundle",
      "baseline": 44454,
      "max": 46500,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/backbone.md"]
    },
    {
      "name": "status_bundle",
      "baseline": 41737,
      "max": 43500,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/status.md"]
    },
    {
      "name": "stories_bundle",
      "baseline": 42554,
      "max": 44500,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/stories.md"]
    },
    {
      "name": "wireframes_bundle",
      "baseline": 45972,
      "max": 48000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/wireframes.md"]
    },
    {
      "name": "srs_core_bundle",
      "baseline": 48416,
      "max": 50500,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/srs.md", "skills/ba-start/steps/srs-core.md", "skills/ba-start/steps/srs-assembly.md"]
    },
    {
      "name": "srs_wireframe_bundle",
      "baseline": 52118,
      "max": 54000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/srs.md", "skills/ba-start/steps/srs-core.md", "skills/ba-start/steps/srs-wireframes.md", "skills/ba-start/steps/srs-assembly.md"]
    }
  ]
}
```

## Cach chay

```bash
scripts/check-token-budget.sh
```

Neu budget fail, uu tien:

1. Go rule trung lap khoi runtime policy files.
2. Tach bot step file neu mot path cu the phinh qua nhanh.
3. Dua phan deterministic sang CLI hoac manifest machine-readable thay vi prose.
