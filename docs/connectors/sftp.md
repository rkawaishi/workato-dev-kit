# SFTP コネクタ

Provider: `sftp`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New/updated CSV file in directory | `new_csv_file` | Yes |  |
| New/updated file in directory | `new_file_in_dir` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
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
