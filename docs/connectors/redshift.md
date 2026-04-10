# Redshift コネクタ

Provider: `redshift`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New row | `new_row` | - |  |
| New rows | `new_rows_batch` | Yes |  |
| New rows via custom SQL | `new_rows_sql_batch` | Yes |  |
| New/updated row | `updated_row` | - |  |
| New/updated rows | `updated_rows_batch` | Yes |  |
| New/updated rows via custom SQL | `updated_rows_sql_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Delete rows | `delete_rows` | Yes |  |
| Export query result | `export_csv_v2` | - |  |
| Insert row | `insert_row` | - |  |
| Insert rows | `insert_row_batch` | Yes |  |
| Run custom SQL | `run_custom_sql` | Yes |  |
| Run long query using custom SQL | `run_custom_sql_async_v2` | - |  |
| Select rows | `search_rows` | Yes |  |
| Select rows using custom SQL | `search_rows_sql` | Yes |  |
| Update rows | `update_rows` | - |  |
| Update rows | `update_rows_batch` | Yes |  |
| Upsert row | `upsert_row` | - |  |
| Upsert rows | `upsert_rows_batch` | Yes |  |
