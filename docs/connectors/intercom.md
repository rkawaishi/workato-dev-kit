# Intercom コネクタ

Provider: `intercom`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New company | `new_company` | - |  |
| New contact | `new_contact` | - |  |
| New conversation | `new_conversation` | - |  |
| New user | `new_user` | - |  |
| Updated contact | `updated_contact` | - |  |
| Updated conversation | `updated_conversation` | - |  |
| Updated user | `updated_user` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add conversation note | `add_conversation_note` | - |  |
| Archive users | `archive_users` | Yes |  |
| Get conversation by ID | `get_conversation_by_id` | - |  |
| Reply to conversation as user | `reply_conversation` | - |  |
| Search conversations by user | `search_conversations_by_user` | Yes |  |
| Search notes by user | `search_notes_by_user` | Yes |  |
| Search segments by user | `search_segments_by_user` | Yes |  |
| Search tags by user | `search_tags_by_user` | Yes |  |
| Search user | `search_user` | - |  |
| Update user | `update_user` | - |  |
| Create/update users | `upsert_users` | Yes |  |
