# RegOnline® by Lanyon recipes

Provider value to use in every step: `active_reg_online`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "active_reg_online"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `on_new_event` | New event | - |
| `on_new_registration` | New registration | - |
| `on_new_transaction` | New transaction | - |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `lookup_event` | Get event details by ID | - |
| `lookup_registration` | Get registration details by ID | - |
| `lookup_transaction` | Get transaction by ID | - |
| `query_events` | Get list of events | yes |
| `query_registrations` | Get list of registrations | yes |
| `query_transactions` | Get list of transactions | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
