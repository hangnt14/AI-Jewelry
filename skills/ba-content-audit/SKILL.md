---
name: ba-content-audit
description: Cross-artifact format and cross-reference consistency audit for BA-kit projects. Read-only — never mutates artifacts.
argument-hint: "--slug <slug> [--date <date>]"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# BA Content Audit

Read-only cross-artifact audit for BA-kit lifecycle projects. Scans all artifacts (intake → backbone → modules → compiled → shared), reports format compliance issues and cross-reference integrity breaks. Output goes to `plans/{slug}-{date}/shared/audit-report.md`.

## Invocation

```text
/ba-content-audit --slug warehouse-rfp
/ba-content-audit --slug warehouse-rfp --date 260611-0900
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--slug <slug>` | Yes | Project slug (e.g., `warehouse-rfp`) |
| `--date <date>` | No | Project date token (`YYMMDD-HHmm`). If omitted: glob `plans/{slug}-*`; single match → use; multiple matches → `AskUserQuestion`; zero → error |

## Execution Context

Read `core/contract.yaml` for path resolution and `core/contract-behavior.md` for shared behavior rules.

Read `references/audit-rules.md` for per-artifact-type format rules, severity classification, and cross-reference resolution logic.

Read `template/audit-report-template.md` for output format.

## Process

### Step 1: Resolve Project Path

1. Parse `--slug` (mandatory) and optional `--date` from `$ARGUMENTS`.
2. Read `core/contract.yaml` → resolve `paths.project_root` with `{slug}` and `{date}`.
3. If `--date` provided → use exact path.
4. If `--date` omitted:
   - Glob `plans/{slug}-*` for matching directories.
   - Single match → auto-select.
   - Multiple matches → `AskUserQuestion` to let user pick.
   - Zero matches → error: "No project found for slug '{slug}'".
5. Verify project root exists on disk. If not → Blocking error, stop.

### Step 2: Route to Audit Flow

1. Read `core/contract.yaml` → resolve `paths.audit_report` → full path to expected report.
2. Check if `audit-report.md` exists at that path.
3. **Exists** → Re-audit flow (see `references/re-audit-workflow.md`).
4. **Not found** → First-audit flow (see `references/first-audit-workflow.md`).

### Step 3: Execute Audit Workflow

Detailed steps in the referenced workflow file. Overview:

**First audit** (`references/first-audit-workflow.md`):
- Scan artifacts in lifecycle order
- Per-file: frontmatter check, mandatory sections check, cross-reference check
- Classify findings as Blocking / Warning / Info per `references/audit-rules.md`
- Write report per `template/audit-report-template.md`

**Re-audit** (`references/re-audit-workflow.md`):
- Load existing report
- Re-scan all artifacts
- Compare old vs new findings using content-hash IDs
- Flag `[NEW]`, bump severity on persistent, move resolved to "Resolved" section
- Overwrite report preserving trace

### Step 4: Output

1. Write audit report to `paths.audit_report` path (resolved from contract.yaml).
2. Print compact chat summary:
   - Blocking count + top 3-5 Blocking findings
   - Warning count + top 3-5 Warning findings
   - Info count
   - Report file path
   - "Fix commands: see `## Fix Commands` in report — copy-paste per finding."

## Boundaries

- **Read-only**: Never mutate any artifact file.
- **No external calls**: No MCP, no API, no network.
- **.pen files skipped**: Pencil MCP-managed, encrypted — skip without reading.
- **Empty modules**: Skip with Info finding.
- **Large files**: Read anyway — audit integrity overrides context budget.
- **P2 artifacts deferred**: Tool-lanes, reverse, QC, memory-deep — not audited in v1.

## References

- `references/audit-rules.md` — Per-artifact-type format rules + cross-reference resolution
- `references/first-audit-workflow.md` — First-audit detailed steps
- `references/re-audit-workflow.md` — Re-audit detailed steps
- `template/audit-report-template.md` — Report output format
- `core/contract.yaml` — Path definitions
- `core/contract-behavior.md` — Shared behavior rules
