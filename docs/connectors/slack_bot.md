# Workbot for Slack コネクタ

Provider: `slack_bot`

## Triggers

| 名前 | provider 内名称 | 説明 |
|---|---|---|
| New command (old version) | `bot_command` | [deprecated] |
| New command | `bot_command_v2` | コマンド実行時（ボタンクリック、テキスト入力） |
| New URL mention | `bot_document_mention` | URL メンション時（Salesforce, GitHub） |
| New dynamic menu event | `dynamic_menu` | 動的メニューの検索イベント |
| New help message trigger | `help_event` | ヘルプメッセージ要求時 |
| New Shortcut trigger | `message_action` | グローバル/メッセージショートカット実行時 |
| New event | `new_event` | Slack Events API イベント発生時 |

## Actions

| 名前 | provider 内名称 | 説明 |
|---|---|---|
| Custom action | `__adhoc_http_action` | API 直接呼び出し |
| Open/update or push modal view | `block_kit_modals` | モーダルの表示・更新・プッシュ |
| Delete message | `delete_message` | メッセージ削除 |
| Download attachment | `download_attachment` | 添付ファイルのダウンロード |
| Return menu options | `generate_menu_options` | 動的メニューのオプション返却 |
| Get user info | `get_user_by_email` | メールアドレスからユーザー情報取得 |
| Publish App Home view | `open_bot_app_home` | App Home の表示 |
| Post dialog | `open_bot_dialog` | ダイアログの表示 |
| Post message | `post_bot_message` | チャンネル/DM にメッセージ投稿 |
| Post notification (old version) | `post_bot_notification` | [deprecated] |
| Post command reply (old version) | `post_bot_reply` | [deprecated] |
| Post command reply | `post_bot_reply_v2` | コマンドへの返信 |
| Update blocks by block id | `update_blocks_by_block_id` | ブロック単位のメッセージ更新 |
| Upload file | `upload_file` | ファイルアップロード |

---

## トリガー詳細

### bot_command_v2 (New command)

コマンド実行時に発火。ボタンクリック、テキスト入力、ショートカットから起動される。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| domain | string | コマンドのカテゴリ（例: `it_onboarding`）— レシピ JSON では app に対応 |
| name | string | コマンド名（例: `approve`）— レシピ JSON では action に対応 |
| scope | string | スコープ（例: `request`）— レシピ JSON では action_data に対応 |
| allow_dialog | string | ダイアログ許可（`true` / `false`） |

#### Output fields
| フィールド | パス | 説明 |
|---|---|---|
| message_id | `message_id` | エポックタイムスタンプ（スレッド返信に使用） |
| context.team_id | `context.team_id` | Slack チーム ID |
| context.user_id | `context.user_id` | 実行ユーザーの Slack ID |
| context.channel_id | `context.channel_id` | チャンネル ID |
| context.user_handle | `context.user_handle` | ユーザーハンドル |
| context.email | `context.email` | ユーザーメール |
| context.name | `context.name` | ユーザー名 |
| context.thread_id | `context.thread_id` | スレッド ID |
| parameters.* | `parameters.<key>` | ボタンの `params` で渡した値 |
| modals.view_id | `modals.view_id` | モーダルの View ID |

#### params 参照

ボタンの `params` で渡した値はトリガー出力の `parameters.<key>` で参照可能:
```
ボタン定義: "params": "record_id: #{_dp('...')}"
トリガー出力: path:["parameters","record_id"]
```

### new_event (New event)

Slack Events API のイベント発生時に発火。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| webhook_suffix | string | イベント種別（例: `reaction_added`, `message`, `app_home_opened`） |

**注意**: イベント種別は `event_type` ではなく `webhook_suffix` で指定する。

### dynamic_menu (New dynamic menu event)

動的メニューの検索イベント。最低5文字入力で発火。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| menu_name | string | 動的メニュー名 |

#### Output fields
| フィールド | 説明 |
|---|---|
| typeahead.parameter_name | パラメータ名 |
| typeahead.value | ユーザー入力値 |
| parameters.* | 親コマンドからのパラメータ |

