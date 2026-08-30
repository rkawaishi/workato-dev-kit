# Pivotal Tracker recipes

Provider value to use in every step: `pivotal_tracker`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "pivotal_tracker"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_or_updated_story` | New or updated story | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_comment` | Create comment | - |
| `create_story` | Create story | - |
| `create_task` | Create task | - |
| `delete_story` | Delete story | - |
| `get_story_by_id` | Get story by ID | - |
| `get_task_by_id` | Get task by ID | - |
| `list_task_in_a_story` | List tasks in a story | yes |
| `update_story` | Update story | - |
| `update_task` | Update task | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
