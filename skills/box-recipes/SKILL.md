# Box recipes

Provider value to use in every step: `box`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "box"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (8)

| Internal name | Title | Batch |
|---|---|---|
| `new_csv_file` | New CSV file in folder | yes |
| `new_event_webhook` | New event in folder | - |
| `new_file` | New/updated file in folder | - |
| `new_line_csv_file` | New line in CSV file | - |
| `new_or_updated_csv_file` | New/updated CSV file in folder | yes |
| `new_updated_file_metadata` | New/updated file metadata in folder | - |
| `new_updated_folder` | New/updated folder in folder | - |
| `new_updated_sign_event` | New/updated sign event in folder | - |


## Actions (27)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_comment_to_file` | Add comment to file | - |
| `cancel_sign_request` | Cancel sign request | - |
| `copy_file` | Copy file or folder | - |
| `create_collaboration` | Create collaboration | - |
| `create_file_shared_link` | Create file shared link | - |
| `create_folder` | Create folder | - |
| `create_folder_shared_link` | Create folder shared link | - |
| `create_metadata` | Create file metadata | - |
| `create_sign_request` | Create sign request | - |
| `delete_file` | Delete file or folder | - |
| `delete_metadata` | Delete file metadata | - |
| `download_file` | Download file | - |
| `download_file_url` | Get file download URL | - |
| `folder_items` | List folder items | yes |
| `get_file_comments` | Get file comments | yes |
| `get_metadata` | Get file metadata | - |
| `get_sign_request` | Get sign request | - |
| `list_sign_requests` | List sign requests | yes |
| `move_file` | Rename/move file or folder | - |
| `rename_other_files` | Rename other user’s file or folder | - |
| `resend_sign_request` | Resend sign request | - |
| `search_files` | Search files or folders | yes |
| `update_csv_file` | Update CSV file in box | - |
| `update_metadata` | Update file metadata | - |
| `upload_file_content` | Upload file using file contents | - |
| `upload_file_from_url` | Upload file using file URL | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `event_notification` | New upload/download event (beta) | - |
| `monitor_sign_request` | Monitor sign requests | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `add_user_as_collaborator` | Add user as collaborator | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
