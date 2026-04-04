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
