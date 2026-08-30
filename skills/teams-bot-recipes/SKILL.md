# Workbot for Microsoft Teams recipes

Provider value to use in every step: `teams_bot`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "teams_bot"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `bot_command` | New command | - |
| `help_event` | New help message trigger | - |
| `new_event` | New real-time event | - |
| `new_message_event` | New message | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `delete_message` | Delete message | - |
| `get_user_by_principal_name` | Get user info by principal name or user ID | - |
| `invoke_response` | Response to real-time event | - |
| `post_blocks_message` | Post message | - |
| `post_blocks_reply_message` | Post reply | - |
| `post_bot_message` | Post message (old version) | - |
| `post_bot_reply` | Post reply (old version) | - |
| `post_simple_message` | Post simple message | - |
| `post_simple_reply` | Post simple reply | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `tab_opened` | Tab opened | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `render_tab` | Show tab using Adaptive Cards | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
