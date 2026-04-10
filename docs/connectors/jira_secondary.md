# Jira secondary コネクタ

Provider: `jira_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Deleted object | `deleted_object` | - |  |
| Export new issues in Jira | `issue_created_bulk` | - |  |
| Export new/updated issues in Jira | `issue_created_or_updated_bulk` | - |  |
| New event | `new_event` | - |  |
| New issue | `new_issue` | - |  |
| New issue | `new_issue_batch` | Yes |  |
| Updated issue priority | `new_issue_priority` | - |  [deprecated] |
| New project | `new_project` | - |  [deprecated] |
| New/updated comment | `updated_comment_webhook` | - |  |
| Updated issue | `updated_issue` | - |  |
| Updated issue | `updated_issue_batch` | Yes |  |
| Updated issue status | `updated_issue_status` | - |  [deprecated] |
| New/updated issue | `updated_issue_webhook` | - |  |
| New/updated worklog | `updated_worklog_webhook` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Assign user to issue | `assign_issue` | - |  |
| Create comment | `create_comment` | - |  |
| Create issue | `create_issue` | - |  |
| Create user | `create_user` | - |  |
| Get user details | `find_user` | - |  |
| Download attachment | `get_attachment` | - |  |
| Get changelog of an issue | `get_changelog` | - |  |
| Get issue | `get_issue` | - |  |
| Get issue comments | `get_issue_comments` | Yes |  |
| Get issue schema | `get_object_schema` | - |  |
| Search assignable users | `search_assignable_users` | Yes |  |
| Search issues | `search_issues` | Yes |  |
| Search issues by JQL | `search_issues_by_JQL` | Yes |  |
| Update comment | `update_comment` | - |  |
| Update issue | `update_issue` | - |  |
| Update issue status | `update_issue_status` | - |  |
| Upload attachment | `upload_attachment` | - |  |
