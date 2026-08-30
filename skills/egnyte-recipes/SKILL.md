# Egnyte recipes

Provider value to use in every step: `egnyte`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "egnyte"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_events` | New/updated/deleted events | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `copy_or_move_file` | Copy or move file | - |
| `copy_or_move_folder` | Copy or move folder | - |
| `create_folder` | Create folder | - |
| `download_file` | Download file from selected folder | - |
| `get_event_details` | Get event details | - |
| `get_object` | Get object details | - |
| `search_objects` | Search objects | yes |
| `upload_file` | Upload file | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
