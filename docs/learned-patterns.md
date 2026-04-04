# Learned Patterns（独自知見）

公式ドキュメントに載っていない、UI フィードバックから学んだ知見。
`/learn-recipe` で自動更新される。

## JSON 構造の非公開仕様

### Datapill 記法

```
#{_dp('{"pill_type":"output","provider":"<provider>","line":"<as>","path":["field"]}')}
```

- `provider`: ステップの provider 名
- `line`: ステップの `as` 値
- `path`: フィールドパス配列。リストの現在アイテムは `{"path_element_type":"current_item"}`

```ruby
#{_('data.provider.step.field')}                    # ドット記法
=_('data.provider.step.list').pluck('f').join(', ') # Ruby式
```

### `as` フィールドの命名規則

- **通常レシピ**: アクション名と同じ値（例: `new_email`, `post_message`）
- **Genie スキルレシピ**: ランダム 8文字 hex（例: `a7c3e1f9`）
- **slack_bot コネクタ**: 通常レシピでもランダム 8文字 hex

### Genie 呼び出し: `assign_task_to_genie`

レシピから Genie を呼び出すアクション:
```json
{
  "provider": "workato_genie",
  "name": "assign_task_to_genie",
  "dynamicPickListSelection": { "genie_handle": "Genie名" },
  "toggleCfg": { "genie_handle": true },
  "input": {
    "genie_handle": { "zip_name": "genie.agentic_genie.json", "name": "Genie名", "folder": "" },
    "task_instructions": "タスク指示文（datapill 可）"
  }
}
```

### Genie スキルレシピのパラメータ

- パラメータ参照: `path:["parameters","<param_name>"]` — `parameters` 配下にネスト
- `workflow_return_result` の入力: `input.result.<field>` に個別マッピング
```json
"input": {
  "result": {
    "field1": "#{_dp('...')}",
    "field2": "#{_dp('...')}"
  }
}
```

### Genie スキル: `start_workflow` のスキーマ例

`parameters_schema_json` と `result_schema_json` は JSON 文字列として格納される。
`extended_output_schema` には `parameters` オブジェクト配下にパラメータが展開される。

**確認済みスキーマ例 (Search similar Jira tickets):**

| スキーマ | フィールド | 型 | 説明 |
|---|---|---|---|
| parameters_schema_json | search_keyword | string | 検索キーワード |
| result_schema_json | issue_key | string | Issue key |
| result_schema_json | summary | string | Summary |
| result_schema_json | description | string | Description |
| result_schema_json | comment | string | Comment |

`workflow_return_result` の `extended_output_schema` / `extended_input_schema` は `result` オブジェクト配下に result_schema_json のフィールドが展開される。

### Custom Action (`__adhoc_http_action`)

コネクタに適切なアクションがない場合、API を直接呼び出す:
```json
{
  "provider": "<connector>",
  "name": "__adhoc_http_action",
  "as": "<任意の参照名>",
  "input": {
    "mnemonic": "表示名",
    "verb": "get|post|put|delete",
    "response_type": "json",
    "path": "api/endpoint",
    "input": {
      "schema": "[{...スキーマJSON文字列...}]",
      "data": { "param": "#{_dp('...')}" }
    },
    "output": "[{...レスポンススキーマJSON文字列...}]"
  },
  "extended_output_schema": [...],
  "extended_input_schema": [...],
  "visible_config_fields": [...],
  "wizardFinished": true
}
```

- `name` は常に `"__adhoc_http_action"`（全コネクタ共通）
- コネクタの認証・base URI を利用しつつ任意の API エンドポイントを呼べる

## Slack コネクタの固有知見

### `slack` vs `slack_bot` のイベント指定

| | `slack`（標準） | `slack_bot`（Workbot） |
|---|---|---|
| イベント種別フィールド | `input.webhook_suffix` | `input.event_name` |
| dynamicPickListSelection | なし | あり |

- 標準コネクタでは `reaction_added` イベント購読や `channels.history` 権限がない
- これらが必要な場合は `slack_bot` + Custom OAuth profile を使用

## Workato のインポート/エクスポート挙動

