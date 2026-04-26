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
| Upload file | `upload_file` | ファイルアップロード（⚠ UI ピッカーで "Return menu options" + File バッジと誤表示される） |

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

### bot_document_mention (New URL mention)

Real-time。チャネル内に対象アプリの URL がメンションされたときに発火。Workbot は Salesforce / Zendesk URL を理解する。Unfurling シナリオに使う。

学習元: /auto-learn (UI 観察) — 2026-04-25

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| Application | string (picklist) | Yes | URL 検出対象のアプリ |
| Business data | string (picklist) | Yes | 対象のビジネスデータ種別（例: invoice, bill, customer） |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Application | string | URL に含まれるアプリ名 |
| Object | string | 対象オブジェクト種別（例: account, opportunity） |
| Object ID | string | 対象オブジェクトの ID |
| Context | object | 実行コンテキスト（コンテナ） |
| Context.Team ID | string | Slack チーム ID |
| Context.User ID | string | 実行ユーザーの Slack ID |
| Context.User handle | string | ユーザーハンドル |
| Context.User name | string | ユーザー名 |
| Context.User email | string | ユーザーメール |
| Context.Conversation ID | string | チャンネル / DM の ID |
| Context.Message text | string | URL を含むメッセージ全文 |
| Context.Reply to | string | 返信先 |
| Context.Timestamp | datetime | 発火タイムスタンプ |
| Context.Thread ID | string | スレッド ID |
| Context.Interactive | boolean | インタラクティブ実行か |
| Context.Trigger ID | string | Slack Trigger ID |
| Context.Callback ID | string | Callback ID |
| Context.Response URL | string | Slack Response URL |
| Context.Original message JSON | string | 元メッセージの JSON |
| Context.Original message timestamp | string | 元メッセージのタイムスタンプ |
| Modals & App home | object | モーダル / App home コンテキスト（コンテナ） |

### help_event (New help message trigger)

Real-time。ユーザーが `help` で DM するか、チャンネルで `@workbot help` のようにメンションしたときに発火。`Post command reply` アクションとペアで bot のヘルプメッセージをカスタマイズする。1 つのコネクションで有効化できる help_event レシピは 1 つだけ（カスタムヘルプより優先）。

学習元: /auto-learn (UI 観察) — 2026-04-25

#### Input fields
入力フィールドなし（"Setup done — This step doesn't need any custom configuration."）。

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Help message text | string | デフォルトの help メッセージテキスト |
| Personalized connections command | string | 個人接続管理用のコマンド |
| Bot info command | string | bot 情報表示コマンド |
| Is bot admin? | boolean | 実行ユーザーが bot 管理者か |
| Bot commands | array | bot に登録されたコマンド一覧（コンテナ） |
| Bot commands[].Recipe ID | string | コマンドを実装するレシピ ID |
| Bot commands[].Command | string | コマンド名 |
| Bot commands[].Description | string | コマンドの説明 |
| Bot commands[].Recipe Name | string | レシピ名 |
| Bot commands[].Recipe URL | string | レシピへの URL |
| Bot commands[].Recipe jobs URL | string | ジョブ一覧への URL |
| Bot commands[].List size | integer | 配列サイズ |
| Bot commands[].List index | integer | 配列イテレーションインデックス |
| Context | object | 実行コンテキスト（コンテナ） |
| Context.Team ID | string | Slack チーム ID |
| Context.User ID | string | 実行ユーザーの Slack ID |
| Context.User handle | string | ユーザーハンドル |
| Context.User name | string | ユーザー名 |
| Context.User email | string | ユーザーメール |
| Context.Conversation ID | string | チャンネル / DM の ID |
| Context.Message text | string | メッセージテキスト |
| Context.Reply to | string | 返信先 |
| Context.Timestamp | datetime | 発火タイムスタンプ |
| Context.Thread ID | string | スレッド ID |
| Context.Interactive | boolean | インタラクティブ実行か |
| Context.Trigger ID | string | Slack Trigger ID（モーダルや dialog 起動に使用） |
| Context.Callback ID | string | Callback ID |
| Context.Response URL | string | Slack Response URL |
| Context.Original message JSON | string | 元メッセージの JSON |
| Context.Original message timestamp | string | 元メッセージのタイムスタンプ |
| Modals & App home | object | モーダル / App home コンテキスト（コンテナ） |

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

