---
description: レシピ JSON を分析して新しいパターンを docs/known-patterns.md に蓄積する。スキル改善のための知識ベースを更新。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /learn-recipe

レシピ JSON を分析し、パターン知識を蓄積・更新するスキル。

## 使い方

- `/learn-recipe <file-path>` — 特定のレシピを分析
- `/learn-recipe <project-name>` — プロジェクト内の全レシピを分析
- `/learn-recipe` — 全プロジェクトの全レシピを分析

## 分析対象

### 1. プロバイダーとアクション

各レシピから以下を抽出:
- `provider` 名（コネクタ）
- `name`（アクション/トリガー名）
- `keyword`（trigger/action/foreach）
- この組み合わせで「どのアプリで何ができるか」を蓄積

### 2. datapill パターン

- `_dp()` の使用パターン
- `_()` ドット記法の使用パターン
- Ruby 式（`=_(...).method()`）の使用パターン
- 新しい記法があれば記録

### 3. レシピ構成パターン

- トリガー → アクションのフロー構成
- foreach ループの使い方
- filter 条件の書き方
- error handling の構造
- Genie ワークフローの構成

### 4. スキーマパターン

- `extended_output_schema` のフィールド定義パターン
- `parameters_schema_json` の型と control_type の組み合わせ
- よく使われるフィールド名

### 5. 命名規則

- ファイル名の命名パターン
- コネクション名の命名パターン（`prefix | Provider`）
- ステップの `as` フィールドの値パターン

## 更新先

分析結果を適切なファイルに振り分ける:

| 知見の種類 | 更新先 |
|---|---|
| 新しいコネクタ/トリガー/アクション | `docs/connectors/<connector>.md`（なければ新規作成） |
| ロジックパターンの新知見 | `docs/logic/` の該当ファイル |
| 公式に載っていない JSON 構造の独自知見 | `docs/learned-patterns.md` |
| フォーマット定義の修正 | `.claude/rules/` の該当ファイル |

### 更新ルール

- 公式ドキュメントで確認できる情報は `docs/connectors/` へ
- 公式に載っていない独自知見のみ `docs/learned-patterns.md` へ
- 既存の情報と重複する場合は追記しない
- 発見元のレシピ名を出典として記録

## 出力

分析完了後、以下を報告:
- 分析したファイル数
- 新たに発見したパターン（あれば）
- 更新した知識ベースのセクション
- ルールファイルの更新提案（あれば）
