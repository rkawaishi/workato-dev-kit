# Slack コネクタ

Provider: `slack`

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

### Triggers
| 名前 | 説明 |
|---|---|
| New button click | ボタンクリックイベント |

### Actions
| 名前 | 説明 |
|---|---|
| Post message | チャンネル/DM にメッセージ投稿 |
| Respond to button | ボタンクリックへの応答メッセージ |

### 備考
- Slack Web API v1 使用
- Slack for teams / Enterprise Grid 両対応
- CN データセンターでは利用不可

## フィールド詳細

### button_action (Button click)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Action name | text | — |
| Action ID | text | — |
| Channel | object | — |
| ID | text | — |
| Name | text | — |
| User | object | — |
| Team | object | — |
| Domain | text | — |
| Action timestamp | text | — |
| Message ID | text | — |
| Attachment ID | text | — |
| Response URL | text | — |

> ⚠ 重複ラベル "ID" / "Name" / "User" は `Channel` と `Team` グループ配下の入れ子フィールド。データツリーの paddingLeft が一律 0 のためフラットに見える点に注意。

### new_event (New event)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Event name | text | Yes | Yes | Allows to run separate triggers for separate connections. E.g. your Team name could be the value. Must be one word, lowercase and contain no special characters. Hyphens and underscores allowed. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Team ID | text | — |
| Api app ID | text | — |
| Event ID | text | — |
| Event time | date | — |
| Event | object | — |
| Type | text | — |
| User | text | — |
| Text | text | — |
| Ts | date | — |
| Channel | text | — |
| Event ts | date | — |
| ID | text | — |
| Authorizations | array | — |
| Enterprise ID | text | — |
| User ID | text | — |
| Is bot | text | — |
| Is enterprise install | text | — |
| List size | integer | — |
| List index | integer | — |
| Is ext shared channel | boolean | — |
| Event context | text | — |
| Original event json | text | — |

> ⚠ Type/User/Text/Ts/Channel/Event ts は `Event` オブジェクト配下のサブフィールド。Authorizations 配下に Enterprise ID/User ID/Is bot/Is enterprise install がネスト。データツリーの paddingLeft が一律 0 のためフラットに見える点に注意。
> ⚠ 部分学習: `webhook_suffix` (event 種別フィールド) は input にあるはずだが UI 上の "Event name" フィールドと内部キーのマッピングは UI 観察では取りきれない（`/learn-recipe` で補完）。

### archive_conversation (Archive conversation)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 出力スキーマなし (no_output_schema, fire-and-forget アクション)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Conversation |  | Yes | Yes | Select from available conversations. If not found, you may toggle to 'Enter conversation ID/name'. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|

### create_conversation (Create conversation (channels and groups))

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Conversation name | text | Yes | Yes | Enter conversation name without '#' prefix. Conversation names may only contain lowercase letters, numbers, hyphens, and underscores, and must be 80 characters or less. |
| Private conversation? | boolean | - | Yes | Creates a private group. |
| Return conversation details if already exists? | boolean | - | No | (optional field) |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| ID | text | — |
| Name | text | — |
| Is archived | boolean | — |
| Created date | date | — |
| Creator | text | — |
| Latest | object | — |
| User | text | — |
| Inviter | text | — |
| Type | text | — |
| Subtype | text | — |
| Text | text | — |
| Unread count | integer | — |
| Unread count display | integer | — |
| Members | text-array | — |
| Topic | object | — |
| Value | text | — |
| Last set | integer | — |
| Purpose | object | — |
| Is channel | boolean | — |
| Is general | boolean | — |
| Is member | boolean | — |
| Is ext shared | boolean | — |
| Is group | boolean | — |
| Is im | boolean | — |
| Is mpim | boolean | — |
| Is pending ext shared | boolean | — |
| Priority | integer | — |

> ⚠ Topic / Purpose オブジェクト配下に Value / Last set がネスト。Latest オブジェクト配下に User / Inviter / Type / Subtype / Text 等がネスト。

### get_user_by_email (Get user info)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Email | text | - | Yes | Provide the user email address |
| User ID | text | - | Yes | Provide the user ID |

> Email と User ID はどちらかを指定（両方とも optional に出るが、実質 OR で必須）。

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| ID | text | — |
| Name | text | — |
| Real name | text | — |
| Team ID | text | — |
| Color | text | — |
| Time zone | text | — |
| Profile | object | — |
| Title | text | — |
| Phone | text | — |
| Skype | text | — |
| Real name (normalized) | text | — |
| Display name | text | — |
| Display name (normalized) | text | — |
| Email | text | — |
| Team | text | — |
| Image 512 | text | — |
| Is admin | boolean | — |
| Is owner | boolean | — |
| Is primary owner | boolean | — |
| Is restricted | boolean | — |
| Is ultra restricted | boolean | — |
| Is bot | boolean | — |
| Is app user | boolean | — |

