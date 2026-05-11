# Runtime-Neutral Token Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce BA-kit input-token/read surface for Codex, Claude Code, and Antigravity without changing lifecycle behavior, source-of-truth order, or HITL guarantees.

**Architecture:** Keep `core/contract.yaml` as the canonical data layer. Split the current monolithic behavior policy into a small shared base plus command-scoped policy shards, then update `ba-start` and runtime adapters to load only the shard required by the active command. Move deterministic checks into scripts/manifests where possible, and use token-budget CI to enforce byte-size guardrails across runtime-neutral bundles.

**Tech Stack:** Markdown playbooks, YAML/JSON contracts, Python validation scripts, PowerShell-compatible verification, existing BA-kit templates and shell budget wrapper.

---

## File Structure

- Modify: `core/contract-behavior.md`
  - Responsibility: keep only shared policy that every command must read.
- Create: `core/behavior/README.md`
  - Responsibility: document behavior shard model and runtime-neutral read order.
- Create: `core/behavior/intake.md`
  - Responsibility: intake-only routing, source extraction, and source-cache token discipline.
- Create: `core/behavior/backbone.md`
  - Responsibility: option gate, backbone generation, project memory, and index creation behavior.
- Create: `core/behavior/impact.md`
  - Responsibility: change triage, broad-read exception, governance, and file-back routing.
- Create: `core/behavior/module-authoring.md`
  - Responsibility: shared FRD, stories, and module-scoped authoring behavior.
- Create: `core/behavior/srs.md`
  - Responsibility: SRS-specific read scope, grouped generation, navigation consistency, and wireframe handoff routing.
- Create: `core/behavior/wireframes.md`
  - Responsibility: standalone wireframe constraints, design-doc handling, and wireframe-state behavior.
- Create: `core/behavior/package-status-next.md`
  - Responsibility: read-only/status/package behavior and dashboard guidance.
- Modify: `core/contract.yaml`
  - Responsibility: add behavior shard path metadata and command-to-policy mapping.
- Modify: `skills/ba-start/SKILL.md`
  - Responsibility: dispatch to `core/contract-behavior.md` plus exactly one behavior shard before reading the step file.
- Modify: `skills/ba-start/steps/srs.md`
  - Responsibility: keep router compact and defer detail to `core/behavior/srs.md`, `srs-core.md`, `srs-wireframes.md`, and `srs-assembly.md`.
- Modify: `skills/ba-start/steps/srs-core.md`
  - Responsibility: remove duplicated navigation/checklist prose now owned by `core/behavior/srs.md` or templates.
- Modify: `skills/ba-start/steps/srs-wireframes.md`
  - Responsibility: remove repeated design and navigation rules now owned by `core/behavior/srs.md` and `core/behavior/wireframes.md`.
- Modify: `templates/manifest.json`
  - Responsibility: expose template groups and deterministic routing metadata so agents do not load full templates for one group.
- Create: `scripts/check-token-budget.py`
  - Responsibility: cross-platform budget checker used by Windows, macOS, Linux, Codex, Claude Code, and Antigravity.
- Modify: `scripts/check-token-budget.sh`
  - Responsibility: thin wrapper around the Python checker.
- Modify: `core/token-budget.md`
  - Responsibility: update baselines and max values after the split, with separate budgets for shared base and behavior shards.
- Modify: `AGENTS.md`
  - Responsibility: point Codex to the new base-plus-shard read order without duplicating policy.
- Modify: `CLAUDE.md`
  - Responsibility: point Claude Code to the same base-plus-shard read order without duplicating policy.
- Modify: `GEMINI.md`
  - Responsibility: point Antigravity to the same base-plus-shard read order without duplicating policy.
- Create: `docs/runtime-token-optimization.md`
  - Responsibility: maintainer-facing explanation of the optimization, expected read bundles, and acceptance criteria.

---

### Task 1: Baseline And Safety Snapshot

