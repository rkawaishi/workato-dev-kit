# BILL recipes

Provider value to use in every step: `bill`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "bill"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_record` | New record | - |
| `new_updated_record` | New/updated record | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_line_item_invoice` | Add line to invoice | - |
| `create_object` | Create record | - |
| `delete_object` | Delete record | - |
| `get_disbursement_data` | Get disbursement data | - |
| `get_record_details_by_id` | Get record details by ID | - |
| `search_record` | Search record | yes |
| `send_invoice` | Send invoice | - |
| `update_object` | Update record | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_invoice_payment` | New invoice payment received | - |
| `new_updated_Vendor` | New/updated vendor | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `create_customer` | Create customer | - |
| `create_invoice` | Create invoice | - |
| `get_customer_by_id` | Get Customer by ID | - |
| `get_invoice_by_id` | Get Invoice by ID | - |
| `search_customers` | Search customers | - |
| `search_items` | Search items | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
