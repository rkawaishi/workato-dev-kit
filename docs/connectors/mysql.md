# MySQL コネクタ

公式: https://docs.workato.com/en/connectors/mysql.html

## Triggers
| 名前 | 説明 |
|---|---|
| New row | 指定テーブルに新しい行が挿入されたときに検知する（各行が個別ジョブとして処理） |
| New batch of rows | 指定テーブルに挿入された新しい行をバッチとして検知する |
| New/updated row | 新規作成および更新された行を検知する |
| Scheduled query | スケジュールに基づいてクエリを実行するトリガー |

## Actions
| 名前 | 説明 |
|---|---|
| Select rows | WHERE条件で行を選択・取得する |
| Insert rows | テーブルに新しいレコードを追加する |
| Delete rows | 指定条件に基づいてテーブルから行を削除する |
