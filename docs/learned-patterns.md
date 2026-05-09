# Learned Patterns（kit canonical）

このファイルは **kit 標準の一時保管バッファ** で、kit メンテナが分類前に置く場所。
**組織の利用者はこのファイルを編集してはならない**（kit submodule の変更になる）。

## 組織側の学習結果は `org/docs/learned-patterns.md` へ

組織のレシピから学習した知見は、すべて **ワークスペースリポジトリ側の `org/docs/`** に書き込む。
詳細な振り分けルールは `@.claude/rules/org-knowledge-overlay.md` を参照。

組織側の分類先:
- レシピ JSON 構造の発見 → `org/docs/learned-patterns.md`（後で適切なファイルに移動）
- ロジック → `org/docs/logic/<topic>.md`
- コネクタ固有のフィールド情報 → `org/docs/connectors/<provider>.md`
- プラットフォーム機能 → `org/docs/platform/<topic>.md`
- デプロイ関連 → `org/docs/patterns/deployment-guide.md`

## kit 側の正規分類先（kit メンテナ向け）

kit に取り込みたい一般的な発見は、kit リポジトリへの PR で以下に分類する:
- レシピ JSON 構造 → `.claude/rules/workato-recipe-format.md`
- ロジック → `docs/logic/` の該当ファイル
- コネクタ固有 → `docs/connectors/<name>.md`
- プラットフォーム機能 → `docs/platform/` の該当ファイル
- デプロイ関連 → `docs/patterns/deployment-guide.md`
