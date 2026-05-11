# BA-kit Internal Artifact Compactness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an artifact-purpose policy so BA-kit keeps generated internal artifacts compact, structured, and format-appropriate.

**Architecture:** Add `artifact_profiles` to the machine contract, enforce profile coverage and compact internal template rules in contract-sync tests, and document runtime behavior in the behavior contract and step files. Keep user-facing BA deliverables unchanged; this plan only governs generated internal artifacts and metadata visibility.

**Tech Stack:** JSON contract stored in `core/contract.yaml`, Markdown behavior/step/template files, Bash test harness, Python helper scripts.

---

## File Structure

- Modify `core/contract.yaml`: add `artifact_profiles` mapping for path keys and optional profile metadata thresholds.
- Modify `core/contract-behavior.md`: add compact internal artifact rules and format policy.
- Modify `scripts/test-contract-sync.sh`: validate artifact profile coverage, profile values, selected internal template size limits, and freshness fields.
- Modify `scripts/context-budget.py`: include artifact profile in the context budget table.
- Modify `skills/ba-start/steps/backbone.md`: require compact `paths.project_memory` and `paths.backbone_index`.
- Modify `skills/ba-start/steps/stories.md`: require compact `paths.stories_index`.
- Modify `skills/ba-start/steps/srs.md`: require compact `paths.srs_index`.
- Modify `skills/ba-start/steps/wireframes.md`: require compact state/map artifacts.
- Modify `core/token-budget.md`: refresh baselines only if intentional contract growth trips guardrails.
- No user-facing deliverable templates should be compacted in this phase.

## Task 1: Contract Profile Test Coverage

**Files:**
- Modify: `scripts/test-contract-sync.sh`
- Modify later: `core/contract.yaml`

- [ ] **Step 1: Add failing profile validation to contract-sync**

Insert this Python validation after the existing `required_outputs` validation in `scripts/test-contract-sync.sh`:

```python
profiles = contract.get("artifact_profiles", {})
allowed_profiles = {"user_facing", "agent_facing", "machine_facing"}
required_profile_keys = {
    "source_manifest",
    "source_summary",
    "source_chunk_index",
    "project_home",
    "collab_home",
    "module_home",
    "review_packet",
    "intake",
    "plan",
    "options_index",
    "option_item",
    "options_comparison",
    "backbone",
    "backbone_index",
    "frd",
    "stories",
    "stories_index",
    "srs",
    "srs_index",
    "srs_group",
    "wireframe_input",
    "wireframe_map",
    "wireframe_state",
    "compiled_frd",
    "compiled_srs",
    "design_doc",
    "project_memory",
    "memory_index",
    "memory_log",
    "memory_hot_vocabulary",
    "memory_hot_decisions",
    "memory_hot_pushback",
    "memory_module_warm",
}
missing_profiles = sorted(required_profile_keys - set(profiles))
if missing_profiles:
    raise SystemExit(f"Missing artifact profile(s): {', '.join(missing_profiles)}")
invalid_profiles = {
    key: value
    for key, value in profiles.items()
    if value not in allowed_profiles
}
if invalid_profiles:
    details = ", ".join(f"{key}={value}" for key, value in sorted(invalid_profiles.items()))
    raise SystemExit(f"Invalid artifact profile value(s): {details}")
unknown_profile_keys = sorted(set(profiles) - set(paths))
if unknown_profile_keys:
    raise SystemExit(f"Artifact profiles reference unknown path key(s): {', '.join(unknown_profile_keys)}")

expected_profiles = {
    "source_manifest": "machine_facing",
    "compiled_frd": "user_facing",
    "compiled_srs": "user_facing",
    "backbone_index": "agent_facing",
    "stories_index": "agent_facing",
    "srs_index": "agent_facing",
    "wireframe_state": "machine_facing",
}
for key, expected in expected_profiles.items():
    actual = profiles.get(key)
    if actual != expected:
        raise SystemExit(f"Artifact profile mismatch for {key}: expected {expected}, got {actual}")
```

- [ ] **Step 2: Run contract-sync to verify failure**

Run with the Windows python shim:

```powershell
$tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP 'bakit-python-shim')
Copy-Item C:\Users\DPC\nhq\venv\python.exe (Join-Path $tmp.FullName 'python3.exe') -Force
$env:PATH = "$($tmp.FullName);$env:PATH"
& 'C:\Program Files\Git\bin\bash.exe' scripts/test-contract-sync.sh
```

Expected: FAIL with `Missing artifact profile(s)` because `core/contract.yaml` does not yet define `artifact_profiles`.

- [ ] **Step 3: Commit failing test**

