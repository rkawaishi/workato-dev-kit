# FTP/FTPS connector

Provider: `ftps`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New CSV file | `new_csv_file` | Yes |  |
| New/updated file in directory | `new_file_in_dir` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Download file | `get_file_content` | - |  |
| List files and directories | `list_directories_files` | Yes |  |
| Remove file | `remove` | - |  |
| Rename file | `rename` | - |  |
| Get file information | `stat` | - |  |
| Download large file | `streamable_get_file_content` | - |  |
| Upload file | `upload` | - |  |
