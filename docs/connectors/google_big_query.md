# Google BigQuery コネクタ

Provider: `google_big_query`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New job completed | `new_job_completed` | - |  |
| New row | `new_row` | - |  |
| New rows | `new_rows_batch` | Yes |  |
| Scheduled query | `scheduled_query` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Get batch of rows by Job ID | `get_query_job_output` | Yes |  |
| Insert row | `insert_row` | - |  |
| Insert rows | `insert_rows` | Yes |  [deprecated] |
| Insert rows | `insert_rows_stream` | Yes |  |
| Load data into BigQuery | `load_data_from_file` | - |  |
| Load data from Google Cloud Storage into BigQuery | `load_data_from_google_table` | - |  |
| Run custom SQL in BigQuery | `run_custom_sql` | - |  [deprecated] |
| Run custom SQL in BigQuery | `run_custom_sql_sync` | - |  |
| Select rows (Old) | `search_rows` | Yes |  |
| Select rows | `search_rows_sync` | Yes |  |
| Select rows using custom SQL (Old) | `search_rows_using_custom_sql` | Yes |  |
| Select rows using custom SQL | `search_rows_using_custom_sql_sync` | Yes |  |
| Select rows using custom SQL and insert into table | `search_rows_using_custom_sql_sync_insert_table` | Yes |  |
