# Oracle E-Business Suite recipes

Provider value to use in every step: `oracle_ebs`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "oracle_ebs"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_business_event` | New Business Event | - |
| `new_custom_business_event` | New Custom Business Event | - |


## Actions (1)

| Internal name | Title | Batch |
|---|---|---|
| `execute_operation` | Execute PL/SQL operation | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
