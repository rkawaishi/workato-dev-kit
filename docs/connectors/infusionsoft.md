# Infusionsoft コネクタ

Provider: `infusionsoft`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New company | `new_company` | - |  |
| New contact | `new_contact` | - |  |
| New order | `new_invoice` | - |  |
| New opportunity | `new_opportunity` | - |  |
| New payment | `new_payment` | - |  [deprecated] |
| New payment | `new_payment_v2` | - |  |
| New product | `new_product` | - |  [deprecated] |
| New tag assigned to contact | `new_tag_assigned_to_contact` | - |  |
| New/updated contact | `new_updated_contact` | - |  |
| New/updated order | `new_updated_invoice` | - |  |
| New/updated note | `new_updated_note` | - |  |
| New/updated product | `new_updated_product` | - |  |
| Product created | `product_created` | - |  |
| Updated contact | `updated_contact` | - |  |
| Updated order | `updated_invoice` | - |  |
| Updated opportunity | `updated_opportunity` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add line item to Order | `add_line_item_to_order` | - |  |
| Add payment to order | `add_payment_to_invoice` | - |  |
| Add tax to order | `add_tax_to_order` | - |  |
| Assign tag to contact | `assign_tag_to_contact` | - |  |
| Charge an invoice | `charge_invoice` | - |  |
| Create company | `create_company` | - |  |
| Create contact | `create_contact` | - |  |
| Create note | `create_note` | - |  |
| Create opportunity | `create_opportunity` | - |  |
| Create order | `create_order` | - |  |
| Create product | `create_product` | - |  |
| Create Task | `create_task` | - |  |
| Get company details by ID | `get_company` | - |  |
| Get contact details by ID | `get_contact` | - |  |
| Get invoice by ID | `get_invoice` | - |  |
| Get payment plan by Invoice ID | `get_pay_plan` | - |  |
| Get payment by ID | `get_payment_by_id` | - |  |
| Get payments by Invoice ID | `get_payments` | - |  |
| Get product details by ID | `get_product` | - |  |
| Make contact marketable | `make_marketable_contact` | - |  |
| Search companies | `search_companies` | Yes |  |
| Search contacts | `search_contact` | Yes |  |
| Search credit cards | `search_credit_cards` | Yes |  |
| Search invoices | `search_invoices` | Yes |  |
| Search order items | `search_order_items` | Yes |  |
| Search orders | `search_orders` | Yes |  |
| Search products | `search_product` | Yes |  |
| Search tags | `search_tags` | Yes |  |
| Search tags by contact ID | `search_tags_by_contact_id` | Yes |  |
| Search users | `search_user` | Yes |  |
| Update company | `update_company` | - |  |
| Update contact | `update_contact` | - |  |
| Update note | `update_note` | - |  |
| Update opportunity | `update_opportunity` | - |  |
| Update order | `update_order` | - |  |
| Update product | `update_product` | - |  |
