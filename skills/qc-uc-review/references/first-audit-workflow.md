## First Audit Workflow

1. **Ingest & Understand** — read all provided artefacts, understand the feature
2. **Audit** — score completeness across all required knowledge areas
3. **Report** — deliver a structured readiness report with verdict, score, gaps, and suggestions

## Phase 1 — Ingest & Understand

### Step 1: Read all artefacts

**Reading order:**
1. Common Rules (CMR) — foundation for detecting conflicts
2. Use Case document in full
3. Wireframe / Design Mockup (if available)
4. API Specification (if available) — only to understand client-side context

Input-type routing:
| Input Type | Action |
| :--- | :--- |
| URL | Invoke `.claude/skills/document-extraction/SKILL.md` |
| PDF | Invoke `.claude/skills/pdf/SKILL.md` |
| DOCX | Invoke `.claude/skills/docx/SKILL.md` |
| File path | Read directly |
| Image | Use Read tool — describe all UI elements, labels, states |
| Pasted text | Analyze directly |

DO NOT score any knowledge area before finishing all documents.

### Step 2: Synthesise a Feature Understanding

After reading all documents (including design images), synthesize into 5 sections with **fixed headings**:

---

## 1. UI Object Inventory & Mapping

Build table of all UI components from Wireframe, mapped to UC:

| # | Component Name | Type | In UC? | In Wireframe? | Notes |
|---|---|---|---|---|---|
| 1 | Example Button | Button | ✅ | ✅ | |

Per component check: display state? action rule? label consistent?

**CMR Cross-Check:**
- UC does not mention applicable CMR → ⚠️ Partial + question
- Conflict UC vs CMR → 🔴 Conflict + High-priority question

Sub-categories: Data Display (grid/list/table), Controls (filters/search), Navigation (buttons), Others.

---

## 2. Object Attributes & Behavior Definition

- System States: default state per object (Enabled/Disabled/Hidden/Read-only) based on permissions, data conditions
- Interaction Matrix: actions + system responses
- Object Behavior: reactive rules when data/state changes

**Edge Case Checklist** — see platform profile for platform-specific groups. If UC does not mention an item → record gap + question.

> Edge cases only check behavior within the platform boundary. Do NOT deduct points for gaps found here (bonus coverage).

---

## 3. Functional Logic & Workflow Decomposition

Per function (view list, filter, search, create, edit, delete, etc.):

```
[Function Name]
MAIN FLOW: Step 1 → Step 2 → ... → Expected Result
ALTERNATIVE FLOWS: [Alt-1] Condition → Flow → Result
EXCEPTION FLOWS: [Err-1] Error → Displayed message → Behavior
BUSINESS RULES: BR-xxx: [Rule]
UI/UX FEEDBACK: Loading / Toast / Error message
```

Per input/display field:
| Field | Data Type | Required? | Min | Max | Format |
|---|---|---|---|---|---|
Missing info → record as gap.

---

## 4. Functional Integration Analysis

- Impact Analysis: state/data change in one function → affects others?
- Data Consistency: data sync across related UI components after execution

---

## 5. Acceptance Criteria Synthesis

Categorize AC into: Interface (UI), Function, Integration.

---

## Preliminary Gaps Found

Record preliminary missing/conflicting points found in Phase 1 — do not score yet.

---

## Phase 2 — Audit & Phase 3 — Report

→ **Apply the full scoring process, verdict, breakdown, conflict check, blocked protocol, and report format from [`scoring-rubric.md`](scoring-rubric.md).**
