# BA-kit Contract Behavior

Use this file as the shared runtime-neutral behavior layer for BA-kit.

- `core/contract.yaml` is canonical for paths, prerequisites, defaults, state enums, thresholds, and resolution sequences.
- This file is canonical for behavior that every command must follow.
- Command-specific policy lives in `core/behavior/` and is selected through `behavior_shards.<command>`.
- If this file and `core/contract.yaml` disagree on a literal path or threshold, trust `core/contract.yaml` for the value and this file for the policy intent.

## Required Read Order

1. Read `core/contract.yaml` for exact paths, prerequisites, defaults, states, command metadata, and `behavior_shards`.
2. Read `core/contract-behavior.md` for shared runtime-neutral policy.
3. Parse arguments and resolve the selected subcommand.
4. Read only the behavior shard(s) listed in `behavior_shards.<command>`.
5. Read only the matching step file.
6. Read templates and upstream artifacts only when the active step needs them.

## Shared Operating Rules

- Write BA deliverables in Vietnamese by default unless the user explicitly requests English.
- Use the defaults defined under `defaults.*`.
- Treat the backbone as the primary authoring source once it exists.
- Use exact artifact matching only. Never infer from closest-looking filenames or mtime.
- Keep module-scoped authoring inside `paths.module_root` and compiled output inside `paths.compiled_root`.
- Treat `paths.project_home` as the BA-facing dashboard. It is not a source of truth and must not override backbone, intake, or module artifacts.
- Runtime-local chat memory is not authoritative. Persist reusable project memory on disk.

## Argument Parsing

Parse arguments before doing any work.

1. Read tokens left to right.
2. Extract `--slug <slug>`, `--date <date>`, `--module <module_slug>`, and `--mode <lite|hybrid|formal>` when present.
3. The first remaining lifecycle token is the subcommand: `intake`, `impact`, `options`, `backbone`, `frd`, `stories`, `srs`, `wireframes`, `package`, `status`, or `next`.
4. Friendly aliases may be translated before execution: continue/resume -> `next`, change assessment -> `impact`, option brainstorming/selection -> `options`, UI handoff -> `wireframes`, handoff package -> `package`, status check -> `status`.
5. If no subcommand is present, run the full lifecycle from intake.
6. For `intake`, allow one free argument as the source path hint.
7. For `impact`, allow one free argument as the change file path hint.
8. For `options`, allow `--select <option-id>` and `--skip` as mutually exclusive controls.
9. For `frd`, `stories`, `srs`, and `wireframes`, enforce `commands.<name>.module_required`.
10. Reject unknown subcommands and unexpected free arguments instead of guessing.

## Natural-Language Routing

Infer `impact` when the user refers to an existing project set or downstream artifact and says a requirement, rule, actor, acceptance criterion, screen behavior, or scope item changed, was added, or was removed.

Also infer `impact` when exactly one project set can be resolved from disk and the user sends a bare correction statement without explicitly asking to update, overwrite, regenerate, or rerun a named artifact.

Do not mutate artifacts directly from a bare correction statement. Route to impact first. Collaboration intent routes to `ba-collab`; GitHub side effects require explicit approval after showing files and action plan.

## Resolution Rules

Use the resolution order from `resolution.*`.

### Slug

- Prefer explicit `--slug`.
- Otherwise inspect directories matching `patterns.project_dir` under `plans/`.
- Ignore legacy report trees.
- If more than one slug exists, stop and ask.

### Date

- Prefer explicit `--date`.
- Otherwise derive the date from the resolved project directory name.
- If more than one dated set exists for the slug, stop and ask.

### Module

- For commands where `commands.<name>.module_required` is `true`, prefer explicit `--module`.
- If the project contains exactly one module directory, use it.
- If multiple module directories exist, stop and ask.
- Never infer a module from partial filename matches.

## Legacy Detection

- Treat anything under `legacy.roots` as out-of-contract for current lifecycle execution.
- If legacy artifacts exist but modular artifacts do not, stop and tell the user to migrate or rerun.
- Do not mix legacy and modular artifacts in one silent pass.

## Prerequisite Behavior

- Use `commands.<name>.requires` plus `paths.*` to resolve exact prerequisite files.
- If any required artifact is missing, print the exact missing path, the prior command to run, and stop.
- For `package`, block only when wireframe state is `missing`.
- If no wireframe-state marker exists, treat it as `not-applicable` only when the SRS set has no UI-backed screens or Screen Contract Plus section. Otherwise treat it as `missing`.

