# TrackVia recipes

Provider value to use in every step: `trackvia`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "trackvia"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `deleted_record` | Deleted record | - |
| `new_record` | New record | - |
| `updated_record` | Updated record | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_record` | Create record | - |
| `create_user` | Create user | - |
| `delete_all_records_in_view` | Delete all records in view | - |
| `delete_record` | Delete record | - |
| `get_all_view_records` | Get all view records | yes |
| `get_file_from_record` | Get file from record | - |
| `get_record` | Get record | - |
| `update_record` | Update record | - |
| `upload_file_to_record` | Upload file to a record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
