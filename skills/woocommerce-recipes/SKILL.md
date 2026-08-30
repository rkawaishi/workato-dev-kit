# WooCommerce recipes

Provider value to use in every step: `woocommerce`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "woocommerce"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (5)

| Internal name | Title | Batch |
|---|---|---|
| `new_customer` | New customer | - |
| `new_order` | New order | - |
| `new_product` | New product | - |
| `new_subscriber` | New subscriber | - |
| `updated_order` | Updated order | - |


## Actions (4)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_product` | Create product | - |
| `search_customers` | Search customers | yes |
| `search_products` | Search products | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
