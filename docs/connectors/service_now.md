# ServiceNow コネクタ

Provider: `service_now`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Closed incident | `closed_incident` | - |  [deprecated] |
| New incident | `new_incident` | - |  [deprecated] |
| New record | `new_object` | - |  |
| New record | `new_object_webhook` | - |  |
| New user | `new_sys_user` | - |  [deprecated] |
| New record | `object_batch_created` | Yes |  |
| New/updated record | `object_batch_created_or_updated` | Yes |  |
| Export new records | `object_created_bulk` | - |  |
| Export new/updated records | `object_created_or_updated_bulk` | - |  |
| Scheduled record search | `scheduled_query` | Yes |  |
| New/updated incident | `updated_incident` | - |  [deprecated] |
| New/updated record | `updated_object` | - |  |
| New/updated record | `updated_object_webhook` | - |  |
| New/updated user | `updated_sys_user` | - |  [deprecated] |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Assign user to incident | `assign_user_to_incident` | - |  [deprecated] |
| Create asset | `create_asset` | - |  [deprecated] |
| Create catalog task | `create_catalog_task` | - |  [deprecated] |
| Create change | `create_change` | - |  [deprecated] |
| Create core company | `create_core_company` | - |  [deprecated] |
| Create incident | `create_incident` | - |  [deprecated] |
| Create record | `create_object` | - |  |
| Create record using a template | `create_object_using_template` | - |  |
| Create problem | `create_problem` | - |  [deprecated] |
| Create user | `create_user` | - |  [deprecated] |
| Get attachment contents | `download_attachment` | - |  |
| Get incident details by ID | `get_incident` | - |  [deprecated] |
| Get object schema | `get_table_schema` | - |  |
| Get user details by ID | `get_user` | - |  [deprecated] |
| Search users | `lookup_user` | - |  [deprecated] |
| Search assets | `search_assets` | - |  [deprecated] |
| Search companies | `search_companies` | - |  [deprecated] |
| Search records | `search_objects` | - |  [deprecated] |
| Search records | `search_objects_v2` | Yes |  |
| Search users | `search_users` | - |  [deprecated] |
| Search records using query | `search_using_query` | Yes |  |
| Update asset | `update_asset` | - |  [deprecated] |
| Update company | `update_company` | - |  [deprecated] |
| Update incident | `update_incident` | - |  [deprecated] |
| Update record | `update_object` | - |  |
| Update record using a template | `update_object_using_template` | - |  |
| Update user | `update_user` | - |  [deprecated] |
| Upload attachment | `upload_attachment` | - |  |
