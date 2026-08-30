# Revel Systems recipes

Provider value to use in every step: `revel_systems`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "revel_systems"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `new_customer` | New customer | - |
| `new_purchaseorder` | New purchase order | - |
| `new_sales` | New sales | - |
| `new_timesheetentry` | New time sheet entry | - |
| `updated_customer` | New/updated customer | - |
| `updated_sales` | New/updated sales | - |


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_customer` | Create customer | - |
| `create_employee` | Create employee | - |
| `get_customer_by_id` | Get customer by ID | - |
| `update_customer` | Update customer | - |
| `update_employee` | Update employee | - |
| `update_product` | Update product | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
