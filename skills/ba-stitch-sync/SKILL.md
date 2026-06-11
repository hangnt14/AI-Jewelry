---
name: ba-stitch-sync
description: Sync approved BA canon to Stitch MCP for consistent UI screen generation. Requires Stitch MCP installed and configured.
argument-hint: "--module <module_slug> [--slug <slug>] [--date <date>] [--device DESKTOP|MOBILE|TABLET|AGNOSTIC]"
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__stitch__list_projects
  - mcp__stitch__create_project
  - mcp__stitch__list_design_systems
  - mcp__stitch__upload_design_md
  - mcp__stitch__create_design_system_from_design_md
  - mcp__stitch__generate_screen_from_text
  - mcp__stitch__get_screen
  - mcp__stitch__get_project
---

# BA Stitch Sync

Downstream visual-consumer command. Reads approved SRS canon + DESIGN.md, bootstraps a Stitch design system, and generates consistent UI screens via Stitch MCP.

## Invocation

```text
/ba-stitch-sync --module auth-flow
/ba-stitch-sync --slug warehouse-rfp --module payment --device MOBILE
/ba-do đồng bộ Stitch cho module auth-flow
/ba-do tạo UI từ SRS module payment
```

## Required Read Order

1. Read `core/contract.yaml`.
2. Read `core/contract-behavior.md`.
3. Read `core/behavior/stitch-sync.md`.
4. Resolve slug, date, module, and `--device` flag per `contract.yaml` resolution rules.

## General Error Handling Rules

**ID Validation Rule (applies to ALL MCP calls):**
After every MCP call that returns an ID (screen ID, asset ID, project ID):
1. Check the value is a non-empty string.
2. Check it is not an error object (no `error` or `code` field at top level).
3. Check it is not a hallucinated placeholder (not "id", "undefined", "null", "TODO", "xxx").
4. If ANY check fails → follow the per-step BLOCK/WARN/retry rule below.
5. Print the ID to user immediately so they can verify.
6. Write ID to disk immediately (not batch at end) to survive mid-phase crashes.

**Recovery Hierarchy:**

| Severity | Action | Example |
|----------|--------|---------|
| **BLOCK** | Stop entire command. Print error + fix instructions. | Asset ID missing, all screens failed, quota exceeded |
| **WARN + skip** | Log warning, skip this item, continue. | Single screen generation failed |
| **Retry** | Retry once after 10s. If still fails → escalate to WARN. | Timeout on upload_design_md |

---

## Phase 0 — Preflight

### Step 0.1: Parse arguments

- Extract `--slug`, `--date`, `--module` from ARGUMENTS.
- Extract `--device` flag: DESKTOP (default) | MOBILE | TABLET | AGNOSTIC.
- Resolve slug/date/module per contract.yaml resolution rules.

### Step 0.2: Read contract

- Read `core/contract.yaml`.
- Read `core/contract-behavior.md`.
- Read `core/behavior/stitch-sync.md`.

### Step 0.3: MCP Connectivity Gate

- Call `mcp__stitch__list_projects()`.
- If tool unavailable or error:
  - Print Stitch MCP setup instructions (API key, .mcp.json config, restart Claude Code).
  - **BLOCK** — do not proceed.
- If success: continue.

### Step 0.3a: Resolve Stitch project

- From `list_projects()` output, find project matching slug or prompt user to select.
- If no matching project exists, create one via `mcp__stitch__create_project(name=<slug>)`.
- Extract `projectId` for all subsequent MCP calls.

### Step 0.4: BA Prerequisite Gate

- Check `paths.design_doc` exists.
- Check `paths.srs_compile_receipt` exists and fresh.
- Check `paths.ascii_screen_index` exists.
- Check `paths.shared_shell_contract` exists.
- Any fail → **BLOCK** + recommend correct `ba-start` command.

---

## Phase 1 — Design System Bootstrap

### Step 1.1: Check existing design system

- Call `mcp__stitch__list_design_systems(projectId)`.
- **VALIDATE:** Check response is an array (not null, not error object).
  If response is not iterable → WARN "Unexpected response from list_design_systems" + treat as no existing DS.
- If existing DS found:
  - Show: "Design system already exists (created {date}). Reuse / Refresh / Abort?"
  - **Refresh: Full regeneration.** Destroy old design system, regenerate ALL screens.
    Existing stitch-screen-map.json is invalidated. User warned about re-generation cost.
  - Abort: exit.
- If no existing DS: continue.

### Step 1.2: Read DESIGN.md

- Read full `paths.design_doc`.
- **VALIDATE:** Content is non-empty string. If empty → **BLOCK** "DESIGN.md is empty. Cannot create design system."
- Compute content hash (SHA-256 or similar) for change detection.

