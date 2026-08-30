# Stripe recipes

Provider value to use in every step: `stripe`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "stripe"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_charge` | New charge | - |
| `new_event` | New object event | - |
| `new_object` | New object | - |
| `new_objects_batch` | New objects | yes |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_charge` | Create charge | - |
| `create_customer` | Create customer | - |
| `create_invoice` | Create invoice | - |
| `create_invoice_item` | Create invoice item | - |
| `get_object_by_id` | Get object by ID | - |
| `list_objects` | List objects | yes |
| `update_customer` | Update customer | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `get_customer_by_id` | Get customer by ID | - |
| `retreive_invoice_by_id` | Retreive invoice by ID | - |
| `search_charges` | Search charges | yes |
| `search_invoice_items` | Search invoice items | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
