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

### IF / ELSE IF / ELSE の keyword

| keyword | 用途 | 配置 | 条件 |
|---|---|---|---|
| `if` | 最初の条件分岐 | block 内のトップレベル | `input.conditions` 必須 |
| `elsif` | 追加の条件分岐（ELSE IF） | `if` の block 内の末尾 | `input.conditions` 必須 |
| `else` | 条件なしのデフォルト分岐 | `if` の block 内の末尾 | 条件不要 |

- `else` と `elsif` は `if` の `block` 配列の**末尾**に配置する（`if` と同レベルではない）
- 条件なしのデフォルト分岐には `else` を使う。`elsif` を条件なしで使うとエラーになる

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

## Workato のインポート/エクスポート挙動

- push 時に datapill を含む input を設定しても、UI でコネクタ未設定だと **空 `{}` にリセット**される
- `version` は UI で編集するたびに自動インクリメント
- コネクション名が微妙に変わることがある（例: `helpdesk_ai` → `helpdesk_ai_by_workato`）
- 別プロジェクトのコネクションを参照する場合、`account_id.folder` にプロジェクト名が入る
- `pull` で削除確認が入る場合がある（`echo "y" | workato pull` で自動承認）

## Data Table UUID 規則

- **input 参照時**: ハイフン区切り UUID（`11fbe9a6-a16d-4d7e-86ea-afe42ec03005`）
- **output スキーマ / datapill パス**: アンダースコア区切り UUID（`11fbe9a6_a16d_4d7e_86ea_afe42ec03005`）
- **`parameters` フィールド内の UUID キー**: アンダースコア区切りが正しい
- `add_record`（`create_record` ではない）— アクション名に注意

## ページコンポーネントの `type` とフィールド型の対応

| Data Table フィールド型 | コンポーネント `type` | 備考 |
|---|---|---|
| `short-text` | `"input"` | `style: "short-text"` |
| `long-text` | `"input"` | `style: "long-text"`, `textareaHeight` 指定可 |
| `number` | `"input"` | `style: "number"` |
| `boolean` | `"input"` | `style: "checkbox"` (要確認) |
| `date` | `"date"` | **`"input"` ではない。`style` 不要** |
| `date-time` | `"date"` | (要確認) |
| `file` | (要確認) | |

**注意**: date 型フィールドに `"type": "input"` + `"style": "date"` を使うとページエディタが無限ロードになる。必ず `"type": "date"` を使うこと。

## Slack コネクタの固有知見

### `slack` vs `slack_bot` のイベント指定

| | `slack`（標準） | `slack_bot`（Workbot） |
|---|---|---|
| イベント種別フィールド | `input.webhook_suffix` | `input.event_name` |
| dynamicPickListSelection | なし | あり |

- 標準コネクタでは `reaction_added` イベント購読や `channels.history` 権限がない
- これらが必要な場合は `slack_bot` + Custom OAuth profile を使用

---
*最終更新: Workflow App 詳細、MCP Server、Gmail Custom Action、try キーワードを各専門ドキュメントに移動*
