# Workflow Apps

公式: https://docs.workato.com/en/workflow-apps.html

## 概要

ノーコードのビジュアル開発プラットフォーム。ユーザー操作と自動化ステップを組み合わせたインタラクティブなアプリケーションを構築できる。

## 主要コンポーネント

### データストレージ
- 統合された Data Tables でレコード（請求書、リクエスト等）を格納
- リンクされた複数テーブルをサポート
- Workflow Apps コネクタ経由でレシピからアクセス
- レシピをリアルタイムデータソースとして使用可能

### ユーザーインターフェース
- ポータル（リクエスト一覧、ナビゲーション）を自動生成
- **Pages**: ドラッグ＆ドロップエディタでカスタムフォーム・ダッシュボードを作成
- 条件付きロジック、バリデーション、フォームのプリフィル
- 公開フォーム（外部ユーザー向け）

### ビジネスロジック
- ワークフローレシピでルーティング、承認、データ更新、システム連携を管理
- New request トリガーでフォーム送信を処理
- タスクのアサインとワークフロー状態遷移

## 動作フロー

```
UI イベント（フォーム送信等）
  → レシピがトリガー
  → 外部データの取得/更新
  → 結果を UI コンポーネントに返却
```

承認ワークフロー:
```
フォーム送信 → New request トリガー → Data Table にレコード作成
  → ビジネスロジック評価 → タスクアサイン → 承認/却下
```

## 主な用途

- 部門管理（HR、Finance、IT）
- 自動化プロセスの例外処理
- リクエストのルーティングと承認
- カスタムアプリケーション・フロントエンド

## レシピで使用するプロバイダーとアクション

### `workato_workflow_task` プロバイダー

Workflow App 専用のトリガーとアクション。

**トリガー:**
- `new_requests_realtime` — 新規リクエスト送信時のリアルタイムトリガー。`input.app_id` で対象 Workflow App を指定
- `app_function_generic_request` — 汎用アプリ関数トリガー（ボタン操作等）。`parameters_schema_json` でパラメータ定義
- `app_function_load_table_request` — テーブルウィジェットのデータ読み込み。`table_schema_json` でカラム定義
- `app_function_load_dropdown_request` — ドロップダウンのオプション読み込み

**アクション:**
- `human_review_on_existing_record` — タスクアサイン＆承認/却下待ち（ブロッキング）
- `change_workflow_stage` — ワークフローステージの変更（例: New → In progress → Done）
- `update_request` — リクエストレコードのフィールド更新
- `app_function_return` — アプリ関数の結果を UI に返却（`rows` でテーブル、`items` でドロップダウン）

### `workato_db_table` プロバイダー

Data Table への直接 CRUD 操作。

- `get_records` — レコード取得（フィルタ、ソート、ページネーション対応）
- `update_record` — レコード更新

### `workato_recipe_function` プロバイダー

- `call_recipe` — 別レシピを関数として呼び出し。外部データ取得（HRMS 等）のラッパーとして使用

### `workato_workflow_task` の詳細 input 一覧

**トリガー詳細:**

| アクション名 | 主要 input |
|---|---|
| `new_requests_realtime` | `app_id` |
| `app_function_generic_request` | `parameters_schema_json` |
| `app_function_load_table_request` | `table_schema_json`, `parameters_schema_json` |
| `app_function_load_dropdown_request` | `search_enabled` |

**アクション詳細:**

| アクション名 | 主要 input |
|---|---|
| `human_review_on_existing_record` | `app_id`, `record_id`, `name`, `email`, `workflow_stage_id`, `page_id` |
| `change_workflow_stage` | `project_id`（lcap_app参照）, `record_id`, `workflow_stage_id` |
| `update_request` | `app_id`, `record_id`, `parameters` |
| `app_function_return` | `rows`（テーブル用）or `items`（ドロップダウン用） |

### `human_review_on_existing_record` の詳細構造

```json
{
  "provider": "workato_workflow_task",
  "name": "human_review_on_existing_record",
  "keyword": "action",
  "dynamicPickListSelection": {
    "user_group_id": "グループ名（optional）",
    "workflow_stage_id": "In progress"
  },
  "toggleCfg": {
    "send_email_notification": true,
    "reassignable": true,
    "workflow_stage_id": true,
    "due_in_days": true
  },
  "input": {
    "app_id": { "zip_name": "...", "name": "App Name", "folder": "" },
    "record_id": "#{_dp('...')}",
    "name": "タスク名（datapill 可）",
    "email": "#{_dp('...created_by.email...')}",
    "workflow_stage_id": { "name": "In progress" },
    "due_in_days": "14",
    "send_email_notification": "true",
    "reassignable": "true",
    "page_id": { "zip_name": "Pages/page.lcap_page.json", "name": "Page Name", "folder": "Pages" }
  }
}
```

