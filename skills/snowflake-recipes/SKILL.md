# Snowflake recipes

Provider value to use in every step: `snowflake`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "snowflake"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (5)

| Internal name | Title | Batch |
|---|---|---|
| `new_row` | New row | - |
| `new_rows_batch` | New rows | yes |
| `scheduled_select` | Scheduled query | yes |
| `updated_row` | New/updated row | - |
| `updated_rows_batch` | New/updated rows | yes |


## Actions (14)

| Internal name | Title | Batch |
|---|---|---|
| `bulk_load_s3` | Bulk load data to table from stage | yes |
| `delete_rows` | Delete rows | yes |
| `export_csv_v2` | Export query result | - |
| `insert_row` | Insert row | - |
| `merge_action` | Merge rows | - |
| `replicate_table_schema` | Replicate schema | - |
| `run_custom_sql` | Run custom SQL | yes |
| `run_custom_sql_async_v2` | Run long query using custom SQL | - |
| `search_rows` | Select rows | yes |
| `search_rows_sql` | Select rows using custom SQL | yes |
| `sync_objects_to_snowflake_v2` | Replicate rows | yes |
| `update_rows` | Update rows | - |
| `upload_to_internal_stage` | Upload file to internal stage | - |
| `upsert_rows_batch` | Upsert rows | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `sync_objects_to_snowflake` | Replicate rows | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
