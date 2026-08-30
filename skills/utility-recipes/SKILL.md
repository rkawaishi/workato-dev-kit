# Utilities recipes

Provider value to use in every step: `utility`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "utility"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (2)

| Internal name | Title | Batch |
|---|---|---|
| `format_name` | Merge name components | - |
| `log_message` | Log message | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `column_chart` | Generate column chart | - |
| `create_csv_lines` | Compose CSV | - |
| `create_list` | Create list | - |
| `parse_csv` | Parse CSV | - |
| `parse_json` | Parse JSON document | - |
| `parse_xml` | Parse XML document | - |
| `pie_chart` | Generate pie chart | - |
| `read_file` | Download file from URL | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