```bash
git add scripts/test-contract-sync.sh
git commit -m "test: require BA-kit artifact profiles"
```

## Task 2: Add Artifact Profiles And Behavior Policy

**Files:**
- Modify: `core/contract.yaml`
- Modify: `core/contract-behavior.md`
- Modify: `scripts/test-contract-sync.sh`

- [ ] **Step 1: Add `artifact_profiles` to the contract**

Add this object near `paths` or before `commands` in `core/contract.yaml`:

```json
  "artifact_profiles": {
    "source_manifest": "machine_facing",
    "source_summary": "agent_facing",
    "source_chunk_index": "agent_facing",
    "project_home": "user_facing",
    "collab_home": "user_facing",
    "module_home": "user_facing",
    "review_packet": "agent_facing",
    "intake": "user_facing",
    "plan": "agent_facing",
    "options_index": "agent_facing",
    "option_item": "user_facing",
    "options_comparison": "user_facing",
    "backbone": "user_facing",
    "backbone_index": "agent_facing",
    "frd": "user_facing",
    "stories": "user_facing",
    "stories_index": "agent_facing",
    "srs": "user_facing",
    "srs_index": "agent_facing",
    "srs_group": "user_facing",
    "wireframe_input": "agent_facing",
    "wireframe_map": "agent_facing",
    "wireframe_state": "machine_facing",
    "compiled_frd": "user_facing",
    "compiled_srs": "user_facing",
    "design_doc": "agent_facing",
    "project_memory": "agent_facing",
    "memory_index": "agent_facing",
    "memory_log": "agent_facing",
    "memory_hot_vocabulary": "agent_facing",
    "memory_hot_decisions": "agent_facing",
    "memory_hot_pushback": "agent_facing",
    "memory_module_warm": "agent_facing"
  },
```

Keep valid JSON syntax. If the insertion is before another property, include the trailing comma.

- [ ] **Step 2: Add behavior contract rule**

Add a new subsection under `## Token Discipline` in `core/contract-behavior.md`:

```markdown
### Internal Artifact Compactness

Artifact profile controls format and length:

- `user_facing`: deliverable or package output; write complete BA-readable content.
- `agent_facing`: navigator, packet, memory shard, or state summary; write compact tables/lists with IDs, paths, freshness, ownership, and route hints only.
- `machine_facing`: deterministic state or manifest; prefer JSON/YAML/NDJSON and avoid prose beyond stable labels.

For generated internal artifacts:

- keep `.md` only when fast human inspection is useful
- never duplicate source-of-truth requirement text from intake, backbone, stories, or SRS
- keep excerpts short and only when needed for routing
- include stale/unknown status instead of guessing
- if substantial prose is needed, move that prose into the source-of-truth artifact or revise the command flow
```

- [ ] **Step 3: Run contract-sync**

Run:

```powershell
$tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP 'bakit-python-shim')
Copy-Item C:\Users\DPC\nhq\venv\python.exe (Join-Path $tmp.FullName 'python3.exe') -Force
$env:PATH = "$($tmp.FullName);$env:PATH"
& 'C:\Program Files\Git\bin\bash.exe' scripts/test-contract-sync.sh
```

Expected: PASS through artifact profile validation. If token budget fails because the behavior contract grew, update `core/token-budget.md` in Task 5 instead of weakening this rule.

- [ ] **Step 4: Commit profile implementation**

```bash
git add core/contract.yaml core/contract-behavior.md
git commit -m "feat: classify BA-kit artifacts by audience profile"
```

## Task 3: Compact Internal Template Guardrails

**Files:**
- Modify: `scripts/test-contract-sync.sh`
- Modify: internal templates under `templates/` that exceed the compact limits

- [ ] **Step 1: Add failing compact template checks**

Add this Python block after the existing required-template check in `scripts/test-contract-sync.sh`:

