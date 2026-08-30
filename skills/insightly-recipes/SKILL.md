# Insightly recipes

Provider value to use in every step: `insightly`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "insightly"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (5)

| Internal name | Title | Batch |
|---|---|---|
| `new_contact` | New contact | - |
| `new_organisation` | New organisation | - |
| `updated_contact` | Updated contact | - |
| `updated_opportunity` | Updated opportunity | - |
| `updated_organisation` | Updated organisation | - |


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_note_to_opportunity` | Add note to opportunity | - |
| `create_contact` | Create contact | - |
| `create_event` | Create event | - |
| `create_opportunity` | Create opportunity | - |
| `create_organisation` | Create organisation | - |
| `get_user_by_id` | Get user by ID | - |
| `search_contacts` | Search contacts | yes |
| `search_pipelines` | Search pipelines | yes |
| `search_users` | Search users | yes |
| `update_contact` | Update contact | - |
| `update_opportunity` | Update opportunity | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
