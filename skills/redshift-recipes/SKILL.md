# Redshift recipes

Provider value to use in every step: `redshift`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "redshift"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `new_row` | New row | - |
| `new_rows_batch` | New rows | yes |
| `new_rows_sql_batch` | New rows via custom SQL | yes |
| `updated_row` | New/updated row | - |
| `updated_rows_batch` | New/updated rows | yes |
| `updated_rows_sql_batch` | New/updated rows via custom SQL | yes |


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `delete_rows` | Delete rows | yes |
| `export_csv_v2` | Export query result | - |
| `insert_row` | Insert row | - |
| `insert_row_batch` | Insert rows | yes |
| `run_custom_sql` | Run custom SQL | yes |
| `run_custom_sql_async_v2` | Run long query using custom SQL | - |
| `search_rows` | Select rows | yes |
| `search_rows_sql` | Select rows using custom SQL | yes |
| `update_rows` | Update rows | - |
| `update_rows_batch` | Update rows | yes |
| `upsert_row` | Upsert row | - |
| `upsert_rows_batch` | Upsert rows | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
