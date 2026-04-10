# Microsoft Sharepoint コネクタ

Provider: `microsoft_sharepoint`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Deleted File or Folder | `deleted_file_folder` | - |  |
| New row in Sharepoint list | `new_row_in_sharepoint_list` | - |  |
| New/updated file in folder hierarchy | `new_updated_file_in_folder_hierarchy` | - |  |
| New/updated file in folder hierarchy (large site) | `new_updated_file_in_folder_hierarchy_v2` | - |  |
| New or updated file | `new_updated_file_in_sharepoint_library` | - |  |
| New/updated row in Sharepoint list | `new_updated_row_in_sharepoint_list` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add row in Sharepoint list | `add_row_in_sharepoint_list` | - |  |
| Copy file | `copy_file` | - |  |
| Create Folder | `create_folder` | - |  |
| Create rows | `create_row_in_sharepoint_list_batch` | Yes |  |
| Delete file or folder from library | `delete_file_from_library` | - |  |
| Delete row | `delete_row_in_sharepoint_list` | - |  |
| Download attachment | `download_attachment` | - |  |
| Download file from library | `download_file_from_library` | - |  |
| Get file and folder details | `get_file_folder` | - |  |
| Get file or folder permissions | `get_permission` | Yes |  |
| List files and folders within a folder | `list_files_folders` | Yes |  |
| Move file | `move_file` | - |  |
| Rename file or folder | `rename_file_folder` | - |  |
| Search files | `search_file_by_name` | Yes |  |
| Search list items | `search_list_items` | Yes |  [deprecated] |
| Search list items | `search_list_items_v2` | Yes |  |
| Search users | `search_users` | Yes |  |
| Update file using file contents | `update_file_in_library` | - |  |
| Update file metadata | `update_file_metadata` | - |  |
| Update row | `update_row_in_sharepoint_list` | - |  |
| Update rows | `update_row_in_sharepoint_list_batch` | Yes |  |
| Upload attachment | `upload_attachment` | - |  |
| Upload file in library | `upload_file_in_library` | - |  |
