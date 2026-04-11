# Microsoft Dynamics 365 コネクタ

Provider: `microsoft_dynamics_crm`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Export new records | `created_bulk_object` | - |  |
| Export new/updated records | `created_or_updated_bulk_object` | - |  |
| Deleted object | `deleted_object` | - |  |
| Monitor changes in entities | `monitor_changes_delta_link_trigger` | - |  |
| Monitor changes in entities | `monitor_changes_delta_link_trigger_batch` | Yes |  |
| New object | `new_object` | - |  [deprecated] |
| New object | `new_object_v2` | - |  |
| New or updated object (batch) | `new_or_updated_batch_object` | Yes |  |
| New or updated object | `new_or_updated_object` | - |  [deprecated] |
| New or updated object | `new_or_updated_object_v2` | - |  |
| New object | `new_webhook` | - |  |
| Scheduled object search | `scheduled_object_search` | Yes |  |
| New/updated object | `updated_webhook` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Close case | `close_case` | - |  |
| Create object | `create_object` | - |  |
| Create object | `create_object_batch` | Yes |  |
| Get object by ID | `get_object_by_id` | - |  |
| Get object schema | `get_object_schema` | - |  |
| Search objects | `search_objects` | Yes |  |
| Update object | `update_object` | - |  |
| Update object | `update_object_batch` | Yes |  |
