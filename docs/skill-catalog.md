# BA-kit Skill Catalog

## Purpose

This catalog explains the BA-kit workflow skill plus the maintenance skills that support packaging, publishing, and runtime upkeep.

## Skill

| Skill | When to Use | Related Templates | Related Agents | Typical Output |
| --- | --- | --- | --- | --- |
| `ba-start` | Full BA engagement, reverse as-built analysis, or resumable step-level reruns from raw input to packaged deliverables | `project-home-template.md`, `intake-form-template.md`, `requirements-backbone-template.md`, `frd-template.md`, `user-story-template.md`, `srs-template.md`, `design-md-template.md`, `wireframe-input-template.md`, `wireframe-map-template.md` | `requirements-engineer`, `ui-ux-designer`, `ba-documentation-manager`, `ba-researcher` | Project Home dashboard, intake form, option pack + comparison when needed, requirements backbone, gated FRD/stories/SRS artifacts, reverse evidence lane, project runtime `DESIGN.md`, wireframe constraint pack, manual wireframe handoff map, FRD/SRS HTML, quality review, artifact status |
| `ba-collab` | Module ownership, review packets, conflict checks, and approval-gated GitHub handoff | `collab-home-template.md`, `module-home-template.md`, `review-packet-template.md` | Lead BA / Module BA roles | Collab Home, Module Home, review packet, optional approved PR handoff |
| `ba-kit-update` | Update the installed BA-kit runtime assets from the registered source repo | None | None | One-command fast-forward update and reinstall |
| `ba-notion` | Publish an exact BA markdown artifact into Notion via MCP | None | None | Notion page created or updated from BA source content |

## Workflow

`/ba-start` with no subcommand handles the forward BA lifecycle:

1. Accept raw input (file or text)
2. Parse and normalize into intake form
3. Create or refresh `PROJECT-HOME.md` as the BA-facing dashboard
4. Gap analysis and clarifying questions
5. Scope lock and engagement-mode selection (`lite`, `hybrid`, `formal`)
6. Option pack + comparison when intake needs multiple solution directions before backbone
7. Requirements backbone production
8. Gated FRD and user story generation
9. Selective use case and Screen Contract Plus production when needed
10. Design decision capture and project runtime `DESIGN.md` creation when wireframe support is justified
11. Manual wireframe constraint-pack and handoff-map production from the persisted wireframe input pack, locked IA snapshot, and approved `DESIGN.md`
12. Final screen description production as an enrich pass from the persisted wireframe constraints and optional manual handoff map
13. Unified browser-editable HTML packaging and quality review across the emitted artifacts

`/ba-start reverse` is the as-built lane. It scans committed source files, locks a baseline commit, and builds an evidence-backed reverse index before any canonical BA artifact is updated. Future-state asks do not belong in this lane; route them through `impact` or the normal forward lifecycle. Reverse mode treats wireframes as skipped / not-applicable because it documents the current implemented system rather than proposing UI changes.

## Invocation

```text
/ba-start
/ba-start intake <file>
/ba-start options --slug <slug>
/ba-start options --slug <slug> --select option-02
/ba-start options --slug <slug> --skip
/ba-start backbone --slug <slug>
/ba-start frd --slug <slug> --module <module_slug>
/ba-start stories --slug <slug> --module <module_slug>
/ba-start srs --slug <slug> --module <module_slug>
/ba-start wireframes --slug <slug> --module <module_slug>
/ba-start package --slug <slug>
/ba-start status --slug <slug>
/ba-notion srs --slug <slug> --page <url|id> --mode overwrite
/ba-start reverse --slug <slug> [--focus <area>] [--commit <hash>]
/ba-start reverse status --slug <slug>
/ba-start reverse refresh --slug <slug> [--commit <hash>]
/ba-start reverse promote --slug <slug> --evidence-ids <id,...>
/ba-start reverse impact --slug <slug> [--evidence-ids <id,...>]
```

## Subcommands

