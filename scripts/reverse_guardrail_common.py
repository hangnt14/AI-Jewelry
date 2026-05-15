#!/usr/bin/env python3
"""Shared helpers for reverse-mode guardrail scripts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Reverse trace ID format: REV-{YYYYMMDD}-{NN} or REV-{slug}-{NN}
# Minimum fields each trace record must carry in the evidence ledger.
# ---------------------------------------------------------------------------
TRACE_ID_RE = re.compile(r"\bREV-[A-Za-z0-9]+-\d+\b")

REQUIRED_TRACE_FIELDS = {"trace_id", "source_file", "claim_summary", "recorded_at"}

# Patterns that indicate live-runtime probing — blocked in v1 source-only mode.
LIVE_PROBE_PATTERNS = [
    re.compile(r"\blocalhost\b"),
    re.compile(r"\b127\.0\.0\.1\b"),
    re.compile(r"\b0\.0\.0\.0\b"),
    re.compile(r"requests\.(get|post|put|delete|patch|head)\s*\("),
    re.compile(r"urllib\.request\.urlopen"),
    re.compile(r"httpx\.(get|post|put|delete|patch|head)\s*\("),
    re.compile(r"subprocess\.(run|call|Popen|check_output)\s*\("),
    re.compile(r"os\.system\s*\("),
]


# ---------------------------------------------------------------------------
# JSON output helpers
# ---------------------------------------------------------------------------

def emit_result(data: dict[str, Any], *, stderr_summary: str = "") -> None:
    """Print JSON to stdout and optional human summary to stderr."""
    import sys
    print(json.dumps(data, indent=2, ensure_ascii=False))
    if stderr_summary:
        print(stderr_summary, file=sys.stderr)


def ok(checks: list[dict], message: str = "", **extra: Any) -> dict[str, Any]:
    return {"status": "ok", "checks": checks, "message": message, **extra}


def block(checks: list[dict], message: str, **extra: Any) -> dict[str, Any]:
    return {"status": "block", "checks": checks, "message": message, **extra}


def warn(checks: list[dict], message: str, **extra: Any) -> dict[str, Any]:
    return {"status": "warn", "checks": checks, "message": message, **extra}


def check_pass(name: str, detail: str = "") -> dict[str, str]:
    return {"check": name, "result": "pass", "detail": detail}


def check_fail(name: str, detail: str = "") -> dict[str, str]:
    return {"check": name, "result": "fail", "detail": detail}


# ---------------------------------------------------------------------------
# File / path helpers
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_contract(repo: Path) -> dict[str, Any]:
    return json.loads((repo / "core" / "contract.yaml").read_text(encoding="utf-8"))


def render_path(template: str, *, slug: str, date: str) -> str:
    return template.replace("{slug}", slug).replace("{date}", date)


def reverse_root(contract: dict[str, Any], *, slug: str, date: str) -> str:
    return render_path(contract["paths"]["reverse_root"], slug=slug, date=date)


def reverse_path(contract: dict[str, Any], key: str, *, slug: str, date: str) -> str:
    return render_path(contract["paths"][key], slug=slug, date=date)


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def git_commit_exists(repo: Path, commit: str) -> bool:
    """Return True if commit hash exists in the repo's git history."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "cat-file", "-t", commit],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0 and result.stdout.strip() == "commit"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def git_file_hash_at_commit(repo: Path, commit: str, rel_path: str) -> str | None:
    """Return the blob hash of rel_path at the given commit, or None."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "show", f"{commit}:{rel_path}"],
            capture_output=True,
            timeout=15,
        )
        if result.returncode != 0:
            return None
        return hashlib.sha256(result.stdout).hexdigest()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


# ---------------------------------------------------------------------------
# Baseline lock helpers
# ---------------------------------------------------------------------------

REQUIRED_BASELINE_FIELDS = {"documented_commit", "locked_at", "focus_selection", "locked_files"}


def load_baseline_lock(path: Path) -> dict[str, Any]:
    return load_json(path)


def validate_baseline_lock(data: dict[str, Any]) -> list[str]:
    """Return list of missing/invalid field names."""
    errors: list[str] = []
    for field in REQUIRED_BASELINE_FIELDS:
        if field not in data or not data[field]:
            errors.append(f"missing_field:{field}")
    if "focus_selection" in data and not data["focus_selection"]:
        errors.append("focus_selection_empty")
    if "documented_commit" in data:
        commit = data["documented_commit"]
        if not re.match(r"^[0-9a-f]{7,40}$", str(commit)):
            errors.append(f"invalid_commit_format:{commit}")
    return errors


# ---------------------------------------------------------------------------
# Trace ID helpers
# ---------------------------------------------------------------------------

def extract_trace_ids(text: str) -> set[str]:
    return set(TRACE_ID_RE.findall(text))


def parse_evidence_ledger(path: Path) -> list[dict[str, str]]:
    """Parse a markdown evidence ledger into a list of trace records.

    Expected format: each record is a markdown section starting with
    `### REV-...` followed by key: value lines.
    """
    text = path.read_text(encoding="utf-8")
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        heading_match = re.match(r"^#{1,4}\s+(REV-[A-Za-z0-9]+-\d+)\b", line)
        if heading_match:
            if current:
                records.append(current)
            current = {"trace_id": heading_match.group(1)}
            continue
        kv_match = re.match(r"^[-*]?\s*\*{0,2}(\w[\w _/-]*?)\*{0,2}\s*:\s*(.+)$", line)
        if kv_match and current:
            key = kv_match.group(1).strip().lower().replace(" ", "_")
            current[key] = kv_match.group(2).strip()
    if current:
        records.append(current)
    return records


# ---------------------------------------------------------------------------
# Live-probe detection (v1 source-only enforcement)
# ---------------------------------------------------------------------------

def detect_live_probes(text: str) -> list[str]:
    """Return list of matched live-probe pattern descriptions found in text."""
    hits: list[str] = []
    for pattern in LIVE_PROBE_PATTERNS:
        if pattern.search(text):
            hits.append(pattern.pattern)
    return hits
