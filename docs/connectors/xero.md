# Xero コネクタ

Provider: `xero`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New/updated credit note | `new_or_updated_credit_note` | - |  |
| New/updated item | `new_or_updated_item` | - |  |
| New/updated overpayment | `new_or_updated_overpayment` | - |  |
| New/updated prepayment | `new_or_updated_prepayment` | - |  |
| New/updated account | `updated_account` | - |  |
| New/updated bill | `updated_bill` | - |  |
| New/updated contact | `updated_contact` | - |  |
| New/updated employee | `updated_employee` | - |  |
| New/updated invoice | `updated_invoice` | - |  |
| New/updated payment | `updated_payment` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Upsert line item to bill or invoice | `add_invoice_line_item` | - |  |
| Add person(s) to contact | `add_person_to_contact` | - |  |
| Create timesheet with 1 line item | `add_timesheet` | - |  |
| Create bank transaction | `create_bank_transaction` | - |  |
| Create bill with 1 line item | `create_bill` | - |  |
| Create bill with multiple line items | `create_bill_with_multiple_line_items` | - |  |
| Create contact | `create_contact` | - |  |
| Create credit note with line items | `create_credit_note` | - |  |
| Create employee (US) | `create_employee` | - |  |
| Create employee (AU) | `create_employee_au` | - |  |
| Create invoice with 1 line item | `create_invoice` | - |  |
| Create invoice with line items | `create_invoice_with_line_item` | - |  |
| Create item | `create_item` | - |  |
| Create manual journal with line items | `create_manual_journal` | - |  |
| Create overpayment | `create_overpayment` | - |  |
| Create invoice payment | `create_payment` | - |  |
| Create prepayment | `create_prepayment` | - |  |
| Create purchase order with line items | `create_purchase_order` | - |  |
| Get contact details | `get_contact_by_id` | - |  |
| Get bill or invoice details | `get_invoice_by_id` | - |  |
| Get online invoice URL | `get_invoice_url` | - |  |
| Get manual journal by ID | `get_manual_journal_by_id` | - |  |
| Get payment | `get_payment_by_id` | - |  |
| Get purchase order | `get_purchase_order_by_id` | - |  |
| List accounts | `list_accounts` | Yes |  |
| List connections | `list_connections` | - |  |
| List currencies | `list_currencies` | Yes |  |
| List organisations | `list_organisations` | - |  |
| List tax rates | `list_tax_rates` | Yes |  |
| Search accounts | `search_accounts` | Yes |  |
| Search bank transactions | `search_bank_transactions` | Yes |  |
| Search contact | `search_contact` | - |  [deprecated] |
| Search contacts | `search_contacts` | Yes |  |
| Search credit notes | `search_credit_note` | Yes |  |
| Search bills or invoices | `search_invoices` | Yes |  |
| Search items | `search_item` | - |  |
| Search manual journals | `search_manual_journals` | Yes |  |
| Search overpayments | `search_overpayment` | Yes |  |
| Search payments | `search_payments` | Yes |  |
| Search prepayments | `search_prepayment` | Yes |  |
| Search purchase orders | `search_purchase_order` | Yes |  |
| Upsert contact | `update_contact` | - |  |
| Update bill or invoice header details | `update_invoice` | - |  |
| Update invoice status | `update_invoice_status` | - |  [deprecated] |
| Update bill or invoice with line items | `update_invoice_with_line_items` | - |  |
| Update item | `update_item` | - |  |
| Update manual journal and line items | `update_manual_journal` | - |  |
| Upload attachment | `upload_attachment` | - |  |
| Void payment | `void_payment` | - |  |
