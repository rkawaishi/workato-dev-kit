# Wrike secondary recipes

Provider value to use in every step: `wrike_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "wrike_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (9)

| Internal name | Title | Batch |
|---|---|---|
| `new_comment_v2` | New comment | - |
| `new_event_webhook` | New event | - |
| `new_or_updated_folder_v2` | New/updated folder | - |
| `new_or_updated_folder_webhook` | New/updated folder | - |
| `new_or_updated_project_v2` | New/updated project | - |
| `new_or_updated_project_webhook` | New/updated project | - |
| `new_or_updated_task_v2` | New/updated task | - |
| `new_or_updated_task_webhook` | New/updated task | - |
| `new_or_updated_timelog` | New/updated timelog | - |


## Actions (44)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `cancel_approval` | Cancel approval | - |
| `copy_folder` | Copy folder | - |
| `copy_project` | Copy project | - |
| `create_approval` | Create approval | - |
| `create_comment_in_folder` | Create comment in folder | - |
| `create_comment_in_task` | Create comment in task | - |
| `create_database` | Create database | - |
| `create_field` | Create field | - |
| `create_folder` | Create folder | - |
| `create_from_blueprint` | Create from blueprint | - |
| `create_project` | Create project | - |
| `create_records` | Create records | - |
| `create_task` | Create task | - |
| `create_timelog` | Create timelog | - |
| `create_work` | Create work from custom item type | - |
| `delete_attachment` | Delete attachment | - |
| `delete_records` | Delete records | - |
| `download_attachment` | Download attachment | - |
| `get_approval_by_id` | Get approval by ID | - |
| `get_attachment_metadata` | Get attachment metadata | yes |
| `get_attachment_url` | Get attachment URL | - |
| `get_folder_by_id` | Get folder by ID | - |
| `get_id` | Get record ID | - |
| `get_task_by_id` | Get task by ID | - |
| `list_approvals` | List approvals | yes |
| `list_attachments` | List attachments | yes |
| `list_custom_fields` | List custom fields | yes |
| `list_users` | List users | yes |
| `list_workflows` | List workflows and statuses | yes |
| `modify_user` | Update user | - |
| `search_approvals` | Search approvals | yes |
| `search_folder` | Search folders | yes |
| `search_project` | Search projects | yes |
| `search_task` | Search tasks | yes |
| `search_timelog` | Search timelogs | yes |
| `update_approval` | Update approval | - |
| `update_attachment` | Update attachment | - |
| `update_folder` | Update folder | - |
| `update_project` | Update project | - |
| `update_records` | Update records | - |
| `update_task` | Update task | - |
| `update_timelog` | Update timelog | - |
| `upload_attachment` | Upload attachment | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_comment` | New comment | - |
| `new_or_updated_folder` | New or updated folder | - |
| `new_or_updated_task` | New or updated task | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
