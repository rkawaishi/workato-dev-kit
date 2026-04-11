# Workbot  for  Slack コネクタ

Provider: `slack_bot`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New command (old version) | `bot_command` | - |  [deprecated] |
| New command | `bot_command_v2` | - |  |
| New URL mention | `bot_document_mention` | - |  |
| New dynamic menu event | `dynamic_menu` | - |  |
| New help message trigger | `help_event` | - |  |
| New Shortcut trigger | `message_action` | - |  |
| New event | `new_event` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Open/update or push modal view | `block_kit_modals` | - |  |
| Delete message | `delete_message` | - |  |
| Download attachment | `download_attachment` | - |  |
| Return menu options | `generate_menu_options` | - |  |
| Get user info | `get_user_by_email` | - |  |
| Publish App Home view | `open_bot_app_home` | - |  |
| Post dialog | `open_bot_dialog` | - |  |
| Post message | `post_bot_message` | - |  |
| Post notification (old version) | `post_bot_notification` | - |  [deprecated] |
| Post command reply (old version) | `post_bot_reply` | - |  |
| Post command reply | `post_bot_reply_v2` | - |  |
| Update blocks by block id | `update_blocks_by_block_id` | - |  |
| Return menu options | `upload_file` | - |  |
