---
paths:
  - "**/*.agentic_genie.json"
  - "**/*.agentic_skill.json"
  - "**/*.mcp_server.json"
  - "**/*.lcap_app.json"
  - "**/*.workato_db_table.json"
---

# Workato Agentic JSON Format

## Genie (AI agent): *.agentic_genie.json

```json
{
  "name": "Genie name",
  "logo_file_name": "logo.png",
  "logo_content_type": "image/png",
  "description": "Short description of the Genie",
  "instructions": "System prompt (Markdown)",
  "ai_provider": "anthropic",
  "ai_model": null,
  "matrix": false,
  "mcp_servers": [],
  "references": {
    "ref_0": {
      "type": "agentic_skill",
      "id": {
        "zip_name": "skill_name.agentic_skill.json",
        "name": "Skill display name",
        "folder": ""
      }
    }
  }
}
```

### Field details

| Field | Description |
|---|---|
| `instructions` | The Genie's system prompt. Describe its role, target users, behavior, and prohibitions. |
| `ai_provider` | `"anthropic"` / `"openai"` / etc. |
| `ai_model` | `null` for the default, or a specific model name. |
| `matrix` | Matrix mode (run multiple skills in parallel). |
| `mcp_servers` | List of MCP servers to connect to. |
| `references` | Use `ref_0`, `ref_1`, ... to reference the skills this Genie uses. |

### Best practices for `instructions`

Structure the Genie's prompt under these sections:
- **What's my job?** — primary responsibilities
- **Who will need my help?** — target users
- **How do I get things done?** — behavior patterns
- **What should I avoid?** — prohibitions
- **What results do you want me to track?** — metrics to follow
- **How should I talk to people?** — communication style
- **Any extra tips?** — anything else

## Agentic Skill: *.agentic_skill.json

```json
{
  "name": "Skill name",
  "trigger_description": "When to use this skill\n\nSpecific trigger conditions",
  "references": {
    "recipe_id": {
      "type": "recipe",
      "id": {
        "zip_name": "skill_recipe.recipe.json",
        "name": "Recipe name",
        "folder": ""
      }
    }
  }
}
```

### Relationship between skills and recipes

```
agentic_genie.json
  └── references → agentic_skill.json (multiple allowed)
                      └── references.recipe_id → recipe.json
```

- A Genie can have multiple skills.
- Each skill is tied to exactly one recipe.
- A skill's recipe uses the `workato_genie` provider with the `start_workflow` trigger.
- The final step of a skill's recipe is `workflow_return_result`, which sends the result back to the Genie.

## Connection: *.connection.json

```json
{
  "name": "Connection name (e.g. Sample1 | Gmail)",
  "provider": "provider_name",
  "root_folder": false
}
```

No credentials — only the name and provider.

## File naming conventions

- Recipe: `<snake_case_name>.recipe.json`
- Connection: `<prefix>_<provider>.connection.json`
- Genie: `<snake_case_name>.agentic_genie.json`
- Skill: `<snake_case_name>.agentic_skill.json`
- Logo: `<genie_name>.agentic_genie.png`
- MCP server: `<name>.mcp_server.json`
- Workflow App: `<snake_case_name>.lcap_app.json`
- Data Table: `<snake_case_name>.workato_db_table.json`
- Workflow App page: `<snake_case_name>.lcap_page.json` / `.lcap_page.zip`
- Insights query: `<snake_case_name>.insights_query.json`

## Workflow App: *.lcap_app.json

```json
{
  "name": "App name",
  "creation_page": { "zip_name": "form.lcap_page.json", "name": "Form", "folder": "" },
  "workato_db_table": { "zip_name": "table.workato_db_table.json", "name": "Table", "folder": "" },
  "workflow_stages": [
    { "name": "New", "color": 0 },
    { "name": "In progress", "color": 1, "task_page": { "..." }, "details_page": { "..." } },
    { "name": "Done", "color": 2, "details_page": { "..." } }
  ],
  "tabs": [
    { "name": "Tab", "kind": "new_request|user_defined", "visibility": "all|managers" }
  ],
  "displayed_columns": [
    { "id": "UUID or CURRENT_STAGE|CURRENT_TASK|ASSIGNED_TO|EXPIRES_AT|CREATED_BY", "visibility": "all|managers|nobody" }
  ]
}
```

- `creation_page` → the submission form; `workato_db_table` → the backend Data Table.
- `workflow_stages` references `task_page` / `details_page` per stage.
- `displayed_columns.id` is either a Data Table field UUID, or one of the uppercase system columns.

### Page component types (important)

| Field type | Component `type` | `style` |
|---|---|---|
| short-text | `"input"` | `"short-text"` |
| long-text | `"input"` | `"long-text"` |
| date / date-time | **`"date"`** | not used |

**Using `"type": "input"` for a date breaks the page editor. Always use `"type": "date"` for dates.**

## Data Table: *.workato_db_table.json

```json
{
  "name": "Table name",
  "schema": [
    { "id": "UUID", "title": "Field name", "type": "short-text|long-text|number|boolean|date|date-time|file|relation",
      "read_only": false, "hidden": false, "required": false }
  ],
  "project_name": "[App] Project Name"
}
```

- `type: "relation"` references another table via `relation.table_id`.
- System fields (Record ID, Created time, Last modified time) are `read_only` and `hidden`.
- Field IDs are UUID v4. Recipe outputs and pages refer to the UUID as the column name.

## MCP Server: *.mcp_server.json

```json
{
  "name": "Server name",
  "description": "Description of the MCP server (the AI uses this to pick a server)",
  "auth_type": "workato_idp",
  "tools_type": "project_assets",
  "tools": [
    {
      "tool": "ref_0",
      "description": "When the AI should use this tool (Use this tool when... / Do not use this tool when...)",
      "vua_required": true
    }
  ],
  "references": {
    "ref_0": {
      "type": "agentic_skill",
      "id": {
        "zip_name": "Folder/skill_name.agentic_skill.json",
        "name": "skill_name",
        "folder": "Folder"
      }
    }
  }
}
```

### Field details

| Field | Description |
|---|---|
| `name` | Display name of the MCP server. |
| `description` | Server-level description. The AI uses this to choose which server to call. |
| `auth_type` | Authentication method. Verified: `"workato_idp"` (Workato Identity Provider). |
| `tools_type` | Tool kind. Verified: `"project_assets"` (assets in this project). |
| `tools[].tool` | A reference key into `references` (`ref_0`, `ref_1`, ...). |
| `tools[].description` | Detailed instructions the AI uses to pick a tool. |
| `tools[].vua_required` | Whether Verified User Access is required. `true` = the API call uses the end user's credentials. |
| `references` | Maps `ref_N` to an agentic_skill. |

### Relationship

```
mcp_server.json
  └── tools[] → references → agentic_skill.json (multiple allowed)
                                └── references.recipe_id → recipe.json
```

- MCP servers expose skills through a different channel than Genie.
- Genie references skills directly via `references`; an MCP server references them through an ordered `tools[]` array with explicit descriptions.
- Each tool's `description` is analogous to a skill's `trigger_description` but carries more detailed AI-facing instructions.
