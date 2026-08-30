# Workbot for Microsoft Teams Old recipes

Provider value to use in every step: `skype_bot`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "skype_bot"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `bot_command` | New command | - |


## Actions (2)

| Internal name | Title | Batch |
|---|---|---|
| `post_bot_notification` | Post notification | - |
| `post_bot_reply` | Post command reply | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
