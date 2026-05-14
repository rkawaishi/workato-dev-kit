# Workflow App build guide

Steps and design points for building Workato Workflow Apps (approval workflows, etc.) in JSON. The same skills and steps work in both Claude Code and Cursor.

## What is a Workflow App

A Workflow App is a Workato feature for building form-based business applications. It is used for approval workflows, request forms, task management, and so on.

**Components:**

```
<project>/
├── lcap_app.json           # App definition (stage ↔ page bindings)
├── Data Tables/
│   └── <table>.data_table.json   # Data schema
├── Pages/
│   ├── submit.page.json    # Request form
│   ├── review.page.json    # Review screen
│   └── done.page.json      # Completion screen
└── Recipes/
    └── *.recipe.json        # Workflow logic
```

## Build steps

### 1. Design

Solidify the overall design with `/spec` → `/plan`. For Workflow Apps, make the following clear in `plan.md`:

- **Stages**: what state transitions exist (e.g. submitted → review → approved/rejected)
- **Data**: data fields needed at each stage
- **Pages**: the screens shown at each stage
- **Recipes**: logic that runs on stage transitions

### 2. Asset generation

```
/create-workflow-app
```

Interactively generates the following:

#### Data Table (`*.data_table.json`)

Define the data schema. System fields are added automatically:

| Field | Type | Description |
|---|---|---|
| `id` | integer | Auto-numbered |
| `created_at` | date_time | Creation timestamp |
| `updated_at` | date_time | Update timestamp |
| `stage` | string | Current stage |
| `created_by` | object | Creator info |

In addition to these, define business-specific fields.

#### Pages (`*.page.json`)

Define the screen for each stage. Main components:

- **Form** — input form (text, dropdown, date, etc.)
- **Table** — list display of data
- **Detail** — detail display
- **Button** — action button (approve, reject, etc.)

For details on page components, see `.claude/rules/workato-page-components.md` (Cursor: `.cursor/rules/workato-page-components.mdc`).

#### App definition (`lcap_app.json`)

Define stage transitions and bind pages to stages:

```json
{
  "stages": [
    { "name": "submitted", "page": "submit.page.json" },
    { "name": "in_review", "page": "review.page.json" },
    { "name": "approved", "page": "done.page.json" }
  ]
}
```

#### Recipes

Delegate to `/create-recipe` to generate logic for stage transitions (sending notifications, updating external systems, etc.).

### 3. Deploy

```
Step 1: Workato UI → Settings → Workflow Apps → Enable
  (Only on the first time. This is the only UI operation.)

Step 2: /push-project
  → Auto-pushes in the order Data Table → lcap_app → Pages → Recipes

Step 3: Verify behavior in the UI
  → Test form input → stage transition → notification
```

## Design points

### Stage design

- Define stage names in **English snake_case** (UI display names can be set separately)
- When there are branches (approve/reject), make each its own stage
- For "send back" cases, define a transition back to the original stage

### Data Table design

- **Do not over-normalize**: data in a Workflow App is self-contained, so one table is the default
- **Hold external IDs**: when integrating with external systems, include the external system's ID as a field
- **Stage history**: include fields that record the approver and approval timestamp

### Page design

- **One page per stage** is the default
- Bind a form's `dataSource` to columns in the Data Table
- Clearly separate read-only fields from editable fields
- Define stage transitions in a button's `action`

## Known limitations

- Enabling a Workflow App can only be done in the UI (not supported by CLI/API)
- Deleting Workflow App assets via `/push-project --delete` can break the app. Delete from the UI
- Some page components (custom CSS, etc.) can only be configured in the UI. After push, fine-tune in the UI and retrieve via pull
