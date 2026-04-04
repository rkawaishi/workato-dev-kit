# Lookup Tables

公式: https://docs.workato.com/en/features/lookup-tables.html

## 概要

クロスリファレンス用のデータストア。レシピから頻繁に参照するデータをテーブル形式で格納し、API コール削減や静的データのキャッシュに使用する。

## 主な用途

- 単位変換（メートル ↔ フィート等）
- ビジネスデータの参照キャッシュ
- 遅い API のデータキャッシュ
- 郵便番号 → 都市名のマッピング

## 制限

| 項目 | 上限 |
|---|---|
| ワークスペースあたりのテーブル数 | 100 |
| テーブルあたりのカラム数 | 10 |
| テーブルあたりの行数 | 100,000 |
| 行サイズ | 128 KB |
| セルあたりのデータ | 10 KB |
| バッチ操作サイズ | 10,000 |
| CSV エクスポート | 50,000 行超はエクスポート不可 |
| Get all entries | 最大 10,000 件まで |

## Actions (9種)

| 名前 | 説明 |
|---|---|
| Add entry | エントリ作成 |
| Add entries (batch) | 複数エントリ一括作成 |
| Lookup entry | カラム値でエントリ検索（最初の一致を返す） |
| Search entries (batch) | 条件に合う全エントリ検索 |
| Get all entries (batch) | 全エントリ取得（最大 10,000 件） |
| Update entry | エントリ更新 |
| Delete entry | エントリ削除 |
| Delete multiple entries (batch) | 複数エントリ一括削除 |
| Truncate table | テーブルの全エントリ削除 |

## フォーミュラでの lookup

```ruby
lookup("TABLE_NAME", "COLUMN": value)["RETURN_COLUMN"]
```

Search entries の出力を使ったインメモリ lookup で、繰り返し検索を高速化できる。

## Data Tables との違い

| | Lookup Tables | Data Tables |
|---|---|---|
| 用途 | 参照・マッピングデータ | アプリのデータストア |
| カラム数上限 | 10 | 制限緩い |
| 行数上限 | 100,000 | スケーラブル |
| トリガー | なし | 4種（real-time/batch） |
| Workflow Apps 連携 | なし | あり |
