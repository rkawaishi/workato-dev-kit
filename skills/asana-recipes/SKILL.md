# Asana recipes

Provider value to use in every step: `asana`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "asana"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_event` | New  event | - |
| `new_or_updated_task_v2` | New or updated tasks trigger | - |


## Actions (17)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_task_to_section` | Add task to section | - |
| `create_subtask` | Create subtask | - |
| `create_tag` | Create tag | - |
| `create_task` | Create task | - |
| `get_people_details_by_id` | Get people details by ID | - |
| `get_project_detail_by_id` | Get project detail by ID | - |
| `get_project_sections` | Get project sections | yes |
| `get_task_details_by_id` | Get task details by ID | - |
| `list_all_tasks_with_tag` | List all tasks with tag | yes |
| `list_people` | List people | yes |
| `list_project_tasks` | List project tasks | yes |
| `list_workspaces` | List workspaces | yes |
| `search_projects` | Search projects | yes |
| `search_tags` | Search tags | yes |
| `search_tasks` | Search tasks | yes |
| `update_task` | Update task | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_or_updated_task` | New or updated task | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
