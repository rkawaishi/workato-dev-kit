# Outreach recipes

Provider value to use in every step: `outreach`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "outreach"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `completed_sequence_task` | Completed sequence task | - |
| `new_or_updated_record` | New or updated record | - |
| `new_record` | New record | - |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_prospect_to_sequence` | Add a prospect to sequence | - |
| `add_template_to_sequence_step` | Add a template to sequence step | - |
| `create_object` | Create record | - |
| `get_object` | Get record by ID | - |
| `get_steps_in_sequence` | Get steps in a sequence | yes |
| `search_object` | Search records | yes |
| `update_object` | Update record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
