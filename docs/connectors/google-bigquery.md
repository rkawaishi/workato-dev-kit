# Google BigQuery コネクタ

公式: https://docs.workato.com/en/connectors/bigquery.html

## Triggers
| 名前 | 説明 |
|---|---|
| New row | 指定テーブルから行を1件ずつ処理する |
| Batch trigger | テーブルから複数の行をバッチで処理する |
| Scheduled query trigger | スケジュールに基づいてクエリを実行する |

## Actions
| 名前 | 説明 |
|---|---|
| Insert row | BigQueryテーブルに1行を追加する |
| Insert rows | BigQueryテーブルに複数の行をバッチで追加する |
| Select rows | WHERE条件に基づいてフィルタされた行を取得する |
| Select rows using custom SQL | カスタムSQLクエリを使用して行を取得する |
| Delete rows | 指定されたWHERE条件に一致する行を削除する |
| Get query job output | 完了したクエリジョブの結果を取得する |
