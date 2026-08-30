# Slack secondary recipes

Provider value to use in every step: `slack_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "slack_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `button_action` | Button click | - |
| `new_event` | New event | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `archive_conversation` | Archive conversation | - |
| `create_conversation` | Create conversation (channels and groups) | - |
| `get_user_by_email` | Get user info | - |
| `invite_user_to_conversation` | Invite users to conversation | - |
| `post_button_action_reply` | Respond to button click | - |
| `post_message_to_channel` | Post message | - |
| `set_conversation_purpose` | Set conversation purpose | - |
| `set_conversation_topic` | Set conversation topic | - |
| `unarchive_conversation` | Unarchive conversation | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `archive_channel` | Archive channel | - |
| `create_channel` | Create channel | - |
| `invite_user_to_channel` | Invite users to channel | - |
| `invite_user_to_group` | Invite users to group | - |
| `set_channel_purpose` | Set channel purpose | - |
| `set_channel_topic` | Set channel topic | - |
| `unarchive_channel` | Unarchive channel | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
