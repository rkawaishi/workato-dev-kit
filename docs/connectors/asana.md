# Asana コネクタ

Provider: `asana`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New  event | `new_event` | - |  |
| New or updated task | `new_or_updated_task` | - |  [deprecated] |
| New or updated tasks trigger | `new_or_updated_task_v2` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add task to section | `add_task_to_section` | - |  |
| Create subtask | `create_subtask` | - |  |
| Create tag | `create_tag` | - |  |
| Create task | `create_task` | - |  |
| Get people details by ID | `get_people_details_by_id` | - |  |
| Get project detail by ID | `get_project_detail_by_id` | - |  |
| Get project sections | `get_project_sections` | Yes |  |
| Get task details by ID | `get_task_details_by_id` | - |  |
| List all tasks with tag | `list_all_tasks_with_tag` | Yes |  |
| List people | `list_people` | Yes |  |
| List project tasks | `list_project_tasks` | Yes |  |
| List workspaces | `list_workspaces` | Yes |  |
| Search projects | `search_projects` | Yes |  |
| Search tags | `search_tags` | Yes |  |
| Search tasks | `search_tasks` | Yes |  |
| Update task | `update_task` | - |  |