### delete_message (Delete message)

Workbot として投稿したメッセージを削除する。

学習元: /auto-learn (UI 観察) — 2026-04-25 / output 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| Message timestamp | string | Yes | 削除対象メッセージのタイムスタンプ |
| Message channel | string | Yes | 削除対象が投稿されているチャンネル |

オプションフィールドなし。

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Channel ID | string | 削除実行されたチャンネル ID |
| Timestamp | string | 削除されたメッセージのタイムスタンプ |

### download_attachment (Download attachment)

Slack 添付ファイルを Workbot 経由でダウンロードする。File 出力タグ付き。

学習元: /auto-learn (UI 観察) — 2026-04-25 / output 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| URL | string | Yes | URL of Slack attachment |

オプションフィールドなし。

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Body | string | 添付ファイルのバイナリコンテンツ（datapill として下流に渡せる） |
| Size | integer | ファイルサイズ（バイト） |

### upload_file (Upload file)

チャンネルまたはスレッドにファイル添付を投稿。初期コメントを付けることもできる。

⚠ **UI 表示バグ**: Workbot for Slack の Action ピッカーで `upload_file` のタイトルが誤って **"Return menu options"**（File バッジ付き）と表示される。`generate_menu_options` (Return menu options, バッジなし) と並んで重複するため、選ぶ際は **File バッジの有無**で判別する必要がある。canvas / panel header にも同じ誤タイトルが表示されるが、フィールド構造は upload_file のもの（"Post to conversations" / "File content" 等）。Recipe data パネルの Step output グループ名も同じく "Return menu options" と表示される。

学習元: /auto-learn (UI 観察) — 2026-04-25 / output 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Post to conversations | string (picklist) | Yes | 表示 | 投稿先チャンネル / 直接会話。Workbot がメンバーである必要あり。複数指定可 |
| File content | string | Yes | 表示 | 直前ステップの File content datapill（例: Google Drive Download attachment 出力） |
| Initial comment | string | - | 表示 | ファイル投稿時の冒頭コメント |
| File name | string | - | 表示 | ファイル名（例: foo.txt） |
| File type | string | - | 表示 | ファイル形式識別子（例: text）。Slack 対応形式は公式参照 |
| Title | string | - | 非表示 | ファイルタイトル |
| Thread ID | string | - | 非表示 | 投稿先スレッド ID |

