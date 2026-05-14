# Workflow apps by Workato connector

Provider: `workato_workflow_task`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New component event | `app_function_generic_request` | - |  |
| New component event (Dropdown) | `app_function_load_dropdown_request` | - |  |
| New component event (Table widget) | `app_function_load_table_request` | - |  |
| New request | `new_requests_realtime` | - |  |
| New/updated request | `updated_requests_realtime` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Create request | `add_request` | - |  |
| Return data to component | `app_function_load_dropdown_return` | - |  [deprecated] |
| Return data to component | `app_function_return` | - |  |
| Change workflow stage | `change_workflow_stage` | - |  |
| Complete workflow task programmatically | `complete_task` | - |  |
| Delete request | `delete_request` | - |  |
| Remove user | `delete_user` | - |  |
| Get user data | `find_users` | Yes |  |
| Search requests | `get_requests` | Yes |  |
| Assign task to users | `human_review_on_existing_record` | - |  |
| Invite user | `invite_user` | - |  |
| List workflow stages | `list_workflow_stages` | - |  |
| Get activity history | `lookup_events` | Yes |  |
| Share request | `share_request` | - |  |
| Unshare request | `unshare_request` | - |  |
| Update request | `update_request` | - |  |
