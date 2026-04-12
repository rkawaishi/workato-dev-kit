# Recipe Function 分離 (Recipe Function Separation)

## いつ使うか

| 条件 | 該当 |
|---|---|
| 同じロジックを複数のレシピで使う | Yes |
| レシピが長く複雑になっている | Yes |
| ブロッキングアクションを含むレシピを構造化したい | Yes |
| テスト・デバッグを容易にしたい | Optional |

## 基本原則

### Function に切り出すべきもの

```
[メインレシピ]
    ├── [Function] データ取得（マネージャー検索、部署取得等）
    ├── [Function] データ変換・バリデーション
    ├── [Function] 外部システム連携（チケット作成、通知送信等）
    └── [インライン] ブロッキングアクション（human_review 等）
```

### Function に入れてはいけないもの

- **`human_review` 系アクション**: ブロッキング（レシピを一時停止して人間の操作を待つ）が Function 内では動作しない
- **トリガー依存のアクション**: `complete_task` 等、特定のトリガーコンテキストに依存するアクション

## 分離判断フローチャート

```
そのロジックは...

├── ブロッキングアクションを含む？
│   ├── Yes → メインレシピにインラインで配置
│   └── No ↓
│
├── 複数レシピで再利用する？
│   ├── Yes → Recipe Function（Shared プロジェクト）
│   └── No ↓
│
├── 10ステップ以上の独立したロジック？
│   ├── Yes → Recipe Function（同一プロジェクト内）
│   └── No → メインレシピにインラインで配置
```

## よくある分離パターン

### パターン 1: データ取得 Function

```
fnc_get_<entity>
  入力: 検索キー（email, ID 等）— 1〜2 パラメータ
  処理: 外部システムから検索
  出力: 必要なフィールドのみ返す
```

例:
- `fnc_get_line_manager` — メールアドレスからマネージャー情報を取得
- `fnc_get_department` — 社員 ID から部署情報を取得

### パターン 2: 後続処理 Function

```
fnc_process_<event>_result
  入力: 処理に必要な全コンテキスト
  処理: 外部システム連携 + 通知 + ステータス更新
  出力: 処理結果（作成された ID 等）
```

例:
- `fnc_process_approval_result` — 承認結果に応じて Jira チケット作成 + 通知
- `fnc_process_onboarding_setup` — アカウント作成 + 権限設定

### パターン 3: 通知 Function

```
fnc_send_<channel>_notification
  入力: channel, message, 追加パラメータ
  処理: メッセージ整形 + 送信
  出力: 送信結果（ok, timestamp 等）
```

例:
- `fnc_send_slack_notification` — Slack チャンネルに通知
- `fnc_send_error_notification` — エラー情報を構造化して通知

## インターフェース設計のガイドライン

| 原則 | 説明 |
|---|---|
| 入力は最小限 | 1〜3 パラメータが理想。多すぎる場合はロジックの責務が大きすぎる |
| 出力は明確 | 呼び出し元が必要とするフィールドを全て `result_schema_json` で定義 |
| エラーを返す | Function 内で try/catch し、`error` フィールドで報告。呼び出し元でハンドリング |
| 副作用を明示 | 外部システムにレコードを作成する場合は命名で明示（`fnc_create_*`） |

## 命名規則

```
fnc_<動詞>_<名詞>.recipe.json
```

| パターン | 例 | 用途 |
|---|---|---|
| `fnc_get_*` | `fnc_get_line_manager` | データ取得（読み取り専用） |
| `fnc_send_*` | `fnc_send_slack_notification` | 通知送信 |
| `fnc_validate_*` | `fnc_validate_budget` | バリデーション |
| `fnc_create_*` | `fnc_create_jira_ticket` | 外部レコード作成 |
| `fnc_update_*` | `fnc_update_employee_status` | 外部レコード更新 |
| `fnc_process_*` | `fnc_process_approval_result` | 複合処理（複数アクション） |

## 既知の注意点

- **ブロッキング制約**: `human_review_on_existing_record` や `wait_for_event` は Recipe Function 内で動作しない。必ずメインレシピに配置する
- **循環呼び出し禁止**: Function A → Function B → Function A のような循環は実行時エラーになる
- **入出力の変更影響**: 共有 Function の入出力スキーマを変更すると、全呼び出し元に影響する。互換性を確認してから変更する
- **デバッグ**: Function 内のジョブログはメインレシピとは別に記録される。エラー追跡時は両方のジョブログを確認する
- **Shared vs ローカル**: 組織横断で使う Function は `Shared` プロジェクトに、プロジェクト固有の Function は同一プロジェクト内に配置する

## 参照

- `docs/patterns/shared-assets.md` — 共有アセットの設計パターン・命名規則
- `docs/patterns/recipe-patterns/approval-workflow.md` — ブロッキングアクション配置の実例
- `docs/logic/error-handling.md` — Function 内のエラーハンドリング
