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

## フィールド詳細

### search_sobjects (Action)

レシピ: Search Contracts in Salesforce

入力・出力スキーマは未設定（コネクション後に動的に決定される）。

> **Note:** このステップは `input: {}` で空のため、Salesforce コネクション設定後にオブジェクト種別とフィールドが動的に生成されます。

---

### update_sobject (Action)

レシピ: Update Contract in Salesforce

入力・出力スキーマは未設定（コネクション後に動的に決定される）。

> **Note:** このステップは `input: {}` で空のため、Salesforce コネクション設定後にオブジェクト種別とフィールドが動的に生成されます。

#### 関連する Genie パラメータ（start_workflow トリガー）

Search Contracts レシピ:

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| contract_name | string | Yes | the name of the contract which user is referencing |
| contract_content | string | Yes | contents of the contract which user is referencing |

Update Contract レシピ:

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| contract_name | string | Yes | Contract name |
| contract_content | string | - | Contract content |

#### Genie Result Schema

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| response | string | Yes | Response |

## 備考
- Salesforce の全エディション対応
- ユーザーの権限に基づいてアクセス可能なオブジェクト/フィールドが決まる
- provider 名: `salesforce`