### Step 1.3: Upload DESIGN.md

- Base64-encode DESIGN.md content.
- Call `mcp__stitch__upload_design_md(projectId, designMdBase64)`.
- **VALIDATE response:**
  - Response must be an object (not null, not error string).
  - Extract `selectedScreenInstance`: must have `id` (non-empty string) and `sourceScreen` (non-empty string).
  - If `id` is missing/empty → **BLOCK** "upload_design_md returned no screen instance ID. Cannot proceed."
  - If `sourceScreen` is missing/empty → **BLOCK** "upload_design_md returned no source screen reference. Cannot proceed."
- Log: `upload_design_md OK — screen instance: {id}`.

### Step 1.4: Create design system

- Call `mcp__stitch__create_design_system_from_design_md(projectId, selectedScreenInstance)`.
- **VALIDATE response:**
  - Wait for completion — this call can take minutes. DO NOT retry on timeout.
  - If timeout → poll `get_project(projectId)` every 30s for up to 10 attempts to check if DS was created.
  - Extract asset ID from response. Must be non-empty string matching `assets/` or numeric pattern.
  - If asset ID is null/empty/undefined after polling → **BLOCK** "Failed to create design system. DESIGN.md was uploaded but design system creation did not complete. Check Stitch project manually."
- **ID VALIDATION GATE — HARD BLOCK:**
  - The asset ID extracted here is CRITICAL. Every subsequent screen depends on it.
  - Write it to `paths.stitch_design_system_id` IMMEDIATELY (before Phase 2).
  - Re-read the file to confirm the write succeeded and the ID is not truncated.
  - If the file write fails or the ID is malformed → **BLOCK** "Cannot persist design system ID."

### Step 1.5: Verify design system exists (sanity check)

- Call `mcp__stitch__list_design_systems(projectId)` again.
- **VALIDATE:** The asset ID from Step 1.4 MUST appear in the list.
  - If NOT found → **BLOCK** "Design system was created (asset ID: {id}) but not found in list_design_systems. Possible Stitch sync delay or ID mismatch. Retry Phase 1 or check Stitch manually."

---

## Phase 2 — Screen Generation

### Step 2.1: Load design system ID

- Read `paths.stitch_design_system_id`.
- **VALIDATE:** `asset_id` field exists, is non-empty string.
  - If missing or empty → **BLOCK** "Design system ID not found. Run Phase 1 bootstrap first."
  - If file doesn't exist → **BLOCK** "stitch-design-system-id.json not found. Run Phase 1 first."
- **CRITICAL:** This ID is used in EVERY screen generation call. Wrong ID = all screens broken.
  Print the ID to user so they can verify: "Using design system: {asset_id}"

### Step 2.2: Build BA-kit ID Reference Index

Before reading any screen file, build a lookup index from shared_shell_contract:
- Read `paths.shared_shell_contract`.
- Extract ALL valid IDs into a structured index:
  ```
  portals: { "PORTAL-APP": { display_name, layout_direction, shell_variant, description }, ... }
  nav_schemas: {
    "NAV-APP-01": {
      portal_id,
      menu_items: [{ label, target, icon_hint?, order }],
      active_rule,
      layout_hint
    },
    ...
  }
  actors: { "ACT-01": {...}, "ACT-02": {...} }  (if defined)
  ```
- **CRITICAL:** The `menu_items` list in each nav_schema is the single source of truth for what navigation items appear. Extract every field — label, target, icon_hint, order. This list will be injected verbatim into every screen generation prompt to ensure navigation consistency.
- **VALIDATE:** Each nav_schema must reference a portal_id that EXISTS in `portals`.
  - If nav_schema references unknown portal → **BLOCK** "shared_shell_contract: NAV-xx references unknown portal PORTAL-xx. Fix shared_shell_contract first."
- Also read `paths.design_doc` — extract Portal Summary and Navigation Schema tables.
  - From Portal Summary: extract portal_id, display_name, layout direction (sidebar|topbar|mixed), shell variant.
  - From Navigation Schema: extract nav_schema_id, menu item list, active/highlight rule.
  - **Chrome & branding (CRITICAL for anti-hallucination):** extract project-level branding elements if present:
    - `app_name`: the application display name (e.g., "WMS Pro")
    - `logo`: logo description or "NO LOGO" / "TEXT ONLY" directive
    - `user_area`: user avatar/name display area description (e.g., "top-right avatar + user name dropdown"), or "NONE"
    - `footer`: footer content or "NONE"
    - `global_header`: any global header content outside the nav, or "NONE"
  - If DESIGN.md does NOT define these → mark each as "UNSPECIFIED" (will trigger anti-hallucination rule in prompt).
