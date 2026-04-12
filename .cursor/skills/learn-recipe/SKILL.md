---
name: learn-recipe
description: レシピ JSON を分析してフィールド情報やパターン知識を適切なドキュメントに直接追記する。pull したレシピから学習し、ナレッジベースを拡充する。
---

# /learn-recipe

レシピ JSON を分析し、発見した知見を **適切なドキュメントに直接追記** するスキル。
中間ファイルへの蓄積ではなく、各ドキュメントを直接拡充する。

## 使い方

- `/learn-recipe <file-path>` — 特定のレシピを分析
- `/learn-recipe <project-name>` — プロジェクト内の全レシピを分析
- `/learn-recipe` — 全プロジェクトの全レシピを分析

## 分析対象と追記先

### 1. フィールド情報（最重要）

各ステップから input/output フィールドスキーマを抽出する。

抽出元:
- `extended_output_schema` — アクション/トリガーの出力フィールド
- `extended_input_schema` — アクション/トリガーの入力フィールド
- `input` — 実際の入力値（datapill 参照含む）
- `parameters_schema_json` — Genie/Function のパラメータ（JSON 文字列）
- `result_schema_json` — Genie/Function の結果（JSON 文字列）
- `input.input.schema` — Custom Action のリクエストスキーマ
- `input.output` — Custom Action のレスポンススキーマ

**追記先**: `docs/connectors/<provider>.md` の該当アクション/トリガーセクション

フォーマット:
```markdown
### <action_name>

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| field_name | type | Yes/- | label |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| field_name | type | label |
| parent.child | type | label (nested) |
```

### 2. 新しいプロバイダー/アクション

レシピ内で未知の provider/name の組み合わせを発見した場合。

**追記先**:
- Pre-built コネクタ → `docs/connectors/<provider>.md` のトリガー/アクション一覧テーブル
- Workato 内部プロバイダー → `docs/platform/workflow-apps.md` または `docs/platform/agent-studio.md`

### 3. JSON 構造の知見

レシピ JSON の構造に関する新しい発見（新しい keyword、未知のフィールド、特殊な構造等）。

**追記先**:
- レシピ構造全般 → `.claude/rules/workato-recipe-format.md`
- Genie/MCP/Skill 構造 → `.claude/rules/workato-agentic-format.md`
- ロジック（if/loop/error）→ `docs/logic/` の該当ファイル

### 4. datapill パターン

新しい datapill 記法や参照パターンの発見。

**追記先**: `docs/logic/data-pills.md`

### 5. デプロイ関連の知見

push/pull 時の挙動に関する新発見（フィールドリセット、スキーマ展開、バージョン変更等）。

**追記先**: `docs/patterns/deployment-guide.md`

### 6. 分類が不明な知見

上記のどこにも当てはまらない新発見。

**追記先**: `docs/learned-patterns.md`（一時保管。後で適切なファイルに移動する）

## 分析手順

1. 対象レシピの `.recipe.json` を読み込む
2. 全ステップを再帰的に走査
3. 各ステップについて:
   a. `provider` と `name` が既知か確認（`docs/connectors/<provider>.md` を参照）
   b. `extended_output_schema` / `extended_input_schema` があればフィールド情報を抽出
   c. 新しい構造パターンがあれば記録
4. 追記先ファイルを読み、既存内容と重複しないか確認
5. 新しい知見のみ追記

## 重複チェック

追記前に必ず対象ファイルを Grep で検索し、同じ内容が既にないか確認する。
- 同じアクション名のフィールド情報がある → 新しいフィールドのみ追加
- 同じルールが既にある → スキップ

## 出力

分析完了後、以下を報告:
- 分析したファイル数
- 追記したドキュメント一覧と追記内容のサマリー
- 新たに発見したパターン（あれば）