**Files:**
- Read: `core/token-budget.md`
- Read: `core/contract-behavior.md`
- Read: `core/contract.yaml`
- Read: `skills/ba-start/SKILL.md`
- Read: `skills/ba-start/steps/srs-core.md`
- Read: `skills/ba-start/steps/srs-wireframes.md`

- [ ] **Step 1: Capture current budget output**

Run:

```powershell
@'
import json
import re
from pathlib import Path

root = Path.cwd()
text = (root / "core" / "token-budget.md").read_text(encoding="utf-8")
budget = json.loads(re.search(r"```json\n(.*?)\n```", text, re.S).group(1))

def size_of(rel_path):
    return (root / rel_path).stat().st_size

for item in budget["files"]:
    actual = size_of(item["path"])
    print(f"FILE {item['path']} actual={actual} max={item['max']}")

for bundle in budget["bundles"]:
    actual = sum(size_of(path) for path in bundle["paths"])
    print(f"BUNDLE {bundle['name']} actual={actual} max={bundle['max']}")
'@ | python -
```

Expected:

```text
FILE skills/ba-start/steps/srs-core.md actual=5406 max=4600
FILE skills/ba-start/steps/srs-wireframes.md actual=4525 max=4200
BUNDLE srs_wireframe_bundle actual=54825 max=54000
```

- [ ] **Step 2: Record target budget rules**

Use these target caps for the implementation:

```text
shared_entry_runtime <= 34000 bytes
contract_behavior_base <= 12000 bytes
each behavior shard <= 4500 bytes
srs_core_bundle <= 46000 bytes
srs_wireframe_bundle <= 50000 bytes
runtime_policies <= 9500 bytes
```

- [ ] **Step 3: Confirm no BA lifecycle output is being changed**

Run:

```powershell
git status --short
```

Expected: note existing dirty files before implementation. Do not revert unrelated files.

---

### Task 2: Add Cross-Platform Token Budget Checker

**Files:**
- Create: `scripts/check-token-budget.py`
- Modify: `scripts/check-token-budget.sh`

- [ ] **Step 1: Create `scripts/check-token-budget.py`**

Implement the Python checker by moving the current inline Python from `scripts/check-token-budget.sh` into a standalone file:

```python
#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def load_budget(root: Path) -> dict:
    budget_doc = root / "core" / "token-budget.md"
    text = budget_doc.read_text(encoding="utf-8")
    match = re.search(r"```json\n(.*?)\n```", text, re.S)
    if not match:
        raise SystemExit(f"Could not find JSON budget block in {budget_doc}")
    return json.loads(match.group(1))


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    budget = load_budget(root)
    failures = []

    def size_of(rel_path: str) -> int:
        path = root / rel_path
        if not path.exists():
            failures.append(f"missing path: {rel_path}")
            return 0
        return path.stat().st_size

    print("Token budget check")
    print("")

    for item in budget.get("files", []):
        actual = size_of(item["path"])
        maximum = item["max"]
        baseline = item["baseline"]
        label = item.get("label", item["path"])
        status = "fail" if actual > maximum else "ok"
        if status == "fail":
            failures.append(f"file budget exceeded: {item['path']} actual={actual} max={maximum}")
        print(f"- [{status}] {label}: {actual} bytes (baseline {baseline}, max {maximum})")

    print("")

    for bundle in budget.get("bundles", []):
        actual = sum(size_of(path) for path in bundle["paths"])
        maximum = bundle["max"]
        baseline = bundle["baseline"]
        status = "fail" if actual > maximum else "ok"
        if status == "fail":
            failures.append(f"bundle budget exceeded: {bundle['name']} actual={actual} max={maximum}")
        print(f"- [{status}] {bundle['name']}: {actual} bytes (baseline {baseline}, max {maximum})")

    if failures:
        print("")
        print("Budget failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("")
    print("Token budget checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Update shell wrapper**

Replace `scripts/check-token-budget.sh` body after `ROOT_DIR=...` with:

```bash
python3 "${ROOT_DIR}/scripts/check-token-budget.py" "${ROOT_DIR}"
```

- [ ] **Step 3: Verify on Windows through Python**

Run:

```powershell
python scripts/check-token-budget.py .
```

Expected: same pass/fail state as the old checker before budget caps are updated.

---

### Task 3: Introduce Behavior Shard Metadata

**Files:**
- Modify: `core/contract.yaml`
- Create: `core/behavior/README.md`

- [ ] **Step 1: Add behavior paths to `core/contract.yaml`**

Add these keys under `paths`:

```yaml
behavior_base: "core/contract-behavior.md"
behavior_root: "core/behavior"
behavior_intake: "core/behavior/intake.md"
behavior_backbone: "core/behavior/backbone.md"
behavior_impact: "core/behavior/impact.md"
behavior_module_authoring: "core/behavior/module-authoring.md"
behavior_srs: "core/behavior/srs.md"
behavior_wireframes: "core/behavior/wireframes.md"
behavior_package_status_next: "core/behavior/package-status-next.md"
```

- [ ] **Step 2: Add command-to-policy mapping**

Add this top-level object after `commands`:

```yaml
behavior_shards:
  intake: ["behavior_intake"]
  options: ["behavior_backbone"]
  backbone: ["behavior_backbone"]
  impact: ["behavior_impact"]
  frd: ["behavior_module_authoring"]
  stories: ["behavior_module_authoring"]
  srs: ["behavior_srs"]
  wireframes: ["behavior_wireframes"]
  package: ["behavior_package_status_next"]
  status: ["behavior_package_status_next"]
  next: ["behavior_package_status_next"]
