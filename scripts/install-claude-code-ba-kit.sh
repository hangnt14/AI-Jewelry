#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_HOME="${HOME}/.claude"
TARGET_BA_KIT="${TARGET_HOME}/ba-kit"
TARGET_SCRIPTS="${TARGET_BA_KIT}/scripts"
TARGET_HOOKS="${TARGET_BA_KIT}/hooks"
TARGET_DOCS="${TARGET_BA_KIT}/docs"
TARGET_STATE="${TARGET_BA_KIT}/state"
LOCAL_BIN_TARGET="${HOME}/.local/bin"
STATE_TARGET="${HOME}/.local/share/ba-kit/installations"
SETTINGS_FILE="${TARGET_HOME}/settings.json"

GUARDRAIL_SCRIPTS=(
  "guardrail-preflight.py"
  "guardrail-build-excerpts.py"
  "guardrail-audit.py"
  "guardrail_common.py"
  "validate-index-quality.py"
  "check-token-budget.py"
  "check-write-scope.py"
)

# ── helpers ──────────────────────────────────────────────────────────

ensure_dir() {
  mkdir -p "$1"
}

install_cli() {
  local temp_target
  mkdir -p "${LOCAL_BIN_TARGET}"
  temp_target="$(mktemp "${LOCAL_BIN_TARGET}/ba-kit.tmp.XXXXXX")"
  cp "${ROOT_DIR}/scripts/ba-kit" "${temp_target}"
  chmod +x "${temp_target}"
  mv "${temp_target}" "${LOCAL_BIN_TARGET}/ba-kit"
}

# ── guardrail script installation ────────────────────────────────────

install_guardrail_scripts() {
  local script_name

  ensure_dir "${TARGET_SCRIPTS}"
  for script_name in "${GUARDRAIL_SCRIPTS[@]}"; do
    if [[ ! -f "${ROOT_DIR}/scripts/${script_name}" ]]; then
      echo "Guardrail script missing: ${ROOT_DIR}/scripts/${script_name}" >&2
      exit 1
    fi
    cp "${ROOT_DIR}/scripts/${script_name}" "${TARGET_SCRIPTS}/${script_name}"
  done
}

install_guardrail_docs() {
  ensure_dir "${TARGET_DOCS}"
  cp "${ROOT_DIR}/docs/runtime-hard-guardrails.md" "${TARGET_DOCS}/runtime-hard-guardrails.md"
  if [[ -f "${ROOT_DIR}/core/token-budget.md" ]]; then
    cp "${ROOT_DIR}/core/token-budget.md" "${TARGET_DOCS}/token-budget.md"
  fi
}

# ── hook script generation ───────────────────────────────────────────

