# Workflow Apps

Official: https://docs.workato.com/en/workflow-apps.html

## Overview

A no-code visual development platform. Lets you build interactive applications that combine user actions with automation steps.

## Key components

### Data storage
- Stores records (invoices, requests, etc.) in integrated Data Tables
- Supports multiple linked tables
- Accessed from recipes via the Workflow Apps connector
- Recipes can be used as real-time data sources

### User interface
- Auto-generated portal (request list, navigation)
- **Pages**: build custom forms and dashboards with a drag-and-drop editor
- Conditional logic, validation, form pre-fill
- Public forms (for external users)

### Business logic
- Workflow recipes manage routing, approvals, data updates, and system integrations
- The New request trigger handles form submissions
- Task assignment and workflow stage transitions

## Runtime flow

```
UI event (form submission, etc.)
  -> Recipe triggers
  -> Fetch/update external data
  -> Return results to UI components
```

Approval workflow:
```
Form submission -> New request trigger -> Create record in Data Table
  -> Evaluate business logic -> Assign task -> Approve/Reject
```

## Common use cases

- Department management (HR, Finance, IT)
- Exception handling for automated processes
- Request routing and approvals
- Custom applications / front ends

## Providers and actions used in recipes

### `workato_workflow_task` provider

Triggers and actions dedicated to Workflow Apps.

**Triggers:**
- `new_requests_realtime` — Real-time trigger fired when a new request is submitted. Specify the target Workflow App via `input.app_id`
- `app_function_generic_request` — Generic app function trigger (for button actions, etc.). Define parameters via `parameters_schema_json`
- `app_function_load_table_request` — Data loading for table widgets. Define columns via `table_schema_json`
- `app_function_load_dropdown_request` — Option loading for dropdowns

**Actions:**
- `human_review_on_existing_record` — Assign a task and wait for approval/rejection (blocking)
- `change_workflow_stage` — Change the workflow stage (e.g. New -> In progress -> Done)
- `update_request` — Update fields on a request record
- `app_function_return` — Return app function results to the UI (`rows` for tables, `items` for dropdowns)
- `complete_task` — Complete a task programmatically (used from external triggers such as a Slack button)

### `complete_task` fields

| Field | Type | Description |
|---|---|---|
| `app_id` | reference | Reference to the Workflow App's lcap_app.json |
| `record_id` | datapill | The request's Record ID |
| `status` | string | `"Approved"` or `"Rejected"` |

`complete_task` completes a task that is waiting in `human_review_on_existing_record` from the outside. Use it when reflecting approve/reject results from a Slack button click etc. back into the Workflow App.

### `workato_db_table` provider

Direct CRUD operations against Data Tables.

- `get_records` — Fetch records (supports filtering, sorting, pagination)
- `update_record` — Update a record

### `workato_recipe_function` provider

- `call_recipe` — Call another recipe as a function. Use it as a wrapper for fetching external data (HRMS, etc.)

### Detailed input list for `workato_workflow_task`

**Trigger details:**

| Action name | Key inputs |
|---|---|
| `new_requests_realtime` | `app_id` |
| `app_function_generic_request` | `parameters_schema_json` |
| `app_function_load_table_request` | `table_schema_json`, `parameters_schema_json` |
| `app_function_load_dropdown_request` | `search_enabled` |

**Action details:**

| Action name | Key inputs |
|---|---|
| `human_review_on_existing_record` | `app_id`, `record_id`, `name`, `email`, `workflow_stage_id`, `page_id` |
| `change_workflow_stage` | `project_id` (lcap_app reference), `record_id`, `workflow_stage_id` |
| `update_request` | `app_id`, `record_id`, `parameters` |
| `app_function_return` | `rows` (for tables) or `items` (for dropdowns) |

### Detailed structure of `human_review_on_existing_record`

```json
{
  "provider": "workato_workflow_task",
  "name": "human_review_on_existing_record",
  "keyword": "action",
  "dynamicPickListSelection": {
    "user_group_id": "Group name (optional)",
    "workflow_stage_id": "In progress"
  },
  "toggleCfg": {
    "send_email_notification": true,
    "reassignable": true,
    "workflow_stage_id": true,
    "due_in_days": true
  },
  "input": {
    "app_id": { "zip_name": "...", "name": "App Name", "folder": "" },
    "record_id": "#{_dp('...')}",
    "name": "Task name (datapill allowed)",
    "email": "#{_dp('...created_by.email...')}",
    "workflow_stage_id": { "name": "In progress" },
    "due_in_days": "14",
    "send_email_notification": "true",
    "reassignable": "true",
    "page_id": { "zip_name": "Pages/page.lcap_page.json", "name": "Page Name", "folder": "Pages" }
  }
}
```

