# Workbot for Microsoft Teams connector

Provider: `teams_bot`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New command | `bot_command` | - |  |
| New help message trigger | `help_event` | - |  |
| New real-time event | `new_event` | - |  |
| New message | `new_message_event` | - |  |
| Tab opened | `tab_opened` | - |  [deprecated] |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Delete message | `delete_message` | - |  |
| Get user info by principal name or user ID | `get_user_by_principal_name` | - |  |
| Response to real-time event | `invoke_response` | - |  |
| Post message | `post_blocks_message` | - |  |
| Post reply | `post_blocks_reply_message` | - |  |
| Post message (old version) | `post_bot_message` | - |  |
| Post reply (old version) | `post_bot_reply` | - |  |
| Post simple message | `post_simple_message` | - |  |
| Post simple reply | `post_simple_reply` | - |  |
| Show tab using Adaptive Cards | `render_tab` | - |  [deprecated] |
