# Lightspeed Commerce recipes

Provider value to use in every step: `vend`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "vend"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (8)

| Internal name | Title | Batch |
|---|---|---|
| `new_consignment` | New consignment | - |
| `new_customer` | New/updated customer | - |
| `new_inventory_record` | New inventory record | - |
| `new_product` | New/updated product | - |
| `new_sales` | New sale | - |
| `updated_consignment` | New/updated consignment | - |
| `updated_inventory_record` | New/updated inventory record | - |
| `updated_sale` | New/updated sale | - |


## Actions (11)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_payment_to_register_sale` | Add payment to register sale | - |
| `create_customer` | Create customer | - |
| `create_product` | Create product | - |
| `create_register_sale` | Create register sale | - |
| `get_customer_by_id` | Get customer details by ID | - |
| `get_sale_details` | Get sale details by ID | - |
| `search_customers` | Search customers | yes |
| `search_product` | Search product | yes |
| `update_customer` | Update customer | - |
| `update_product` | Update product | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `get_register_sale_by_id` | Get register sale details by ID | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
