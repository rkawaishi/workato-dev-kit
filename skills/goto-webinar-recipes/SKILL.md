# GotoWebinar recipes

Provider value to use in every step: `goto_webinar`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "goto_webinar"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_webinar_session` | New webinar session | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `get_attendees_from_session` | Get attendees from session | yes |
| `get_webinar_details` | Get webinar details | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
