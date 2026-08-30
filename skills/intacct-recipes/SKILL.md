# Sage Intacct recipes

Provider value to use in every step: `intacct`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "intacct"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (18)

| Internal name | Title | Batch |
|---|---|---|
| `ap_bill_updated` | New/updated AP bill | - |
| `ap_payment_updated` | New/updated AP payment | - |
| `ar_payment_created` | New AR payment | - |
| `contact_created` | New contact | - |
| `contact_updated` | New/updated contact | - |
| `expense_created` | New expense | - |
| `expense_updated` | New/updated expense | - |
| `glaccount_updated` | New/updated GL account | - |
| `invoice_created` | New invoice | - |
| `item_created` | New item | - |
| `item_updated` | New/updated item | - |
| `project_created` | New project | - |
| `project_task_created` | New project task | - |
| `project_task_updated` | New/updated project task | - |
| `project_updated` | New/updated project | - |
| `purchase_order_updated` | New/updated purchase order | - |
| `updated_object` | New/updated object | - |
| `vendor_updated` | New/updated vendor | - |


## Actions (45)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_EEXPENSES` | Create expense | - |
| `create_contact` | Create contact | - |
| `create_customer` | Create customer | - |
| `create_glaccount` | Create GL account | - |
| `create_gltransaction` | Create journal entry with lines | - |
| `create_invoice` | Create single invoice | - |
| `create_item` | Create item | - |
| `create_object` | Create object | - |
| `create_other_receipt` | Create other receipt | - |
| `create_payment` | Create payment | - |
| `create_project` | Create project | - |
| `create_purchase_order` | Create/convert purchase transaction | - |
| `create_recurring_order_entry_transaction` | Create recurring order entry transaction | - |
| `create_recursotransaction` | Create recurring invoice | - |
| `create_statgltransaction` | Create statistical journal entry with lines | - |
| `create_transaction` | Create/convert sales transaction | - |
| `create_vendor_v2` | Create vendor | - |
| `delete_sales_order` | Delete sales order | - |
| `get_custom_relationship_v2` | Get custom relationship values | - |
| `get_expense_by_id` | Get expense by record number | - |
| `get_invoice_items` | Get invoice items | - |
| `get_item_by_id` | Get item by id | - |
| `get_sales_order_by_id` | Get sales order by id | - |
| `link_payment_to_invoices` | Link payment to invoices | - |
| `search_EEXPENSES` | Search expenses | yes |
| `search_ar_terms` | Search AR terms | yes |
| `search_contacts` | Search contacts | yes |
| `search_customers` | Search customers | yes |
| `search_dimensions` | Search dimensions | yes |
| `search_glaccount` | Search GL account | yes |
| `search_gltransactions` | Search journal entries | yes |
| `search_invoices` | Search invoices | yes |
| `search_items` | Search items | yes |
| `search_objects` | Search objects | yes |
| `search_projects` | Search projects | yes |
| `search_purchase_orders` | Search purchasing documents | yes |
| `search_sales_orders` | Search sales documents | yes |
| `update_contact` | Update contact | - |
| `update_customer` | Update customer | - |
| `update_item_component` | Update component of item | - |
| `update_object` | Update object | - |
| `update_project` | Update project | - |
| `update_sales_order_v2` | Update sales order and lines | - |
| `update_vendor_v2` | Update vendor | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `payment_created` | New AR payment | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `create_bill` | Create bill | - |
| `create_sales_order` | Create/convert sales transaction | - |
| `create_vendor` | Create vendor | - |
| `get_custom_relationship` | Get custom relationship values | - |
| `update_sales_order` | Update sales order and lines | - |
| `update_vendor` | Update vendor | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
