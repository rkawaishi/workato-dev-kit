# SQL Server secondary recipes

Provider value to use in every step: `mssql_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "mssql_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (7)

| Internal name | Title | Batch |
|---|---|---|
| `new_row_v2` | New row | - |
| `new_rows_batch` | New rows | yes |
| `new_rows_sql_batch` | New rows via custom SQL | yes |
| `scheduled_select` | Scheduled query | yes |
| `updated_row_v2` | New/updated row | - |
| `updated_rows_batch` | New/updated rows | yes |
| `updated_rows_sql_batch` | New/updated rows via custom SQL | yes |


## Actions (17)

| Internal name | Title | Batch |
|---|---|---|
| `bulk_load` | Bulk load from an on-prem file | - |
| `delete_rows` | Delete rows | yes |
| `execute_procedure` | Execute stored procedure | yes |
| `export_csv_v2` | Export query result | - |
| `insert_row` | Insert row | - |
| `insert_rows_batch` | Insert rows | yes |
| `replicate_table_schema` | Replicate schema | - |
| `run_custom_sql` | Run custom SQL | yes |
| `run_custom_sql_async_v2` | Run long query using custom SQL | - |
| `search_rows` | Select rows | yes |
| `search_rows_sql` | Select rows using custom SQL | yes |
| `sync_objects_to_sqlserver` | Replicate rows | yes |
| `table_schema_info` | Get table schema | - |
| `update_rows` | Update rows | - |
| `update_rows_batch` | Update rows | yes |
| `upsert_rows` | Upsert row | - |
| `upsert_rows_batch` | Upsert rows | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `export_csv` | Export query result | yes |
| `run_custom_sql_async` | Run long query using custom SQL | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