`generate_menu_options` アクションとペアで使用する。

### message_action (New Shortcut trigger)

グローバルショートカットまたはメッセージショートカットの実行時に発火。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| shortcut_type | string | `global` or `message` |

---

## アクション詳細

### post_bot_message (Post message)

チャンネルまたは DM にメッセージを投稿。最も汎用的なメッセージ投稿アクション。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| channel | string | 投稿先（`#channel` or ユーザー ID で DM） |
| text | string | メッセージテキスト（blocks 使用時は通知テキストとして表示） |
| blocks | array | Block Kit ブロック定義 |
| attachment_buttons | array | ボタン付きメッセージ（レガシー形式） |
| advanced.thread_ts | string | スレッド返信先のタイムスタンプ |
| advanced.message_to_update | string | 更新対象のメッセージ ID |

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

### post_bot_reply_v2 (Post command reply)

コマンド（bot_command_v2）への返信を投稿。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| text | string | 返信テキスト |
| blocks | array | Block Kit ブロック定義 |
| send_only_to_user | boolean | エフェメラル（本人のみ表示）メッセージ |
| replace_original | boolean | 元メッセージを置換 |
| delete_original | boolean | 元メッセージを削除 |

**特別な機能**: `wait_for_user_action` — ユーザーの入力を待機してジョブを一時停止。複数ステップのインタラクションを単一レシピで実現。

### block_kit_modals (Open/update or push modal view)

モーダルダイアログの表示・更新・プッシュ。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| modal_action | string | `open` / `update` / `push` |
| trigger_id | string | トリガー ID（open 時に必要、ユーザー操作から自動生成） |
| view_id | string | View ID（update 時に必要） |
| title | string | モーダルタイトル（最大24文字） |
| blocks | array | モーダル内の Block Kit ブロック |
| submit_label | string | 送信ボタンラベル（最大24文字） |
| close_label | string | 閉じるボタンラベル（最大24文字） |
| clear_on_close | boolean | 閉じた時にモーダルスタックをクリア |
| notify_on_close | boolean | 閉じた時にイベントを発火 |
| private_metadata | string | 暗号化メタデータ（最大3000文字） |
| callback_id | string | コールバック ID（最大255文字） |

**制限**: CamelCase 文字やカンマ区切りの name-value ペアは非対応。JSON 形式を使用すること。

**特別な機能**: `wait_for_user_input` — モーダルが閉じられるまでジョブを一時停止。

### open_bot_app_home (Publish App Home view)

Bot の App Home タブにリッチコンテンツを表示。ユーザーごとにパーソナライズ可能。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| user_id | string | 対象ユーザーの Slack ID（必須） |
| blocks | array | App Home の Block Kit ブロック |

**前提条件**:
- Slack App 設定で `app_home_opened` イベントのサブスクリプションが必要
- Home Tab が有効になっていること

### update_blocks_by_block_id (Update blocks by block id)

メッセージ、App Home、モーダルの特定ブロックを更新・置換・削除。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| surface | string | `message` / `app_home` / `modal` |
| original_json | string | 元のブロック JSON（トリガー出力やアクション結果から取得） |
| blocks | array | 更新するブロック（block_id で対象を特定） |
| remove | boolean | ブロックを削除する場合 `true` |

1つのブロックを複数ブロックに置換可能。複数ブロックの同時更新にも対応。

### generate_menu_options (Return menu options)

動的メニューのオプションを返却。`dynamic_menu` トリガーとペアで使用。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| options | array | 選択肢リスト（静的指定 or リスト datapill） |
| group_options | boolean | オプションをグループ化 |

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

---

## Block Kit

Slack の UI フレームワーク。メッセージ、モーダル、App Home の3つのサーフェスで使用可能。

### ブロック数の上限

| サーフェス | 最大ブロック数 |
|---|---|
| メッセージ | 50 |
| モーダル | 100 |
| App Home | 100 |

