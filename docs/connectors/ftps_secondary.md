# FTP/FTPS secondary コネクタ

Provider: `ftps_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New CSV file | `new_csv_file` | Yes |  |
| New/updated file in directory | `new_file_in_dir` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Download file | `get_file_content` | - |  |
| List files and directories | `list_directories_files` | Yes |  |
| Remove file | `remove` | - |  |
| Rename file | `rename` | - |  |
| Get file information | `stat` | - |  |
| Download large file | `streamable_get_file_content` | - |  |
| Upload file | `upload` | - |  |