出力: `task` オブジェクト（`is_approved` boolean, `assigned_user`, `assigned_group`, `expires_at`, `link`）と `record` オブジェクト。

### `workato_db_table` プロバイダーの詳細

| アクション名 | 用途 | 主要 input |
|---|---|---|
| `add_record` | Data Table にレコード作成 | `table_id`, `parameters` |
| `get_records` | Data Table からレコード取得 | `table_id`, `limit`, `order_direction`, `filters` |
| `update_record` | Data Table のレコード更新 | `table_id`, `record_id`, `parameters` |

#### `add_record` の注意点

- アクション名は `add_record`（`create_record` ではない）
- `parameters` のフィールドキーは **アンダースコア区切り** の UUID（ハイフンではない）
  ```json
  "parameters": {
    "b1a2c3d4_e5f6_4a7b_8c9d_100000000001": "値"
  }
  ```
- `update_request` の `parameters` も **アンダースコア区切り** を使う（ハイフンではない）
- **全ての `parameters` フィールド内の UUID キーはアンダースコア区切り** が正しい
- `extended_input_schema` の `parameters` 内に Data Table の全フィールドがスキーマとして展開される

#### `get_records` のフィルタ構造

```json
"filters": [
  {
    "field_id": "UUID-with-hyphens",
    "op_id": "eq",
    "value_default": "#{_dp('...')}"
  }
]
```

### `workato_recipe_function` の詳細構造

```json
{
  "provider": "workato_recipe_function",
  "name": "call_recipe",
  "keyword": "action",
  "dynamicPickListSelection": { "flow_id": "レシピ名" },
  "input": {
    "flow_id": "数値ID（文字列）",
    "parameters": { "ParamName": "値またはdatapill" }
  }
}
```

- 出力は `result` オブジェクト配下に呼び出し先レシピの返り値が格納される
- `skip: true` が設定されている場合、そのステップはスキップされる（プレースホルダー用途）

### Workflow App の特殊フィールド型

- `custom_type: "relation"` — 他テーブルへのリレーション。`record_id` と `display_name` を持つ
- `custom_type: "file"` — ファイルフィールド。`filename` と `file_content` を持つ
- `created_by` — 共通の作成者オブジェクト（`id`, `name`, `email`, `status`, `user_groups[]`, `is_guest`）
- `stage` — ワークフローステージ（`id`, `name`）
- `task` — アクティブタスク（`id`, `name`, `status`, `assigned_user`, `assigned_group`, `expires_at`, `link`）

### `extended_input_schema` の内部型宣言（Data Table）

Data Table の `get_records` では、`extended_input_schema` にカラムの型宣言が隠しフィールドとして格納される:
```json
{
  "label": "$internal_value_<uuid-with-hyphens>",
  "name": "<uuid-with-hyphens>",
  "default": "string|date|date_time|id",
  "ngIf": "false",
  "optional": true,
  "type": "string"
}
```

## レシピからの Data Table 参照

レシピ内で Data Table を参照する際は `table_id` に zip 参照を使用:
```json
"table_id": {
  "zip_name": "employees.workato_db_table.json",
  "name": "Employees",
  "folder": ""
}
```

Data Table のカラムは UUID で識別される。レシピ JSON 内では:
- **input フィールド名**: ハイフン区切り（`11fbe9a6-a16d-4d7e-86ea-afe42ec03005`）
- **output / datapill パス**: アンダースコア区切り（`11fbe9a6_a16d_4d7e_86ea_afe42ec03005`）

全テーブル共通の予約カラム:
- `11fbe9a6-...` = Record ID
- `a5612739-...` = Created at
- `61aae604-...` = Updated at

## 典型的なレシピフロー

### 承認ワークフロー
```
new_requests_realtime → call_recipe（外部データ取得）→ update_request
  → human_review_on_existing_record → if/else → change_workflow_stage
```

### テーブルウィジェットデータ取得
```
app_function_load_table_request → get_records → app_function_return(rows)
```

### ドロップダウンデータ取得
```
app_function_load_dropdown_request → get_records → app_function_return(items)
```

### app_function_return の入力構造

**テーブルウィジェット (`rows`):**
```json
{
  "rows": {
    "____source": "#{_dp('...records...')}",
    "ColumnName": "#{_dp('...records.current_item.uuid_field...')}"
  }
}
```

**ドロップダウン (`items`):**
```json
{
  "items": {
    "____source": "#{_dp('...records...')}",
    "value": "#{_dp('...record_id_field...')}",
    "label": "#{_dp('...display_field...')}"
  }
}
```

