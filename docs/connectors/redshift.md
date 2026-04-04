# Redshift コネクタ

公式: https://docs.workato.com/en/connectors/redshift.html

## Triggers
| 名前 | 説明 |
|---|---|
| New row | 選択したテーブルまたはビューに挿入された行を検知する |
| New batch of rows | 選択したテーブルまたはビューに挿入された行をバッチとして検知する |
| New batch of rows via custom SQL | カスタムSQLに一致する挿入された行をバッチとして検知する |
| New/updated row | テーブル内で新規作成または更新された行を検知する |

## Actions
| 名前 | 説明 |
|---|---|
| Select rows | WHERE条件で指定した基準に基づいて行を取得する |
| Select rows using custom SQL | カスタムSQLクエリに基づいて行を取得する |
| Insert row | 選択したテーブルに1行を挿入する |
| Insert batch of rows | 複数行を一括で挿入する |
| Update rows | WHERE条件で指定した行を更新する |
| Update batch of rows | 複数行を一括で更新する |
| Upsert row | ユニークキーに基づいて行を挿入または更新する |
| Upsert batch of rows | 複数行を一括でアップサートする |
| Delete rows | WHERE条件で指定した基準に基づいて行を削除する |
