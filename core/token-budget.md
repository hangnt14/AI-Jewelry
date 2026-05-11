# Token Budget Baseline

Muc tieu cua file nay la khoa tran kich thuoc cho instruction surface cua BA-kit sau refactor `contract + shared behavior + command shard + step files`.

- Don vi dung trong CI la `bytes`, khong phai token.
- `bytes` on dinh hon tokenization runtime va du tot de bat drift som.
- Cac nguong `max` la guardrail, khong phai muc tieu de lap day.
- Khi mo rong instruction surface co chu y, cap nhat `baseline` va `max`, roi chay lai budget check.

## Baseline hien tai

- Shared entry runtime: `core/contract.yaml` + `core/contract-behavior.md` + `skills/ba-start/SKILL.md` = `25,978 bytes`
- Runtime policies: `AGENTS.md` + `GEMINI.md` + `CLAUDE.md` = `7,138 bytes`
- Command runtime bundle lon nhat: `srs_runtime_bundle` = `37,981 bytes`
- Behavior base cap: `12,000 bytes`; moi behavior shard cap: `4,500 bytes`

## Guardrail source

```json
{
  "version": 6,
  "captured_at": "2026-05-11",
  "units": "bytes",
  "notes": "Baselines updated after splitting shared behavior into command-scoped shards. Runtime bundles now model the required read order: contract, shared behavior, one behavior shard, ba-start stub, and active step files.",
  "files": [
    { "path": "core/contract.yaml", "baseline": 12607, "max": 13200, "label": "machine contract" },
    { "path": "core/contract-behavior.md", "baseline": 9956, "max": 12000, "label": "shared behavior contract" },
    { "path": "core/behavior/intake.md", "baseline": 700, "max": 4500, "label": "intake behavior shard" },
    { "path": "core/behavior/backbone.md", "baseline": 2332, "max": 4500, "label": "backbone behavior shard" },
    { "path": "core/behavior/impact.md", "baseline": 2032, "max": 4500, "label": "impact behavior shard" },
    { "path": "core/behavior/module-authoring.md", "baseline": 1287, "max": 4500, "label": "module authoring behavior shard" },
    { "path": "core/behavior/srs.md", "baseline": 2916, "max": 4500, "label": "srs behavior shard" },
    { "path": "core/behavior/wireframes.md", "baseline": 1509, "max": 4500, "label": "wireframes behavior shard" },
    { "path": "core/behavior/package-status-next.md", "baseline": 1605, "max": 4500, "label": "package status next behavior shard" },
    { "path": "skills/ba-start/SKILL.md", "baseline": 3415, "max": 3600, "label": "ba-start stub" },
    { "path": "skills/ba-start/steps/intake.md", "baseline": 5447, "max": 6000, "label": "intake step" },
    { "path": "skills/ba-start/steps/impact.md", "baseline": 4793, "max": 5200, "label": "impact step" },
    { "path": "skills/ba-start/steps/backbone.md", "baseline": 4854, "max": 5000, "label": "backbone step" },
    { "path": "skills/ba-start/steps/frd.md", "baseline": 2407, "max": 2700, "label": "frd step" },
    { "path": "skills/ba-start/steps/stories.md", "baseline": 2953, "max": 3100, "label": "stories step" },
    { "path": "skills/ba-start/steps/srs.md", "baseline": 1510, "max": 2200, "label": "srs router step" },
    { "path": "skills/ba-start/steps/srs-core.md", "baseline": 2394, "max": 4200, "label": "srs core step" },
    { "path": "skills/ba-start/steps/srs-wireframes.md", "baseline": 3000, "max": 3900, "label": "srs wireframes step" },
    { "path": "skills/ba-start/steps/srs-assembly.md", "baseline": 2183, "max": 2400, "label": "srs assembly step" },
    { "path": "skills/ba-start/steps/wireframes.md", "baseline": 3719, "max": 4200, "label": "wireframes step" },
    { "path": "skills/ba-start/steps/package.md", "baseline": 2766, "max": 3100, "label": "package step" },
    { "path": "skills/ba-start/steps/status.md", "baseline": 1980, "max": 2200, "label": "status step" },
    { "path": "AGENTS.md", "baseline": 2767, "max": 3600, "label": "codex runtime policy" },
    { "path": "GEMINI.md", "baseline": 2423, "max": 2900, "label": "antigravity runtime policy" },
    { "path": "CLAUDE.md", "baseline": 1948, "max": 2400, "label": "claude runtime policy" }
  ],
  "bundles": [
    {
      "name": "runtime_policies",
      "baseline": 7138,
      "max": 9000,
      "paths": ["AGENTS.md", "GEMINI.md", "CLAUDE.md"]
    },
    {
      "name": "shared_entry_runtime",
      "baseline": 25978,
      "max": 34000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "skills/ba-start/SKILL.md"]
    },
    {
      "name": "intake_runtime_bundle",
      "baseline": 32125,
      "max": 36000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/intake.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/intake.md"]
    },
    {
      "name": "backbone_runtime_bundle",
      "baseline": 33164,
      "max": 38000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/backbone.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/backbone.md"]
    },
    {
      "name": "impact_runtime_bundle",
      "baseline": 32803,
      "max": 37000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/impact.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/impact.md"]
    },
    {
      "name": "module_authoring_runtime_bundle",
      "baseline": 32625,
      "max": 37000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/module-authoring.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/frd.md", "skills/ba-start/steps/stories.md"]
    },
    {
      "name": "srs_core_bundle",
      "baseline": 34981,
      "max": 46000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/srs.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/srs.md", "skills/ba-start/steps/srs-core.md", "skills/ba-start/steps/srs-assembly.md"]
    },
    {
      "name": "srs_runtime_bundle",
      "baseline": 37981,
      "max": 50000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/srs.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/srs.md", "skills/ba-start/steps/srs-core.md", "skills/ba-start/steps/srs-wireframes.md", "skills/ba-start/steps/srs-assembly.md"]
    },
    {
      "name": "wireframes_runtime_bundle",
      "baseline": 31206,
      "max": 36000,
      "paths": ["core/contract.yaml", "core/contract-behavior.md", "core/behavior/wireframes.md", "skills/ba-start/SKILL.md", "skills/ba-start/steps/wireframes.md"]
    },
    {
      "name": "package_status_next_runtime_bundle",
      "baseline": 32329,
      "max": 36000,
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
