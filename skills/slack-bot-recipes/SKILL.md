# Workbot for Slack recipes

Provider value to use in every step: `slack_bot`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "slack_bot"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `bot_command_v2` | New command | yes |
| `bot_document_mention` | New URL mention | yes |
| `dynamic_menu` | New dynamic menu event | yes |
| `help_event` | New help message trigger | yes |
| `message_action` | New Shortcut trigger | yes |
| `new_event` | New event | yes |


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | yes |
| `block_kit_modals` | Open/update or push modal view | yes |
| `delete_message` | Delete message | yes |
| `download_attachment` | Download attachment | yes |
| `generate_menu_options` | Return menu options | yes |
| `get_user_by_email` | Get user info | yes |
| `open_bot_app_home` | Publish App Home view | yes |
| `open_bot_dialog` | Post dialog | yes |
| `post_bot_message` | Post message | yes |
| `post_bot_reply_v2` | Post command reply | yes |
| `update_blocks_by_block_id` | Update blocks by block id | yes |
| `upload_file` | Upload file | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `bot_command` | New command (old version) | yes |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `post_bot_notification` | Post notification (old version) | yes |
| `post_bot_reply` | Post command reply (old version) | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
