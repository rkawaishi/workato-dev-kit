# BILL コネクタ

Provider: `bill`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New invoice payment received | `new_invoice_payment` | - |  [deprecated] |
| New record | `new_record` | - |  |
| New/updated vendor | `new_updated_Vendor` | - |  [deprecated] |
| New/updated record | `new_updated_record` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add line to invoice | `add_line_item_invoice` | - |  |
| Create customer | `create_customer` | - |  [deprecated] |
| Create invoice | `create_invoice` | - |  [deprecated] |
| Create record | `create_object` | - |  |
| Delete record | `delete_object` | - |  |
| Get Customer by ID | `get_customer_by_id` | - |  [deprecated] |
| Get disbursement data | `get_disbursement_data` | - |  |
| Get Invoice by ID | `get_invoice_by_id` | - |  [deprecated] |
| Get record details by ID | `get_record_details_by_id` | - |  |
| Search customers | `search_customers` | - |  [deprecated] |
| Search items | `search_items` | - |  [deprecated] |
| Search record | `search_record` | Yes |  |
| Send invoice | `send_invoice` | - |  |
| Update record | `update_object` | - |  |
