# Lightspeed Commerce コネクタ

Provider: `vend`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New consignment | `new_consignment` | - |  |
| New/updated customer | `new_customer` | - |  |
| New inventory record | `new_inventory_record` | - |  |
| New/updated product | `new_product` | - |  |
| New sale | `new_sales` | - |  |
| New/updated consignment | `updated_consignment` | - |  |
| New/updated inventory record | `updated_inventory_record` | - |  |
| New/updated sale | `updated_sale` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add payment to register sale | `add_payment_to_register_sale` | - |  |
| Create customer | `create_customer` | - |  |
| Create product | `create_product` | - |  |
| Create register sale | `create_register_sale` | - |  |
| Get customer details by ID | `get_customer_by_id` | - |  |
| Get register sale details by ID | `get_register_sale_by_id` | - |  [deprecated] |
| Get sale details by ID | `get_sale_details` | - |  |
| Search customers | `search_customers` | Yes |  |
| Search product | `search_product` | Yes |  |
| Update customer | `update_customer` | - |  |
| Update product | `update_product` | - |  |
