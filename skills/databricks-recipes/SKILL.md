# Databricks recipes

Provider value to use in every step: `databricks`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "databricks"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_rows_batch` | New rows | yes |
| `new_rows_sql_batch` | New rows via custom SQL | yes |
| `updated_rows_batch` | New/updated rows via custom SQL | yes |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `delete_rows` | Delete rows | yes |
| `export_csv_v2` | Export query result | - |
| `insert_row` | Insert row | - |
| `run_custom_sql` | Run custom SQL | yes |
| `search_rows` | Select rows | yes |
| `search_rows_sql` | Select rows using custom SQL | yes |
| `update_rows` | Update rows | - |
| `upload_to_volume` | Upload file to Volume | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
