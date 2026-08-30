# Workfront secondary recipes

Provider value to use in every step: `workfront_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workfront_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_event` | New event | - |
| `new_object` | New record | - |
| `new_or_updated_object` | New/updated record | - |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_object` | Create record | - |
| `download_document` | Download document | - |
| `search_objects` | Search records | yes |
| `update_object` | Update record | - |
| `upload_document` | Upload document | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
