# Salesforce Marketing Cloud recipes

Provider value to use in every step: `salesforce_marketing_cloud`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "salesforce_marketing_cloud"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_data_extension_row` | New data extension row | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `copy_data_extension` | Copy data extension | - |
| `create_asset` | Create email from HTML template | - |
| `create_data_extension_from_template` | Create data extension from template | - |
| `delete_data_extension` | Delete data extension | - |
| `list_data_extension` | Search data extension | yes |
| `read_data_extension` | Search data extension row | yes |
| `upload_asset` | Upload asset | - |
| `upsert_data_extension` | Upsert data extension row | - |
| `upsert_data_extension_row_bulk` | Upsert data extension row | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