- **CROSS-CHECK:** Portal IDs and Nav Schema IDs in DESIGN.md MUST match shared_shell_contract exactly.
  - If DESIGN.md has PORTAL-X but shared_shell_contract has PORTAL-Y → **BLOCK** "DESIGN.md and shared_shell_contract disagree on portals. Align them first."
  - If DESIGN.md has NAV-xx but shared_shell_contract doesn't → **BLOCK** "DESIGN.md defines NAV-xx but shared_shell_contract has no matching schema."
- Print the resolved index: "Resolved {N} portals, {M} nav schemas ({menu_count} total menu items)."

### Step 2.3: Read screen index

- Read `paths.ascii_screen_index`.
- **VALIDATE:** Index is parsable, contains at least 1 screen entry.
  - If empty → WARN "No screens found in ascii_screen_index. Nothing to generate." + skip Phase 2.
- Filter: skip screens with `stitch_sync_eligible: false`.

### Step 2.4: Cross-Reference Validation Gate (MANDATORY — before ANY screen generation)

For each eligible screen, read the canon file and extract IDs. Validate ALL of them against the reference index BEFORE calling any MCP tool:

1. **Screen ID (`id` or `screen_id`):**
   - Must be non-empty.
   - Must follow expected pattern (e.g., `SCR-NN`).
   - If missing → **BLOCK** "Screen file {path}: missing screen ID. Add it before generating."
   - If malformed (e.g., `SCR-`, `SCREEN01`, no prefix) → WARN "Unusual screen ID format: {id}" + continue.

2. **Portal ID (`portal_id`):**
   - Must be non-empty.
   - Must exist in the reference index `portals` built in Step 2.2.
   - If NOT found → **BLOCK** "Screen {id}: portal_id '{portal_id}' not found in shared_shell_contract. Valid portals: {list}. Fix screen file."
   - If screen file doesn't declare portal_id → **BLOCK** "Screen {id}: missing portal_id. Every screen must declare which portal it belongs to."

3. **Nav Schema ID (`nav_schema_id`):**
   - Must be non-empty.
   - Must exist in the reference index `nav_schemas`.
   - Must belong to the same portal declared in `portal_id` (cross-check: nav_schema.portal_id == screen.portal_id).
   - If NOT found → **BLOCK** "Screen {id}: nav_schema_id '{nav_schema_id}' not found. Valid schemas: {list}."
   - If schema belongs to different portal → **BLOCK** "Screen {id}: nav_schema_id '{nav_schema_id}' belongs to portal '{actual_portal}', but screen declares portal '{screen_portal}'. Mismatch."

4. **Expected Active Menu Item:**
   - If declared, must match an item in the nav schema's `menu_item_list`.
   - If NOT found → WARN "Screen {id}: active_menu '{item}' not in nav schema '{nav_schema_id}' menu list: {valid_items}. Active highlight may be wrong."

5. **Overlay Context (`overlay_context.parent_screen`):**
   - If screen is modal/dialog/drawer/overlay, `parent_screen` must reference an existing screen ID in the index.
   - If parent NOT found → **BLOCK** "Screen {id}: overlay parent '{parent}' not found in screen index. Parent screen must exist."

6. **Cross-screen Portal consistency:**
   - All screens in the same portal MUST use the same nav_schema_id (unless an explicit exception is documented).
   - Group screens by portal_id. Check nav_schema_id is uniform per portal group.
   - If mismatch → WARN "Portal {portal_id}: screens use different nav schemas: {list}. This may cause navigation inconsistency. Explicit exception documented?"

7. **Duplicate Screen IDs:**
   - Check no two screen canon files declare the same screen ID.
   - If found → **BLOCK** "Duplicate screen ID '{id}' in files: {file1}, {file2}. Screen IDs must be unique."

**Gate outcome:**
- Print validation summary: "{N} screens checked, {W} warnings, {E} errors."
- If E > 0 → **BLOCK** entire Phase 2. "Fix {E} cross-reference errors above before generating screens."
- If W > 0 → show warnings, ask user "Continue with {W} warnings? (Y/n)". Default Y.
- If 0 errors + 0 warnings → proceed to generation.

### Step 2.5: Prompt Building Rules — Plain Text Only (NO IDs, NO keys)

Stitch MCP's `generate_screen_from_text` is stateless. Each call is an isolated AI generation. It has NO knowledge of BA-kit IDs, contract keys, or the project's shared shell. **Every piece of information the model needs must be in the prompt as full natural language text.**

**HARD RULES:**

