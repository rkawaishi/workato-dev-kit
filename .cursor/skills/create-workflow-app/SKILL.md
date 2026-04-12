---
name: create-workflow-app
description: Workato Workflow App（承認ワークフロー等）を構築する。UI 操作は App 有効化のみ。Data Table、ステージ、ページ、レシピは全て JSON で生成し push する。
---

# /create-workflow-app

Workato Workflow App を構築するスキル。UI 操作は Workflow App の有効化のみ。それ以外（Data Table、ステージ、ページ、レシピ）は全て JSON で生成し push する。

## 使い方

- `/create-workflow-app` — 対話的に新しい Workflow App を構築
- `/create-workflow-app <name>` — 指定名で構築開始

## 前提知識

以下を参照する:
- `docs/platform/workflow-apps.md` — 構築パターン、プロバイダー/アクション
- `docs/patterns/deployment-guide.md` — デプロイ手順、よくあるエラー
- `.cursor/rules/workato-agentic-format.mdc` — lcap_app / workato_db_table / lcap_page の JSON 構造

## Phase 1: 設計 + プロジェクト作成

### ユーザーに確認

- **アプリの目的**: 何のリクエスト/承認フローか
- **Data Table のフィールド**: どんな情報を格納するか
- **ワークフローステージ**: どんな承認段階があるか（例: New → Manager review → Done / Canceled）
- **承認者の特定方法**: 固定ユーザー / HRMS から動的取得 / フォームで指定
- **外部連携**: 承認後に何をするか（Jira 起票、Slack 通知、メール送信等）

### プロジェクト作成（CLI）

**ファイル生成前に** プロジェクトを CLI で作成する（ディレクトリ非空エラーを防ぐ）:

```bash
workato init --non-interactive --profile default --project-name "[App] <Name>" --folder-name "projects/[App] <Name>"
```

### Workflow App 有効化（唯一の UI 操作）

プロジェクト作成後、`.workatoenv` から `folder_id` を取得し、プロジェクト URL を案内:

```
Workato UI で Workflow App を有効化してください:

  URL: https://app.trial.workato.com/recipes?fid=<folder_id>

  1. プロジェクトを開く
  2. 「Workflow App」を有効化する（アプリ名は何でもOK、push で上書きされます）

完了したら教えてください。
```

> **補足**: Workato のリージョンによって URL のドメインが異なる（US: www.workato.com, EU: app.eu.workato.com, JP: app.jp.workato.com, Trial: app.trial.workato.com）。`workato profiles list` でリージョンを確認し、正しい URL を生成する。

## Phase 2: 全構成要素を JSON で生成 → push

ファイル配置は `.cursor/rules/workato-project-structure.mdc` に従う。

### 1. Data Tables/workato_db_table.json（Data Table スキーマ）

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

### 2. Pages/lcap_page.json（ページ定義）

4ページを生成:

**送信フォーム** (`Pages/submit_<name>.lcap_page.json`):
- テキスト系: `"type": "input"` + `"style": "short-text"` or `"long-text"`
- 数値: `"type": "input"` + `"style": "number"`
- 連絡先: `"type": "input"` + `"style": "email"` / `"phone"` / `"url"`（自動バリデーション付き）
- 日付系: **`"type": "date"`**（`"input"` + `"style": "date"` は NG — エディタが壊れる）
- 選択式: `"type": "dropdown"` + `"options"` で固定選択肢を定義。`"multiValue": true` で複数選択
- チェックボックス: `"type": "checkbox"`（※JSON type 要確認）→ Data Table の `boolean` 型
- ファイル: `"type": "file"`（※JSON type 要確認）→ Data Table の `file` 型
- button コンポーネント（`handlers.click.type`: `"save-data"` / `"complete-task"` / `"open-url"` / `"run-recipe"` / `"reset-reload"`）
- `dataSource` は **Data Table カラムへの保存先**を指定する。`dataSource.id` には Data Table フィールドの **title**（UUID ではない）を指定。`dataSource` が `null` だと送信時に値が保存されない

