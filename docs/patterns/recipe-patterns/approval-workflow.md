# 承認ワークフロー (Approval Workflow)

## いつ使うか

| 条件 | 該当 |
|---|---|
| ユーザーがフォーム等で申請を送信する | Yes |
| 別の人間が承認/却下を判断する | Yes |
| 承認結果で後続処理が分岐する | Yes |
| Slack ボタンで承認操作をしたい | Optional |
| Workflow App でステージ管理をする | Optional |

## レシピ構成図

```
--- メインレシピ ---
[トリガー] New request (Workflow App / Webhook / etc.)
    │
    ├── [Function] 承認者を特定（例: マネージャー取得）
    ├── [Action] 承認依頼通知（Slack DM ボタン付き / Email）
    ├── [Action] human_review_on_existing_record（ブロッキング — 承認待ち）
    │
    ├── [IF] 承認（is_approved == true）
    │   ├── [Action] 外部システム連携（Jira チケット作成 etc.）
    │   ├── [Action] ステージ変更 → 完了
    │   └── [Action] 完了通知
    │
    └── [ELSE] 却下
        ├── [Action] ステージ変更 → キャンセル
        └── [Action] 却下通知

--- Slack ボタンハンドラ（別レシピ） ---
[トリガー] bot_command_v2（Slack ボタンクリック）
    ├── [IF] approve → complete_task (Approved)
    └── [ELSE] → complete_task (Rejected)

--- Recipe Function（別レシピ） ---
[Function] 承認者取得
    入力: employee_email
    出力: manager_name, manager_email
```

## ステップ構成

### メインレシピ

| # | Provider | Action | 目的 |
|---|---|---|---|
| 0 | workato_workflow_task | new_requests_realtime | フォーム送信で起動 |
| 1 | workato_recipe_function | call_recipe | 承認者を特定（Function 呼び出し） |
| 2 | slack_bot | post_bot_message | 承認依頼通知（ボタン付き） |
| 3 | workato_workflow_task | human_review_on_existing_record | 承認待ち（ブロッキング） |
| 4 | (if/else) | | 承認/却下の分岐 |
| 5+ | 外部サービス | 各種アクション | 承認後の後続処理 |
| 6 | workato_workflow_task | change_workflow_stage | ステージ変更 |

### Slack ボタンハンドラ

| # | Provider | Action | 目的 |
|---|---|---|---|
| 0 | slack_bot | bot_command_v2 | ボタンクリックで起動 |
| 1 | (if/else) | | approve/reject の判定 |
| 2 | workato_workflow_task | complete_task | タスク完了（Approved/Rejected） |

## 設計判断ポイント

| 判断 | 推奨 | 理由 |
|---|---|---|
| `human_review` の配置 | メインレシピ内 | ブロッキングアクションは Recipe Function 内に置けない |
| Slack ボタンハンドラ | 別レシピ | `bot_command_v2` トリガーは独立レシピが必要 |
| 承認者の取得 | Recipe Function | 複数プロジェクトで再利用可能 |
| 承認後の分岐 | if/else | `human_review` の `is_approved` フラグで判定 |
| 後続処理（Jira 等） | Recipe Function or インライン | 再利用性に応じて判断（→ recipe-function-separation パターン参照） |
| Slack 通知のボタン | `attachment_buttons` | `record_id` をパラメータに含めて `complete_task` と紐付ける |

## Slack ボタンの構成

承認依頼メッセージにボタンを付ける場合:

```json
"attachment_buttons": [
  {
    "title": "Approve",
    "bot_command": "<domain> approve <resource>",
    "params": "result: approve record_id: #{_dp(...)}"
  },
  {
    "title": "Reject",
    "bot_command": "<domain> reject <resource>",
    "params": "result: reject record_id: #{_dp(...)}"
  }
]
```

- `bot_command` の `domain` と `name` はハンドラレシピのトリガー設定と一致させる
- `params` に `record_id` を渡し、`complete_task` でどのタスクを完了するか特定する

## 既知の注意点

- `human_review_on_existing_record` は **Recipe Function 内に配置不可**（ブロッキングが効かない）
- Slack ボタンの `complete_task` には `app_id` と `record_id` が必要 — ボタンの `params` に record_id を渡す
- `bot_command_v2` の `domain` と `name` でボタンを識別する — プロジェクト間で一意に設定すること
- ステージ変更は承認/却下の **両方のパス** で行い、最終状態を明確にする
- `human_review` に `due_in_days` を設定して承認期限を設ける（デフォルト推奨: 7日）
- `reassignable: true` を設定すると、承認者が別の人に委任できる

## 参照

- `docs/patterns/shared-assets.md` — Recipe Function の設計ガイドライン
- `docs/patterns/recipe-function-separation.md` — ブロッキングアクションの扱い
