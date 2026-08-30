# QuickBooks Online recipes

Provider value to use in every step: `quickbooks`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "quickbooks"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (29)

| Internal name | Title | Batch |
|---|---|---|
| `deleted_bill` | Deleted bill | - |
| `deleted_item` | Deleted item | - |
| `new_account` | New account | - |
| `new_bank_deposit` | New bank deposit | - |
| `new_bill` | New bill | - |
| `new_bill_payment` | New bill payment | - |
| `new_credit_notes` | New credit notes | - |
| `new_customer` | New customer | - |
| `new_employee` | New employee | - |
| `new_estimate` | New estimate | - |
| `new_invoice` | New invoice | - |
| `new_item` | New item | - |
| `new_payment` | New payment | - |
| `new_purchase` | New purchase | - |
| `new_sales_receipt` | New sales receipt | - |
| `new_updated_account` | New/updated account | - |
| `new_updated_bill` | New/updated bill | - |
| `new_updated_tax_code` | New/updated tax code | - |
| `new_updated_tax_rate` | New/updated tax rate | - |
| `new_vendor` | New vendor | - |
| `updated_bill` | Updated bill | - |
| `updated_credit_notes` | Updated credit notes | - |
| `updated_customer` | Updated customer | - |
| `updated_employee` | Updated employee | - |
| `updated_estimate` | Updated estimate | - |
| `updated_invoice` | Updated invoice | - |
| `updated_item` | Updated item | - |
| `updated_purchase` | Updated purchase | - |
| `updated_vendor` | Updated vendor | - |


## Actions (84)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_line_item_credit_memo` | Add line to credit memo | - |
| `add_line_item_estimate` | Add line to estimate | - |
| `add_line_item_invoice` | Add line to invoice | - |
| `add_line_item_sales_receipt` | Add line to sales receipt | - |
| `create_account` | Create G/L account | - |
| `create_bill_payment` | Create bill payment | - |
| `create_bill_v2` | Create bill | - |
| `create_cheque` | Create check / cheque | - |
| `create_class` | Create class | - |
| `create_credit_card_credit` | Create credit card credit | - |
| `create_credit_memo_v2` | Create credit memo | - |
| `create_customer` | Create customer | - |
| `create_deposit` | Create bank deposit | - |
| `create_employee` | Create employee | - |
| `create_estimate_v2` | Create estimate | - |
| `create_expense` | Create expense | - |
| `create_invoice_v3` | Create invoice | - |
| `create_item` | Create item (product or service) | - |
| `create_journal_entry` | Create journal entry | - |
| `create_journal_entry_v2` | Create journal entry with line items | - |
| `create_payment_v2` | Create payment | - |
| `create_purchase_order_v2` | Create purchase order | - |
| `create_refund_receipt` | Create refund receipt | - |
| `create_sales_receipt_v3` | Create sales receipt | - |
| `create_time_activity` | Create timesheet with 1 line item | - |
| `create_transfer` | Create transfer | - |
| `create_vendor` | Create vendor | - |
| `create_vendor_credit` | Create vendor / supplier credit | - |
| `get_attachments` | Get attachments | yes |
| `get_customer_sales_reports` | Get customer sales reports | - |
| `get_estimate` | Get estimate details | - |
| `get_exchange_rate` | Get exchange rate | - |
| `get_invoice` | Get invoice details | - |
| `get_item_by_id` | Get item (product or service) details | - |
| `get_profit_and_loss` | Get profit and loss | - |
| `get_sales_receipt` | Get sales receipt details | - |
| `get_time_activity` | Get timesheet details | - |
| `lookup_account` | Search G/L accounts | yes |
| `lookup_customer_by_id` | Get customer details | - |
| `lookup_employee` | Search employees | yes |
| `lookup_employee_by_id` | Get employee details | - |
| `lookup_payment_method` | Get payment method details | - |
| `lookup_sales_term` | Get sales term details | - |
| `lookup_vendor_by_id` | Get vendor details | - |
| `search_bills` | Search vendor bills | yes |
| `search_budgets` | Search budgets | yes |
| `search_checks` | Search checks | yes |
| `search_class` | Search classes | yes |
| `search_customer` | Search customers | yes |
| `search_departments` | Search departments | yes |
| `search_deposits` | Search bank deposits | yes |
| `search_estimates` | Search estimates | yes |
| `search_invoice` | Search invoices | yes |
| `search_item` | Search items (products or services) | yes |
| `search_journal_entries` | Search journal entries | yes |
| `search_payment_method` | Search payment methods | yes |
| `search_purchase` | Search purchases | yes |
| `search_sales_receipt` | Search sales receipts | yes |
| `search_tax_code` | Search tax codes | yes |
| `search_term` | Search terms | yes |
| `search_time_activity` | Search timesheets | yes |
| `search_vendors` | Search vendors | yes |
| `send_invoice_via_email` | Send invoice via email | - |
| `update_bill_payment` | Update a bill payment | - |
| `update_bill_v2` | Update bill | - |
| `update_cheque` | Update check / cheque | - |
| `update_credit_card_credit` | Update credit card credit | - |
| `update_credit_memo_v2` | Update credit memo | - |
| `update_customer` | Update customer | - |
| `update_deposit` | Update a bank deposit | - |
| `update_employee` | Update employee | - |
| `update_estimate_v2` | Update estimate | - |
| `update_expense` | Update expense | - |
| `update_invoice_v3` | Update invoice | - |
| `update_item` | Update item (product or service) | - |
| `update_payment_v2` | Update a payment | - |
| `update_purchase_order` | Update purchase order | - |
| `update_refund_receipt` | Update refund receipt | - |
| `update_sales_receipt_v3` | Update sales receipt | - |
| `update_time_activity` | Update timesheet | - |
| `update_transfer` | Update a transfer | - |
| `update_vendor` | Update vendor | - |
| `update_vendor_credit` | Update vendor / supplier credit | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `add_line_item_bill` | Add line to bill | - |
| `add_line_item_purchase` | Add line to purchase | - |
| `add_line_item_purchase_order` | Add line to purchase order | - |
| `create_bank_deposit` | Create bank deposit | - |
| `create_bill` | Create bill with 1 line item | - |
| `create_bill_with_line_items` | Create bill with line items | - |
| `create_credit_memo` | Create credit memo | - |
| `create_estimate` | Create estimate with 1 line item | - |
| `create_invoice` | Create invoice with 1 line item | - |
| `create_invoice_v2` | Create invoice with line items | - |
| `create_payment` | Create payment with 1 line item | - |
| `create_purchase` | Create purchase with 1 line item | - |
| `create_purchase_order` | Create purchase order | - |
| `create_sales_receipt` | Create sales receipt with 1 line item | - |
| `create_sales_receipt_v2` | Create sales receipt with line items | - |
| `lookup_customer` | Search customers | - |
| `update_bank_deposit` | Update bank deposit and line items | - |
| `update_bill` | Update bill and line items | - |
| `update_estimate` | Update estimate header details | - |
| `update_invoice` | Update invoice header details | - |
| `update_invoice_v2` | Update invoice and line items | - |
| `update_sales_receipt` | Update sales receipt header details | - |
| `update_sales_receipt_v2` | Update sales receipt and lines items | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
