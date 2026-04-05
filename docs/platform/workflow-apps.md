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

詳細なパターンと JSON 構造は `docs/learned-patterns.md` の「Workflow App レシピパターン」セクションを参照。

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
- `input` — 入力フィールド（`dataSource.id` で Data Table フィールド名を参照、`editable`, `validations`）
- `button` — ボタン（`handlers.click.type: "save-data"` で送信）
- `image` — 画像（`image: "illustration-N"` でプリセット画像）
- `divider` — 区切り線

input の `dataSource.id` は Data Table のフィールド **title**（UUID ではない）を指定する。

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

### push/pull サイクルの注意

- push した JSON は Workato 側で変換される（`extended_output_schema` 展開、`dynamicPickListSelection` 追加、`version` インクリメント）
- pull すると push 時と異なるファイルが返ってくるのは正常動作
- `creation_page: null` で push → UI でページ作成後 pull すると参照が自動設定される
