# Google Contacts recipes

Provider value to use in every step: `google_contacts`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "google_contacts"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (0)

_None._


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_contact` | New contact added | - |
| `updated_contact` | Updated contact | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `create_contact` | Create contact | - |
| `search_contact` | Search contacts | - |
| `update_contact` | Update contact | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
