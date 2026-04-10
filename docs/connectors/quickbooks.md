# QuickBooks Online コネクタ

Provider: `quickbooks`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Deleted bill | `deleted_bill` | - |  |
| Deleted item | `deleted_item` | - |  |
| New account | `new_account` | - |  |
| New bank deposit | `new_bank_deposit` | - |  |
| New bill | `new_bill` | - |  |
| New bill payment | `new_bill_payment` | - |  |
| New credit notes | `new_credit_notes` | - |  |
| New customer | `new_customer` | - |  |
| New employee | `new_employee` | - |  |
| New estimate | `new_estimate` | - |  |
| New invoice | `new_invoice` | - |  |
| New item | `new_item` | - |  |
| New payment | `new_payment` | - |  |
| New purchase | `new_purchase` | - |  |
| New sales receipt | `new_sales_receipt` | - |  |
| New/updated account | `new_updated_account` | - |  |
| New/updated bill | `new_updated_bill` | - |  |
| New/updated tax code | `new_updated_tax_code` | - |  |
| New/updated tax rate | `new_updated_tax_rate` | - |  |
| New vendor | `new_vendor` | - |  |
| Updated bill | `updated_bill` | - |  |
| Updated credit notes | `updated_credit_notes` | - |  |
| Updated customer | `updated_customer` | - |  |
| Updated employee | `updated_employee` | - |  |
| Updated estimate | `updated_estimate` | - |  |
| Updated invoice | `updated_invoice` | - |  |
| Updated item | `updated_item` | - |  |
| Updated purchase | `updated_purchase` | - |  |
| Updated vendor | `updated_vendor` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add line to bill | `add_line_item_bill` | - |  [deprecated] |
| Add line to credit memo | `add_line_item_credit_memo` | - |  |
| Add line to estimate | `add_line_item_estimate` | - |  |
| Add line to invoice | `add_line_item_invoice` | - |  |
| Add line to purchase | `add_line_item_purchase` | - |  [deprecated] |
| Add line to purchase order | `add_line_item_purchase_order` | - |  [deprecated] |
| Add line to sales receipt | `add_line_item_sales_receipt` | - |  |
| Create G/L account | `create_account` | - |  |
| Create bank deposit | `create_bank_deposit` | - |  [deprecated] |
| Create bill with 1 line item | `create_bill` | - |  [deprecated] |
| Create bill payment | `create_bill_payment` | - |  |
| Create bill | `create_bill_v2` | - |  |
| Create bill with line items | `create_bill_with_line_items` | - |  [deprecated] |
| Create check / cheque | `create_cheque` | - |  |
| Create class | `create_class` | - |  |
| Create credit card credit | `create_credit_card_credit` | - |  |
| Create credit memo | `create_credit_memo` | - |  [deprecated] |
| Create credit memo | `create_credit_memo_v2` | - |  |
| Create customer | `create_customer` | - |  |
| Create bank deposit | `create_deposit` | - |  |
| Create employee | `create_employee` | - |  |
| Create estimate with 1 line item | `create_estimate` | - |  [deprecated] |
| Create estimate | `create_estimate_v2` | - |  |
| Create expense | `create_expense` | - |  |
| Create invoice with 1 line item | `create_invoice` | - |  [deprecated] |
| Create invoice with line items | `create_invoice_v2` | - |  [deprecated] |
| Create invoice | `create_invoice_v3` | - |  |
| Create item (product or service) | `create_item` | - |  |
| Create journal entry | `create_journal_entry` | - |  |
| Create journal entry with line items | `create_journal_entry_v2` | - |  |
| Create payment with 1 line item | `create_payment` | - |  [deprecated] |
| Create payment | `create_payment_v2` | - |  |
| Create purchase with 1 line item | `create_purchase` | - |  [deprecated] |
| Create purchase order | `create_purchase_order` | - |  [deprecated] |
| Create purchase order | `create_purchase_order_v2` | - |  |
| Create refund receipt | `create_refund_receipt` | - |  |
| Create sales receipt with 1 line item | `create_sales_receipt` | - |  [deprecated] |
| Create sales receipt with line items | `create_sales_receipt_v2` | - |  [deprecated] |
| Create sales receipt | `create_sales_receipt_v3` | - |  |
| Create timesheet with 1 line item | `create_time_activity` | - |  |
| Create transfer | `create_transfer` | - |  |
| Create vendor | `create_vendor` | - |  |
| Create vendor / supplier credit | `create_vendor_credit` | - |  |
| Get attachments | `get_attachments` | Yes |  |
| Get customer sales reports | `get_customer_sales_reports` | - |  |
| Get estimate details | `get_estimate` | - |  |
| Get exchange rate | `get_exchange_rate` | - |  |
| Get invoice details | `get_invoice` | - |  |
| Get item (product or service) details | `get_item_by_id` | - |  |
| Get profit and loss | `get_profit_and_loss` | - |  |
| Get sales receipt details | `get_sales_receipt` | - |  |
| Get timesheet details | `get_time_activity` | - |  |
| Search G/L accounts | `lookup_account` | Yes |  |
| Search customers | `lookup_customer` | - |  [deprecated] |
| Get customer details | `lookup_customer_by_id` | - |  |
| Search employees | `lookup_employee` | Yes |  |
| Get employee details | `lookup_employee_by_id` | - |  |
| Get payment method details | `lookup_payment_method` | - |  |
| Get sales term details | `lookup_sales_term` | - |  |
| Get vendor details | `lookup_vendor_by_id` | - |  |
| Search vendor bills | `search_bills` | Yes |  |
| Search budgets | `search_budgets` | Yes |  |
| Search checks | `search_checks` | Yes |  |
| Search classes | `search_class` | Yes |  |
| Search customers | `search_customer` | Yes |  |
| Search departments | `search_departments` | Yes |  |
| Search bank deposits | `search_deposits` | Yes |  |
| Search estimates | `search_estimates` | Yes |  |
| Search invoices | `search_invoice` | Yes |  |
| Search items (products or services) | `search_item` | Yes |  |
| Search journal entries | `search_journal_entries` | Yes |  |
| Search payment methods | `search_payment_method` | Yes |  |
| Search purchases | `search_purchase` | Yes |  |
| Search sales receipts | `search_sales_receipt` | Yes |  |
| Search tax codes | `search_tax_code` | Yes |  |
| Search terms | `search_term` | Yes |  |
| Search timesheets | `search_time_activity` | Yes |  |
| Search vendors | `search_vendors` | Yes |  |
| Send invoice via email | `send_invoice_via_email` | - |  |
| Update bank deposit and line items | `update_bank_deposit` | - |  [deprecated] |
| Update bill and line items | `update_bill` | - |  [deprecated] |
| Update a bill payment | `update_bill_payment` | - |  |
| Update bill | `update_bill_v2` | - |  |
| Update check / cheque | `update_cheque` | - |  |
| Update credit card credit | `update_credit_card_credit` | - |  |
| Update credit memo | `update_credit_memo_v2` | - |  |
| Update customer | `update_customer` | - |  |
| Update a bank deposit | `update_deposit` | - |  |
| Update employee | `update_employee` | - |  |
| Update estimate header details | `update_estimate` | - |  [deprecated] |
| Update estimate | `update_estimate_v2` | - |  |
| Update expense | `update_expense` | - |  |
| Update invoice header details | `update_invoice` | - |  [deprecated] |
| Update invoice and line items | `update_invoice_v2` | - |  [deprecated] |
| Update invoice | `update_invoice_v3` | - |  |
| Update item (product or service) | `update_item` | - |  |
| Update a payment | `update_payment_v2` | - |  |
| Update purchase order | `update_purchase_order` | - |  |
| Update refund receipt | `update_refund_receipt` | - |  |
| Update sales receipt header details | `update_sales_receipt` | - |  [deprecated] |
| Update sales receipt and lines items | `update_sales_receipt_v2` | - |  [deprecated] |
| Update sales receipt | `update_sales_receipt_v3` | - |  |
| Update timesheet | `update_time_activity` | - |  |
| Update a transfer | `update_transfer` | - |  |
| Update vendor | `update_vendor` | - |  |
| Update vendor / supplier credit | `update_vendor_credit` | - |  |
