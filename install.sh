#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_HOME="${HOME}/.claude"
SKILLS_TARGET="${TARGET_HOME}/skills"
RULES_TARGET="${TARGET_HOME}/rules/ba-kit"
AGENTS_TARGET="${TARGET_HOME}/agents"
TEMPLATES_TARGET="${TARGET_HOME}/templates"
CORE_SOURCE="${ROOT_DIR}/core"
CORE_TARGET="${TARGET_HOME}/ba-kit"
LOCAL_BIN_TARGET="${HOME}/.local/bin"
STATE_TARGET="${HOME}/.local/share/ba-kit/installations"
STALE_TEMPLATE_FILES=(
  "wireframe-input-template.md"
  "wireframe-map-template.md"
)
STALE_CORE_PATHS=(
  "references"
)
MANAGED_SKILL_DIRS=(
  "ba-*"
  "brainstorm"
  "reverse-web"
  "qc-uc-review"
)

cleanup_managed_skill_dirs() {
  local pattern path

  mkdir -p "${SKILLS_TARGET}"
  shopt -s nullglob
  for pattern in "${MANAGED_SKILL_DIRS[@]}"; do
    for path in "${SKILLS_TARGET}"/${pattern}; do
      [[ -e "${path}" ]] || continue
      rm -rf "${path}"
    done
  done
  shopt -u nullglob
}

cleanup_managed_agent_files() {
  local agent_path

  mkdir -p "${AGENTS_TARGET}"
  shopt -s nullglob
  for agent_path in "${ROOT_DIR}"/agents/*; do
    [[ -f "${agent_path}" ]] || continue
    rm -f "${AGENTS_TARGET}/$(basename "${agent_path}")"
  done
  shopt -u nullglob
}

cleanup_managed_template_files() {
  local template_path

  mkdir -p "${TEMPLATES_TARGET}"
  shopt -s nullglob
  for template_path in "${ROOT_DIR}"/templates/*; do
    [[ -f "${template_path}" ]] || continue
    rm -f "${TEMPLATES_TARGET}/$(basename "${template_path}")"
  done
  shopt -u nullglob
}

cleanup_previous_install() {
  cleanup_managed_skill_dirs
  cleanup_managed_agent_files
  cleanup_managed_template_files
  rm -rf "${RULES_TARGET}" "${CORE_TARGET}"
}

copy_tree() {
  local source_dir="$1"
  local target_dir="$2"

  mkdir -p "$target_dir"
  cp -R "${source_dir}/." "$target_dir/"
}

remove_stale_templates() {
  local target_dir="$1"
  local file_name

  for file_name in "${STALE_TEMPLATE_FILES[@]}"; do
    rm -f "${target_dir}/${file_name}"
  done
}

remove_stale_core_paths() {
  local target_dir="$1"
  local path_name

  for path_name in "${STALE_CORE_PATHS[@]}"; do
    rm -rf "${target_dir}/${path_name}"
  done
}

install_cli() {
  local temp_target
  mkdir -p "${LOCAL_BIN_TARGET}"
  temp_target="$(mktemp "${LOCAL_BIN_TARGET}/ba-kit.tmp.XXXXXX")"
  cp "${ROOT_DIR}/scripts/ba-kit" "${temp_target}"
  chmod +x "${temp_target}"
  mv "${temp_target}" "${LOCAL_BIN_TARGET}/ba-kit"
}

write_manifest() {
  mkdir -p "${STATE_TARGET}"
  cat > "${STATE_TARGET}/claude.env" <<EOF
BA_KIT_RUNTIME=claude
BA_KIT_SOURCE_REPO=${ROOT_DIR}
BA_KIT_INSTALLED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BA_KIT_INSTALLER=install.sh
EOF
}

echo "Installing BA-kit from: ${ROOT_DIR}"
mkdir -p "${TARGET_HOME}"
cleanup_previous_install

mkdir -p "${SKILLS_TARGET}"
for skill_dir in "${ROOT_DIR}"/skills/*; do
  if [[ -d "${skill_dir}" ]]; then
    copy_tree "${skill_dir}" "${SKILLS_TARGET}/$(basename "${skill_dir}")"
  fi
done
copy_tree "${ROOT_DIR}/rules" "${RULES_TARGET}"
copy_tree "${ROOT_DIR}/agents" "${AGENTS_TARGET}"
copy_tree "${ROOT_DIR}/templates" "${TEMPLATES_TARGET}"
remove_stale_templates "${TEMPLATES_TARGET}"
copy_tree "${CORE_SOURCE}" "${CORE_TARGET}"
remove_stale_core_paths "${CORE_TARGET}"
install_cli

mkdir -p "${ROOT_DIR}/docs" "${ROOT_DIR}/templates" "${ROOT_DIR}/designs"

echo "Installed skills to ${SKILLS_TARGET}"
echo "Installed rules to ${RULES_TARGET}"
echo "Installed agents to ${AGENTS_TARGET}"
echo "Installed templates to ${TEMPLATES_TARGET}"
echo "Installed BA core to ${CORE_TARGET}"
echo "Installed update CLI to ${LOCAL_BIN_TARGET}/ba-kit"

if [[ -f "${ROOT_DIR}/scripts/install-claude-code-ba-kit.sh" ]]; then
  echo ""
  echo "Executing Claude Code guardrail installation..."
  if bash "${ROOT_DIR}/scripts/install-claude-code-ba-kit.sh"; then
    echo ""
    echo "BA-kit installation complete (core + guardrails)."
  else
    rc=$?
    echo "" >&2
    echo "WARNING: Guardrail installation failed (exit code ${rc})." >&2
    echo "BA-kit core installed successfully, but guardrail hooks may be incomplete." >&2
    echo "Re-run ./install.sh or check scripts/install-claude-code-ba-kit.sh for errors." >&2
    write_manifest
    echo ""
    echo "BA-kit installation complete (core only, guardrails failed)."
  fi
else
  write_manifest
  echo ""
  echo "BA-kit installation complete."
fi