1. **NO IDs in prompt.** Do NOT pass `portal_id`, `nav_schema_id`, `screen_id`, or any BA-kit internal key to Stitch. These strings are opaque garbage to the generation model.
   - WRONG: "Portal: PORTAL-APP, Nav Schema: NAV-APP-01"
   - RIGHT: "This screen belongs to the Admin Portal — a left-sidebar layout with 5 navigation items."

2. **Resolve all IDs to their display text.** For every ID in the reference index, substitute the human-readable text:
   - `portal_id` → portal `display_name` + `description` in natural language
   - `nav_schema_id` → describe the navigation structure in prose, then list every menu item with its visible label
   - `active_menu` → "The '{menu_label}' menu item must be visually highlighted/active on this screen"
   - `layout_direction` → "The navigation appears as a vertical sidebar on the left" or "The navigation is a horizontal top bar"
   - `shell_variant` → describe the chrome layout in words

3. **Menu items as full sentences, not keys.** List each navigation item with its exact display label, position, and what it navigates to:
   ```
   The navigation menu contains these items, in this order:
   1. "Tổng quan" — links to the dashboard overview page
   2. "Quản lý kho" — links to warehouse management
   3. "Báo cáo" — links to reports
   4. "Cài đặt" — links to settings
   ```

4. **Consistency directive must be in plain text.** Do not reference nav_schema_id. Instead: "Every screen in this portal must show the exact same navigation menu with the exact same items in the same order. Do not add, remove, rename, or reorder any menu item."

5. **Cross-screen anchoring uses display names, not IDs.** "Previous screens already generated with this navigation: 'Trang tổng quan', 'Danh sách kho hàng'. Your navigation must match theirs exactly."

6. **Use the screen's human-readable name**, not its SCR-xx ID, when describing what this screen is.

### Step 2.6: Generate each screen (sequential)

For each eligible screen:
1. Read ascii-screen canon file.
2. Extract: name, portal_id, nav_schema_id, field table, state coverage, ASCII wireframe.
3. **VALIDATE extracted data:**
   - `name` must be non-empty.
   - `portal_id` must match a known portal from shared_shell_contract.
   - `nav_schema_id` must match a known schema.
   - If any missing → WARN "Screen {file}: missing {field}. Generation may be inconsistent." + continue.
4. **CRITICAL — Do NOT pass extracted IDs directly to the prompt.** The IDs from Step 2 (`portal_id`, `nav_schema_id`) are internal BA-kit keys. Stitch does not know what "PORTAL-APP" or "NAV-APP-01" means. You MUST look each one up in the Step 2.2 reference index and substitute the full text:

   **Mechanical lookup process (do this for EVERY screen):**

   ```
   Step A: Read screen file → extract: name="Danh sách kho hàng", portal_id="PORTAL-APP", nav_schema_id="NAV-APP-01"

   Step B: Look up portal_id in reference index:
           portals["PORTAL-APP"] → {
             display_name: "Ứng dụng quản lý kho",
             description: "Portal chính cho nhân viên quản lý hàng hóa, nhập/xuất kho, kiểm kê.",
             layout_direction: "vertical sidebar on the left",
             shell_variant: "fixed sidebar + scrollable content area"
           }

   Step C: Look up nav_schema_id in reference index:
           nav_schemas["NAV-APP-01"] → {
             menu_items: [
               { label: "Tổng quan", target: "dashboard", icon_hint: "home icon", order: 1 },
               { label: "Quản lý kho", target: "warehouse", icon_hint: "package icon", order: 2 },
               { label: "Nhập hàng", target: "import", icon_hint: "arrow-down icon", order: 3 },
               { label: "Xuất hàng", target: "export", icon_hint: "arrow-up icon", order: 4 },
               { label: "Báo cáo", target: "reports", icon_hint: "chart icon", order: 5 }
             ],
             layout_hint: "vertical sidebar, items stacked top-to-bottom"
           }

   Step D: Look up active_menu for this screen (validated in Step 2.4.4):
           → "Quản lý kho"

   Step E: NOW build the prompt using ONLY the resolved text from Steps B, C, D.
           ZERO IDs from Step A appear in the final prompt.
   ```