Output: a `task` object (`is_approved` boolean, `assigned_user`, `assigned_group`, `expires_at`, `link`) and a `record` object.

### Details of the `workato_db_table` provider

| Action name | Purpose | Key inputs |
|---|---|---|
| `add_record` | Create a record in a Data Table | `table_id`, `parameters` |
| `get_records` | Fetch records from a Data Table | `table_id`, `limit`, `order_direction`, `filters` |
| `update_record` | Update a record in a Data Table | `table_id`, `record_id`, `parameters` |

#### Notes on `add_record`

- The action name is `add_record` (not `create_record`)
- Field keys under `parameters` are **underscore-separated** UUIDs (not hyphenated)
  ```json
  "parameters": {
    "b1a2c3d4_e5f6_4a7b_8c9d_100000000001": "value"
  }
  ```
- `parameters` for `update_request` also uses **underscore-separated** keys (not hyphenated)
- **All UUID keys inside any `parameters` field must be underscore-separated**
- All Data Table fields are expanded as schema inside `parameters` under `extended_input_schema`

#### Filter structure for `get_records`

```json
"filters": [
  {
    "field_id": "UUID-with-hyphens",
    "op_id": "eq",
    "value_default": "#{_dp('...')}"
  }
]
```

### Detailed structure of `workato_recipe_function`

```json
{
  "provider": "workato_recipe_function",
  "name": "call_recipe",
  "keyword": "action",
  "dynamicPickListSelection": { "flow_id": "Recipe name" },
  "input": {
    "flow_id": "Numeric ID (as a string)",
    "parameters": { "ParamName": "value or datapill" }
  }
}
```

- The callee recipe's return value is stored under the `result` output object
- If `skip: true` is set, that step is skipped (used for placeholders)

### Special Workflow App field types

- `custom_type: "relation"` — Relation to another table. Has `record_id` and `display_name`
- `custom_type: "file"` — File field. Has `filename` and `file_content`
- `created_by` — Shared creator object (`id`, `name`, `email`, `status`, `user_groups[]`, `is_guest`)
- `stage` — Workflow stage (`id`, `name`)
- `task` — Active task (`id`, `name`, `status`, `assigned_user`, `assigned_group`, `expires_at`, `link`)

### Internal type declarations inside `extended_input_schema` (Data Table)

For `get_records` on a Data Table, column type declarations are stored as hidden fields inside `extended_input_schema`:
```json
{
  "label": "$internal_value_<uuid-with-hyphens>",
  "name": "<uuid-with-hyphens>",
  "default": "string|date|date_time|id",
  "ngIf": "false",
  "optional": true,
  "type": "string"
}
```

## Referencing Data Tables from recipes

When referencing a Data Table from within a recipe, use a zip reference for `table_id`:
```json
"table_id": {
  "zip_name": "employees.workato_db_table.json",
  "name": "Employees",
  "folder": ""
}
```

Data Table columns are identified by UUIDs. Within the recipe JSON:
- **Input field names**: hyphen-separated (`11fbe9a6-a16d-4d7e-86ea-afe42ec03005`)
- **Output / datapill paths**: underscore-separated (`11fbe9a6_a16d_4d7e_86ea_afe42ec03005`)

Reserved columns common to all tables:
- `11fbe9a6-...` = Record ID
- `a5612739-...` = Created at
- `61aae604-...` = Updated at

## Typical recipe flows

### Approval workflow
```
new_requests_realtime -> call_recipe (fetch external data) -> update_request
  -> human_review_on_existing_record -> if/else -> change_workflow_stage
```

### Loading data for a table widget
```
app_function_load_table_request -> get_records -> app_function_return(rows)
```

### Loading data for a dropdown
```
app_function_load_dropdown_request -> get_records -> app_function_return(items)
```

### Input structure for `app_function_return`

**Table widget (`rows`):**
```json
{
  "rows": {
    "____source": "#{_dp('...records...')}",
    "ColumnName": "#{_dp('...records.current_item.uuid_field...')}"
  }
}
```

**Dropdown (`items`):**
```json
{
  "items": {
    "____source": "#{_dp('...records...')}",
    "value": "#{_dp('...record_id_field...')}",
    "label": "#{_dp('...display_field...')}"
  }
}
```

### Data update app function pattern
```
app_function_generic_request trigger (receives parameters)
  -> workato_db_table.get_records (find target record by filter)
  -> if (record exists)
      -> workato_db_table.update_record
```

## Workflow App construction patterns

