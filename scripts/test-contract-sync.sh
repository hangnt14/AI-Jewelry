#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

legacy_hits="$(
  cd "${ROOT_DIR}" &&
    rg -n "artifact-contract\\.md|plans/reports/final|plans/reports/drafts|plans/\\{date\\}-\\{slug\\}" \
      AGENTS.md GEMINI.md CLAUDE.md skills core scripts codex templates \
      --glob '!core/contract.yaml' \
      --glob '!rules/ba-workflow.md' \
      --glob '!scripts/test-contract-sync.sh' \
      || true
)"

if [[ -n "${legacy_hits}" ]]; then
  echo "Unexpected legacy contract references found:" >&2
  echo "${legacy_hits}" >&2
  exit 1
fi

python3 - "${ROOT_DIR}/templates/manifest.json" "${ROOT_DIR}/templates" <<'PY'
import json
import re
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
templates_dir = Path(sys.argv[2])
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
heading_re = re.compile(r"^(#{1,6})\s+(.+)$")

for template_name, info in manifest.items():
    template_path = templates_dir / template_name
    if not template_path.exists():
        raise SystemExit(f"Missing template from manifest: {template_path}")
    headings = {
        line.strip()
        for line in template_path.read_text(encoding="utf-8").splitlines()
        if heading_re.match(line.strip())
    }
    for group_name, group_info in info.get("groups", {}).items():
        for heading in group_info.get("headings", []):
            if heading not in headings:
                raise SystemExit(
                    f"Manifest heading not found: template={template_name} group={group_name} heading={heading}"
                )
PY

python3 - "${ROOT_DIR}/core/contract.yaml" <<'PY'
import json
import sys
from pathlib import Path

contract_path = Path(sys.argv[1])
contract = json.loads(contract_path.read_text(encoding="utf-8"))
paths = contract.get("paths", {})
commands = contract.get("commands", {})
required_paths = {
    "source_chunk_index",
    "backbone_index",
    "stories_index",
    "srs_index",
}
missing_paths = sorted(required_paths - set(paths))
if missing_paths:
    raise SystemExit(f"Missing token optimization path(s): {', '.join(missing_paths)}")

required_outputs = {
    "intake": {"source_summary", "source_chunks_dir", "source_chunk_index"},
    "backbone": {"backbone", "backbone_index"},
    "stories": {"stories", "stories_index"},
    "srs": {"srs", "srs_group", "wireframe_input", "srs_index"},
}
for command, expected in required_outputs.items():
    outputs = set(commands.get(command, {}).get("outputs", []))
    missing = sorted(expected - outputs)
    if missing:
        raise SystemExit(
            f"Command '{command}' missing token optimization output(s): {', '.join(missing)}"
        )

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

activation = contract.get("activation", {})
signals = set(activation.get("signals", {}))
thresholds = activation.get("thresholds", {})
operators = {"gte", "equals"}


def validate_rule(rule, path):
    if not isinstance(rule, dict):
        raise SystemExit(f"Activation threshold rule must be an object: {path}")

    branch_keys = {"any_of", "all_of"} & set(rule)
    if branch_keys:
        if len(branch_keys) != 1 or len(rule) != 1:
            raise SystemExit(f"Activation threshold branch must contain only one branch key: {path}")
        key = next(iter(branch_keys))
        children = rule[key]
        if not isinstance(children, list) or not children:
            raise SystemExit(f"Activation threshold branch must be a non-empty list: {path}.{key}")
        for index, child in enumerate(children):
            validate_rule(child, f"{path}.{key}[{index}]")
        return

    required = {"signal", "operator", "value"}
    if set(rule) != required:
        raise SystemExit(f"Activation threshold leaf must contain exactly signal/operator/value: {path}")
    if rule["signal"] not in signals:
        raise SystemExit(f"Activation threshold references unknown signal '{rule['signal']}': {path}")
    if rule["operator"] not in operators:
        raise SystemExit(f"Activation threshold uses unsupported operator '{rule['operator']}': {path}")
    if rule["operator"] == "gte" and (not isinstance(rule["value"], (int, float)) or isinstance(rule["value"], bool)):
        raise SystemExit(f"Activation threshold gte value must be numeric: {path}")


for level in ("modular", "program"):
    if level not in thresholds:
        raise SystemExit(f"Missing activation threshold level: {level}")
    validate_rule(thresholds[level], f"activation.thresholds.{level}")
PY

python3 - "${ROOT_DIR}/templates/manifest.json" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
required_templates = {
    "source-chunk-index-template.md",
    "backbone-index-template.md",
    "user-stories-index-template.md",
    "srs-index-template.md",
}
missing = sorted(required_templates - set(manifest))
if missing:
    raise SystemExit(f"Missing token optimization template(s): {', '.join(missing)}")
PY

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

python3 - "${ROOT_DIR}" <<'PY'
import sys
from pathlib import Path

