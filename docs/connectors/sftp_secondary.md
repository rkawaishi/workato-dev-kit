# SFTP secondary connector

Provider: `sftp_secondary`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New/updated CSV file in directory | `new_csv_file` | Yes |  |
| New/updated file in directory | `new_file_in_dir` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Copy file | `copy` | - |  [deprecated] |
| List folder | `dir` | Yes |  |
| Download file | `download` | - |  [deprecated] |
| Create folder | `mkdir` | - |  |
| Delete file | `remove` | - |  |
| Delete folder | `remove_folder` | - |  |
| Rename/move file | `rename` | - |  |
| Search files/folders | `search_files_folders` | Yes |  |
| Change permission of a file or a folder | `set_permissions` | - |  |
| Get file information | `stat` | - |  |
| Download file | `streamable_download` | - |  |
| Upload file | `upload` | - |  |
