# Lookup tables by Workato recipes

Provider value to use in every step: `lookup_table`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "lookup_table"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `add_batch_of_entries` | Add entries | yes |
| `add_entry` | Add entry | - |
| `delete_entries` | Delete multiple entries | yes |
| `delete_entry` | Delete entry | - |
| `get_entries` | Get all entries | yes |
| `get_entry` | Lookup entry | - |
| `search_entries` | Search entries | yes |
| `truncate` | Truncate table | yes |
| `update_entry` | Update entry | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
