# Eloqua recipes

Provider value to use in every step: `eloqua`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "eloqua"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_objects` | New record | - |
| `new_or_updated_objects` | New or updated record | - |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_object` | Create record | - |
| `delete_object` | Delete record | - |
| `get_object_by_id` | Get record details | - |
| `search_object` | Search records | yes |
| `update_object` | Update record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
