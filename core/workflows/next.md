<purpose>
Detect the next logical BA step from the current BA-kit artifact set.

This command is the BA equivalent of a lightweight state machine. It reads the current project
artifacts and recommends the next exact command.  It must stay deterministic and compact — no
broad artifact reads, no content parsing beyond what is needed to classify state.
</purpose>

<required_reading>
Read `contract.yaml` and `contract-behavior.md` only.  Do not read full backbone, stories, or SRS
to compute the next step.
</required_reading>

<discovery_strategy>
Snapshot-first, then stat-only fallback:

1. Check for `plans/{slug}-{date}/02_backbone/package-snapshot.md`.
   - If present and `snapshot_state: current`, derive artifact existence from its `artifacts` list.
   - If absent or `snapshot_state: degraded`, fall back to filesystem stat checks only.
2. Read `paths.plan` header (first 30 lines) to detect options status and selected option.
3. Do not read backbone content, stories content, or SRS content to determine the next step.
4. Emit `READ_ESCALATION: next read {path} due to {reason}` only when content is genuinely
   required to resolve an ambiguous gate (e.g., backbone gate section missing from snapshot).
</discovery_strategy>

<process>

<step name="resolve_project">
Resolve the target slug and dated set using the artifact contract.

Rules:
- prefer explicit `--slug`
- otherwise detect a single existing project set from exact BA-kit artifact patterns
- if ambiguous, stop and ask the user to choose
- when the next exact command would be module-scoped (`frd`, `stories`, `srs`, or `wireframes`),
  resolve the module using the contract rules before emitting the command
- if multiple module directories exist, stop and ask instead of emitting an incomplete
  module-scoped command
</step>

<step name="inspect_artifacts">
Using the snapshot manifest or stat-only checks, determine which of these exist:
- intake
- plan
- options index
- option files
- comparison file
- backbone
- frd
- user stories
- srs
- wireframe-input
- wireframe-map
- wireframe-state
- packaged FRD/SRS HTML
- reverse_baseline_lock (stat only: `plans/{slug}-{date}/00_reverse/reverse-baseline-lock.json`)
- reverse_index (stat only: `plans/{slug}-{date}/00_reverse/reverse-index.md`)
- reverse_evidence_ledger (stat only: `plans/{slug}-{date}/00_reverse/reverse-evidence-ledger.md`)
- reverse_drift_state (stat only: `plans/{slug}-{date}/00_reverse/reverse-drift-state.json`)

When the snapshot is current, use its `artifacts` list directly.
When the snapshot is absent or degraded, use filesystem stat only — do not open files.
Read the backbone gate section only when the snapshot is absent and gate ambiguity cannot be
resolved from artifact presence alone.
Do not open reverse lane files to determine next step — stat checks only.
</step>

<step name="determine_next_step">
Apply the first matching rule:

1. no intake -> next step `ba-start intake`
2. intake exists and `paths.plan` says options are `recommended` or `in-progress` -> `ba-start options --slug <slug>`
3. intake exists and `paths.plan` is missing, invalid, or says `completed` without `selected option` -> `ba-start status --slug <slug>`
4. intake exists, `paths.plan` says options are `not-needed`, and no backbone -> `ba-start backbone --slug <slug>`
5. intake exists, `paths.plan` says options are `skipped`, or `completed` with `selected option` recorded in `paths.plan`, and no backbone -> `ba-start backbone --slug <slug>`
6. backbone exists and FRD is explicitly required but missing -> `ba-start frd --slug <slug> --module <module_slug>`
7. backbone exists but user stories are missing -> `ba-start stories --slug <slug> --module <module_slug>`
8. SRS is required and missing -> `ba-start srs --slug <slug> --module <module_slug>`
9. wireframe-input exists and wireframe-state is missing while wireframe handoff is required -> `ba-start wireframes --slug <slug> --module <module_slug>`
10. final markdown exists but required packaged HTML is missing -> `ba-start package --slug <slug>`
11. everything required already exists -> `ba-start status --slug <slug>`

Reverse lane rules (apply only when reverse_baseline_lock exists):

R1. reverse_baseline_lock exists but reverse_evidence_ledger is absent -> `ba-start reverse impact --slug <slug>`
    Reason: baseline scan complete but evidence not yet classified.
R2. reverse_evidence_ledger exists and has unclassified entries (stat check only — do not open file to count) -> `ba-start reverse impact --slug <slug>`
    Reason: unclassified evidence blocks promotion.
    Block rule: do NOT guess next step from evidence content. If classification state is unknown from stat alone, emit `ba-start reverse status --slug <slug>` instead.
R3. reverse_evidence_ledger exists and reverse_drift_state is absent -> `ba-start reverse status --slug <slug>`
    Reason: drift state not yet computed; user should inspect before promoting.
R4. reverse_drift_state exists and reverse_evidence_ledger has unpromoted as_built_drift entries -> `ba-start reverse promote --slug <slug> --evidence-ids <ids>`
    Reason: classified drift ready for promotion.
    Block rule: do NOT infer evidence IDs from file content. Emit the command template and tell the user to supply IDs from `ba-start reverse status`.
R5. all reverse evidence promoted and no unclassified remain -> continue to forward lifecycle rules above (rules 1–11).

Reverse lane guard:
- Never auto-pick a reverse lane step when focus_selection is missing from baseline lock.
- If reverse_baseline_lock exists but focus_selection is empty or absent, emit:
  `ba-start reverse --slug <slug>` with reason "focus_selection missing — re-run baseline scan to select focus areas."
- Reverse lane rules (R1–R5) take priority over forward rules (1–11) only when reverse_baseline_lock exists and the reverse lane is not yet complete.

When FRD/SRS/wireframe-handoff gates are unclear, explain the uncertainty and recommend
`ba-start status --slug <slug>` instead of guessing.
</step>

<step name="display">
Print a compact, deterministic block:

```text
BA Next

Project: {slug}
Date set: {date}
Snapshot: current | degraded | absent
Project Home: {PROJECT-HOME.md exists/missing}
Reverse lane: active | complete | absent
Next command: /ba-start ...
BA-facing next step: ...
Reason: ...
```

Do not mutate artifacts during this command.
</step>

</process>

<success_criteria>
- [ ] Project set resolved exactly or ambiguity surfaced
- [ ] Artifact state derived from snapshot or stat-only — no broad content reads
- [ ] Next BA command recommended from the current state
- [ ] Output is deterministic and compact
- [ ] No artifacts mutated
</success_criteria>
