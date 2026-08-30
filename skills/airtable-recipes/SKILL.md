# Airtable recipes

Provider value to use in every step: `airtable`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "airtable"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_or_updated_record` | New/updated record | - |
| `new_record` | New record | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_record` | Create record | - |
| `delete_records` | Delete record | - |
| `delete_records_batch` | Delete records | yes |
| `get_records` | Get record | - |
| `list_records` | List records | yes |
| `search_records` | Search records | yes |
| `update_record` | Update record | - |
| `upsert_record` | Upsert record | - |
| `upsert_records_batch` | Upsert records | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