### データ更新アプリ関数パターン
```
app_function_generic_request トリガー（parameters でパラメータ受取）
  → workato_db_table.get_records（フィルタで対象レコード検索）
  → if (レコードが存在)
      → workato_db_table.update_record
```

## Workflow App 構築パターン

### 構築の流れ

Workflow App 本体の有効化のみ UI 操作が必要。それ以外は全て JSON で定義し push できる。

```
1. Workato UI でプロジェクト内の Workflow App を有効化（1回のみ）
2. JSON で全構成要素を定義 → push
   - workato_db_table.json（Data Table スキーマ）
   - lcap_app.json（ステージ、ページ参照、表示カラム）
   - lcap_page.json（ページ定義: フォーム、レビュー、承認/却下）
   - recipe.json（ワークフローレシピ）
   - connection.json（外部サービスコネクション）
3. pull → 調整 → push のサイクルを繰り返す
```

### 何が JSON で定義でき、何が UI 必須か

| 要素 | JSON で定義可能 | UI 必須 |
|---|---|---|
| Workflow App の有効化 | ❌ | ✅ UI で1回だけ |
| ワークフローステージ | ✅ `lcap_app.json` の `workflow_stages` | |
| Data Table スキーマ | ✅ `workato_db_table.json` | |
| 表示カラム | ✅ `lcap_app.json` の `displayed_columns` | |
| タブ | ✅ `lcap_app.json` の `tabs` | |
| ページ（フォーム、レビュー画面等） | ✅ `lcap_page.json` | |
| ページの紐付け | ✅ `creation_page`, `task_page`, `details_page` | |
| レシピ | ✅ `.recipe.json` | |
| コネクション | ✅ `.connection.json`（認証は UI） | |

### ページの JSON 構造

ページ（`lcap_page.json`）は JSON で定義して push できる。既存プロジェクトのページを参考にレイアウトを構成する。

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
    "layout": [ /* ネストされたコンポーネントツリー */ ]
  }
}
```

主要コンポーネント:
- `container` — レイアウトコンテナ（`x`, `width`, `backgroundColor`, `padding`）
- `text` — テキスト表示（マークダウン対応、`text`, `color`, `alignment`）
- `input` — テキスト系入力フィールド（short-text, long-text, number）
- `date` — 日付入力フィールド（**`"input"` ではなく `"date"` を使う**）
- `button` — ボタン（`handlers.click.type: "save-data"` で送信）
- `image` — 画像（`image: "illustration-N"` でプリセット画像）
- `divider` — 区切り線

**コンポーネント type とフィールド型の対応**（重要）:

| Data Table フィールド型 | コンポーネント `type` | `style` |
|---|---|---|
| `short-text` | `"input"` | `"short-text"` |
| `long-text` | `"input"` | `"long-text"` |
| `number` | `"input"` | `"number"` |
| `date` | **`"date"`** | 不要 |
| `date-time` | **`"date"`** | 不要 |

> **注意**: date 型に `"type": "input"` + `"style": "date"` を使うとページエディタが壊れる（無限ロード）。

`dataSource.id` は Data Table のフィールド **title**（UUID ではない）を指定する。

### ページ参照の扱い

`lcap_app.json` でページファイルと同時に push すれば、ページ参照も正しく解決される。

```json
{
  "creation_page": {
    "zip_name": "submit_form.lcap_page.json",
    "name": "Submit form",
    "folder": ""
  },
  "workflow_stages": [
    { "name": "Manager review", "color": 1,
      "task_page": { "zip_name": "review.lcap_page.json", "name": "Review", "folder": "" }
    }
  ]
}
```

### 必要なファイル一式

典型的な承認ワークフローアプリ:

```
projects/[App] <Name>/
├── <name>.lcap_app.json                    # Workflow App 定義
├── <name>.lcap_app.png                     # アプリアイコン（自動生成）
├── <table_name>.workato_db_table.json      # Data Table スキーマ
├── <main_recipe>.recipe.json               # メインレシピ（承認フロー）
├── fnc_<helper>.recipe.json                # Recipe Function（マネージャー取得等）
├── <connection>.connection.json            # 外部サービスコネクション
├── <page>.lcap_page.json + .zip            # ページ定義（UI で作成後 pull で取得）
└── <query>.insights_query.json             # 分析クエリ（UI で作成後 pull で取得）
```

### 承認ワークフローのレシピテンプレート

```
[0] trigger: new_requests_realtime (app_id → lcap_app)
  [1] action: call_recipe (HRMS からマネージャー取得)
  [2] action: human_review_on_existing_record
        - email: call_recipe の result.manager_email（動的）
        - record_id: trigger の request.Record_ID（一貫して trigger から取得）
  [3] if: task.is_approved == true
    [4] action: 外部システム連携（Jira 起票、Slack 通知等）
    [5] action: update_request（結果をレコードに保存）
    [6] action: change_workflow_stage → Done
  [7] else:
    [8] action: change_workflow_stage → Canceled
