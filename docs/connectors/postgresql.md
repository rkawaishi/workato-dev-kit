# PostgreSQL コネクタ

公式: https://docs.workato.com/en/connectors/postgresql.html

## Triggers
| 名前 | 説明 |
|---|---|
| New row | テーブルまたはビューに挿入された行を個別ジョブとして処理する |
| New batch of rows | テーブルまたはビューに挿入された行をバッチで処理する |
| New/updated row | 新規作成または変更された行を検出する |

## Actions
| 名前 | 説明 |
|---|---|
| Select rows | WHERE条件に基づいてテーブルから行を取得する |
| Insert row | テーブルに新しい行を挿入する |
| Upsert row | 行の挿入または既存行の更新を行う |
| Delete rows | WHERE条件に一致する行を削除する |
| Run custom SQL | カスタムSQLクエリを直接実行する |
