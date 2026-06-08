#!/usr/bin/env python3
"""Deterministic SRS compiler: merge canon sources into srs-template.md structure.

Usage:
    python3 scripts/compile-srs.py --module-root plans/X/03_modules/auth
    python3 scripts/compile-srs.py --repo . --slug project --date 260608-1400 --module auth
    python3 scripts/compile-srs.py ... --no-html

Reads srs-template.md for heading skeleton, merges canon sources into matching
sections, writes srs.md + srs-compile-receipt.json, optionally generates
per-module HTML.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

REQUIRED_SOURCE_FILES = ["srs/spec.md"]
OPTIONAL_SOURCE_FILES = ["srs/flows.md", "srs/erd.md"]

REQUIRED_INDEX_FILES = ["usecases/index.md", "ascii-screen/index.md"]
REQUIRED_CONTENT_GLOBS = {
    "usecases": "uc-*.md",
    "ascii-screen": "*.md",
}

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


def slugify(text: str) -> str:
    """Convert Vietnamese heading text to ASCII slug."""
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── YAML frontmatter stripper ─────────────────────────────────────────

YAML_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Patterns that indicate an unfilled template placeholder
PLACEHOLDER_PATTERNS = [
    r"\[Tên dự án\]",
    r"\[Tên module\]",
    r"\[Tên portal[^\]]*\]",
    r"\[Tên màn hình\]",
    r"\[Tên UC\]",
    r"\[Mô tả\]",
    r"\[TBD\]",
    r"\[placeholder[^\]]*\]",
    r"\[Project\]",
    r"\[Module\]",
    r"\[Screen Name\]",
    r"\[Use Case Name\]",
]


def strip_yaml_frontmatter(text: str) -> tuple[str, dict]:
    """Strip YAML frontmatter from markdown text.

    Returns (body_without_frontmatter, frontmatter_dict).
    """
    m = YAML_FRONTMATTER_RE.match(text)
    if not m:
        return text, {}
    raw = m.group(1)
    fm = {}
    for line in raw.splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return text[m.end():], fm


def detect_placeholders(text: str, source_label: str) -> list[str]:
    """Find unfilled template placeholders in text."""
    found = []
    for pattern in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pattern, text):
            found.append(f"{source_label}: {m.group(0)}")
    return found


def verify_index_against_disk(index_path: Path, source_dir: Path) -> list[str]:
    """Cross-validate index entries against actual files on disk.

    Parses the index table's 'File' column and checks each referenced file exists.
    Returns list of missing file paths (empty = all good).
    """
    missing = []
    if not index_path.exists():
        return [f"Index file missing: {index_path}"]
    text = index_path.read_text(encoding="utf-8")
    # Parse the section index table — find rows with a File column
    in_table = False
    file_col_idx = -1
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells:
            continue
        # Detect header row
        if any(c == "File" for c in cells):
            file_col_idx = next((i for i, c in enumerate(cells) if c == "File"), -1)
            in_table = True
            continue
        # Skip separator rows
        if all(c.startswith("-") or c == "" for c in cells if c):
            continue
        if in_table and file_col_idx >= 0 and file_col_idx < len(cells):
            fname = cells[file_col_idx].strip("`").strip()
            if fname and fname != "—":
                fp = source_dir / fname
                if not fp.exists():
                    missing.append(str(fname))
    return missing


def load_project_context(plan_root: Path) -> dict[str, str]:
    """Load project-level context for auto-filling placeholders.

    Reads backbone.md and DESIGN.md for project name, slug, module info.
    """
    ctx: dict[str, str] = {}

    # Try backbone
    backbone_path = plan_root / "02_backbone" / "backbone.md"
    if backbone_path.exists():
        bb_text = backbone_path.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", bb_text, re.MULTILINE)
        if m:
            ctx["project_name"] = m.group(1).strip()

    # Try PROJECT-HOME
    home_path = plan_root / "PROJECT-HOME.md"
    if home_path.exists():
        home_text = home_path.read_text(encoding="utf-8")
        m = re.search(r"Slug:\s*(\S+)", home_text)
        if m:
            ctx["slug"] = m.group(1).strip()

    # Try DESIGN.md
    design_glob = list(plan_root.parent.glob("designs/*/DESIGN.md"))
    if design_glob:
        design_text = design_glob[0].read_text(encoding="utf-8")
        m = re.search(r"Project:\s*(.+)", design_text)
        if m:
            ctx["project_name"] = ctx.get("project_name") or m.group(1).strip()

    return ctx


def auto_fill_placeholder(text: str, context: dict[str, str], module_name: str) -> tuple[str, int]:
    """Fill known [Placeholder] patterns from project context.

    Returns (filled_text, filled_count).
    Only fills patterns where context can provide a value.
    Does NOT fill portal IDs, nav schema IDs, or spec-level fields.
    """
    fill_map = {
        "Tên dự án": context.get("project_name", ""),
        "Tên module": module_name,
        "Project": context.get("project_name", ""),
        "Module": module_name,
    }
    count = 0

    def _refill(m: re.Match) -> str:
        nonlocal count
        inner = m.group(1).strip()
        if inner in fill_map and fill_map[inner]:
            count += 1
            return fill_map[inner]
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]", _refill, text), count


def parse_template(path: Path) -> list[dict]:
    """Extract heading structure from template file.

    Returns list of {level, slug, text, line_index}.
    """
    headings = []
    lines = path.read_text(encoding="utf-8").splitlines()
    heading_re = re.compile(r"^(#{1,4})\s+(.+)$")
    for i, line in enumerate(lines):
        m = heading_re.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            headings.append({"level": level, "slug": slugify(text), "text": text, "line_index": i})
    return headings


def find_section(lines: list[str], heading_slug: str) -> tuple[int, int, int | None]:
    """Find start/end line indices for a heading section.

    Returns (start_index, end_index, heading_level) or (-1, -1, None) if not found.
    Matches against slug of heading text with parenthesized parts stripped.
    """
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


def extract_section_body(lines: list[str], heading_slug: str) -> str:
    """Extract body content under a heading (excludes the heading line itself)."""
    start, end, level = find_section(lines, heading_slug)
    if start < 0:
        return ""
    return "\n".join(lines[start + 1:end]).strip()


def extract_fr_section(spec_content: str) -> str:
    """Extract FR table body from srs/spec.md (without heading line)."""
    lines = spec_content.splitlines()
    return extract_section_body(lines, "yeu-cau-chuc-nang")


def extract_nfr_section(spec_content: str) -> str:
    """Extract NFR section body from srs/spec.md (without heading line)."""
    lines = spec_content.splitlines()
    return extract_section_body(lines, "yeu-cau-phi-chuc-nang")


def extract_subsection(content: str, heading_slug: str) -> str:
    """Extract body under a subsection heading (excludes heading line)."""
    lines = content.splitlines()
    start, end, _ = find_section(lines, heading_slug)
    if start < 0:
        return ""
    return "\n".join(lines[start + 1:end]).strip()


def extract_uc_field(text: str, label: str) -> str:
    """Extract a bold markdown field value from a UC document."""
    match = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def build_uc_summary_table(uc_items: list[tuple[Path, str]]) -> str:
    """Build the SRS-level UC summary table from detailed UC canon files."""
    rows = [
        "| Mã UC (Use Case ID) | Tên UC (Use Case Name) | Tác nhân chính (Primary Actor) | Trigger | Điều kiện tiên quyết (Precondition) | Hậu điều kiện (Postcondition) |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for uc_file, uc_text in uc_items:
        first_heading = next((line.lstrip("#").strip() for line in uc_text.splitlines() if line.startswith("#")), "")
        uc_id = extract_uc_field(uc_text, "Mã UC (Use Case ID)") or uc_file.stem.replace("uc-", "UC-")
        name = first_heading.split(":", 1)[-1].strip() if first_heading else uc_id
        actor = extract_uc_field(uc_text, "Tác nhân chính (Primary Actor)") or "TBD"
        precondition = extract_uc_field(uc_text, "Điều kiện tiên quyết (Preconditions)") or "TBD"
        postcondition = extract_uc_field(uc_text, "Hậu điều kiện (Postconditions)") or "TBD"
        rows.append(f"| {uc_id} | {name} | {actor} | TBD | {precondition} | {postcondition} |")
    return "\n".join(rows)


def render_path(template: str, slug: str, date: str, module: str) -> str:
    return template.replace("{slug}", slug).replace("{date}", date).replace("{module_slug}", module)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic SRS compiler")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--module-root", type=Path, help="Direct path to module root")
    group.add_argument("--slug", help="Project slug (requires --repo)")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT, help=f"Repo root path (default: {REPO_ROOT})")
    parser.add_argument("--date", help="Date token YYMMDD-HHmm (required with --slug)")
    parser.add_argument("--module", help="Module slug (required with --slug)")
    parser.add_argument("--no-html", action="store_true", help="Skip HTML generation")
    args = parser.parse_args()

    if args.module_root:
        module_root = args.module_root.resolve()
        plan_root = module_root.parent.parent
        module_name = module_root.name
        date_token = plan_root.name.rsplit("-", 2)
        slug_val = "-".join(date_token[:-2]) if len(date_token) >= 3 else plan_root.name
        date_val = "-".join(date_token[-2:]) if len(date_token) >= 3 else ""
    else:
        if not (args.date and args.module):
            parser.error("--date and --module required with --slug")
        repo_path = args.repo.resolve()
        contract = json.loads((repo_path / "core" / "contract.yaml").read_text(encoding="utf-8"))
        module_rel = render_path(
            contract["paths"]["module_root"],
            slug=args.slug, date=args.date, module=args.module,
        )
        module_root = repo_path / module_rel
        plan_root = repo_path / f"plans/{args.slug}-{args.date}"
        slug_val = args.slug
        date_val = args.date
        module_name = args.module

    repo_root = args.repo.resolve()

    if not module_root.exists():
        print(f"ERROR: module root does not exist: {module_root}", file=sys.stderr)
        return 2

    template_path = repo_root / "templates" / "srs-template.md"
    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=sys.stderr)
        return 2

    template_headings = parse_template(template_path)
    template_lines = template_path.read_text(encoding="utf-8").splitlines()

    required_status = {}
    for rel in REQUIRED_SOURCE_FILES:
        p = module_root / rel
        required_status[rel] = {"exists": p.exists(), "path": p}
    for rel in OPTIONAL_SOURCE_FILES:
        p = module_root / rel
        required_status[rel] = {"exists": p.exists(), "path": p}

    missing_required = [rel for rel in REQUIRED_SOURCE_FILES if not required_status[rel]["exists"]]
    if missing_required:
        for rel in missing_required:
            print(f"ERROR: required source missing: {rel}", file=sys.stderr)
        return 2

    # Enforce required indexes and at least one content file per directory
    for rel in REQUIRED_INDEX_FILES:
        idx_path = module_root / rel
        if not idx_path.exists():
            print(f"ERROR: required index missing: {rel}", file=sys.stderr)
            return 2

    for dir_name, glob_pattern in REQUIRED_CONTENT_GLOBS.items():
        content_dir = module_root / dir_name
        content_files = sorted(content_dir.glob(glob_pattern))
        non_index = [f for f in content_files if f.name != "index.md"]
        if not non_index:
            print(f"ERROR: required content files missing in {dir_name}/ (pattern: {glob_pattern})", file=sys.stderr)
            return 2

    spec_content = (module_root / "srs" / "spec.md").read_text(encoding="utf-8")

    source_hashes = {}
    source_hashes["srs/spec.md"] = sha256_file(module_root / "srs" / "spec.md")

    for rel in OPTIONAL_SOURCE_FILES:
        if required_status[rel]["exists"]:
            source_hashes[rel] = sha256_file(required_status[rel]["path"])

    output_lines = list(template_lines)

    def replace_section(heading_slug: str, content: str):
        start, end, level = find_section(output_lines, heading_slug)
        if start < 0:
            return
        if content:
            content_lines = content.splitlines()
            output_lines[start + 1 : end] = content_lines
        else:
            pass

    compiled_sections = []
    placeholder_warnings = []
    index_disk_errors = []
    project_ctx = load_project_context(plan_root)
    auto_fill_total = 0

    # FR section
    fr_content = extract_fr_section(spec_content)
    if fr_content:
        replace_section("yeu-cau-chuc-nang", fr_content)
        compiled_sections.append("FR")

    # NFR section
    nfr_content = extract_nfr_section(spec_content)
    if nfr_content:
        replace_section("yeu-cau-phi-chuc-nang", nfr_content)
        compiled_sections.append("NFR")

    # Merge usecases
    usecases_index = module_root / "usecases" / "index.md"
    uc_entries = []
    cross_function_stats = {
        "ucs_scanned": 0, "ucs_with_section": 0, "ucs_with_edges": 0,
        "intra_module_resolved": 0, "inter_module_resolved": 0,
        "inter_module_pending": 0, "inter_module_mismatch": 0,
    }
    if usecases_index.exists():
        uc_dir = module_root / "usecases"
        uc_files = sorted(
            f for f in uc_dir.glob("uc-*.md")
            if f.name != "uc-index.md"
        )
        source_hashes["usecases/index.md"] = sha256_file(usecases_index)
        uc_items = []
        for uc_file in uc_files:
            source_hashes[f"usecases/{uc_file.name}"] = sha256_file(uc_file)
        for uc_file in uc_files:
            uc_raw = uc_file.read_text(encoding="utf-8")
            uc_text, uc_fm = strip_yaml_frontmatter(uc_raw)
            # Auto-fill placeholders from project context
            uc_text, filled = auto_fill_placeholder(uc_text, project_ctx, module_name)
            auto_fill_total += filled
            uc_items.append((uc_file, uc_text))
            cross_function_stats["ucs_scanned"] += 1
            # Detect remaining unfilled placeholders
            uc_label = f"usecases/{uc_file.name}"
            placeholder_warnings.extend(detect_placeholders(uc_text, uc_label))
            if "## Cross-Function Impact" in uc_text:
                cross_function_stats["ucs_with_section"] += 1
                edges = uc_text.count("|") - uc_text[:uc_text.find("## Cross-Function Impact")].count("|") if "## Cross-Function Impact" in uc_text else 0
                cross_function_stats["ucs_with_edges"] += 1 if edges > 2 else 0
                for status_line in uc_text.splitlines():
                    if "| Resolved " in status_line:
                        if "inter-module" in status_line.lower():
                            cross_function_stats["inter_module_resolved"] += 1
                        else:
                            cross_function_stats["intra_module_resolved"] += 1
                    elif "| Pending " in status_line:
                        cross_function_stats["inter_module_pending"] += 1
                    elif "| Mismatch " in status_line:
                        cross_function_stats["inter_module_mismatch"] += 1
        uc_entries.append(build_uc_summary_table(uc_items))
        uc_entries.extend(text for _, text in uc_items)
        compiled_sections.append("UseCases")
        # HARD GATE: verify index entries exist on disk
        uc_missing = verify_index_against_disk(usecases_index, module_root)
        if uc_missing:
            index_disk_errors.extend(f"usecases/index.md → {m}" for m in uc_missing)

    # Merge diagrams.md
    diagrams_path = module_root / "usecases" / "diagrams.md"
    if diagrams_path.exists():
        uc_entries.append(diagrams_path.read_text(encoding="utf-8"))
        source_hashes["usecases/diagrams.md"] = sha256_file(diagrams_path)

    if uc_entries:
        replace_section("dac-ta-use-case", "\n\n".join(uc_entries))

    # Merge screens (ascii-screen/)
    ascii_screen_index = module_root / "ascii-screen" / "index.md"
    screen_entries = []
    if ascii_screen_index.exists():
        screen_dir = module_root / "ascii-screen"
        screen_files = sorted(
            f for f in screen_dir.glob("*.md")
            if f.name != "index.md"
        )
        source_hashes["ascii-screen/index.md"] = sha256_file(ascii_screen_index)
        for sf in screen_files:
            source_hashes[f"ascii-screen/{sf.name}"] = sha256_file(sf)
        for sf in screen_files:
            screen_raw = sf.read_text(encoding="utf-8")
            screen_text, screen_fm = strip_yaml_frontmatter(screen_raw)
            # Auto-fill placeholders from project context
            screen_text, filled = auto_fill_placeholder(screen_text, project_ctx, module_name)
            auto_fill_total += filled
            screen_entries.append(screen_text)
            # Detect remaining unfilled placeholders
            sc_label = f"ascii-screen/{sf.name}"
            placeholder_warnings.extend(detect_placeholders(screen_text, sc_label))
        compiled_sections.append("Screens")
        # HARD GATE: verify index entries exist on disk
        sc_missing = verify_index_against_disk(ascii_screen_index, module_root)
        if sc_missing:
            index_disk_errors.extend(f"ascii-screen/index.md → {m}" for m in sc_missing)

    # BLOCK compile if index claims files that don't exist on disk
    if index_disk_errors:
        print("ERROR: Index-disk mismatch — index references files that do not exist:", file=sys.stderr)
        for err in index_disk_errors:
            print(f"  {err}", file=sys.stderr)
        print("Fix: write missing source files or update the index. Compile aborted.", file=sys.stderr)
        return 2

    if screen_entries:
        replace_section("mo-ta-man-hinh", "\n\n".join(screen_entries))

    # Optional: flows
    flows_path = module_root / "srs" / "flows.md"
    if flows_path.exists():
        flows_content = flows_path.read_text(encoding="utf-8")
        replace_section("so-do-luong-du-lieu", flows_content)
        compiled_sections.append("Flows")

    # Optional: erd
    erd_path = module_root / "srs" / "erd.md"
    if erd_path.exists():
        erd_content = erd_path.read_text(encoding="utf-8")
        replace_section("so-do-thuc-the-quan-he", erd_content)
        compiled_sections.append("ERD")

    # Navigation consistency validation
    design_paths = sorted(plan_root.parent.glob("designs/*/DESIGN.md")) if plan_root.parent.name != "BA-kit" else []
    nav_issues = []
    if design_paths and screen_entries:
        design_doc = design_paths[0]
        srs_temp = module_root / ".compile-temp-srs.md"
        srs_temp.write_text("\n".join(output_lines), encoding="utf-8")
        try:
            nav_result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "validate-navigation-consistency.py"),
                    "--design", str(design_doc),
                    "--screen-contract", str(srs_temp),
                ],
                capture_output=True, text=True, check=False,
            )
            if nav_result.returncode != 0:
                nav_issues.append({
                    "severity": "error",
                    "code": "NAV_CONSISTENCY_FAIL",
                    "message": nav_result.stderr.strip() or nav_result.stdout.strip(),
                })
        finally:
            if srs_temp.exists():
                srs_temp.unlink()

    # Assemble output
    now = datetime.now(timezone.utc)
    metadata_header = [
        f"> **Tài liệu tổng hợp:** Compile tự động từ canon sources lúc {now.strftime('%Y-%m-%d %H:%M:%S')} UTC.",
        f"> Module: {module_name} | Slug: {slug_val} | Date: {date_val}",
        f"> Sources: {', '.join(k for k in source_hashes)}",
        "",
    ]
    output_lines = metadata_header + output_lines

    full_output = "\n".join(output_lines)

    # Generate TOC
    heading_re = re.compile(r"^(#{1,3})\s+(.+)$")
    toc_lines = []
    for line in output_lines:
        m = heading_re.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            anchor = slugify(text)
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- [{text}](#{anchor})")

    # Write srs.md first (needed for compliance check)
    srs_path = module_root / "srs.md"
    srs_path.write_text(full_output, encoding="utf-8")

    # Run compliance checker for authoritative template_compliance
    compliance_errors = []
    try:
        compliance_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "check-srs-template-compliance.py"),
                "--srs", str(srs_path),
                "--repo", str(repo_root),
            ],
            capture_output=True, text=True, check=False,
        )
        if compliance_result.returncode != 0:
            try:
                checker_output = json.loads(compliance_result.stdout)
                compliance_errors = [
                    i.get("code", "") for i in checker_output.get("issues", [])
                    if i.get("severity") == "error"
                ]
            except json.JSONDecodeError:
                compliance_errors.append("compliance_checker_output_parse_error")
    except Exception:
        compliance_errors.append("compliance_checker_not_runnable")

    template_compliance = len(compliance_errors) == 0

    # HTML generation
    html_status = "skipped"
    html_path_str = ""
    html_error_str = ""

    if not args.no_html:
        compiled_root = plan_root / "04_compiled" / module_name
        compiled_root.mkdir(parents=True, exist_ok=True)
        html_out = compiled_root / "compiled-srs.html"

        try:
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "md-to-html.py"),
                    str(srs_path),
                    "--base-dir", str(module_root),
                    "--output", str(html_out),
                ],
                capture_output=True, text=True, check=True,
            )
            html_status = "generated"
            html_path_str = str(plan_root / "04_compiled" / module_name / "compiled-srs.html")
        except subprocess.CalledProcessError as e:
            html_status = "failed"
            html_error_str = e.stderr.strip()[:500]
        except OSError as e:
            html_status = "failed"
            html_error_str = str(e)[:500]

    # Write receipt
    receipt = {
        "compile_scope": "module",
        "requested_sections": compiled_sections,
        "included_sources": [k for k, v in required_status.items() if v["exists"]],
        "excluded_sources": [k for k, v in required_status.items() if not v["exists"]],
        "source_hashes": source_hashes,
        "cross_function": cross_function_stats,
        "template_compliance": template_compliance,
        "placeholder_autofill_count": auto_fill_total,
        "placeholder_warnings": placeholder_warnings,
        "html_status": html_status,
        "html_path": html_path_str,
        "html_error": html_error_str,
        "navigation_issues": nav_issues,
        "validation_errors": compliance_errors,
        "generated_at": now.isoformat(),
    }
    receipt_path = module_root / "srs-compile-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Report
    print(f"Compiled: {srs_path}")
    print(f"  Sections: {len(compiled_sections)} ({', '.join(compiled_sections)})")
    print(f"  Template compliance: {'PASS' if template_compliance else 'FAIL'}")
    if not template_compliance:
        for err in compliance_errors:
            print(f"    - {err}")
    if auto_fill_total > 0:
        print(f"  Auto-filled placeholders: {auto_fill_total}")
    if placeholder_warnings:
        print(f"  Placeholder warnings: {len(placeholder_warnings)} unfilled template placeholders")
        for pw in placeholder_warnings[:10]:
            print(f"    - {pw}")
        if len(placeholder_warnings) > 10:
            print(f"    ... and {len(placeholder_warnings) - 10} more")
    print(f"  HTML: {html_status}")
    if html_status == "failed":
        print(f"    Error: {html_error_str[:200]}")
    print(f"  Receipt: {receipt_path}")

    if not template_compliance:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
