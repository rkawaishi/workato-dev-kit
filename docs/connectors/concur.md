# SAP Concur コネクタ

Provider: `concur`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New expense report | `new_expense_report` | - |  [deprecated] |
| New expense report submission | `new_expense_report_submission` | - |  [deprecated] |
| New expense report submission | `new_expense_report_submission_v3` | - |  |
| New expense report | `new_expense_report_v3` | - |  [deprecated] |
| New expense report | `new_expense_report_v3_new` | - |  |
| New or updated invoice | `new_or_updated_invoice` | - |  |
| New or updated user | `new_or_updated_user` | - |  |
| New or updated expense report | `updated_expense_report` | - |  [deprecated] |
| New or updated expense report | `updated_expense_report_v3` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Upload receipt image | `add_receipt_image` | - |  [deprecated] |
| Upload receipt image | `add_receipt_image_v3` | - |  |
| Create list item | `create_list_item` | - |  [deprecated] |
| Create list item | `create_list_item_v4` | - |  |
| Create user | `create_user_v4` | - |  |
| Create users | `create_user_v4_batch` | Yes |  |
| Create vendors | `create_vendor` | Yes |  |
| Delete list item | `delete_list_item` | - |  [deprecated] |
| Delete list item | `delete_list_item_v4` | - |  |
| Retrieve children of list item | `fetch_children_of_list_item` | - |  |
| Get all attendee types | `get_all_attendee_types` | Yes |  |
| Get all expense group configurations | `get_all_expense_group_configurations` | Yes |  |
| Get all expense types | `get_all_expense_types` | Yes |  |
| Get all lists | `get_all_list_v3` | - |  [deprecated] |
| Get all lists | `get_all_lists` | Yes |  |
| Get all payment types | `get_all_payment_types` | Yes |  |
| Search users | `get_all_users` | Yes |  |
| Get entry image URL | `get_entry_image_url` | - |  |
| Get itemizations of specific expense | `get_expense_itemizations` | - |  |
| Get expense report details | `get_expense_report_details_v2` | - |  [deprecated] |
| Get expense report details | `get_expense_report_details_v4` | - |  |
| Get all list item | `get_first_level_list_items_v4` | Yes |  |
| Get invoice details | `get_invoice_by_id` | - |  |
| Get list items | `get_linked_list_items` | - |  [deprecated] |
| Get user | `get_user_profile` | - |  |
| Get user provisioning status details | `get_user_provisioning_detail` | - |  |
| Submit expense report through a workflow | `post_workflow_action` | - |  |
| Search expense reports | `search_expense_reports` | Yes |  |
| Search vendors | `search_vendors` | Yes |  |
| Update user | `update_user_v4` | - |  |
| Update users | `update_user_v4_batch` | Yes |  |
| Update vendors | `update_vendor` | Yes |  |