### Build flow

Only enabling the Workflow App itself requires a UI action. Everything else can be defined in JSON and pushed.

```
1. Enable the Workflow App inside the project from the Workato UI (one-time only)
2. Define all components in JSON -> push
   - workato_db_table.json (Data Table schema)
   - lcap_app.json (stages, page references, displayed columns)
   - lcap_page.json (page definitions: form, review, approve/reject)
   - recipe.json (workflow recipes)
   - connection.json (external service connection)
3. Repeat the pull -> adjust -> push cycle
```

### What can be defined in JSON vs. what requires the UI

| Element | Definable in JSON | UI required |
|---|---|---|
| Enabling the Workflow App | No | Yes, once via UI |
| Workflow stages | Yes, `workflow_stages` in `lcap_app.json` | |
| Data Table schema | Yes, `workato_db_table.json` | |
| Displayed columns | Yes, `displayed_columns` in `lcap_app.json` | |
| Tabs | Yes, `tabs` in `lcap_app.json` | |
| Pages (forms, review screens, etc.) | Yes, `lcap_page.json` | |
| Page linkage | Yes, `creation_page`, `task_page`, `details_page` | |
| Recipes | Yes, `.recipe.json` | |
| Connections | Yes, `.connection.json` (authentication via UI) | |

### JSON structure of a page