**コンポーネント type の対応表（重要）**:
| フィールド型 | `type` | `style` |
|---|---|---|
| short-text | `"input"` | `"short-text"` |
| long-text | `"input"` | `"long-text"` |
| number | `"input"` | `"number"` |
| email | `"input"` | `"email"` |
| phone | `"input"` | `"phone"` |
| url | `"input"` | `"url"` |
| date / date-time | **`"date"`** | 不要 |
| 選択式（単一） | **`"dropdown"`** | 不要 |
| 選択式（複数） | **`"dropdown"`** + `multiValue: true` | 不要 |
| チェックボックス | **`"checkbox"`** (※要確認) | 不要 |
| ファイル | **`"file"`** (※要確認) | 不要 |

**レビューページ** (`Pages/review_<name>.lcap_page.json`):
- input / date コンポーネント（`editable: false`）でリクエスト内容を読み取り表示
- Review comments フィールドのみ `editable: true`

**承認済みページ** (`Pages/approved_page.lcap_page.json`):
- リクエスト内容の読み取り表示 + 「APPROVED」ステータス表示
- 外部連携結果（Jira チケットキー等）の表示

**却下ページ** (`Pages/rejected_page.lcap_page.json`):
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
  "creation_page": { "zip_name": "Pages/submit_<name>.lcap_page.json", "name": "...", "folder": "Pages" },
  "workato_db_table": { "zip_name": "Data Tables/<table>.workato_db_table.json", "name": "...", "folder": "Data Tables" },
  "workflow_stages": [
    { "name": "New", "color": 0 },
    { "name": "<承認ステージ>", "color": 1,
      "task_page": { "zip_name": "Pages/review_<name>.lcap_page.json", "name": "...", "folder": "Pages" } },
    { "name": "Done", "color": 2,
      "details_page": { "zip_name": "Pages/approved_page.lcap_page.json", "name": "...", "folder": "Pages" } },
    { "name": "Canceled", "color": 3,
      "details_page": { "zip_name": "Pages/rejected_page.lcap_page.json", "name": "...", "folder": "Pages" } }
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

### 4. レシピは `/create-recipe` に委譲

Workflow App のレシピ（メインレシピ、Recipe Function）は `/create-recipe` スキルに委譲する:

- メインレシピの要件を整理してユーザーに提示:
  - トリガー: `workato_workflow_task/new_requests_realtime`
  - 必要なアクション: 承認、外部連携、ステージ変更
- `/create-recipe` を呼び出し、ヒアリング含むレシピ生成を実行
- Recipe Function が必要な場合も同様に `/create-recipe` で生成

典型的な承認ワークフローの構成:
```
メインレシピ:
  trigger → call_recipe(マネージャー取得) → human_review → if/else → 外部連携 → change_stage

Recipe Function:
  execute → HRMS 検索 → return_result
```

## Phase 3: デプロイと動作確認

`docs/patterns/deployment-guide.md` の「Workflow App のデプロイフロー」に従い、段階的に案内する:

1. **push**: `workato push` で全アセットを push
2. **コネクション認証を最初に案内**（push 直後、レシピ確認より先）:
   ```
   push 完了。まずコネクションの認証を行ってください:
   URL: https://<region>/recipes?fid=<folder_id>

   以下のコネクションを開いて認証情報を設定してください:
   - <connection_name_1> (<provider_1>)
   - <connection_name_2> (<provider_2>)
   ...

   認証が完了したら教えてください。
   ```
3. **認証完了後に UI 確認を案内**:
   ```
   次に以下を確認してください:
   1. Workflow App にステージ・ページが反映されているか
   2. 送信フォームのフィールド確認
   3. レシピを開いてフィールドマッピング確認
   ```
4. **テスト実行を案内**: フォーム送信 → 承認フロー全体のテスト
5. **調整があった場合**: pull → `/learn-recipe` で学習

## 出力

各 Phase 完了時に:
- 生成したファイル一覧
- push 結果
- **プロジェクト URL**（`.workatoenv` の `folder_id` + リージョンから生成）
- ユーザーが UI で行うべき操作を具体的に案内（デプロイガイド参照）
