# Salesforce コネクタ

公式: https://docs.workato.com/en/connectors/salesforce.html

## 認証
- OAuth 2.0 または JWT bearer
- Platform events を使用する場合は Salesforce 側で有効化が必要

## 主な機能カテゴリ

### Triggers
- 新規/更新レコード（ポーリング）
- 新規/更新レコード（リアルタイム — Salesforce Workflow rules 使用）
- Platform event トリガー
- バッチトリガー

### Actions
- レコードの CRUD（Create, Read, Update, Delete）
- SOQL クエリ検索 (`search_sobjects`)
- レコード更新 (`update_sobject`)
- バルク操作
- Platform event の発行

## 対応オブジェクト
- 標準オブジェクト（Account, Contact, Lead, Opportunity 等）
- カスタムオブジェクト
- フィールドレベルの権限に基づくアクセス制御

## 備考
- Salesforce の全エディション対応
- ユーザーの権限に基づいてアクセス可能なオブジェクト/フィールドが決まる
- provider 名: `salesforce`
