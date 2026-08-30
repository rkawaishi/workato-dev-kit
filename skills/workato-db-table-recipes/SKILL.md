# Workato Data Tables recipes

Provider value to use in every step: `workato_db_table`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_db_table"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_records_polling` | New records | yes |
| `new_records_realtime` | New record | - |
| `updated_records_polling` | New/updated records | yes |
| `updated_records_realtime` | New/updated record | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `add_record` | Create record | - |
| `create_records_batch` | Create records | yes |
| `delete_record` | Delete record | - |
| `delete_records_batch` | Delete records | yes |
| `get_records` | Search records | yes |
| `remove_values_from_record` | Remove values from a record | - |
| `truncate_table` | Truncate table | yes |
| `update_record` | Update record | - |
| `update_records_batch` | Update records | yes |
| `upsert_record` | Upsert record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
