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

## フィールド詳細

### post_bot_message

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| channel | string | 投稿先（チャンネル名 `#channel` or ユーザー ID で DM） |
| text | string | メッセージテキスト |
| advanced.thread_ts | string | スレッド返信先のタイムスタンプ |
| blocks | array | Block Kit ブロック定義 |
| attachment_buttons | array | ボタン付きメッセージ（下記参照） |

#### attachment_buttons の構造

```json
"attachment_buttons": [
  {
    "title": "ボタン表示名",
    "bot_command": "<domain> <name> <scope>",
    "params": "key1: value1\nkey2: value2"
  }
]
```

- ボタンクリックで `bot_command_v2` トリガーが発火
- `bot_command` は `"<domain> <name> <scope>"` 形式（スペース区切り）
- `params` は改行区切りの key: value 形式

### bot_command_v2 (trigger)

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| domain | string | コマンドのカテゴリ（例: `it_onboarding`） |
| name | string | コマンド名（例: `approve`） |
| scope | string | スコープ（例: `request`） |
| allow_dialog | string | ダイアログ許可（`true` / `false`） |

### get_user_by_email

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| email | string | ユーザーのメールアドレス |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| id | string | Slack ユーザー ID（DM の channel に使用） |
| name | string | ユーザー名 |
