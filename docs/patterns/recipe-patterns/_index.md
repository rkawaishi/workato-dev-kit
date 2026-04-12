# レシピ構築デザインパターン

レシピの構築でよく使われるパターンのカタログ。
`/create-recipe` や `/design` が新規レシピ生成時に参照する。

## パターン一覧

| パターン名 | ファイル | 適用場面 |
|---|---|---|
| 承認ワークフロー | approval-workflow.md | フォーム申請 → 人間の承認 → 後続処理 |
| データ同期 | data-sync.md | トリガー → 検索 → upsert（作成 or 更新） |
| エラー通知 | error-notification.md | Monitor/Error → Slack/Email 通知 |
| Recipe Function 分離 | recipe-function-separation.md | ブロッキングアクションの分離・ロジック切り出し |

## パターンの使い方

- `/design new` — ユーザー体験ヒアリング後に該当パターンを提案
- `/create-recipe` — パターンをテンプレートとしてレシピ構造を生成
- `/learn-pattern` — 完成レシピから新しいパターンを抽出・登録
