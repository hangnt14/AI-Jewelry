# QC Review Behavior

> Behavior shard for `qc-review` command. Loaded after `core/contract.yaml` and `core/contract-behavior.md`.
> Defines gate trigger logic, verdict handling, auto-remediation loop, gap classification, escape hatch, and traceability.

---

## Read Scope

| Category | Paths |
|---|---|
| Must read | `core/contract.yaml`, `core/contract-behavior.md`, `skills/qc-uc-review/SKILL.md` |
| Must read | `skills/qc-uc-review/profiles/{platform}.md` |
| Must read | `skills/qc-uc-review/references/scoring-rubric.md` |
| May read | Target UC/SRS artifacts, CMR, wireframes (as needed by audit) |
| May read | `skills/qc-uc-review/references/first-audit-workflow.md` or `re-audit-workflow.md` |
| Must not read | Module artifacts outside the current audit scope |
| Must not read | Other modules' warm shards unless assembling compiled output |

---

## Gate Trigger

After a mutable command completes, check `quality_gates` in `contract.yaml` for a gate with `trigger_after` matching the completed command.

If found:
1. Resolve platform: use `--platform` flag if present, else `defaults.platform`.
2. Load profile from `skills/qc-uc-review/profiles/{platform}.md`.
3. Execute audit per `skills/qc-uc-review/references/first-audit-workflow.md`.
4. Produce verdict signal: `{ verdict, score, platform, blockers, report_path }`.
5. Evaluate `block_on` condition from gate config.
6. If `block_on` is false: log gate pass, proceed.
7. If `block_on` is true: enter Remediation Loop below.

---

## Verdict Handling

Parse verdict signal: `{ verdict, score, platform, blockers, report_path }`

| Verdict | Score range | Action |
|---|---|---|
| `READY` | score >= 85 | Log pass. Proceed to next lifecycle step. |
| `CONDITIONALLY_READY` | 70 <= score < 85 | Enter remediation loop. |
| `NOT_READY` | score < 70 | Enter remediation loop. |
| Auto-fail | Any critical KA (#1–#9) = 0 | Enter remediation loop regardless of score. |

---

## Auto-Remediation Loop

```
max_retries: 2
retry_count: 0

LOOP:
  1. Read gap report from report_path.
  2. For each gap/blocker in report:
     - Classify: fixable_from_context | requires_user_input
  3. Fix all fixable_from_context gaps inline in the target artifact.
  4. Increment retry_count.
  5. Re-trigger audit (same profile, same platform).
  6. If verdict == READY: exit loop, log pass, proceed.
  7. If retry_count >= max_retries: exit loop, escalate to user.

On requires_user_input gaps (any retry):
  Surface: "Gap [ID]: [question] — needed for KA#[N] (impact: [score delta]pts)"
  Wait for user response before proceeding to next retry.

On max_retries_exceeded:
  Surface: "QC gate failed after 2 remediation attempts. Remaining gaps:"
  List all remaining blockers with KA reference and score impact.
  Offer: "Fix these gaps manually and re-run, or use --skip-gate to proceed."
```

Hard limit: max_retries = 2. After 2 attempts, always escalate — never loop further.

---

## Gap Classification

### fixable_from_context

Gaps where the required information is derivable from existing artifacts without a business decision:

- Missing exception flows → derivable from CMR error patterns
- Edge case coverage gaps → derivable from platform profile checklist (groups A–E)
- Missing AC section → synthesizable from documented flows and postconditions
- Inconsistent terminology → fixable by aligning to backbone canonical vocabulary
- Missing postconditions → derivable from flow outcomes already described in UC
- Missing CMR cross-references → resolvable by scanning CMR and matching applicable rules

### requires_user_input

Gaps that require a business decision or information not present in any artifact:

- Undefined business rules (e.g., "what happens when role is unknown?")
- Missing stakeholder decisions (e.g., "which exact error message to show?")
- Ambiguous scope (e.g., "is feature X in scope for this UC?")
- Conflicting requirements between artifacts where resolution requires BA judgment
- Missing data that does not exist in any available artifact

When in doubt between classifications → choose `requires_user_input`. Never invent business rules.

---

## Escape Hatch

User may pass `--skip-gate` to bypass QC gate enforcement.

Requires explicit confirmation before proceeding:

> "Are you sure? Skipping the QC gate means downstream artifacts may be built on untestable requirements. Type 'confirm skip' to proceed."

On confirmation: log skip event and continue lifecycle.
On no confirmation: abort skip, return to gate enforcement.

Log entry: `QC gate SKIPPED by user at {command} step — {timestamp}`

---

## Traceability

After each gate execution (pass, fail, or skip), append a log entry to project memory:

```
Gate: {gate_name}
Timestamp: {YYYY-MM-DD HH:mm}
Command: {trigger_after command}
Platform: {platform}
Profile: {profile}
Score: {score}/100
Verdict: {READY | CONDITIONALLY_READY | NOT_READY}
Remediation attempts: {retry_count}
Gaps fixed inline: {count}
Gaps escalated to user: {count}
Disposition: passed | skipped | user-resolved | blocked
Report: {report_path}
```

Append to `paths.memory_log` when it exists. If only compact memory exists, append a summary line to `paths.project_memory` under a `## QC Gate Log` section.