5. Build prompt in plain natural language, using ONLY the resolved text from Step 4 lookup. Follow Step 2.5 rules strictly — NO IDs, NO keys:

   **Prompt structure (all sections required):**

   a. **Portal description:**
      "You are generating a screen for the 'Ứng dụng quản lý kho' portal. Portal chính cho nhân viên quản lý hàng hóa, nhập/xuất kho, kiểm kê."

   b. **Layout description:**
      "The layout uses a vertical sidebar on the left — fixed sidebar + scrollable content area."

   c. **Navigation menu (verbatim list — MOST CRITICAL):**
      "The navigation menu has 5 items, displayed as a vertical sidebar stacked top-to-bottom. They must appear on every screen in this portal exactly as follows:
      1. 'Tổng quan' — home icon
      2. 'Quản lý kho' — package icon
      3. 'Nhập hàng' — arrow-down icon
      4. 'Xuất hàng' — arrow-up icon
      5. 'Báo cáo' — chart icon"

   d. **Active menu state:**
      "On THIS screen, the menu item 'Quản lý kho' must be visually highlighted as the active/selected item."

   e. **Screen identity:**
      "This screen is 'Danh sách kho hàng'. Hiển thị danh sách tất cả kho hàng trong hệ thống dưới dạng bảng có phân trang."
      Then summarize key fields, behaviours, and states from the canon file.

   f. **Wireframe layout (DETAILED — mirror ASCII positions exactly):**
      The ASCII wireframe defines exact element positions. Translate it into a structured text description Stitch can follow. Do NOT summarize or skip elements.

      Translation rules:
      - **Read order:** top-to-bottom, left-to-right. Describe elements in the order they appear.
      - **Copy the ASCII wireframe itself into the prompt** as a visual reference block. Stitch can interpret ASCII art.
      - **For each visible element**, state: what it is (button/input/dropdown/table/label/link), its label text, its approximate position (top-left, center, right side, below X, etc.), and its purpose.
      - **Group related elements:** fields in a form → "A form with 4 input fields arranged vertically: ..."
      - **Describe layout zones:** "The screen is divided into: (1) a top search bar, (2) a data table filling the main area, (3) a bottom pagination bar, (4) a 'Tạo mới' button above the table on the right."
      - **State transitions:** if the screen has multiple states (empty, error, loading), describe what differs in each state.
      - **Exact labels:** use the EXACT field labels from the ASCII wireframe. Same wording, same capitalization.
      - **Exact placeholder data (CRITICAL — prevents Stitch from inventing numbers):** all numbers, counts, percentages, and text values visible in the ASCII wireframe are exact placeholder values. Copy them verbatim and add the directive: "Use these exact values as shown. Do NOT invent different numbers, different counts, or different text." If the wireframe says "3 Presale, 5 Won", the generated screen must show exactly "3" and "5" — not "12" and "28".
      - **Zone coverage — empty zones MUST be declared (CRITICAL — prevents Stitch from filling gaps):** after describing every element in the wireframe, enumerate ALL shell zones and declare each one's status:
        1. **Topbar zone** (above content, below nav): list what appears here. If nothing appears → "The topbar is INTENTIONALLY EMPTY except for the page title. Do NOT add a search bar, notification bell, help icon, settings gear, or any other controls to the topbar."
        2. **Sidebar header** (top of sidebar): list what appears. If only nav menu → "The sidebar header is INTENTIONALLY EMPTY. Do NOT add a logo, brand name, or product title."
        3. **Sidebar footer** (bottom of sidebar): list what appears. If nothing → "The sidebar footer is INTENTIONALLY EMPTY. Do NOT add a user avatar, user name, profile link, or logout button."
        4. **Filter bar** (below page header, above main content): list every filter. If no filters in wireframe → "There is NO filter bar. Do NOT add any filter dropdowns or search inputs."
        5. **Main content area**: describe what fills it. Any sub-zone not occupied → "This area is INTENTIONALLY EMPTY."
        6. **Footer**: if wireframe shows no footer → "There is NO footer. Do NOT add a footer line, copyright text, or version number."
        Any zone not explicitly declared → treat as a coverage gap and add an explicit ban before generation.

      Example for a list screen:
      ```
      ASCII wireframe reference:
      ┌─────────────────────────────────────────────┐
      │  [Tạo kho mới]              [Tìm kiếm...]   │
      ├─────────────────────────────────────────────┤
      │  Mã kho  │ Tên kho   │ Địa chỉ    │ Hành động│
      ├──────────┼───────────┼────────────┼─────────│
      │  K-001   │ Kho A     │ 123 ABC    │ [Sửa]   │
      │  K-002   │ Kho B     │ 456 DEF    │ [Sửa]   │
      ├─────────────────────────────────────────────┤
      │  ← Trước   Trang 1/5   Sau →               │
      └─────────────────────────────────────────────┘

      Layout zones, top to bottom:
      1. Top toolbar: "[Tạo kho mới]" button on the left, "[Tìm kiếm...]" search input on the right
      2. Data table: 4 columns — "Mã kho", "Tên kho", "Địa chỉ", "Hành động". Each row has a "[Sửa]" action button in the last column.
      3. Bottom pagination: "← Trước" link, "Trang 1/5" text, "Sau →" link. Centered.

      Zone coverage:
      - Topbar: ONLY page title. NO search bar, NO notification bell, NO help icon.
      - Sidebar header: INTENTIONALLY EMPTY. NO logo, NO product name.
      - Sidebar footer: INTENTIONALLY EMPTY. NO user avatar, NO profile section.
      - Filter bar: the search input in the top toolbar serves as the only filter. NO separate filter bar with extra dropdowns.
      - Footer: NO footer.
      ```

   f2. **Field Table priority over wireframe for widget structure (CRITICAL):**
      The Field Table in the screen canon defines the widget TYPE (table, cards, form, dropdown, etc.). The ASCII wireframe defines approximate LAYOUT POSITIONS. When they conflict on structure → **Field Table wins.**

      Resolution rule:
      - If Field Table says "Project list | table" with columns listed → render a TABLE with those exact columns, placed where the wireframe shows the list zone.
      - If Field Table says "Kanban board | cards" → render CARDS, regardless of wireframe simplification.
      - If Field Table says a widget is a "dropdown" → render a dropdown, not a radio group or toggle.
      - The wireframe's visual arrangement (bullet points, boxes, dashes) is a layout hint — not the final widget type.
      - When Field Table and wireframe agree on widget type → use both for exact positioning.
      - When Field Table specifies structure but wireframe omits it → add the widget at the wireframe's corresponding zone position.

      In the prompt, state the widget type explicitly using Field Table terms: "The project list is a TABLE with columns: Mã dự án, Tên dự án, Khách hàng, % hoàn thành." Do NOT say "a list of projects" if the Field Table says "table".

   g. **Branding & chrome elements (from DESIGN.md — resolve "UNSPECIFIED" to explicit bans):**
      These are shell-level elements that stay the same across all screens. They are NOT part of individual screen wireframes — they come from the shared_shell_contract and DESIGN.md.

      Resolve each chrome field from the Step 2.2 index. If the field is "UNSPECIFIED" → explicitly ban it:
      - `app_name`: if set → "The application name '{app_name}' must appear in the {position}." If UNSPECIFIED → "NO application name or brand title in the header. Leave it blank."
      - `logo`: if set → "Include logo: {logo_description}." If UNSPECIFIED → "NO logo. Do not invent a logo or icon."
      - `user_area`: if set → "Show user area: {user_area_description}." If UNSPECIFIED → "NO user avatar, user name, or profile area. Do not invent user identity elements."
      - `footer`: if set → "Show footer: {footer_content}." If UNSPECIFIED → "NO footer. Do not add a footer line."
      - `global_header`: if set → include it. If UNSPECIFIED → "NO extra header content beyond the navigation sidebar/topbar."

   h. **Anti-hallucination directive with per-zone negative space (CRITICAL — prevents Stitch from inventing):**
      Generic "do not add" directives are insufficient — Stitch's model fills perceived gaps. Every zone must carry an explicit ban list.

      **Global bans (apply to entire screen):**
      "Do NOT add any UI element that is not explicitly described in the wireframe or field table above. Every button, field, label, and link on this screen must correspond to something listed. If it's not listed, it doesn't exist."

      **Per-zone ban lists (inserted directly into each zone description — NOT separate):**
      After describing what IS in each zone, append the zone-specific ban. These MUST appear inline in the zone description, not as a separate bullet list at the end:

      | Zone | Ban directive (append to zone description) |
      |------|---------------------------------------------|
      | Topbar | "NO search bar, NO notification bell, NO help icon, NO settings gear, NO user menu. Only the elements listed above appear in the topbar." |
      | Sidebar header | "NO logo, NO product name, NO brand icon. Only the navigation menu items listed above appear in the sidebar." |
      | Sidebar footer | "NO user avatar, NO user name, NO profile link, NO logout button, NO role label. This area is empty." |
      | Content header | "NO breadcrumbs unless the wireframe explicitly shows them. NO tabs unless the wireframe shows them." |
      | Filter bar | "ONLY the filter controls listed above. NO additional filter dropdowns, NO 'advanced filter' button, NO search input unless specified." |
      | Main content | "ONLY the widgets listed in the Field Table. NO empty-state illustrations, NO onboarding tooltips, NO 'no data' graphics unless the screen is in Empty state." |
      | Footer | "NO footer line, NO copyright text, NO version number, NO links. The page ends at the bottom of the main content area." |

      **Common Stitch invention patterns to explicitly ban (include in every prompt):**
      - Do NOT invent a brand/product name (like "ProjectFlow", "AppName", etc.) — use the portal display name or leave blank.
      - Do NOT invent user identity elements (avatar photo, user name, role title, "Business Analyst" label).
      - Do NOT invent notification UI (bell icon, badge count, notification dropdown).
      - Do NOT invent help/support UI (help icon, "?" button, chat widget).
      - Do NOT add extra menu items beyond the {N} listed above.
      - Do NOT translate labels from one language to another — use exact wording from the wireframe.
      - Do NOT change numeric values — use exact numbers from the wireframe.

   i. **Consistency directive:**
      "CRITICAL: Every screen in the 'Ứng dụng quản lý kho' portal must have the exact same navigation menu — same items, same order, same labels. Do NOT add, remove, rename, or reorder any menu item. The navigation must be pixel-identical across all screens in this portal."

   j. **Cross-screen anchor (if applicable):**
      If other screens in this portal were already generated: "The following screens were already generated with this exact navigation and must be matched: 'Trang tổng quan'."

