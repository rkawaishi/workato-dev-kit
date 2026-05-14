# Quickbase connector

Provider: `quickbase`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New record | `new_form_entry` | - |  [deprecated] |
| New record | `new_record` | - |  |
| New record | `new_record_webhook` | - |  [deprecated] |
| New record | `new_record_webhook_trigger` | - |  |
| Scheduled record search using query | `scheduled_table_query` | Yes |  |
| Updated record | `updated_form_entry` | - |  [deprecated] |
| New/updated record | `updated_record` | - |  |
| New/updated record | `updated_record_webhook` | - |  [deprecated] |
| New/updated record | `updated_record_webhook_trigger` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create record | `add_record` | - |  |
| Create and update records in bulk from CSV file | `bulk_upsert_records` | Yes |  |
| Delete record | `delete_record` | - |  |
| Download attachment | `download_attachment` | - |  |
| Update record | `edit_record` | - |  |
| Get records from report in Quickbase | `get_records_from_a_report` | Yes |  |
| Delete records in a report | `purge_records_by_query` | Yes |  |
| Search record | `search_record` | - |  [deprecated] |
| Search records | `search_records` | Yes |  |
| Update record | `update_record` | - |  [deprecated] |