A page (`lcap_page.json`) can be defined in JSON and pushed. Use existing project pages as references to lay out the page.

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
    "layout": [ /* Nested component tree */ ]
  }
}
```

#### Common properties

Common to all components:
- `type` — Component kind
- `id` — Unique 8-digit hex ID
- `name` — Component name
- `x`, `width` — Grid position (12-column layout)
- `visible` — Visibility control (`true` / conditional expression)

Common to data-input components:
- `dataSource` — **Save destination for the Data Table column**. Set `dataSource.id` to the **title** of the Data Table field (not its UUID). If `null`, the value is not saved on submission
- `editable` — Editability (`true` / `false` / conditional expression)
- `validations.required.condition` — Required input (`true` / `false` / conditional expression)
- `label`, `hint`, `placeholder` — Display text

#### Conditional properties

Official: https://docs.workato.com/features/conditions.html (Conditional control of page components)

The following three properties can be controlled dynamically with conditional expressions:

| Property | Choices | Applicable components |
|---|---|---|
| **Visible** | Always show / Conditional | Almost all components |
| **Editable** | Yes / No / Conditional | Input fields, dropdown, checkbox, table |
| **Required** | Yes / No / Conditional | Input fields, dropdown, checkbox |

- Conditions use the same syntax as recipe IF conditions (AND / OR chaining supported)
- Through the **Page data modal** you can reference these as conditions:
  - App user info (user, role)
  - Request metadata (stage, etc.)
  - Values of other page components
  - Workflow stage
- Typical usage: "Show/edit only when a specific user is at a specific workflow stage"
- Recommended: configure the condition in the UI first, then pull and inspect the JSON (no JSON-form documentation exists)

#### Data-input components

**Mapping of component `type` to field type** (important):

| Purpose | Component `type` | `style` | Data Table field type |
|---|---|---|---|
| Short text | `"input"` | `"short-text"` | `short-text` |
| Long text | `"input"` | `"long-text"` | `long-text` |
| Number | `"input"` | `"number"` | `number` |
| Email | `"input"` | `"email"` | `short-text` |
| Phone | `"input"` | `"phone"` | `short-text` |
| URL | `"input"` | `"url"` | `short-text` |
| Date | **`"date"`** | not needed | `date` |
| Date and time | **`"date"`** | `"date-time"` | `date-time` |
| Selection (single) | **`"dropdown"`** | not needed | `short-text` |
| Selection (multi) | **`"dropdown"`** + `"multiValue": true` | not needed | `short-text` |
| Checkbox | **`"checkbox"`** | not needed | `boolean` |
| File | **`"file"`** | not needed | `file` |

> **Caution**: Using `"type": "input"` + `"style": "date"` for a date breaks the page editor (infinite loading).

**`input` component** — text, number, contact inputs:
- `style`: `"short-text"`, `"long-text"`, `"number"`, `"email"`, `"phone"`, `"url"`
- Contact styles (email, phone, url) include automatic validation
- short-text supports regex validation; number supports min/max

**`dropdown` component** — selection input:
```json
{
  "type": "dropdown",
  "id": "abca2e40",
  "name": "PC type",
  "dataSource": { "id": "PC type", "type": "short-text" },
  "editable": true,
  "appFunctionOptions": null,
  "options": [
    { "title": "Windows", "value": "Windows" },
    { "title": "Mac", "value": "Mac" }
  ],
  "dataSourceOptions": null,
  "labelDataSource": null,
  "multiValue": false
}
```
- `options`: static option list (`title` is displayed, `value` is saved)
- `dataSource`: destination column for the selected value (Data Table column). **Always set this**
- `appFunctionOptions`: use this when the recipe returns options dynamically (the `app_function_load_dropdown_request` trigger)
- `dataSourceOptions`: use this when another Data Table column is the source of options
- `multiValue`: `true` for multi-select (up to 20). For multi-select, the data source must be manual or recipe-only
- The Data Table field type can stay `short-text`

**`file` component** — file upload/download:
- Upload: file type restriction, max size (default 10MB, up to 500MB)
- Download: displayed from a Data Table file column
- Public forms include a malware scan

#### Display components

- `container` — Layout container (`backgroundColor`, `borderColor`, `padding`: large/medium/small/none)
- `text` — Text display (Markdown supported: headings, bold, italic, links, lists)
- `image` — Image (preset `"illustration-N"` / upload / URL)
- `divider` — Divider line (color via `backgroundColor`)

#### Data table components

- **Data Table** — Display and edit columns of the app's main data table. Only for apps with approval/request features
- **Linked Data Tables / View** — Display and edit linked tables. Supports filters, column reordering, and add/remove control

#### Visual components

- **Chart** — Data visualization (table, bar, line, pie, KPI). **Dashboard pages only** (cannot be used on approval/submission/blank pages)

#### Action components

- `button` — Button. `style`: `"filled"` (primary) / `"outline"` (secondary)
  - Action kinds via `handlers.click.type`:
    - `"save-data"` — Save data to a Data Table (submission form)
    - `"complete-task"` — Complete a task (approve/reject)
    - `"open-url"` — Open a URL
    - `"run-recipe"` — Run a recipe
    - `"reset-reload"` — Reset/reload components

#### Form pre-fill via URL parameters

Official: https://docs.workato.com/en/workflow-apps/prefill-forms.html

Append `?prefilled_values=<URL-encoded JSON>` to the form URL to set default values.

**JSON structure:**
```json
{
  "Component Title": {
    "value": "Value",
    "disabled": false
  }
}
```
- Keys use the component's **Title** (the builder-facing name), not the user-facing Label
- `disabled`: `true` (default) for read-only, `false` for editable
- Maximum URL length: 8,000 characters

**Supported components and value formats:**

| Component | Value type | Example |
|---|---|---|
| Text (short/long) | string | `"value": "Peter"` |
| Number (integer) | number | `"value": 10` |
| Number (decimal) | number | `"value": 0.2` |
| Date | string `"YYYY-MM-DD"` | `"value": "2024-07-26"` |
| Date and Time | string `"YYYY-MM-DD HH:MM"` | `"value": "2024-07-25 16:00"` |
| Checkbox | boolean | `"value": true` |
| Dropdown (manual) | string | `"value": "Sales"` |
| Dropdown (table) | object | `"value": {"record_id": "uuid", "value": "123"}` |
| Description | string | `"value": "Description"` |

### Handling page references

If you push page files together with `lcap_app.json`, page references resolve correctly.

```json
{
  "creation_page": {
    "zip_name": "submit_form.lcap_page.json",
    "name": "Submit form",
    "folder": ""
  },
  "workflow_stages": [
    { "name": "Manager review", "color": 1,
      "task_page": { "zip_name": "review.lcap_page.json", "name": "Review", "folder": "" }
    }
  ]
}
```

### Required file set

A typical approval workflow app:

```
projects/[App] <Name>/
├── <name>.lcap_app.json                    # Workflow App definition
├── <name>.lcap_app.png                     # App icon (auto-generated)
├── <table_name>.workato_db_table.json      # Data Table schema
├── <main_recipe>.recipe.json               # Main recipe (approval flow)
├── fnc_<helper>.recipe.json                # Recipe Function (e.g., fetch manager)
├── <connection>.connection.json            # External service connection
├── <page>.lcap_page.json + .zip            # Page definition (create via UI then pull)
└── <query>.insights_query.json             # Analytics query (create via UI then pull)
```

### Recipe template for an approval workflow

```
[0] trigger: new_requests_realtime (app_id -> lcap_app)
  [1] action: call_recipe (fetch manager from HRMS)
  [2] action: human_review_on_existing_record
        - email: result.manager_email from call_recipe (dynamic)
        - record_id: trigger's request.Record_ID (always sourced from the trigger)
  [3] if: task.is_approved == true
    [4] action: external system integration (raise Jira, post to Slack, etc.)
    [5] action: update_request (persist the result to the record)
    [6] action: change_workflow_stage -> Done
  [7] else:
    [8] action: change_workflow_stage -> Canceled
