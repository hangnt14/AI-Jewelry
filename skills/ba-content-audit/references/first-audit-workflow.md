# First-Audit Workflow

Detailed step-by-step for first-time audit when no existing `audit-report.md` is found.

## Preconditions

- Project root resolved and verified to exist
- `contract.yaml` loaded (paths resolved)
- `references/audit-rules.md` loaded (artifact rules)
- `template/audit-report-template.md` loaded (output format)

## Step 1: Build File Manifest

Scan project root to discover all artifacts. For each contract.yaml path key in core lifecycle (P0), resolve with `{slug}`, `{date}`, and `{module_slug}` placeholders.

### 1a: System-Level Artifacts

Scan in order:
1. `01_intake/intake.md`
2. `01_intake/plan.md`
3. `PROJECT-HOME.md`
4. `02_backbone/backbone.md`
5. `02_backbone/backbone-index.md`
6. `02_backbone/common-rules.md` (if exists)
7. `02_backbone/message-list.md` (if exists)
8. `02_backbone/shared-rule-message-index.md` (if exists)
9. `02_backbone/shared-shell-contract.md` (if exists)
10. `02_backbone/shared-shell-index.md` (if exists)
11. `02_backbone/project-memory.md` (if exists)

### 1b: Design Doc

- `designs/{slug}/DESIGN.md` (if exists)

### 1c: Module Artifacts

For each `03_modules/{module_slug}/` directory found:
1. `MODULE-HOME.md` (if exists)
2. `frd.md` (if exists)
3. `srs/spec.md` (if exists)
4. `srs/flows.md` (if exists)
5. `srs/states.md` (if exists)
6. `srs/erd.md` (if exists)
7. `srs.md` (compiled, if exists)
8. `screen-field-contract.yaml` (if exists)
9. `userstories/index.md` + all `us-*.md` files
10. `usecases/index.md` + all `uc-*.md` files
11. `ascii-screen/index.md` + all `*.md` files (except `.pen`)
12. `brainstorms/index.md` + all `*.md` files (if brainstorm root exists)

Skip: `.pen` files, `tool-lanes/` directory, `figma-sync/` directory, `qc-review/` directory (P2).

### 1d: Compiled & Shared

1. `04_compiled/compiled-frd.html` (if exists)
2. `04_compiled/compiled-srs.html` (if exists)
3. Per-module `04_compiled/{module_slug}/compiled-srs.html` (if exists)
4. `shared/traceability.md` (if exists)
5. `shared/staleness.md` (if exists)
6. `shared/definitions.md` (if exists)

### 1e: Changes & Impacts

If `changes/` or `impacts/` directories exist under project root:
1. `changes/CR-*.md` files
2. `impacts/CR-*-impact.md` files

If these directories do not exist → skip silently (no finding emitted). These artifacts are optional extensions.

### Empty Module Handling

If `03_modules/{module_slug}/` exists but has no artifact files → emit one Info finding: "Module '{module_slug}' directory exists but contains no artifacts."

## Step 2: First Pass — Collect ID Definitions

Scan all discovered files to build a global ID definition map. For each file, parse:

1. **Frontmatter IDs**: If frontmatter has explicit `id:` or `story_id:` fields
2. **Body ID patterns**: Match regex patterns from `audit-rules.md` ID Pattern Regex section
3. **Heading IDs**: Headings containing ID patterns like `## FR-payment-001`

Store as: `{id: {file_path, line_number, type}}`

Also collect:
- **Defined wikilinks**: All file paths are candidates for link targets
- **Index file entries**: For cross-reference validation in Step 3

## Step 3: Second Pass — Audit Each File

For each file in manifest, run three check groups:

### 3a: Frontmatter Check

1. Parse YAML frontmatter (between opening `---` and closing `---`)
2. If no frontmatter → Blocking: `B-{hash}` "Missing YAML frontmatter"
3. If frontmatter exists but malformed YAML → Blocking: `B-{hash}` "Cannot parse frontmatter: {error}"
4. Check required fields per `audit-rules.md` for this artifact type:
   - Missing required field → Blocking
   - Missing optional field → Info
   - Wrong value for `type` field → Blocking