5a. **PROMPT SANITIZER GATE (HARD — before EVERY MCP call):**

   Before calling `generate_screen_from_text`, scan the assembled prompt for leaked BA-kit IDs. This gate catches AI instruction-skipping, partial lookups, and copy-paste errors.

   **Check 1 — Banned ID patterns:**
   Scan the prompt for any string matching these BA-kit ID prefixes. If found → **BLOCK this screen**, record the matched string, skip to next screen:
   - `PORTAL-`, `NAV-`, `SCR-`, `UC-`, `FR-`, `NFR-`, `BR-`, `MSG-`, `CR-`, `BO-`, `CAP-`, `E-`, `AC-`
   - Also: `portal_id`, `nav_schema_id`, `screen_id` (raw field names)
   - Also: any string matching `{...}` placeholder not yet substituted

   **Check 2 — Empty resolved values:**
   Verify every resolved field from Step 4 lookup is non-empty:
   - `portal_display_name` is not empty/null
   - `portal_description` is not empty/null
   - `menu_items` list is not empty
   - Every `label` in menu_items is a non-empty string
   - `active_menu_label` is not empty/null
   - `layout_direction_description` is not empty/null

   **Check 3 — Menu item count matches:**
   The number of menu items in the prompt must equal the number in `nav_schemas[{nav_schema_id}].menu_items` from the reference index. If count differs → **BLOCK** "Menu item count mismatch: index has {N}, prompt has {M}. Prompt may have truncated or invented items."

   **Check 4 — Chrome fields NOT left as "UNSPECIFIED":**
   Scan the prompt for the literal string "UNSPECIFIED". If found → the AI failed to resolve a chrome/branding field from Step 2.2 into an explicit description or ban. **BLOCK this screen** "PROMPT CHROME LEAK: 'UNSPECIFIED' found in prompt. Chrome field not resolved. Check Step 2.2 chrome extraction."

   **Check 5 — Zone coverage completeness:**
   Verify every shell zone is declared in the prompt (see Step 2.6.4f zone list). Scan for these zone markers:
   - "topbar" or "top bar" or "header" — must appear at least once
   - "sidebar header" — must appear at least once
   - "sidebar footer" — must appear at least once
   - "filter" — must appear at least once (either describing filters or explicitly banning them)
   - "footer" — must appear at least once (either describing footer or explicitly "NO footer")
   - For each zone, check it is followed by either a description of content OR an explicit "INTENTIONALLY EMPTY" / "NO ..." ban within 2 sentences.
   If any zone is missing entirely from the prompt → WARN "ZONE COVERAGE GAP: '{zone_name}' not declared in prompt. Stitch may invent content for this zone. Skipping screen {name}." → mark screen as `failed`, continue to next screen.

   **Gate outcome:**
   - **PASS** → print "Prompt gate OK: {N} IDs resolved, 0 leaked, {Z} zones covered." → proceed to Step 6.
   - **FAIL Check 1** → WARN "PROMPT LEAK: found banned pattern '{matched}' in prompt. Skipping screen {name}. Fix Step 4 lookup." → mark screen as `failed`, continue to next screen.
   - **FAIL Check 2** → WARN "PROMPT INCOMPLETE: empty value for '{field}'. Index lookup may have returned nothing. Skipping screen {name}." → mark screen as `failed`, continue.
   - **FAIL Check 3** → WARN "PROMPT MENU COUNT WRONG: index={N} prompt={M}. Skipping screen {name}." → mark screen as `failed`, continue.
   - **FAIL Check 4** → WARN "PROMPT CHROME LEAK: 'UNSPECIFIED' found in prompt. Skipping screen {name}." → mark screen as `failed`, continue.
   - **FAIL Check 5** → WARN "ZONE COVERAGE GAP: '{zone_name}' not declared in prompt. Skipping screen {name}." → mark screen as `failed`, continue.

   **If ALL screens fail the gate** → **BLOCK** entire Phase 2. "All screens failed prompt sanitizer gate. The reference index or lookup process is broken. Fix Step 2.2 and Step 2.6 Step 4 before retrying."

