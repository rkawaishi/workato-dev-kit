# Sage Intacct コネクタ

Provider: `intacct`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New/updated AP bill | `ap_bill_updated` | - |  |
| New/updated AP payment | `ap_payment_updated` | - |  |
| New AR payment | `ar_payment_created` | - |  |
| New contact | `contact_created` | - |  |
| New/updated contact | `contact_updated` | - |  |
| New expense | `expense_created` | - |  |
| New/updated expense | `expense_updated` | - |  |
| New/updated GL account | `glaccount_updated` | - |  |
| New invoice | `invoice_created` | - |  |
| New item | `item_created` | - |  |
| New/updated item | `item_updated` | - |  |
| New AR payment | `payment_created` | - |  [deprecated] |
| New project | `project_created` | - |  |
| New project task | `project_task_created` | - |  |
| New/updated project task | `project_task_updated` | - |  |
| New/updated project | `project_updated` | - |  |
| New/updated purchase order | `purchase_order_updated` | - |  |
| New/updated object | `updated_object` | - |  |
| New/updated vendor | `vendor_updated` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create expense | `create_EEXPENSES` | - |  |
| Create bill | `create_bill` | - |  [deprecated] |
| Create contact | `create_contact` | - |  |
| Create customer | `create_customer` | - |  |
| Create GL account | `create_glaccount` | - |  |
| Create journal entry with lines | `create_gltransaction` | - |  |
| Create single invoice | `create_invoice` | - |  |
| Create item | `create_item` | - |  |
| Create object | `create_object` | - |  |
| Create other receipt | `create_other_receipt` | - |  |
| Create payment | `create_payment` | - |  |
| Create project | `create_project` | - |  |
| Create/convert purchase transaction | `create_purchase_order` | - |  |
| Create recurring order entry transaction | `create_recurring_order_entry_transaction` | - |  |
| Create recurring invoice | `create_recursotransaction` | - |  |
| Create/convert sales transaction | `create_sales_order` | - |  [deprecated] |
| Create statistical journal entry with lines | `create_statgltransaction` | - |  |
| Create/convert sales transaction | `create_transaction` | - |  |
| Create vendor | `create_vendor` | - |  [deprecated] |
| Create vendor | `create_vendor_v2` | - |  |
| Delete sales order | `delete_sales_order` | - |  |
| Get custom relationship values | `get_custom_relationship` | - |  [deprecated] |
| Get custom relationship values | `get_custom_relationship_v2` | - |  |
| Get expense by record number | `get_expense_by_id` | - |  |
| Get invoice items | `get_invoice_items` | - |  |
| Get item by id | `get_item_by_id` | - |  |
| Get sales order by id | `get_sales_order_by_id` | - |  |
| Link payment to invoices | `link_payment_to_invoices` | - |  |
| Search expenses | `search_EEXPENSES` | Yes |  |
| Search AR terms | `search_ar_terms` | Yes |  |
| Search contacts | `search_contacts` | Yes |  |
| Search customers | `search_customers` | Yes |  |
| Search dimensions | `search_dimensions` | Yes |  |
| Search GL account | `search_glaccount` | Yes |  |
| Search journal entries | `search_gltransactions` | Yes |  |
| Search invoices | `search_invoices` | Yes |  |
| Search items | `search_items` | Yes |  |
| Search objects | `search_objects` | Yes |  |
| Search projects | `search_projects` | Yes |  |
| Search purchasing documents | `search_purchase_orders` | Yes |  |
| Search sales documents | `search_sales_orders` | Yes |  |
| Update contact | `update_contact` | - |  |
| Update customer | `update_customer` | - |  |
| Update component of item | `update_item_component` | - |  |
| Update object | `update_object` | - |  |
| Update project | `update_project` | - |  |
| Update sales order and lines | `update_sales_order` | - |  [deprecated] |
| Update sales order and lines | `update_sales_order_v2` | - |  |
| Update vendor | `update_vendor` | - |  [deprecated] |
| Update vendor | `update_vendor_v2` | - |  |
