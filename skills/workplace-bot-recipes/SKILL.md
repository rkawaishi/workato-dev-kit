# Workbot for Workplace recipes

Provider value to use in every step: `workplace_bot`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workplace_bot"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `bot_command` | New command | - |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `post_bot_attachment` | Post attachment | - |
| `post_bot_message` | Post message | - |
| `post_bot_reply` | Post message | - |
| `post_simple_message` | Post simple message | - |
| `post_simple_reply` | Post simple reply | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
