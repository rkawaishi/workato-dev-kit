# エラー通知 (Error Notification)

## いつ使うか

| 条件 | 該当 |
|---|---|
| レシピ内のアクションが失敗する可能性がある | Yes |
| 失敗時に担当者へ通知したい | Yes |
| エラー内容を Slack やメールで送りたい | Yes |
| リトライ後も失敗した場合のみ通知したい | Optional |

## レシピ構成図

### パターン A: インラインエラーハンドリング

レシピ内で直接 try/catch してエラー通知する。

```
[トリガー] 任意のイベント
    │
    └── [Handle Errors]
        ├── Monitor block
        │   ├── [Action] メインの処理 1
        │   ├── [Action] メインの処理 2
        │   └── ...
        │
        └── Error block
            ├── (retry 設定: 回数・間隔)
            ├── [Action] Slack/Email でエラー通知
            └── [Action] Stop job (failed)  ※必要に応じて
```

### パターン B: 集約エラーハンドラ（Recipe Function）

エラー通知ロジックを共通 Function に集約する。

```
[トリガー] 任意のイベント
    │
    └── [Handle Errors]
        ├── Monitor block
        │   └── [Action] メインの処理
        │
        └── Error block
            └── [Function] fnc_send_error_notification
                  入力: recipe_name, step_name, error_message, channel
                  処理: Slack に構造化エラーメッセージを投稿
```

## ステップ構成（パターン A）

| # | Provider | Action | 目的 |
|---|---|---|---|
| 0 | 任意 | 任意のトリガー | レシピ起動 |
| 1 | (try) | | Handle Errors ブロック開始 |
| 1.1 | 外部サービス | メインアクション | 監視対象の処理 |
| 1.2 | (catch) | | Error block 開始 |
| 1.2.1 | slack_bot | post_bot_message | エラー通知 |

## 設計判断ポイント

| 判断 | 選択肢 | 判断基準 |
|---|---|---|
| エラー通知先 | Slack / Email / 両方 | チームの運用に合わせる。即時対応なら Slack、記録なら Email |
| エラーハンドラの配置 | インライン / Recipe Function | 1レシピだけなら inline、複数レシピで共通なら Function |
| リトライ設定 | あり / なし | 外部 API のタイムアウト等、一時的エラーが想定される場合はリトライ |
| 失敗時の動作 | Stop job / 続行 | クリティカルな処理なら Stop、通知だけして続行する場合もある |
| 通知メッセージ | 最小限 / 詳細 | レシピ名・ステップ名・エラーメッセージ・ジョブ URL を含めると調査が早い |

## エラー通知メッセージの構成例

Slack に送るエラー通知に含めると有用な情報:

```
:rotating_light: *レシピエラー*
*レシピ*: <レシピ名>
*ステップ*: <失敗したステップ名>
*エラー*: <エラーメッセージ>
*ジョブ URL*: <Workato のジョブ詳細 URL>
*発生日時*: <タイムスタンプ>
```

## Handle Errors の JSON 構造

```json
{
  "keyword": "try",
  "block": [
    {
      "comment": "Monitor block — 監視対象のアクション",
      "...": "メインの処理ステップ"
    }
  ],
  "on_error": {
    "keyword": "catch",
    "block": [
      {
        "comment": "Error block — エラー時の処理",
        "provider": "slack_bot",
        "name": "post_bot_message",
        "input": { "...": "エラー通知の内容" }
      }
    ]
  }
}
```

## 既知の注意点

- `try` ブロックのリトライ設定は JSON 内の `retry` フィールドで定義される
- Error block 内のアクション自体がエラーになるとジョブ全体が失敗する — 通知アクションは極力シンプルにする
- `Stop job` を使う場合、`failed` と `successful` を使い分ける。エラーを記録したいなら `failed`
- 集約エラーハンドラ（パターン B）を使う場合、Recipe Function 自体が失敗しないよう、Function 内でもエラーハンドリングを入れる
- Workato のジョブ URL は `https://<region>.workato.com/recipes/<recipe_id>/jobs/<job_id>` の形式

## 参照

- `docs/logic/error-handling.md` — Handle Errors / Stop Job の詳細
- `docs/patterns/shared-assets.md` — Recipe Function の設計ガイドライン