write_preflight_hook() {
  cat > "${TARGET_HOOKS}/guardrail-preflight-hook.sh" <<'HOOKEOF'
#!/usr/bin/env bash
# BA-kit guardrail preflight hook — UserPromptSubmit
# Detects BA-kit context, resolves command/slug/date, runs guardrail-preflight.py,
# and outputs a compact verdict into the prompt context.

set -euo pipefail

BA_KIT_HOOK_HOME="${HOME}/.claude/ba-kit"
BA_KIT_STATE_DIR="${BA_KIT_HOOK_HOME}/state"

# ── detect BA-kit context ────────────────────────────────────────────

detect_plan_dir() {
  local dir="${PWD}"
  while [[ "${dir}" != "/" ]]; do
    if [[ "${dir}" =~ /plans/[^/]+-[0-9]{6}-[0-9]{4}$ ]]; then
      printf '%s\n' "${dir}"
      return 0
    fi
    if [[ "${dir}" == "${HOME}" ]]; then
      break
    fi
    dir="$(dirname "${dir}")"
  done

  if [[ -n "${BA_KIT_HOME:-}" ]] && [[ -d "${BA_KIT_HOME}" ]]; then
    printf '%s\n' "${BA_KIT_HOME}"
    return 0
  fi

  return 1
}

extract_slug_date() {
  local plan_dir="$1"
  local dirname
  dirname="$(basename "${plan_dir}")"
  # plans/{slug}-{YYMMDD-HHmm}
  local slug="${dirname%-[0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]}"
  local date_token="${dirname#${slug}-}"
  printf '%s\n%s\n' "${slug}" "${date_token}"
}

detect_command_from_prompt() {
  local prompt_text="$1"

  # Explicit ba-start subcommands
  if echo "${prompt_text}" | grep -qiE '\bba-start\s+(frd|stories|srs|package|status|next)\b'; then
    echo "${prompt_text}" | grep -oiE '\bba-start\s+(frd|stories|srs|package|status|next)\b' \
      | head -1 | sed 's/ba-start //'
    return 0
  fi

  # Natural language patterns (from core/workflows/do.md routing table)
  if echo "${prompt_text}" | grep -qiE '\b(create|generate|produce|build|write)\b.*\b(FRD|functional requirements)\b'; then
    echo "frd"
    return 0
  fi
  if echo "${prompt_text}" | grep -qiE '\b(create|generate|produce|build|write)\b.*\b(user stories|stories)\b'; then
    echo "stories"
    return 0
  fi
  if echo "${prompt_text}" | grep -qiE '\b(create|generate|produce|build|write)\b.*\b(SRS|software requirements|spec)\b'; then
    echo "srs"
    return 0
  fi
  if echo "${prompt_text}" | grep -qiE '\b(package|bundle|handoff|deliver|ban giao|xuat goi)\b'; then
    echo "package"
    return 0
  fi
  if echo "${prompt_text}" | grep -qiE '\b(status|check|kiem tra)\b.*\b(progress|tien do)\b'; then
    echo "status"
    return 0
  fi
  if echo "${prompt_text}" | grep -qiE '\b(tiep tuc|tiep theo|next|continue|resume)\b'; then
    echo "next"
    return 0
  fi

  return 1
}

detect_module() {
  local plan_dir="$1"
  local modules_dir="${plan_dir}/03_modules"
  if [[ ! -d "${modules_dir}" ]]; then
    return 0
  fi

  # If user typed --module in prompt, extract it
  local module_from_prompt
  module_from_prompt="$(echo "${PROMPT_TEXT:-}" | grep -oP '(?<=--module\s)\S+' | head -1 || true)"
  if [[ -n "${module_from_prompt}" ]]; then
    printf '%s\n' "${module_from_prompt}"
    return 0
  fi

  # If only one module exists, use it
  local count=0
  local single=""
  for d in "${modules_dir}"/*/; do
    [[ -d "${d}" ]] || continue
    count=$((count + 1))
    single="$(basename "${d}")"
  done
  if [[ "${count}" -eq 1 ]]; then
    printf '%s\n' "${single}"
  fi
}

# ── main ─────────────────────────────────────────────────────────────

PLAN_DIR="$(detect_plan_dir)" || exit 0

PROMPT_TEXT="${1:-}"
if [[ -z "${PROMPT_TEXT}" ]] && [[ -n "${CLAUDE_PROMPT:-}" ]]; then
  PROMPT_TEXT="${CLAUDE_PROMPT}"
fi

COMMAND="$(detect_command_from_prompt "${PROMPT_TEXT}")" || exit 0

# Only preflight guarded commands
case "${COMMAND}" in
  frd|stories|srs|package|status|next) ;;
  *) exit 0 ;;
esac

SLUG_DATE=($(extract_slug_date "${PLAN_DIR}"))
SLUG="${SLUG_DATE[0]}"
DATE_TOKEN="${SLUG_DATE[1]}"
MODULE="$(detect_module "${PLAN_DIR}")"

# Build preflight args
# Resolve BA-kit source repo from manifest (same logic as CLI resolve_registered_repo)
SOURCE_REPO=""
if [[ -f "${HOME}/.local/share/ba-kit/installations/claude.env" ]]; then
  SOURCE_REPO="$(grep '^BA_KIT_SOURCE_REPO=' "${HOME}/.local/share/ba-kit/installations/claude.env" | head -1 | cut -d= -f2-)"
fi
if [[ -z "${SOURCE_REPO}" ]] && [[ -f "${HOME}/.local/share/ba-kit/installations/claude-code.env" ]]; then
  SOURCE_REPO="$(grep '^BA_KIT_SOURCE_REPO=' "${HOME}/.local/share/ba-kit/installations/claude-code.env" | head -1 | cut -d= -f2-)"
fi
if [[ -z "${SOURCE_REPO}" ]]; then
  exit 0
fi

PREFLIGHT_ARGS=(
  --command "${COMMAND}"
  --slug "${SLUG}"
  --date "${DATE_TOKEN}"
  --repo "${SOURCE_REPO}"
)
if [[ -n "${MODULE:-}" ]]; then
  PREFLIGHT_ARGS+=(--module "${MODULE}")
fi

mkdir -p "${BA_KIT_STATE_DIR}"
PREFLIGHT_OUT="${BA_KIT_STATE_DIR}/last-preflight.json"

python3 "${HOME}/.claude/ba-kit/scripts/guardrail-preflight.py" \
  "${PREFLIGHT_ARGS[@]}" \
  --output "${PREFLIGHT_OUT}" >/dev/null 2>&1 || true

if [[ ! -f "${PREFLIGHT_OUT}" ]]; then
  exit 0
fi

# Parse preflight JSON and emit verdict
python3 - "${PREFLIGHT_OUT}" <<'PYEOF'
import json, sys, pathlib

preflight = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
status = preflight.get("status", "")
command = preflight.get("command", "")
resolved_slug = preflight.get("resolved_slug", "")
message = preflight.get("message", "").strip()
indexes = preflight.get("indexes", {})

has_current = any(
    v.get("state") == "current" for v in indexes.values() if isinstance(v, dict)
)
action_guardrail = preflight.get("action_guardrail", {})

if status == "block":
    output_mode = "probe"
elif has_current:
    output_mode = "delta"
else:
    output_mode = "full"

lines = [
    "",
    "Guardrail preflight:",
    f"output_mode={output_mode}",
    f"status={status}",
    f"command={command}",
    f"resolved_slug={resolved_slug}",
    message,
]

if output_mode in ("delta", "full"):
    allow_reads = preflight.get("allow_reads", [])
    if allow_reads:
        lines.append("ALLOW_READS:")
        lines.extend(f"- {item}" for item in allow_reads)

    for idx_name, idx_val in indexes.items():
        if isinstance(idx_val, dict):
            lines.append(f"INDEX: {idx_name} state={idx_val.get('state', '')}")

    if action_guardrail.get("required"):
        lines.extend([
            "ACTION_GUARDRAIL:",
            f"- navigation_source={action_guardrail.get('navigation_source', '')}",
            f"- packet_scope={action_guardrail.get('packet_scope', '')}",
            f"- reason={action_guardrail.get('reason', '')}",
        ])

if output_mode == "full":
    deny_reads = preflight.get("deny_reads", [])
    if deny_reads:
        lines.append("DENY_READS:")
        lines.extend(f"- {item}" for item in deny_reads)

    canonical_state_summary = preflight.get("canonical_state_summary", "").strip()
    if canonical_state_summary:
        lines.extend(["CANONICAL_STATE:", f"- {canonical_state_summary}"])

    canonical_next = preflight.get("canonical_next_command", "").strip()
    if canonical_next:
        lines.extend(["CANONICAL_NEXT_COMMAND:", f"- {canonical_next}"])

    refresh_cmd = preflight.get("refresh_command", "").strip()
    if refresh_cmd and status == "block":
        lines.append(f"REFRESH_COMMAND: {refresh_cmd}")

lines.append(
    f"If a broader read is necessary, emit exactly: READ_ESCALATION: {command} read <path> due to <reason>."
)

print("\n".join(lines))
PYEOF
HOOKEOF

  chmod +x "${TARGET_HOOKS}/guardrail-preflight-hook.sh"
}

write_audit_hook() {
  cat > "${TARGET_HOOKS}/guardrail-audit-hook.sh" <<'HOOKEOF'
#!/usr/bin/env bash
# BA-kit guardrail audit hook — Stop
# After Claude Code session ends, audits actual reads against preflight allowlist.

set -euo pipefail

PREFLIGHT_PATH="${HOME}/.claude/ba-kit/state/last-preflight.json"
AUDIT_OUT="${HOME}/.claude/ba-kit/state/last-audit.json"

if [[ ! -f "${PREFLIGHT_PATH}" ]]; then
  exit 0
fi

READS_MANIFEST="${HOME}/.claude/ba-kit/state/reads-manifest.json"
if [[ ! -f "${READS_MANIFEST}" ]]; then
  # No reads tracked — nothing to audit
  rm -f "${PREFLIGHT_PATH}"
  exit 0
fi

python3 "${HOME}/.claude/ba-kit/scripts/guardrail-audit.py" \
  --preflight "${PREFLIGHT_PATH}" \
  --reads-manifest "${READS_MANIFEST}" \
  --output "${AUDIT_OUT}" >/dev/null 2>&1 || true

if [[ -f "${AUDIT_OUT}" ]]; then
  status="$(python3 -c "
import json, pathlib
d = json.loads(pathlib.Path('${AUDIT_OUT}').read_text())
print(d.get('status', ''))
" 2>/dev/null || echo "")"

  case "${status}" in
    fail)
      echo "GUARDRAIL_AUDIT_FAIL: read audit found violations" >&2
      ;;
    warn)
      echo "GUARDRAIL_AUDIT_WARN: read audit found minor issues" >&2
      ;;
    pass)
      echo "GUARDRAIL_AUDIT_PASS" >&2
      ;;
  esac
fi

# Cleanup state after audit
rm -f "${PREFLIGHT_PATH}" "${READS_MANIFEST}"
HOOKEOF

  chmod +x "${TARGET_HOOKS}/guardrail-audit-hook.sh"
}

write_write_scope_hook() {
  cat > "${TARGET_HOOKS}/guardrail-write-scope-hook.sh" <<'HOOKEOF'
#!/usr/bin/env bash
# BA-kit write-scope enforcement hook — PreToolUse (matcher: Write|Edit)
# Blocks file writes outside the command-owned artifact scope.

set -euo pipefail

BA_KIT_HOOK_HOME="${HOME}/.claude/ba-kit"
BA_KIT_STATE_DIR="${BA_KIT_HOOK_HOME}/state"

# ── detect BA-kit context ────────────────────────────────────────────

detect_plan_dir() {
  local dir="${PWD}"
  while [[ "${dir}" != "/" ]]; do
    if [[ "${dir}" =~ /plans/[^/]+-[0-9]{6}-[0-9]{4}$ ]]; then
      printf '%s\n' "${dir}"
      return 0
    fi
    if [[ "${dir}" == "${HOME}" ]]; then
      break
    fi
    dir="$(dirname "${dir}")"
  done

  if [[ -n "${BA_KIT_HOME:-}" ]] && [[ -d "${BA_KIT_HOME}" ]]; then
    printf '%s\n' "${BA_KIT_HOME}"
    return 0
  fi

  return 1
}

detect_plan_dir >/dev/null 2>&1 || exit 0

# ── extract target path from tool input ──────────────────────────────

TOOL_INPUT="${1:-}"
TOOL_NAME="${2:-}"

# Claude Code passes tool input as JSON on stdin for PreToolUse hooks
# The hook receives: tool_name, tool_input (JSON string)
if [[ -z "${TOOL_INPUT}" ]]; then
  # Try reading from stdin (Claude Code hook interface)
  TOOL_INPUT="$(cat - 2>/dev/null || echo "")"
fi

# Extract file path from tool input
TARGET_PATH="$(echo "${TOOL_INPUT}" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('file_path', data.get('path', data.get('file', ''))))
except Exception:
    pass
" 2>/dev/null || echo "")"

if [[ -z "${TARGET_PATH}" ]]; then
  exit 0
fi

# ── resolve last detected command ────────────────────────────────────

PREFLIGHT_PATH="${HOME}/.claude/ba-kit/state/last-preflight.json"
DETECTED_CMD=""
if [[ -f "${PREFLIGHT_PATH}" ]]; then
  DETECTED_CMD="$(python3 -c "
import json, pathlib
d = json.loads(pathlib.Path('${PREFLIGHT_PATH}').read_text())
print(d.get('command', ''))
" 2>/dev/null || echo "")"
fi

if [[ -z "${DETECTED_CMD}" ]]; then
  exit 0
fi

# ── run write-scope check ────────────────────────────────────────────

if "${HOME}/.local/bin/ba-kit" check-write-scope --command "${DETECTED_CMD}" "${TARGET_PATH}" 2>/dev/null; then
  exit 0
else
  echo "GUARDRAIL_BLOCK: write-scope violation — ${TARGET_PATH} not in allowed scope for ${DETECTED_CMD}" >&2
  exit 1
fi
HOOKEOF

  chmod +x "${TARGET_HOOKS}/guardrail-write-scope-hook.sh"
}

# ── settings.json hook registration ──────────────────────────────────

register_hooks() {
  ensure_dir "${TARGET_HOME}"

  # Initialize settings.json if it doesn't exist
  if [[ ! -f "${SETTINGS_FILE}" ]]; then
    echo '{}' > "${SETTINGS_FILE}"
  fi

  python3 - "${SETTINGS_FILE}" "${TARGET_HOOKS}" <<'PYEOF'
import json, pathlib, sys

settings_path = pathlib.Path(sys.argv[1])
hooks_dir = sys.argv[2]
settings = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
if not isinstance(settings, dict):
    settings = {}

hooks = settings.setdefault("hooks", {})

# UserPromptSubmit — preflight
ups_hooks = hooks.setdefault("UserPromptSubmit", [])
# Remove any existing ba-kit UserPromptSubmit hooks
ups_hooks[:] = [h for h in ups_hooks if "guardrail-preflight-hook.sh" not in str(h)]
ups_hooks.append({
    "matcher": "",
    "hooks": [{
        "type": "command",
        "command": f"bash \"{hooks_dir}/guardrail-preflight-hook.sh\""
    }]
})

# Stop — audit
stop_hooks = hooks.setdefault("Stop", [])
stop_hooks[:] = [h for h in stop_hooks if "guardrail-audit-hook.sh" not in str(h)]
stop_hooks.append({
    "hooks": [{
        "type": "command",
        "command": f"bash \"{hooks_dir}/guardrail-audit-hook.sh\""
    }]
})

# PreToolUse — write-scope (matcher: Write|Edit)
ptu_hooks = hooks.setdefault("PreToolUse", [])
ptu_hooks[:] = [h for h in ptu_hooks if "guardrail-write-scope-hook.sh" not in str(h)]
ptu_hooks.append({
    "matcher": "Write|Edit",
    "hooks": [{
        "type": "command",
        "command": f"bash \"{hooks_dir}/guardrail-write-scope-hook.sh\""
    }]
})

settings["hooks"] = hooks
settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PYEOF
}

# ── manifest ─────────────────────────────────────────────────────────

write_manifest() {
  mkdir -p "${STATE_TARGET}"
  cat > "${STATE_TARGET}/claude.env" <<EOF
BA_KIT_RUNTIME=claude-code
BA_KIT_SOURCE_REPO=${ROOT_DIR}
BA_KIT_INSTALLED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BA_KIT_INSTALLER=scripts/install-claude-code-ba-kit.sh
BA_KIT_GUARDRAIL_ROOT=${TARGET_BA_KIT}
BA_KIT_GUARDRAIL_PREFLIGHT=${TARGET_SCRIPTS}/guardrail-preflight.py
BA_KIT_GUARDRAIL_EXCERPTS=${TARGET_SCRIPTS}/guardrail-build-excerpts.py
BA_KIT_GUARDRAIL_AUDIT=${TARGET_SCRIPTS}/guardrail-audit.py
BA_KIT_INDEX_VALIDATOR=${TARGET_SCRIPTS}/validate-index-quality.py
BA_KIT_CHECK_TOKEN_BUDGET=${TARGET_SCRIPTS}/check-token-budget.py
BA_KIT_CHECK_WRITE_SCOPE=${TARGET_SCRIPTS}/check-write-scope.py
BA_KIT_GUARDRAIL_DOC=${TARGET_DOCS}/runtime-hard-guardrails.md
EOF
}

# ── main ─────────────────────────────────────────────────────────────

echo "Installing BA-kit guardrail system for Claude Code from: ${ROOT_DIR}"

ensure_dir "${TARGET_BA_KIT}"
ensure_dir "${TARGET_HOOKS}"
ensure_dir "${TARGET_STATE}"

install_guardrail_scripts
echo "Installed guardrail scripts to ${TARGET_SCRIPTS}"

install_guardrail_docs
echo "Installed guardrail docs to ${TARGET_DOCS}"

write_preflight_hook
write_audit_hook
write_write_scope_hook
echo "Created hook scripts in ${TARGET_HOOKS}"

register_hooks
echo "Registered hooks in ${SETTINGS_FILE}"

install_cli
echo "Installed CLI to ${LOCAL_BIN_TARGET}/ba-kit"

write_manifest
echo "Wrote manifest to ${STATE_TARGET}/claude.env"

echo ""
echo "BA-kit Claude Code installation complete."
echo ""
echo "Installed:"
echo "  - 7 guardrail Python scripts → ${TARGET_SCRIPTS}"
echo "  - 3 hook scripts → ${TARGET_HOOKS}"
echo "  - Guardrail docs → ${TARGET_DOCS}"
echo "  - CLI → ${LOCAL_BIN_TARGET}/ba-kit"
echo "  - Hooks registered in ${SETTINGS_FILE}"
echo ""
echo "Hooks active for:"
echo "  - UserPromptSubmit: guardrail preflight (detects BA-kit context, emits verdict)"
echo "  - Stop: guardrail audit (post-session read compliance)"
echo "  - PreToolUse (Write|Edit): write-scope enforcement"
echo ""
echo "Hooks silent outside BA-kit plan directories. No overhead for non-BA work."
