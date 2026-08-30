# FreshBooks recipes

Provider value to use in every step: `fresh_books`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "fresh_books"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_or_updated_client` | New/updated client | - |
| `new_or_updated_estimate` | New/updated estimate | - |
| `new_or_updated_invoice` | New/updated invoice | - |
| `new_or_updated_payment` | New/updated payment | - |


## Actions (11)

| Internal name | Title | Batch |
|---|---|---|
| `add_line_item_to_invoice` | Add line item to invoice | - |
| `create_client` | Create client | - |
| `create_expense` | Create expense | - |
| `create_invoice` | Create invoice | - |
| `create_item` | Create item | - |
| `get_client_by_id` | Get client details by ID | - |
| `get_item_by_id` | Get item details by ID | - |
| `lookup_staff_member` | Search staff members | - |
| `make_payment` | Make payment | - |
| `search_client` | Search a client by email/username | - |
| `update_client` | Update client | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
