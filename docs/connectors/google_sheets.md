# Google Sheets コネクタ

Provider: `google_sheets`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New row in sheet in My Drive | `new_polling_spreadsheet_row_v4` | - |  |
| New spreadsheet row added | `new_spreadsheet_row` | - |  [deprecated] |
| New row in sheet in My Drive | `new_spreadsheet_row_v4` | - |  |
| New row in sheet in Team Drive | `team_drive_new_spreadsheet_row_v4` | - |  |
| New/updated row in sheet in Team Drive | `team_drive_updated_spreadsheet_row_v4` | - |  [deprecated] |
| New/updated row in sheet in Team Drive | `team_drive_updated_spreadsheet_row_v4_2` | - |  |
| New/updated row in sheet in My Drive | `updated_polling_spreadsheet_row_v4_2` | - |  |
| New/updated row in sheet in My Drive | `updated_spreadsheet_row_v4` | - |  [deprecated] |
| New/updated row in sheet in My Drive | `updated_spreadsheet_row_v4_2` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add rows in bulk | `add_row_v4_bulk` | Yes |  |
| Add a new row | `add_spreadsheet_row` | - |  [deprecated] |
| Add row | `add_spreadsheet_row_v4` | - |  |
| Get rows | `get_spreadsheet_rows_v4` | Yes |  |
| Search rows by query | `search_spreadsheet_rows` | - |  [deprecated] |
| Search rows using query (old version) | `search_spreadsheet_rows_v3_new` | - |  [deprecated] |
| Search rows | `search_spreadsheet_rows_v4_new` | Yes |  |
| Update rows in bulk | `update_row_v4_bulk` | Yes |  |
| Update row | `update_row_v4_new` | - |  |
| Update a row | `update_spreadsheet_row` | - |  [deprecated] |
| Update row using row ID (Deprecated) | `update_spreadsheet_row_v3_new` | - |  |