```

- [ ] **Step 3: Create `core/behavior/README.md`**

Use this content:

```markdown
# BA-kit Behavior Shards

`core/contract-behavior.md` contains shared behavior every runtime must read.

Command-specific behavior lives in this folder. Runtime adapters must load:

1. `core/contract.yaml`
2. `core/contract-behavior.md`
3. the shard(s) listed in `behavior_shards.<command>`
4. the selected step file
5. templates and upstream artifacts only when the active step needs them

Shard files are policy overlays. They must not redefine literal paths or thresholds from `core/contract.yaml`.
```

---

### Task 4: Split Shared Behavior Policy

**Files:**
- Modify: `core/contract-behavior.md`
- Create: `core/behavior/intake.md`
- Create: `core/behavior/backbone.md`
- Create: `core/behavior/impact.md`
- Create: `core/behavior/module-authoring.md`
- Create: `core/behavior/srs.md`
- Create: `core/behavior/wireframes.md`
- Create: `core/behavior/package-status-next.md`

- [ ] **Step 1: Keep only universal policy in `core/contract-behavior.md`**

Retain these sections only:

```text
# BA-kit Contract Behavior
Required Read Order
Shared Operating Rules
Argument Parsing
Natural-Language Routing
Resolution Rules
Legacy Detection
Prerequisite Behavior
Overwrite Behavior
Context-Loss Recovery
Accepted-Scope Execution Lock
Token Discipline
Internal Artifact Compactness
Large Artifact Write Protocol
Runtime-Neutral HITL Contract
Granular Artifact Intervention
Active Push-back And Fail-Closed Behavior
Read Scope Contract introduction
Index-First Navigation Rule
Escalation Rule
```

Remove command-heavy details that are moved into shards. Keep the base file below `12000 bytes`.

- [ ] **Step 2: Create `core/behavior/intake.md`**

Include only intake-specific source handling:

```markdown
# Intake Behavior

## Read Scope

- Must read: `core/contract.yaml`, `core/contract-behavior.md`, `skills/ba-start/steps/intake.md`
- May read: `paths.source_summary`, `paths.source_chunk_index`, selected source chunks, `paths.project_memory` compact summary
- Must not read: memory shards, `log.md`, `paths.memory_index`

## Source Handling

