# Dropbox コネクタ

Provider: `dropbox`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New file revision | `file_revision` | - |  |
| New lines in CSV file | `new_batch_csv_file_lines` | Yes |  |
| New line in CSV file | `new_csv_file_line` | - |  |
| New/updated file in directory | `new_or_changed_file` | - |  |
| New/updated CSV file in directory | `new_or_updated_csv_file` | - |  |
| New/updated line in CSV file | `updated_csv_file_line` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Copy file or folder | `copy_file` | - |  |
| Create folder | `create_folder` | - |  |
| Delete file or folder | `delete_file` | - |  |
| Fetch deleted files and folders | `fetch_deleted_files_and_folders` | - |  |
| Download file | `file_download` | - |  |
| Get metadata of a file or folder | `get_metadata` | - |  |
| Move/rename file or folder | `move_file` | - |  |
| Read CSV file lines | `read_csv_file_lines` | Yes |  |
| Search files | `search_files` | Yes |  |
| Search folders | `search_folder` | Yes |  |
| Update CSV file in dropbox | `update_csv_file` | - |  |
| Upload file using file contents | `upload_file_content` | - |  [deprecated] |
| Upload file using file contents | `upload_file_content_stream` | - |  |
| Upload file from URL | `upload_file_from_url` | - |  |
| Upload multiline file | `upload_multiline_file` | - |  |
