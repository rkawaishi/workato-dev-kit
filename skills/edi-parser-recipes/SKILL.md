# EDI tools by Workato recipes

Provider value to use in every step: `edi_parser`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "edi_parser"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (2)

| Internal name | Title | Batch |
|---|---|---|
| `generate_edi_v2` | Generate EDI message | - |
| `parse_edi_v2` | Parse EDI message | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `generate_edi` | Generate EDI | - |
| `parse_edi` | Parse EDI | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
