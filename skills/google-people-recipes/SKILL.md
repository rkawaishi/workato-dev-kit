# Google People recipes

Provider value to use in every step: `google_people`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "google_people"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_contact` | New contact | - |
| `updated_contact` | New or updated contact | - |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `copy_other_contacts` | Copy other contacts to my contacts | - |
| `create_contact` | Create contact | - |
| `search_contacts` | Search contacts | yes |
| `search_other_contacts` | Search other contacts | yes |
| `update_contact` | Update contact | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
