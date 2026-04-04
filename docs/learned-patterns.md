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

---
*最終更新: MCP Server JSON 形式、Gmail パターン、try キーワード追加*
