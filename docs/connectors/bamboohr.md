# BambooHR コネクタ

Provider: `bamboohr`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New employee | `new_employee` | - |  |
| New employee | `new_employee_webhook` | - |  |
| Schedule custom employee report | `schedule_custom_report` | Yes |  |
| New/updated employee | `updated_employee` | - |  |
| New/updated employee | `updated_employee_webhook` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create employee | `create_employee` | - |  |
| Create/update time off request | `create_or_update_time_off_request` | - |  |
| Create table record of employee | `create_table_record` | - |  |
| Delete table record | `delete_table_record` | - |  |
| Get company employee report by ID | `get_company_report` | - |  |
| Get employee details by ID | `get_employee_by_id` | - |  |
| Get table records of employee | `get_table_records` | Yes |  |
| List employees in directory | `list_employees_in_directory` | Yes |  |
| List time off requests | `list_time_off_requests` | Yes |  |
| Create custom employee report | `request_custom_report` | Yes |  |
| Update employee | `update_employee` | - |  |
| Update table record of employee | `update_table_record` | - |  |
| Update time off request status | `update_time_off_request_status` | - |  |
