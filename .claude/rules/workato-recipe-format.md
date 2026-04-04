---
paths:
  - "**/*.recipe.json"
---

# Workato Recipe JSON Format

## トップレベル構造

```json
{
  "name": "レシピ名",
  "description": "マークダウン対応の説明文",
  "version": 1,
  "private": true,
  "concurrency": 1,
  "code": { /* トリガー + アクションツリー */ },
  "config": [ /* コネクション設定 */ ]
}
```

## code: ステップツリー（再帰構造）

各ステップは以下のフィールドを持つ:

| フィールド | 型 | 説明 |
|---|---|---|
| `number` | int | ステップ番号（0始まり、トリガーが0） |
| `provider` | string | コネクタ名（例: `gmail`, `slack`, `salesforce`） |
| `name` | string | アクション名（例: `new_email`, `post_message`） |
| `as` | string | ステップの参照名（datapill で使用） |
| `keyword` | string | `"trigger"` / `"action"` / `"foreach"` |
| `input` | object | 入力パラメータ（datapill 参照を含む） |
| `block` | array | 子ステップの配列（ネスト可） |
| `filter` | object | 条件フィルタ（optional） |
| `comment` | string | ステップのコメント（optional） |
| `uuid` | string | UUID v4 |
| `extended_output_schema` | array/null | カスタム出力スキーマ（optional） |
| `extended_input_schema` | array/null | カスタム入力スキーマ（optional） |

### Slack イベントトリガー

```json
{
  "provider": "slack",
  "name": "new_event",
  "keyword": "trigger",
  "input": {
    "webhook_suffix": "reaction_added"
  }
}
```

- イベント種別は `webhook_suffix` フィールドで指定（`event_type` ではない）

### keyword の種別

- `"trigger"` — レシピの起点（number: 0 のステップ）
- `"action"` — 通常のアクションステップ
- `"foreach"` — ループ。`source` フィールドでイテレート対象を指定、`block` に子ステップ

### Genie ワークフロー用トリガー

provider が `workato_genie` の場合:
```json
{
  "provider": "workato_genie",
  "name": "start_workflow",
  "keyword": "trigger",
  "input": {
    "requires_user_confirmation": "false",
    "description": "スキルの説明",
    "parameters_schema_json": "[{\"name\":\"param1\",\"type\":\"string\",...}]",
    "result_schema_json": "[{\"name\":\"response\",\"type\":\"string\",...}]"
  }
}
```

## Custom Action (`__adhoc_http_action`)

コネクタに適切なアクションがない場合、API を直接呼び出す:

```json
{
  "provider": "<connector>",
  "name": "__adhoc_http_action",
  "as": "<任意の参照名>",
  "keyword": "action",
  "input": {
    "mnemonic": "表示名",
    "verb": "get",
    "response_type": "json",
    "path": "api/endpoint",
    "input": {
      "schema": "[{...}]",
      "data": { "param": "#{_dp('...')}" }
    },
    "output": "[{...}]"
  },
  "extended_output_schema": [...],
  "extended_input_schema": [...],
  "visible_config_fields": [...],
  "wizardFinished": true
}
```

- `name` は常に `"__adhoc_http_action"`（全コネクタ共通）
- `input.verb`: HTTP メソッド（`get`, `post`, `put`, `delete`）
- `input.path`: API パス（コネクタの base URI に追加）
- `input.input.schema`: リクエストパラメータスキーマ（JSON文字列）
- `input.input.data`: パラメータ値（datapill 可）
- `input.output`: レスポンススキーマ（JSON文字列）

## Datapill 記法

データ参照は `_dp()` 関数で記述:
```
#{_dp('{"pill_type":"output","provider":"<provider>","line":"<as>","path":["field","nested_field"]}')}
```

- `pill_type`: 通常 `"output"`
- `provider`: 参照元ステップの `provider`
- `line`: 参照元ステップの `as` 値
- `path`: フィールドパス配列。リストの現在アイテムは `{"path_element_type":"current_item"}` を使用

### その他のデータ参照

```ruby
#{_('data.gmail.new_email.subject')}                          # ドット記法
=_('data.gmail.new_email.attachments').pluck('filename').join(', ')  # Ruby式
```

## filter: 条件フィルタ

```json
{
  "conditions": [
    {
      "operand": "contains",
      "lhs": "#{_dp('...')}",
      "rhs": "High",
      "uuid": "..."
    }
  ],
  "operand": "and",
  "type": "compound"
}
```

operand: `contains`, `equals`, `not_equals`, `starts_with`, `ends_with`, `greater_than`, `less_than`, `is_true`, `is_false`, `is_present`, `is_not_present`

## config: コネクション参照

```json
{
  "keyword": "application",
  "provider": "gmail",
  "account_id": {
    "zip_name": "sample1_gmail.connection.json",
    "name": "Sample1 | Gmail",
    "folder": ""
  },
  "skip_validation": false
}
```

`account_id` が `null` の場合はコネクション未設定。

## スキーマ定義（extended_output_schema / parameters_schema_json）

```json
{
  "name": "field_name",
  "type": "string",           // string, number, boolean, object, array
  "label": "表示名",
  "control_type": "text",     // text, number, url, select, multiselect, checkbox
  "optional": false,
  "hint": "入力のヒント",
  "properties": [],           // type=object の場合の子フィールド
  "of": "object",             // type=array の場合の要素型
  "parse_output": "float_conversion"  // 出力パース方法（optional）
}
```

## job_report_schema / job_report_config

レシピ実行レポートのカスタムカラム:
```json
"job_report_schema": [
  { "name": "custom_column_1", "label": "表示名" }
],
"job_report_config": {
  "custom_column_1": "#{_('data.provider.step.field')}"
}
```