### 利用可能なブロックタイプ

| ブロック | 説明 |
|---|---|
| Section with text | テキスト表示 |
| Section with image | テキスト + サムネイル画像 |
| Section with button | テキスト + ボタン（コマンド実行/URL 遷移） |
| Section with fields | テキスト + title-value ペア（最大10件、各2000文字） |
| Section with select menu | テキスト + ドロップダウンメニュー |
| Section with overflow menu | テキスト + オーバーフローメニュー |
| Section with date picker | テキスト + 日付選択 |
| Repeat block group | Workato 固有: リスト datapill でブロックを動的生成 |
| Divider | 区切り線 |
| Image | 画像表示（公開 URL） |
| Actions | インタラクティブ要素のコンテナ |
| Context | コンテキスト情報（画像/テキスト） |

### 文字数制限

| 要素 | 最大文字数 | 備考 |
|---|---|---|
| ボタン | 2000 | コマンド + 入力値 + Workbot オーバーヘッド（9文字）含む |
| セレクトメニュー | 255 | |
| オーバーフローメニュー | 75 | |
| 日付ピッカー | 255 | |

### attachment_buttons vs Block Kit ボタン

| | attachment_buttons | Block Kit ボタン |
|---|---|---|
| 形式 | レガシー（Slack Attachments API） | 現行（Block Kit） |
| JSON フィールド | `attachment_buttons` | `blocks` 内の section with button |
| 見た目 | シンプル | リッチ（スタイル指定可能） |
| Workato での push | 安定 | blocks の構造に注意（push エラーの原因になりやすい） |
| 推奨 | シンプルなボタン操作 | リッチな UI が必要な場合 |

**注意**: Block Kit の `blocks` フィールドを使う場合、push 前に UI で設定するのが確実。JSON で直接書く場合は `visible_config_fields` の設定が必要になることがある。

### ボタンの設計ガイドライン

- ボタン数は **5個以下** が推奨（会話型 UI として自然な範囲）
- ボタンのコマンドテキストは受信側の `bot_command_v2` トリガーと完全一致が必要
- **動的ボタン**: リスト datapill からボタンを動的生成可能（Dynamic List オプション）
  - ボタンソースリスト: リスト datapill（例: Salesforce のアカウント一覧）
  - ボタンタイトル: リストアイテムのフィールド
  - コマンド入力値: 各アイテムのデータをパラメータとして渡す

---

## インターフェースデザインパターン

### パターン 1: 承認ボタン付き DM 通知

```
post_bot_message (DM + attachment_buttons)
  → ユーザーがボタンクリック
  → bot_command_v2 トリガー発火（別レシピ）
  → complete_task / 処理実行
  → post_bot_reply_v2 で結果返信
```

適用例: 承認フロー、確認操作

### パターン 2: モーダルによるフォーム入力

```
bot_command_v2 トリガー（ボタン or コマンド）
  → block_kit_modals (open) + wait_for_user_input
  → ユーザーがモーダルに入力して送信
  → 入力値を取得して処理
```

適用例: データ入力、設定変更

### パターン 3: App Home ダッシュボード

```
new_event (webhook_suffix: app_home_opened)
  → データ取得（Jira, Salesforce 等）
  → open_bot_app_home (blocks でリスト表示)
  → ユーザーがボタンクリック
  → bot_command_v2 で詳細表示/操作
```

適用例: タスク一覧、承認待ちリスト

### パターン 4: 動的メニュー付きコマンド

```
bot_command_v2 トリガー（コマンド入力）
  → dynamic_menu トリガー（別レシピ）
  → 外部システムを検索
  → generate_menu_options で選択肢返却
  → ユーザーが選択
  → 処理実行
```

適用例: レコード検索、ユーザー検索

### パターン 5: メッセージの動的更新

```
post_bot_message（初期メッセージ + blocks）
  → 処理の進行に応じて update_blocks_by_block_id
  → ステータス表示を更新
```

適用例: 進捗表示、ステータス変更の反映
