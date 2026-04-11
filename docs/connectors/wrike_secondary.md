# Wrike secondary コネクタ

Provider: `wrike_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New comment | `new_comment` | - |  [deprecated] |
| New comment | `new_comment_v2` | - |  |
| New event | `new_event_webhook` | - |  |
| New or updated folder | `new_or_updated_folder` | - |  [deprecated] |
| New/updated folder | `new_or_updated_folder_v2` | - |  |
| New/updated folder | `new_or_updated_folder_webhook` | - |  |
| New/updated project | `new_or_updated_project_v2` | - |  |
| New/updated project | `new_or_updated_project_webhook` | - |  |
| New or updated task | `new_or_updated_task` | - |  [deprecated] |
| New/updated task | `new_or_updated_task_v2` | - |  |
| New/updated task | `new_or_updated_task_webhook` | - |  |
| New/updated timelog | `new_or_updated_timelog` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Cancel approval | `cancel_approval` | - |  |
| Copy folder | `copy_folder` | - |  |
| Copy project | `copy_project` | - |  |
| Create approval | `create_approval` | - |  |
| Create comment in folder | `create_comment_in_folder` | - |  |
| Create comment in task | `create_comment_in_task` | - |  |
| Create database | `create_database` | - |  |
| Create field | `create_field` | - |  |
| Create folder | `create_folder` | - |  |
| Create from blueprint | `create_from_blueprint` | - |  |
| Create project | `create_project` | - |  |
| Create records | `create_records` | - |  |
| Create task | `create_task` | - |  |
| Create timelog | `create_timelog` | - |  |
| Create work from custom item type | `create_work` | - |  |
| Delete attachment | `delete_attachment` | - |  |
| Delete records | `delete_records` | - |  |
| Download attachment | `download_attachment` | - |  |
| Get approval by ID | `get_approval_by_id` | - |  |
| Get attachment metadata | `get_attachment_metadata` | Yes |  |
| Get attachment URL | `get_attachment_url` | - |  |
| Get folder by ID | `get_folder_by_id` | - |  |
| Get record ID | `get_id` | - |  |
| Get task by ID | `get_task_by_id` | - |  |
| List approvals | `list_approvals` | Yes |  |
| List attachments | `list_attachments` | Yes |  |
| List custom fields | `list_custom_fields` | Yes |  |
| List users | `list_users` | Yes |  |
| List workflows and statuses | `list_workflows` | Yes |  |
| Update user | `modify_user` | - |  |
| Search approvals | `search_approvals` | Yes |  |
| Search folders | `search_folder` | Yes |  |
| Search projects | `search_project` | Yes |  |
| Search tasks | `search_task` | Yes |  |
| Search timelogs | `search_timelog` | Yes |  |
| Update approval | `update_approval` | - |  |
| Update attachment | `update_attachment` | - |  |
| Update folder | `update_folder` | - |  |
| Update project | `update_project` | - |  |
| Update records | `update_records` | - |  |
| Update task | `update_task` | - |  |
| Update timelog | `update_timelog` | - |  |
| Upload attachment | `upload_attachment` | - |  |
