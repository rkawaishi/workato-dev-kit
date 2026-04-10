# Snowflake secondary コネクタ

Provider: `snowflake_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New row | `new_row` | - |  |
| New rows | `new_rows_batch` | Yes |  |
| Scheduled query | `scheduled_select` | Yes |  |
| New/updated row | `updated_row` | - |  |
| New/updated rows | `updated_rows_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Bulk load data to table from stage | `bulk_load_s3` | Yes |  |
| Delete rows | `delete_rows` | Yes |  |
| Export query result | `export_csv_v2` | - |  |
| Insert row | `insert_row` | - |  |
| Merge rows | `merge_action` | - |  |
| Replicate schema | `replicate_table_schema` | - |  |
| Run custom SQL | `run_custom_sql` | Yes |  |
| Run long query using custom SQL | `run_custom_sql_async_v2` | - |  |
| Select rows | `search_rows` | Yes |  |
| Select rows using custom SQL | `search_rows_sql` | Yes |  |
| Replicate rows | `sync_objects_to_snowflake` | Yes |  [deprecated] |
| Replicate rows | `sync_objects_to_snowflake_v2` | Yes |  |
| Update rows | `update_rows` | - |  |
| Upload file to internal stage | `upload_to_internal_stage` | - |  |
| Upsert rows | `upsert_rows_batch` | Yes |  |
