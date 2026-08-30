# Jira secondary recipes

Provider value to use in every step: `jira_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "jira_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (11)

| Internal name | Title | Batch |
|---|---|---|
| `deleted_object` | Deleted object | - |
| `issue_created_bulk` | Export new issues in Jira | - |
| `issue_created_or_updated_bulk` | Export new/updated issues in Jira | - |
| `new_event` | New event | - |
| `new_issue` | New issue | - |
| `new_issue_batch` | New issue | yes |
| `updated_comment_webhook` | New/updated comment | - |
| `updated_issue` | Updated issue | - |
| `updated_issue_batch` | Updated issue | yes |
| `updated_issue_webhook` | New/updated issue | - |
| `updated_worklog_webhook` | New/updated worklog | - |


## Actions (18)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `assign_issue` | Assign user to issue | - |
| `create_comment` | Create comment | - |
| `create_issue` | Create issue | - |
| `create_user` | Create user | - |
| `find_user` | Get user details | - |
| `get_attachment` | Download attachment | - |
| `get_changelog` | Get changelog of an issue | - |
| `get_issue` | Get issue | - |
| `get_issue_comments` | Get issue comments | yes |
| `get_object_schema` | Get issue schema | - |
| `search_assignable_users` | Search assignable users | yes |
| `search_issues` | Search issues | yes |
| `search_issues_by_JQL` | Search issues by JQL | yes |
| `update_comment` | Update comment | - |
| `update_issue` | Update issue | - |
| `update_issue_status` | Update issue status | - |
| `upload_attachment` | Upload attachment | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_issue_priority` | Updated issue priority | - |
| `new_project` | New project | - |
| `updated_issue_status` | Updated issue status | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
