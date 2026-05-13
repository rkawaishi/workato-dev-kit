---
name: catalog
description: Scan the organization's shared assets (Recipe Functions, connections) and catalog them. Referenced by `/create-recipe` and `/plan`. Japanese prompts are also supported.
---

# /catalog

Scans assets in the **shared projects** under the organization's `projects/` and generates / updates a catalog file.
Other skills (`/create-recipe`, `/plan`) consult the catalog to propose reusing existing assets.

**Important**: do not scan private-scope projects. Respect departmental visibility controls.

## Usage

- `/catalog` — display the catalog
- `/catalog scan` — scan shared projects and regenerate the catalog
- `/catalog config` — view / edit scope settings
- `/catalog add <file-path>` — manually add an asset to the catalog

## File layout

```
projects/
├── CATALOG.md              ← shared asset catalog (auto-generated)
├── CATALOG_CONFIG.yaml     ← per-project scope definitions
├── Shared/                 ← scope: global
├── Finance - Common/       ← scope: team:finance
├── [App] IT Onboarding/    ← scope: private (excluded from catalog)
└── [App] Expense Report/   ← scope: private
```

All of these should be protected via `.workatoignore`.

## Project scopes

### CATALOG_CONFIG.yaml

Define the visibility of each project:

```yaml
# projects/CATALOG_CONFIG.yaml
projects:
  Shared:
    scope: global          # public to all teams; included in the catalog
    description: Org-wide shared logic and connections

  "Finance - Common":
    scope: team:finance    # shared within the Finance team; included in the catalog
    description: Common recipes for the Finance team

  "[App] IT Onboarding":
    scope: private         # excluded from the catalog
    description: IT onboarding for new hires

# Projects not listed here are treated as private
```

### Scope types

| Scope | Catalog inclusion | Use case |
|---|---|---|
| `global` | Every asset is listed | Shared across the org (e.g. the Shared project) |
| `team:<name>` | Every asset is listed (with team name) | Shared within a department (e.g. Finance - Common) |
| `private` | **Not listed** | Project-specific (e.g. a Workflow App) |

### Initial setup

`/catalog config` walks you through this interactively:

1. Show the project list under `projects/`.
2. Confirm the scope of each project with the user.
3. Generate `CATALOG_CONFIG.yaml`.
4. Add `CATALOG_CONFIG.yaml` and `CATALOG.md` to `.workatoignore`.

## Catalog structure

```markdown
# Shared Asset Catalog
Last updated: <YYYY-MM-DD>

## Connections

| Name | Provider | Project | Scope |
|---|---|---|---|
| Shared \| Slack | slack_bot | Shared | global |
| Shared \| Jira | jira | Shared | global |
| Finance \| SAP | sap | Finance - Common | team:finance |

## Recipe Functions

### fnc: Get line manager
- **Project**: Shared (global)
- **File**: `Shared/Recipes/fnc_get_line_manager.recipe.json`
- **Input**: `employee_email` (string) — the employee's email address
- **Output**: `manager_name` (string), `manager_email` (string)
- **Purpose**: look up manager info from HRMS / Google Sheets

## MCP Servers

| Name | Project | Scope | Tools |
|---|---|---|---|
| IT Onboarding | Shared | global | 1 |
```

## `/catalog scan` — procedure

### 1. Load scope settings

Read `projects/CATALOG_CONFIG.yaml`. If it's missing, point the user to `/catalog config`.

### 2. Filter target projects

Only scan projects whose `scope` is `global` or `team:*`.
Skip `private` projects and projects not listed in the config.

### 3. Collect connections

Scan `*.connection.json` in the target projects.
Extract `name` and `provider` from each file.

### 4. Collect Recipe Functions

Scan recipes whose name starts with `fnc_*.recipe.json` or `fnc: *`.
From each file, extract:

- `name` — recipe name
- `code.input.parameters_schema_json` — input parameter schema (parse the JSON string)
- `code.input.result_schema_json` — output schema (parse the JSON string)
- The recipe's `comment` — purpose description

For each parameter field, extract `name`, `type`, `label`, `optional` and list them in the catalog.

### 5. Collect Workflow Apps / MCP servers

Scan `*.lcap_app.json` and `*.mcp_server.json` in the target projects.

### 6. Generate the catalog file

Write the collected info to `projects/CATALOG.md`.
If an existing catalog is present, do a diff update (preserve manually-added descriptions like `Purpose`).

## How other skills consume this

### From `/create-recipe`

When `/create-recipe` is generating a recipe:

1. Check whether `projects/CATALOG.md` exists.
2. If so, load it and search for **shared** assets that match the requirements:
   - Connections: is there a shared connection for the same provider?
   - Recipe Functions: does the logic already exist?
3. If matches are found, propose them:
   ```
   Existing shared assets are available:
   - fnc: Get line manager (Shared / global) — manager lookup
   - Shared | Slack (slack_bot / global) — Slack connection

   Use these?
   ```
4. On user approval, generate a recipe that references the shared assets via `call_recipe` or `config`.

### From `/plan`

In the technical-design phase of `/plan <project>/<NNN>-<slug>`:

1. Load the catalog.
2. From the user experience in spec.md, identify the required capabilities.
3. List the parts covered by shared assets in `plan.md`'s `## Reused Assets`.
4. Plan the remainder under `## New Components` for new development.

## Proposing consolidation

When you detect duplicate logic across private projects (during `/learn-recipe` or `/plan`):
- Do not expose the specific code content.
- Suggest: "the same logic appears in multiple projects; consider extracting it into a shared Recipe Function."
- The user decides whether to consolidate.
- If they do, place it in a `global` / `team` shared project and register it in the catalog.
