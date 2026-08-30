# Deputy recipes

Provider value to use in every step: `deputy`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "deputy"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_employee` | New employee | - |
| `new_leave` | New leave | - |
| `new_timesheet` | New timesheet | - |


## Actions (13)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `associate` | Associate employee | - |
| `create_employee` | Create employee | - |
| `create_object` | Create resource | - |
| `create_salesdata` | Create sales data | - |
| `create_task` | Create task | - |
| `disassociate` | Unassociate employee | - |
| `get_object` | Get resource | - |
| `search_employees` | Search employees | yes |
| `search_object` | Search resources | yes |
| `search_operational_unit` | Search operational unit | yes |
| `update_employee` | Update employee | - |
| `update_object` | Update resource | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