5. Check `type` field matches expected value per `audit-rules.md`:
   - `type` mismatch → Blocking: `B-{hash}` "Expected type '{expected}', got '{actual}'"
6. Check naming convention (filename matches expected pattern) → Warning if deviation

### 3b: Template Section Check

**Template-at-runtime approach**: For artifact types with a template reference in `audit-rules.md`:

1. Read the referenced template file from `templates/`
2. Extract all `##` level headings from template (these are expected sections)
3. For the target artifact, extract all `##` level headings
4. Compare:
   - Template section present in artifact → OK
   - Template section missing in artifact → Blocking: `B-{hash}` "Missing mandatory section '{section_name}'"
   - Artifact section not in template → Info: `I-{hash}` "Extra section '{section_name}' not in template"

**Skip for**: HTML files (compiled), machine_facing artifacts without templates, agent_facing artifacts (structure varies — only frontmatter check).

### 3c: Cross-Reference Check

For each file, scan content for cross-references:

1. **Frontmatter `links:`**: Parse YAML list, resolve each path relative to project root, check if file exists.
   - Missing target → Blocking
2. **Wikilinks `[[path]]` / `[[path|text]]` / `[[path#anchor|text]]`**:
   - Extract path before `#` or `|`
   - Resolve relative to project root
   - Check if file exists → Blocking if broken
   - Check anchor if present → Info (P2)
3. **ID references**: Match regex patterns from `audit-rules.md`
   - Look up in Step 2 ID definition map
   - Found → OK
   - Not found → Warning
   - Never referenced → Info (computed after all files scanned)
4. **Index file entries**: Match `- [label](path)` patterns in index files
   - Resolve path relative to index location
   - Check if target file exists → Warning if broken
5. **Markdown links `[text](url)`**:
   - Skip `https?://` URLs
   - Resolve relative paths, check if file exists → Warning if broken
6. **Backbone module list**: In `backbone.md`, extract module names from relevant sections (e.g., module tables, lists)
   - Verify `03_modules/{module_slug}/` directory exists → Blocking if missing

## Step 4: Orphan ID Detection

After all files scanned, for each ID in the Step 2 definition map:
- If ID is defined but never referenced in any other file → Info: `I-{hash}` "ID '{id}' defined but never cross-referenced"

## Step 5: Classify & Assign Finding IDs

For each finding:
1. Determine severity: Blocking / Warning / Info per `audit-rules.md`
2. Generate content-hash ID: `{Prefix}-{first 6 chars of SHA-256("{file_path}:{check_type}:{location_key}")}`
   - `check_type`: `frontmatter`, `section`, `crossref`, `naming`, `id_orphan`
   - `location_key`: section name, field name, link path, or ID string
3. Generate hash using available tools (Bash: `echo -n "string" | shasum -a 256 | cut -c1-6`)

## Step 6: Write Report

Write audit report to `paths.audit_report` path per `template/audit-report-template.md`:
- Frontmatter: `type: audit-report`, `audit_version: 1`, `previous_audit: none`
- Summary table: Blocking / Warning / Info counts
- Findings grouped by severity, then by artifact path
- Each finding: ID, severity, location, description, suggested fix
- **Fix Commands**: Map every Blocking and Warning finding to an actionable command per `references/audit-rules.md` Finding-to-Fix-Command Mapping section, grouped into Direct Edit / Skill-Based / Manual Actions tables

## Step 7: Print Chat Summary

```
✅ Audit complete: {slug}
   Blocking: {N} | Warning: {M} | Info: {K}
   Report: {report_path}

🔴 Blocking:
   - {id}: {file} {location} — {description}
   ... (max 5, then "+{remaining} more")

🟡 Top Warnings:
   - {id}: {file} {location} — {description}
   ... (max 5, then "+{remaining} more")

🔵 Info: {K} findings (see report for details)
```
