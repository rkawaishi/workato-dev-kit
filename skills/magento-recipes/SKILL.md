# Magento 2 recipes

Provider value to use in every step: `magento`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "magento"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `new_customer` | New customer | - |
| `new_invoice` | New invoice | - |
| `new_or_updated_customer` | New or updated customer | - |
| `new_or_updated_product` | New or updated product | - |
| `new_product` | New product | - |
| `new_purchase_order` | New purchase order | - |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_customer` | Create customer | - |
| `create_or_update_product` | Create or update product | - |
| `get_customer_by_ID` | Get customer by ID | - |
| `get_order_by_ID` | Get order by ID | - |
| `search_customer` | Search customer | yes |
| `search_order` | Search order | yes |
| `search_product` | Search product | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
