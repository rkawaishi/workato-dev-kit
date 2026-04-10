# PostgreSQL コネクタ

Provider: `postgresql`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New row | `new_row_v2` | - |  |
| New rows | `new_rows_batch` | Yes |  |
| New/updated row | `updated_row_v2` | - |  |
| New/updated rows | `updated_rows_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Delete rows | `delete_rows` | Yes |  |
| Export query result | `export_csv` | Yes |  [deprecated] |
| Export query result | `export_csv_v2` | - |  |
| Insert row | `insert_row` | - |  |
| Run custom SQL | `run_custom_sql` | Yes |  |
| Run long query using custom SQL | `run_custom_sql_async_v2` | - |  |
| Select rows | `search_rows` | Yes |  |
| Select rows using custom SQL | `search_rows_sql` | Yes |  |
| Get table schema | `table_schema_info` | - |  |
| Update rows | `update_rows` | - |  |
| Upsert rows | `upsert_rows_batch` | Yes |  |
