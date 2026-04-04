# Workato Known Patterns

レシピ分析から蓄積したパターン知識。`/learn-recipe` で自動更新される。

## プロバイダー・アクション一覧

| Provider | Action/Trigger | Keyword | 用途 | 出典 |
|---|---|---|---|---|
| `gmail` | `new_email` | trigger | 新着メール受信 | Sample project 1 |
| `gmail` | `download_attachment` | action | 添付ファイルダウンロード | Sample project 1 |
| `google_drive` | `upload_file` | action | ファイルアップロード | Sample project 1 |
| `jira` | `new_issue` | trigger | 新規チケット作成 | Sample project 2 |
| `slack` | `new_event` | trigger | Slack イベント（リアクション追加等）。`input.webhook_suffix` でイベント種別指定 | Helpdesk auto reply |
| `slack` | `get_message` | action | メッセージ内容を取得 | Helpdesk auto reply |
| `slack` | `post_message` | action | チャンネルへのメッセージ投稿 | Sample project 2 |
| `jira` | `search_issues` | action | JQL によるチケット検索 | Helpdesk auto reply |
| `salesforce` | `search_sobjects` | action | オブジェクト検索 | Sample project 3 |
| `salesforce` | `update_sobject` | action | オブジェクト更新 | Sample project 3 |
| `open_ai_utility` | `analyse_document` | action | ドキュメント分析 | Sample project 3 |
| `workato_genie` | `start_workflow` | trigger | Genie スキルワークフロー開始 | Sample project 3 |
| `workato_genie` | `workflow_return_result` | action | Genie に結果を返す | Sample project 3 |

## レシピ構成パターン

### パターン1: トリガー → foreach → アクション

メール添付ファイルのような「1トリガーで複数アイテムを処理」するパターン。

```
trigger (gmail/new_email)
  └── foreach (attachments)
        ├── action (gmail/download_attachment)
        └── action (google_drive/upload_file)
```

- `foreach` ステップは `source` フィールドでイテレート対象を datapill 指定
- `clear_scope: false` で親スコープの変数にアクセス可能
- 出典: `upload_gmail_attachments_to_google_drive.recipe.json`

### パターン2: トリガー + フィルタ → アクション

条件に合致するイベントのみ処理するパターン。

```
trigger (jira/new_issue) [filter: priority contains "High"]
  └── action (slack/post_message)
```

- `filter` はトリガーステップに設定
- `filter.type: "compound"`, `filter.operand: "and"` で複数条件を AND 結合
- 出典: `notify_slack_channel_for_high_or_highest_priority_jira_tickets.recipe.json`

### パターン3: Genie スキルワークフロー

AIエージェントが呼び出すスキルのレシピパターン。

```
trigger (workato_genie/start_workflow)
  ├── action (外部API操作)
  ├── action (AI分析 etc.) [optional]
  └── action (workato_genie/workflow_return_result)
```

- トリガーの `input` に `parameters_schema_json` と `result_schema_json` を JSON 文字列で定義
- `as` フィールドにはランダム8文字 hex を使用（通常レシピとの違い）
- 最終ステップで必ず `workflow_return_result` を呼ぶ
- 出典: `search_contracts_in_salesforce.recipe.json`, `update_contract_in_salesforce.recipe.json`

### パターン4: イベントトリガー → データ取得 → AI分析 → 通知

Slack リアクション等のイベントをトリガーに、関連データを収集し AI で分析・回答するパターン。

```
trigger (slack/new_event) [webhook_suffix: "reaction_added"]
  ├── action (slack/get_message)        — 元メッセージ取得
  ├── action (jira/search_issues)       — 関連データ検索
  ├── action (open_ai_utility/analyse_document) — AI 分析・回答生成
  └── action (slack/post_message)       — スレッドに投稿
```

- `slack/new_event` トリガーは `input.webhook_suffix` でイベント種別を指定（`reaction_added` 等）
- **注意**: `event_type` や `reaction` ではなく `webhook_suffix` がフィールド名
- コネクションは別プロジェクトのものも `folder` 指定で参照可能
- 出典: `auto_reply_to_slack_ticket_reactions.recipe.json`

## Workato のインポート時の挙動

- ローカルで設定した `input` フィールドは、UI で対応するコネクタの設定が未完了だと **空 `{}` にリセットされる**
- `version` は UI で編集するたびに自動インクリメントされる
- コネクション名が微妙に変わることがある（例: `helpdesk_ai` → `helpdesk_ai_by_workato`）
- 別プロジェクトのコネクションを参照する場合、`account_id.folder` にプロジェクト名が入る

## Datapill パターン

### _dp() 形式（主流）
```
#{_dp('{"pill_type":"output","provider":"gmail","line":"new_email","path":["id"]}')}
```

### foreach 内の current_item 参照
```
#{_dp('{"pill_type":"output","provider":"foreach","line":"foreach","path":["attachmentId"]}')}
```

### _() ドット記法
```
#{_('data.gmail.new_email.subject')}
```

### Ruby 式（リストメタデータ・結合等）
```
=_('data.gmail.new_email.attachments').pluck('filename').join(', ')
```

### リストサイズ取得
```
#{_('data.gmail.new_email.attachments.first.____Size', 'list_meta', '____Size', 'data.gmail.new_email.attachments')}
```

## コネクション命名規則

観測されたパターン: `<prefix> | <Provider名>`
- `Sample1 | Gmail`
- `Sample1 | Google Drive`
- `Sample2 | Slack`
- `Sample2 | Jira`

## open_ai_utility の特殊入力

```json
{
  "_settings_version": "2",
  "text": "<分析対象テキストまたはURL + datapill>",
  "question": "分析プロンプト"
}
```

---
*最終更新: Helpdesk auto reply フィードバック反映 (Sample project 1-3 + Helpdesk)*
