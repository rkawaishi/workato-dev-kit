# SQL Server コネクタ

公式: https://docs.workato.com/en/connectors/mssql/introduction.html

## Triggers

| 名前 | 説明 |
|---|---|
| New row | テーブル内の新しく挿入された行をインクリメンタルユニークキーに基づいて検出・処理する |
| New/updated row | ユニークキーとソートカラムを使用して、新しい行と既存行の変更の両方を検出する |
| Scheduled query | 定義されたスケジュールでクエリを実行し、データベースの変更を監視する |

## Actions

| 名前 | 説明 |
|---|---|
| Select | カスタマイズ可能なフィルタ条件を使用してテーブルまたはビューから行を取得する |
| Insert | 指定されたカラム値でテーブルに新しい行を追加する |
| Update | WHERE句の条件に基づいて既存の行を変更する |
| Upsert | 行の存在に応じて挿入または更新操作を実行する |
| Delete | 指定されたWHERE条件に一致する行を削除する |
| Run custom SQL | 複雑なデータベース操作のために任意のSQL文を実行する |
| Execute stored procedure | パラメータサポート付きで事前定義されたストアドプロシージャを呼び出す |