root = Path(sys.argv[1])
checks = {
    "core/contract-behavior.md": ["paths.backbone_index", "paths.stories_index", "paths.srs_index"],
    "skills/ba-start/steps/backbone.md": ["paths.backbone_index"],
    "skills/ba-start/steps/frd.md": ["paths.backbone_index"],
    "skills/ba-start/steps/stories.md": ["paths.backbone_index", "paths.stories_index"],
    "skills/ba-start/steps/srs.md": ["paths.backbone_index", "paths.stories_index", "paths.srs_index", "paths.design_doc"],
    "skills/ba-start/steps/srs-core.md": ["validate-navigation-consistency.py", "MENU_SCHEMA_GAP"],
    "skills/ba-start/steps/srs-assembly.md": ["validate-navigation-consistency.py", "MENU_SCHEMA_MISMATCH"],
    "skills/ba-start/steps/wireframes.md": ["validate-navigation-consistency.py"],
    "skills/ba-start/steps/package.md": ["paths.backbone_index", "paths.stories_index", "paths.srs_index"],
    "skills/ba-start/steps/impact.md": ["affected_node_ids", "owner_artifact", "stale_artifacts", "read_escalation"],
}
for rel_path, tokens in checks.items():
    text = (root / rel_path).read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    if missing:
        raise SystemExit(f"{rel_path} missing index-first token(s): {', '.join(missing)}")
PY

SOURCE_FIXTURE="${TMP_DIR}/large-source.md"
{
  printf '# Large Source\n\n'
  for i in $(seq 1 24); do
    printf '## Section %02d\n\n' "${i}"
    printf 'Requirement %02d explains actor behavior, validation rules, workflow constraints, and reporting expectations for the BA source extraction test.\n\n' "${i}"
  done
} >"${SOURCE_FIXTURE}"

SOURCE_CACHE_ROOT="${TMP_DIR}/source-cache/{source_hash}"
SOURCE_EXTRACT_MANIFEST="${TMP_DIR}/source-extract-manifest.json"
python3 "${ROOT_DIR}/scripts/source-extract.py" "${SOURCE_FIXTURE}" \
  --cache-root "${SOURCE_CACHE_ROOT}" \
  --chunk-chars 900 >"${SOURCE_EXTRACT_MANIFEST}"
SOURCE_CACHE_DIR="$(python3 - "${SOURCE_EXTRACT_MANIFEST}" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(manifest["cache_dir"])
PY
)"
if [[ ! -f "${SOURCE_CACHE_DIR}/chunk-index.md" ]]; then
  echo "Missing source chunk index: ${SOURCE_CACHE_DIR}/chunk-index.md" >&2
  exit 1
fi

python3 -m py_compile \
  "${ROOT_DIR}/scripts/source-extract.py" \
  "${ROOT_DIR}/scripts/context-budget.py" \
  "${ROOT_DIR}/scripts/design-snapshot.py" \
  "${ROOT_DIR}/scripts/validate-navigation-consistency.py" \
  "${ROOT_DIR}/scripts/stitch-state.py" \
  "${ROOT_DIR}/scripts/runtime-parity-normalize.py"

CONTEXT_BUDGET_OUTPUT="$(
  python3 "${ROOT_DIR}/scripts/context-budget.py" --repo "${ROOT_DIR}" --command status
)"
if [[ "${CONTEXT_BUDGET_OUTPUT}" != *"| Profile |"* ]]; then
  echo "context-budget output missing Profile column" >&2
  exit 1
fi

bash -n "${ROOT_DIR}/scripts/ba-kit"
bash -n "${ROOT_DIR}/scripts/check-token-budget.sh"
bash -n "${ROOT_DIR}/install.sh"
bash -n "${ROOT_DIR}/scripts/install-codex-ba-kit.sh"
bash -n "${ROOT_DIR}/scripts/install-antigravity-ba-kit.sh"
bash -n "${ROOT_DIR}/scripts/install-plantuml.sh"
bash -n "${ROOT_DIR}/scripts/generate-codex-assets.sh"
bash -n "${ROOT_DIR}/scripts/test-activation-thresholds.sh"
bash -n "${ROOT_DIR}/scripts/test-runtime-parity.sh"
bash -n "${ROOT_DIR}/scripts/runtime-parity-adapter.sh"
bash -n "${ROOT_DIR}/scripts/test-runtime-install-smoke.sh"
bash -n "${ROOT_DIR}/scripts/test-navigation-consistency.sh"
bash "${ROOT_DIR}/scripts/check-token-budget.sh" >/dev/null
bash "${ROOT_DIR}/scripts/test-activation-thresholds.sh" >/dev/null
bash "${ROOT_DIR}/scripts/test-options-flow-contract.sh" >/dev/null
bash "${ROOT_DIR}/scripts/test-navigation-consistency.sh" >/dev/null
bash "${ROOT_DIR}/scripts/test-runtime-parity.sh" --check-structure >/dev/null
bash "${ROOT_DIR}/scripts/test-runtime-parity.sh" >/dev/null

cp "${ROOT_DIR}/codex/skills/ba-start/SKILL.md" "${TMP_DIR}/ba-start.before"
bash "${ROOT_DIR}/scripts/generate-codex-assets.sh" >"${TMP_DIR}/generator.log"
cmp "${TMP_DIR}/ba-start.before" "${ROOT_DIR}/codex/skills/ba-start/SKILL.md" >/dev/null
bash "${ROOT_DIR}/scripts/test-runtime-install-smoke.sh" >/dev/null

echo "Contract sync checks passed."