```

### `.lcap_app.json` — Workflow App 定義（詳細）

```json
{
  "name": "App名",
  "creation_page": {
    "zip_name": "submit_form.lcap_page.json",
    "name": "Submit form",
    "folder": ""
  },
  "workato_db_table": {
    "zip_name": "table_name.workato_db_table.json",
    "name": "Table Name",
    "folder": ""
  },
  "workflow_stages": [
    { "name": "New", "color": 0 },
    {
      "name": "In progress", "color": 1,
      "task_page": { "zip_name": "...", "name": "...", "folder": "" },
      "details_page": { "zip_name": "...", "name": "...", "folder": "" }
    },
    { "name": "Done", "color": 2, "details_page": { "..." } },
    { "name": "Canceled", "color": 3, "details_page": { "..." } }
  ],
  "tabs": [
    { "name": "Tab名", "kind": "new_request", "visibility": "all" },
    { "name": "Analytics", "kind": "user_defined", "visibility": "managers",
      "page": { "zip_name": "analytics.lcap_page.json", "name": "...", "folder": "" } }
  ],
  "displayed_columns": [
    { "id": "UUID or CURRENT_STAGE|CURRENT_TASK|ASSIGNED_TO|EXPIRES_AT|CREATED_BY", "visibility": "all|managers|nobody" }
  ]
}
```

- `creation_page`: リクエスト送信フォームの lcap_page を参照
- `workato_db_table`: バックエンドの Data Table を参照
- `workflow_stages`: ステージ一覧。各ステージに `task_page`（タスク実行画面）と `details_page`（詳細表示画面）を持てる
- `tabs`: アプリのタブ。`kind` は `new_request`（デフォルト）/ `user_defined`（カスタムページ）
- `displayed_columns`: テーブルビューで表示するカラム。UUID は Data Table のフィールド ID、大文字はシステムカラム
- `color`: ステージの色コード（0=New, 1=In progress, 2=Done/完了系, 3=Canceled, 8=中間ステージ）

### `.workato_db_table.json` — Data Table スキーマ（詳細）

```json
{
  "name": "テーブル名",
  "schema": [
    {
      "id": "UUID",
      "title": "フィールド名",
      "type": "short-text|long-text|number|boolean|date|date-time|file|relation",
      "read_only": false,
      "hidden": false,
      "required": false,
      "default_value": "デフォルト値（省略可）",
      "hint": "入力ヒント（省略可）",
      "metadata": {},
      "relation": {
        "table_id": { "zip_name": "other.workato_db_table.json", "name": "Other Table", "folder": "" },
        "field_id": "UUID"
      }
    }
  ],
  "project_name": "[App] Project Name"
}
```

- システムフィールド（Record ID, Created time, Last modified time）は `read_only: true, hidden: true`
- `type: "relation"` の場合、`relation` オブジェクトで外部テーブルとフィールドを参照
- フィールド ID は UUID v4 形式。レシピの output やページ内で UUID がカラム名として使われる
- `project_name`: このテーブルが属するプロジェクト名

### `.insights_query.json` — Insights クエリ定義

```json
{
  "page_id": { "zip_name": "page.lcap_page.json", "name": "Page Name", "folder": "" },
  "name": "クエリ名",
  "index": 0,
  "version": "v1",
  "query": {
    "relation": "Aggregate",
    "groupKey": [],
    "aggCalls": [
      { "qualifier": "hex16桁", "function": "COUNT", "operand": null }
    ],
    "input": {
      "relation": "TableScan",
      "catalog": "lcap",
      "schema": "public",
      "table": "__ref__1",
      "columnQualifiers": [
        { "column": "workflow_stage|UUID|assignee|creator|...", "qualifier": "hex16桁" }
      ]
    }
  },
  "references": {
    "__ref__1": {
      "type": "lcap_app",
      "id": { "zip_name": "app.lcap_app.json", "name": "App Name", "folder": "" }
    }
  }
}
```

- `page_id`: このクエリが表示される lcap_page を参照
- `references.__ref__N`: クエリ対象の lcap_app を参照（テーブルスキャン先）
- `columnQualifiers` の `column` には UUID（Data Table フィールド ID）やシステムカラム名が使われる
- `aggCalls` の `function`: `COUNT`, `SUM`, `AVG` 等の集約関数

### push/pull サイクルの注意

- push した JSON は Workato 側で変換される（`extended_output_schema` 展開、`dynamicPickListSelection` 追加、`version` インクリメント）
- pull すると push 時と異なるファイルが返ってくるのは正常動作
- `creation_page: null` で push → UI でページ作成後 pull すると参照が自動設定される
