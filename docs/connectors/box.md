# Box コネクタ

Provider: `box`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New upload/download event (beta) | `event_notification` | - |  [deprecated] |
| Monitor sign requests | `monitor_sign_request` | - |  [deprecated] |
| New CSV file in folder | `new_csv_file` | Yes |  |
| New event in folder | `new_event_webhook` | - |  |
| New/updated file in folder | `new_file` | - |  |
| New line in CSV file | `new_line_csv_file` | - |  |
| New/updated CSV file in folder | `new_or_updated_csv_file` | Yes |  |
| New/updated file metadata in folder | `new_updated_file_metadata` | - |  |
| New/updated folder in folder | `new_updated_folder` | - |  |
| New/updated sign event in folder | `new_updated_sign_event` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add comment to file | `add_comment_to_file` | - |  |
| Add user as collaborator | `add_user_as_collaborator` | - |  [deprecated] |
| Cancel sign request | `cancel_sign_request` | - |  |
| Copy file or folder | `copy_file` | - |  |
| Create collaboration | `create_collaboration` | - |  |
| Create file shared link | `create_file_shared_link` | - |  |
| Create folder | `create_folder` | - |  |
| Create folder shared link | `create_folder_shared_link` | - |  |
| Create file metadata | `create_metadata` | - |  |
| Create sign request | `create_sign_request` | - |  |
| Delete file or folder | `delete_file` | - |  |
| Delete file metadata | `delete_metadata` | - |  |
| Download file | `download_file` | - |  |
| Get file download URL | `download_file_url` | - |  |
| List folder items | `folder_items` | Yes |  |
| Get file comments | `get_file_comments` | Yes |  |
| Get file metadata | `get_metadata` | - |  |
| Get sign request | `get_sign_request` | - |  |
| List sign requests | `list_sign_requests` | Yes |  |
| Rename/move file or folder | `move_file` | - |  |
| Rename other user’s file or folder | `rename_other_files` | - |  |
| Resend sign request | `resend_sign_request` | - |  |
| Search files or folders | `search_files` | Yes |  |
| Update CSV file in box | `update_csv_file` | - |  |
| Update file metadata | `update_metadata` | - |  |
| Upload file using file contents | `upload_file_content` | - |  |
| Upload file using file URL | `upload_file_from_url` | - |  |