```

### `.lcap_app.json` — Workflow App definition (detailed)

```json
{
  "name": "App name",
  "creation_page": {
    "zip_name": "submit_form.lcap_page.json",
    "name": "Submit form",
    "folder": ""
  },
  "workato_db_table": {
    "zip_name": "table_name.workato_db_table.json",
    "name": "Table Name",
    "folder": ""
  },
  "workflow_stages": [
    { "name": "New", "color": 0 },
    {
      "name": "In progress", "color": 1,
      "task_page": { "zip_name": "...", "name": "...", "folder": "" },
      "details_page": { "zip_name": "...", "name": "...", "folder": "" }
    },
    { "name": "Done", "color": 2, "details_page": { "..." } },
    { "name": "Canceled", "color": 3, "details_page": { "..." } }
  ],
  "tabs": [
    { "name": "Tab name", "kind": "new_request", "visibility": "all" },
    { "name": "Analytics", "kind": "user_defined", "visibility": "managers",
      "page": { "zip_name": "analytics.lcap_page.json", "name": "...", "folder": "" } }
  ],
  "displayed_columns": [
    { "id": "UUID or CURRENT_STAGE|CURRENT_TASK|ASSIGNED_TO|EXPIRES_AT|CREATED_BY", "visibility": "all|managers|nobody" }
  ]
}
```

- `creation_page`: reference to the lcap_page used as the submission form
- `workato_db_table`: reference to the backing Data Table
- `workflow_stages`: list of stages. Each stage can have a `task_page` (task screen) and `details_page` (details screen)
- `tabs`: app tabs. `kind` is `new_request` (default) or `user_defined` (custom page)
- `displayed_columns`: columns shown in the table view. UUIDs are Data Table field IDs; uppercase tokens are system columns
- `color`: stage color codes (0=New, 1=In progress, 2=Done/completion family, 3=Canceled, 8=intermediate stage)

### `.workato_db_table.json` — Data Table schema (detailed)

```json
{
  "name": "Table name",
  "schema": [
    {
      "id": "UUID",
      "title": "Field name",
      "type": "short-text|long-text|number|boolean|date|date-time|file|relation",
      "read_only": false,
      "hidden": false,
      "required": false,
      "default_value": "Default value (optional)",
      "hint": "Input hint (optional)",
      "metadata": {},
      "relation": {
        "table_id": { "zip_name": "other.workato_db_table.json", "name": "Other Table", "folder": "" },
        "field_id": "UUID"
      }
    }
  ],
  "project_name": "[App] Project Name"
}
```

- System fields (Record ID, Created time, Last modified time) are `read_only: true, hidden: true`
- For `type: "relation"`, reference the foreign table and field via the `relation` object
- Field IDs are UUID v4. In recipe output and on pages, UUIDs are used as column names
- `project_name`: name of the project this table belongs to

### `.insights_query.json` — Insights query definition

```json
{
  "page_id": { "zip_name": "page.lcap_page.json", "name": "Page Name", "folder": "" },
  "name": "Query name",
  "index": 0,
  "version": "v1",
  "query": {
    "relation": "Aggregate",
    "groupKey": [],
    "aggCalls": [
      { "qualifier": "16-digit hex", "function": "COUNT", "operand": null }
    ],
    "input": {
      "relation": "TableScan",
      "catalog": "lcap",
      "schema": "public",
      "table": "__ref__1",
      "columnQualifiers": [
        { "column": "workflow_stage|UUID|assignee|creator|...", "qualifier": "16-digit hex" }
      ]
    }
  },
  "references": {
    "__ref__1": {
      "type": "lcap_app",
      "id": { "zip_name": "app.lcap_app.json", "name": "App Name", "folder": "" }
    }
  }
}
```

- `page_id`: reference to the lcap_page where this query is displayed
- `references.__ref__N`: reference to the lcap_app the query targets (table scan source)
- `column` in `columnQualifiers` uses a UUID (Data Table field ID) or a system column name
- `function` in `aggCalls`: aggregate functions such as `COUNT`, `SUM`, `AVG`

### Notes on the push/pull cycle

- JSON you push gets transformed on the Workato side (`extended_output_schema` is expanded, `dynamicPickListSelection` is added, `version` is incremented)
- It is normal for `pull` to return files different from what you pushed
- Pushing `creation_page: null` and then creating the page in the UI and pulling auto-populates the reference
