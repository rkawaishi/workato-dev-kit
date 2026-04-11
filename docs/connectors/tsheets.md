# TSheets コネクタ

Provider: `tsheets`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New job | `new_jobcode` | - |  |
| New timesheet | `new_timesheet` | - |  |
| New user | `new_user` | - |  |
| New/updated timesheet | `updated_timesheet` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create timesheet | `add_timesheet` | - |  |
| Create user | `add_user` | - |  |
| Delete timesheet | `delete_timesheet` | - |  |
| Edit timesheet | `edit_timesheet` | - |  |
| Edit user | `edit_user` | - |  |
| Get jobcode details by ID | `get_jobcode` | - |  |
| Get payroll report | `get_payroll_report` | Yes |  |
| Get user details by ID/employee number | `get_user` | - |  |
