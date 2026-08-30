# Rollbar recipes

Provider value to use in every step: `rollbar`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "rollbar"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_item` | New item | - |
| `new_occurrence` | New occurrence | - |


## Actions (2)

| Internal name | Title | Batch |
|---|---|---|
| `invite_user` | Invite user | - |
| `search_item` | Search item | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