- For large PDF, DOCX, Markdown, TXT, or pasted input, stage source material and use `ba-kit source-extract` before normalization.
- Read `paths.source_summary` first.
- Read `paths.source_chunk_index` before selecting chunk files.
- Open only chunk files needed for the current normalization pass.
- Reuse `plans/_source-cache/{source_hash}` when present.
```

- [ ] **Step 3: Create `core/behavior/backbone.md`**

Include option gate, backbone source-of-truth behavior, compact project memory, and index creation. Keep under `4500 bytes`.

- [ ] **Step 4: Create `core/behavior/impact.md`**

Include impact routing, broad-read exception, stale-artifact mapping, file-back approval, and governance preconditions. Keep under `4500 bytes`.

- [ ] **Step 5: Create `core/behavior/module-authoring.md`**

Include shared FRD/stories behavior:

```markdown
# Module Authoring Behavior

FRD and stories must start from `paths.backbone_index`. If the index is current, read targeted `paths.backbone` sections only.

Do not read unrelated module shards, `log.md`, or `cold/`.

Generated module indexes are navigators only. They must include IDs, source headings, trace hints, counts, freshness, and route hints, not duplicated requirement prose.
```

- [ ] **Step 6: Create `core/behavior/srs.md`**

Move SRS read scope, grouped execution order, navigation schema rules, validator invocation, and wireframe handoff gates here. Keep under `4500 bytes`.

- [ ] **Step 7: Create `core/behavior/wireframes.md`**

Move standalone wireframe read scope, design-doc approval, wireframe-state enum usage, and allowed outputs here. Keep under `4500 bytes`.

- [ ] **Step 8: Create `core/behavior/package-status-next.md`**

Move package/status/next read scope, index-first package behavior, and dashboard-not-source-of-truth guidance here. Keep under `4500 bytes`.

---

### Task 5: Update BA-start Dispatch

**Files:**
- Modify: `skills/ba-start/SKILL.md`

- [ ] **Step 1: Change required read order**

Replace the current read order with:

```markdown
## Required Read Order

