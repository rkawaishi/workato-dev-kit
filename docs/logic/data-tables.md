# Data Tables

公式: https://docs.workato.com/en/data-tables.html
コネクタ: https://docs.workato.com/en/data-tables/data-table-connector.html

## 概要

Workato 内蔵のデータストア。スプレッドシートのようなインターフェースでデータを管理し、レシピから読み書きできる。外部 API やデータベースに依存せずにデータを保持する。

## 主な用途

- サードパーティ API のレスポンスキャッシュ
- 遅い API のデータストア
- Workflow App のデータ基盤（単一または複数テーブルのリンク）

## 非推奨の用途

- リレーショナルデータベースの代替
- 大量データの単一セル格納
- PCI 機密データ（クレジットカード番号等）の格納

## 構成要素

| 用語 | 説明 |
|---|---|
| **Record** | テーブルの1行。自動生成の Record ID で一意に識別 |
| **Column** | テーブルのフィールド（列）。自動生成の Column ID を持つ |
| **Record ID** | 更新・削除操作に必要な一意識別子 |
| **Column ID** | 列名の変更に耐性のある内部識別子 |

## カラム型

- 標準的なデータ型（string, number, boolean, date 等）
- **Long text**: 1セルあたり最大 10,000 文字

## Triggers (4種)

| 名前 | 説明 |
|---|---|
| New record (real-time) | 新規レコード作成時（リアルタイム） |
| New records (batch) | 新規レコードのバッチ検出 |
| New/updated record (real-time) | 新規/更新レコード（リアルタイム） |
| New/updated records (batch) | 新規/更新レコードのバッチ検出 |

## Actions (10種)

| 名前 | 説明 |
|---|---|
| Create record | レコード作成 |
| Create records (batch) | 複数レコード一括作成 |
| Update record | レコード更新 |
| Update records (batch) | 複数レコード一括更新 |
| Upsert record | レコードの作成または更新（マッチング条件ベース） |
| Delete record | レコード削除 |
| Delete records (batch) | 複数レコード一括削除 |
| Remove values from a record | レコードの特定フィールド値をクリア |
| Search records (batch) | 条件に合うレコードを検索 |
| Truncate table (batch) | テーブルの全レコード削除 |

## フォーミュラでの lookup

レシピのフォーミュラモードから Data Table のレコードを直接参照できる。

公式: https://docs.workato.com/en/formulas/other-formulas.html#data-table-lookup

## 備考

- スケーラブルかつセキュア、メンテナンス不要
- UI からテーブルの作成・カラム変更が可能
- レシピからは Data Tables コネクタ経由でアクセス
- Column ID を使うことでカラム名変更時もレシピが壊れない
