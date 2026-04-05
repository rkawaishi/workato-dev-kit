---
description: Workato Workflow App（承認ワークフロー等）を構築する。UI 操作は App 有効化のみ。Data Table、ステージ、ページ、レシピは全て JSON で生成し push する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# /create-workflow-app

Workato Workflow App を構築するスキル。UI 操作は Workflow App の有効化のみ。それ以外（Data Table、ステージ、ページ、レシピ）は全て JSON で生成し push する。

## 使い方

- `/create-workflow-app` — 対話的に新しい Workflow App を構築
- `/create-workflow-app <name>` — 指定名で構築開始

## 前提知識

以下を参照する:
- `@docs/platform/workflow-apps.md` — 構築パターン、プロバイダー/アクション
- `@docs/learned-patterns.md` — Workflow App ファイル種別、レシピパターン
- `@.claude/rules/workato-agentic-format.md` — lcap_app / workato_db_table / lcap_page の JSON 構造

## Phase 1: 設計 + App 有効化

### ユーザーに確認

- **アプリの目的**: 何のリクエスト/承認フローか
- **Data Table のフィールド**: どんな情報を格納するか
- **ワークフローステージ**: どんな承認段階があるか（例: New → Manager review → Done / Canceled）
- **承認者の特定方法**: 固定ユーザー / HRMS から動的取得 / フォームで指定
- **外部連携**: 承認後に何をするか（Jira 起票、Slack 通知、メール送信等）

### ユーザーに依頼（唯一の UI 操作）

```
Workato UI で以下を実行してください:
1. Projects にプロジェクト「[App] <Name>」を作成（未作成の場合）
2. プロジェクト内で Workflow App を有効化

完了したら教えてください。
```

### プロジェクト初期化

```bash
workato init --non-interactive --profile default --project-id <id> --folder-name "projects/[App] <Name>"
```

または:
```bash
workato projects use "[App] <Name>" && echo "y" | workato pull
```

## Phase 2: 全構成要素を JSON で生成 → push

以下のファイルを一括生成する。

### 1. workato_db_table.json（Data Table スキーマ）

```json
{
  "name": "<テーブル名>",
  "schema": [
    { "id": "11fbe9a6-a16d-4d7e-86ea-afe42ec03005", "title": "Record ID", "type": "short-text", "read_only": true, "hidden": true },
    { "id": "a5612739-5401-4ae7-bd07-782c1a6fb2d1", "title": "Created time", "type": "date-time", "read_only": true, "hidden": true },
    { "id": "61aae604-a95e-4519-9091-bb0bf754a67f", "title": "Last modified time", "type": "date-time", "read_only": true, "hidden": true },
    { "id": "<uuidgen>", "title": "<フィールド名>", "type": "<型>", "read_only": false, "hidden": false, "required": true/false, "metadata": {} }
  ],
  "project_name": "[App] <Name>"
}
```

- システムフィールド3つの UUID は全テーブル共通
- ユーザー定義フィールドの UUID は `uuidgen` で新規生成
- type: `short-text`, `long-text`, `number`, `boolean`, `date`, `date-time`, `file`, `relation`

### 2. lcap_page.json（ページ定義）

4ページを生成:

**送信フォーム** (`submit_<name>.lcap_page.json`):
- input コンポーネント（`editable: true`）で各フィールド
- button コンポーネント（`handlers.click.type: "save-data"`）で送信
- `dataSource.id` には Data Table フィールドの **title**（UUID ではない）を指定

**レビューページ** (`review_<name>.lcap_page.json`):
- input コンポーネント（`editable: false`）でリクエスト内容を読み取り表示
- Review comments フィールドのみ `editable: true`

**承認済みページ** (`approved_page.lcap_page.json`):
- リクエスト内容の読み取り表示 + 「APPROVED」ステータス表示
- 外部連携結果（Jira チケットキー等）の表示

**却下ページ** (`rejected_page.lcap_page.json`):
- リクエスト内容の読み取り表示 + 「REJECTED」ステータス表示
- Review comments の表示

ページの JSON 構造:
```json
{
  "name": "ページ名",
  "path": "url-slug",
  "content": {
    "type": "common",
    "maxWidth": "fixed",
    "background": { "style": "pattern", "pattern": "light-2" },
    "variables": [],
    "handlers": { "pageLoad": null },
    "layout": [ /* コンポーネントツリー */ ]
  }
}
```

コンポーネント: 既存プロジェクトの lcap_page.json を参照してレイアウトを構成する。
各コンポーネントの `id` は8桁の hex を生成する。

### 3. lcap_app.json（Workflow App 定義 + ページ参照）

pull した lcap_app.json を更新。Data Table、ステージ、ページ参照を全て含める:

```json
{
  "name": "<App名>",
  "creation_page": { "zip_name": "submit_<name>.lcap_page.json", "name": "...", "folder": "" },
  "workato_db_table": { "zip_name": "<table>.workato_db_table.json", "name": "...", "folder": "" },
  "workflow_stages": [
    { "name": "New", "color": 0 },
    { "name": "<承認ステージ>", "color": 1,
      "task_page": { "zip_name": "review_<name>.lcap_page.json", "name": "...", "folder": "" } },
    { "name": "Done", "color": 2,
      "details_page": { "zip_name": "approved_page.lcap_page.json", "name": "...", "folder": "" } },
    { "name": "Canceled", "color": 3,
      "details_page": { "zip_name": "rejected_page.lcap_page.json", "name": "...", "folder": "" } }
  ],
  "tabs": [
    { "name": "Workflow requests", "kind": "new_request", "visibility": "all" }
  ],
  "displayed_columns": [
    { "id": "CURRENT_STAGE", "visibility": "all" },
    { "id": "ASSIGNED_TO", "visibility": "all" },
    { "id": "CREATED_BY", "visibility": "all" }
  ]
}
```

### 4. recipe.json（メインレシピ + Recipe Function）

承認ワークフローテンプレート:
```
[0] trigger: workato_workflow_task/new_requests_realtime (app_id → lcap_app)
  [1] action: workato_recipe_function/call_recipe（承認者を特定 ※動的の場合）
  [2] action: workato_workflow_task/human_review_on_existing_record
  [3] if: task.is_approved == true
    [4] action: 外部連携（Jira, Slack 等）
    [5] action: workato_workflow_task/update_request（結果を保存）
    [6] action: workato_workflow_task/change_workflow_stage → Done
  [7] else:
    [8] action: workato_workflow_task/change_workflow_stage → Canceled
```

レシピ生成時の注意:
- record_id は **trigger output** から一貫して取得
- Data Table UUID: input はハイフン区切り、output/datapill はアンダースコア区切り
- 外部連携のフィールドが不明な場合は `input: {}` にして push → UI で設定 → pull

### 5. connection.json（外部サービスコネクション）

```json
{ "name": "<prefix> | <Provider>", "provider": "<provider>", "root_folder": false }
```

### 一括 push

```bash
workato push
```

## Phase 3: 動作確認

```
push 完了。Workato UI で確認してください:
1. Workflow App にステージ・ページが反映されているか
2. 送信フォームからリクエストを送信できるか
3. レシピの構造が正しく表示されるか
4. コネクション認証の設定（外部サービス利用時）

調整が必要な場合は pull してフィードバックをください。
```

## 出力

各 Phase 完了時に:
- 生成したファイル一覧
- push 結果
- 次の手順（UI 操作が必要な場合はその内容）
