# OneDrive コネクタ

Provider: `onedrive`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New line in CSV file | `new_csv_line` | - |  |
| New event | `new_event_trigger` | - |  |
| New file | `new_file` | - |  |
| New folder | `new_folder` | - |  |
| New/updated file | `updated_file` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create folder | `create_folder` | - |  |
| Add permission | `create_permission` | - |  |
| Delete file or folder | `delete_file_or_folder` | - |  |
| Remove permission | `delete_permission` | - |  |
| Download File | `download_file` | - |  |
| List files and folders | `list_files_folders` | Yes |  |
| List permissions | `list_permission` | Yes |  |
| Search files | `search_files` | - |  [deprecated] |
| Search files | `search_files_new` | Yes |  |
| Upload file via file content | `upload_file` | - |  |
| Upload file from URL | `upload_file_from_url` | - |  |
| Upload large file via session | `upload_file_session` | - |  |
