# Snowflake コネクタ

公式: https://docs.workato.com/en/connectors/snowflake.html
Provider: `snowflake`

## Triggers
| 名前 | 説明 |
|---|---|
| New row | フィルタ条件に基づく新規行の検出 |
| New/updated row | 新規/更新行の検出 |
| New rows (batch) | 新規行のバッチ取得 |
| New/updated rows (batch) | 新規/更新行のバッチ取得 |

## Actions
| 名前 | 説明 |
|---|---|
| Select rows | WHERE 条件でクエリ |
| Insert row | 行の挿入 |
| Insert rows (batch) | 行の一括挿入 |
| Update rows | 行の更新 |
| Delete rows | 行の削除 |
| Run custom SQL | カスタム SQL 実行 |

## 備考
- SELECT, INSERT, UPDATE, DELETE 操作対応
- バッチ処理: 1〜100行/バッチ
- WHERE 条件のサポート
- ウェアハウスの自動サスペンド/リジュームに注意
