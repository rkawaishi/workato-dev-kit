# Bigtincan recipes

Provider value to use in every step: `bigtincan`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "bigtincan"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_form_submission` | New form submission | - |
| `new_story` | New story | - |


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_story` | Create story | - |
| `delete_story` | Delete story | - |
| `get_form_by_id` | Get form by ID | - |
| `get_form_data_by_id` | Get form data by ID | yes |
| `get_story_by_id` | Get story by ID | - |
| `list_channels` | List channels | yes |
| `list_form_categories` | List form categories | yes |
| `list_form_fields` | List form fields | - |
| `list_forms` | List forms | yes |
| `list_stories` | List stories | yes |
| `update_story` | Update story | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