```python
python3 - "${ROOT_DIR}/templates" <<'PY'
import sys
from pathlib import Path

templates_dir = Path(sys.argv[1])
max_bytes = {
    "source-chunk-index-template.md": 1800,
    "backbone-index-template.md": 1800,
    "user-stories-index-template.md": 1800,
    "srs-index-template.md": 1800,
    "project-memory-index-template.md": 2600,
    "project-memory-template.md": 2600,
    "project-memory-hot-canonical-vocabulary-template.md": 2200,
    "project-memory-hot-approved-decisions-template.md": 2200,
    "project-memory-hot-pushback-triggers-template.md": 2200,
    "project-memory-module-template.md": 2200,
    "wireframe-map-template.md": 3600,
    "review-packet-template.md": 2600,
    "sub-agent-handoff-template.md": 2600,
}
required_tokens = {
    "source-chunk-index-template.md": ["index_type", "source_artifact", "generated_at", "stale_status"],
    "backbone-index-template.md": ["index_type", "source_artifact", "generated_at", "stale_status"],
    "user-stories-index-template.md": ["index_type", "source_artifact", "generated_at", "stale_status"],
    "srs-index-template.md": ["index_type", "source_artifact", "generated_at", "stale_status"],
}
for name, limit in max_bytes.items():
    path = templates_dir / name
    if not path.exists():
        raise SystemExit(f"Missing compact internal template: {name}")
    size = len(path.read_bytes())
    if size > limit:
        raise SystemExit(f"Internal template too large: {name} actual={size} max={limit}")
for name, tokens in required_tokens.items():
    text = (templates_dir / name).read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    if missing:
        raise SystemExit(f"Internal template missing freshness token(s): {name}: {', '.join(missing)}")
PY
```

- [ ] **Step 2: Run contract-sync and record failures**

Run:

```powershell
$tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP 'bakit-python-shim')
Copy-Item C:\Users\DPC\nhq\venv\python.exe (Join-Path $tmp.FullName 'python3.exe') -Force
$env:PATH = "$($tmp.FullName);$env:PATH"
& 'C:\Program Files\Git\bin\bash.exe' scripts/test-contract-sync.sh
```

Expected: FAIL for the current oversized internal templates:

```text
Internal template too large: project-memory-index-template.md actual=3223 max=2600
Internal template too large: project-memory-template.md actual=3838 max=2600
Internal template too large: project-memory-hot-approved-decisions-template.md actual=2215 max=2200
Internal template too large: project-memory-module-template.md actual=2466 max=2200
```

- [ ] **Step 3: Compact only failing internal templates**

Edit only the four oversized internal templates listed in Step 2. Preserve each file's first heading exactly as registered in `templates/manifest.json`.

For `project-memory-template.md`, keep only metadata plus these tables: `Canonical Vocabulary`, `Approved Decisions`, `Accepted Assumptions`, `Corrections And Pushback`. Remove the narrative purpose section and runtime handoff prose.

For `project-memory-index-template.md`, keep only metadata plus these tables: `Activation State`, `Shard Registry`, `Module Shards`, `Owner Metadata`, `Packet Registry`. Remove duplicated `Shard Health`, `Read Guide`, and prose paragraphs.

For `project-memory-hot-approved-decisions-template.md`, keep only metadata plus these tables: `Decision Table`, `Accepted Assumptions`, `Rejected Assumptions`, `Accepted Corrections`. Remove usage notes.

For `project-memory-module-template.md`, keep only metadata plus these tables: `Module Scope`, `Key Module Decisions`, `Cross-Module Dependencies`, `Trace Links`, `Open Issues`, `Promotion Trace`. Remove ownership prose and long module scope instructions.

Do not compact user-facing templates such as `srs-template.md`, `frd-template.md`, `requirements-backbone-template.md`, `user-story-template.md`, `project-home-template.md`, `collab-home-template.md`, or `module-home-template.md`.

- [ ] **Step 4: Run contract-sync again**

Run the same `scripts/test-contract-sync.sh` command.

Expected: PASS.

- [ ] **Step 5: Commit guardrails**

```bash
git add scripts/test-contract-sync.sh templates
git commit -m "test: guard compact internal artifact templates"
```

## Task 4: Surface Artifact Profiles In Context Budget

**Files:**
- Modify: `scripts/context-budget.py`
- Modify: `scripts/test-contract-sync.sh`

- [ ] **Step 1: Add failing smoke assertion for profile column**

Replace the current smoke line in `scripts/test-contract-sync.sh`:

```bash
python3 "${ROOT_DIR}/scripts/context-budget.py" --repo "${ROOT_DIR}" --command status >/dev/null
```

with:

```bash
CONTEXT_BUDGET_OUTPUT="$(
  python3 "${ROOT_DIR}/scripts/context-budget.py" --repo "${ROOT_DIR}" --command status
)"
if [[ "${CONTEXT_BUDGET_OUTPUT}" != *"| Profile |"* ]]; then
  echo "context-budget output missing Profile column" >&2
  exit 1
fi
```

- [ ] **Step 2: Run contract-sync to verify failure**

Run:

```powershell
$tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP 'bakit-python-shim')
Copy-Item C:\Users\DPC\nhq\venv\python.exe (Join-Path $tmp.FullName 'python3.exe') -Force
$env:PATH = "$($tmp.FullName);$env:PATH"
& 'C:\Program Files\Git\bin\bash.exe' scripts/test-contract-sync.sh
```