1. Read `core/contract.yaml` for exact paths, prerequisites, defaults, states, command metadata, and `behavior_shards`.
2. Read `core/contract-behavior.md` for shared runtime-neutral policy.
3. Parse arguments and resolve the selected subcommand.
4. Read only the behavior shard(s) listed in `behavior_shards.<command>`.
5. Read only the matching file under `steps/`.
6. Read templates and upstream artifacts only when the active step actually needs them.
```

- [ ] **Step 2: Add stop condition for missing shard**

Add:

```markdown
- If `behavior_shards.<command>` references a missing path, stop and report the exact missing shard path.
```

- [ ] **Step 3: Re-run budget checker**

Run:

```powershell
python scripts/check-token-budget.py .
```

Expected: may still fail until `core/token-budget.md` is updated, but no file should exceed the old caps by more than before.

---

### Task 6: Slim SRS Step Files

**Files:**
- Modify: `skills/ba-start/steps/srs.md`
- Modify: `skills/ba-start/steps/srs-core.md`
- Modify: `skills/ba-start/steps/srs-wireframes.md`
- Modify: `skills/ba-start/steps/srs-assembly.md`

- [ ] **Step 1: Slim `srs.md` router**

Keep only prerequisites, read order, outputs, and execution order. Remove rules duplicated in `core/behavior/srs.md`.

- [ ] **Step 2: Slim `srs-core.md`**

Keep group A, B, C output expectations and the handoff to `srs-wireframes.md`. Move detailed navigation schema rules to `core/behavior/srs.md`.

Target:

```text
skills/ba-start/steps/srs-core.md <= 4200 bytes
```

- [ ] **Step 3: Slim `srs-wireframes.md`**

Keep Step 8.2, Group D, Step 9, Step 10, and field table format. Move repeated design approval and navigation mismatch rules to `core/behavior/srs.md` and `core/behavior/wireframes.md`.

Target:

```text
skills/ba-start/steps/srs-wireframes.md <= 3900 bytes
```

- [ ] **Step 4: Verify deterministic validator remains referenced once**

Run:

```powershell
rg -n "validate-navigation-consistency|NAV_SCHEMA_MISMATCH|MENU_SCHEMA_MISMATCH|MENU_ACTIVE_MISSING" core skills
```

Expected: references exist in `core/behavior/srs.md` and only minimal command invocation remains in SRS step files.

---

### Task 7: Update Runtime Adapter Instructions

**Files:**
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `GEMINI.md`

- [ ] **Step 1: Update canonical source wording**

For each runtime file, replace the `contract-behavior.md` bullet with:

```markdown
- `core/contract-behavior.md` plus the command shard in `core/behavior/` listed by `core/contract.yaml.behavior_shards`
```

- [ ] **Step 2: Add shared read-order sentence**

Add this sentence to each runtime file:

```markdown
For lifecycle work, read `contract.yaml`, then shared behavior, then only the selected command behavior shard and step file.
```

- [ ] **Step 3: Remove duplicated policy if covered by base or shards**

Delete runtime-local prose that repeats exact lifecycle policy already held in `core/contract-behavior.md` or shards. Keep runtime files as adapters, not second policy sources.

Target:

```text
AGENTS.md <= 3600 bytes
CLAUDE.md <= 2400 bytes
GEMINI.md <= 2900 bytes
runtime_policies <= 9000 bytes
```

---

### Task 8: Update Budget Baselines

**Files:**
- Modify: `core/token-budget.md`

- [ ] **Step 1: Add new files to budget JSON**

Add entries for:

```json
{ "path": "core/behavior/intake.md", "baseline": 0, "max": 4500, "label": "intake behavior shard" }
{ "path": "core/behavior/backbone.md", "baseline": 0, "max": 4500, "label": "backbone behavior shard" }
{ "path": "core/behavior/impact.md", "baseline": 0, "max": 4500, "label": "impact behavior shard" }
{ "path": "core/behavior/module-authoring.md", "baseline": 0, "max": 4500, "label": "module authoring behavior shard" }
{ "path": "core/behavior/srs.md", "baseline": 0, "max": 4500, "label": "srs behavior shard" }
{ "path": "core/behavior/wireframes.md", "baseline": 0, "max": 4500, "label": "wireframes behavior shard" }
{ "path": "core/behavior/package-status-next.md", "baseline": 0, "max": 4500, "label": "package status next behavior shard" }
```

After implementation, replace `baseline: 0` with actual byte sizes reported by `python scripts/check-token-budget.py .`.

- [ ] **Step 2: Replace old bundle definitions**

Define runtime bundles by command:

```json
{
  "name": "srs_runtime_bundle",
  "baseline": 0,
  "max": 50000,
  "paths": [
    "core/contract.yaml",
    "core/contract-behavior.md",
    "core/behavior/srs.md",
    "skills/ba-start/SKILL.md",
    "skills/ba-start/steps/srs.md",
    "skills/ba-start/steps/srs-core.md",
    "skills/ba-start/steps/srs-wireframes.md",
    "skills/ba-start/steps/srs-assembly.md"
  ]
}
```

Add similar bundles for `intake`, `backbone`, `impact`, `module_authoring`, `wireframes`, and `package_status_next`.

- [ ] **Step 3: Run budget checker**

Run:

```powershell
python scripts/check-token-budget.py .
```

Expected:

```text
Token budget checks passed.
```

---

### Task 9: Runtime Parity Documentation

**Files:**
- Create: `docs/runtime-token-optimization.md`

- [ ] **Step 1: Document read bundles**

Create a table:

```markdown
| Command | Required behavior shard | Must not load by default |
| --- | --- | --- |
| intake | `core/behavior/intake.md` | memory shards, `log.md`, full raw source when cached summary exists |
| backbone | `core/behavior/backbone.md` | downstream module artifacts |
| impact | `core/behavior/impact.md` | `cold/` unless escalated |
| frd/stories | `core/behavior/module-authoring.md` | unrelated module shards |
| srs | `core/behavior/srs.md` | full backbone/stories when indexes are current |
| wireframes | `core/behavior/wireframes.md` | unrelated module shards |
| package/status/next | `core/behavior/package-status-next.md` | full source-of-truth artifacts when indexes are current |
```

- [ ] **Step 2: Add runtime-neutral acceptance criteria**

Use:

```markdown
## Acceptance Criteria