> ⚠ Title / Phone / Skype / Real name (normalized) / Display name / Display name (normalized) / Email / Team / Image 512 は `Profile` オブジェクト配下のネスト。

### invite_user_to_conversation (Invite users to conversation)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| User |  | Yes | Yes | Select from available users. For dynamic user names, toggle to 'Enter user ID/name'. |
| Conversation |  | Yes | Yes | Select from available conversations. If not found, you may toggle to 'Enter conversation ID/name'. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| ID | text | — |
| Name | text | — |
| Is archived | boolean | — |
| Created date | date | — |
| Creator | text | — |
| Latest | object | — |
| User | text | — |
| Inviter | text | — |
| Type | text | — |
| Subtype | text | — |
| Text | text | — |
| Unread count | integer | — |
| Unread count display | integer | — |
| Members | text-array | — |
| Topic | object | — |
| Value | text | — |
| Last set | integer | — |
| Purpose | object | — |
| Is channel | boolean | — |
| Is general | boolean | — |
| Is member | boolean | — |
| Is ext shared | boolean | — |
| Is group | boolean | — |
| Is im | boolean | — |
| Is mpim | boolean | — |
| Is pending ext shared | boolean | — |
| Priority | integer | — |

> ⚠ create_conversation と同じスキーマ構造。Topic / Purpose オブジェクト配下に Value / Last set がネスト。

### post_button_action_reply (Respond to button click)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 出力スキーマなし (no_output_schema, fire-and-forget アクション)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Button response URL | text | Yes | Yes | Identifies button to respond to. Response URL datapill can be found in New button click trigger output. Learn more. |
| Response type | text | Yes | Yes | In channel posts a normal chat message; ephemeral posts message only visible to user. |
| Replace original? | boolean | - | Yes | Replaces the original message with buttons. New message will be posted in the same position in channel. |
| Delete original? | boolean | - | Yes | Deletes the original message with buttons. New message will be posted at the end of channel. |
| Basic text | text | Yes | Yes | Slack message to send. |
| Attachment title | text | - | Yes | Title of the Slack message attachment. |
| Attachment title link | text | - | Yes | Attachment titles are clickable. Provide URL of page to direct users when clicked. |
| Attachment text | text | - | Yes | Text that appears within the attachment block. |
| Attachment message fields |  | - | No | (optional field) |
| Attachment color |  | - | No | (optional field) |
| Thumb URL | text | - | No | (optional field) |
| Image URL | text | - | No | (optional field) |
| Allow Slack formatting |  | - | No | (optional field) |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|

### post_message_to_channel (Post message)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Channel |  | Yes | Yes | Select from available channels. If not found, you may toggle to 'Enter channel ID/name'. |
| Basic text | text | Yes | Yes | Slack message to send. |
| Attachment title | text | - | Yes | Title of the Slack message attachment. |
| Attachment title link | text | - | Yes | Attachment titles are clickable. Provide URL of page to direct users when clicked. |
| Attachment text | text | - | Yes | Text that appears within the attachment block. |
| Buttons |  | - | Yes | — |
| Attachment color |  | - | Yes | Determines the vertical bar color. Red for danger, orange for warning, green for good. |
| Allow Slack formatting |  | - | Yes | Allow parsing of <URL link\|title> <userID> <channel\|name> tags in the message. More information here. Links should be expressed in full e.g. https://workato.com. |
| Attachment message fields |  | - | No | (optional field) |
| Thumb URL | text | - | No | (optional field) |
| Image URL | text | - | No | (optional field) |
| Thread ID | text | - | No | (optional field) |
| Post message as | text | - | No | (optional field) |
| Icon image URL | text | - | No | (optional field) |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Text | text | — |
| Username | text | — |
| User | text | — |
| Type | text | — |
| Subtype | text | — |
| Message ID | text | — |
| Thread ID | text | — |

### set_conversation_purpose (Set conversation purpose)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 出力スキーマなし (no_output_schema, fire-and-forget アクション)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Conversation |  | Yes | Yes | Select from available conversations. To set dynamic conversation names, toggle to 'Enter conversation ID/name'. |
| Conversation purpose | text | Yes | Yes | Set conversation purpose. Slack formatting useable here, including user tagging. Learn more. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|

