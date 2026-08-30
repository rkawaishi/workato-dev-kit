# Maxio recipes

Provider value to use in every step: `chargify`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "chargify"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_customer` | New customer | - |
| `new_event` | New site event | - |
| `new_subscription` | New subscription | - |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_charge` | Create charge | - |
| `create_subscription` | Create subscription | - |
| `get_customer_by_id` | Get customer details by ID | - |
| `get_product_by_id` | Get product details by ID | - |
| `get_subscription_by_id` | Get subscription details by ID | - |
| `get_transaction_by_id` | Get transaction details by ID | - |
| `lookup_customer_by_reference` | Search customer by reference | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