- push 時に datapill を含む input を設定しても、UI でコネクタ未設定だと **空 `{}` にリセット**される
- `version` は UI で編集するたびに自動インクリメント
- コネクション名が微妙に変わることがある（例: `helpdesk_ai` → `helpdesk_ai_by_workato`）
- 別プロジェクトのコネクションを参照する場合、`account_id.folder` にプロジェクト名が入る
- `pull` で削除確認が入る場合がある（`echo "y" | workato pull` で自動承認）

## コネクション参照の構造

```json
"account_id": {
  "zip_name": "file.connection.json",  // 同一プロジェクト
  "name": "Display Name",
  "folder": ""
}
```

```json
"account_id": {
  "zip_name": "Other Project/file.connection.json",  // 別プロジェクト
  "name": "Display Name",
  "folder": "Other Project"
}
```

## MCP Server JSON (`*.mcp_server.json`)

### ファイル構造

```json
{
  "name": "サーバー名",
  "description": "MCP サーバーの説明（AI がサーバー選択に使用）",
  "auth_type": "workato_idp",
  "tools_type": "project_assets",
  "tools": [
    {
      "tool": "ref_0",
      "description": "ツールの使用条件（AI がツール選択に使用）",
      "vua_required": true
    }
  ],
  "references": {
    "ref_0": {
      "type": "agentic_skill",
      "id": {
        "zip_name": "Folder/skill_name.agentic_skill.json",
        "name": "skill_name",
        "folder": "Folder"
      }
    }
  }
}
```

### 構造の関係

```
mcp_server.json
  └── tools[] → references → agentic_skill.json (複数可)
                                └── references.recipe_id → recipe.json
```

- MCP サーバーは複数のツール（tools）を持つ
- 各ツールは `ref_N` キーで `references` 内の agentic_skill を参照
- 各 agentic_skill は1つのレシピに紐づく
- `description` フィールドは AI がツール選択に使う詳細な指示（「Use this tool when...」「Do not use this tool when...」形式）
- `vua_required: true` は Verified User Access（エンドユーザーの認証情報で API 呼出し）が必要であることを示す

### 確認済みの値

- `auth_type`: `"workato_idp"` — Workato Identity Provider 認証
- `tools_type`: `"project_assets"` — プロジェクト内のアセットをツールとして公開

### Gmail MCP Server の例

Gmail サーバーでは 20 個のツール/スキルが定義されている:
search_threads, search_messages, list_labels, get_thread, get_message, list_attachments, add_labels, remove_labels, unstar_messages, star_messages, unarchive_threads, archive_threads, create_draft, get_draft, update_draft, send_draft, mark_message_read_state, list_drafts, add_attachments, remove_attachments

## Gmail カスタムアクションのパターン

- Gmail は `gmail` プロバイダーで `__adhoc_http_action` を使用
- パス例: `me/messages/{messageId}?format=full` — Gmail API の REST エンドポイント
- base URI は Gmail API（`https://gmail.googleapis.com/gmail/v1/users/`）

## レシピの新しいキーワード: `try`

- `keyword: "try"` はエラーハンドリングブロック（try/catch パターン）を示す
- `docs/logic/error-handling.md` の Monitor/Error ブロックに対応するJSON表現
- try ブロック内のステップでエラーが発生した場合、catch ブロック（エラーハンドラー）に制御が移る

## Workflow App ファイル種別

### `.lcap_app.json` — Workflow App 定義

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

### `.workato_db_table.json` — Data Table スキーマ

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

