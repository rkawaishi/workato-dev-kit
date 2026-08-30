# Hive recipes

Provider value to use in every step: `hive`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "hive"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_updated_record` | New/updated record | - |


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `apply_action_template` | Apply action template | - |
| `create_record` | Create record | - |
| `delete_record` | Delete record | - |
| `get_record_by_id` | Get record details by ID | - |
| `list_records` | List records | yes |
| `update_record` | Update record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
