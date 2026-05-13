---
name: create-workflow-app
description: Build a Workato Workflow App (approval workflows, etc.). The only UI action is enabling the App. Everything else (Data Table, stages, pages, recipes) is generated as JSON and pushed. Japanese prompts are also supported.
---

# $create-workflow-app

Build a Workato Workflow App. The only UI action required is enabling the Workflow App itself; everything else (Data Tables, stages, pages, recipes) is generated as JSON and pushed.

## Usage

- `$create-workflow-app <project>/<NNN>-<slug>` — pull context from `plan.md` and build (**preferred**; how `$implement` invokes it)
- `$create-workflow-app` — build a new Workflow App interactively (fallback when no plan.md)
- `$create-workflow-app <name>` — start with a fixed name (legacy invocation from before spec-driven workflow; DESIGN.md is not consulted)

> **Note**: as part of the migration to the spec-driven workflow, the legacy `DESIGN.md` reference is retired. Start new projects with `$spec`; for existing projects, run `$design migrate` first to convert into `specs/`.

## Background reading

- `docs/platform/workflow-apps.md` — construction patterns, providers, actions
- `docs/patterns/deployment-guide.md` — deployment steps and common errors
- `AGENTS.md` — JSON structure for lcap_app / workato_db_table / lcap_page

## Phase 0: pull context from plan.md

When `<project>/<NNN>-<slug>` is supplied, read `projects/<project>/specs/<NNN>-<slug>/plan.md` and take the following as **defaults**:

| plan.md section | What to pull in |
|---|---|
| `## New Components` `### Data Tables` | Table names, field definitions |
| `## New Components` `### Pages` | Page roles, main components |
| `## Stage Transitions` | Stage transition diagram |
| `## New Components` `### Recipes` | Recipe definitions to generate alongside |
| `## Resource Inventory` | Resource values (choices for external services) |

If plan.md is missing, fall back to the interactive Phase 1.

## Phase 1: design + project creation

### Interview the user

- **App purpose**: what request / approval flow is this?
- **Data Table fields**: what info is stored?
- **Workflow stages**: which approval stages exist (e.g. New → Manager review → Done / Canceled)?
- **How is the approver identified**: fixed user / dynamic from HRMS / specified in the form?
- **External integrations**: what happens after approval (Jira creation, Slack notification, email, etc.)?

### Create the project (CLI)

Create the project via the CLI **before generating files** (avoids the directory-not-empty error):

```bash
workato init --non-interactive --profile default --project-name "[App] <Name>" --folder-name "projects/[App] <Name>"
```

### Enable the Workflow App (the only UI action)

After the project is created, read `folder_id` from `.workatoenv` and share the project URL:

```
Please enable the Workflow App in the Workato UI:

  URL: https://app.trial.workato.com/recipes?fid=<folder_id>

  1. Open the project
  2. Enable "Workflow App" (the app name doesn't matter — push will overwrite it)

Let me know once you're done.
```

> **Note**: the URL domain varies by Workato region (US: www.workato.com, EU: app.eu.workato.com, JP: app.jp.workato.com, Trial: app.trial.workato.com). Check the region with `workato profiles list` and build the right URL.

## Phase 2: generate every component as JSON, then push

File layout follows `AGENTS.md`.

### 1. Data Tables/workato_db_table.json (Data Table schema)

```json
{
  "name": "<table name>",
  "schema": [
    { "id": "11fbe9a6-a16d-4d7e-86ea-afe42ec03005", "title": "Record ID", "type": "short-text", "read_only": true, "hidden": true },
    { "id": "a5612739-5401-4ae7-bd07-782c1a6fb2d1", "title": "Created time", "type": "date-time", "read_only": true, "hidden": true },
    { "id": "61aae604-a95e-4519-9091-bb0bf754a67f", "title": "Last modified time", "type": "date-time", "read_only": true, "hidden": true },
    { "id": "<uuidgen>", "title": "<field name>", "type": "<type>", "read_only": false, "hidden": false, "required": true/false, "metadata": {} }
  ],
  "project_name": "[App] <Name>"
}
```

- The three system field UUIDs are common across every table.
- Generate a fresh UUID with `uuidgen` for each user-defined field.
- `type`: `short-text`, `long-text`, `number`, `boolean`, `date`, `date-time`, `file`, `relation`.

### 2. Pages/lcap_page.json (page definitions)

Generate four pages:

**Submission form** (`Pages/submit_<name>.lcap_page.json`):
- Text: `"type": "input"` + `"style": "short-text"` or `"long-text"`.
- Number: `"type": "input"` + `"style": "number"`.
- Contact: `"type": "input"` + `"style": "email"` / `"phone"` / `"url"` (auto-validated).
- Date: **`"type": "date"`** (`"input"` + `"style": "date"` is broken — it breaks the editor).
- Dropdown: `"type": "dropdown"` + `"options"` for static choices. `"multiValue": true` for multi-select.
- Checkbox: `"type": "checkbox"` → Data Table `boolean`.
- File: `"type": "file"` → Data Table `file`.
- Button component (`handlers.click.type`: `"save-data"` / `"complete-task"` / `"open-url"` / `"run-recipe"` / `"reset-reload"`).
- `dataSource` specifies **the Data Table column to save into**. `dataSource.id` must be the field's **title** (not its UUID). When `dataSource` is `null`, the value is not persisted on submit.