6. Call `mcp__stitch__generate_screen_from_text(projectId, prompt, deviceType=<resolved_device>, designSystem=<assetId>)`.
7. **VALIDATE response:**
   - Response must contain a screen ID (non-empty string).
   - If screen ID is null/empty/undefined → mark screen as `failed`, record error "generate_screen_from_text returned no screen ID", continue to next screen.
   - If timeout (no response after 5 minutes) → mark as `failed`, record "timeout", continue.
   - If error code `RATE_LIMITED` → **BLOCK** entire Phase 2. "Stitch daily quota exceeded. {N} screens remaining. Retry after midnight UTC."
8. **ID VALIDATION — POST-WRITE:**
   - Record in in-memory map FIRST: `{ba_screen_id: {stitch_screen_id, generated_at, status: "ok"|"failed", error: "..."}}`.
   - Write `paths.stitch_screen_map` AFTER EACH screen (not batch at end) — prevents data loss on mid-phase failure.
   - Re-read the file to confirm write succeeded.
9. Print progress: "[{N}/{total}] {screen_name} → {stitch_screen_id} ✓" or "✗ {error}"

### Step 2.7: Post-generation sanity check

- Count screens in `paths.stitch_screen_map`.
- **VALIDATE:** Count matches number of eligible screens.
  - If fewer → WARN "{N} screens failed to generate. See stitch-sync-report.md for details."
