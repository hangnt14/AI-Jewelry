# Token Budget Baseline

Muc tieu cua file nay la khoa tran kich thuoc cho instruction surface cua BA-kit sau refactor `contract + shared behavior + command shard + step files`.

- Don vi dung trong CI la `bytes`, khong phai token.
- `bytes` on dinh hon tokenization runtime va du tot de bat drift som.
- Cac nguong `max` la guardrail, khong phai muc tieu de lap day.
- Khi mo rong instruction surface co chu y, cap nhat `baseline` va `max`, roi chay lai budget check.

## Baseline hien tai

- Shared entry runtime: `core/contract.yaml` + `core/contract-behavior.md` + `skills/ba-start/SKILL.md` = `45,736 bytes`
- Runtime policies: `AGENTS.md` + `GEMINI.md` + `CLAUDE.md` = `12,491 bytes`
- Command runtime bundle lon nhat: `srs_runtime_bundle` = `64,414 bytes`
- Behavior base cap: `14,000 bytes`; moi behavior shard cap: `4,500 bytes`

## Guardrail source

```json
{
  "version": 12,
  "captured_at": "2026-05-25",
  "units": "bytes",
  "notes": "Baselines updated after SRS canon-first, ASCII wireframe, Figma sync boundary, and hard guardrail command-surface expansion.",
  "files": [
    { "path": "core/contract.yaml", "baseline": 23074, "max": 24500, "label": "machine contract" },
    { "path": "core/contract-behavior.md", "baseline": 18796, "max": 19800, "label": "shared behavior contract" },
    { "path": "core/behavior/intake.md", "baseline": 700, "max": 4500, "label": "intake behavior shard" },
    { "path": "core/behavior/backbone.md", "baseline": 2332, "max": 4500, "label": "backbone behavior shard" },
    { "path": "core/behavior/impact.md", "baseline": 2032, "max": 4500, "label": "impact behavior shard" },
    { "path": "core/behavior/module-authoring.md", "baseline": 1771, "max": 4500, "label": "module authoring behavior shard" },
    { "path": "core/behavior/srs.md", "baseline": 4646, "max": 4900, "label": "srs behavior shard" },
    { "path": "core/behavior/wireframes.md", "baseline": 3777, "max": 4500, "label": "wireframes behavior shard" },
    { "path": "core/behavior/package-status-next.md", "baseline": 2589, "max": 4500, "label": "package status next behavior shard" },
    { "path": "core/behavior/figma-sync.md", "baseline": 1700, "max": 4500, "label": "figma sync behavior shard" },
    { "path": "skills/ba-start/SKILL.md", "baseline": 3866, "max": 4100, "label": "ba-start stub" },
    { "path": "skills/ba-start/steps/intake.md", "baseline": 5323, "max": 6000, "label": "intake step" },
    { "path": "skills/ba-start/steps/impact.md", "baseline": 5604, "max": 5900, "label": "impact step" },
    { "path": "skills/ba-start/steps/backbone.md", "baseline": 5628, "max": 6000, "label": "backbone step" },
    { "path": "skills/ba-start/steps/frd.md", "baseline": 2548, "max": 2800, "label": "frd step" },
    { "path": "skills/ba-start/steps/stories.md", "baseline": 3418, "max": 3600, "label": "stories step" },
    { "path": "skills/ba-start/steps/srs.md", "baseline": 3327, "max": 3500, "label": "srs router step" },
    { "path": "skills/ba-start/steps/srs-core.md", "baseline": 3127, "max": 4200, "label": "srs core step" },
    { "path": "skills/ba-start/steps/srs-wireframes.md", "baseline": 4341, "max": 4600, "label": "srs wireframes step" },
    { "path": "skills/ba-start/steps/srs-assembly.md", "baseline": 3237, "max": 3400, "label": "srs assembly step" },
    { "path": "skills/ba-start/steps/wireframes.md", "baseline": 6095, "max": 6500, "label": "wireframes step" },
    { "path": "skills/ba-start/steps/package.md", "baseline": 4209, "max": 4400, "label": "package step" },
    { "path": "skills/ba-start/steps/status.md", "baseline": 4382, "max": 4600, "label": "status step" },
    { "path": "AGENTS.md", "baseline": 2767, "max": 3600, "label": "codex runtime policy" },
    { "path": "GEMINI.md", "baseline": 5304, "max": 5600, "label": "antigravity runtime policy" },
    { "path": "CLAUDE.md", "baseline": 4420, "max": 4700, "label": "claude runtime policy" }
  ],
  "bundles": [
    {
      "name": "runtime_policies",
      "baseline": 12491,
      "max": 13000,
      "paths": ["AGENTS.md", "GEMINI.md", "CLAUDE.md"]
    },
    {
      "name": "shared_entry_runtime",
      "baseline": 45736,
      "max": 48200,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md"]
    },
    {
      "name": "intake_runtime_bundle",
      "baseline": 51759,
      "max": 54500,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/intake.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/intake.md"]
    },
    {
      "name": "backbone_runtime_bundle",
      "baseline": 53696,
      "max": 56500,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/backbone.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/backbone.md"]
    },
    {
      "name": "impact_runtime_bundle",
      "baseline": 53372,
      "max": 56200,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/impact.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/impact.md"]
    },
    {
      "name": "module_authoring_runtime_bundle",
      "baseline": 53473,
      "max": 56300,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/module-authoring.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/frd.md", "skills/ba-start/steps/stories.md"]
    },
    {
      "name": "srs_core_bundle",
      "baseline": 60073,
      "max": 63200,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/srs.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/srs.md", "skills/ba-start/steps/srs-core.md", "skills/ba-start/steps/srs-assembly.md"]
    },
    {
      "name": "srs_runtime_bundle",
      "baseline": 64414,
      "max": 67700,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/srs.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/srs.md", "skills/ba-start/steps/srs-core.md", "skills/ba-start/steps/srs-wireframes.md", "skills/ba-start/steps/srs-assembly.md"]
    },
    {
      "name": "wireframes_runtime_bundle",
      "baseline": 55608,
      "max": 58500,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/wireframes.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/wireframes.md"]
    },
    {
      "name": "package_status_next_runtime_bundle",
      "baseline": 56916,
      "max": 59800,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/package-status-next.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/package.md", "skills/ba-start/steps/status.md"]
    }
  ]
}
```

## Cach chay

Windows:

```powershell
python scripts/check-token-budget.py .
```

Unix-like:

```bash
scripts/check-token-budget.sh
```

Neu budget fail, uu tien:

1. Go rule trung lap khoi runtime policy files.
2. Tach bot step file hoac behavior shard neu mot path phinh qua nhanh.
3. Dua phan deterministic sang CLI hoac manifest machine-readable thay vi prose.
