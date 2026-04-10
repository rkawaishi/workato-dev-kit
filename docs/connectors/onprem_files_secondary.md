# On-prem files secondary コネクタ

Provider: `onprem_files_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New CSV file in folder | `csv_file_batch` | Yes |  |
| New lines in CSV file | `new_csv_file_batch` | Yes |  |
| New line in CSV file | `new_csv_file_line` | - |  |
| New file in folder | `new_file` | - |  |
| New/updated files and folders | `new_or_changed_file` | - |  [deprecated] |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Append line to CSV file | `add_csv_line` | - |  |
| Append content to file | `append_file_content` | - |  [deprecated] |
| Create folder | `create_folder` | - |  |
| Delete file | `delete_file` | - |  |
| Delete folder | `delete_folder` | - |  |
| Download file | `download_file` | - |  |
| Download file contents | `download_file_contents` | - |  [deprecated] |
| Generate on-prem file URL | `generate_file_url` | - |  |
| List files in folder | `list_files` | Yes |  |
| Move file | `move_file` | - |  |
| Read lines from CSV file | `read_csv_file_lines` | - |  [deprecated] |
| Rename file | `rename_file` | - |  |
| Update line in CSV file | `update_csv_line` | - |  [deprecated] |
| Upload file (Legacy) | `upload_file` | - |  |
| Send file in directory | `upload_file_content` | - |  [deprecated] |
| Upload file | `upload_file_multistep` | - |  |
