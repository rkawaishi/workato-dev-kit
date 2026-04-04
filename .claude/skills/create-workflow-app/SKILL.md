---
description: Workato Workflow App（承認ワークフロー等）を段階的に構築する。Data Table、ステージ、レシピの JSON 生成と push/UI 操作のガイドを提供。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# /create-workflow-app

Workato Workflow App を段階的に構築するスキル。JSON 生成と UI 操作のガイドを組み合わせてアプリを完成させる。

## 使い方

- `/create-workflow-app` — 対話的に新しい Workflow App を構築
- `/create-workflow-app <name>` — 指定名で構築開始

## 前提知識

以下を参照する:
- `@docs/platform/workflow-apps.md` — プロバイダー/アクション、構築パターン
- `@docs/learned-patterns.md` — Workflow App ファイル種別、レシピパターン
- `@.claude/rules/workato-agentic-format.md` — lcap_app / workato_db_table の JSON 構造

## Phase 1: 設計

ユーザーに以下を確認:

- **アプリの目的**: 何のリクエスト/承認フローか
- **Data Table のフィールド**: どんな情報を格納するか
- **ワークフローステージ**: どんな承認段階があるか（例: New → Manager review → Done / Canceled）
- **承認者の特定方法**: 固定ユーザー / HRMS から動的取得 / フォームで指定
- **外部連携**: 承認後に何をするか（Jira 起票、Slack 通知、メール送信等）
- **格納先プロジェクト名**: `projects/[App] <Name>` 形式

## Phase 2: Workflow App 作成（UI）

ユーザーに以下を依頼:

```
Workato UI で以下を実行してください:
1. Projects > 新規プロジェクト「[App] <Name>」を作成
2. プロジェクト内で Workflow App「<Name>」を新規作成

作成したら教えてください。pull してから次のステップに進みます。
```

pull コマンド:
```bash
workato init --non-interactive --profile default --project-id <id> --folder-name "projects/[App] <Name>"
```

または既にプロジェクトがある場合:
```bash
workato projects use "[App] <Name>" && workato pull
```

## Phase 3: Data Table + ステージ定義（JSON → push）

以下のファイルを生成して push:

### workato_db_table.json

```json
{
  "name": "<テーブル名>",
  "schema": [
    {
      "id": "11fbe9a6-a16d-4d7e-86ea-afe42ec03005",
      "title": "Record ID",
      "type": "short-text",
      "read_only": true,
      "hidden": true
    },
    {
      "id": "a5612739-5401-4ae7-bd07-782c1a6fb2d1",
      "title": "Created time",
      "type": "date-time",
      "read_only": true,
      "hidden": true
    },
    {
      "id": "61aae604-a95e-4519-9091-bb0bf754a67f",
      "title": "Last modified time",
      "type": "date-time",
      "read_only": true,
      "hidden": true
    }
    // ユーザー定義フィールドを追加（UUID v4 を生成）
  ],
  "project_name": "[App] <Name>"
}
```

- システムフィールド（Record ID, Created time, Last modified time）の UUID は全テーブル共通
- ユーザー定義フィールドの UUID は `uuidgen` 等で新規生成
- type: `short-text`, `long-text`, `number`, `boolean`, `date`, `date-time`, `file`, `relation`

### lcap_app.json の更新

pull した lcap_app.json を編集してステージと Data Table を追加:

```json
{
  "name": "<App名>",
  "creation_page": null,
  "workato_db_table": {
    "zip_name": "<table>.workato_db_table.json",
    "name": "<テーブル名>",
    "folder": ""
  },
  "workflow_stages": [
    { "name": "New", "color": 0 },
    { "name": "<承認ステージ>", "color": 1 },
    { "name": "Done", "color": 2 },
    { "name": "Canceled", "color": 3 }
  ],
  ...
}
```

- `creation_page` は null のまま（Phase 4 でページ作成後に自動設定）
- `task_page` / `details_page` も null のまま
- ステージの color: 0=New, 1=進行中, 2=完了, 3=キャンセル, 8=中間

push して確認:
```bash
workato push
```

## Phase 4: ページ作成（UI）

ユーザーに以下を依頼:

```
Workato UI で以下のページを作成してください:
1. 送信フォーム — フィールド: <Data Table のユーザー定義フィールド一覧>
2. レビューページ — 承認者がリクエスト内容を確認して承認/却下するページ
3. 承認済みページ — 承認後の表示
4. 却下ページ — 却下後の表示

作成したら教えてください。pull してレシピを作成します。
```

pull:
```bash
echo "y" | workato pull
```

## Phase 5: レシピ作成（JSON → push）

pull 結果を確認し、レシピを生成する。

### メインレシピのテンプレート（承認ワークフロー）

```
[0] trigger: workato_workflow_task/new_requests_realtime
      input.app_id → lcap_app.json
  [1] action: workato_recipe_function/call_recipe（承認者を特定）
      ※ 固定ユーザーの場合はこのステップを省略
  [2] action: workato_workflow_task/human_review_on_existing_record
      input.email → [1] の result.manager_email（動的）または固定メール
      input.record_id → trigger の request.Record_ID
  [3] if: task.is_approved == true
    [4] action: 外部連携（Jira, Slack 等）
    [5] action: workato_workflow_task/update_request（結果を保存）
    [6] action: workato_workflow_task/change_workflow_stage → Done
  [7] else:
    [8] action: workato_workflow_task/change_workflow_stage → Canceled
```

### レシピ生成時の注意

- record_id は **trigger output** (`new_requests_realtime` → `request.11fbe9a6_...`) から一貫して取得
- Data Table フィールド UUID: input ではハイフン区切り、output/datapill ではアンダースコア区切り
- `human_review` の `email` / `name` に datapill を使えば動的アサイン可能
- 外部連携のコネクタフィールドが不明な場合は `input: {}` にして push → UI で設定 → pull で学習

### Recipe Function（承認者特定）が必要な場合

```json
{
  "provider": "workato_recipe_function",
  "name": "execute",
  "input": {
    "parameters_schema_json": "[{\"name\":\"requestor_email\",\"type\":\"string\",...}]",
    "result_schema_json": "[{\"name\":\"manager_email\",\"type\":\"string\",...}]"
  }
}
```

- HRMS（Workday, BambooHR 等）への接続は UI で設定
- return_result で `result.manager_name` / `result.manager_email` を返す

### コネクション

必要な外部サービスの `.connection.json` を生成:
```json
{ "name": "<prefix> | <Provider>", "provider": "<provider>", "root_folder": false }
```

push:
```bash
workato push
```

## Phase 6: 動作確認

ユーザーに以下を案内:

```
push 完了。Workato UI で確認してください:
1. Workflow App にステージが反映されているか
2. レシピの構造が正しく表示されるか
3. 外部サービスのコネクション認証を設定
4. human_review のアサイン先が正しいか
5. テスト実行して動作確認

調整が必要な場合は pull してフィードバックをください。
```

## 出力

各 Phase 完了時に以下を表示:
- 生成/更新したファイル一覧
- 次の Phase の手順
- ユーザーに UI 操作が必要な場合はその内容
