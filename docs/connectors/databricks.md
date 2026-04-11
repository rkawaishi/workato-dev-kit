# Databricks コネクタ

Provider: `databricks`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New rows | `new_rows_batch` | Yes |  |
| New rows via custom SQL | `new_rows_sql_batch` | Yes |  |
| New/updated rows via custom SQL | `updated_rows_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Delete rows | `delete_rows` | Yes |  |
| Export query result | `export_csv_v2` | - |  |
| Insert row | `insert_row` | - |  |
| Run custom SQL | `run_custom_sql` | Yes |  |
| Select rows | `search_rows` | Yes |  |
| Select rows using custom SQL | `search_rows_sql` | Yes |  |
| Update rows | `update_rows` | - |  |
| Upload file to Volume | `upload_to_volume` | - |  |
