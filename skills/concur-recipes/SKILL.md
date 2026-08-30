# SAP Concur recipes

Provider value to use in every step: `concur`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "concur"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (5)

| Internal name | Title | Batch |
|---|---|---|
| `new_expense_report_submission_v3` | New expense report submission | - |
| `new_expense_report_v3_new` | New expense report | - |
| `new_or_updated_invoice` | New or updated invoice | - |
| `new_or_updated_user` | New or updated user | - |
| `updated_expense_report_v3` | New or updated expense report | - |


## Actions (27)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_receipt_image_v3` | Upload receipt image | - |
| `create_list_item_v4` | Create list item | - |
| `create_user_v4` | Create user | - |
| `create_user_v4_batch` | Create users | yes |
| `create_vendor` | Create vendors | yes |
| `delete_list_item_v4` | Delete list item | - |
| `fetch_children_of_list_item` | Retrieve children of list item | - |
| `get_all_attendee_types` | Get all attendee types | yes |
| `get_all_expense_group_configurations` | Get all expense group configurations | yes |
| `get_all_expense_types` | Get all expense types | yes |
| `get_all_lists` | Get all lists | yes |
| `get_all_payment_types` | Get all payment types | yes |
| `get_all_users` | Search users | yes |
| `get_entry_image_url` | Get entry image URL | - |
| `get_expense_itemizations` | Get itemizations of specific expense | - |
| `get_expense_report_details_v4` | Get expense report details | - |
| `get_first_level_list_items_v4` | Get all list item | yes |
| `get_invoice_by_id` | Get invoice details | - |
| `get_user_profile` | Get user | - |
| `get_user_provisioning_detail` | Get user provisioning status details | - |
| `post_workflow_action` | Submit expense report through a workflow | - |
| `search_expense_reports` | Search expense reports | yes |
| `search_vendors` | Search vendors | yes |
| `update_user_v4` | Update user | - |
| `update_user_v4_batch` | Update users | yes |
| `update_vendor` | Update vendors | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_expense_report` | New expense report | - |
| `new_expense_report_submission` | New expense report submission | - |
| `new_expense_report_v3` | New expense report | - |
| `updated_expense_report` | New or updated expense report | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `add_receipt_image` | Upload receipt image | - |
| `create_list_item` | Create list item | - |
| `delete_list_item` | Delete list item | - |
| `get_all_list_v3` | Get all lists | - |
| `get_expense_report_details_v2` | Get expense report details | - |
| `get_linked_list_items` | Get list items | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