Expected: FAIL with `context-budget output missing Profile column`.

- [ ] **Step 3: Update `context-budget.py` output**

Change `scripts/context-budget.py` so it loads profiles and prints a profile column:

```python
    profiles = contract.get("artifact_profiles", {})

    rows = []
    total = 0
    for key in COMMAND_SCOPES[args.command]:
        template = paths.get(key)
        if not template:
            continue
        rendered = render_path(template, slug=args.slug, date=args.date, module=args.module)
        size = 0 if "{" in rendered else size_for(repo, rendered)
        total += size
        rows.append((key, profiles.get(key, "unclassified"), rendered, size))

    print(f"Context budget for command: {args.command}")
    print("")
    print("| Path Key | Profile | Resolved Path | Bytes |")
    print("| --- | --- | --- | --- |")
    for key, profile, rendered, size in rows:
        print(f"| {key} | {profile} | `{rendered}` | {size} |")
    print(f"| TOTAL | | | {total} |")
```

- [ ] **Step 4: Run contract-sync**

Run the same `scripts/test-contract-sync.sh` command.

Expected: PASS through the context-budget smoke.

- [ ] **Step 5: Commit context budget profile output**

```bash
git add scripts/context-budget.py scripts/test-contract-sync.sh
git commit -m "feat: show artifact profiles in context budget"
```

## Task 5: Step Rules, Budget Refresh, And Final Verification

**Files:**
- Modify: `skills/ba-start/steps/backbone.md`
- Modify: `skills/ba-start/steps/stories.md`
- Modify: `skills/ba-start/steps/srs.md`
- Modify: `skills/ba-start/steps/wireframes.md`
- Modify: `core/token-budget.md` when the verified byte budget changes because of intentional contract growth

- [ ] **Step 1: Add compactness instructions to generation steps**

Add one short rule to each relevant step file:

```markdown
- Treat generated index/state/memory artifacts as `agent_facing` or `machine_facing`; keep them compact and do not duplicate source-of-truth requirement text.
```

Apply this to:

- `skills/ba-start/steps/backbone.md`
- `skills/ba-start/steps/stories.md`
- `skills/ba-start/steps/srs.md`
- `skills/ba-start/steps/wireframes.md`

- [ ] **Step 2: Run token budget check**

Run:

```powershell
$tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP 'bakit-python-shim')
Copy-Item C:\Users\DPC\nhq\venv\python.exe (Join-Path $tmp.FullName 'python3.exe') -Force
$env:PATH = "$($tmp.FullName);$env:PATH"
& 'C:\Program Files\Git\bin\bash.exe' scripts/check-token-budget.sh
```

Expected: PASS. If it fails because of intentional contract growth, update `core/token-budget.md` baselines and max values using the actual output with modest headroom.

- [ ] **Step 3: Run full contract sync**

Run:

```powershell
$tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP 'bakit-python-shim')
Copy-Item C:\Users\DPC\nhq\venv\python.exe (Join-Path $tmp.FullName 'python3.exe') -Force
$env:PATH = "$($tmp.FullName);$env:PATH"
& 'C:\Program Files\Git\bin\bash.exe' scripts/test-contract-sync.sh
```

Expected: `Contract sync checks passed.`

- [ ] **Step 4: Run runtime parity checks**

Run:

```powershell
$tmp = New-Item -ItemType Directory -Force -Path (Join-Path $env:TEMP 'bakit-python-shim')
Copy-Item C:\Users\DPC\nhq\venv\python.exe (Join-Path $tmp.FullName 'python3.exe') -Force
$env:PATH = "$($tmp.FullName);$env:PATH"
& 'C:\Program Files\Git\bin\bash.exe' scripts/test-runtime-parity.sh --check-structure
& 'C:\Program Files\Git\bin\bash.exe' scripts/test-runtime-parity.sh
```

Expected: structure check passes and full parity ends with `Status: PASS.`

- [ ] **Step 5: Run whitespace and status checks**

Run:

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only intended files are modified.

- [ ] **Step 6: Commit final step/budget changes**

```bash
git add skills/ba-start/steps core/token-budget.md
git commit -m "docs: enforce compact internal artifact generation"
```

If `core/token-budget.md` did not change, omit it from `git add`.

## Final Verification

- [ ] Run `scripts/check-token-budget.sh`.
- [ ] Run `scripts/test-contract-sync.sh`.
- [ ] Run `scripts/test-runtime-parity.sh --check-structure`.
- [ ] Run `scripts/test-runtime-parity.sh`.
- [ ] Run `git status --short` and confirm no uncommitted implementation changes remain.