### `.lcap_page.json` — Workflow App ページ定義

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
    "layout": [ ... ]
  }
}
```

- `content.layout` はネストされたコンポーネントツリー（container, text, image, input, divider 等）
- 各コンポーネントは `type`, `id`（8桁hex）, `name`, `x`, `width`, `visible` を持つ
- `input` コンポーネントの `dataSource.id` は Data Table のフィールド title と対応
- ページは非常に大きくなるため（数百〜数千行）、通常は参照のみで直接編集しない
- `.lcap_page.zip` も存在する — UI アセット（画像等）のバイナリ、編集不可

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

### `workato_workflow_task` プロバイダー — 全アクション一覧

Workflow App のトリガー・アクションに使用されるプロバイダー:

**トリガー:**

| アクション名 | 用途 | 主要 input |
|---|---|---|
| `new_requests_realtime` | 新規リクエスト送信時にリアルタイム発火 | `app_id` |
| `app_function_generic_request` | 汎用アプリ関数（ボタン等から呼出） | `parameters_schema_json` |
| `app_function_load_table_request` | テーブルウィジェット用データ読込 | `table_schema_json`, `parameters_schema_json` |
| `app_function_load_dropdown_request` | ドロップダウンウィジェット用データ読込 | `search_enabled` |

**アクション:**

| アクション名 | 用途 | 主要 input |
|---|---|---|
| `human_review_on_existing_record` | タスクアサイン＆承認/却下待ち | `app_id`, `record_id`, `name`, `email`, `workflow_stage_id`, `page_id` |
| `change_workflow_stage` | ワークフローステージ変更 | `project_id`（lcap_app参照）, `record_id`, `workflow_stage_id` |
| `update_request` | リクエストレコードのフィールド更新 | `app_id`, `record_id`, `parameters` |
| `app_function_return` | アプリ関数の結果を UI に返却 | `rows`（テーブル用）or `items`（ドロップダウン用） |

### `workato_db_table` プロバイダー — Data Table 操作

| アクション名 | 用途 | 主要 input |
|---|---|---|
| `get_records` | Data Table からレコード取得 | `table_id`, `limit`, `order_direction`, `filters` |
| `update_record` | Data Table のレコード更新 | `table_id`, `record_id`, `parameters` |

**`get_records` のフィルタ構造:**
```json
"filters": [
  {
    "field_id": "UUID-with-hyphens",
    "op_id": "eq",
    "value_default": "#{_dp('...')}"
  }
]
```

### `workato_recipe_function` プロバイダー — レシピ関数呼び出し

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

## Workflow App レシピパターン（典型フロー）

### パターン 1: 承認ワークフロー

Generic Workflow Request, Application Access, Expense Reimbursement で共通:
```
new_requests_realtime トリガー
  → [optional] call_recipe（外部データ取得、例: マネージャー情報）
  → [optional] update_request（リクエストにデータ追加）
  → human_review_on_existing_record（タスクアサイン＆承認待ち）
  → if (task.is_approved)
      → change_workflow_stage("Done" / "Approved")
    else
      → change_workflow_stage("Canceled" / "Rejected")
```

### パターン 2: テーブルウィジェットデータ取得

```
app_function_load_table_request トリガー
  → workato_db_table.get_records
  → app_function_return (rows)
```

`app_function_return` の `rows` 入力:
```json
{
  "rows": {
    "____source": "#{_dp('...records...')}",
    "ColumnName": "#{_dp('...records.current_item.uuid_field...')}"
  }
}
```

### パターン 3: ドロップダウンデータ取得

```
app_function_load_dropdown_request トリガー
  → workato_db_table.get_records
  → app_function_return (items)
```

`app_function_return` の `items` 入力:
```json
{
  "items": {
    "____source": "#{_dp('...records...')}",
    "value": "#{_dp('...record_id_field...')}",
    "label": "#{_dp('...display_field...')}"
  }
}
```

### パターン 4: データ更新アプリ関数

```
app_function_generic_request トリガー（parameters でパラメータ受取）
  → workato_db_table.get_records（フィルタで対象レコード検索）
  → if (レコードが存在)
      → workato_db_table.update_record
```

### Data Table カラム ID の UUID 規則

- **input 参照時**: ハイフン区切り UUID（`11fbe9a6-a16d-4d7e-86ea-afe42ec03005`）
- **output スキーマ / datapill パス**: アンダースコア区切り UUID（`11fbe9a6_a16d_4d7e_86ea_afe42ec03005`）
- 共通の予約カラム（全 Data Table 共通）:
  - `11fbe9a6-a16d-4d7e-86ea-afe42ec03005` = **Record ID**
  - `a5612739-5401-4ae7-bd07-782c1a6fb2d1` = **Created at**
  - `61aae604-a95e-4519-9091-bb0bf754a67f` = **Updated at**

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

---
*最終更新: Workflow App レシピパターン（承認フロー、テーブル/ドロップダウン関数、データ更新）、全プロバイダー・アクション一覧追加*
