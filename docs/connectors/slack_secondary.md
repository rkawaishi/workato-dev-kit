# Slack secondary コネクタ

Provider: `slack_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Button click | `button_action` | - |  |
| New event | `new_event` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Archive channel | `archive_channel` | - |  [deprecated] |
| Archive conversation | `archive_conversation` | - |  |
| Create channel | `create_channel` | - |  [deprecated] |
| Create conversation (channels and groups) | `create_conversation` | - |  |
| Get user info | `get_user_by_email` | - |  |
| Invite users to channel | `invite_user_to_channel` | - |  [deprecated] |
| Invite users to conversation | `invite_user_to_conversation` | - |  |
| Invite users to group | `invite_user_to_group` | - |  [deprecated] |
| Respond to button click | `post_button_action_reply` | - |  |
| Post message | `post_message_to_channel` | - |  |
| Set channel purpose | `set_channel_purpose` | - |  [deprecated] |
| Set channel topic | `set_channel_topic` | - |  [deprecated] |
| Set conversation purpose | `set_conversation_purpose` | - |  |
| Set conversation topic | `set_conversation_topic` | - |  |
| Unarchive channel | `unarchive_channel` | - |  [deprecated] |
| Unarchive conversation | `unarchive_conversation` | - |  |
