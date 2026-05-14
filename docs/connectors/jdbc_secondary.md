# JDBC secondary connector

Provider: `jdbc_secondary`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New row | `new_row` | - |  |
| New rows | `new_rows_batch` | Yes |  |
| New rows via custom SQL | `new_rows_sql_batch` | Yes |  |
| Scheduled query | `scheduled_select` | Yes |  |
| New/updated rows via custom SQL | `updated_rows_sql_batch` | Yes |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Export query result | `export_csv` | Yes |  [deprecated] |
| Export query result | `export_csv_v2` | - |  |
| Insert rows | `insert_rows_batch` | Yes |  |
| Run custom SQL | `run_custom_sql` | Yes |  |
| Run long query using custom SQL | `run_custom_sql_async` | Yes |  [deprecated] |
| Run long query using custom SQL | `run_custom_sql_async_v2` | - |  |
| Select rows | `search_rows` | Yes |  |
| Select rows using custom SQL | `search_rows_sql` | Yes |  |
