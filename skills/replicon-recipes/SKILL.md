# Replicon recipes

Provider value to use in every step: `replicon`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "replicon"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_client` | New client | - |
| `new_invoice_v2` | New or updated invoice ready to sync | - |
| `new_project` | New project | - |
| `new_user` | New user | - |


## Actions (45)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_all_users_to_project` | Assign all users to project | - |
| `add_comanager_to_project` | Assign co-manager to project | - |
| `add_expense_sheet_entry` | Add line item to expense sheet | - |
| `assign_manager_to_project` | Assign manager to project | - |
| `assign_user_to_project` | Assign user to project | - |
| `change_invoice_status_v2` | Update invoice status | - |
| `create_client` | Create client | - |
| `create_expense_sheet` | Create expense sheet | - |
| `create_project` | Create project | - |
| `create_project_task` | Create project task | - |
| `create_timesheet` | Create timesheet | - |
| `create_user` | Create user | - |
| `get_all_project_task` | Get all tasks for a project | yes |
| `get_client_details` | Get client details | - |
| `get_cost_amount_series` | Get project cost amount details | - |
| `get_expensable_projects_by_expense_sheet` | Get expensable projects | yes |
| `get_invoice_details_v2` | Get invoice details by URI | - |
| `get_invoice_items_details_v2` | Get invoice item details by URI | - |
| `get_project_details` | Get project details | - |
| `get_project_team_members` | Get list of project team members | yes |
| `get_task_assignments_for_resource` | Get task assignments for resource | yes |
| `get_user_details` | Get user details | - |
| `list_clients` | Get list of clients | yes |
| `list_project_leaders` | Get all eligible project leaders | yes |
| `list_projects` | Get list of projects | yes |
| `list_users` | Get list of users | yes |
| `payroll_details` | Get payroll details | yes |
| `search_clients` | Search clients | yes |
| `search_program` | Search programs | yes |
| `search_projects` | Search projects | yes |
| `search_users` | Search users | yes |
| `submit_expense_sheet` | Submit expense sheet | - |
| `update_client` | Update client | - |
| `update_invoice_dates` | Update payment due date and issue date | - |
| `update_invoice_description` | Update invoice description | - |
| `update_invoice_sync_status` | Update invoice sync status | - |
| `update_project` | Update project | - |
| `update_project_client` | Update project client | - |
| `update_project_end_date` | Update project end date | - |
| `update_project_fixed_bid_rate` | Update project fixed bid rate | - |
| `update_project_name` | Update project name | - |
| `update_project_program` | Update project program | - |
| `update_project_status` | Update project status | - |
| `update_user` | Update user | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `get_invoice` | New invoice | - |
| `new_invoice` | New invoice ready to sync | - |
| `updated_timesheet` | Updated timesheet | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `change_invoice_status` | Update invoice status | - |
| `get_invoice_billing_items` | Get invoice billing items - V1 | - |
| `get_invoice_details` | Get invoice details by URI (deprecated) | - |
| `update_invoice_due_date` | Update invoice due date - V1 | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
