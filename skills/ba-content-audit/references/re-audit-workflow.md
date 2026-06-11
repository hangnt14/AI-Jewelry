# Re-Audit Workflow

Detailed step-by-step for re-audit when an existing `audit-report.md` is found.

## Preconditions

- Project root resolved and verified to exist
- Existing `audit-report.md` found at `paths.audit_report` path
- `contract.yaml` loaded (paths resolved)
- `references/audit-rules.md` loaded (artifact rules)
- `template/audit-report-template.md` loaded (output format)

## Step 1: Load Existing Report

1. Read existing `audit-report.md` from `paths.audit_report`.
2. Parse frontmatter:
   - `audit_version`: current version number N
   - `previous_audit`: timestamp of previous audit (if any)
   - `total_findings`, `blocking`, `warning`, `info`
3. Extract all existing finding IDs into a set `old_finding_ids`.
4. Parse each finding row to extract: `{id, severity, file_path, location, description}`.

## Step 2: Re-Scan All Artifacts

Run the full first-audit scan (Steps 1–4 from `first-audit-workflow.md`):
1. Build file manifest
2. First pass: collect ID definitions
3. Second pass: audit each file (frontmatter, sections, cross-refs)
4. Orphan ID detection

This produces a new set of findings with content-hash IDs.

## Step 3: Compare & Classify

For each new finding:
- **ID exists in old set** → **Persistent** finding
  - If old severity was Warning, bump to Blocking (repeated issue) → annotate "Persistent (was Warning in v{N})"
  - If old severity was Blocking, keep Blocking → annotate "Persistent (was Blocking in v{N})"
  - If old severity was Info, keep Info → annotate "Persistent (was Info in v{N})"
- **ID NOT in old set** → **`[NEW]`** finding
  - Flag in finding row: `[NEW] B-{hash}`
  - Standard severity per audit-rules.md

For each old finding NOT in new set:
- **Finding resolved** → Move to "Resolved" section of report
  - Record: `{id, original_location, original_severity, resolution: "No longer detected — likely fixed"}`

## Step 4: Assemble Report

Write audit report with re-audit metadata:

### Frontmatter
```yaml
---
type: audit-report
project_slug: {slug}
project_date: {date}
audit_version: {N+1}
audit_timestamp: {iso_timestamp}
total_findings: {total}
blocking: {blocking_count}
warning: {warning_count}
info: {info_count}
previous_audit: {prev_timestamp}
new_findings: {new_count}
persistent_findings: {persistent_count}
resolved_findings: {resolved_count}
---
```

Note: `persistent_count = total_findings - new_count`. Computed after classification.

### Body Structure

1. **Summary** — updated counts
2. **Delta Summary** — new section for re-audit:
   ```
   | Metric | Count |
   |--------|-------|
   | [NEW] findings | {N} |
   | Persistent findings | {M} |
   | Resolved since v{prev_version} | {K} |
   ```
3. **Blocking** — grouped by file, `[NEW]` flag on new ones
4. **Warning** — grouped by file, `[NEW]` flag on new ones
5. **Info** — grouped by file, `[NEW]` flag on new ones
6. **Fix Commands** — Map every Blocking and Warning finding to an actionable command per `references/audit-rules.md` Finding-to-Fix-Command Mapping section, grouped into Direct Edit / Skill-Based / Manual Actions tables.

## Step 5: Print Chat Summary

```
🔄 Re-audit complete: {slug} (v{new_version})
   [NEW]: {N} | Persistent: {M} | Resolved: {K}
   Blocking: {B} | Warning: {W} | Info: {I}
   Report: {report_path}

🔴 [NEW] Blocking:
   - {id}: {file} {location} — {description}
   ... (max 5)

🔄 Persistent Blocking:
   - {id}: {file} {location} — {description}
   ... (max 5)

🟡 Top [NEW] Warnings:
   ... (max 5)

✅ Resolved: {K} findings (see report for details)
```