### set_conversation_topic (Set conversation topic)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 出力スキーマなし (no_output_schema, fire-and-forget アクション)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Conversation |  | Yes | Yes | Select from available conversations. To set dynamic conversation names, toggle to 'Enter conversation ID/name'. |
| Conversation topic | text | Yes | Yes | Set conversation topic. Slack formatting useable here, including user tagging. Learn more. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|

### unarchive_conversation (Unarchive conversation)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 出力スキーマなし (no_output_schema, fire-and-forget アクション)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Conversation |  | Yes | Yes | Select from available conversations. If not found, you may toggle to 'Enter conversation ID/name'. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|

## Workbot for Slack (`slack_bot`)

### Triggers
| 名前 | provider 内名称 | 説明 |
|---|---|---|
| New event | `new_event` | Slack イベント購読（`event_name` でイベント種別指定） |

### Actions
| 名前 | provider 内名称 | 説明 |
|---|---|---|
| Post bot message | `post_bot_message` | Bot としてメッセージ投稿。Block Kit 対応 |
| Custom action | `__adhoc_http_action` | Slack API を直接呼出し |

### event_name 一覧（確認済み）
- `reaction_added` — リアクション追加

### new_event (reaction_added)

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| reaction_added.type | string | Type |
| reaction_added.user | string | User |
| reaction_added.reaction | string | Reaction |
| reaction_added.item_user | string | Item user |
| reaction_added.item.type | string | Type (nested) |
| reaction_added.item.channel | string | Channel (nested) |
| reaction_added.item.ts | string | Ts (nested) |
| reaction_added.event_ts | string | Event ts |

### Custom action: conversations.history (GET)

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| path | string | Yes | Path (API endpoint) |
| response_type | string | - | Response type (json, raw, xml2, text) |
| input.data.channel | string | - | channel |
| input.data.latest | string | - | latest |
| input.data.oldest | string | - | oldest |
| input.data.inclusive | boolean | - | inclusive |
| input.data.limit | integer | - | limit |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| ok | boolean | Ok |
| messages[].type | string | Type |
| messages[].user | string | User |
| messages[].text | string | Text |
| messages[].ts | string | Ts |
| has_more | boolean | Has more |
| pin_count | number | Pin count |
| response_metadata.next_cursor | string | Next cursor (nested) |

### `slack` vs `slack_bot` のイベント指定フィールド

| | `slack`（標準） | `slack_bot`（Workbot） |
|---|---|---|
| イベント種別フィールド | `input.webhook_suffix` | `input.event_name` |
| dynamicPickListSelection | なし | あり |

- 標準コネクタ: `"webhook_suffix": "reaction_added"` のように直接値を指定
- Workbot: `"event_name": "reaction_added"` + `dynamicPickListSelection` が付与される

### post_bot_message の主要フィールド
- `channel` — 投稿先チャンネル
- `text` — メッセージテキスト
- `advanced.thread_ts` — スレッド返信先のタイムスタンプ
- `blocks` — Block Kit ブロック定義

---

## 学習サマリ

最終実行: 2026-04-27 by /auto-learn
- 試行: 11 op (2 triggers + 9 actions)
- 完全成功: 5 — `button_action`, `create_conversation`, `get_user_by_email`, `invite_user_to_conversation`, `post_message_to_channel`
- 部分学習: 6 — `new_event` (internal key), `archive_conversation` / `unarchive_conversation` / `set_conversation_purpose` / `set_conversation_topic` / `post_button_action_reply` (fire-and-forget)
- 学習失敗: 0
- スキップ:
  - Deprecated: 7
  - adhoc: 1 — `__adhoc_http_action`
  - 既学習: 0

### 要 follow-up

- **Fire-and-forget (UI 仕様・追加学習不要)**
  - `archive_conversation` — チャンネルアーカイブ
  - `unarchive_conversation` — チャンネル復元
  - `set_conversation_purpose` — チャンネル目的設定
  - `set_conversation_topic` — チャンネルトピック設定
  - `post_button_action_reply` — Block Kit ボタン応答
- **Internal key 不明 (要 /learn-recipe)**
  - `new_event` — `Event name` フィールドが内部 `webhook_suffix` キーに対応。UI 観察では label しか取れない

### 構造的注記（参考）

- 重複ラベル `ID` / `Name` / `User`: `Channel` と `Team` グループ配下の入れ子フィールド。データツリー paddingLeft=0 でフラット表示（`button_action`, `new_event` 等）
- 動的 `Channel` picklist: 多くのアクションで Channel 選択が必要（sandbox 値なし。static のみ捕捉）
