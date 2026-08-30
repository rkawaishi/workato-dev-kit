# Percolate recipes

Provider value to use in every step: `percolate`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "percolate"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `delete_object` | Deleted object | - |
| `new_object` | New object | - |
| `new_updated_object` | New or Updated object | - |


## Actions (11)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `check_content_workflow_step` | Check content workflow step | - |
| `copy_asset` | Copy asset | - |
| `create_object` | Create object | - |
| `custom_action` | Custom action | - |
| `download_asset` | Download asset | - |
| `get_object_details_by_id` | Get object details by ID | - |
| `search_objects` | Search objects | yes |
| `update_object` | Update object | - |
| `update_production_workflow_transition` | Update object's production workflow step | - |
| `upload_asset` | Upload asset | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
