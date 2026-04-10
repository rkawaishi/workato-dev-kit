# Stripe コネクタ

Provider: `stripe`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New charge | `new_charge` | - |  |
| New object event | `new_event` | - |  |
| New object | `new_object` | - |  |
| New objects | `new_objects_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create charge | `create_charge` | - |  |
| Create customer | `create_customer` | - |  |
| Create invoice | `create_invoice` | - |  |
| Create invoice item | `create_invoice_item` | - |  |
| Get customer by ID | `get_customer_by_id` | - |  [deprecated] |
| Get object by ID | `get_object_by_id` | - |  |
| List objects | `list_objects` | Yes |  |
| Retreive invoice by ID | `retreive_invoice_by_id` | - |  [deprecated] |
| Search charges | `search_charges` | Yes |  [deprecated] |
| Search invoice items | `search_invoice_items` | Yes |  [deprecated] |
| Update customer | `update_customer` | - |  |
