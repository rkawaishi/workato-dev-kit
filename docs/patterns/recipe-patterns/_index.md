# レシピ構築デザインパターン（kit canonical）

レシピの構築でよく使われるパターンのカタログ。
`/create-recipe` や `/design` が新規レシピ生成時に参照する。

このファイルは **kit canonical** で、kit メンテナのみが更新する（read-only）。
組織が学習した汎用パターンは `org/docs/patterns/recipe-patterns/_index.md` に蓄積され、
`/create-recipe` や `/design` は両方を併読する（`@.claude/rules/org-knowledge-overlay.md` 参照）。

## パターン一覧

| パターン名 | ファイル | 適用場面 |
|---|---|---|
| ページネーションループ | pagination-loop.md | API の全件取得（オフセット / トークン方式） |

## パターンの使い方

- `/learn-pattern` — エキスパートがパターンを記録・更新（書き込み先は `org/docs/patterns/recipe-patterns/` または `projects/docs/patterns/`）
- `/create-recipe` — ステップ構成の設計時にパターンを適用
- `/design new` — ユーザー体験ヒアリング後に該当パターンを提案
