#!/usr/bin/env python3
"""Validate srs.md heading structure against srs-template.md.

Usage:
    python3 scripts/check-srs-template-compliance.py \\
        --srs plans/X/03_modules/auth/srs.md \\
        --repo .

Exit codes: 0=pass, 1=validation errors, 2=input missing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_HEADING_SLUGS = [
    "dac-ta-yeu-cau-phan-mem",
    "muc-dich-va-pham-vi",
    "yeu-cau-chuc-nang",
    "dac-ta-use-case",
    "hop-dong-man-hinh-tien-wireframe",
    "danh-muc-man-hinh",
    "mo-ta-man-hinh",
    "yeu-cau-phi-chuc-nang",
    "ascii-wireframes",
]

OPTIONAL_HEADING_SLUGS = [
    "so-do-luong-du-lieu",
    "so-do-thuc-the-quan-he",
    "dac-ta-api",
]

REQUIRED_TABLE_MARKERS = [
    ("yeu-cau-chuc-nang", "| Mã (ID) | Yêu cầu"),
    ("dac-ta-use-case", "| Mã UC"),
    ("hop-dong-man-hinh-tien-wireframe", "| Mã (Screen ID)"),
    ("danh-muc-man-hinh", "| Mã (Screen/Frame ID)"),
    ("yeu-cau-phi-chuc-nang", "| Mã (ID) | Danh mục"),
]


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[àáảãạăằắẳẵặâầấẩẫậ]", "a", s)
    s = re.sub(r"[èéẻẽẹêềếểễệ]", "e", s)
    s = re.sub(r"[ìíỉĩị]", "i", s)
    s = re.sub(r"[òóỏõọôồốổỗộơờớởỡợ]", "o", s)
    s = re.sub(r"[ùúủũụưừứửữự]", "u", s)
    s = re.sub(r"[ỳýỷỹỵ]", "y", s)
    s = re.sub(r"đ", "d", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def find_section(lines: list[str], heading_slug: str) -> tuple[int, int, int | None]:
    heading_re = re.compile(r"^(#{1,4})\s+(.+)$")
    for i, line in enumerate(lines):
        m = heading_re.match(line)
        if m:
            text = m.group(2).strip()
            text_stripped = re.sub(r"\s*\([^)]+\)", "", text).strip()
            if slugify(text_stripped) == heading_slug:
                level = len(m.group(1))
                end = len(lines)
                for j in range(i + 1, len(lines)):
                    m2 = heading_re.match(lines[j])
                    if m2 and len(m2.group(1)) <= level:
                        end = j
                        break
                return i, end, level
    return -1, -1, None


def parse_template(path: Path) -> list[str]:
    heading_re = re.compile(r"^(#{1,4})\s+(.+)$")
    lines = path.read_text(encoding="utf-8").splitlines()
    slugs = []
    for line in lines:
        m = heading_re.match(line)
        if m:
            text = m.group(2).strip()
            text_stripped = re.sub(r"\s*\([^)]+\)", "", text).strip()
            slugs.append(slugify(text_stripped))
    return slugs


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate srs.md heading structure against template")
    parser.add_argument("--srs", type=Path, help="Path to srs.md")
    parser.add_argument("--repo", default=".", help="Repo root path")
    parser.add_argument("--output", help="Write JSON result to this path")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    template_path = repo / "templates" / "srs-template.md"

    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=sys.stderr)
        return 2

    srs_path = args.srs.resolve() if args.srs else None
    if not srs_path or not srs_path.exists():
        print(f"ERROR: srs.md not found: {srs_path}", file=sys.stderr)
        return 2

    srs_lines = srs_path.read_text(encoding="utf-8").splitlines()

    result: dict = {
        "status": "pass",
        "srs_path": str(srs_path),
        "issues": [],
        "message": "",
    }

    # Check required headings
    for slug in REQUIRED_HEADING_SLUGS:
        start, end, level = find_section(srs_lines, slug)
        if start < 0:
            result["issues"].append({
                "severity": "error",
                "code": "missing_required_heading",
                "heading_slug": slug,
            })

    # Check optional headings
    for slug in OPTIONAL_HEADING_SLUGS:
        start, end, level = find_section(srs_lines, slug)
        if start < 0:
            result["issues"].append({
                "severity": "warning",
                "code": "missing_optional_heading",
                "heading_slug": slug,
            })

    # Check required tables exist within their sections
    for section_slug, table_marker in REQUIRED_TABLE_MARKERS:
        start, end, _ = find_section(srs_lines, section_slug)
        if start < 0:
            continue
        found = False
        for i in range(start, end):
            if table_marker in srs_lines[i]:
                found = True
                break
        if not found:
            result["issues"].append({
                "severity": "error",
                "code": "missing_required_table",
                "section": section_slug,
                "expected_marker": table_marker,
            })

    # Check heading level consistency (no skipped levels)
    heading_re = re.compile(r"^(#{1,4})\s+(.+)$")
    prev_level = 1
    for i, line in enumerate(srs_lines):
        m = heading_re.match(line)
        if m:
            level = len(m.group(1))
            if level > prev_level + 1:
                result["issues"].append({
                    "severity": "warning",
                    "code": "heading_level_skip",
                    "line": i + 1,
                    "from_level": prev_level,
                    "to_level": level,
                })
            prev_level = level

    errors = [i for i in result["issues"] if i["severity"] == "error"]
    warnings = [i for i in result["issues"] if i["severity"] == "warning"]

    if errors:
        result["status"] = "fail"
        result["message"] = f"SRS_TEMPLATE_COMPLIANCE_FAIL: {len(errors)} errors, {len(warnings)} warnings"
    elif warnings:
        result["status"] = "warn"
        result["message"] = f"SRS_TEMPLATE_COMPLIANCE_WARN: {len(warnings)} warnings"
    else:
        result["status"] = "pass"
        result["message"] = "SRS_TEMPLATE_COMPLIANCE_PASS"

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    print(output)

    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
