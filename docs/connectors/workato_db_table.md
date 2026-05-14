# Workato Data Tables connector

Provider: `workato_db_table`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New records | `new_records_polling` | Yes |  |
| New record | `new_records_realtime` | - |  |
| New/updated records | `updated_records_polling` | Yes |  |
| New/updated record | `updated_records_realtime` | - |  |

## Actions

| Name | Internal name | Batch | Description |
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
