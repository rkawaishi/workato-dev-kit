---
description: レシピ JSON を分析してコネクタのフィールド情報やパターン知識を蓄積する。pull したレシピから input/output フィールドを抽出し docs/connectors/ に反映。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /learn-recipe

レシピ JSON を分析し、コネクタのフィールド情報とパターン知識を蓄積・更新するスキル。

## 使い方

- `/learn-recipe <file-path>` — 特定のレシピを分析
- `/learn-recipe <project-name>` — プロジェクト内の全レシピを分析
- `/learn-recipe` — 全プロジェクトの全レシピを分析

## 分析対象

### 1. フィールド情報の抽出（最重要）

各ステップから input/output フィールドスキーマを抽出する。

#### 抽出元フィールド

| JSON フィールド | 内容 |
|---|---|
| `extended_output_schema` | アクション/トリガーの出力フィールド定義（配列） |
| `extended_input_schema` | アクション/トリガーの入力フィールド定義（配列） |
| `input` | 実際に設定された入力値（datapill 参照を含む） |
| `input.parameters_schema_json` | Genie スキルのパラメータスキーマ（JSON 文字列） |
| `input.result_schema_json` | Genie スキルの結果スキーマ（JSON 文字列） |
| `input.input.schema` | Custom Action のリクエストパラメータスキーマ（JSON 文字列） |
| `input.output` | Custom Action のレスポンススキーマ（JSON 文字列） |

#### 抽出するフィールド情報

各フィールドから以下を抽出:
```json
{
  "name": "フィールド名",
  "type": "string|number|boolean|object|array|integer",
  "label": "表示名",
  "control_type": "text|number|select|checkbox|...",
  "optional": true/false,
  "properties": [...],  // type=object の場合の子フィールド
  "of": "object"         // type=array の場合の要素型
}
```

#### コネクタドキュメントへの反映フォーマット

`docs/connectors/<provider>.md` の該当アクション/トリガーの下にフィールド情報を追記:

```markdown
## Actions

| 名前 | 説明 |
|---|---|
| search_issues | JQL でチケット検索 |

### search_issues

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| Description | string | - | 検索キーワード |
| Key | string | - | チケットキー |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| issues | array of object | 検索結果のチケット一覧 |
| issues[].id | string | チケット ID |
| issues[].key | string | チケットキー（例: PROJ-123） |
| issues[].fields.summary | string | チケットのサマリー |
| issues[].fields.description | string | チケットの説明 |
| issues[].fields.status.name | string | ステータス名 |
| issues[].fields.priority.name | string | 優先度名 |
| issues[].fields.comment | object | コメント情報 |
```

ネストされたオブジェクトは `parent.child` 形式でフラット化して記載する。
`properties` を再帰的に展開し、datapill の `path` 指定に直接使える形式にする。

### 2. プロバイダーとアクション

各レシピから以下を抽出:
- `provider` 名（コネクタ）
- `name`（アクション/トリガー名）
- `keyword`（trigger/action/foreach）
- コネクタドキュメントに未登録のアクション/トリガーがあれば追加

### 3. datapill パターン

- `_dp()` の使用パターン
- `_()` ドット記法の使用パターン
- Ruby 式（`=_(...).method()`）の使用パターン
- 新しい記法があれば `docs/learned-patterns.md` に記録

### 4. レシピ構成パターン

- トリガー → アクションのフロー構成
- foreach ループの使い方
- filter 条件の書き方
- error handling の構造
- Genie ワークフローの構成

### 5. 命名規則

- ファイル名の命名パターン
- コネクション名の命名パターン（`prefix | Provider`）
- ステップの `as` フィールドの値パターン

## 更新先

分析結果を適切なファイルに振り分ける:

| 知見の種類 | 更新先 |
|---|---|
| **フィールド情報（input/output）** | `docs/connectors/<provider>.md` の該当アクションセクション |
| 新しいコネクタ/トリガー/アクション | `docs/connectors/<connector>.md`（なければ新規作成） |
| ロジックパターンの新知見 | `docs/logic/` の該当ファイル |
| 公式に載っていない JSON 構造の独自知見 | `docs/learned-patterns.md` |
| フォーマット定義の修正 | `.claude/rules/` の該当ファイル |

### 更新ルール

- フィールド情報は既存の一覧テーブルの下にサブセクションとして追記
- 同じアクションのフィールド情報が既にある場合、新しいフィールドのみ追加
- `extended_output_schema` / `extended_input_schema` が null や空の場合はスキップ
- JSON 文字列として格納されているスキーマ（`parameters_schema_json` 等）はパースして展開
- 発見元のレシピ名を出典として記録

## 出力

分析完了後、以下を報告:
- 分析したファイル数
- 抽出したフィールド情報の件数（コネクタ × アクション）
- 更新したコネクタドキュメント一覧
- 新たに発見したパターン（あれば）