| Command | Purpose | Prerequisite |
| --- | --- | --- |
| `intake` | Parse input, normalize intake, save Project Home, and save the work plan | Raw file or pasted text |
| `options` | Generate or review the pre-backbone option pack, comparison, and explicit select/skip decision | Matching intake artifact |
| `backbone` | Build the persisted source-of-truth artifact after scope lock and refresh Project Home | Matching intake artifact |
| `frd` | Produce the FRD and FRD HTML only when the gate is open | Matching backbone artifact |
| `stories` | Produce user stories only | Matching backbone artifact |
| `srs` | Produce grouped SRS artifacts, the persisted wireframe input pack, and merged SRS | Matching backbone and user stories |
| `wireframes` | Re-run Step 9 from the persisted wireframe input pack or exact fallback sources | Wireframe input pack plus an approved or refreshable project `DESIGN.md`, or exact Group B + Group C / merged SRS fallback |
| `package` | Run quality review, validate existing packaged HTML artifacts, and regenerate only the needed packaged outputs | Emitted artifact set and non-missing wireframe state |
| `status` | Print artifact checklist with dates | Resolved slug and dated set |
| `reverse` | Scan committed source files, lock the baseline commit, and build the reverse evidence index | None (creates `00_reverse/` lane) |
| `reverse status` | Print reverse lane progress: baseline lock, index freshness, evidence counts, drift state | `reverse_baseline_lock` |
| `reverse refresh` | Re-scan against a new commit and update drift state | `reverse_baseline_lock` |
| `reverse promote` | Promote validated `as_built_drift` evidence to canonical backbone or SRS | `reverse_baseline_lock`, `reverse_evidence_ledger`, `--evidence-ids` |
| `reverse impact` | Classify evidence entries as `as_built_drift`, `future_state_request`, or `mixed_change` | `reverse_baseline_lock`, `reverse_focus_excerpts` |

Subcommand targeting rules:

- Use `--slug <slug>` first when rerunning an existing project.
- If exactly one slug exists in the modular `plans/{slug}-{date}/` tree, BA-kit may use it automatically.
- If multiple slugs exist, BA-kit should stop and ask the user to choose.
- If one slug has multiple dated artifact sets, BA-kit should stop and ask which dated set to use.

## Agent Delegation

| Agent | Role in Workflow |
| --- | --- |
| `requirements-engineer` | Backbone, FRD, user stories, use cases, Screen Contract Plus, final screen descriptions |
| `ui-ux-designer` | Manual wireframe constraint-pack and handoff-map preparation from use cases, pre-wireframe screen spec, locked IA snapshot, and approved `DESIGN.md` |
| `ba-documentation-manager` | Validation pack, quality review, consistency, packaging |
| `ba-researcher` | Domain research when external context is needed |

Delegation is intentionally partitioned. Large SRS work should be split into grouped slices and passed downstream as narrow handoff packets with exact excerpts and trace IDs, not as full merged artifacts. If one delegated slice becomes too large to keep consistent, repartition and rerun only that slice.

Use [`templates/sub-agent-handoff-template.md`](../templates/sub-agent-handoff-template.md) as the default packet structure when delegation is non-trivial.
For non-trivial delegated work, also create a tracker under `plans/{slug}-{date}/delegation/` so `/ba-start status` can expose `queued`, `running`, `blocked`, `needs-repartition`, `completed`, or likely stalled slices.

## HTML Editing

Packaged HTML artifacts are meant to be edited in the browser. Update copy, swap images, and add or remove blocks directly in the rendered HTML instead of hand-editing source HTML.

If the user manually inserts wireframe images or links into the markdown source, the packaged HTML preserves those references only when the asset path stays inside the allowed base directory. Mermaid diagrams are rendered explicitly after the DOM is ready, and PlantUML diagrams always prefer local rendering. Use `ba-kit install-plantuml` or the renderer's `--auto-install-plantuml` option before falling back to a configured server.

`/ba-start status` reports `PROJECT-HOME.md` first as the BA-facing dashboard, then regular artifacts as exists or missing with last-modified dates, including the persisted backbone. Wireframe handoff is reported as `completed`, `skipped`, `not-applicable`, or `missing` from the explicit wireframe-state marker, and completed runs should expose the project runtime `DESIGN.md` together with the persisted wireframe input pack and wireframe map. Delegated slices should also appear from their trackers, with likely stalled slices flagged when heartbeats go stale.

## Expected Quality Bar

- Outputs reference business goals
- Backbone decisions explain why downstream artifacts were emitted or skipped
- Every requirement has acceptance criteria
- Use cases cover primary and alternate flows
- Screen descriptions use field tables with Display/Behaviour/Validation rules
- Approved `DESIGN.md` decisions are reflected in the wireframe constraint pack and any user-supplied wireframes
- Every SRS requirement, use case, and screen traces to user stories
- Diagrams use PlantUML for swimlanes and Mermaid for the rest
- Risks, assumptions, and open questions are visible
