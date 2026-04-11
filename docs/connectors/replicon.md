# Replicon コネクタ

Provider: `replicon`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New invoice | `get_invoice` | - |  [deprecated] |
| New client | `new_client` | - |  |
| New invoice ready to sync | `new_invoice` | - |  [deprecated] |
| New or updated invoice ready to sync | `new_invoice_v2` | - |  |
| New project | `new_project` | - |  |
| New user | `new_user` | - |  |
| Updated timesheet | `updated_timesheet` | - |  [deprecated] |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Assign all users to project | `add_all_users_to_project` | - |  |
| Assign co-manager to project | `add_comanager_to_project` | - |  |
| Add line item to expense sheet | `add_expense_sheet_entry` | - |  |
| Assign manager to project | `assign_manager_to_project` | - |  |
| Assign user to project | `assign_user_to_project` | - |  |
| Update invoice status | `change_invoice_status` | - |  [deprecated] |
| Update invoice status | `change_invoice_status_v2` | - |  |
| Create client | `create_client` | - |  |
| Create expense sheet | `create_expense_sheet` | - |  |
| Create project | `create_project` | - |  |
| Create project task | `create_project_task` | - |  |
| Create timesheet | `create_timesheet` | - |  |
| Create user | `create_user` | - |  |
| Get all tasks for a project | `get_all_project_task` | Yes |  |
| Get client details | `get_client_details` | - |  |
| Get project cost amount details | `get_cost_amount_series` | - |  |
| Get expensable projects | `get_expensable_projects_by_expense_sheet` | Yes |  |
| Get invoice billing items - V1 | `get_invoice_billing_items` | - |  [deprecated] |
| Get invoice details by URI (deprecated) | `get_invoice_details` | - |  [deprecated] |
| Get invoice details by URI | `get_invoice_details_v2` | - |  |
| Get invoice item details by URI | `get_invoice_items_details_v2` | - |  |
| Get project details | `get_project_details` | - |  |
| Get list of project team members | `get_project_team_members` | Yes |  |
| Get task assignments for resource | `get_task_assignments_for_resource` | Yes |  |
| Get user details | `get_user_details` | - |  |
| Get list of clients | `list_clients` | Yes |  |
| Get all eligible project leaders | `list_project_leaders` | Yes |  |
| Get list of projects | `list_projects` | Yes |  |
| Get list of users | `list_users` | Yes |  |
| Get payroll details | `payroll_details` | Yes |  |
| Search clients | `search_clients` | Yes |  |
| Search programs | `search_program` | Yes |  |
| Search projects | `search_projects` | Yes |  |
| Search users | `search_users` | Yes |  |
| Submit expense sheet | `submit_expense_sheet` | - |  |
| Update client | `update_client` | - |  |
| Update payment due date and issue date | `update_invoice_dates` | - |  |
| Update invoice description | `update_invoice_description` | - |  |
| Update invoice due date - V1 | `update_invoice_due_date` | - |  [deprecated] |
| Update invoice sync status | `update_invoice_sync_status` | - |  |
| Update project | `update_project` | - |  |
| Update project client | `update_project_client` | - |  |
| Update project end date | `update_project_end_date` | - |  |
| Update project fixed bid rate | `update_project_fixed_bid_rate` | - |  |
| Update project name | `update_project_name` | - |  |
| Update project program | `update_project_program` | - |  |
| Update project status | `update_project_status` | - |  |
| Update user | `update_user` | - |  |
