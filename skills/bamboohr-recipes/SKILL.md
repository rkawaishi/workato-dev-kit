# BambooHR recipes

Provider value to use in every step: `bamboohr`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "bamboohr"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (5)

| Internal name | Title | Batch |
|---|---|---|
| `new_employee` | New employee | - |
| `new_employee_webhook` | New employee | - |
| `schedule_custom_report` | Schedule custom employee report | yes |
| `updated_employee` | New/updated employee | - |
| `updated_employee_webhook` | New/updated employee | - |


## Actions (14)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_employee` | Create employee | - |
| `create_or_update_time_off_request` | Create/update time off request | - |
| `create_table_record` | Create table record of employee | - |
| `delete_table_record` | Delete table record | - |
| `get_company_report` | Get company employee report by ID | - |
| `get_employee_by_id` | Get employee details by ID | - |
| `get_table_records` | Get table records of employee | yes |
| `list_employees_in_directory` | List employees in directory | yes |
| `list_time_off_requests` | List time off requests | yes |
| `request_custom_report` | Create custom employee report | yes |
| `update_employee` | Update employee | - |
| `update_table_record` | Update table record of employee | - |
| `update_time_off_request_status` | Update time off request status | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