**Component `type` mapping (important)**:
| Field type | `type` | `style` |
|---|---|---|
| short-text | `"input"` | `"short-text"` |
| long-text | `"input"` | `"long-text"` |
| number | `"input"` | `"number"` |
| email | `"input"` | `"email"` |
| phone | `"input"` | `"phone"` |
| url | `"input"` | `"url"` |
| date / date-time | **`"date"`** | not used |
| Single-select dropdown | **`"dropdown"`** | not used |
| Multi-select dropdown | **`"dropdown"`** + `multiValue: true` | not used |
| Checkbox | **`"checkbox"`** | not used |
| File | **`"file"`** | not used |

**Review page** (`Pages/review_<name>.lcap_page.json`):
- Use input / date components with `editable: false` to display the request read-only.
- Only the Review comments field is `editable: true`.

**Approved page** (`Pages/approved_page.lcap_page.json`):
- Read-only display of the request + an "APPROVED" status indicator.
- Display the external integration result (Jira ticket key, etc.).

**Rejected page** (`Pages/rejected_page.lcap_page.json`):
- Read-only display of the request + a "REJECTED" status indicator.
- Display the Review comments.

Page JSON structure:
```json
{
  "name": "Page name",
  "path": "url-slug",
  "content": {
    "type": "common",
    "maxWidth": "fixed",
    "background": { "style": "pattern", "pattern": "light-2" },
    "variables": [],
    "handlers": { "pageLoad": null },
    "layout": [ /* component tree */ ]
  }
}
```

Components: use the lcap_page.json of an existing project as a reference for the layout.
Generate an 8-digit hex `id` for each component.

### 3. lcap_app.json (Workflow App definition + page references)

Update the pulled lcap_app.json to include the Data Table, stages, and page references:

```json
{
  "name": "<App name>",
  "creation_page": { "zip_name": "Pages/submit_<name>.lcap_page.json", "name": "...", "folder": "Pages" },
  "workato_db_table": { "zip_name": "Data Tables/<table>.workato_db_table.json", "name": "...", "folder": "Data Tables" },
  "workflow_stages": [
    { "name": "New", "color": 0 },
    { "name": "<approval stage>", "color": 1,
      "task_page": { "zip_name": "Pages/review_<name>.lcap_page.json", "name": "...", "folder": "Pages" } },
    { "name": "Done", "color": 2,
      "details_page": { "zip_name": "Pages/approved_page.lcap_page.json", "name": "...", "folder": "Pages" } },
    { "name": "Canceled", "color": 3,
      "details_page": { "zip_name": "Pages/rejected_page.lcap_page.json", "name": "...", "folder": "Pages" } }
  ],
  "tabs": [
    { "name": "Workflow requests", "kind": "new_request", "visibility": "all" }
  ],
  "displayed_columns": [
    { "id": "CURRENT_STAGE", "visibility": "all" },
    { "id": "ASSIGNED_TO", "visibility": "all" },
    { "id": "CREATED_BY", "visibility": "all" }
  ]
}
```

### 4. Delegate recipes to `$create-recipe`

The Workflow App's recipes (main recipe, Recipe Functions) are delegated to `$create-recipe`:

- Summarize the main recipe's requirements for the user:
  - Trigger: `workato_workflow_task/new_requests_realtime`
  - Required actions: approval, external integration, stage change
- Call `$create-recipe`, which runs the recipe-generation interview.
- Same goes for Recipe Functions — generate them via `$create-recipe`.

A typical approval workflow:
```
Main recipe:
  trigger → call_recipe(manager lookup) → human_review → if/else → external integration → change_stage

Recipe Function:
  execute → HRMS lookup → return_result
```

## Phase 3: deploy and verify

Follow "Workflow App deployment flow" in `docs/patterns/deployment-guide.md` and walk through the stages:

1. **Push**: `workato push` to push every asset.
2. **Connection auth first** (right after push, before recipe review):
   ```
   Push complete. First, authenticate the connections:
   URL: https://<region>/recipes?fid=<folder_id>

   Open each of the following connections and supply credentials:
   - <connection_name_1> (<provider_1>)
   - <connection_name_2> (<provider_2>)
   ...

   Let me know once authentication is done.
   ```
3. **After auth, guide UI verification**:
   ```
   Next, please verify:
   1. The Workflow App shows the stages and pages
   2. The submission form's fields look right
   3. Open the recipe and verify the field mappings
   ```
4. **Test run**: submit a form → run the full approval flow.
5. **If anything was adjusted**: pull → `$learn-recipe` to learn.

## Output

After each Phase, display:
- The list of generated files.
- The push result.
- **Project URL** (built from `.workatoenv`'s `folder_id` + the region).
- Concrete instructions for what the user should do in the UI (see the deployment guide).

## Git management

Generated files (`*.lcap_app.json`, `Pages/`, `Data Tables/`, `Recipes/`, `Connections/`) live under `projects/<project-name>/`. Commit in the workspace repository:

```bash
git add projects/<project-name>/
git commit -m "Add workflow app: <name>"
git push origin
```
