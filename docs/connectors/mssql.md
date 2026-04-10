# SQL Server コネクタ

Provider: `mssql`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New row | `new_row_v2` | - |  |
| New rows | `new_rows_batch` | Yes |  |
| New rows via custom SQL | `new_rows_sql_batch` | Yes |  |
| Scheduled query | `scheduled_select` | Yes |  |
| New/updated row | `updated_row_v2` | - |  |
| New/updated rows | `updated_rows_batch` | Yes |  |
| New/updated rows via custom SQL | `updated_rows_sql_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Bulk load from an on-prem file | `bulk_load` | - |  |
| Delete rows | `delete_rows` | Yes |  |
| Execute stored procedure | `execute_procedure` | Yes |  |
| Export query result | `export_csv` | Yes |  [deprecated] |
| Export query result | `export_csv_v2` | - |  |
| Insert row | `insert_row` | - |  |
| Insert rows | `insert_rows_batch` | Yes |  |
| Replicate schema | `replicate_table_schema` | - |  |
| Run custom SQL | `run_custom_sql` | Yes |  |
| Run long query using custom SQL | `run_custom_sql_async` | Yes |  [deprecated] |
| Run long query using custom SQL | `run_custom_sql_async_v2` | - |  |
| Select rows | `search_rows` | Yes |  |
| Select rows using custom SQL | `search_rows_sql` | Yes |  |
| Replicate rows | `sync_objects_to_sqlserver` | Yes |  |
| Get table schema | `table_schema_info` | - |  |
| Update rows | `update_rows` | - |  |
| Update rows | `update_rows_batch` | Yes |  |
| Upsert row | `upsert_rows` | - |  |
| Upsert rows | `upsert_rows_batch` | Yes |  |