#### Output fields
Slack `files.upload` API のレスポンスに準拠（[Slack 公式リファレンス](https://api.slack.com/methods/files.upload)参照）。

| フィールド | 型 | 説明 |
|---|---|---|
| Ok | string | API 結果ステータス |
| File | object | アップロード結果ファイルメタデータ（コンテナ） |
| File.ID | string | ファイル ID |
| File.Created | string | 作成タイムスタンプ |
| File.Timestamp | string | タイムスタンプ |
| File.Name | string | ファイル名 |
| File.Title | string | タイトル |
| File.User | string | アップロードユーザー ID |
| File.Editable | boolean | 編集可能か |
| File.Size | integer | サイズ（バイト） |
| File.Mode | string | アップロードモード |
| File.Is external | boolean | 外部ファイルか |
| File.External type | string | 外部タイプ |
| File.Is public | boolean | パブリックか |
| File.Public URL shared | boolean | パブリック URL が共有されているか |
| File.Display as bot | boolean | bot として表示するか |
| File.Username | string | ユーザー名 |
| File.URL private | string | プライベート URL |
| File.URL private download | string | プライベートダウンロード URL |
| File.Permalink | string | パーマリンク |
| File.Permalink public | string | パブリックパーマリンク |
| File.User | string | ユーザー（重複ラベル — Slack API の異なるパスを表示） |
| File.Comments count | integer | コメント数 |
| File.Is starred | boolean | スター付きか |
| File.Channels | string[] | 投稿先チャンネル ID 配列 |
| File.Has rich preview | boolean | リッチプレビューがあるか |

### open_bot_dialog (Post dialog)

ボタンクリックやメニュー選択時に bot dialog を開く。**Legacy** API（モーダルが推奨）。`New command` トリガーとペアで使う。Submit 押下時に別の bot コマンドを実行する構造。

学習元: /auto-learn (UI 観察) — 2026-04-25 / output 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Trigger ID | string | Yes | 表示 | New command トリガー出力の Trigger ID。ボタン / メニュー由来のもののみ有効 |
| Dialog title | string | Yes | 表示 | dialog のタイトル（最大 24 文字） |
| Submit button command | string (picklist) | Yes | 表示 | Submit 時に呼び出す Workbot コマンド |
| State(Callback id) | string | - | 表示 | dialog 識別子（最大 3000 文字）。Submit 時のレシピに渡される |
| Submit button label | string | - | 非表示 | Submit ボタンのラベル |

#### Output fields
**出力フィールドなし**（Recipe data パネルに `Step N output` グループが現れない fire-and-forget 型のアクション）。dialog 送信後の処理は `Submit button command` で指定した別の bot コマンドレシピで行う。

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

---

## モーダル詳細

### モーダル操作タイプ

| タイプ | 用途 | 必要な ID |
|---|---|---|
| Open | 新規モーダルを開く | Trigger ID |
| Update | 既存モーダルを更新 | Trigger ID + View ID |
| Push | 現在のモーダルの上に新しいビューを重ねる | Trigger ID（アクティブビューから） |

Trigger ID はボタン、メニュー、セレクトメニュー、日付ピッカー、ショートカット、スラッシュコマンド、モーダル送信から生成される。

### モーダル専用の入力ブロック

通常のメッセージでは使えないモーダル専用の入力要素:
- Single-line input
- Multi-line input
- Select menu input
- Datepicker input
- Checkboxes input

**重要**: 入力ブロックはビュー送信時にのみコマンドを発火する（クリック時ではない）。

### モーダル間のデータ受け渡し

`bot_command_v2` トリガーの出力に含まれる Modals オブジェクト:

| フィールド | 説明 |
|---|---|
| View ID | アクティブビューの ID |
| Root View ID | 最初のビューの ID |
| Previous View ID | 直前のビューの ID |
| Private metadata | 暗号化データ（最大3000文字） |
| Hash | 非同期更新の検証トークン |

### モーダルの注意点

- タイトルは最大24文字、ボタンラベルも最大24文字
- CamelCase やカンマ区切りの name-value ペアは非対応 → **JSON 形式を使用**
  - 例: `{"OpportunityId": "OPP1234567"}`
- ビュー送信するとアクティブビューの ID は無効になる → Root View ID または Previous View ID を使用
- Push は最大3段まで
- 入力ブロックを使う場合は submit / close ボタンの定義が必須

---

## ダイアログ（レガシー）

モーダルの前身。3つのレシピで構成される:

1. **トリガーレシピ** — ボタン/メニュークリックでダイアログ表示レシピを起動
2. **ダイアログ表示レシピ** — `open_bot_dialog` でダイアログを表示（最大5フィールド）
3. **実行レシピ** — ダイアログ送信でトリガーされ処理を実行

### ダイアログ vs モーダル

| | ダイアログ | モーダル |
|---|---|---|
| フィールド数 | 最大5 | 制限なし（blocks で構成） |
| UI の柔軟性 | テキスト/セレクトのみ | Block Kit の全要素 |
| スタック | 不可 | 最大3段 |
| 推奨 | レガシー互換 | **新規開発はモーダルを使用** |

---

## 動的メニュー詳細

2つのレシピで構成される:

### 1. プライマリレシピ（コマンドレシピ）
- パラメータの dialog control type を `Select` に設定
- Menu options で `Dynamic` を選択
- 動的メニューレシピ ID を指定
- `Dynamic menu recipe params` でコンテキストパラメータを渡す（カンマ区切り key-value）

### 2. 動的メニューレシピ
```
dynamic_menu トリガー → 外部システム検索（typeahead 値でフィルタ）→ generate_menu_options
```

- ユーザーが3文字以上入力するとイベント発火
- `typeahead.value` に入力文字列が格納
- `generate_menu_options` で検索結果を選択肢として返却

### Post dialog での JSON 設定

```json
{
  "type": "select",
  "name": "your_parameter",
  "data_source": "external",
  "dynamic_menu_recipe": "28748",
  "dynamic_menu_recipe_params": "stagename: Closed Won",
  "min_query_length": 3
}
```

---

## メッセージメニュー

ドロップダウン形式で複数のアクションを提供。ボタンの代替。

### 静的メニュー

| フィールド | 説明 |
|---|---|
| Menu Name | メニュー表示ラベル |
| Display Text | 選択肢の表示テキスト |
| Submit Command | 実行するコマンド（bot_command_v2 と一致） |
| Input Values | 下流レシピに渡す name-value ペア |

### 動的メニュー

リスト datapill からオプションを動的生成:
- Menu options source list: リスト datapill
- Display text: リスト要素のフィールド
- Submit command: 実行するコマンド
- Input values: 渡すパラメータ

推奨: メニューオプション数は **5個以下**。

---

## スラッシュコマンド

`/createissue` のような Slack スラッシュコマンドで Workbot レシピをトリガー。

### 設定手順

1. **Workato**: レシピのトリガーでスラッシュコマンドを有効化し、コマンド名を入力
2. **Workato**: 生成された Request URL をコピー
3. **Slack API**: アプリの Slash Commands セクションで新規コマンドを作成
4. **Slack API**: Request URL を貼り付け、説明とヒントを追加
5. **Slack API**: "Escape channels, users, and links" を有効化

### パラメータ入力方法

- ダイアログボックス（設定時）
- インライン: `/createissue project_issue_type: UI--Bug summary: バグの説明`
- 会話プロンプト

### Enterprise vs レガシースラッシュコマンド

| 機能 | Enterprise Workbot | レガシー |
|---|---|---|
| ダイアログ起動 | 可 | 不可 |
| 不足入力のダイアログ | 可 | 不可 |
| エフェメラルメッセージ | 可 | 不可 |
| カスタム Slack アプリ必要 | はい | いいえ |
| チャンネル投稿 | 招待済みのみ | 全チャンネル |
| 複数コマンド/コネクション | レシピごとにユニーク | 複数トークン保存可 |

**レガシーは将来的に廃止予定。新規開発は Enterprise Workbot を使用すること。**

### 注意

- スラッシュコマンドは名前空間がないため、Enterprise Workbot 全体でユニークな名前にすること
- Enterprise Grid 環境では組織レベルでのインストールが必要
- Enterprise Workbot は招待されたチャンネルにのみ投稿可能（レガシーとの違い）

---

## Enterprise Grid セットアップ

Enterprise Grid 環境での Workbot 設定手順。

### 前提条件
- Slack Enterprise Grid プラン
- Workato で Enterprise Workbot を作成済み（Standard Workbot ではない）
- Custom OAuth profiles へのアクセス
- Slack の Org Admin または Org Owner 権限

### 手順

1. **App-Level Token の生成**: Slack API → アプリ → Basic Information → App-Level Tokens → `authorizations:read` スコープで生成
2. **Custom OAuth Profile の更新**: Workato → Tools → Custom OAuth profiles → トークンを貼り付け
3. **Workbot の再接続**: Platform → Workbot → Edit → Disconnect → Reconnect → **組織レベル**で認証
4. **Slack でアプリ承認**: Settings → Organization settings → Apps → Approve
5. **ワークスペースに追加**: Apps → Add to more workspaces → 対象ワークスペースを選択

---

## Embed（パートナー配布）

SaaS ベンダーが顧客にホワイトラベルの Slack Bot を配布する仕組み。

- Custom OAuth Profile を顧客ワークスペースに共有
- レシピをマニフェストとしてエクスポート → 顧客ワークスペースにインポート
- 顧客は共有された OAuth Profile で認証するだけで Bot が動作
- 顧客側で Slack OAuth アプリを作成する必要がない