- Codex, Claude Code, and Antigravity point to the same contract and shard mapping.
- Runtime adapter files do not duplicate lifecycle policy already present in `core/`.
- `python scripts/check-token-budget.py .` passes on Windows without Bash.
- `scripts/check-token-budget.sh` remains usable on Unix-like environments.
- SRS and wireframe bundles are below the new command-scoped caps.
- No command requires loading unrelated memory shards or full source-of-truth artifacts when a current index exists.
```

---

### Task 10: Final Verification

**Files:**
- Verify: all modified files

- [ ] **Step 1: Run budget verification**

Run:

```powershell
python scripts/check-token-budget.py .
```

Expected:

```text
Token budget checks passed.
```

- [ ] **Step 2: Verify shell wrapper syntax remains simple**

Run:

```powershell
Get-Content scripts/check-token-budget.sh
```

Expected: wrapper calls `scripts/check-token-budget.py` and contains no large inline checker logic.

- [ ] **Step 3: Verify no stale old read-order instruction remains**

Run:

```powershell
rg -n "Read `core/contract.yaml` for exact values\\.|Read `core/contract-behavior.md` for shared LLM policy\\.|Read only the step file" core skills AGENTS.md CLAUDE.md GEMINI.md
```

Expected: no old monolithic read-order wording remains outside historical docs.

- [ ] **Step 4: Verify shard mapping coverage**

Run:

```powershell
@'
import yaml
from pathlib import Path

contract = yaml.safe_load(Path("core/contract.yaml").read_text(encoding="utf-8"))
commands = set(contract["commands"])
mapped = set(contract["behavior_shards"])
missing = sorted(commands - mapped)
extra = sorted(mapped - commands)
if missing or extra:
    raise SystemExit(f"missing={missing} extra={extra}")
for command, shard_keys in contract["behavior_shards"].items():
    for shard_key in shard_keys:
        rel = contract["paths"][shard_key]
        if not Path(rel).exists():
            raise SystemExit(f"{command} references missing shard {rel}")
print("behavior shard mapping ok")
'@ | python -
```

Expected:

```text
behavior shard mapping ok
```

- [ ] **Step 5: Review diff for behavior drift**

Run:

```powershell
git diff -- core/contract-behavior.md core/behavior skills/ba-start AGENTS.md CLAUDE.md GEMINI.md
```

Expected: changes reduce read surface and move policy ownership; they do not remove lifecycle guarantees, exact resolution rules, impact-first routing, overwrite gates, project memory governance, or fail-closed behavior.

---

## Commit Plan

- [ ] Commit 1: `test: add cross-platform token budget checker`
- [ ] Commit 2: `refactor: split BA-kit behavior into command shards`
- [ ] Commit 3: `refactor: slim SRS instruction surface`
- [ ] Commit 4: `docs: document runtime-neutral token optimization`
- [ ] Commit 5: `chore: update token budget baselines`

---

## Self-Review

Spec coverage:

- Reduces input-token/read surface for Codex, Claude Code, and Antigravity.
- Keeps runtime-neutral contract and avoids duplicating policy in adapter files.
- Addresses current budget failures in `srs-core.md`, `srs-wireframes.md`, and `srs_wireframe_bundle`.
- Adds Windows-compatible budget verification.
- Keeps BA lifecycle behavior, impact routing, HITL, governance, and source-of-truth order intact.

Placeholder scan:

- No task uses `TBD`, `TODO`, `implement later`, or unspecified test language.

Type and path consistency:

- `behavior_shards` keys reference path keys under `paths`.
- Commands in `behavior_shards` match `commands`.
- Runtime adapters point to `core/contract.yaml`, `core/contract-behavior.md`, command shards, and step files in the same order.