## Overwrite Behavior

Before mutating `backbone`, `frd`, `stories`, `srs`, `wireframes`, or `package`:

1. Check whether the target output path already exists.
2. If it exists, print the exact path and ask whether to overwrite.
3. If overwrite is not explicitly approved, stop without mutating.

## Context-Loss Recovery

If exploration consumes context or the host truncates conversation history:

1. Reconstruct the active target from command, slug, date, optional module, and on-disk artifacts.
2. Continue from the next unresolved step when those values are still unambiguous.
3. Do not ask the user to restate the request merely because exploration consumed context.

## Accepted-Scope Execution Lock

After the user explicitly approves a mutating rerun step:

- keep the current step locked for the rest of the run
- do not reopen generic discovery
- do not ask what to do next unless command, slug, date, module, or overwrite approval becomes genuinely ambiguous

## Token Discipline

- Read the selected step file, not the whole BA lifecycle.
- Read only the exact upstream artifacts needed by the active step.
- Use `templates/manifest.json` or CLI extraction helpers instead of loading full templates when only one group is needed.
- Reuse summaries and excerpts instead of rereading large raw sources when normalized artifacts already exist.
- For large source inputs, read `paths.source_summary` and `paths.source_chunk_index` before selecting chunk files.
- After `paths.backbone_index`, `paths.stories_index`, or `paths.srs_index` exists, read the index first and open only targeted sections from the source artifact.
- Treat index files as navigators only; they do not replace source-of-truth artifacts.

### Internal Artifact Compactness

Artifact profile controls format and length:

- `user_facing`: deliverable or package output; write complete BA-readable content.
- `agent_facing`: navigator, packet, memory shard, or state summary; write compact tables/lists with IDs, paths, freshness, ownership, and route hints only.
- `machine_facing`: deterministic state or manifest; prefer JSON/YAML/NDJSON and avoid prose beyond stable labels.

Generated internal artifacts must not duplicate requirement prose from intake, backbone, stories, or SRS. Keep excerpts short, include stale/unknown status instead of guessing, and move substantial prose into the source-of-truth artifact.

## Large Artifact Write Protocol

When generating artifacts that exceed about 150 lines, use incremental writes:

1. Write the skeleton first using the template structure.
2. Append group content sequentially into the correct section.
3. Confirm each append before moving on.
4. Never assemble and flush the full artifact in one large write.

## Runtime-Neutral HITL Contract

BA-kit is a playbook, not a UI product. Human-in-the-loop behavior is enforced through artifact routing and contract rules, not screen interactions.

- Core guarantees must stay identical across Claude Code, Codex, and Antigravity.
- A runtime adapter may translate command syntax or prompts, but it must preserve the same resolution, stop conditions, approval gates, and rerun rules.

## Granular Artifact Intervention

Minimum intervention units include goal IDs, actor IDs, feature IDs, FR/NFR IDs, story IDs, acceptance criteria, use case IDs, screen IDs, rule/message codes, and glossary terms.

When a user change attaches to stable nodes, update only the narrowest source-of-truth artifact that owns those nodes. Do not rewrite the whole project set when a narrower rerun path is sufficient.

## Active Push-back And Fail-Closed Behavior

When uncertainty is material, stop and ask instead of filling the gap with plausible prose.

Material uncertainty includes ambiguous scope or module, conflicting terminology, unclear behavior or ownership, unclear navigation schema, and changes that could touch multiple source-of-truth layers.

Fail-closed rules:

- If a required fact is missing, mark it as an assumption or open question instead of presenting it as settled.
- If a downstream artifact would require guessing an upstream decision, stop and route back to the owning step.
- If a correction invalidates a persisted assumption, record the rejected assumption in project memory on the next approved mutating rerun.

## Read Scope Contract

Every command has deterministic read scope. Load the selected command shard for its must-read, may-read, and must-not-read rules. Commands navigate summary -> index -> targeted shards.

### Index-First Navigation Rule

When shard memory exists:

1. Read `paths.memory_index` first to determine which shards are relevant.
2. Load only the shards the index routes to.
3. Never load the full shard tree when a targeted read is possible.

### Escalation Rule

A command may escalate its read scope only when the index routes to an additional shard, the user states an explicit audit/context need, or missing shard routing would otherwise require guessing.

Emit: `READ_ESCALATION: {command} read {path} due to {reason}.`
