# Jira コネクタ

公式: https://docs.workato.com/en/connectors/jira.html

## Triggers (11種)

| 名前 | provider 内名称 | 説明 |
|---|---|---|
| New issue | `new_issue` | 新規チケット（ポーリング） |
| New issue (batch) | — | 新規チケット（バッチ取得） |
| Updated issue | — | 更新チケット（ポーリング） |
| Updated issue (batch) | — | 更新チケット（バッチ取得） |
| New/updated issue (real-time) | — | 新規/更新チケット（リアルタイム、Webhook 必要） |
| New/updated comment (real-time) | — | 新規/更新コメント（リアルタイム） |
| New/updated worklog (real-time) | — | 新規/更新ワークログ（リアルタイム） |
| New event (real-time) | — | 新規イベント（リアルタイム） |
| Deleted object (real-time) | — | オブジェクト削除（リアルタイム） |
| Export new issues | — | 新規チケット（スケジュール取得） |
| Export new/updated issues | — | 新規/更新チケット（スケジュール取得） |

## Actions (17種)

| 名前 | provider 内名称 | 説明 |
|---|---|---|
| Create issue | — | チケット作成 |
| Update issue | — | チケット更新 |
| Update issue status | — | チケットのステータス変更 |
| Get issue | — | チケット取得 |
| Get changelog of an issue | — | チケットの変更履歴取得 |
| Get issue schema | — | フィールドスキーマ取得 |
| Search issues (batch) | `search_issues` | 条件一致チケット検索 |
| Search issues by JQL (batch) | — | JQL クエリでチケット検索 |
| Create comment | — | コメント作成 |
| Update comment | — | コメント更新 |
| Get issue comments (batch) | — | チケットのコメント一覧取得 |
| Create user | — | ユーザー作成 |
| Get user details | — | ユーザー詳細取得 |
| Search assignable users (batch) | — | アサイン可能ユーザー検索 |
| Assign user to issue | — | チケットにユーザーをアサイン |
| Upload attachment | — | 添付ファイルアップロード |
| Download attachment | — | 添付ファイルダウンロード |

## 備考
- リアルタイムトリガーには Jira 側の Webhook 登録が必要
- `search_issues` は UI 上で検索フィールドを指定する形式（JQL 直接入力は `Search issues by JQL` を使用）
