# eTapestry recipes

Provider value to use in every step: `etapestry`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "etapestry"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `account_created` | Account created | - |
| `account_updated` | Account updated | - |


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `add_account` | Add account | - |
| `add_contact` | Add contact | - |
| `add_gift` | Add gift | - |
| `search_accounts` | Search accounts | yes |
| `update_account` | Update account | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
