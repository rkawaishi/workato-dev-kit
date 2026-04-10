# Google Drive コネクタ

Provider: `google_drive`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New activity | `new_activity` | - |  |
| New CSV file | `new_csv_file_batch` | Yes |  |
| New file or folder in folder hierarchy | `new_file_in_subfolder` | - |  |
| New file or folder | `new_file_or_folder` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add permission to a file | `add_permission` | - |  |
| Copy file | `copy_file` | - |  |
| Create folder | `create_folder` | - |  |
| Delete file | `delete_file` | - |  |
| Download file | `download_file_contents` | - |  |
| Export file | `export_file` | - |  |
| Get permission of a file | `get_permission` | - |  |
| List permissions of a file | `list_permission` | Yes |  |
| Rename or move file/folder | `move_rename_file` | - |  |
| Remove permissions from a file | `remove_permission` | - |  |
| Search files or folders | `search_file_or_folder` | Yes |  |
| Update permission of a file | `update_permission` | - |  |
| Upload small file | `upload_file` | - |  [deprecated] |
| Upload file | `upload_file_stream` | - |  |
