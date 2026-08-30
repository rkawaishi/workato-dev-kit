# SendGrid recipes

Provider value to use in every step: `sendgrid`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "sendgrid"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (2)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `send_email` | Send email | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `add_recipient_to_list` | Add recipient to list | - |
| `create_or_update_recipient` | Create or update recipient | - |
| `search_recipient` | Search recipient | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
