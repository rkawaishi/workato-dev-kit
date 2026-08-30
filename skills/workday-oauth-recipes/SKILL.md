# Workday Web Services recipes

Provider value to use in every step: `workday_oauth`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workday_oauth"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_updated_object` | New/updated business object | - |
| `new_updated_object_batch` | New/updated business object | yes |


## Actions (4)

| Internal name | Title | Batch |
|---|---|---|
| `Get_business_object_details` | Get business object details | yes |
| `Search_business_object` | Search business object | yes |
| `Update_business_object` | Update business object | - |
| `call_operation` | Call operation | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
