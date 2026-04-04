# Slack コネクタ

公式: https://docs.workato.com/en/connectors/slack.html

## 2つの Slack コネクタ

| | Slack (標準) | Workbot for Slack (slack_bot) |
|---|---|---|
| provider 名 | `slack` | `slack_bot` |
| 認証 | OAuth 2.0 | Custom OAuth profile |
| 用途 | 基本的な Slack 連携 | 高度なイベント、Bot メッセージ、Block Kit |
| 公式ドキュメント | /connectors/slack.html | /workbot/workbot.html |

**使い分け**: 標準コネクタにないイベント（`reaction_added` 等）や権限（`channels.history` 等）が必要な場合は `slack_bot` + Custom OAuth を使用する。

## Slack（標準コネクタ）

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

### post_bot_message の主要フィールド
- `channel` — 投稿先チャンネル
- `text` — メッセージテキスト
- `advanced.thread_ts` — スレッド返信先のタイムスタンプ
- `blocks` — Block Kit ブロック定義
