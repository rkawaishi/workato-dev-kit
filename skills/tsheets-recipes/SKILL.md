# TSheets recipes

Provider value to use in every step: `tsheets`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "tsheets"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_jobcode` | New job | - |
| `new_timesheet` | New timesheet | - |
| `new_user` | New user | - |
| `updated_timesheet` | New/updated timesheet | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_timesheet` | Create timesheet | - |
| `add_user` | Create user | - |
| `delete_timesheet` | Delete timesheet | - |
| `edit_timesheet` | Edit timesheet | - |
| `edit_user` | Edit user | - |
| `get_jobcode` | Get jobcode details by ID | - |
| `get_payroll_report` | Get payroll report | yes |
| `get_user` | Get user details by ID/employee number | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
