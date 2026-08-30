# Expensify recipes

Provider value to use in every step: `expensify`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "expensify"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `expense_report_created` | Expense report created | - |


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_expense` | Create expense | - |
| `create_report` | Create expense report | - |
| `get_policy_list` | Get policy list | yes |
| `get_report_status` | Get expense report status | - |
| `manage_employee` | Create/Update employee | - |
| `update_report_status` | Update expense report status | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
