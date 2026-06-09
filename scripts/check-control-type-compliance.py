#!/usr/bin/env python3
"""Validate screen canon Control Type usage against the Control Type Library.

Usage:
    python3 scripts/check-control-type-compliance.py ascii-screen/ [--json]
    python3 scripts/check-control-type-compliance.py screen.md [--library path]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

# Built-in fallback when library file is missing
BUILTIN_CONTROL_TYPES: dict[str, dict[str, Any]] = {
    "text_input": {"name": "Text Input", "interactive": True, "has_states": True},
    "textarea": {"name": "Text Area", "interactive": True, "has_states": True},
    "button": {"name": "Button", "interactive": True, "has_states": True},
    "button (primary)": {"name": "Button (Primary)", "interactive": True, "has_states": True},
    "button (secondary)": {"name": "Button (Secondary)", "interactive": True, "has_states": True},
    "button (danger)": {"name": "Button (Danger)", "interactive": True, "has_states": True},
    "button (ghost)": {"name": "Button (Ghost)", "interactive": True, "has_states": True},
    "button (icon)": {"name": "Button (Icon)", "interactive": True, "has_states": True},
    "dropdown": {"name": "Dropdown", "interactive": True, "has_states": True},
    "select": {"name": "Select", "interactive": True, "has_states": True},
    "checkbox": {"name": "Checkbox", "interactive": True, "has_states": True},
    "radio": {"name": "Radio Button", "interactive": True, "has_states": True},
    "date_picker": {"name": "Date Picker", "interactive": True, "has_states": True},
    "toggle": {"name": "Toggle", "interactive": True, "has_states": True},
    "table": {"name": "Table", "interactive": True, "has_states": True},
    "file_upload": {"name": "File Upload", "interactive": True, "has_states": True},
    "search": {"name": "Search", "interactive": True, "has_states": True},
    "modal": {"name": "Modal", "interactive": False, "has_states": False, "is_overlay": True},
    "drawer": {"name": "Drawer", "interactive": False, "has_states": False, "is_overlay": True},
    "toast": {"name": "Toast", "interactive": False, "has_states": False},
    "banner": {"name": "Banner", "interactive": False, "has_states": False},
    "pagination": {"name": "Pagination", "interactive": True, "has_states": False},
    "tabs": {"name": "Tabs", "interactive": True, "has_states": True},
    "breadcrumb": {"name": "Breadcrumb", "interactive": True, "has_states": False},
    "stepper": {"name": "Stepper", "interactive": True, "has_states": True},
    "rich_text_editor": {"name": "Rich Text Editor", "interactive": True, "has_states": True},
}

REQUIRED_COLUMNS = ["Field ID", "Field Name", "Control Type", "Display Rules", "Behaviour Rules", "Validation Rules"]
DEFAULT_BEHAVIOUR_RE = re.compile(r"^\(default\)")
OVERRIDE_BEHAVIOUR_RE = re.compile(r"^\*\*Khác default:\*\*")
CT_ID_RE = re.compile(r"`([^`]+)`")


def load_library(library_path: Path | None) -> dict[str, dict[str, Any]]:
    """Load control type definitions from library markdown file.
    Falls back to BUILTIN_CONTROL_TYPES if library not found.
    """
    if library_path and library_path.exists():
        text = library_path.read_text(encoding="utf-8")
        parsed = _parse_library(text)
        if parsed:
            return parsed
    return dict(BUILTIN_CONTROL_TYPES)


def _parse_library(text: str) -> dict[str, dict[str, Any]]:
    """Parse control types from library markdown."""
    result: dict[str, dict[str, Any]] = {}
    sections = re.split(r"^###\s+\d+\.\s+", text, flags=re.MULTILINE)
    for section in sections[1:]:
        m = re.match(r".+?\(`([^`]+)`\)", section)
        if not m:
            continue
        ct_id = m.group(1)
        info: dict[str, Any] = {"name": section.split("\n")[0].split("(`")[0].strip()}
        info["interactive"] = ct_id not in {"modal", "drawer", "toast", "banner"}
        info["has_states"] = "**Default States:**" in section
        info["is_overlay"] = ct_id in {"modal", "drawer", "dialog"}
        result[ct_id] = info
    return result


def split_row(line: str) -> list[str]:
    return [cell.replace(r"\|", "|").strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def is_separator(line: str) -> bool:
    cells = split_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def check_file(path: Path, library: dict[str, dict[str, Any]]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    issues: list[dict[str, Any]] = []
    in_fields = False
    columns: list[str] = []
    has_control_type_col = False

    for line_num, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped == "## Fields":
            in_fields = True
            continue
        if in_fields and stripped.startswith("#") and not stripped.startswith("###"):
            in_fields = False
            continue
        if not in_fields or not stripped.startswith("|") or is_separator(stripped):
            continue

        cells = split_row(stripped)
        if not columns:
            columns = cells
            missing = [c for c in REQUIRED_COLUMNS if c not in columns]
            if missing:
                issues.append({
                    "severity": "BLOCK", "code": "missing_column",
                    "message": f"Missing required column(s): {', '.join(missing)}",
                    "line": line_num,
                })
            has_control_type_col = "Control Type" in columns
            continue

        if not has_control_type_col or len(cells) < 4:
            continue

        # Map cells to column names
        row = dict(zip(columns, cells + [""] * (len(columns) - len(cells))))
        field_name = row.get("Field Name", "?")
        control_type_raw = row.get("Control Type", "").strip()
        behaviour = row.get("Behaviour Rules", "").strip()
        field_id = row.get("Field ID", "").strip()

        # Extract control_type_id from backtick-quoted value
        ct_match = CT_ID_RE.search(control_type_raw)
        ct_id = ct_match.group(1) if ct_match else control_type_raw

        # Check 1: control_type must be in library
        if ct_id and ct_id not in library:
            issues.append({
                "severity": "BLOCK", "code": "unknown_control_type",
                "message": f"Control Type '{ct_id}' not found in library. Valid types: {', '.join(sorted(library.keys())[:10])}...",
                "field": field_name, "line": line_num,
            })

        # Check 2: interactive control must have Behaviour Rules
        ct_info = library.get(ct_id, {})
        if ct_info.get("interactive") and (not behaviour or behaviour == "-"):
            issues.append({
                "severity": "BLOCK", "code": "missing_behaviour",
                "message": f"Interactive control '{ct_id}' has empty Behaviour Rules. Use '(default)' to inherit from library.",
                "field": field_name, "line": line_num,
            })

        # Check 3: (default) only valid if control_type is in library
        if DEFAULT_BEHAVIOUR_RE.match(behaviour) and ct_id not in library:
            issues.append({
                "severity": "BLOCK", "code": "invalid_default",
                "message": f"Cannot use '(default)' for unknown control type '{ct_id}'.",
                "field": field_name, "line": line_num,
            })

        # Check 4: Field ID format
        if field_id and not re.match(r"^SCR-\d{2}-F\d{2}$", field_id):
            issues.append({
                "severity": "WARN", "code": "field_id_format",
                "message": f"Field ID '{field_id}' does not match expected format SCR-NN-FNN.",
                "field": field_name, "line": line_num,
            })

    # Check 5: button primary in form needs disabled condition
    has_button_primary = "button (primary)" in text or "`button (primary)`" in text
    has_form_fields = bool(re.search(r"\b(text_input|textarea|dropdown|date_picker)\b", text))
    if has_button_primary and has_form_fields:
        if DEFAULT_BEHAVIOUR_RE.search(text) or OVERRIDE_BEHAVIOUR_RE.search(text):
            pass  # default or explicit override — OK
        elif "disabled" not in text.lower() and "bật" not in text.lower():
            issues.append({
                "severity": "BLOCK", "code": "button_primary_no_disabled",
                "message": "Button (primary) in form must declare disabled condition. "
                           "Inherit '(default)' from library or override with explicit conditions.",
            })

    # Check 6: edge cases from library documented but not covered in screen
    screen_lower = text.lower()
    for ct_id, ct_info in library.items():
        if f"`{ct_id}`" not in text:
            continue
        edge_cases = ct_info.get("edge_cases", [])
        for ec in edge_cases:
            keywords = [w for w in re.findall(r"\b\w+\b", ec.lower()) if len(w) > 3]
            if keywords and not any(kw in screen_lower for kw in keywords):
                issues.append({
                    "severity": "WARN", "code": "edge_case_not_covered",
                    "message": f"'{ct_id}' edge case '{ec[:60]}...' not covered in screen.",
                    "field": ct_info.get("name", ct_id),
                })

    # Check 7: custom Behaviour Rules that look like default — suggest using (default)
    for line_num, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|") or is_separator(stripped):
            continue
        cells = split_row(stripped)
        if len(cells) < 6:
            continue
        behaviour = cells[5].strip() if len(cells) > 5 else ""
        if behaviour and behaviour not in {"-", "—"} and not DEFAULT_BEHAVIOUR_RE.match(behaviour) and not OVERRIDE_BEHAVIOUR_RE.match(behaviour):
            # Check if it looks like a default behaviour description
            if any(kw in behaviour.lower() for kw in ["disabled khi", "active khi", "loading khi", "focus", "blur"]):
                ct_val = cells[3].strip() if len(cells) > 3 else ""
                ct_match = CT_ID_RE.search(ct_val)
                ct_id = ct_match.group(1) if ct_match else ""
                if ct_id in library:
                    issues.append({
                        "severity": "WARN", "code": "custom_looks_like_default",
                        "message": f"Behaviour for '{ct_id}' looks like default — consider using '(default)' + override for edge cases only.",
                        "field": cells[1].strip() if len(cells) > 1 else "?",
                        "line": line_num,
                    })

    # Screen-level checks
    is_overlay = any(
        ct_info.get("is_overlay") for ct_id, ct_info in library.items()
        if f"`{ct_id}`" in text
    )
    if is_overlay and "## Overlay Context" not in text:
        issues.append({
            "severity": "BLOCK", "code": "missing_overlay_context",
            "message": "Screen is a modal/drawer but missing ## Overlay Context section.",
        })
    if is_overlay and "### Close Triggers" not in text:
        issues.append({
            "severity": "BLOCK", "code": "missing_close_triggers",
            "message": "Overlay screen must have ### Close Triggers table in ## Overlay Context.",
        })

    # Check: interactive controls should have Control States
    has_interactive = any(
        ct_info.get("interactive")
        for ct_match in re.finditer(r"`([^`]+)`", text)
        if (ct_match.group(1) in library and library[ct_match.group(1)].get("interactive"))
    )
    if has_interactive and "## Control States" not in text:
        issues.append({
            "severity": "WARN", "code": "missing_control_states",
            "message": "Screen has interactive controls but missing ## Control States section.",
        })

    return {"path": str(path), "issues": issues}


def collect_files(raw_paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in raw_paths:
        p = Path(raw_path)
        if p.is_dir():
            files += sorted(item for item in p.glob("*.md") if item.name != "index.md")
        elif p.is_file() and p.name != "index.md":
            files.append(p)
    return files


def emit_report(results: list[dict[str, Any]], files_checked: int, as_json: bool) -> None:
    failing = [r for r in results if r["issues"]]
    if as_json:
        output = {
            "files_checked": files_checked,
            "files_with_issues": len(failing),
            "results": failing,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return
    if not failing:
        print(f"OK: {files_checked} screen files — all Control Types compliant")
        return
    for result in failing:
        print(f"\n{result['path']}:")
        for item in result["issues"]:
            location = f" line {item['line']}:" if item.get("line") else ""
            field = f" [{item['field']}]" if item.get("field") else ""
            print(f"  [{item['severity']}] [{item['code']}]{location}{field} {item['message']}")
    block_count = sum(1 for r in failing for i in r["issues"] if i["severity"] == "BLOCK")
    warn_count = sum(1 for r in failing for i in r["issues"] if i["severity"] == "WARN")
    print(f"\n{f'BLOCK: {block_count}, ' if block_count else ''}WARN: {warn_count} — {len(failing)}/{files_checked} files with issues")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate screen Control Type usage")
    parser.add_argument("path", nargs="+", help="Screen canon file(s) or directory")
    parser.add_argument("--library", type=Path, help="Path to control-type-library.md")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT, help="Repo root for template resolution")
    args = parser.parse_args()

    library_path = args.library
    if not library_path:
        template_path = args.repo / "templates" / "control-type-library-template.md"
        if template_path.exists():
            library_path = template_path

    library = load_library(library_path)

    try:
        files = collect_files(args.path)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if not files:
        print("No screen files found", file=sys.stderr)
        return 2

    results = [check_file(f, library) for f in files]
    emit_report(results, len(files), args.json)

    has_blocks = any(
        i["severity"] == "BLOCK" for r in results for i in r["issues"]
    )
    return 1 if has_blocks else 0


if __name__ == "__main__":
    sys.exit(main())
