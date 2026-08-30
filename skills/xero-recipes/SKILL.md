# Xero recipes

Provider value to use in every step: `xero`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "xero"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (10)

| Internal name | Title | Batch |
|---|---|---|
| `new_or_updated_credit_note` | New/updated credit note | - |
| `new_or_updated_item` | New/updated item | - |
| `new_or_updated_overpayment` | New/updated overpayment | - |
| `new_or_updated_prepayment` | New/updated prepayment | - |
| `updated_account` | New/updated account | - |
| `updated_bill` | New/updated bill | - |
| `updated_contact` | New/updated contact | - |
| `updated_employee` | New/updated employee | - |
| `updated_invoice` | New/updated invoice | - |
| `updated_payment` | New/updated payment | - |


## Actions (48)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_invoice_line_item` | Upsert line item to bill or invoice | - |
| `add_person_to_contact` | Add person(s) to contact | - |
| `add_timesheet` | Create timesheet with 1 line item | - |
| `create_bank_transaction` | Create bank transaction | - |
| `create_bill` | Create bill with 1 line item | - |
| `create_bill_with_multiple_line_items` | Create bill with multiple line items | - |
| `create_contact` | Create contact | - |
| `create_credit_note` | Create credit note with line items | - |
| `create_employee` | Create employee (US) | - |
| `create_employee_au` | Create employee (AU) | - |
| `create_invoice` | Create invoice with 1 line item | - |
| `create_invoice_with_line_item` | Create invoice with line items | - |
| `create_item` | Create item | - |
| `create_manual_journal` | Create manual journal with line items | - |
| `create_overpayment` | Create overpayment | - |
| `create_payment` | Create invoice payment | - |
| `create_prepayment` | Create prepayment | - |
| `create_purchase_order` | Create purchase order with line items | - |
| `get_contact_by_id` | Get contact details | - |
| `get_invoice_by_id` | Get bill or invoice details | - |
| `get_invoice_url` | Get online invoice URL | - |
| `get_manual_journal_by_id` | Get manual journal by ID | - |
| `get_payment_by_id` | Get payment | - |
| `get_purchase_order_by_id` | Get purchase order | - |
| `list_accounts` | List accounts | yes |
| `list_connections` | List connections | - |
| `list_currencies` | List currencies | yes |
| `list_organisations` | List organisations | - |
| `list_tax_rates` | List tax rates | yes |
| `search_accounts` | Search accounts | yes |
| `search_bank_transactions` | Search bank transactions | yes |
| `search_contacts` | Search contacts | yes |
| `search_credit_note` | Search credit notes | yes |
| `search_invoices` | Search bills or invoices | yes |
| `search_item` | Search items | - |
| `search_manual_journals` | Search manual journals | yes |
| `search_overpayment` | Search overpayments | yes |
| `search_payments` | Search payments | yes |
| `search_prepayment` | Search prepayments | yes |
| `search_purchase_order` | Search purchase orders | yes |
| `update_contact` | Upsert contact | - |
| `update_invoice` | Update bill or invoice header details | - |
| `update_invoice_with_line_items` | Update bill or invoice with line items | - |
| `update_item` | Update item | - |
| `update_manual_journal` | Update manual journal and line items | - |
| `upload_attachment` | Upload attachment | - |
| `void_payment` | Void payment | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `search_contact` | Search contact | - |
| `update_invoice_status` | Update invoice status | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
