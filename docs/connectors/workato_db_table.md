# Workato Data Tables コネクタ

Provider: `workato_db_table`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New records | `new_records_polling` | Yes |  |
| New record | `new_records_realtime` | - |  |
| New/updated records | `updated_records_polling` | Yes |  |
| New/updated record | `updated_records_realtime` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Create record | `add_record` | - |  |
| Create records | `create_records_batch` | Yes |  |
| Delete record | `delete_record` | - |  |
| Delete records | `delete_records_batch` | Yes |  |
| Search records | `get_records` | Yes |  |
| Remove values from a record | `remove_values_from_record` | - |  |
| Truncate table | `truncate_table` | Yes |  |
| Update record | `update_record` | - |  |
| Update records | `update_records_batch` | Yes |  |
| Upsert record | `upsert_record` | - |  |
