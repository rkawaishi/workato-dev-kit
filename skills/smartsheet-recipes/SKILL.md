# Smartsheet recipes

Provider value to use in every step: `smartsheet`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "smartsheet"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_or_updated_row` | New or updated row in a sheet | - |
| `new_or_updated_row_in_report` | New or updated row in report | - |
| `new_row_in_report` | New row in report | - |


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_row` | Create row | - |
| `get_row_by_id` | Get row by ID | - |
| `search_rows` | Search rows | yes |
| `update_row` | Update row | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
