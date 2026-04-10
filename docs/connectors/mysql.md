# MySQL コネクタ

Provider: `mysql`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New row | `new_row_v2` | - |  |
| New rows | `new_rows_batch` | Yes |  |
| Scheduled query | `scheduled_select` | Yes |  |
| New/updated row | `updated_row_v2` | - |  |
| New/updated rows | `updated_rows_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Delete rows | `delete_rows` | Yes |  |
| Execute stored procedure | `execute_procedure` | Yes |  |
| Export query result | `export_csv` | Yes |  [deprecated] |
| Export query result | `export_csv_v2` | - |  |
| Insert row | `insert_row` | - |  |
| Insert rows | `insert_row_batch` | Yes |  |
| Run custom SQL | `run_custom_sql` | Yes |  |
| Run long query using custom SQL | `run_custom_sql_async_v2` | - |  |
| Select rows | `search_rows` | Yes |  |
| Get table schema | `table_schema_info` | - |  |
| Update rows | `update_rows` | - |  |
| Upsert rows | `upsert_row_batch` | Yes |  |
| Upsert row | `upsert_rows` | - |  |
