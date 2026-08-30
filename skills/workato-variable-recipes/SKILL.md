# Variables by Workato recipes

Provider value to use in every step: `workato_variable`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_variable"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `clear_list` | Clear all items from list | yes |
| `declare_list` | Create list | yes |
| `declare_variable` | Create variable | - |
| `insert_to_list` | Add items to list | - |
| `insert_to_list_batch` | Add items to list | yes |
| `update_variables` | Update variables | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `update_variable` | Update variable | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