- **VALIDATE:** At least 1 screen succeeded.
  - If 0 screens succeeded → **BLOCK** "All screen generations failed. Check Stitch quota and project state. No reports written."
- Check for duplicate stitch_screen_ids (same ID for different BA screens):
  - If found → WARN "Duplicate stitch_screen_id detected: {id}. Possible AI hallucination or Stitch bug. Mark affected screens for re-generation."

---

## Phase 3 — Validation

### Step 3.1: Load generated screens

- Read `paths.stitch_screen_map`.
- **VALIDATE:** File exists and contains valid JSON.
  - If file missing → **BLOCK** "No screen map found. Phase 2 may not have run or failed completely."
- Filter to screens with `status: "ok"`.
  - If 0 OK screens → WARN "No successfully generated screens to validate." + skip validation.

### Step 3.2: Cross-screen consistency check

- For each generated screen, get screenshot via `mcp__stitch__get_screen(name, projectId)`.
- **VALIDATE each get_screen call:**
  - If call fails or returns no image data → mark screen as `validation: "skipped"`, record reason.
  - If timeout → skip screen, continue.
- Compare across screens: navbar region, logo placement, primary CTA color, font usage.
- Flag any drift with severity: `high` (different color), `medium` (spacing shift), `low` (minor).

### Step 3.3: Write reports

- Write `paths.stitch_sync_report`:
  - Generated: N screens (list with stitch IDs)
  - Skipped: M screens (with reasons)
  - Failed: K screens (with errors)
  - Validated: V screens (with consistency score)
  - Design system asset ID
- Write `paths.stitch_mismatch_report` (if drift detected):
  - Which screens drifted
  - What drifted (color, layout, typography)
  - Severity
  - Recommendation (re-run specific screen / adjust DESIGN.md / accept)

---

## Write Scope

Allowed repo writes:

- `plans/{slug}-{date}/05_tool-lanes/stitch/stitch-design-system-id.json`
- `plans/{slug}-{date}/05_tool-lanes/stitch/stitch-screen-map.json`
- `plans/{slug}-{date}/05_tool-lanes/stitch/stitch-sync-report.md`
- `plans/{slug}-{date}/05_tool-lanes/stitch/stitch-mismatch-report.md`

Forbidden repo writes:

- `srs.md`, `srs/spec.md`, `srs/flows.md`, `srs/states.md`, `srs/erd.md`
- `ascii-screen/*.md`
- `usecases/*.md`
- `userstories/*.md`
- `frd.md`
- `DESIGN.md`
- `shared-shell-contract.md`
- `backbone.md`
- Any canon BA artifact

## Stop Conditions

- Stitch MCP unavailable → **BLOCK** with setup instructions
- Missing or stale `srs-compile-receipt.json`
- Missing `ascii-screen/index.md`
- Missing `DESIGN.md`
- Missing `shared-shell-contract.md`
- Design system creation fails
- All screen generations fail
- RATE_LIMITED error from Stitch MCP
- Cross-reference validation errors (>0)

## Output

After the run, report:
- resolved project/module
- design system asset ID (or reused)
- screens attempted, succeeded, failed, skipped
- device type used
- consistency check results
- report paths written
