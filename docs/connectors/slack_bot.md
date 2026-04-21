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

Slack Events API のイベント発生時に発火。**Slash command も実はこの new_event 経由**（専用トリガーではない）。

#### Input fields

**`format_version: 2` 以降（新版）**:
| フィールド | 型 | 説明 |
|---|---|---|
| event_name | string | イベント名（例: `slash_command`, `reaction_added`, `message`, `app_home_opened`） |

UI で作成すると `dynamicPickListSelection.event_name`（表示用）と `toggleCfg.event_name: true` も付与される。

**旧版（format_version なし / 1）**:
| フィールド | 型 | 説明 |
|---|---|---|
| webhook_suffix | string | イベント種別（同義） |

**注意**: 新規作成時は `event_name` を使うこと（Workato が format_version=2 でレシピを管理）。

#### Output fields（slash_command の場合）

`event_name: "slash_command"` を使った場合、トリガー出力の `slash_command` オブジェクト配下に以下が入る:

| フィールド | パス | 型 | 説明 |
|---|---|---|---|
| api_app_id | `slash_command.api_app_id` | string | Slack App の ID |
| channel_id | `slash_command.channel_id` | string | コマンド実行チャンネル |
| channel_name | `slash_command.channel_name` | string | チャンネル名 |
| command | `slash_command.command` | string | スラッシュコマンド名（例: `/workato-key`） |
| is_enterprise_install | `slash_command.is_enterprise_install` | boolean | Enterprise Grid インストール判定 |
| response_url | `slash_command.response_url` | string | 遅延応答用 URL |
| team_domain | `slash_command.team_domain` | string | Slack workspace ドメイン |
| team_id | `slash_command.team_id` | string | Slack workspace ID |
| text | `slash_command.text` | string | コマンド引数（`/workato-key foo bar` なら `foo bar`） |
| trigger_id | `slash_command.trigger_id` | string | モーダル open 用 |
| user_id | `slash_command.user_id` | string | 実行者の Slack user ID |
| user_name | `slash_command.user_name` | string | 実行者のユーザー名 |

⚠️ **slash_command の出力に email は含まれない**。email が必要な場合は `get_user_by_email` アクションに `user_id` を渡して profile を取得する（後述）。

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

⚠️ **名前と入力が一致しない罠**: アクション名は "get user by email" だが、input フィールドは `email` と `id`（Slack user ID）の**どちらでも受け付ける**。UI の toggle 切り替えで選択できる。slash_command のようにトリガー出力に email が無い場合は `id` に Slack user_id を渡すパターンで使う。

#### Input fields
| フィールド | 型 | 説明 |
|---|---|---|
| email | string | ユーザーのメールアドレス |
| id | string | Slack user ID（`email` が無い場合はこちら。toggle で切替） |

#### Output fields

`profile` オブジェクトにユーザー情報がネストされて返る:

| フィールド | パス | 型 | 説明 |
|---|---|---|---|
| id | `id` | string | Slack ユーザー ID |
| name | `name` | string | ユーザー名 |
| profile.email | `profile.email` | string | メールアドレス（slash_command 経由で email を取得する主用途） |
| profile.real_name | `profile.real_name` | string | 本名 |
| profile.display_name | `profile.display_name` | string | 表示名 |

> **slash_command トリガー後の email 取得パターン**:
> `new_event(event_name: slash_command) → get_user_by_email(id: slash_command.user_id) → 後続で profile.email を参照`
> これは Slack Events API の slash_command が email を含まないため必須のワンステップ。

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
